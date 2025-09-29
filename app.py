import streamlit as st
from datetime import date

# ------------------------------
# Custom CSS (to look like Figma)
# ------------------------------
st.markdown("""
    <style>
    body {
        background-color: #f5f5f5;
        font-family: 'Arial', sans-serif;
    }
    .chat-box {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 15px;
        height: 300px;
        overflow-y: auto;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .user-msg {
        background-color: #007bff;
        color: white;
        padding: 8px 12px;
        border-radius: 12px;
        margin: 5px 0;
        text-align: right;
    }
    .bot-msg {
        background-color: #e9ecef;
        color: black;
        padding: 8px 12px;
        border-radius: 12px;
        margin: 5px 0;
        text-align: left;
    }
    .status-card {
        padding: 12px;
        border-radius: 10px;
        margin: 8px 0;
    }
    .accepted {background-color: #d4edda; color: #155724;}
    .declined {background-color: #f8d7da; color: #721c24;}
    .waitlist {background-color: #fff3cd; color: #856404;}
    </style>
""", unsafe_allow_html=True)


# ------------------------------
# Navigation State
# ------------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"


def go_to(page):
    st.session_state.page = page


# ------------------------------
# Login Page
# ------------------------------
if st.session_state.page == "login":
    st.title("🔑 Login to Autopilot HR")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        if email and password:
            go_to("onboarding")
        else:
            st.error("Please enter email and password")


# ------------------------------
# Onboarding
# ------------------------------
elif st.session_state.page == "onboarding":
    st.title("🤖 Welcome to Autopilot HR")

    company = st.selectbox("Select Company", ["Google", "Amazon", "Microsoft", "WP Bridge"])

    if st.button("Proceed Next"):
        go_to("fill_info")


# ------------------------------
# Fill Information
# ------------------------------
elif st.session_state.page == "fill_info":
    st.title("📋 Fill Information")

    full_name = st.text_input("Full Name")
    contact = st.text_input("Contact Number")
    email = st.text_input("Email")
    cnic = st.text_input("CNIC ID")
    dept = st.text_input("Department")
    resume = st.file_uploader("Upload Resume", type=["pdf", "docx"])

    if st.button("Proceed Next"):
        go_to("dashboard")


# ------------------------------
# Dashboard
# ------------------------------
elif st.session_state.page == "dashboard":
    st.title("📊 AI Dashboard")

    tabs = st.tabs(["💬 Chatbot", "📌 Request Form", "✅ Status"])

    # ---------------- Chatbot ----------------
    with tabs[0]:
        st.subheader("AI Chatbot")
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"sender": "bot", "text": "Hello 👋, how can I help you today?"}
            ]

        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-box">', unsafe_allow_html=True)
            for msg in st.session_state.messages:
                css_class = "user-msg" if msg["sender"] == "user" else "bot-msg"
                st.markdown(f'<div class="{css_class}">{msg["text"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        user_input = st.text_input("Type your message here...")
        if st.button("Send"):
            if user_input:
                st.session_state.messages.append({"sender": "user", "text": user_input})
                # Dummy bot reply (replace with AI API)
                st.session_state.messages.append({"sender": "bot", "text": "Got it 👍"})
                st.experimental_rerun()

    # ---------------- Request Form ----------------
    with tabs[1]:
        st.subheader("Leave Request Form")

        email = st.text_input("Email")
        leave_date = st.date_input("Leave Date", date.today())
        leave_type = st.selectbox("Leave Type", ["Sickness", "Casual", "Annual"])
        reason = st.text_area("Reason")

        if st.button("Submit Request"):
            st.success(f"Request submitted for {leave_date} ({leave_type}) ✅")

    # ---------------- Status ----------------
    with tabs[2]:
        st.subheader("Request Status")

        st.markdown('<div class="status-card waitlist">📅 22 September - Sick leave due to dengue → WAITLIST</div>', unsafe_allow_html=True)
        st.markdown('<div class="status-card declined">📅 18 April - Family marriage → DECLINED</div>', unsafe_allow_html=True)
        st.markdown('<div class="status-card accepted">📅 12 January - Illness → ACCEPTED</div>', unsafe_allow_html=True)
