import streamlit as st
import requests
import json
import time

# 发送验证码到手机号
def send_verification_code(phone, device):
    try:
        # 假设此URL为发送验证码的API
        url = f"https://api.tiktok.com/send_code?phone={phone}"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": device["payload"]["user-agent"],
            # 其他必要的headers信息
        }
        response = requests.post(url, headers=headers)
        data = response.json()
        if data.get("status") == "success":
            return {"message": "验证码已发送"}
        else:
            return {"message": "发送验证码失败", "error": data.get("error")}
    except Exception as e:
        return {"message": f"error: {str(e)}"}

# 从接码API获取验证码
def get_verification_code(api_link):
    try:
        response = requests.get(api_link)
        data = response.json()
        if data.get("status") == "success":
            return data.get("sms_code")  # 假设返回数据包含'sms_code'字段
        else:
            return None
    except Exception as e:
        return None

# 验证验证码
def verify_code(phone, code):
    try:
        # 假设此URL为验证验证码的API
        url = f"https://api.tiktok.com/verify_code?phone={phone}&code={code}"
        response = requests.post(url)
        data = response.json()
        if data.get("status") == "success":
            return "账号未封禁"
        elif data.get("error") == "account_disabled":
            return "账号已被封禁"
        else:
            return "验证失败"
    except Exception as e:
        return f"验证时出错: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="手机号封禁检测", page_icon="📱")
st.title("手机号封禁检测")
st.write("请输入手机号和接码API链接")

# 输入框
phone_input = st.text_input("手机号")
api_link_input = st.text_input("接码API链接")

# 按钮点击事件
if st.button("检测封禁状态"):
    device = {
        "payload": {
            "user-agent": "Your-User-Agent-Here"  # 请替换为实际的User-Agent
            # 其他必要的设备信息
        }
    }

    # 1. 发送验证码
    send_result = send_verification_code(phone_input, device)
    st.write(send_result["message"])

    if send_result["message"] == "验证码已发送":
        # 2. 等待验证码发送
        st.write("等待验证码...")
        time.sleep(5)  # 暂停5秒，等待接码服务获取验证码

        # 3. 从接码API获取验证码
        code = get_verification_code(api_link_input)
        if code:
            st.write(f"获取到的验证码: {code}")

            # 4. 验证验证码
            verify_result = verify_code(phone_input, code)
            st.write(f"检测结果: {verify_result}")
        else:
            st.write("未获取到验证码，请重试")
    else:
        st.write("验证码发送失败，请检查手机号和设备信息")

