def format_schema_dsl(schema: dict, with_type: bool = True, with_comment: bool = True) -> str:
    """
    将数据库表结构格式化为DSL
    """
    type_aliases = {
        # 通用类型
        'INT': 'i', 'INTEGER': 'i', 'BIGINT': 'i', 'SMALLINT': 'i', 'TINYINT': 'i',
        'VARCHAR': 's', 'TEXT': 's', 'CHAR': 's', 'NVARCHAR': 's', 'NCHAR': 's',
        'DATETIME': 'dt', 'DATE': 'dt', 'TIMESTAMP': 'dt', 'TIME': 'dt',
        'DECIMAL': 'f', 'NUMERIC': 'f', 'FLOAT': 'f', 'DOUBLE': 'f', 'REAL': 'f',
        'BOOLEAN': 'b', 'BOOL': 'b',
        'JSON': 'j', 
        
        # SQL Server特有
        'MONEY': 'f', 'SMALLMONEY': 'f', 'DATETIME2': 'dt', 'DATETIMEOFFSET': 'dt',
        'HIERARCHYID': 's', 'UNIQUEIDENTIFIER': 's',
        
        # PostgreSQL特有
        'JSONB': 'j', 'BYTEA': 's', 'SERIAL': 'i', 'BIGSERIAL': 'i', 
        'TSVECTOR': 's', 'UUID': 's',
        
        # MySQL特有
        'YEAR': 'i', 'SET': 's', 'ENUM': 's', 'MEDIUMINT': 'i'
    }
    
    lines = []
    for table_name, table_data in schema.items():
        column_parts = []
        
        # 处理表注释
        if with_comment and (table_comment := table_data.get('comment', '')):
            lines.append(f"# {table_comment}")
        
        # 处理字段
        for col in table_data['columns']:
            parts = [col['name']]
            
            if with_type:
                raw_type = col['type'].upper()
                col_type = type_aliases.get(raw_type, raw_type.lower())
                parts.append(col_type)
                
            if with_comment and (col_comment := col.get('comment', '')):
                parts.append(f"# {col_comment}")
                
            column_parts.append(":".join(parts))
        
        # 构建表行
        table_line = f"T:{table_name}({', '.join(column_parts)})"
        lines.append(table_line)
    
    return "\n".join(lines)