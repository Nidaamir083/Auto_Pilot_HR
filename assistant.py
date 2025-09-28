import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(
    page_title="AutoPilot HR",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE ---
st.markdown("""
    <style>
    body {
        background: #f7f9fc;
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
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown(
    """
    <div class="main-header">
        <img src="AutoPilot HR logo.jpg" alt="AutoPilot HR Logo">
        <h1>AutoPilot HR Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- SIDEBAR NAVIGATION ---
menu = st.sidebar.radio(
    "📌 Admin Navigation",
    ["Dashboard", "Employees", "Attendance", "Leave", "Performance", "Promotion", "Employee Records"]
)

# --- DUMMY DATA ---
employee_data = pd.DataFrame({
    "Employee ID": [101, 102, 103],
    "Name": ["Ali", "Babar", "Sara"],
    "Department": ["HR", "Finance", "IT"],
    "Status": ["Active", "On Leave", "Active"],
    "Position": ["HR Officer", "Finance Analyst", "IT Engineer"]
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

# --- MAIN CONTENT ---
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

elif menu == "Performance":
    st.subheader("📈 Performance Management")
    st.write("⚡ Coming soon: KPI tracking, appraisals, and more!")

elif menu == "Promotion":
    st.subheader("🚀 Employee Promotion")
    with st.form("promote_employee"):
        selected_emp = st.selectbox("Select Employee", employee_data["Name"])
        new_position = st.text_input("Enter New Position")
        submitted = st.form_submit_button("Promote")
        if submitted:
            st.success(f"🎉 {selected_emp} has been promoted to {new_position}!")

elif menu == "Employee Records":
    st.subheader("👥 Employee Records")
    
    # Dummy placeholder for database fetch
    def get_employees():
        return [
            (101, "Ali", "Khan", "ali@example.com", "03001234567", "HR", "Active", "2023-01-15", "80,000 PKR"),
            (102, "Babar", "Ahmed", "babar@example.com", "03007654321", "Finance", "On Leave", "2022-05-10", "95,000 PKR"),
            (103, "Sara", "Iqbal", "sara@example.com", "03001112222", "IT", "Active", "2021-09-20", "100,000 PKR"),
        ]
    
    rows = get_employees()
    if rows:
        for r in rows:
            st.markdown(f"### {r[1]} {r[2]}  ({r[5]} - {r[6]})")
            st.write(f"📧 {r[3]} | 📱 {r[4]} | Hired: {r[7]} | 💰 {r[8]} | Status: {r[6]}")
            st.divider()
    else:
        st.info("No employees yet.")
