from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List


class DatabaseInterface(ABC):
    """数据库操作的基础接口类"""
    
    @abstractmethod
    def connect(self) -> bool:
        """建立数据库连接"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """关闭数据库连接"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """执行SQL查询"""
        pass
    
    @abstractmethod
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """获取表结构信息"""
        pass
    
    @abstractmethod
    def list_tables(self) -> List[str]:
        """获取所有表名"""
        pass