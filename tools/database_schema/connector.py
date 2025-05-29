from .schema import DatabaseSchema
def get_db_schema(
      db_type: str,
      host: str,
      port: int,
      database: str,
      username: str,
      password: str,
      table_names: str | None = None,
      schema_name: str | None = None
) -> dict | None:
  # print("数据库连接参数", host, port, database, password, username)
  try:
    result = []
    dbInspector = DatabaseSchema()
    dbInspector.connect(
       db_type=db_type,
        config=
       {
          'host': host,
          'port': port,
          'user': username,
          'password':password ,
          'database': database,
        }
    )
    tables_metadata = {}
    # tables_list = [t.strip() for t in list_tables.split(',')]
    list_tables = dbInspector.list_tables()
    if isinstance(table_names, str) and table_names.strip():
      tables_select = [t.strip() for t in table_names.split(',')]
      tables_list = [table for table in list_tables if table['TABLE_NAME'] in tables_select]
    else:
      tables_list = list_tables
      
    # 初始化 metadata 字典
    for row in tables_list:
      table_name = row['TABLE_NAME']
      result = dbInspector.get_table_schema(table_name)
      tables_metadata[table_name] = {
        "table_comment": row['TABLE_COMMENT'],
        "columns": result
      }
    # table_name = "device_info"
    # if not table_name:
    #     print("表名为空")
    #     return None
    # result = dbInspector.get_table_schema(table_name)
    return tables_metadata
  except Exception as e:
    print(f"数据库错误，请查看{e}")
  finally:
    dbInspector.disconnect()
    print("主动断开数据库连接")
  return None

def get_execute_query(
      db_type: str,
      host: str,
      port: int,
      database: str,
      username: str,
      password: str,
      sql: str,
) -> dict | None:
  # print("数据库连接参数", host, port, database, password, username)
  try:
    result = []
    dbInspector = DatabaseSchema()
    dbInspector.connect(
       db_type=db_type,
        config=
       {
          'host': host,
          'port': port,
          'user': username,
          'password':password ,
          'database': database,
        }
    )
    result = dbInspector.execute_query(sql)
    return result
  except Exception as e:
    print(f"数据库错误，请查看{e}")
  finally:
    dbInspector.disconnect()
    print("主动断开数据库连接")
  return None