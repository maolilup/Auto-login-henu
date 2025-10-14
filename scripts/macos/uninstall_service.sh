#!/bin/bash
# 卸载macOS LaunchAgent

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "河南大学校园网自动登录 - 服务卸载"
echo "========================================"
echo

PLIST_NAME="com.henu.autologin"
PLIST_FILE="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"

# 检查服务是否存在
if [ ! -f "$PLIST_FILE" ]; then
    echo -e "${YELLOW}服务未安装${NC}"
    exit 0
fi

# 卸载服务
echo "正在卸载服务..."
launchctl unload "$PLIST_FILE" 2>/dev/null

# 删除plist文件
rm "$PLIST_FILE"

echo
echo -e "${GREEN}服务已成功卸载！${NC}"
echo

# 询问是否删除日志文件
read -p "是否删除日志文件？(y/n): " DELETE_LOGS
if [ "$DELETE_LOGS" = "y" ] || [ "$DELETE_LOGS" = "Y" ]; then
    rm -f "${HOME}/Library/Logs/henu_autologin.log"
    rm -f "${HOME}/Library/Logs/henu_autologin_error.log"
    echo "日志文件已删除"
fi
