#!/bin/bash
# 安装Linux systemd服务 - 开机自动登录

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}错误: 需要root权限运行此脚本${NC}"
    echo "请使用 sudo 运行: sudo $0"
    exit 1
fi

echo "========================================"
echo "河南大学校园网自动登录 - 服务安装"
echo "========================================"
echo

# 获取实际用户（不是root）
REAL_USER="${SUDO_USER:-$USER}"
if [ "$REAL_USER" = "root" ]; then
    echo -e "${YELLOW}警告: 检测到以root用户身份运行${NC}"
    echo -n "请输入要运行服务的用户名: "
    read REAL_USER
fi

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SERVICE_NAME="henu-autologin"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
TIMER_FILE="/etc/systemd/system/${SERVICE_NAME}.timer"

# 检查systemd是否可用
if ! command -v systemctl &> /dev/null; then
    echo -e "${RED}错误: 未找到systemd，此脚本仅支持使用systemd的Linux发行版${NC}"
    exit 1
fi

# 创建systemd service文件
echo "正在创建服务文件..."
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=HENU Campus Network Auto Login Service
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=$REAL_USER
WorkingDirectory=$SCRIPT_DIR
ExecStart=/usr/bin/python3 $SCRIPT_DIR/auto_login_enhanced.py
StandardOutput=journal
StandardError=journal
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF

# 创建systemd timer文件（每5分钟检查一次）
echo "正在创建定时器文件..."
cat > "$TIMER_FILE" << EOF
[Unit]
Description=HENU Campus Network Auto Login Timer
Requires=${SERVICE_NAME}.service

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min
Unit=${SERVICE_NAME}.service

[Install]
WantedBy=timers.target
EOF

# 重新加载systemd配置
echo "重新加载systemd配置..."
systemctl daemon-reload

# 启用并启动服务
echo "启用服务..."
systemctl enable "${SERVICE_NAME}.timer"
systemctl start "${SERVICE_NAME}.timer"

# 立即运行一次
echo "立即运行一次测试..."
systemctl start "${SERVICE_NAME}.service"

echo
echo "========================================"
echo -e "${GREEN}安装成功！${NC}"
echo "========================================"
echo
echo "服务名称: ${SERVICE_NAME}"
echo "定时器: ${SERVICE_NAME}.timer"
echo "触发条件: "
echo "  - 系统启动1分钟后"
echo "  - 每5分钟检查一次"
echo
echo "常用命令:"
echo "  查看状态: systemctl status ${SERVICE_NAME}.timer"
echo "  查看日志: journalctl -u ${SERVICE_NAME}.service -f"
echo "  立即运行: sudo systemctl start ${SERVICE_NAME}.service"
echo "  停止服务: sudo systemctl stop ${SERVICE_NAME}.timer"
echo "  禁用服务: sudo systemctl disable ${SERVICE_NAME}.timer"
echo
