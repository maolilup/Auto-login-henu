#!/bin/bash
# 卸载Linux systemd服务

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}错误: 需要root权限运行此脚本${NC}"
    echo "请使用 sudo 运行: sudo $0"
    exit 1
fi

echo "========================================"
echo "河南大学校园网自动登录 - 服务卸载"
echo "========================================"
echo

SERVICE_NAME="henu-autologin"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
TIMER_FILE="/etc/systemd/system/${SERVICE_NAME}.timer"

# 检查服务是否存在
if [ ! -f "$SERVICE_FILE" ] && [ ! -f "$TIMER_FILE" ]; then
    echo -e "${YELLOW}服务未安装${NC}"
    exit 0
fi

# 停止并禁用服务
echo "停止服务..."
systemctl stop "${SERVICE_NAME}.timer" 2>/dev/null
systemctl stop "${SERVICE_NAME}.service" 2>/dev/null

echo "禁用服务..."
systemctl disable "${SERVICE_NAME}.timer" 2>/dev/null
systemctl disable "${SERVICE_NAME}.service" 2>/dev/null

# 删除服务文件
echo "删除服务文件..."
rm -f "$SERVICE_FILE"
rm -f "$TIMER_FILE"

# 重新加载systemd配置
echo "重新加载systemd配置..."
systemctl daemon-reload

echo
echo -e "${GREEN}服务已成功卸载！${NC}"
echo
