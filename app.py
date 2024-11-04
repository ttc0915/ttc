import streamlit as st
import requests
import time
import hashlib
import urllib
import logging

# 设置日志配置
logging.basicConfig(filename='error_log.txt', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# 定义全局设备信息
device = {
    "payload": {
        "iid": "7432390588739929861",
        "device_id": "7432390066955470341",
        "passport-sdk-version": "19",
        "ac": "wifi",
        "channel": "googleplay",
        "aid": "1233",
        "app_name": "musical_ly",
        "version_code": "320402",
        "version_name": "32.4.2",
        "device_platform": "android",
        "os": "android",
        "ab_version": "32.4.2",
        "ssmix": "a",
        "device_type": "SHARP_D9XLH",
        "device_brand": "sharp",
        "language": "en",
        "os_api": "26",
        "os_version": "8.0.0",
        "openudid": "d34d7bc383c9a34e",
        "manifest_version_code": "2023204020",
        "resolution": "1080*1920",
        "dpi": "320",
        "update_version_code": "2023204020",
        "app_type": "normal",
        "sys_region": "SG",
        "mcc_mnc": "5255",
        "timezone_name": "Asia/Singapore",
        "timezone_offset": "28800",
        "build_number": "32.4.2",
        "region": "SG",
        "carrier_region": "SG",
        "uoo": "0",
        "app_language": "en",
        "locale": "en",
        "op_region": "SG",
        "ac2": "wifi",
        "host_abi": "armeabi-v7a",
        "cdid": "841d4caf-1b90-450f-b717-b897ff555177",
        "support_webview": "1",
        "okhttp_version": "4.2.137.31-tiktok",
        "use_store_region_cookie": "1",
        "user-agent": "com.zhiliaoapp.musically/2023204020 (Linux; U; Android 8.0.0; en_SG; SHARP_D9XLH; Build/N2G48H;tt-ok/3.12.13.4-tiktok)"
    }
}

# 哈希函数
def hashed_id(value):
    if "+" in value:
        type_value = "1"
    elif "@" in value:
        type_value = "2"
    else:
        type_value = "3"
    hashed_id = value + "aDy0TUhtql92P7hScCs97YWMT-jub2q9"
    hashed_value = hashlib.sha256(hashed_id.encode()).hexdigest()
    return f"hashed_id={hashed_value}&type={type_value}"

# 获取邮箱注册状态的函数
def get_email_registration_status(email, session, device):
    try:
        params = {
            'device_id': device['payload']['device_id'],
            'ac': 'wifi',
            'channel': 'googleplay',
            'aid': '567753',
            'app_name': 'tiktok',
            'version_code': '320906',
            'device_platform': 'android',
            'os': 'android',
            'os_version': '9',
            'openudid': device['payload']['openudid'],
            'timezone_name': device['payload']['timezone_name'],
            'timezone_offset': device['payload']['timezone_offset'],
            'cdid': device['payload']['cdid'],
        }
        url_encoded_str = urllib.parse.urlencode(params)
        url = f"https://api.tiktok.com/user/check_email/?{url_encoded_str}"

        payload = hashed_id(email)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'com.zhiliaoapp.musically',
        }

        logging.info(f"Sending request to URL: {url}")
        logging.info(f"Payload: {payload}")
        response = session.post(url, headers=headers, data=payload)

        # 打印原始响应内容和状态码
        logging.info(f"Response Code: {response.status_code}")
        logging.info(f"Response Text: {response.text}")

        # 检查响应状态码
        if response.status_code != 200:
            error_message = f"HTTP Error {response.status_code}: {response.text}"
            logging.error(error_message)
            return {"message": "error", "details": error_message}

        try:
            response_data = response.json()
        except ValueError as e:
            error_message = f"Error parsing JSON response: {str(e)}"
            logging.error(error_message)
            return {"message": "error", "details": error_message}

        # 检查返回数据的结构
        if 'status_code' in response_data:
            if response_data['status_code'] == 200:  # 假设200表示成功
                is_registered = response_data.get('is_registered', False)
                return {"message": "success", "is_registered": is_registered}
            else:
                error_message = f"API Error {response_data['status_code']}: {response_data.get('message')}"
                logging.error(error_message)
                return {"message": "error", "details": error_message}
        else:
            error_message = "Unexpected response structure."
            logging.error(error_message)
            return {"message": "error", "details": error_message}

    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")
        return {
            "message": f"error: {str(e)}"
        }

# Streamlit UI
st.title("TikTok 注册检查工具")
st.write("请输入每个手机号或邮箱，每行一个")

# 邮箱输入框
emails = st.text_area("邮箱地址 (每行一个)")

# 检查邮箱按钮
if st.button("检查邮箱"):
    session = requests.Session()
    email_results = []
    for email in emails.strip().split("\n"):
        email = email.strip()
        if not email:
            continue
        result = get_email_registration_status(email, session, device)
        
        if result["message"] == "success":
            if result["is_registered"]:
                email_results.append(f"邮箱 {email}, 注册: 是")
            else:
                email_results.append(f"邮箱 {email}, 注册: 否")
        else:
            email_results.append(f"邮箱 {email} 的错误: {result['details']}")

    # 显示邮箱结果
    st.write("### 邮箱检查结果:")
    for line in email_results:
        st.write(line)
