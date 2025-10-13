"""
河南大学校园网自动登录核心库
提供生产级别的网络认证功能，支持完整的错误处理、日志记录和安全特性
"""

import socket
import requests
import time
import urllib.parse
import json
import logging
from typing import Tuple, Optional, Dict, Any
from datetime import datetime


class HENULoginError(Exception):
    """HENU登录相关的自定义异常"""
    pass


class NetworkChecker:
    """网络连接检查器"""
    
    def __init__(self, test_url: str = "http://www.baidu.com", timeout: int = 5):
        self.test_url = test_url
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
    
    def check_internet_connection(self) -> bool:
        """
        检查网络连接状态，主要检查是否能访问外网
        
        Returns:
            bool: True表示网络正常，False表示需要登录
        """
        try:
            self.logger.info(f"正在检查网络连接，访问 {self.test_url} ...")
            temp_session = requests.Session()
            temp_response = temp_session.get(self.test_url, timeout=self.timeout)
            
            if temp_response.status_code == 200:
                response_text_lower = temp_response.text.lower()
                if 'baidu' in response_text_lower or '搜索' in response_text_lower:
                    self.logger.info(f"网络连接正常，能够访问 {self.test_url}")
                    return True
                else:
                    self.logger.warning(f"访问 {self.test_url} 返回200但内容不符合预期，可能被重定向到登录页")
                    return False
            else:
                self.logger.warning(f"访问 {self.test_url} 返回状态码 {temp_response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            self.logger.warning(f"访问 {self.test_url} 超时")
            return False
        except requests.exceptions.ConnectionError:
            self.logger.warning(f"无法连接到 {self.test_url}")
            return False
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"访问 {self.test_url} 发生请求异常: {e}")
            return False
        except Exception as e:
            self.logger.error(f"网络检查发生未知错误: {e}", exc_info=True)
            return False


class HENUAuthenticator:
    """河南大学网络认证器"""
    
    # 运营商后缀映射
    OPERATOR_SUFFIXES = {
        "local": "@henulocal",
        "yd": "@henuyd",
        "lt": "@henult",
        "dx": "@henudx"
    }
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.last_login_time: Optional[datetime] = None
        self.login_count = 0
    
    def login(self, url: str, username: str, password: str, operator: str = "local") -> bool:
        """
        执行登录操作
        
        Args:
            url: 登录URL，包含wlanuserip和wlanacname参数
            username: 用户名
            password: 密码
            operator: 运营商类型（local/yd/lt/dx）
            
        Returns:
            bool: 登录是否成功
            
        Raises:
            HENULoginError: 登录过程中的错误
        """
        try:
            start_time = time.time()
            self.logger.info(f"开始登录流程，用户: {username}, 运营商: {operator}")
            
            # 获取运营商后缀
            operator_suffix = self.OPERATOR_SUFFIXES.get(operator, "@henulocal")
            full_username = username + operator_suffix
            
            # 设置请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': url
            }
            
            # 1. 获取登录页面，提取URL参数
            self.logger.debug("步骤1: 获取登录页面参数")
            wlanuserip, wlanacname = self._extract_url_params(url)
            
            # 2. 认证接口
            self.logger.debug("步骤2: 调用认证接口")
            self._call_auth_api(username, password, operator_suffix, headers)
            
            # 3. 检查用户接口
            self.logger.debug("步骤3: 调用用户检查接口")
            self._call_check_api(username, password, operator_suffix, headers)
            
            # 4. 最终认证请求
            self.logger.debug("步骤4: 发起最终认证请求")
            success = self._final_authentication(
                full_username, password, wlanuserip, wlanacname, url, headers
            )
            
            elapsed_time = time.time() - start_time
            
            if success:
                self.last_login_time = datetime.now()
                self.login_count += 1
                self.logger.info(f"登录成功！耗时: {elapsed_time:.2f}秒, 累计登录次数: {self.login_count}")
            else:
                self.logger.error(f"登录失败！耗时: {elapsed_time:.2f}秒")
            
            return success
            
        except HENULoginError as e:
            self.logger.error(f"登录过程中发生错误: {e}", exc_info=True)
            raise
        except Exception as e:
            self.logger.error(f"登录过程中发生未知错误: {e}", exc_info=True)
            raise HENULoginError(f"登录失败: {str(e)}")
    
    def _extract_url_params(self, url: str) -> Tuple[str, str]:
        """从URL中提取wlanuserip和wlanacname参数"""
        try:
            parsed_url = urllib.parse.urlparse(url)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            wlanuserip = query_params.get('wlanuserip', [None])[0]
            wlanacname = query_params.get('wlanacname', [None])[0]
            
            if not wlanuserip or not wlanacname:
                raise HENULoginError("无法从URL获取 wlanuserip 或 wlanacname 参数")
            
            self.logger.debug(f"提取参数: wlanuserip={wlanuserip}, wlanacname={wlanacname}")
            return wlanuserip, wlanacname
            
        except Exception as e:
            raise HENULoginError(f"解析URL参数失败: {str(e)}")
    
    def _call_auth_api(self, username: str, password: str, operator_suffix: str, headers: Dict) -> None:
        """调用认证API"""
        auth_url = "http://172.29.35.27:8088/aaa-auth/api/v1/auth"
        auth_data = {
            'campusCode': '92c8c96e4c37100777c7190b76d28233',
            'username': username,
            'password': password,
            'operatorSuffix': operator_suffix
        }
        
        try:
            response = self.session.post(auth_url, data=auth_data, timeout=self.timeout, headers=headers)
            self.logger.debug(f"认证API响应: {response.text}")
            
            try:
                result = response.json()
                if result.get('code') not in [1, -1]:
                    msg = result.get('msg', '未知错误')
                    self.logger.warning(f"认证API返回警告: {msg}")
                else:
                    self.logger.debug("认证API调用成功")
            except json.JSONDecodeError:
                self.logger.debug("认证API响应非JSON格式，继续执行")
                
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"认证API调用失败: {e}，继续尝试登录")
    
    def _call_check_api(self, username: str, password: str, operator_suffix: str, headers: Dict) -> None:
        """调用用户检查API"""
        check_url = "http://172.29.35.27:8882/user/check-only"
        check_data = {
            'username': username,
            'password': password,
            'operatorSuffix': operator_suffix
        }
        
        try:
            response = self.session.post(check_url, data=check_data, timeout=self.timeout, headers=headers)
            self.logger.debug(f"检查API响应: {response.text}")
            
            try:
                result = response.json()
                if result.get('code') not in [1, -1]:
                    msg = result.get('msg', '未知错误')
                    self.logger.warning(f"检查API返回警告: {msg}")
                else:
                    self.logger.debug("检查API调用成功")
            except json.JSONDecodeError:
                self.logger.debug("检查API响应非JSON格式，继续执行")
                
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"检查API调用失败: {e}，继续尝试登录")
    
    def _final_authentication(self, full_username: str, password: str, wlanuserip: str, 
                             wlanacname: str, original_url: str, headers: Dict) -> bool:
        """执行最终的认证请求"""
        quickauth_base_url = "http://172.29.35.36:6060/quickauth.do"
        quickauth_params = {
            'userid': full_username,
            'passwd': password,
            'wlanuserip': wlanuserip,
            'wlanacname': wlanacname,
            'wlanacIp': '172.22.254.253',
            'ssid': '',
            'vlan': '',
            'mac': '',
            'version': '0',
            'portalpageid': '9',
            'timestamp': int(time.time() * 1000),
            'uuid': '83206179-4e59-4357-afd1-b0bd2d670f26',
            'portaltype': '0',
            'hostname': '',
            'bindCtrlId': ''
        }
        
        quickauth_url = quickauth_base_url + '?' + urllib.parse.urlencode(
            quickauth_params, quote_via=urllib.parse.quote
        )
        
        try:
            self.logger.debug(f"发起最终认证请求: {quickauth_url}")
            response = self.session.get(quickauth_url, headers=headers, timeout=self.timeout)
            
            self.logger.debug(f"最终认证响应状态码: {response.status_code}")
            self.logger.debug(f"最终认证响应内容: {response.text[:200]}...")
            
            if response.status_code != 200:
                self.logger.error(f"最终认证请求失败，状态码: {response.status_code}")
                return False
            
            # 检查响应内容
            if 'error' in response.text.lower() or 'fail' in response.text.lower():
                self.logger.error("认证响应包含错误信息")
                return False
            
            # 验证是否能访问外网
            return self._verify_internet_access()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"最终认证请求异常: {e}")
            return False
    
    def _verify_internet_access(self) -> bool:
        """验证是否能访问外网"""
        try:
            test_response = self.session.get("http://www.baidu.com", timeout=5)
            if test_response.status_code == 200 and len(test_response.text) > 500:
                if 'baidu' in test_response.text.lower() or '搜索' in test_response.text:
                    self.logger.info("验证成功：能够访问外网")
                    return True
            
            self.logger.warning("验证失败：无法正常访问外网")
            return False
            
        except requests.RequestException as e:
            self.logger.warning(f"验证访问外网时发生异常: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """获取认证器状态信息"""
        return {
            'last_login_time': self.last_login_time.isoformat() if self.last_login_time else None,
            'login_count': self.login_count,
            'session_active': bool(self.session.cookies)
        }
