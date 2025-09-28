import streamlit as st

# --- HEADER WITH LOGO ---
st.image("AutoPilot HR logo.jpg", width=120)
st.markdown("<h1 style='display:inline; margin-left:10px;'>AutoPilot HR Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🔧 Admin Panel")
menu = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Attendance", "Leave Requests", "Add New Employee", "Promotions"]
)

# --- MAIN PAGE CONTENT ---
if menu == "Dashboard":
    st.subheader("📊 Admin Dashboard Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Employees", 120)
    with col2:
        st.metric("Pending Leave Requests", 5)
    with col3:
        st.metric("Attendance Today", "95%")

    st.markdown("### Quick Actions")
    st.button("➕ Add Employee")
    st.button("📌 Review Promotions")
    st.button("📄 Check Leave Requests")

elif menu == "Attendance":
    st.subheader("🕒 Attendance Records")
    st.write("Here you can track employee attendance.")
    # Example placeholder
    st.dataframe({
        "Employee": ["Ali", "Sara", "John"],
        "Date": ["2025-09-28", "2025-09-28", "2025-09-28"],
        "Status": ["Present", "Absent", "Present"]
    })

elif menu == "Leave Requests":
    st.subheader("📩 Leave Requests")
    st.write("Manage employee leave applications here.")
    st.dataframe({
        "Employee": ["Sara", "John"],
        "Leave Type": ["Sick", "Vacation"],
        "Dates": ["2025-10-01 to 2025-10-05", "2025-10-10 to 2025-10-15"],
        "Status": ["Pending", "Approved"]
    })

elif menu == "Add New Employee":
    st.subheader("👤 Add New Employee")
    name = st.text_input("Employee Name")
    dept = st.text_input("Department")
    role = st.text_input("Role")
    if st.button("Save"):
        st.success(f"New employee {name} added successfully!")

elif menu == "Promotions":
    st.subheader("🚀 Employee Promotions")
    st.write("Track and manage promotions.")
    st.dataframe({
        "Employee": ["Ali", "Sara"],
        "Current Role": ["Analyst", "HR Associate"],
        "Proposed Role": ["Senior Analyst", "HR Manager"],
        "Status": ["Pending", "Approved"]
    })

        
