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

# 获取域名信息的函数
def getdomain(email, session, device):
    try:
        params = {
            'iid': device['payload']['iid'],
            'device_id': device['payload']['device_id'],
            'ac': 'wifi',
            'channel': 'googleplay',
            'aid': '567753',
            'app_name': 'tiktok_studio',
            'version_code': '320906',
            'version_name': '32.9.6',
            'device_platform': 'android',
            'os': 'android',
            'ab_version': '32.9.6',
            'ssmix': 'a',
            'device_type': device['payload']['device_type'],
            'device_brand': device['payload']['device_brand'],
            'language': 'en',
            'os_api': '28',
            'os_version': '9',
            'openudid': device['payload']['openudid'],
            'manifest_version_code': '320906',
            'resolution': '540*960',
            'dpi': '240',
            'update_version_code': '320906',
            '_rticket': str(int(time.time())),
            'is_pad': '0',
            'current_region': device['payload']['carrier_region'],
            'app_type': 'normal',
            'sys_region': 'US',
            'mcc_mnc': '45201',
            'timezone_name': device['payload']['timezone_name'],
            'carrier_region_v2': '452',
            'residence': device['payload']['carrier_region'],
            'app_language': 'en',
            'carrier_region': device['payload']['carrier_region'],
            'ac2': 'wifi5g',
            'uoo': '0',
            'op_region': device['payload']['carrier_region'],
            'timezone_offset': device['payload']['timezone_offset'],
            'build_number': '32.9.6',
            'host_abi': 'arm64-v8a',
            'locale': 'en',
            'region': device['payload']['carrier_region'],
            'content_language': 'en',
            'ts': str(int(time.time())),
            'cdid': device['payload']['cdid']
        }
        url_encoded_str = urllib.parse.urlencode(params, doseq=True).replace('%2A', '*')
        url = f"https://api16-normal-useast5.tiktokv.us/passport/app/region/?{url_encoded_str}"

        payload = hashed_id(email)
        headers = {
            'Accept-Encoding': 'gzip',
            'Connection': 'Keep-Alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'passport-sdk-version': '6010090',
            'User-Agent': 'com.ss.android.tt.creator/320906 (Linux; U; Android 9; en_US; SM-G960N; Build/PQ3A.190605.07291528;tt-ok/3.12.13.4-tiktok)',
            'x-vc-bdturing-sdk-version': '2.3.4.i18n',
        }

        response = session.post(url, headers=headers, data=payload)
        return {
            "data": response.json()['data'],
            "message": "success"
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
        if not phone.strip():
            continue
        result = getdomain(phone.strip(), session, device)
        if result["message"] == "success" and result["data"].get('country_code') != 'sg':
            results.append(f"Phone number {phone.strip()}, register: True")
        elif result["message"] == "success":
            results.append(f"Phone number {phone.strip()}, register: False")
        else:
            results.append(f"Error for {phone.strip()}: {result['message']}")

    # 显示结果
    st.write("### Results:")
    for line in results:
        st.write(line)
