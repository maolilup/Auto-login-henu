"""
凭证管理器
提供安全的凭证加密和解密功能
"""

import os
import base64
import logging
from pathlib import Path
from typing import Dict, Optional

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


class CredentialManager:
    """凭证加密管理器"""
    
    def __init__(self, key_file: str = ".keyfile"):
        """
        初始化凭证管理器
        
        Args:
            key_file: 密钥文件路径
        """
        self.logger = logging.getLogger(__name__)
        self.key_file = key_file
        self.cipher = None
        
        if not CRYPTO_AVAILABLE:
            self.logger.warning("cryptography库未安装，凭证加密功能不可用")
        else:
            self._initialize_cipher()
    
    def _initialize_cipher(self) -> None:
        """初始化加密器"""
        if not CRYPTO_AVAILABLE:
            return
        
        try:
            key = self._load_or_create_key()
            self.cipher = Fernet(key)
            self.logger.debug("加密器初始化成功")
        except Exception as e:
            self.logger.error(f"初始化加密器失败: {e}", exc_info=True)
    
    def _load_or_create_key(self) -> bytes:
        """加载或创建加密密钥"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                key = f.read()
            self.logger.debug(f"从文件加载密钥: {self.key_file}")
        else:
            key = Fernet.generate_key()
            self._save_key(key)
            self.logger.info(f"生成新密钥并保存到: {self.key_file}")
        
        return key
    
    def _save_key(self, key: bytes) -> None:
        """保存密钥到文件"""
        # 确保密钥文件的目录存在
        key_dir = os.path.dirname(self.key_file)
        if key_dir:
            os.makedirs(key_dir, exist_ok=True)
        
        with open(self.key_file, 'wb') as f:
            f.write(key)
        
        # 设置文件权限为仅所有者可读写（Unix系统）
        try:
            os.chmod(self.key_file, 0o600)
        except:
            pass
    
    def encrypt(self, plaintext: str) -> Optional[str]:
        """
        加密字符串
        
        Args:
            plaintext: 明文
            
        Returns:
            加密后的Base64编码字符串，失败返回None
        """
        if not CRYPTO_AVAILABLE or not self.cipher:
            self.logger.warning("加密功能不可用")
            return None
        
        try:
            encrypted = self.cipher.encrypt(plaintext.encode())
            return base64.b64encode(encrypted).decode()
        except Exception as e:
            self.logger.error(f"加密失败: {e}", exc_info=True)
            return None
    
    def decrypt(self, ciphertext: str) -> Optional[str]:
        """
        解密字符串
        
        Args:
            ciphertext: Base64编码的密文
            
        Returns:
            解密后的明文，失败返回None
        """
        if not CRYPTO_AVAILABLE or not self.cipher:
            self.logger.warning("解密功能不可用")
            return None
        
        try:
            encrypted = base64.b64decode(ciphertext.encode())
            decrypted = self.cipher.decrypt(encrypted)
            return decrypted.decode()
        except Exception as e:
            self.logger.error(f"解密失败: {e}", exc_info=True)
            return None
    
    def encrypt_credentials(self, username: str, password: str, operator: str = "local") -> Dict[str, str]:
        """
        加密凭证
        
        Args:
            username: 用户名
            password: 密码
            operator: 运营商
            
        Returns:
            包含加密后凭证的字典
        """
        return {
            'username': self.encrypt(username) or username,
            'password': self.encrypt(password) or password,
            'operator': operator,
            'encrypted': CRYPTO_AVAILABLE and self.cipher is not None
        }
    
    def decrypt_credentials(self, encrypted_creds: Dict[str, str]) -> Dict[str, str]:
        """
        解密凭证
        
        Args:
            encrypted_creds: 包含加密凭证的字典
            
        Returns:
            包含明文凭证的字典
        """
        if not encrypted_creds.get('encrypted', False):
            # 凭证未加密，直接返回
            return {
                'username': encrypted_creds.get('username', ''),
                'password': encrypted_creds.get('password', ''),
                'operator': encrypted_creds.get('operator', 'local')
            }
        
        return {
            'username': self.decrypt(encrypted_creds.get('username', '')) or '',
            'password': self.decrypt(encrypted_creds.get('password', '')) or '',
            'operator': encrypted_creds.get('operator', 'local')
        }
    
    @staticmethod
    def is_available() -> bool:
        """检查加密功能是否可用"""
        return CRYPTO_AVAILABLE
