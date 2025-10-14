#!/bin/bash
# 河南大学校园网自动登录脚本 - Linux版本

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$SCRIPT_DIR"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到Python3，请先安装Python 3.7或更高版本${NC}"
    exit 1
fi

# 检查依赖是否安装
echo "检查依赖..."
if ! python3 -c "import requests" &> /dev/null; then
    echo "正在安装依赖..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}错误: 依赖安装失败${NC}"
        exit 1
    fi
fi

# 检查配置文件
if [ ! -f "config.json" ]; then
    if [ -f "config.json.example" ]; then
        echo -e "${YELLOW}警告: 未找到config.json，正在从config.json.example复制...${NC}"
        cp config.json.example config.json
        echo -e "${YELLOW}请编辑config.json文件，填入您的账号信息${NC}"
        echo "按Enter键继续编辑配置文件..."
        read
        ${EDITOR:-nano} config.json
    else
        echo -e "${RED}错误: 未找到配置文件${NC}"
        exit 1
    fi
fi

# 运行自动登录程序
echo -e "${GREEN}正在启动自动登录...${NC}"
python3 auto_login_enhanced.py "$@"
