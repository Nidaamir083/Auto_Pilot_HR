# assistant.py

import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(
    page_title="AutoPilot HR",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GOOGLE API KEY (replace with your own secure method) ---
Google_API_Key = "AIzaSyCmYETfsB7RKk9SqwNRFd7W0smr15LvJW8"

# --- STYLE ---
st.markdown("""
    <style>
    body {
        background: #f7f9fc; /* soft neutral background */
        color: #333333;
    }
    .main-header {
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(90deg, #004aad, #007bff);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    }
    .main-header img {
        height: 50px;
        margin-right: 15px;
        border-radius: 8px;
    }
    .main-header h1 {
        font-size: 1.8rem;
        margin: 0;
        font-weight: bold;
    }
    .figma-frame iframe {
        border-radius: 12px;
        box-shadow: 0px 4px 16px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER WITH LOGO ---
col1, col2 = st.columns([1, 5])

with col1:
    st.image("AutoPilot HR logo.jpg", width=80)

with col2:
    st.markdown(
        "<h1 style='margin-top:10px;'>AutoPilot HR Dashboard</h1>",
        unsafe_allow_html=True
    )


# --- SIDEBAR NAVIGATION ---
menu = st.sidebar.radio(
    "📌 Navigation",
    ["Dashboard", "Employees", "Attendance", "Leave", "Performance", "Figma Designs"]
)

# --- DUMMY DATA ---
employee_data = pd.DataFrame({
    "Employee ID": [101, 102, 103],
    "Name": ["Ali", "Babar", "Sara"],
    "Department": ["HR", "Finance", "IT"],
    "Status": ["Active", "On Leave", "Active"]
})

attendance_data = pd.DataFrame({
    "Employee ID": [101, 102, 103],
    "Name": ["Ali", "Babar", "Sara"],
    "Date": ["2025-09-28", "2025-09-28", "2025-09-28"],
    "Status": ["Present", "Absent", "Present"]
})

leave_data = pd.DataFrame({
    "Leave ID": [1, 2],
    "Employee": ["Ali", "Babar"],
    "Type": ["Annual", "Sick"],
    "Status": ["Approved", "Pending"]
})

# --- PAGES ---
if menu == "Dashboard":
    st.subheader("📊 Overview")
    st.metric("Total Employees", len(employee_data))
    st.metric("Employees Present Today", sum(attendance_data["Status"] == "Present"))
    st.metric("Pending Leave Requests", sum(leave_data["Status"] == "Pending"))

elif menu == "Employees":
    st.subheader("👩‍💼 Employee Management")
    st.dataframe(employee_data, use_container_width=True)
    with st.form("add_employee"):
        st.text_input("Name")
        st.text_input("Department")
        submitted = st.form_submit_button("➕ Add Employee")
        if submitted:
            st.success("✅ Employee added successfully!")

elif menu == "Attendance":
    st.subheader("🕒 Attendance Tracking")
    st.dataframe(attendance_data, use_container_width=True)
    with st.form("mark_attendance"):
        st.selectbox("Select Employee", employee_data["Name"])
        st.selectbox("Status", ["Present", "Absent", "Remote"])
        submitted = st.form_submit_button("Mark Attendance")
        if submitted:
            st.success("✅ Attendance marked!")

elif menu == "Leave":
    st.subheader("🌴 Leave Management")
    st.dataframe(leave_data, use_container_width=True)
    with st.form("apply_leave"):
        st.selectbox("Select Employee", employee_data["Name"])
        st.selectbox("Leave Type", ["Annual", "Sick", "Maternity", "Unpaid"])
        submitted = st.form_submit_button("Apply for Leave")
        if submitted:
            st.success("✅ Leave applied successfully!")



    
