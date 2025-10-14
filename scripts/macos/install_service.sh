#!/bin/bash
# 安装macOS LaunchAgent - 开机自动登录

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "河南大学校园网自动登录 - 服务安装"
echo "========================================"
echo

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PLIST_NAME="com.henu.autologin"
PLIST_FILE="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"

# 创建LaunchAgents目录（如果不存在）
mkdir -p "$HOME/Library/LaunchAgents"

# 检查plist是否已存在
if [ -f "$PLIST_FILE" ]; then
    echo -e "${YELLOW}服务已存在${NC}"
    read -p "是否删除并重新创建？(y/n): " CHOICE
    if [ "$CHOICE" = "y" ] || [ "$CHOICE" = "Y" ]; then
        launchctl unload "$PLIST_FILE" 2>/dev/null
        rm "$PLIST_FILE"
        echo "已删除旧服务"
    else
        echo "安装取消"
        exit 0
    fi
fi

# 获取Python3路径
PYTHON3_PATH=$(which python3)

# 创建plist文件
echo "正在创建LaunchAgent配置文件..."
cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_NAME}</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON3_PATH}</string>
        <string>${SCRIPT_DIR}/auto_login_enhanced.py</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>${SCRIPT_DIR}</string>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>StartInterval</key>
    <integer>300</integer>
    
    <key>StandardOutPath</key>
    <string>${HOME}/Library/Logs/henu_autologin.log</string>
    
    <key>StandardErrorPath</key>
    <string>${HOME}/Library/Logs/henu_autologin_error.log</string>
    
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
EOF

# 设置文件权限
chmod 644 "$PLIST_FILE"

# 加载服务
echo "正在加载服务..."
launchctl load "$PLIST_FILE"

if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo -e "${GREEN}安装成功！${NC}"
    echo "========================================"
    echo
    echo "服务名称: ${PLIST_NAME}"
    echo "配置文件: ${PLIST_FILE}"
    echo "触发条件: "
    echo "  - 用户登录时"
    echo "  - 每5分钟检查一次"
    echo
    echo "日志文件:"
    echo "  标准输出: ${HOME}/Library/Logs/henu_autologin.log"
    echo "  错误输出: ${HOME}/Library/Logs/henu_autologin_error.log"
    echo
    echo "常用命令:"
    echo "  立即运行: launchctl start ${PLIST_NAME}"
    echo "  停止服务: launchctl stop ${PLIST_NAME}"
    echo "  卸载服务: launchctl unload ${PLIST_FILE}"
    echo "  查看日志: tail -f ${HOME}/Library/Logs/henu_autologin.log"
    echo
else
    echo -e "${RED}错误: 服务加载失败${NC}"
    exit 1
fi
