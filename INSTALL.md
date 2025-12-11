# 安装指南

本文档提供详细的安装步骤，适用于不同操作系统和使用场景。

## 📋 前置要求

- Python 3.7 或更高版本
- pip 包管理器
- 稳定的网络连接

## 🔍 检查Python版本

```bash
python3 --version
# 或
python --version
```

如果未安装或版本过低，请参考下方的Python安装指南。

## 🐍 Python安装

### Windows

1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载最新版本的Python安装程序
3. 运行安装程序，**务必勾选"Add Python to PATH"**
4. 验证安装：打开命令提示符，运行 `python --version`

### Linux

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### CentOS/RHEL
```bash
sudo yum install python3 python3-pip
```

#### Fedora
```bash
sudo dnf install python3 python3-pip
```

### macOS

#### 使用Homebrew（推荐）
```bash
brew install python3
```

#### 使用官方安装包
访问 [Python官网](https://www.python.org/downloads/) 下载macOS安装包

## 📦 安装自动登录工具

### 方法一：下载源码

```bash
# 克隆仓库
git clone https://github.com/LCYLYM/Auto-login-henu.git
cd Auto-login-henu

# 安装依赖
pip3 install -r requirements.txt
```

### 方法二：下载ZIP包

1. 访问 [GitHub仓库](https://github.com/LCYLYM/Auto-login-henu)
2. 点击 "Code" -> "Download ZIP"
3. 解压到目标目录
4. 打开终端/命令提示符，进入解压目录
5. 运行 `pip3 install -r requirements.txt`

## ⚙️ 配置

### 1. 创建配置文件

```bash
cp config.json.example config.json
```

### 2. 获取登录URL

登录URL包含关键参数（wlanuserip和wlanacname），需要从浏览器抓包获取：

#### 使用Chrome/Edge开发者工具

1. 打开浏览器，按 `F12` 打开开发者工具
2. 切换到 "Network"（网络）标签
3. 访问校园网登录页面
4. 输入账号密码，点击登录
5. 在Network标签中找到 `portalReceiveAction.do` 请求
6. 复制完整的URL（包含所有参数）

示例URL：
```
http://172.29.35.36:6060/portalReceiveAction.do?wlanuserip=10.16.211.160&wlanacname=HD-SuShe-ME60
```

### 3. 编辑配置文件

使用文本编辑器打开 `config.json`：

```json
{
    "network": {
        "login_url": "粘贴您抓取的URL",
        "test_url": "http://www.baidu.com",
        "timeout": 10,
        "retry_attempts": 3,
        "retry_delay": 5
    },
    "credentials": {
        "username": "您的学号",
        "password": "您的密码",
        "operator": "local"
    },
    "scheduler": {
        "enabled": true,
        "check_interval": 300,
        "auto_retry_on_failure": true
    }
}
```

**运营商选择**：
- `local`: 校园网（默认）
- `yd`: 移动
- `lt`: 联通
- `dx`: 电信

## 🧪 测试安装

运行一次登录测试：

```bash
python3 auto_login_enhanced.py
```

如果看到"登录成功"消息，说明配置正确。

## 🚀 设置自动启动

### Windows - 任务计划程序

#### 图形界面方式

1. 右键点击 `scripts/windows/install_service.bat`
2. 选择"以管理员身份运行"
3. 按提示完成安装

#### 手动配置

1. 按 `Win+R`，输入 `taskschd.msc`，打开任务计划程序
2. 点击"创建任务"
3. 配置触发器：
   - 新建触发器：用户登录时
   - 新建触发器：每5分钟重复一次
4. 配置操作：
   - 程序：`python`
   - 参数：`auto_login_enhanced.py`
   - 起始于：程序所在目录
5. 保存任务

### Linux - systemd

```bash
sudo ./scripts/linux/install_service.sh
```

验证安装：
```bash
systemctl status henu-autologin.timer
```

### macOS - LaunchAgent

```bash
./scripts/macos/install_service.sh
```

验证安装：
```bash
launchctl list | grep henu
```

## 🌐 安装Web界面（可选）

Web界面提供图形化的管理功能。

### 安装额外依赖

```bash
pip3 install flask flask-cors
```

### 启动Web服务

```bash
python3 web_interface.py
```

访问 `http://localhost:5000` 查看Web界面。

### 设置Web服务自动启动

#### Windows

创建新的任务计划，命令改为：
```
python web_interface.py --host 0.0.0.0 --port 5000
```

#### Linux

创建systemd服务文件 `/etc/systemd/system/henu-web.service`：

```ini
[Unit]
Description=HENU Auto Login Web Interface
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/Auto-login-henu
ExecStart=/usr/bin/python3 web_interface.py --host 0.0.0.0 --port 5000
Restart=always

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl enable henu-web.service
sudo systemctl start henu-web.service
```

#### macOS

修改 LaunchAgent plist文件，将命令改为：
```xml
<string>python3</string>
<string>/path/to/web_interface.py</string>
<string>--host</string>
<string>0.0.0.0</string>
<string>--port</string>
<string>5000</string>
```

## 🔐 启用凭证加密（推荐）

1. 确保已安装加密库：
```bash
pip3 install cryptography
```

2. 在 `config.json` 中启用加密：
```json
{
    "security": {
        "encrypt_credentials": true,
        "encryption_key_file": ".keyfile"
    }
}
```

3. 首次运行时会自动生成密钥并加密凭证

**重要**：备份 `.keyfile` 文件，丢失后无法解密！

## 📱 Docker部署（高级）

创建 `Dockerfile`（参考）：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "auto_login_enhanced.py", "--daemon"]
```

构建和运行：
```bash
docker build -t henu-autologin .
docker run -d --name henu-autologin \
  -v $(pwd)/config.json:/app/config.json \
  henu-autologin
```

## 🐛 故障排除

### 问题：pip install 失败

**解决方案**：使用国内镜像源

```bash
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题：权限不足

**Windows**：以管理员身份运行
**Linux/macOS**：使用 `sudo`

### 问题：找不到python3命令

**Windows**：使用 `python` 而不是 `python3`
**Linux/macOS**：确认Python 3已安装

### 问题：导入模块失败

确认依赖已安装：
```bash
pip3 list | grep requests
```

如未安装，手动安装：
```bash
pip3 install requests cryptography pyyaml flask flask-cors
```

## 📚 下一步

- 阅读 [README_ENHANCED.md](README_ENHANCED.md) 了解详细功能
- 查看 [Web界面使用指南](#) 
- 参与项目贡献：[CONTRIBUTING.md](CONTRIBUTING.md)

## 💡 提示

- 定期备份配置文件和密钥文件
- 查看日志文件排查问题：`auto_login.log`
- 使用 `--status` 参数查看运行状态
- Web界面可用于监控和管理

## 📞 获取帮助

如遇到安装问题，请：

1. 查看日志文件 `auto_login.log`
2. 阅读 [FAQ.md](FAQ.md)
3. 在GitHub提交 [Issue](https://github.com/LCYLYM/Auto-login-henu/issues)
4. 加入讨论组寻求帮助

---

安装完成！祝您使用愉快！ 🎉
