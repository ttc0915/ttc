import streamlit as st
import requests
import time
import hashlib
import urllib

# Global device information
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
        "device_type": "SHARP_D9XLH",
        "device_brand": "sharp",
        "language": "en",
        "timezone_name": "Asia/Singapore",
        "timezone_offset": "28800",
        "cdid": "841d4caf-1b90-450f-b717-b897ff555177",
        "user-agent": "com.zhiliaoapp.musically/2023204020 (Linux; U; Android 8.0.0; en_SG; SHARP_D9XLH; Build/N2G48H;tt-ok/3.12.13.4-tiktok)"
    }
}

# Hash function to create a hashed ID
def hashed_id(value):
    type_value = "1" if "+" in value else "2" if "@" in value else "3"
    hashed_id = value + "aDy0TUhtql92P7hScCs97YWMT-jub2q9"
    hashed_value = hashlib.sha256(hashed_id.encode()).hexdigest()
    return f"hashed_id={hashed_value}&type={type_value}"

# Function to check registration and ban status
def get_account_status(email, session, device):
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
            'device_type': device['payload']['device_type'],
            'device_brand': device['payload']['device_brand'],
            'language': 'en',
            'timezone_name': device['payload']['timezone_name'],
            'timezone_offset': device['payload']['timezone_offset'],
            'cdid': device['payload']['cdid']
        }
        
        url = f"https://api16-normal-useast5.tiktokv.us/passport/app/region/?{urllib.parse.urlencode(params)}"
        payload = hashed_id(email)
        
        headers = {
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': device['payload']['user-agent']
        }
        
        response = session.post(url, headers=headers, data=payload)
        response_data = response.json()
        
        # Check response fields for registration and ban status
        is_registered = response_data.get('data', {}).get('country_code') != 'sg'
        is_banned = response_data.get('data', {}).get('is_banned', False)
        
        return {
            "register": is_registered,
            "ban": is_banned,
            "message": "success"
        }
    except Exception as e:
        return {
            "message": f"error: {str(e)}"
        }

# Streamlit UI configuration
st.set_page_config(page_title="Phone Number Checker", page_icon="📱")
st.markdown(
    """
    <style>
    body { background-color: #FFC0CB; color: #000000; }
    .stTextInput, .stTextArea { background-color: #FFB6C1; }
    .stButton { background-color: #FF69B4; color: white; }
    </style>
    """, unsafe_allow_html=True
)

st.title("Phone Number Checker")
st.write("Please enter each phone number, one per line (请输入每个手机号，每行一个)")

# Input field
phones = st.text_area("Phone Numbers (one per line)")

# Error log box
error_logs = st.empty()  # To display logs in real-time
error_log_messages = []  # Store error messages

# On button click, process phone numbers
if st.button("Start Check"):
    session = requests.Session()
    results = []
    
    for phone in phones.strip().split("\n"):
        phone = phone.strip()
        if not phone:
            continue
        
        result = get_account_status(phone, session, device)
        
        # Check for success or error in response
        if result["message"] == "success":
            register_status = "True" if result["register"] else "False"
            ban_status = "True" if result["ban"] else "False"
            results.append(f"Phone number {phone}, register: {register_status}, Ban: {ban_status}")
        else:
            # Capture and display errors
            error_log_messages.append(f"Error for {phone}: {result['message']}")
            error_logs.write("\n".join(error_log_messages))  # Real-time update
        
    # Display results
    st.write("### Results (结果):")
    for line in results:
        st.write(line)

    # "Hacker" effect after checking
    st.markdown(
        """
        <div style="font-family: monospace; color: #00FF00;">
            <h2>Hacker Effect (黑客特效)</h2>
            <p>Loading... (加载中...)</p>
        </div>
        """, unsafe_allow_html=True
    )
    st.balloons()
