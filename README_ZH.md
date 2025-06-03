# Dify Tool LLM

一个强大的Dify插件，用于自动生成SQL语句并执行数据库查询操作。

## 功能特点

- 🚀 自动生成SQL查询语句
- 📊 执行数据库查询操作
- 🔍 支持多语言（en_US, zh_Hans, ja_JP, pt_BR）
- 🛠 灵活的配置选项

## 系统要求

- Python 3.12
- MySQL数据库
- Dify平台（最低版本：0.0.1）

## 安装步骤

1. 克隆仓库：
```bash
git clone [repository-url]
cd dify-tool-llm
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
   - 复制`.env.example`文件为`.env`
   - 修改以下配置项：
```env
# MySQL数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database
```

## 配置说明

### 基本配置
- `INSTALL_METHOD`: 安装方式（remote/local）
- `REMOTE_INSTALL_URL`: 远程安装URL
- `REMOTE_INSTALL_KEY`: 远程安装密钥

### 数据库配置
- `MYSQL_HOST`: MySQL服务器地址
- `MYSQL_PORT`: MySQL服务器端口
- `MYSQL_USER`: 数据库用户名
- `MYSQL_PASSWORD`: 数据库密码
- `MYSQL_DATABASE`: 数据库名称

## 使用示例

1. 确保MySQL服务已启动并正确配置
2. 启动Dify平台
3. 在Dify平台中启用该插件
4. 使用插件生成和执行SQL查询

## 资源限制

- 内存限制：256MB
- 存储空间：1MB

## 支持的功能

- ✅ LLM支持
- ✅ 文本嵌入
- ✅ 重排序
- ✅ 内容审核
- ❌ 语音合成
- ❌ 语音识别

## 贡献指南

1. Fork该项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个Pull Request

## 作者

**Author:** happyjing  
**Version:** 0.0.1

## 隐私政策

详细的隐私政策请参考 [PRIVACY.md](PRIVACY.md)

## 许可证

[许可证类型] - 查看 LICENSE 文件了解更多详情

---

**注意：** 本插件仍在开发中，某些功能可能会发生变化。如有问题或建议，请提交Issue。