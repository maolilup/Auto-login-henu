# 🚀 快速开始指南

5分钟内完成安装和配置！

## 📋 第一步：检查环境

确保已安装Python 3.7或更高版本：

```bash
python3 --version
```

如果未安装，请先安装Python：
- Windows: https://www.python.org/downloads/
- Linux: `sudo apt install python3 python3-pip`
- macOS: `brew install python3`

## 📥 第二步：下载项目

### 方法1：使用Git

```bash
git clone https://github.com/LCYLYM/Auto-login-henu.git
cd Auto-login-henu
```

### 方法2：下载ZIP

1. 访问 https://github.com/LCYLYM/Auto-login-henu
2. 点击 "Code" -> "Download ZIP"
3. 解压到任意目录
4. 打开终端/命令提示符，进入该目录

## 📦 第三步：安装依赖

```bash
pip install -r requirements.txt
```

> 💡 如果速度慢，可使用国内镜像：
> ```bash
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

## ⚙️ 第四步：配置账号

### 1. 创建配置文件

```bash
cp config.json.example config.json
```

### 2. 获取登录URL

**重要！** 你需要从浏览器抓包获取：

1. 打开Chrome/Edge浏览器，按F12
2. 切换到"Network"（网络）标签
3. 访问校园网登录页面
4. 输入账号密码，点击登录
5. 找到`portalReceiveAction.do`请求
6. 右键 -> Copy -> Copy link address

URL示例：
```
http://172.29.35.36:6060/portalReceiveAction.do?wlanuserip=10.16.211.160&wlanacname=HD-SuShe-ME60
```

### 3. 编辑配置文件

打开 `config.json`，填入信息：

```json
{
    "network": {
        "login_url": "粘贴你抓取的URL"
    },
    "credentials": {
        "username": "你的学号",
        "password": "你的密码",
        "operator": "local"
    }
}
```

**运营商选择**：
- `local`: 校园网（默认）
- `yd`: 移动
- `lt`: 联通
- `dx`: 电信

## ▶️ 第五步：运行测试

```bash
python3 auto_login_enhanced.py
```

看到"登录成功"就大功告成了！🎉

## 🎯 进阶使用

### 守护进程模式（持续运行）

```bash
python3 auto_login_enhanced.py --daemon
```

程序会每5分钟自动检查一次网络状态。

### Web界面（图形化管理）

```bash
python3 web_interface.py
```

然后访问 http://localhost:5000

### 设置开机自启

#### Windows
1. 双击 `scripts/windows/install_service.bat`
2. 或右键"以管理员身份运行"

#### Linux
```bash
sudo ./scripts/linux/install_service.sh
```

#### macOS
```bash
./scripts/macos/install_service.sh
```

## 📱 使用场景

### 场景1：临时使用
适合偶尔需要登录的情况
```bash
python3 auto_login_enhanced.py
```

### 场景2：持续监控
适合宿舍路由器、服务器等需要持续联网的设备
```bash
python3 auto_login_enhanced.py --daemon
```
或安装系统服务

### 场景3：图形化管理
适合不熟悉命令行的用户
```bash
python3 web_interface.py
```

## 🔧 常见问题

### ❌ 登录失败

1. **检查账号密码**：在config.json中确认
2. **检查URL**：确保包含wlanuserip和wlanacname参数
3. **检查运营商**：尝试不同的operator值
4. **查看日志**：`tail -f auto_login.log`

### ❌ 找不到Python

Windows用户尝试使用`python`而不是`python3`：
```bash
python auto_login_enhanced.py
```

### ❌ 依赖安装失败

使用国内镜像：
```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

## 📚 更多帮助

- 📖 [完整文档](README_ENHANCED.md)
- 📖 [安装指南](INSTALL.md)
- ❓ [常见问题](FAQ.md)
- 📝 [更新日志](CHANGELOG.md)

## 💡 小贴士

1. **定期更新URL**：IP变化后需要重新抓包
2. **备份配置**：记得备份config.json和.keyfile
3. **查看日志**：遇到问题先看日志文件
4. **使用加密**：启用凭证加密保护密码安全

## 🎉 完成！

现在你已经成功配置了自动登录工具！

享受自动登录带来的便利吧！如有问题，欢迎提Issue。

---

**下一步**：

- 🌐 尝试Web界面：`python3 web_interface.py`
- ⚙️ 设置开机自启：运行对应平台的install_service脚本
- 🔐 启用加密：在config.json中设置`"encrypt_credentials": true`

**需要帮助？**

在GitHub提交Issue：https://github.com/LCYLYM/Auto-login-henu/issues
