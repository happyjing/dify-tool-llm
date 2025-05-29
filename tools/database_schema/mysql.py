import os
from typing import Optional, Dict, Any, List
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

from .base import DatabaseInterface


class MySQLDatabase(DatabaseInterface):
    """MySQL数据库实现类"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化MySQL数据库连接
        
        Args:
            config: 数据库配置，如果未提供则从环境变量读取
        """
        load_dotenv()  # 加载.env文件中的环境变量
        
        self.config = config or {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', '3306')),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'database': os.getenv('MYSQL_DATABASE', '')
        }
        # self.config = {
        #     'host': '192.168.32.191',
        #     'port': '9030',
        #     'user': 'anxiaomei',
        #     'password': 'Longing86106522.',
        #     'database': 'anxiaomei',
        # }
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """
        建立MySQL数据库连接
        
        Returns:
            bool: 连接是否成功
        """
        # print('数据库连接数据', self.config)
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
        return False
    
    def disconnect(self) -> None:
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        执行SQL查询
        
        Args:
            query: SQL查询语句
            params: 查询参数
            
        Returns:
            查询结果列表
        """
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    raise Exception("Failed to connect to database")
            
            self.cursor.execute(query, params or ())
            if query.strip().upper().startswith(('SELECT', 'SHOW', 'DESC', 'DESCRIBE')):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return [{"affected_rows": self.cursor.rowcount}]
        
        except Error as e:
            print(f"Error executing query: {e}")
            raise
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """
        获取表结构信息
        
        Args:
            table_name: 表名
            
        Returns:
            表结构信息
            COLUMN_NAME as name,
                DATA_TYPE as type,
                IS_NULLABLE as nullable,
                COLUMN_KEY as 'key',
                COLUMN_DEFAULT as default_value,
                EXTRA as extra,
                COLUMN_COMMENT as comment
        """
        query = """
            SELECT 
                DATA_TYPE as type,
                COLUMN_NAME as name,
                COLUMN_COMMENT as comment
            FROM 
                INFORMATION_SCHEMA.COLUMNS 
            WHERE 
                TABLE_SCHEMA = %s 
                AND TABLE_NAME = %s
            ORDER BY 
                ORDINAL_POSITION
        """
        return self.execute_query(query, (self.config['database'], table_name))
    
    def list_tables(self) -> List[str]:
        """
        获取数据库中所有表名
        
        Returns:
            表名列表
        """
        query = """
            SELECT 
                TABLE_NAME,TABLE_COMMENT
            FROM 
                INFORMATION_SCHEMA.TABLES 
            WHERE 
                TABLE_SCHEMA = %s
        """
        results = self.execute_query(query, (self.config['database'],))
        # print("查看所有表名",results)
        # return [row['TABLE_NAME'] for row in results]
        return results