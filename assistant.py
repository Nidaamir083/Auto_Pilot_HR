import streamlit as st

st.set_page_config(page_title="AutoPilot HR", layout="wide")

# --- HEADER ---
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:15px;padding:10px;
                background:linear-gradient(90deg,#004aad,#007bff);color:white;
                border-radius:10px;margin-bottom:20px;">
        <img src="AutoPilot HR logo.jpg" width="60">
        <h1 style="margin:0;">AutoPilot HR Dashboard</h1>
    </div>
    """, unsafe_allow_html=True
)

# --- SIDEBAR (ADMIN PANEL) ---
st.sidebar.title("👨‍💼 Admin Panel")

admin_menu = st.sidebar.radio(
    "Select Action",
    ["➕ Add Employee", "🌴 Manage Leaves", "🕒 Manage Attendance", "🚀 Promote Employee", "📊 Reports"]
)

# --- MAIN PAGE CONTENT ---
if admin_menu == "➕ Add Employee":
    st.subheader("Add New Employee")
    with st.form("add_employee"):
        col1, col2 = st.columns(2)
        with col1:
            fname = st.text_input("First Name")
            lname = st.text_input("Last Name")
            dept = st.text_input("Department")
        with col2:
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            position = st.text_input("Position")
        salary = st.number_input("Salary", min_value=0.0, step=1000.0)
        submit = st.form_submit_button("Save Employee")
        if submit:
            st.success(f"✅ Employee {fname} {lname} added successfully!")

elif admin_menu == "🌴 Manage Leaves":
    st.subheader("Pending Leave Requests")
    st.info("Here admin will see pending requests (approve/reject buttons).")

elif admin_menu == "🕒 Manage Attendance":
    st.subheader("Attendance Manager")
    st.info("Admin can mark/check attendance here.")

elif admin_menu == "🚀 Promote Employee":
    st.subheader("Promotion Manager")
    emp_name = st.selectbox("Select Employee", ["Ali", "Babar", "Sara"])
    new_pos = st.text_input("New Position")
    new_sal = st.number_input("New Salary", min_value=0.0, step=1000.0)
    if st.button("Promote"):
        st.success(f"🎉 {emp_name} promoted to {new_pos} with salary {new_sal}!")

elif admin_menu == "📊 Reports":
    st.subheader("Reports & Analytics")
    st.info("Download CSV/Excel or view summaries here.")

# --- MAIN PAGE (EMPLOYEE VIEW) ---
st.markdown("---")
st.subheader("👩‍💼 Employee Portal")
st.write("This area is for employees to see their own records (attendance, leaves, promotions, etc.).")





   
