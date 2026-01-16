import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Placement Analytics Dashboard", layout="wide")

# ---------- STYLING ----------
st.markdown("""
<style>
.stButton>button {
    background-color: #BB86FC;
    color: black;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.image("placement1.jpg", use_container_width=True)
st.title("📊 Smart Placement Analytics Dashboard")

# ---------- SIDEBAR ----------
st.sidebar.title("🎓 Placement Portal")
st.sidebar.markdown("### Select Company")

company_rules = {
    "TCS": {"cgpa": 6.0, "backlogs": 1, "year": "Final Year"},
    "Infosys": {"cgpa": 6.5, "backlogs": 0, "year": "Final Year"},
    "Wipro": {"cgpa": 6.0, "backlogs": 2, "year": "Final Year"},
    "Google": {"cgpa": 8.0, "backlogs": 0, "year": "Final Year"}
}

company_logos = {
    "TCS": "TCS.jpg",
    "Infosys": "Infosys.png",
    "Wipro": "Wipro.png",
    "Google": "download.jpg"
}

company = st.sidebar.selectbox("Company", list(company_rules.keys()))
st.sidebar.image(company_logos[company], width=120)

st.sidebar.info("Check eligibility based on company rules")

# ---------- SESSION STATE ----------
if "students" not in st.session_state:
    st.session_state.students = []

# ---------- INPUT FORM ----------
st.subheader("➕ Add Student")
with st.form("eligibility_form"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Student Name")
        reg_no = st.text_input("Register Number")
        cgpa = st.number_input("CGPA", 0.0, 10.0, step=0.1)

    with col2:
        backlogs = st.number_input("Backlogs", 0, 10)
        year = st.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "Final Year"])

    submitted = st.form_submit_button("Check Eligibility")

# ---------- PROCESS ----------
if submitted:
    rule = company_rules[company]

    if cgpa >= rule["cgpa"] and backlogs <= rule["backlogs"] and year == rule["year"]:
        status = "Eligible"
        st.success(f"🎉 Eligible for {company}")
        st.image("pass.png", width=80)
    else:
        status = "Not Eligible"
        st.error(f"❌ Not Eligible for {company}")
        st.image("fail.png", width=80)

    st.session_state.students.append({
        "Name": name,
        "Register No": reg_no,
        "Company": company,
        "CGPA": cgpa,
        "Backlogs": backlogs,
        "Year": year,
        "Status": status
    })

# ---------- ANALYTICS ----------
if st.session_state.students:

    df = pd.DataFrame(st.session_state.students)

    st.subheader("📋 Student Data")
    st.dataframe(df)

    col1, col2 = st.columns(2)

    # -------- PIE CHART --------
    eligible = df[df["Status"] == "Eligible"].shape[0]
    not_eligible = df[df["Status"] == "Not Eligible"].shape[0]

    with col1:
        st.subheader("🥧 Eligibility Distribution")
        fig, ax = plt.subplots()
        ax.pie(
            [eligible, not_eligible],
            labels=["Eligible", "Not Eligible"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)

    # -------- BAR CHART --------
    with col2:
        st.subheader("🏢 Company-wise Eligible Students")
        company_counts = df[df["Status"] == "Eligible"]["Company"].value_counts()
        st.bar_chart(company_counts)

    # -------- CGPA HISTOGRAM --------
    st.subheader("📈 CGPA Distribution")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        fig2, ax2 = plt.subplots(figsize=(5, 3))   # smaller size
        ax2.hist(df["CGPA"], bins=8)
        ax2.set_xlabel("CGPA")
        ax2.set_ylabel("Students")
        st.pyplot(fig2)
