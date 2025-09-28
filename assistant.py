import streamlit as st
import sqlite3
import google.generativeai as genai
from datetime import datetime, date
import pandas as pd

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Autopilot HR",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- STYLE (without theme selector) -----------------
st.markdown("""
    <style>
    .stApp {background-color: #f7f9fc;}
    .chat-container {max-width: 600px; margin: auto; padding-bottom: 100px;}
    .message {
        padding: 10px 15px; border-radius: 20px; margin: 10px;
        display: inline-block; max-width: 80%; word-wrap: break-word; font-size: 15px;
    }
    .user {
        background-color: #DCF8C6;
        margin-left: auto; display: block; text-align: right;
        color: black;
    }
    .bot {
        background-color: #ffffff;
        border: 1px solid #ddd;
        margin-right: auto; display: block; text-align: left;
        color: black;
    }
    .sticky-bar {
        position: fixed; bottom: 0; left: 0; right: 0;
        background: white; padding: 10px;
        border-top: 1px solid #ddd;
        display: flex; gap: 10px; z-index: 1000; align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- TITLE -----------------
st.markdown("<h1 style='text-align: center; color:#004aad;'>Autopilot HR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px; color:gray;'>Manage employees, leaves, attendance, promotions & reports</p>", unsafe_allow_html=True)

# ----------------- GEMINI SETUP -----------------
genai.configure(api_key=st.secrets["Google_API_Key"])
model = genai.GenerativeModel("gemini-2.0-flash")

# ----------------- DATABASE -----------------
DB = "employees.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
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
        emp_id INTEGER,
        start_date TEXT,
        end_date TEXT,
        reason TEXT,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY(emp_id) REFERENCES employees(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER,
        date TEXT,
        check_in TEXT,
        check_out TEXT,
        FOREIGN KEY(emp_id) REFERENCES employees(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS promotions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER,
        promotion_date TEXT,
        old_position TEXT,
        new_position TEXT,
        old_salary REAL,
        new_salary REAL,
        FOREIGN KEY(emp_id) REFERENCES employees(id)
    )""")
    conn.commit()
    conn.close()

# ----------------- INIT -----------------
init_db()

# ----------------- SIDEBAR (ADMIN PANEL with LOGO) -----------------
with st.sidebar:
    st.image("AutoPilot HR logo.jpg", width=150)
    st.title("📊 Admin Panel")

    # Employee form
    st.subheader("➕ Add New Employee")
    with st.form("emp_form"):
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        dept = st.text_input("Department")
        pos = st.text_input("Position")
        doh = st.date_input("Date of Hire")
        salary = st.number_input("Salary", min_value=0.0, step=1000.0)
        addr = st.text_area("Address")
        submit = st.form_submit_button("Save Employee")
        if submit:
            try:
                add_employee((fname,lname,email,phone,dept,pos,str(doh),salary,addr))
                st.success("✅ Employee Added!")
            except Exception as e:
                st.error(f"⚠️ Error: {e}")

    # Leave form
    st.subheader("📅 Apply for Leave")
    with st.form("leave_form"):
        employees = get_employees()
        emp_map = {f"{e[1]} {e[2]}": e[0] for e in employees}
        emp_name = st.selectbox("Select Employee", list(emp_map.keys()) if emp_map else ["No employees"])
        start = st.date_input("Start Date")
        end = st.date_input("End Date")
        reason = st.text_area("Reason")
        leave_submit = st.form_submit_button("Apply Leave")
        if leave_submit and employees:
            apply_leave(emp_map[emp_name], str(start), str(end), reason)
            st.success("✅ Leave Applied!")

    # Attendance
    st.subheader("🕒 Attendance")
    with st.form("attendance_form"):
        employees = get_employees()
        emp_map = {f"{e[1]} {e[2]}": e[0] for e in employees}
        emp_name = st.selectbox("Select Employee", list(emp_map.keys()) if emp_map else ["No employees"], key="att_emp")
        action = st.radio("Action", ["Check-in","Check-out"])
        att_submit = st.form_submit_button("Mark Attendance")
        if att_submit and employees:
            if action=="Check-in":
                mark_check_in(emp_map[emp_name])
                st.success("✅ Check-in marked!")
            else:
                mark_check_out(emp_map[emp_name])
                st.success("✅ Check-out marked!")

    # Promotion
    st.subheader("⬆️ Promotion")
    with st.form("promotion_form"):
        employees = get_employees()
        emp_map = {f"{e[1]} {e[2]}": e[0] for e in employees}
        emp_name = st.selectbox("Select Employee", list(emp_map.keys()) if emp_map else ["No employees"], key="prom_emp")
        new_pos = st.text_input("New Position")
        new_sal = st.number_input("New Salary", min_value=0.0, step=1000.0)
        prom_submit = st.form_submit_button("Promote Employee")
        if prom_submit and employees:
            add_promotion(emp_map[emp_name], new_pos, new_sal)
            st.success("✅ Promotion Added!")

