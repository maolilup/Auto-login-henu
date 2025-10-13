import socket
import requests
import time
import urllib.parse
import json


def check_internet_connection():
    """
       检查网络连接状态，主要检查是否能访问外网（通过访问百度）。
       """
    test_url = "http://www.baidu.com"

    try:
        print(f"正在尝试访问 {test_url} ...")
        # 创建一个临时session，避免影响主登录流程
        temp_session = requests.Session()
        # 设置一个较短的超时时间
        temp_response = temp_session.get(
            test_url,
            timeout=5
        )

        # 如果状态码是 200，并且页面内容包含 'baidu' 或 '搜索'
        if temp_response.status_code == 200:
            response_text_lower = temp_response.text.lower()
            if 'baidu' in response_text_lower or '搜索' in response_text_lower:
                print(f"网络检查: 能够访问 {test_url}，网络连接正常。")
                return True
            else:
                # 如果返回200但内容不匹配预期（例如，返回了登录页），则认为网络不正常
                print(f"网络检查: 访问 {test_url} 返回200但内容不符合预期（可能被重定向到登录页），网络连接可能有问题。")
                return False
        else:
            print(f"网络检查: 访问 {test_url} 返回状态码 {temp_response.status_code}，网络连接可能有问题。")
            return False

    except requests.exceptions.Timeout:
        print(f"网络检查: 访问 {test_url} 超时。")
        return False
    except requests.exceptions.ConnectionError:
        print(f"网络检查: 无法连接到 {test_url}。")
        return False
    except requests.exceptions.RequestException as e:
        print(f"网络检查: 访问 {test_url} 发生请求异常: {e}")
        return False
    except Exception as e:
        print(f"网络检查: 访问 {test_url} 发生未知错误: {e}")
        return False


def login_henu(url, username, password, operator="local"):
    """
    登录河南大学网络认证系统
    """
    # 运营商后缀映射
    operator_suffixes = {
        "local": "@henulocal",
        "yd": "@henuyd",
        "lt": "@henult",
        "dx": "@henudx"
    }
    operator_suffix = operator_suffixes.get(operator, "@henulocal")
    full_username = username + operator_suffix

    # 创建session对象
    session = requests.Session()

    try:
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': url
        }

        # 1. 获取登录页面，提取URL参数
        print("正在获取登录页面...")
        response = session.get(url, headers=headers)
        response.encoding = 'utf-8'  # 确保编码正确
        # 从原始URL中提取 wlanuserip 和 wlanacname
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        wlanuserip = query_params.get('wlanuserip', [None])[0]
        wlanacname = query_params.get('wlanacname', [None])[0]

        if not wlanuserip or not wlanacname:
            print("错误：无法从URL获取 wlanuserip 或 wlanacname")
            return False

        # 2. 认证接口 (auth API)
        auth_url = "http://172.29.35.27:8088/aaa-auth/api/v1/auth"
        print("正在进行认证...")
        auth_data = {
            'campusCode': '92c8c96e4c37100777c7190b76d28233',
            'username': username,
            'password': password,
            'operatorSuffix': operator_suffix
        }
        auth_response = session.post(auth_url, data=auth_data, timeout=10, headers=headers)
        print(f"认证响应: {auth_response.text}")

        # 3. 检查认证结果
        try:
            auth_result = auth_response.json()
            if auth_result.get('code') in [1, -1]:
                print("认证成功或跳过认证")
            else:
                print(f"认证失败: {auth_result.get('msg', '未知错误')}")
                return False
        except:
            print("认证响应格式异常，继续尝试登录")

        # 4. 检查用户接口 (check API)
        check_url = "http://172.29.35.27:8882/user/check-only"
        print("正在检查用户...")
        check_data = {
            'username': username,
            'password': password,
            'operatorSuffix': operator_suffix
        }
        check_response = session.post(check_url, data=check_data, timeout=10, headers=headers)
        print(f"检查响应: {check_response.text}")

        # 5. 检查结果
        try:
            check_result = check_response.json()
            if check_result.get('code') in [1, -1]:
                print("检查成功或跳过检查")
            else:
                print(f"检查失败: {check_result.get('msg', '未知错误')}")
                return False
        except:
            print("检查响应格式异常，继续尝试登录")

        # 6. 发起最终的 quickauth 请求 (模拟 $("#loginsubmit").click() 后的行为)
        # 构建 quickauth.do 的URL参数
        # 要实际抓捕出来，或者直接抓出来喂给ai
        quickauth_base_url = "http://172.29.35.36:6060/quickauth.do"
        quickauth_params = {
            'userid': full_username,
            'passwd': password,
            'wlanuserip': wlanuserip,
            'wlanacname': wlanacname,
            'wlanacIp': '172.22.254.253',  # 这个IP可能需要根据实际情况调整，或者从页面/响应中获取
            'ssid': '',  # 空
            'vlan': '',  # 空
            'mac': '',  # 空
            'version': '0',
            'portalpageid': '9',  # 这个ID可能固定，或者从页面获取
            'timestamp': int(time.time() * 1000),  # 当前时间戳 (毫秒)
            'uuid': '83206179-4e59-4357-afd1-b0bd2d670f26',  # 可以使用固定UUID或生成新的
            'portaltype': '0',
            'hostname': '',  # 空
            'bindCtrlId': ''  # 空
        }

        # 构建完整的URL
        quickauth_url = quickauth_base_url + '?' + urllib.parse.urlencode(quickauth_params,
                                                                          quote_via=urllib.parse.quote)

        print("正在发起最终认证请求...")
        print(f"请求URL: {quickauth_url}")

        final_response = session.get(quickauth_url, headers=headers, timeout=10)

        print(f"最终认证响应状态码: {final_response.status_code}")
        print(f"最终认证响应内容: {final_response.text}")

        # 检查最终登录结果
        if final_response.status_code == 200:
            try:
                response_json = final_response.json()
                # 检查响应JSON来判断登录是否成功
                # 这里需要根据实际的响应格式来判断
                # 例如，可能有 code, msg, success 等字段
                # 假设 code 为 0 或 success 为 true 表示成功
                # 示例判断（请根据实际响应调整）：
                # if response_json.get('code') == 0:
                #     print("登录成功！")
                #     return True
                # elif response_json.get('success') == True:
                #     print("登录成功！")
                #     return True
                # else:
                #     print(f"登录失败: {response_json}")
                #     return False

                # 由于不知道具体的成功/失败标识，先打印响应，根据实际内容调整判断逻辑
                print(f"服务器返回: {response_json}")
                # 如果响应不包含错误信息，可以暂时认为成功
                if 'error' not in final_response.text.lower() and 'fail' not in final_response.text.lower():
                    print("认证请求已发送，响应不包含明显错误，可能已成功。")
                    # 尝试访问外部网络验证
                    try:
                        test_response = session.get("http://www.baidu.com", timeout=5)
                        if test_response.status_code == 200 and len(test_response.text) > 500 and (
                                'baidu' in test_response.text.lower() or '搜索' in test_response.text):
                            print("验证访问成功，确认已登录！")
                            return True
                        else:
                            print("验证访问返回内容异常或失败，可能未登录。")
                            return False
                    except requests.RequestException as e:
                        print(f"验证访问失败: {e}")

                        return True
                else:
                    print("认证请求返回错误信息。")
                    return False
            except json.JSONDecodeError:
                print("最终认证响应不是JSON格式，可能失败或页面被重定向。")
                return False
        else:
            print(f"最终认证请求失败，状态码: {final_response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
        return False
    except Exception as e:
        print(f"登录过程中发生错误: {e}")
        return False


if __name__ == "__main__":
    if  not check_internet_connection():
        login_url = "http://172.29.35.36:6060/portalReceiveAction.do?wlanuserip=10.16.211.160&wlanacname=HD-SuShe-ME60"
        #实际抓包的url
        username = "你的账号"
        password = "你的密码"
        success = login_henu(login_url, username, password, "你的运营商")

        if success:
            print("登录成功！")
        else:
            print("登录失败！")
    else:
        print("网络正常")
