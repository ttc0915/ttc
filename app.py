import streamlit as st
import requests
import time
import hashlib
import urllib

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
        "region": "SG",
        "app_language": "en",
        "locale": "en",
        "cdid": "841d4caf-1b90-450f-b717-b897ff555177",
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

# 获取域名信息的函数
def getdomain(email, session, device):
    try:
        params = {
            'iid': device['payload']['iid'],
            'device_id': device['payload']['device_id'],
            'aid': '567753',
            'app_name': 'tiktok_studio',
            'device_platform': 'android',
            'device_type': device['payload']['device_type'],
            'device_brand': device['payload']['device_brand'],
            'os': 'android',
            'app_language': 'en',
            'region': device['payload']['region'],
            'cdid': device['payload']['cdid'],
            '_rticket': str(int(time.time() * 1000)),
            'ts': str(int(time.time()))
        }
        url_encoded_str = urllib.parse.urlencode(params, doseq=True).replace('%2A', '*')
        url = f"https://api16-normal-useast5.tiktokv.us/passport/app/region/?{url_encoded_str}"

        payload = hashed_id(email)
        headers = {
            'Accept-Encoding': 'gzip',
            'Connection': 'Keep-Alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'passport-sdk-version': '6010090',
            'User-Agent': device['payload']['user-agent'],
            'x-vc-bdturing-sdk-version': '2.3.4.i18n',
        }

        response = session.post(url, headers=headers, data=payload)
        response_data = response.json()

        # 调试输出
        print(f"Debug - Response for {email}: {response_data}")

        if response.status_code == 200:
            return {
                "data": response_data.get('data', {}),
                "message": "success"
            }
        else:
            return {
                "message": f"error: status {response.status_code}, response {response_data}"
            }

    except Exception as e:
        return {
            "message": f"error: {str(e)}"
        }

# Streamlit UI
st.title("Phone Number Checker")
st.write("请输入每个手机号， 每行一个")

# 输入框
phones = st.text_area("Phone Numbers (one per line)")

# 按钮点击事件
if st.button("Start Check"):
    session = requests.Session()
    results = []
    for phone in phones.strip().split("\n"):
        phone = phone.strip()
        if not phone:
            continue
        result = getdomain(phone, session, device)
        time.sleep(0.5)  # 增加请求间隔
        
        if result["message"] == "success":
            country_code = result["data"].get('country_code', 'unknown')
            register_status = "True" if country_code != 'sg' else "False"
            results.append(f"Phone number {phone}, register: {register_status}")
        else:
            results.append(f"Error for {phone}: {result['message']}")

    # 显示结果
    st.write("### Results:")
    for line in results:
        st.write(line)
