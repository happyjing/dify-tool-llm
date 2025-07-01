from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.entities.model.message import SystemPromptMessage, UserPromptMessage
from tools.database_schema import DatabaseOperations
from tools.database_schema.db_operations import DatabaseOperations
from .database_schema.connector import get_db_schema
from .database_schema.formatter import format_schema_dsl
from utils.prompt_loader import PromptLoader
class DifyToolLlmTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        mysqlState = get_db_schema(
            db_type=tool_parameters.get('db_type', 'mysql'),
            host=tool_parameters['host'],
            port=tool_parameters['port'],
            database=tool_parameters['db_name'],
            username=tool_parameters['username'],
            password=tool_parameters['password'],
            table_names=tool_parameters.get('table_names', ''),
            schema_name=tool_parameters.get('schema_name')
        )
         # table_names=tool_parameters['table_names'],
        # schema_name=tool_parameters.get('schema_name')
        # yield self.create_json_message({
        #     "result": mysqlState
        # })
        # tableInfo = {
        #     "device_info": {
        #         "table_comment": "设备信息表",
        #         "columns": mysqlState
        #     }
        # }
        # print('数据库所有表的结构', mysqlState)
        dsl_text = format_schema_dsl(mysqlState)
        # 初始化模版记载器
        prompt_loader = PromptLoader()
        # 构建模版上下文
        context = {
            'db_type': "mysql",
            'meta_data': dsl_text
        }
        print(context)
        # 获取动态提示词
        system_prompt = prompt_loader.get_prompt(
            db_type="mysql",
            context=context,
            is_think=tool_parameters.get('is_thinking', False),
            limit=tool_parameters.get( 'limit', 10 ),
            user_custom_prompt=tool_parameters.get('custom_prompt', '') # 自定义提示词
        )
        # print(system_prompt)
        # 默认执行LLM调用
        model_info = tool_parameters["model"]
        # print(model_info)
        response = self.session.model.llm.invoke(
            model_config=model_info,
            prompt_messages=[
                SystemPromptMessage(
                    content=system_prompt
                ),
                UserPromptMessage(
                    content=f"数据库类型：{tool_parameters.get('db_type', 'mysql')}\n"
                            f"用户需求：{tool_parameters['query']}"
                )
            ],
            stream=False
        )
        out_sql = response.message.content
        sql_query = ''
        if (out_sql and '</think>\n\n' in out_sql): 
            sql_query = out_sql.split('</think>\n\n')[1]
        else:
            sql_query = out_sql
        # sql_query = out_sql.split('</think>\n\n')[1]
        yield self.create_text_message(sql_query)
        # yield self.create_json_message({
        #     "result": out_sql
        # })
        # for chunk in response:
        #     if chunk.delta.message:
        #         assert isinstance(chunk.delta.message.content, str)
        #         yield self.create_text_message(text=chunk.delta.message.content)