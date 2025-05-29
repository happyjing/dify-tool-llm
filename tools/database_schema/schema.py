from typing import Dict, Any, Optional, List, Type

from .base import DatabaseInterface
from .mysql import MySQLDatabase


class DatabaseSchema:
    """
    数据库模式工具类
    
    提供统一的数据库操作接口，支持多种数据库类型
    """
    
    # 注册的数据库类型
    _db_types = {
        'mysql': MySQLDatabase,
        # 未来可以添加更多数据库类型
        # 'postgresql': PostgreSQLDatabase,
        # 'sqlite': SQLiteDatabase,
    }
    
    def __init__(self):
        """初始化数据库模式工具"""
        self.db_instance = None
        self.db_type = None
    
    def register_db_type(self, db_type: str, db_class: Type[DatabaseInterface]) -> None:
        """
        注册新的数据库类型
        
        Args:
            db_type: 数据库类型名称
            db_class: 数据库实现类
        """
        self._db_types[db_type.lower()] = db_class
    
    def connect(self, db_type: str = 'mysql', config: Optional[Dict[str, Any]] = None) -> bool:
        """
        连接到指定类型的数据库
        
        Args:
            db_type: 数据库类型，默认为'mysql'
            config: 数据库配置信息
            
        Returns:
            连接是否成功
        """
        db_class = self._db_types.get(db_type.lower())
        if not db_class:
            raise ValueError(f"Unsupported database type: {db_type}")
        config1 = {
            'host': '192.168.32.191',
            'port': '9030',
            'user': 'anxiaomei',
            'password': 'Longing86106522.',
            'database': 'anxiaomei',
        }
        self.db_instance = db_class(config=config1)
        self.db_type = db_type.lower()
        return self.db_instance.connect()
    
    def disconnect(self) -> None:
        """关闭数据库连接"""
        if self.db_instance:
            self.db_instance.disconnect()
            self.db_instance = None
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        执行SQL查询
        
        Args:
            query: SQL查询语句
            params: 查询参数
            
        Returns:
            查询结果列表
        """
        self._check_connection()
        return self.db_instance.execute_query(query, params)
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """
        获取表结构信息
        
        Args:
            table_name: 表名
            
        Returns:
            表结构信息
        """
        self._check_connection()
        return self.db_instance.get_table_schema(table_name)
    
    def list_tables(self) -> List[str]:
        """
        获取数据库中所有表名
        
        Returns:
            表名列表
        """
        self._check_connection()
        return self.db_instance.list_tables()
    
    def get_supported_db_types(self) -> List[str]:
        """
        获取支持的数据库类型列表
        
        Returns:
            支持的数据库类型列表
        """
        return list(self._db_types.keys())
    
    def _check_connection(self) -> None:
        """检查数据库连接状态"""
        if not self.db_instance:
            raise Exception("Database not connected. Call connect() first.")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.disconnect()