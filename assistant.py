# assistant.py
import os
import streamlit as st
import google.generativeai as genai
import pandas as pd

# ===============================
# CONFIGURE GOOGLE GEMINI API
# ===============================
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"  # 🔑 Replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini Model
model = genai.GenerativeModel("gemini-1.5-pro")

# ===============================
# CUSTOM PAGE CONFIG
# ===============================
st.set_page_config(page_title="AutoPilot HR Assistant", layout="wide")

# Apply fullscreen gradient background
page_bg = """
<style>
.stApp {
    background: linear-gradient(135deg, #0047AB, #1E90FF);
    color: white !important;
}
.sidebar .sidebar-content {
    background: rgba(0,0,0,0.4);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ===============================
# SIDEBAR NAVIGATION
# ===============================
st.sidebar.image("logo.png", use_column_width=True)  # place your logo file in the same dir
st.sidebar.title("AutoPilot HR")
menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "👥 Employees", "📅 Attendance", "📝 Leave", "💰 Payroll",
     "🎯 Performance", "🧑‍💼 Recruitment", "🤖 HR Assistant"]
)

# ===============================
# DUMMY HR DATA
# ===============================
employees = pd.DataFrame({
    "Employee ID": [101, 102, 103],
    "Name": ["Alice Johnson", "Bob Smith", "Charlie Brown"],
    "Department": ["HR", "Engineering", "Finance"],
    "Status": ["Active", "Active", "On Leave"]
})

attendance = pd.DataFrame({
    "Employee ID": [101, 102, 103],
    "Date": ["2025-09-25", "2025-09-25", "2025-09-25"],
    "Status": ["Present", "Present", "Absent"]
})

leave = pd.DataFrame({
    "Leave ID": [1, 2],
    "Employee": ["Charlie Brown", "Alice Johnson"],
    "Type": ["Medical", "Annual"],
    "Status": ["Approved", "Pending"]
})

payroll = pd.DataFrame({
    "Employee ID": [101, 102, 103],
    "Name": ["Alice Johnson", "Bob Smith", "Charlie Brown"],
    "Salary": [5000, 7000, 6000],
    "Status": ["Paid", "Pending", "Paid"]
})

performance = pd.DataFrame({
    "Employee ID": [101, 102, 103],
    "Name": ["Alice Johnson", "Bob Smith", "Charlie Brown"],
    "Rating": ["Excellent", "Good", "Average"]
})

recruitment = pd.DataFrame({
    "Candidate": ["David Miller", "Emma Wilson"],
    "Position": ["Software Engineer", "HR Manager"],
    "Status": ["Interview Scheduled", "Under Review"]
})

# ===============================
# DASHBOARD
# ===============================
if menu == "🏠 Dashboard":
    st.title("📊 HR Dashboard - AutoPilot HR")
    st.metric("Total Employees", employees.shape[0])
    st.metric("On Leave Today", leave[leave["Status"] == "Approved"].shape[0])
    st.metric("Pending Payroll", payroll[payroll["Status"] == "Pending"].shape[0])

# ===============================
# EMPLOYEES
# ===============================
elif menu == "👥 Employees":
    st.title("👥 Employee Records")
    st.dataframe(employees, use_container_width=True)

# ===============================
# ATTENDANCE
# ===============================
elif menu == "📅 Attendance":
    st.title("📅 Attendance")
    st.dataframe(attendance, use_container_width=True)

# ===============================
# LEAVE
# ===============================
elif menu == "📝 Leave":
    st.title("📝 Leave Management")
    st.dataframe(leave, use_container_width=True)

# ===============================
# PAYROLL
# ===============================
elif menu == "💰 Payroll":
    st.title("💰 Payroll Status")
    st.dataframe(payroll, use_container_width=True)

# ===============================
# PERFORMANCE
# ===============================
elif menu == "🎯 Performance":
    st.title("🎯 Performance Reviews")
    st.dataframe(performance, use_container_width=True)

# ===============================
# RECRUITMENT
# ===============================
elif menu == "🧑‍💼 Recruitment":
    st.title("🧑‍💼 Recruitment")
    st.dataframe(recruitment, use_container_width=True)

# ===============================
# HR ASSISTANT (Gemini)
# ===============================
elif menu == "🤖 HR Assistant":
    st.title("🤖 AutoPilot HR - AI Assistant")
    st.write("Ask me anything about employees, leave, payroll, or HR policies.")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Chat UI
    user_input = st.text_input("You:", key="user_input")
    if user_input:
        with st.spinner("Thinking..."):
            chat = model.start_chat(history=st.session_state["chat_history"])
            response = chat.send_message(user_input)
            st.session_state["chat_history"].append({"role": "user", "parts": [user_input]})
            st.session_state["chat_history"].append({"role": "model", "parts": [response.text]})
            st.markdown(f"**Assistant:** {response.text}")

    # Display chat history
    if st.session_state["chat_history"]:
        st.write("### Conversation History")
        for msg in st.session_state["chat_history"]:
            role = "👤 You" if msg["role"] == "user" else "🤖 Assistant"
            st.markdown(f"**{role}:** {msg['parts'][0]}")


    
    
  







