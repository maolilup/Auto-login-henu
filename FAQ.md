# 常见问题解答（FAQ）

## 📋 目录

- [安装问题](#安装问题)
- [配置问题](#配置问题)
- [登录问题](#登录问题)
- [自动启动问题](#自动启动问题)
- [Web界面问题](#web界面问题)
- [安全问题](#安全问题)
- [其他问题](#其他问题)

---

## 安装问题

### Q1: 提示"未找到Python"或"python不是内部或外部命令"

**A:** Python未安装或未添加到系统PATH。

**解决方案**：
1. 访问 [Python官网](https://www.python.org/downloads/) 下载安装
2. 安装时**务必勾选"Add Python to PATH"**
3. 重启命令行窗口
4. 验证：`python --version` 或 `python3 --version`

### Q2: pip install 失败，提示网络错误

**A:** 可能是网络问题或pip源速度慢。

**解决方案**：
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或永久配置镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 提示"ModuleNotFoundError: No module named 'requests'"

**A:** 依赖库未安装。

**解决方案**：
```bash
pip install requests
# 或安装所有依赖
pip install -r requirements.txt
```

---

## 配置问题

### Q4: 如何获取正确的login_url？

**A:** 需要从浏览器抓包获取。

**详细步骤**：
1. 打开Chrome/Edge浏览器
2. 按F12打开开发者工具
3. 切换到"Network"（网络）标签
4. 访问校园网登录页面
5. 输入账号密码，点击登录
6. 在Network标签中找到`portalReceiveAction.do`请求
7. 右键该请求 -> Copy -> Copy link address
8. 粘贴到配置文件的`login_url`字段

**URL示例**：
```
http://172.29.35.36:6060/portalReceiveAction.do?wlanuserip=10.16.211.160&wlanacname=HD-SuShe-ME60
```

### Q5: 配置文件在哪里？

**A:** 配置文件位置优先级：

1. 当前目录的`config.json`
2. 用户目录的`~/.henu_login/config.json`
3. 系统目录的`/etc/henu_login/config.json`（Linux）

**创建配置文件**：
```bash
cp config.json.example config.json
```

### Q6: 运营商类型怎么选？

**A:** 根据您的网络接入方式选择：

- `local`: 校园网（默认，推荐）
- `yd`: 中国移动
- `lt`: 中国联通
- `dx`: 中国电信

**如何确定**：
- 如果不确定，先尝试`local`
- 查看您的校园网账号是否有运营商后缀

---

## 登录问题

### Q7: 提示"登录失败"怎么办？

**A:** 可能的原因和解决方案：

1. **账号密码错误**
   - 检查config.json中的username和password
   - 尝试在浏览器手动登录验证

2. **login_url不正确**
   - 重新抓包获取正确的URL
   - 确保URL包含wlanuserip和wlanacname参数

3. **运营商类型错误**
   - 尝试更换operator值（local/yd/lt/dx）

4. **网络问题**
   - 检查是否连接到校园网
   - 尝试ping内网地址：`ping 172.29.35.27`

5. **IP地址变化**
   - 如果是笔记本等移动设备，IP会变化
   - 需要重新抓包获取新的URL

### Q8: 提示"网络连接正常，无需登录"但实际无法上网

**A:** 测试URL可能需要调整。

**解决方案**：
在config.json中修改test_url：
```json
{
    "network": {
        "test_url": "http://www.baidu.com"
    }
}
```

### Q9: 登录成功但几分钟后又断网

**A:** 可能是网络不稳定或认证超时。

**解决方案**：
1. 启用守护进程模式：
   ```bash
   python3 auto_login_enhanced.py --daemon
   ```

2. 或安装系统服务（推荐）：
   - Windows: `scripts/windows/install_service.bat`
   - Linux: `sudo scripts/linux/install_service.sh`
   - macOS: `scripts/macos/install_service.sh`

---

## 自动启动问题

### Q10: Windows任务计划安装失败

**A:** 需要管理员权限。

**解决方案**：
1. 右键点击`install_service.bat`
2. 选择"以管理员身份运行"
3. 如仍失败，手动创建任务计划：
   - Win+R -> `taskschd.msc`
   - 创建基本任务
   - 触发器：用户登录时
   - 操作：启动程序 `python`，参数`auto_login_enhanced.py`

### Q11: Linux systemd服务无法启动

**A:** 检查服务状态和日志。

**解决方案**：
```bash
# 查看服务状态
systemctl status henu-autologin.service

# 查看详细日志
journalctl -u henu-autologin.service -n 50

# 检查配置文件路径
systemctl cat henu-autologin.service

# 重新安装
sudo ./scripts/linux/uninstall_service.sh
sudo ./scripts/linux/install_service.sh
```

### Q12: macOS LaunchAgent不工作

**A:** 检查plist文件和权限。

**解决方案**：
```bash
# 查看LaunchAgent状态
launchctl list | grep henu

# 查看日志
tail -f ~/Library/Logs/henu_autologin.log
tail -f ~/Library/Logs/henu_autologin_error.log

# 重新加载
launchctl unload ~/Library/LaunchAgents/com.henu.autologin.plist
launchctl load ~/Library/LaunchAgents/com.henu.autologin.plist
```

---

## Web界面问题

### Q13: Web界面无法访问

**A:** 检查Flask是否安装和端口是否占用。

**解决方案**：
```bash
# 安装Flask
pip install flask flask-cors

# 检查端口占用
# Windows:
netstat -ano | findstr :5000
# Linux/macOS:
lsof -i :5000

# 使用其他端口
python3 web_interface.py --port 8080
```

### Q14: 局域网其他设备无法访问Web界面

**A:** 防火墙阻止或监听地址错误。

**解决方案**：
```bash
# 监听所有网卡
python3 web_interface.py --host 0.0.0.0 --port 5000

# Windows防火墙：
# 控制面板 -> 系统和安全 -> Windows Defender 防火墙 -> 高级设置
# 入站规则 -> 新建规则 -> 端口 -> TCP 5000

# Linux防火墙（firewalld）：
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload

# Linux防火墙（ufw）：
sudo ufw allow 5000/tcp
```

### Q15: Web界面显示"登录失败"

**A:** 配置文件问题。

**解决方案**：
1. 确认config.json存在且配置正确
2. 在命令行先测试：`python3 auto_login_enhanced.py`
3. 查看Web界面日志标签页的错误信息

---

## 安全问题

### Q16: 密码明文存储在配置文件中安全吗？

**A:** 可以启用加密功能。

**解决方案**：
```bash
# 安装加密库
pip install cryptography

# 在config.json中启用加密
{
    "security": {
        "encrypt_credentials": true,
        "encryption_key_file": ".keyfile"
    }
}

# 首次运行会自动加密
python3 auto_login_enhanced.py
```

**重要**：备份`.keyfile`文件，丢失后无法解密！

### Q17: 如何保护配置文件不被其他用户查看？

**A:** 设置文件权限。

**解决方案**：
```bash
# Linux/macOS
chmod 600 config.json
chmod 600 .keyfile

# Windows（使用PowerShell）
icacls config.json /inheritance:r /grant:r "$env:USERNAME:(R,W)"
```

---

## 其他问题

### Q18: 支持多账号吗？

**A:** 当前版本不直接支持，但可以通过以下方式实现：

**方案1：多个配置文件**
```bash
python3 auto_login_enhanced.py --config config1.json
python3 auto_login_enhanced.py --config config2.json
```

**方案2：修改代码**
在`auto_login_enhanced.py`中添加多账号逻辑。

### Q19: 可以在树莓派上运行吗？

**A:** 可以！树莓派是ARM架构的Linux系统。

**安装步骤**：
```bash
# 更新系统
sudo apt update && sudo apt upgrade

# 安装Python和依赖
sudo apt install python3 python3-pip
pip3 install -r requirements.txt

# 配置和运行
cp config.json.example config.json
# 编辑config.json
python3 auto_login_enhanced.py --daemon

# 或安装systemd服务
sudo ./scripts/linux/install_service.sh
```

### Q20: 如何更新到最新版本？

**A:** 使用git更新或下载新版本。

**解决方案**：
```bash
# 方法1：使用git
cd Auto-login-henu
git pull origin main

# 方法2：手动下载
# 1. 备份config.json
# 2. 下载新版本ZIP
# 3. 解压覆盖
# 4. 恢复config.json
# 5. 更新依赖：pip install -r requirements.txt
```

### Q21: 如何查看运行日志？

**A:** 日志位置：

**命令行版本**：
```bash
# 默认日志文件
tail -f auto_login.log

# 或在config.json中指定路径
```

**系统服务**：
```bash
# Windows任务计划：
# 任务计划程序 -> 历史记录

# Linux systemd：
journalctl -u henu-autologin.service -f

# macOS LaunchAgent：
tail -f ~/Library/Logs/henu_autologin.log
```

**Web界面**：
访问Web界面的"系统日志"标签页

### Q22: 程序占用资源多吗？

**A:** 非常少。

**资源占用**：
- 内存：约10-20MB
- CPU：检查时短暂<1%，平时0%
- 网络：仅在检查和登录时产生少量流量（<1KB）

---

## 💡 没有找到答案？

1. 查看完整文档：
   - [README_ENHANCED.md](README_ENHANCED.md)
   - [INSTALL.md](INSTALL.md)

2. 查看日志文件获取详细错误信息

3. 在GitHub提交Issue：
   - [提交Issue](https://github.com/LCYLYM/Auto-login-henu/issues)
   - 请包含：操作系统、Python版本、错误信息、日志内容

4. 查看现有Issues，可能已有解答

---

**提示**：大部分问题都可以通过查看日志文件找到原因！
