import streamlit as st
import sqlite3
import google.generativeai as genai
from datetime import datetime, date
import pandas as pd

# ----------------- THEME -----------------
theme = st.sidebar.radio("Theme", ["Light", "Dark"])
if theme == "Light":
    bg_color, user_color, bot_color, bot_border = "#FFFFFF", "#DCF8C6", "#FFFFFF", "#DDD"
    title_color, subtitle_color, user_text_color, bot_text_color = "black", "gray", "black", "black"
else:
    bg_color, user_color, bot_color, bot_border = "#181818", "#2E7D32", "#2C2C2C", "#444"
    title_color, subtitle_color, user_text_color, bot_text_color = "white", "white", "white", "white"

st.markdown(f"""
    <style>
    .stApp {{background-color: {bg_color};}}
    .chat-container {{max-width: 600px; margin: auto; padding-bottom: 100px;}}
    .message {{
        padding: 10px 15px; border-radius: 20px; margin: 10px;
        display: inline-block; max-width: 80%; word-wrap: break-word; font-size: 15px;
    }}
    .user {{
        background-color: {user_color};
        margin-left: auto; display: block; text-align: right;
        color: {user_text_color};
    }}
    .bot {{
        background-color: {bot_color};
        border: 1px solid {bot_border};
        margin-right: auto; display: block; text-align: left;
        color: {bot_text_color};
    }}
    .sticky-bar {{
        position: fixed; bottom: 0; left: 0; right: 0;
        background: white; padding: 10px;
        border-top: 1px solid #ddd;
        display: flex; gap: 10px; z-index: 1000; align-items: center;
    }}
    </style>
""", unsafe_allow_html=True)

# ----------------- HEADER WITH LOGO -----------------
col1, col2 = st.columns([1,5])
with col1:
    st.image("AutoPilot HR logo.jpg", width=100)
with col2:
    st.markdown(f"<h1 style='color:{title_color}; margin-top:20px;'>Autopilot HR Dashboard</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size:18px; color:{subtitle_color};'>Manage employees, leaves, attendance, promotions & reports</p>", unsafe_allow_html=True)
st.markdown("---")

# ----------------- GEMINI SETUP -----------------
genai.configure(api_key=st.secrets["Google_PI_Key"])
model = genai.GenerativeModel("gemini-2.0-flash")

# ----------------- DATABASE INIT -----------------
DB = "employees.db"
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # (tables: employees, leaves, attendance, promotions)
    c.execute("""CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT, last_name TEXT,
        email TEXT UNIQUE, phone TEXT,
        department TEXT, position TEXT,
        date_of_hire TEXT, salary REAL,
        address TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS leaves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER, start_date TEXT, end_date TEXT, reason TEXT,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY(emp_id) REFERENCES employees(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER, date TEXT, check_in TEXT, check_out TEXT,
        FOREIGN KEY(emp_id) REFERENCES employees(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS promotions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER, promotion_date TEXT,
        old_position TEXT, new_position TEXT,
        old_salary REAL, new_salary REAL,
        FOREIGN KEY(emp_id) REFERENCES employees(id)
    )""")
    conn.commit()
    conn.close()
init_db()

# ----------------- FUNCTIONS (same as before) -----------------
# add_employee, get_employees, apply_leave, update_leave_status, etc.
# (keep your existing function implementations here, unchanged)

# ----------------- LAYOUT SPLIT -----------------
role = st.sidebar.radio("Login as:", ["Admin", "Employee"])

if role == "Admin":
    # --- ADMIN PANEL (SIDEBAR) ---
    st.sidebar.title("👨‍💼 Admin Panel")

    st.sidebar.subheader("Add New Employee")
    with st.sidebar.form("emp_form"):
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        dept = st.text_input("Department")
        pos = st.text_input("Position")
        doh = st.date_input("Date of Hire")
        salary = st.number_input("Salary", min_value=0.0, step=1000.0)
        addr = st.text_area("Address")
        if st.form_submit_button("Save Employee"):
            add_employee((fname,lname,email,phone,dept,pos,str(doh),salary,addr))
            st.sidebar.success("Employee Added!")

    # Leaves pending
    st.subheader("📩 Pending Leave Requests")
    # (reuse your existing pending leave approval block here)

    # Reports
    st.subheader("📊 Reports Manager")
    # (reuse your upload/download code here)

    # QnA assistant
    st.sidebar.subheader("🤖 HR QnA Assistant")
    question = st.sidebar.text_area("Ask...")
    if st.sidebar.button("Answer"):
        # (reuse your gemini QnA block here)

   elif menu == "Employee Records":
    # Admin can see all employee data
    st.subheader("👥 Employee Records")
    rows = get_employees()
    if rows:
        for r in rows:
            st.markdown(f"### {r[1]} {r[2]}  ({r[5]} - {r[6]})")
            st.write(f"📧 {r[3]} | 📱 {r[4]} | Hired: {r[7]} | 💰 {r[8]} | {r[6]}")
            st.divider()
    else:
        st.info("No employees yet.")

elif role == "Employee":
    # --- EMPLOYEE PANEL (MAIN PAGE) ---
    st.subheader("👤 Employee Dashboard")
    employees = get_employees()
    emp_map = {f"{e[1]} {e[2]}": e[0] for e in employees}
    emp_name = st.selectbox("Select Your Name", list(emp_map.keys()) if emp_map else ["No employees"])
    if emp_name != "No employees":
        emp_id = emp_map[emp_name]

        st.markdown(f"### Welcome, {emp_name}!")

        # Attendance
        st.write("🕒 Attendance")
        action = st.radio("Action", ["Check-in","Check-out"], horizontal=True)
        if st.button("Submit Attendance"):
            if action=="Check-in":
                mark_check_in(emp_id)
                st.success("Checked in!")
            else:
                mark_check_out(emp_id)
                st.success("Checked out!")

        # Leave Request
        st.write("📩 Request Leave")
        with st.form("leave_form_emp"):
            start = st.date_input("Start Date")
            end = st.date_input("End Date")
            reason = st.text_area("Reason")
            if st.form_submit_button("Submit Leave"):
                apply_leave(emp_id, str(start), str(end), reason)
                st.success("Leave request submitted!")

        # Promotions
        st.write("🚀 Promotion History")
        proms = get_promotions(emp_id)
        if proms:
            for p in proms:
                st.write(f"{p[0]} | {p[1]} → {p[2]} | {p[3]} → {p[4]}")
        else:
            st.info("No promotions yet.")

        # Attendance history
        st.write("📜 Your Attendance History")
        att = get_attendance_by_employee(emp_id)
        if att:
            st.dataframe(pd.DataFrame(att, columns=["Date","Check-in","Check-out"]))
        else:
            st.info("No attendance records.")

        # Leave history
        st.write("📜 Your Leave History")
        leaves = get_leaves_by_employee(emp_id)
        if leaves:
            st.dataframe(pd.DataFrame(leaves, columns=["Start","End","Reason","Status"]))
        else:
            st.info("No leave records.")

    


        
