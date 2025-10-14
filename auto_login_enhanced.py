#!/usr/bin/env python3
"""
河南大学校园网自动登录工具（增强版）
支持配置文件、日志、加密、重试机制、定时检查等生产级功能
"""

import sys
import time
import argparse
import signal
from typing import Optional

from henu_login_lib import NetworkChecker, HENUAuthenticator, HENULoginError
from config_manager import ConfigManager
from credential_manager import CredentialManager
from logger_setup import LoggerSetup


class AutoLoginService:
    """自动登录服务"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化自动登录服务
        
        Args:
            config_file: 配置文件路径
        """
        # 加载配置
        self.config_manager = ConfigManager(config_file)
        
        # 设置日志
        log_config = self.config_manager.config.get('logging', {})
        self.logger = LoggerSetup.setup_logger(
            level=log_config.get('level', 'INFO'),
            log_file=log_config.get('file', 'auto_login.log'),
            max_size_mb=log_config.get('max_size_mb', 10),
            backup_count=log_config.get('backup_count', 5),
            console_output=log_config.get('console_output', True)
        )
        
        # 初始化凭证管理器
        security_config = self.config_manager.config.get('security', {})
        self.credential_manager = CredentialManager(
            security_config.get('encryption_key_file', '.keyfile')
        )
        
        # 初始化网络检查器和认证器
        network_config = self.config_manager.config.get('network', {})
        self.network_checker = NetworkChecker(
            test_url=network_config.get('test_url', 'http://www.baidu.com'),
            timeout=network_config.get('timeout', 5)
        )
        self.authenticator = HENUAuthenticator(
            timeout=network_config.get('timeout', 10)
        )
        
        # 运行控制
        self.running = True
        self.setup_signal_handlers()
    
    def setup_signal_handlers(self):
        """设置信号处理器"""
        def signal_handler(signum, frame):
            self.logger.info(f"收到信号 {signum}，准备退出...")
            self.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def login_with_retry(self) -> bool:
        """
        带重试机制的登录
        
        Returns:
            是否登录成功
        """
        network_config = self.config_manager.config.get('network', {})
        retry_attempts = network_config.get('retry_attempts', 3)
        retry_delay = network_config.get('retry_delay', 5)
        login_url = network_config.get('login_url', '')
        
        # 获取凭证
        creds = self.config_manager.get_credentials()
        
        # 验证配置
        is_valid, errors = self.config_manager.validate_config()
        if not is_valid:
            self.logger.error("配置验证失败:")
            for error in errors:
                self.logger.error(f"  - {error}")
            return False
        
        # 尝试登录
        for attempt in range(1, retry_attempts + 1):
            try:
                self.logger.info(f"尝试登录 ({attempt}/{retry_attempts})...")
                
                success = self.authenticator.login(
                    url=login_url,
                    username=creds['username'],
                    password=creds['password'],
                    operator=creds['operator']
                )
                
                if success:
                    self.logger.info("登录成功！")
                    return True
                else:
                    self.logger.warning(f"登录失败，尝试 {attempt}/{retry_attempts}")
                    
            except HENULoginError as e:
                self.logger.error(f"登录错误: {e}")
            except Exception as e:
                self.logger.error(f"未知错误: {e}", exc_info=True)
            
            # 如果不是最后一次尝试，等待后重试
            if attempt < retry_attempts:
                self.logger.info(f"等待 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
        
        self.logger.error(f"登录失败，已重试 {retry_attempts} 次")
        return False
    
    def run_once(self) -> bool:
        """
        运行一次登录检查
        
        Returns:
            是否需要继续运行
        """
        try:
            # 检查网络连接
            if self.network_checker.check_internet_connection():
                self.logger.info("网络连接正常，无需登录")
                return True
            
            # 网络未连接，尝试登录
            self.logger.info("检测到网络未连接，准备登录...")
            self.login_with_retry()
            return True
            
        except KeyboardInterrupt:
            self.logger.info("用户中断操作")
            return False
        except Exception as e:
            self.logger.error(f"运行时错误: {e}", exc_info=True)
            return True
    
    def run_daemon(self):
        """以守护进程模式运行"""
        scheduler_config = self.config_manager.config.get('scheduler', {})
        check_interval = scheduler_config.get('check_interval', 300)
        
        self.logger.info(f"启动守护进程模式，检查间隔: {check_interval} 秒")
        
        while self.running:
            try:
                if not self.run_once():
                    break
                
                if self.running:
                    self.logger.info(f"等待 {check_interval} 秒后进行下一次检查...")
                    time.sleep(check_interval)
                    
            except KeyboardInterrupt:
                self.logger.info("用户中断，退出守护进程")
                break
            except Exception as e:
                self.logger.error(f"守护进程运行错误: {e}", exc_info=True)
                time.sleep(30)  # 发生错误时等待30秒后重试
        
        self.logger.info("守护进程已停止")
    
    def show_status(self):
        """显示当前状态"""
        print("=" * 60)
        print("河南大学校园网自动登录工具 - 状态信息")
        print("=" * 60)
        
        # 网络状态
        print("\n[网络状态]")
        is_connected = self.network_checker.check_internet_connection()
        print(f"  网络连接: {'正常' if is_connected else '未连接'}")
        
        # 认证器状态
        print("\n[认证状态]")
        status = self.authenticator.get_status()
        print(f"  上次登录时间: {status['last_login_time'] or '从未登录'}")
        print(f"  累计登录次数: {status['login_count']}")
        print(f"  会话状态: {'活跃' if status['session_active'] else '未激活'}")
        
        # 配置信息
        print("\n[配置信息]")
        print(f"  配置文件: {self.config_manager.config_file}")
        creds = self.config_manager.get_credentials()
        print(f"  用户名: {creds['username']}")
        print(f"  运营商: {creds['operator']}")
        
        network_config = self.config_manager.config.get('network', {})
        print(f"  登录URL: {network_config.get('login_url', '未配置')}")
        
        scheduler_config = self.config_manager.config.get('scheduler', {})
        print(f"  定时检查: {'启用' if scheduler_config.get('enabled') else '禁用'}")
        if scheduler_config.get('enabled'):
            print(f"  检查间隔: {scheduler_config.get('check_interval', 300)} 秒")
        
        print("\n" + "=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='河南大学校园网自动登录工具（增强版）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                    # 运行一次登录检查
  %(prog)s --daemon           # 以守护进程模式运行
  %(prog)s --status           # 显示状态信息
  %(prog)s --config custom.json  # 使用自定义配置文件
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        help='配置文件路径',
        default=None
    )
    
    parser.add_argument(
        '--daemon', '-d',
        action='store_true',
        help='以守护进程模式运行'
    )
    
    parser.add_argument(
        '--status', '-s',
        action='store_true',
        help='显示状态信息'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='%(prog)s 2.0.0'
    )
    
    args = parser.parse_args()
    
    try:
        service = AutoLoginService(config_file=args.config)
        
        if args.status:
            service.show_status()
        elif args.daemon:
            service.run_daemon()
        else:
            service.run_once()
            
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
