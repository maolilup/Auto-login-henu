#!/usr/bin/env python3
"""
河南大学校园网自动登录 - Web界面
提供Web管理界面，支持配置管理、手动登录、状态监控
"""

import os
import sys
import json
import threading
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

from henu_login_lib import NetworkChecker, HENUAuthenticator, HENULoginError
from config_manager import ConfigManager
from logger_setup import LoggerSetup

app = Flask(__name__, static_folder='web_static', template_folder='web_templates')
CORS(app)

# 全局变量
config_manager = None
authenticator = None
network_checker = None
logger = None
auto_login_thread = None
auto_login_running = False


def init_app():
    """初始化应用"""
    global config_manager, authenticator, network_checker, logger
    
    # 加载配置
    config_manager = ConfigManager()
    
    # 设置日志
    log_config = config_manager.config.get('logging', {})
    logger = LoggerSetup.setup_logger(
        level=log_config.get('level', 'INFO'),
        log_file=log_config.get('file', 'auto_login.log'),
        console_output=True
    )
    
    # 初始化组件
    network_config = config_manager.config.get('network', {})
    network_checker = NetworkChecker(
        test_url=network_config.get('test_url', 'http://www.baidu.com')
    )
    authenticator = HENUAuthenticator(timeout=network_config.get('timeout', 10))
    
    logger.info("Web界面已初始化")


def auto_login_worker():
    """自动登录工作线程"""
    global auto_login_running
    
    logger.info("自动登录线程已启动")
    
    scheduler_config = config_manager.config.get('scheduler', {})
    check_interval = scheduler_config.get('check_interval', 300)
    
    while auto_login_running:
        try:
            # 检查网络状态
            if not network_checker.check_internet_connection():
                logger.info("检测到网络未连接，尝试登录...")
                
                # 获取凭证并登录
                network_config = config_manager.config.get('network', {})
                creds = config_manager.get_credentials()
                
                authenticator.login(
                    url=network_config.get('login_url', ''),
                    username=creds['username'],
                    password=creds['password'],
                    operator=creds['operator']
                )
            
            # 等待下一次检查
            time.sleep(check_interval)
            
        except Exception as e:
            logger.error(f"自动登录线程错误: {e}", exc_info=True)
            time.sleep(30)
    
    logger.info("自动登录线程已停止")


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/status')
def get_status():
    """获取系统状态"""
    try:
        # 网络状态
        is_connected = network_checker.check_internet_connection()
        
        # 认证器状态
        auth_status = authenticator.get_status()
        
        # 配置状态
        creds = config_manager.get_credentials()
        network_config = config_manager.config.get('network', {})
        scheduler_config = config_manager.config.get('scheduler', {})
        
        return jsonify({
            'success': True,
            'data': {
                'network': {
                    'connected': is_connected,
                    'test_url': network_config.get('test_url', '')
                },
                'auth': {
                    'last_login_time': auth_status['last_login_time'],
                    'login_count': auth_status['login_count'],
                    'session_active': auth_status['session_active']
                },
                'config': {
                    'username': creds['username'],
                    'operator': creds['operator'],
                    'login_url': network_config.get('login_url', ''),
                    'auto_login_enabled': auto_login_running,
                    'check_interval': scheduler_config.get('check_interval', 300)
                },
                'timestamp': datetime.now().isoformat()
            }
        })
    except Exception as e:
        logger.error(f"获取状态失败: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/login', methods=['POST'])
def do_login():
    """执行登录"""
    try:
        data = request.json or {}
        
        # 使用请求中的凭证或配置中的凭证
        network_config = config_manager.config.get('network', {})
        creds = config_manager.get_credentials()
        
        username = data.get('username') or creds['username']
        password = data.get('password') or creds['password']
        operator = data.get('operator') or creds['operator']
        login_url = data.get('login_url') or network_config.get('login_url', '')
        
        # 验证参数
        if not all([username, password, login_url]):
            return jsonify({
                'success': False,
                'error': '缺少必需参数：username, password, login_url'
            }), 400
        
        # 执行登录
        success = authenticator.login(
            url=login_url,
            username=username,
            password=password,
            operator=operator
        )
        
        return jsonify({
            'success': success,
            'message': '登录成功' if success else '登录失败'
        })
        
    except Exception as e:
        logger.error(f"登录失败: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    """获取或更新配置"""
    if request.method == 'GET':
        # 获取配置（隐藏敏感信息）
        config = config_manager.config.copy()
        if 'credentials' in config and 'password' in config['credentials']:
            config['credentials']['password'] = '******'
        
        return jsonify({
            'success': True,
            'data': config
        })
    
    else:  # POST
        try:
            new_config = request.json
            
            # 如果密码是******，保持原密码
            if (new_config.get('credentials', {}).get('password') == '******'):
                original_password = config_manager.get('credentials.password')
                new_config['credentials']['password'] = original_password
            
            # 更新配置
            config_manager.config = new_config
            config_manager.save_config()
            
            return jsonify({
                'success': True,
                'message': '配置已更新'
            })
            
        except Exception as e:
            logger.error(f"更新配置失败: {e}", exc_info=True)
            return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auto_login', methods=['POST'])
def toggle_auto_login():
    """启动/停止自动登录"""
    global auto_login_running, auto_login_thread
    
    try:
        data = request.json or {}
        enable = data.get('enable', False)
        
        if enable and not auto_login_running:
            # 启动自动登录
            auto_login_running = True
            auto_login_thread = threading.Thread(target=auto_login_worker, daemon=True)
            auto_login_thread.start()
            
            return jsonify({
                'success': True,
                'message': '自动登录已启动'
            })
            
        elif not enable and auto_login_running:
            # 停止自动登录
            auto_login_running = False
            if auto_login_thread:
                auto_login_thread.join(timeout=5)
            
            return jsonify({
                'success': True,
                'message': '自动登录已停止'
            })
        
        return jsonify({
            'success': True,
            'message': '状态未改变'
        })
        
    except Exception as e:
        logger.error(f"切换自动登录失败: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/logs')
def get_logs():
    """获取日志"""
    try:
        log_file = config_manager.get('logging.file', 'auto_login.log')
        lines = int(request.args.get('lines', 100))
        
        if not os.path.exists(log_file):
            return jsonify({
                'success': True,
                'data': {
                    'logs': [],
                    'message': '日志文件不存在'
                }
            })
        
        # 读取最后N行日志
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
        
        return jsonify({
            'success': True,
            'data': {
                'logs': [line.strip() for line in recent_lines],
                'total_lines': len(all_lines)
            }
        })
        
    except Exception as e:
        logger.error(f"读取日志失败: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='河南大学校园网自动登录 - Web界面')
    parser.add_argument('--host', default='0.0.0.0', help='监听地址')
    parser.add_argument('--port', type=int, default=5000, help='监听端口')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    
    args = parser.parse_args()
    
    # 初始化应用
    init_app()
    
    print(f"""
    ========================================
    河南大学校园网自动登录 - Web界面
    ========================================
    
    访问地址: http://{args.host}:{args.port}
    
    按 Ctrl+C 停止服务器
    ========================================
    """)
    
    # 启动Flask应用
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
