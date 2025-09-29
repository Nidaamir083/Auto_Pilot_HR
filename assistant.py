# assistant.py (corrected)
import os
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

# ----------------- SIMPLE STYLES -----------------
st.markdown("""
    <style>
      .stApp { background-color: #f7f9fc; }
      .chat-container { max-width: 600px; margin: auto; padding-bottom: 100px; }
      .message { padding: 10px 15px; border-radius: 20px; margin: 10px; display:inline-block; max-width:80%; word-wrap:break-word; font-size:15px; }
      .user { background-color: #DCF8C6; margin-left:auto; display:block; text-align:right; color:black; }
      .bot { background-color:#ffffff; border:1px solid #ddd; margin-right:auto; display:block; text-align:left; color:black; }
      .sticky-bar { position:fixed; bottom:0; left:0; right:0; background:white; padding:10px; border-top:1px solid #ddd; display:flex; gap:10px; z-index:1000; align-items:center; }
      /* sidebar clean background */
      section[data-testid="stSidebar"] { background-color: white; }
    </style>
""", unsafe_allow_html=True)

# ----------------- HEADER -----------------
st.markdown("<h1 style='text-align:center; color:#004aad;'>Autopilot HR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Manage employees, leaves, attendance, promotions & reports</p>", unsafe_allow_html=True)

# ----------------- GEMINI SETUP (safe) -----------------
# Try several possible secret names (so missing/wrong name won't crash app)
api_key = (
    st.secrets.get("Google_API_Key") 
    or st.secrets.get("Google_API_Key")
    or st.secrets.get("Google_API_KEY")
    or st.secrets.get("google_api_key")
)

model = None
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
    except Exception as e:
        st.warning("Warning: Could not configure Gemini model (QnA will be disabled). Check Google API key in secrets.")
        model = None
else:
    st.info("Info: No Google API key found in st.secrets — Gemini QnA is disabled. Add 'GOOGLE_API_KEY' to secrets if you want QnA.")

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

# ----------------- DB FUNCTIONS -----------------
def add_employee(data):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""INSERT INTO employees
        (first_name,last_name,email,phone,department,position,date_of_hire,salary,address)
        VALUES (?,?,?,?,?,?,?,?,?)""", data)
    conn.commit()
    conn.close()

def get_employees():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM employees")
    rows = c.fetchall()
    conn.close()
    return rows

def apply_leave(emp_id, start, end, reason):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO leaves (emp_id,start_date,end_date,reason) VALUES (?,?,?,?)",
              (emp_id,start,end,reason))
    conn.commit()
    conn.close()

def get_leaves():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""SELECT leaves.id, employees.first_name||' '||employees.last_name, 
                        leaves.start_date, leaves.end_date, leaves.reason, leaves.status, leaves.emp_id
                 FROM leaves JOIN employees ON leaves.emp_id = employees.id""")
    rows = c.fetchall()
    conn.close()
    return rows

def get_leaves_by_employee(emp_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT start_date,end_date,reason,status FROM leaves WHERE emp_id=?", (emp_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def update_leave_status(leave_id, status):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE leaves SET status=? WHERE id=?", (status,leave_id))
    conn.commit()
    conn.close()

def mark_check_in(emp_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    today = str(date.today())
    now = datetime.now().strftime("%H:%M:%S")
    c.execute("INSERT INTO attendance (emp_id,date,check_in) VALUES (?,?,?)", (emp_id,today,now))
    conn.commit()
    conn.close()

def mark_check_out(emp_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    today = str(date.today())
    now = datetime.now().strftime("%H:%M:%S")
    c.execute("UPDATE attendance SET check_out=? WHERE emp_id=? AND date=? AND check_out IS NULL", (now,emp_id,today))
    conn.commit()
    conn.close()

def get_attendance_by_employee(emp_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT date,check_in,check_out FROM attendance WHERE emp_id=?", (emp_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def add_promotion(emp_id, new_pos, new_sal):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    today = str(date.today())
    c.execute("SELECT position,salary FROM employees WHERE id=?", (emp_id,))
    res = c.fetchone()
    if res is None:
        conn.close()
        raise ValueError("Employee not found when adding promotion.")
    old_pos, old_sal = res
    c.execute("UPDATE employees SET position=?, salary=? WHERE id=?", (new_pos,new_sal,emp_id))
    c.execute("""INSERT INTO promotions (emp_id,promotion_date,old_position,new_position,old_salary,new_salary)
                 VALUES (?,?,?,?,?,?)""", (emp_id,today,old_pos,new_pos,old_sal,new_sal))
    conn.commit()
    conn.close()

def get_promotions(emp_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT promotion_date,old_position,new_position,old_salary,new_salary FROM promotions WHERE emp_id=?", (emp_id,))
    rows = c.fetchall()
    conn.close()
    return rows

# ----------------- INIT DB -----------------
init_db()

# ----------------- SIDEBAR (ADMIN PANEL with LOGO) -----------------
with st.sidebar:
    # try a few common logo paths
    logo_candidates = [
        "assets/AutoPilot HR logo.jpg",
        "assets/logo.jpg",
        "AutoPilot HR logo.jpg",
        "logo.jpg",
        "assets/logo.png",
        "logo.png"
    ]
    logo_path = None
    for p in logo_candidates:
        if os.path.exists(p):
            logo_path = p
            break

    if logo_path:
        st.image(logo_path, width=150)
    else:
        st.markdown("**AutoPilot HR**")
        st.caption("Place your logo at `assets/AutoPilot HR logo.jpg` or `logo.png` in the app repo.")

    st.markdown("---")
    st.title("📊 Admin Panel")

    ## Add Employee
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
                st.error(f"⚠️ Error adding employee: {e}")

    ## Apply for Leave (Admin can add on behalf)
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
            try:
                apply_leave(emp_map[emp_name], str(start), str(end), reason)
                st.success("✅ Leave Applied!")
            except Exception as e:
                st.error(f"⚠️ Error applying leave: {e}")

    ## Attendance
    st.subheader("🕒 Attendance")
    with st.form("attendance_form"):
        employees = get_employees()
        emp_map = {f"{e[1]} {e[2]}": e[0] for e in employees}
        emp_name = st.selectbox("Select Employee", list(emp_map.keys()) if emp_map else ["No employees"], key="att_emp")
        action = st.radio("Action", ["Check-in","Check-out"])
        att_submit = st.form_submit_button("Mark Attendance")
        if att_submit and employees:
            try:
                if action == "Check-in":
                    mark_check_in(emp_map[emp_name])
                    st.success("✅ Check-in marked!")
                else:
                    mark_check_out(emp_map[emp_name])
                    st.success("✅ Check-out marked!")
            except Exception as e:
                st.error(f"⚠️ Attendance error: {e}")

    ## Promotion
    st.subheader("⬆️ Promotion")
    with st.form("promotion_form"):
        employees = get_employees()
        emp_map = {f"{e[1]} {e[2]}": e[0] for e in employees}
        emp_name = st.selectbox("Select Employee", list(emp_map.keys()) if emp_map else ["No employees"], key="prom_emp")
        new_pos = st.text_input("New Position")
        new_sal = st.number_input("New Salary", min_value=0.0, step=1000.0)
        prom_submit = st.form_submit_button("Promote Employee")
        if prom_submit and employees:
            try:
                add_promotion(emp_map[emp_name], new_pos, new_sal)
                st.success("✅ Promotion Added!")
            except Exception as e:
                st.error(f"⚠️ Promotion error: {e}")


# ----------------- SIDEBAR: QnA ASSISTANT -----------------
st.sidebar.subheader(" QnA Assistant:")

user_question = st.sidebar.text_area("Ask about HR data...")

if st.sidebar.button("Get Answer"):
    try:
        # fetch data from DB
        employees = get_employees()
        leaves = get_leaves()

        conn = sqlite3.connect(DB)
        attendance = pd.read_sql("SELECT * FROM attendance", conn).to_dict(orient="records")
        promotions = pd.read_sql("SELECT * FROM promotions", conn).to_dict(orient="records")
        conn.close()

        context = f"""
        Employees: {employees}
        Leaves: {leaves}
        Attendance: {attendance}
        Promotions: {promotions}

        Question: {user_question}
        """

        response = model.generate_content(context)
        st.sidebar.markdown("**Answer:**")
        st.sidebar.write(response.text)

    except Exception as e:
        st.sidebar.error(f"⚠️ Error: {e}")


# ----------------- MAIN PAGE -----------------
st.subheader("👥 Employee Records")
rows = get_employees()
if rows:
    for r in rows:
        st.markdown(f"### {r[1]} {r[2]}  ({r[5]} - {r[6]})")
        st.write(f"📧 {r[3]} | 📱 {r[4]} | Hired: {r[7]} | 💰 {r[8]}")
        leaves = get_leaves_by_employee(r[0])
        if leaves:
            st.write("**Leave History:**")
            for l in leaves:
                st.write(f"📅 {l[0]} → {l[1]} | {l[2]} | Status: {l[3]}")
        att = get_attendance_by_employee(r[0])
        if att:
            st.write("**Attendance History:**")
            for a in att[-5:]:
                st.write(f"📅 {a[0]} | In: {a[1]} | Out: {a[2]}")
        prom = get_promotions(r[0])
        if prom:
            st.write("**Promotion History:**")
            for p in prom:
                st.write(f"📅 {p[0]} | {p[1]} → {p[2]} | 💰 {p[3]} → {p[4]}")
        st.divider()
else:
    st.info("No employees yet. Add from sidebar.")

# ----------------- PENDING LEAVES (approve/reject) -----------------
st.subheader("📌 Pending Leave Requests")
leaves = [l for l in get_leaves() if l[5] == "Pending"]
if leaves:
    for l in leaves:
        col1, col2, col3 = st.columns([3,2,2])
        with col1:
            st.write(f"**{l[1]}** ({l[2]} → {l[3]}) \nReason: {l[4]} \nStatus: {l[5]}")
        with col2:
            if st.button("Approve", key=f"approve_{l[0]}"):
                update_leave_status(l[0], "Approved")
                st.experimental_rerun()
        with col3:
            if st.button("Reject", key=f"reject_{l[0]}"):
                update_leave_status(l[0], "Rejected")
                st.experimental_rerun()
else:
    st.info("No pending leave requests.")

# ----------------- REPORT MANAGER (simple) -----------------
st.subheader("📑 Report Manager")
report_type = st.selectbox("Choose Report", ["Employees","Leaves","Attendance","Promotions"])
uploaded_file = st.file_uploader(f"Upload {report_type} CSV/Excel", type=["csv","xlsx"], key=f"{report_type}_upload")
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        conn = sqlite3.connect(DB)
        df.to_sql(report_type.lower(), conn, if_exists="append", index=False)
        conn.close()
        st.success(f"✅ {report_type} file imported successfully!")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# ----------------- CHAT / QnA -----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "bot"
    st.markdown(f"<div class='message {role}'>{msg['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

def send_message():
    user_msg = st.session_state.chat_input.strip()
    if user_msg == "":
        return
    st.session_state.messages.append({"role": "user", "content": user_msg})
    try:
        # prepare context
        employees = get_employees()
        leaves = get_leaves()
        context = f"Employees: {employees}\nLeaves: {leaves}\n\nUser query: {user_msg}"
        if model:
            response = model.generate_content(context)
            reply = getattr(response, "text", str(response))
        else:
            reply = "QnA model not configured. Add GOOGLE_API_KEY in secrets to enable."
    except Exception as e:
        reply = f"⚠️ Error: {e}"
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.chat_input = ""

st.markdown('<div class="sticky-bar">', unsafe_allow_html=True)
col1, col2 = st.columns([10, 1])
with col1:
    st.text_input("Type a message...", key="chat_input", label_visibility="collapsed", on_change=send_message)
with col2:
    if st.button("➤"):
        send_message()
st.markdown('</div>', unsafe_allow_html=True)
