# 河南大学校园网自动登录工具（增强版）

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](README_ENHANCED.md)

## 📖 简介

这是一个生产级的河南大学校园网自动登录工具，提供完整的功能实现、错误处理、日志记录和安全特性。

### ✨ 主要特性

- 🔐 **安全可靠**：支持凭证加密存储，保护账号安全
- 🌐 **跨平台支持**：原生支持 Windows、Linux、macOS
- ⚙️ **自动化运行**：开机自启、定时检查、断网重连
- 📊 **Web管理界面**：提供现代化的Web控制面板
- 📝 **完整日志**：详细的日志记录和日志轮转
- 🔄 **智能重试**：失败自动重试，可配置重试策略
- 🛠️ **模块化设计**：易于扩展和维护
- 📦 **配置管理**：支持JSON/YAML配置文件
- 🚀 **多种运行模式**：命令行、守护进程、Web服务

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置账号信息

复制配置文件模板：
```bash
cp config.json.example config.json
```

编辑 `config.json`，填入您的账号信息：
```json
{
    "network": {
        "login_url": "http://172.29.35.36:6060/portalReceiveAction.do?wlanuserip=YOUR_IP&wlanacname=YOUR_AC_NAME"
    },
    "credentials": {
        "username": "your_username",
        "password": "your_password",
        "operator": "local"
    }
}
```

### 3. 运行程序

#### 命令行模式（运行一次）
```bash
python3 auto_login_enhanced.py
```

#### 守护进程模式（持续运行）
```bash
python3 auto_login_enhanced.py --daemon
```

#### Web界面模式
```bash
python3 web_interface.py
# 访问 http://localhost:5000
```

## 🖥️ 平台特定安装

### Windows

#### 使用批处理脚本
双击运行 `scripts/windows/auto_login.bat`

#### 安装开机自启服务
1. 右键点击 `scripts/windows/install_service.bat`
2. 选择"以管理员身份运行"
3. 按提示完成安装

**卸载服务**：以管理员身份运行 `scripts/windows/uninstall_service.bat`

### Linux

#### 使用Shell脚本
```bash
./scripts/linux/auto_login.sh
```

#### 安装systemd服务（开机自启）
```bash
sudo ./scripts/linux/install_service.sh
```

**常用命令**：
```bash
# 查看状态
systemctl status henu-autologin.timer

# 查看日志
journalctl -u henu-autologin.service -f

# 立即运行
sudo systemctl start henu-autologin.service

# 卸载服务
sudo ./scripts/linux/uninstall_service.sh
```

### macOS

#### 使用Shell脚本
```bash
./scripts/macos/auto_login.sh
```

#### 安装LaunchAgent（开机自启）
```bash
./scripts/macos/install_service.sh
```

**常用命令**：
```bash
# 立即运行
launchctl start com.henu.autologin

# 停止服务
launchctl stop com.henu.autologin

# 查看日志
tail -f ~/Library/Logs/henu_autologin.log

# 卸载服务
./scripts/macos/uninstall_service.sh
```

## 📋 配置说明

### 配置文件结构

```json
{
    "network": {
        "login_url": "登录URL",
        "test_url": "http://www.baidu.com",
        "timeout": 10,
        "retry_attempts": 3,
        "retry_delay": 5
    },
    "credentials": {
        "username": "用户名",
        "password": "密码",
        "operator": "运营商类型：local/yd/lt/dx"
    },
    "scheduler": {
        "enabled": true,
        "check_interval": 300,
        "auto_retry_on_failure": true
    },
    "logging": {
        "level": "INFO",
        "file": "auto_login.log",
        "max_size_mb": 10,
        "backup_count": 5,
        "console_output": true
    },
    "security": {
        "encrypt_credentials": false,
        "encryption_key_file": ".keyfile"
    }
}
```

### 运营商类型说明

- `local`: 校园网
- `yd`: 移动
- `lt`: 联通
- `dx`: 电信

### 环境变量配置

也可以通过环境变量配置（优先级高于配置文件）：

```bash
export HENU_USERNAME="your_username"
export HENU_PASSWORD="your_password"
export HENU_OPERATOR="local"
```

## 🌐 Web界面

### 启动Web服务

```bash
python3 web_interface.py --host 0.0.0.0 --port 5000
```

### 功能特性

- 📊 **实时状态监控**：网络连接状态、认证信息
- 🚀 **快速登录**：直接在Web界面输入账号登录
- ⚙️ **自动登录控制**：启动/停止自动登录功能
- 📋 **日志查看**：实时查看系统日志
- 🔄 **自动刷新**：状态信息自动更新

### 访问方式

- 本机访问：`http://localhost:5000`
- 局域网访问：`http://YOUR_IP:5000`

## 🔐 安全特性

### 凭证加密

启用凭证加密功能：

1. 安装加密库（如未安装）：
```bash
pip install cryptography
```

2. 在配置文件中启用加密：
```json
{
    "security": {
        "encrypt_credentials": true,
        "encryption_key_file": ".keyfile"
    }
}
```

3. 首次运行时会自动生成密钥文件，并加密存储凭证

**注意**：请妥善保管密钥文件（`.keyfile`），丢失后无法解密凭证。

## 📝 命令行选项

### auto_login_enhanced.py

```
usage: auto_login_enhanced.py [-h] [--config CONFIG] [--daemon] [--status] [--version]

optional arguments:
  -h, --help            显示帮助信息
  --config CONFIG, -c CONFIG
                        指定配置文件路径
  --daemon, -d          以守护进程模式运行
  --status, -s          显示状态信息
  --version, -v         显示版本信息
```

### web_interface.py

```
usage: web_interface.py [-h] [--host HOST] [--port PORT] [--debug]

optional arguments:
  -h, --help     显示帮助信息
  --host HOST    监听地址（默认：0.0.0.0）
  --port PORT    监听端口（默认：5000）
  --debug        启用调试模式
```

## 📊 项目结构

```
Auto-login-henu/
├── auto_login.py              # 原始版本
├── auto_login_enhanced.py     # 增强版主程序
├── henu_login_lib.py          # 核心登录库
├── config_manager.py          # 配置管理模块
├── credential_manager.py      # 凭证加密模块
├── logger_setup.py            # 日志配置模块
├── web_interface.py           # Web界面服务
├── config.json.example        # 配置文件模板
├── requirements.txt           # Python依赖
├── README.md                  # 原始说明文档
├── README_ENHANCED.md         # 增强版说明文档
├── scripts/                   # 平台特定脚本
│   ├── windows/              # Windows脚本
│   │   ├── auto_login.bat
│   │   ├── install_service.bat
│   │   └── uninstall_service.bat
│   ├── linux/                # Linux脚本
│   │   ├── auto_login.sh
│   │   ├── install_service.sh
│   │   └── uninstall_service.sh
│   └── macos/                # macOS脚本
│       ├── auto_login.sh
│       ├── install_service.sh
│       └── uninstall_service.sh
├── web_templates/            # Web界面模板
│   └── index.html
└── web_static/               # Web静态资源
```

## 🔧 开发指南

### 核心模块说明

#### henu_login_lib.py
- `NetworkChecker`: 网络连接检查器
- `HENUAuthenticator`: 网络认证器
- `HENULoginError`: 自定义异常类

#### config_manager.py
- `ConfigManager`: 配置文件管理器
- 支持JSON/YAML格式
- 环境变量优先级

#### credential_manager.py
- `CredentialManager`: 凭证加密管理器
- 使用Fernet对称加密
- 自动生成和管理密钥

#### logger_setup.py
- `LoggerSetup`: 日志系统配置器
- 支持日志轮转
- 多级别日志记录

### 扩展开发

添加新功能的步骤：

1. 在相应模块中添加功能代码
2. 更新配置文件结构（如需要）
3. 添加命令行参数（如需要）
4. 更新文档
5. 添加单元测试（推荐）

## 🐛 故障排除

### 常见问题

**Q: 提示"未找到Python"**
A: 请确保已安装Python 3.7或更高版本，并添加到系统PATH

**Q: 依赖安装失败**
A: 尝试使用国内镜像：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

**Q: 登录失败**
A: 
1. 检查账号密码是否正确
2. 检查login_url是否正确（需要从浏览器抓包获取）
3. 查看日志文件获取详细错误信息

**Q: Web界面无法访问**
A: 
1. 检查防火墙是否允许端口访问
2. 确认Flask已正确安装
3. 查看控制台错误信息

### 日志查看

- 默认日志文件：`auto_login.log`
- Web界面日志：通过Web界面的日志页面查看
- 系统日志（Linux）：`journalctl -u henu-autologin.service`
- 系统日志（macOS）：`~/Library/Logs/henu_autologin.log`

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## ⚠️ 免责声明

本工具仅供学习交流使用，请遵守学校网络使用规定。使用本工具产生的任何后果由使用者自行承担。

## 📮 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/LCYLYM/Auto-login-henu/issues)
- 发送邮件到项目维护者

## 🙏 致谢

感谢所有为本项目做出贡献的开发者！

---

**注意**：使用前请确保已获取正确的登录URL（包含wlanuserip和wlanacname参数），可通过浏览器开发者工具抓包获取。
