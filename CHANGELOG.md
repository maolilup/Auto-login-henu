# 更新日志

所有重要的项目更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

## [2.0.0] - 2025-10-13

### 新增 ✨

#### 核心功能
- 🏗️ **模块化架构**：全新的模块化设计，易于维护和扩展
  - `henu_login_lib.py`: 核心登录库
  - `config_manager.py`: 配置管理
  - `credential_manager.py`: 凭证加密
  - `logger_setup.py`: 日志系统
  
- 📝 **配置文件支持**：
  - JSON格式配置文件
  - YAML格式支持（可选）
  - 环境变量配置支持
  - 配置文件模板（config.json.example）

- 🔐 **安全特性**：
  - 凭证加密存储（使用Fernet对称加密）
  - 自动密钥生成和管理
  - 文件权限保护建议

- 📊 **日志系统**：
  - 多级别日志（DEBUG, INFO, WARNING, ERROR, CRITICAL）
  - 日志轮转（自动限制文件大小）
  - 控制台和文件双输出
  - 详细的日志格式

- 🔄 **智能重试机制**：
  - 可配置重试次数
  - 可配置重试延迟
  - 失败自动重试

- ⏰ **定时检查**：
  - 守护进程模式（`--daemon`）
  - 可配置检查间隔
  - 断网自动重连

#### 跨平台支持

- 🖥️ **Windows支持**：
  - BAT批处理脚本
  - 任务计划程序自动安装脚本
  - 开机自启支持
  - 定时检查支持

- 🐧 **Linux支持**：
  - Shell脚本包装器
  - systemd服务单元
  - 自动安装/卸载脚本
  - 日志集成到journalctl

- 🍎 **macOS支持**：
  - Shell脚本包装器
  - LaunchAgent配置
  - 自动安装/卸载脚本
  - 用户级服务支持

#### Web界面

- 🌐 **Flask Web服务**：
  - 现代化的响应式UI
  - 实时状态监控
  - 快速登录功能
  - 自动登录控制
  - 日志查看功能
  - RESTful API接口

#### 命令行工具

- 🎯 **增强的CLI**：
  - `--daemon`: 守护进程模式
  - `--status`: 状态查看
  - `--config`: 自定义配置文件
  - `--version`: 版本信息
  - 详细的帮助信息

#### 文档

- 📚 **完整文档**：
  - README_ENHANCED.md: 完整功能说明
  - INSTALL.md: 详细安装指南
  - FAQ.md: 常见问题解答
  - CHANGELOG.md: 更新日志
  - 更新的README.md

### 改进 🔧

- ♻️ **代码质量**：
  - 完整的类型注解
  - 异常处理优化
  - 代码注释完善
  - PEP 8风格遵循

- 🎨 **用户体验**：
  - 友好的错误信息
  - 彩色终端输出（Linux/macOS）
  - 进度提示
  - 详细的状态反馈

- 🔍 **调试支持**：
  - 详细的日志输出
  - 调试模式支持
  - 错误堆栈跟踪
  - 网络请求日志

### 技术栈

- Python 3.7+
- requests >= 2.31.0
- cryptography >= 41.0.0 (可选)
- pyyaml >= 6.0 (可选)
- flask >= 3.0.0 (Web界面)
- flask-cors >= 4.0.0 (Web界面)

### 文件结构

```
新增文件（21个）:
├── auto_login_enhanced.py      # 增强版主程序
├── henu_login_lib.py           # 核心库
├── config_manager.py           # 配置管理
├── credential_manager.py       # 凭证加密
├── logger_setup.py             # 日志配置
├── web_interface.py            # Web界面
├── config.json.example         # 配置模板
├── requirements.txt            # 依赖列表
├── .gitignore                  # Git忽略规则
├── README_ENHANCED.md          # 增强版文档
├── INSTALL.md                  # 安装指南
├── FAQ.md                      # 常见问题
├── CHANGELOG.md                # 更新日志
├── scripts/
│   ├── windows/
│   │   ├── auto_login.bat
│   │   ├── install_service.bat
│   │   └── uninstall_service.bat
│   ├── linux/
│   │   ├── auto_login.sh
│   │   ├── install_service.sh
│   │   └── uninstall_service.sh
│   └── macos/
│       ├── auto_login.sh
│       ├── install_service.sh
│       └── uninstall_service.sh
└── web_templates/
    └── index.html              # Web界面HTML
```

### 兼容性

- ✅ 保持原有`auto_login.py`功能完整
- ✅ 向后兼容，可与原版本共存
- ✅ 新旧版本可独立使用

### 升级指南

从1.0升级到2.0：

1. 备份现有配置（如有）
2. 下载新版本文件
3. 创建配置文件：`cp config.json.example config.json`
4. 填入账号信息
5. 安装依赖：`pip install -r requirements.txt`
6. 运行增强版：`python3 auto_login_enhanced.py`

### 已知问题

- Web界面在某些旧版浏览器可能显示异常（建议使用Chrome/Edge/Firefox最新版）
- Windows防火墙可能阻止Web界面访问（需手动添加规则）

---

## [1.0.0] - 初始版本

### 功能

- ✅ 基本登录功能
- ✅ 网络状态检查
- ✅ 支持多运营商
- ✅ 简单的错误处理

### 文件

- auto_login.py: 主程序
- README.md: 基础说明

---

## 版本说明

### 版本号规则

遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范：

- 主版本号：不兼容的API修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

### 变更类型

- **新增**：新功能
- **改进**：对现有功能的改进
- **修复**：问题修复
- **废弃**：即将移除的功能
- **移除**：已移除的功能
- **安全**：安全性改进
