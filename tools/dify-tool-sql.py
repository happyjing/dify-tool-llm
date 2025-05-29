from collections.abc import Generator
from typing import Any, Optional
from dify_plugin import Tool
from datetime import datetime, date
import json
from decimal import Decimal
from dify_plugin.entities.tool import ToolInvokeMessage
from .database_schema.connector import get_execute_query
import re
class DifyToolLlmTool(Tool):
    RISK_KEYWORDS = {"DROP", "DELETE", "TRUNCATE", "ALTER", "UPDATE", "INSERT"}
    SUPPORTED_FORMATS = {"json", "csv", "html", "text"}
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            execute_params = self._validate_and_prepare_params(tool_parameters)
            result = get_execute_query(
                db_type=execute_params.get('db_type', 'mysql'),
                host=execute_params['host'],
                port=execute_params['port'],
                database=execute_params['database'],
                username=execute_params['username'],
                password=execute_params['password'],
                sql=execute_params['sql']
            )
            # yield self.create_text_message('123')
            # yield self.create_json_message({
            #     "result": result
            # })
            # self._handle_result_format(result, 'text', '')
            yield from self._handle_result_format(
                result, 
                'text',
                ''
            )
        except Exception as e:
            raise ValueError(f"数据库操作失败：{str(e)}")
        
    def _contains_risk_commands(self, sql: str) -> bool:
        """增强的SQL注入检测"""
        cleaned_sql = re.sub(r'/\*.*?\*/|--.*', '', sql, flags=re.DOTALL)
        statements = [s.strip() for s in cleaned_sql.split(';') if s.strip()]
        
        for stmt in statements:
            first_token = re.search(r'\b(\w+)\b', stmt, re.IGNORECASE)
            if first_token and first_token.group(1).upper() in self.RISK_KEYWORDS:
                return True
        return False
    def _validate_and_prepare_params(self, params: dict) -> dict:
        """参数验证和预处理"""
        required_params = ['query', 'db_type', 'host', 'port', 'db_name', 'username', 'password']
        missing = [p for p in required_params if not params.get(p)]
        if missing:
            raise ValueError(f"缺少必要参数: {', '.join(missing)}")

        try:
            port = int(params['port'])
        except ValueError:
            raise ValueError("端口号必须是整数")

        if self._contains_risk_commands(params['query']):
            raise ValueError("SQL语句包含危险操作")
        # params['schema'] = params.get('schema')if params.get('schema') != None else 'dbo' if params['db_type'] == 'sqlserver' else 'public'
        # 数据库执行参数
        execute_params = {
            'db_type': params['db_type'],
            'host': params['host'],
            'port': port,
            'database': params['db_name'],
            'username': params['username'],
            'password': params['password'],
            'sql': params['query'],
            'params': {},
            'schema': params.get('schema')
        }

        # 结果格式参数
        # result_format = params.get('result_format', 'text').lower()

        return execute_params
    
    def _handle_result_format(self, result: Any, fmt: str, schema: Optional[str]) -> Generator[ToolInvokeMessage, None, None]:
        """处理不同格式的结果输出"""
        if fmt not in self.SUPPORTED_FORMATS:
            raise ValueError(f"不支持的格式: {fmt}。支持格式: {', '.join(self.SUPPORTED_FORMATS)}")

        # 处理空结果
        if self._is_empty_result(result):
            yield self.create_text_message("未查询到数据")
            return

        try:
            if fmt == 'json':
                yield self._handle_json(result)
            elif fmt == 'html':
                yield from self._handle_html(result)
            else:
                yield self._handle_text(result, schema)
        except Exception as e:
            raise ValueError(f"结果格式化失败: {str(e)}")
    def _handle_json(self, data: Any) -> ToolInvokeMessage:
        """生成JSON格式消息"""
        return self.create_json_message({
            "status": "success",
            "result": self._safe_serialize(data)
        })

    def _handle_text(self, data: Any, schema: Optional[str]) -> ToolInvokeMessage:
        """生成可读文本消息"""
        readable_text = self._to_readable_text(data, schema)
        return self.create_text_message(readable_text)

    def _handle_html(self, data: list[dict]) -> Generator[ToolInvokeMessage, None, None]:
        """生成HTML表格"""
        html_table = self._generate_html_table(data)
        yield self.create_blob_message(
            html_table.encode('utf-8'),
            meta={'mime_type': 'text/html', 'filename': 'result.html'}
        )

    def _is_empty_result(self, result: Any) -> bool:
        """判断是否为空结果"""
        if result is None:
            return True
        if isinstance(result, list) and not result:
            return True
        if isinstance(result, dict) and result.get("rowcount", 0) == 0:
            return True
        return False
    
    def _custom_serializer(self, obj: Any) -> Any:
        """增强的数据类型序列化"""
        if isinstance(obj, (datetime, date)):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, bytes):
            return obj.decode('utf-8', errors='replace')
        return str(obj)
    def _to_readable_text(self, data: Any, schema: Optional[str]) -> str:
        """生成可读性文本"""
        if schema:
            header = f"Schema: {schema}\n"
        else:
            header = ""

        if isinstance(data, list):
            return header + "\n".join(
                json.dumps(row, ensure_ascii=False, indent=2, default=self._custom_serializer)
                for row in data
            )
        return header + json.dumps(data, indent=2, ensure_ascii=False, default=self._custom_serializer)
    def _custom_serializer(self, obj: Any) -> Any:
        """增强的数据类型序列化"""
        if isinstance(obj, (datetime, date)):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, bytes):
            return obj.decode('utf-8', errors='replace')
        return str(obj)
