# Dify Tool LLM

A powerful Dify plugin for automatically generating SQL statements and executing database queries.

## Features

- 🚀 Automatic SQL query generation
- 📊 Database query execution
- 🔍 Multi-language support (en_US, zh_Hans, ja_JP, pt_BR)
- 🛠 Flexible configuration options

## System Requirements

- Python 3.x
- MySQL Database
- Dify Plugin SDK (>=0.2.0, <0.3.0)

## Dependencies

```bash
dify_plugin>=0.2.0,<0.3.0
mysql-connector-python==8.2.0
python-dotenv==1.0.0
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd dify-tool-llm
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Modify the following settings:
```env
# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database
```

## Configuration

### Basic Settings
- `INSTALL_METHOD`: Installation method (remote/local)
- `REMOTE_INSTALL_URL`: Remote installation URL
- `REMOTE_INSTALL_KEY`: Remote installation key

### Database Settings
- `MYSQL_HOST`: MySQL server address
- `MYSQL_PORT`: MySQL server port
- `MYSQL_USER`: Database username
- `MYSQL_PASSWORD`: Database password
- `MYSQL_DATABASE`: Database name

## Usage

1. Ensure MySQL service is running and properly configured
2. Start the Dify platform
3. Enable this plugin in the Dify platform
4. Use the plugin to generate and execute SQL queries

Example query:
```sql
-- The plugin will help you generate SQL queries like this
SELECT column_name FROM table_name WHERE condition;
```

## Supported Features

This plugin focuses on:
- ✅ SQL Query Generation
- ✅ Database Operations
- ✅ Multi-language Support

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Author

**Author:** happyjing  
**Version:** 0.0.1  
**Type:** tool

## Privacy Policy

For detailed privacy information, please refer to [PRIVACY.md](PRIVACY.md)

## License

This project is open-source software. Please check with the project maintainers for licensing details.

---

**Note:** 
- This plugin requires proper MySQL database configuration to work correctly
- For issues or suggestions, please submit an Issue
- Make sure to read the configuration instructions carefully before use