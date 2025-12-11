# 河南大学校园网自动登录工具

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](README_ENHANCED.md)

## 📖 简介

基于Python开发的河南大学校园网自动登录脚本，模拟网页JavaScript中的auth()和check()函数进行身份验证，通过requests库直接模拟JS发起的关键网络请求（API认证和最终的quickauth GET请求），直接与后端认证服务进行交互，完成自动登录。

## 🆕 最新版本

**现已发布生产级增强版本！** 🎉

增强版本提供：
- ✅ 生产级代码质量（完整的错误处理、日志、安全特性）
- ✅ 跨平台支持（Windows、Linux、macOS）
- ✅ 开机自启和定时检查
- ✅ Web管理界面
- ✅ 凭证加密存储
- ✅ 模块化设计，易于扩展

**快速开始**：查看 [README_ENHANCED.md](README_ENHANCED.md) 和 [INSTALL.md](INSTALL.md)

## 🚀 快速使用

### 原始版本（简单直接）

1. 编辑 `auto_login.py`，修改账号信息：
```python
username = "你的账号"
password = "你的密码"
login_url = "你的登录URL"  # 需要从浏览器抓包获取
```

2. 运行脚本：
```bash
python auto_login.py
```

### 增强版本（推荐，功能更强大）

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置账号：
```bash
cp config.json.example config.json
# 编辑 config.json 填入账号信息
```

3. 运行：
```bash
python3 auto_login_enhanced.py
```

详细说明请查看 [完整文档](README_ENHANCED.md)

## 📚 文档

- [增强版完整说明](README_ENHANCED.md) - 功能特性、使用方法
- [安装指南](INSTALL.md) - 详细安装步骤
- [原始版本说明](#原始版本详细说明) - 见下文

## 🌟 功能特性对比

| 特性 | 原始版本 | 增强版本 |
|------|---------|---------|
| 基本登录功能 | ✅ | ✅ |
| 网络状态检查 | ✅ | ✅ |
| 配置文件支持 | ❌ | ✅ |
| 日志记录 | 简单 | 完整（轮转、级别） |
| 错误处理 | 基础 | 生产级 |
| 重试机制 | ❌ | ✅ |
| 定时检查 | ❌ | ✅ |
| 开机自启 | ❌ | ✅ |
| Web界面 | ❌ | ✅ |
| 跨平台脚本 | ❌ | ✅ |
| 凭证加密 | ❌ | ✅ |
| 模块化设计 | ❌ | ✅ |

---

## 原始版本详细说明

### 工作原理

脚本通过以下步骤完成自动登录：

1. **网络检查**：检测是否能访问外网（访问百度）
2. **获取参数**：从登录URL提取wlanuserip和wlanacname
3. **认证API调用**：发送认证请求到aaa-auth接口
4. **用户检查**：调用user/check-only接口验证用户
5. **最终认证**：发起quickauth.do请求完成登录
6. **验证登录**：访问外网验证登录是否成功

### 使用方法

1. **获取登录URL**：
   - 打开浏览器，按F12打开开发者工具
   - 访问校园网登录页面
   - 输入账号密码登录
   - 在Network标签找到portalReceiveAction.do请求
   - 复制完整URL

2. **修改脚本**：
```python
if __name__ == "__main__":
    if not check_internet_connection():
        login_url = "你抓取的URL"
        username = "你的学号"
        password = "你的密码"
        operator = "local"  # local/yd/lt/dx
        
        success = login_henu(login_url, username, password, operator)
        if success:
            print("登录成功！")
        else:
            print("登录失败！")
```

3. **运行脚本**：
```bash
python auto_login.py
```

### 运营商类型

- `local`: 校园网
- `yd`: 移动
- `lt`: 联通  
- `dx`: 电信

### 依赖库

```bash
pip install requests
```

## 🔧 故障排除

### 常见问题

**Q: 登录失败怎么办？**
- 检查账号密码是否正确
- 确认login_url是否正确（需要包含wlanuserip和wlanacname参数）
- 查看控制台输出的错误信息

**Q: 如何设置开机自启？**
- 使用增强版本，提供了完整的自启动安装脚本
- 查看 [INSTALL.md](INSTALL.md) 的详细说明

**Q: 能否定时检查网络状态？**
- 使用增强版本的守护进程模式：`python3 auto_login_enhanced.py --daemon`
- 或使用增强版本的系统服务安装脚本

## 📖 扩展阅读

- [增强版功能说明](README_ENHANCED.md)
- [详细安装指南](INSTALL.md)
- [Web界面使用](README_ENHANCED.md#-web界面)

## 🤝 贡献

欢迎提交Issue和Pull Request！

## ⚠️ 免责声明

本工具仅供学习交流使用，请遵守学校网络使用规定。使用本工具产生的任何后果由使用者自行承担。

## 📄 许可证

MIT License

---

**推荐使用增强版本以获得更好的体验！** 🚀
