import streamlit as st

# ----------------- AUTOPILOT HR THEME -----------------
st.markdown("""
    <style>
    /* Full-screen softer gradient */
    .stApp {
        background: linear-gradient(135deg, #4A90E2, #50E3C2);
        color: #fdfdfd;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #ffffff;
        color: #003366;
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #4A90E2, #50E3C2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-size: 15px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #50E3C2, #4A90E2);
        transform: scale(1.03);
    }

    /* Titles */
    h1, h2, h3 {
        color: #ffffff !important;
    }
    p, label, .stMarkdown {
        color: #f8faff !important;
    }

    /* Input Fields */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #333333;
        border-radius: 6px;
        border: 1px solid #d0d7de;
    }
    </style>
""", unsafe_allow_html=True)


# ----------------- SIDEBAR -----------------
try:
    st.sidebar.image("logo.png", use_container_width=True)
except Exception:
    st.sidebar.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/512px-React-icon.svg.png",
        use_container_width=True
    )

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", [
    "Dashboard", "Employees", "Leave", "Attendance",
    "Promotions", "Reports", "Prototype", "Settings"
])


# ----------------- MAIN TITLE -----------------
st.markdown("<h1 style='text-align: center;'>Autopilot HR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Manage employees, leaves, attendance, promotions & reports</p>", unsafe_allow_html=True)


# ----------------- PAGES -----------------
if menu == "Dashboard":
    st.subheader("📊 Overview")
    st.write("Welcome to the AutoPilot HR Dashboard.")

elif menu == "Employees":
    st.subheader("👥 Employee Management")
    with st.form("add_employee"):
        name = st.text_input("Employee Name")
        role = st.text_input("Role")
        dept = st.text_input("Department")
        submitted = st.form_submit_button("➕ Add Employee")
        if submitted:
            st.success(f"Employee {name} added successfully!")

elif menu == "Leave":
    st.subheader("🗓️ Leave Management")
    with st.form("leave_request"):
        emp = st.text_input("Employee Name")
        days = st.number_input("Days Requested", 1, 30)
        reason = st.text_area("Reason")
        leave_sub = st.form_submit_button("Submit Leave Request")
        if leave_sub:
            st.info(f"Leave request from {emp} submitted for {days} days.")

elif menu == "Attendance":
    st.subheader("📅 Attendance")
    emp = st.text_input("Employee Name for Attendance")
    mark = st.button("✅ Mark Present")
    if mark:
        st.success(f"Attendance marked for {emp}")

elif menu == "Promotions":
    st.subheader("📈 Promotions")
    emp = st.text_input("Employee Name for Promotion")
    new_role = st.text_input("New Role")
    promote = st.button("Promote Employee")
    if promote:
        st.success(f"{emp} has been promoted to {new_role}")

elif menu == "Reports":
    st.subheader("📑 Reports")
    st.write("Generate HR reports here.")

elif menu == "Prototype":
    st.subheader("🎨 Figma Prototype")
    figma_embed = """
    <div class="figma-container" style="margin-top: 20px;">
      <iframe
        src="https://www.figma.com/embed?embed_host=share&url=https://www.figma.com/proto/QRbk8IThJie8AkWB9SaQF6/Untitled?page-id=0%3A1&node-id=3-591&p=f&viewport=181%2C-260%2C0.61&scaling=scale-down&content-scaling=fixed&starting-point-node-id=15%3A190"
        width="100%"
        height="600"
        style="border: none; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.15);"
        allowfullscreen>
      </iframe>
    </div>
    """
    st.markdown(figma_embed, unsafe_allow_html=True)

elif menu == "Settings":
    st.subheader("⚙️ Settings")
    st.write("App configuration options.")



    
    
  







