from typing import Any, Dict, List, Optional, Generator
from dify_plugin.entities.tool import ToolInvokeMessage

from .schema import DatabaseSchema


class DatabaseOperations:
    """
    数据库操作类
    
    提供数据库连接管理和操作方法
    """
    
    def __init__(self, tool_instance=None):
        """
        初始化数据库操作类
        
        Args:
            tool_instance: 工具实例，用于创建消息
        """
        self.db = DatabaseSchema()
        self.db.connect()  # 连接数据库（使用环境变量中的配置）
        self.tool = tool_instance
        print("Database connected successfully")
    
    def __del__(self):
        """确保在对象销毁时关闭数据库连接"""
        if hasattr(self, 'db'):
            self.db.disconnect()
            print("Database connection closed")
    
    def check_db_connection(self) -> bool:
        """
        检查数据库连接状态
        
        Returns:
            bool: 连接是否可用
        """
        try:
            # 执行一个简单的查询来测试连接
            self.db.execute_query("SELECT 1")
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def ensure_db_connection(self) -> bool:
        """
        确保数据库连接可用，如果断开则尝试重连
        
        Returns:
            bool: 连接是否可用
        """
        if not self.check_db_connection():
            print("Attempting to reconnect to database...")
            try:
                self.db.disconnect()  # 确保旧连接已关闭
                return self.db.connect()
            except Exception as e:
                print(f"Database reconnection failed: {e}")
                return False
        return True
    
    def execute_db_query(self, query: str, params: tuple = None) -> Any:
        """
        执行数据库查询的包装方法，包含自动重连机制
        
        Args:
            query: SQL查询语句
            params: 查询参数
            
        Returns:
            查询结果
        """
        if self.ensure_db_connection():
            try:
                return self.db.execute_query(query, params)
            except Exception as e:
                print(f"Query execution error: {e}")
                raise
        else:
            raise Exception("Database connection is not available")
    
    def get_database_info(self) -> dict:
        """
        获取数据库基本信息
        
        Returns:
            包含数据库信息的字典
        """
        try:
            info = {
                'connected': self.check_db_connection(),
                'tables': [],
                'version': None
            }
            
            if info['connected']:
                # 获取数据库表列表
                info['tables'] = self.db.list_tables()
                
                # 获取数据库版本
                version_result = self.execute_db_query("SELECT VERSION() as version")
                if version_result:
                    info['version'] = version_result[0].get('version')
                
            return info
            
        except Exception as e:
            print(f"Error getting database info: {e}")
            return {
                'connected': False,
                'error': str(e)
            }
    
    def handle_database_operation(self, parameters: dict[str, Any]) -> Generator[Any, None, None]:
        """
        处理数据库操作请求
        
        支持的操作类型：
        1. 获取数据库信息
           {
               "operation": "database",
               "action": "info"
           }
        
        2. 执行SQL查询
           {
               "operation": "database",
               "action": "query",
               "query": "SELECT * FROM table_name",
               "params": None  # 可选参数
           }
        
        3. 获取表结构
           {
               "operation": "database",
               "action": "schema",
               "table": "table_name"
           }
        
        4. 获取表列表
           {
               "operation": "database",
               "action": "tables"
           }
        
        Args:
            parameters: 操作参数，包含action和其他必要参数
            
        Returns:
            操作结果，直接返回数据结构
        """
        try:
            db_action = parameters.get('action', 'info')
            
            # 获取数据库信息
            if db_action == 'info':
                info = self.get_database_info()
                yield info
                return
            
            # 执行SQL查询
            elif db_action == 'query':
                query = parameters.get('query')
                params = parameters.get('params')
                
                if not query:
                    yield {"error": "SQL query is required"}
                    return
                
                results = self.execute_db_query(query, params)
                yield {"results": results}
                return
            
            # 获取表结构
            elif db_action == 'schema':
                table_name = parameters.get('table')
                if not table_name:
                    yield {"error": "Table name is required"}
                    return
                
                schema = self.db.get_table_schema(table_name)
                yield {"schema": schema}
                return
            
            # 获取表列表
            elif db_action == 'tables':
                tables = self.db.list_tables()
                yield {"tables": tables}
                return
            
            else:
                yield {"error": f"Unknown database action '{db_action}'"}
                
        except Exception as e:
            yield {"error": f"Database operation error: {str(e)}"}