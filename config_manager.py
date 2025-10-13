"""
配置管理器
支持JSON和YAML格式的配置文件，以及环境变量配置
"""

import json
import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """配置文件管理器"""
    
    DEFAULT_CONFIG = {
        "network": {
            "login_url": "",
            "test_url": "http://www.baidu.com",
            "timeout": 10,
            "retry_attempts": 3,
            "retry_delay": 5
        },
        "credentials": {
            "username": "",
            "password": "",
            "operator": "local"
        },
        "scheduler": {
            "enabled": False,
            "check_interval": 300,
            "auto_retry_on_failure": True
        },
        "logging": {
            "level": "INFO",
            "file": "auto_login.log",
            "max_size_mb": 10,
            "backup_count": 5,
            "console_output": True
        },
        "security": {
            "encrypt_credentials": False,
            "encryption_key_file": ".keyfile"
        }
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径，如果为None则使用默认路径
        """
        self.logger = logging.getLogger(__name__)
        self.config_file = config_file or self._find_config_file()
        self.config = self._load_config()
    
    def _find_config_file(self) -> str:
        """查找配置文件"""
        possible_locations = [
            "config.json",
            "config.yaml",
            "config.yml",
            os.path.expanduser("~/.henu_login/config.json"),
            "/etc/henu_login/config.json"
        ]
        
        for location in possible_locations:
            if os.path.exists(location):
                self.logger.info(f"找到配置文件: {location}")
                return location
        
        self.logger.warning("未找到配置文件，将使用默认配置")
        return "config.json"
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(self.config_file):
            self.logger.warning(f"配置文件 {self.config_file} 不存在，使用默认配置")
            return self.DEFAULT_CONFIG.copy()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                if self.config_file.endswith(('.yaml', '.yml')):
                    try:
                        import yaml
                        config = yaml.safe_load(f)
                    except ImportError:
                        self.logger.error("需要安装PyYAML才能读取YAML配置文件")
                        return self.DEFAULT_CONFIG.copy()
                else:
                    config = json.load(f)
            
            # 合并默认配置和用户配置
            merged_config = self._merge_configs(self.DEFAULT_CONFIG, config)
            self.logger.info(f"成功加载配置文件: {self.config_file}")
            return merged_config
            
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {e}", exc_info=True)
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """递归合并默认配置和用户配置"""
        merged = default.copy()
        for key, value in user.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        return merged
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        保存配置到文件
        
        Args:
            config: 要保存的配置，如果为None则保存当前配置
            
        Returns:
            bool: 是否保存成功
        """
        config_to_save = config or self.config
        
        try:
            # 确保目录存在
            config_dir = os.path.dirname(self.config_file)
            if config_dir:
                os.makedirs(config_dir, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                if self.config_file.endswith(('.yaml', '.yml')):
                    try:
                        import yaml
                        yaml.safe_dump(config_to_save, f, default_flow_style=False)
                    except ImportError:
                        self.logger.error("需要安装PyYAML才能保存YAML配置文件")
                        return False
                else:
                    json.dump(config_to_save, f, indent=4, ensure_ascii=False)
            
            self.logger.info(f"配置已保存到: {self.config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"保存配置文件失败: {e}", exc_info=True)
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        获取配置项
        
        Args:
            key_path: 配置项路径，使用点号分隔，如 "network.timeout"
            default: 默认值
            
        Returns:
            配置项的值
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """
        设置配置项
        
        Args:
            key_path: 配置项路径，使用点号分隔
            value: 要设置的值
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def get_credentials(self) -> Dict[str, str]:
        """
        获取认证凭据
        优先从环境变量读取，其次从配置文件读取
        
        Returns:
            包含username, password, operator的字典
        """
        return {
            'username': os.environ.get('HENU_USERNAME') or self.get('credentials.username', ''),
            'password': os.environ.get('HENU_PASSWORD') or self.get('credentials.password', ''),
            'operator': os.environ.get('HENU_OPERATOR') or self.get('credentials.operator', 'local')
        }
    
    def validate_config(self) -> tuple[bool, list[str]]:
        """
        验证配置是否有效
        
        Returns:
            (是否有效, 错误信息列表)
        """
        errors = []
        
        # 检查必需的配置项
        login_url = self.get('network.login_url')
        if not login_url:
            errors.append("缺少必需的配置项: network.login_url")
        
        creds = self.get_credentials()
        if not creds['username']:
            errors.append("缺少必需的配置项: credentials.username")
        if not creds['password']:
            errors.append("缺少必需的配置项: credentials.password")
        
        # 检查配置项的有效性
        timeout = self.get('network.timeout', 0)
        if timeout <= 0:
            errors.append("network.timeout 必须大于0")
        
        retry_attempts = self.get('network.retry_attempts', 0)
        if retry_attempts < 0:
            errors.append("network.retry_attempts 不能小于0")
        
        return len(errors) == 0, errors
