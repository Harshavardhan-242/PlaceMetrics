import streamlit as st

st.set_page_config(
    page_title="Placement Eligibility Checker",
    layout="centered"
)

# -------------------------------------------------
# DATA
# -------------------------------------------------
company_rules = {
    "TCS": {
        "cgpa": 6.0,
        "backlogs": 1,
        "logo": "TCS.jpg",
        "skills": ["Aptitude", "Basic DSA", "Communication"]
    },
    "Infosys": {
        "cgpa": 6.5,
        "backlogs": 0,
        "logo": "Infosys.png",
        "skills": ["Python", "DBMS", "Problem Solving"]
    },
    "Wipro": {
        "cgpa": 6.0,
        "backlogs": 2,
        "logo": "Wipro.png",
        "skills": ["Java", "OOPs", "SQL"]
    },
    "Google": {
        "cgpa": 8.0,
        "backlogs": 0,
        "logo": "Google.png",
        "skills": ["DSA", "System Design", "Competitive Programming"]
    }
}

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "evaluated" not in st.session_state:
    st.session_state.evaluated = False
if "eligible" not in st.session_state:
    st.session_state.eligible = None

# -------------------------------------------------
# HEADER (KEPT, COMPACT)
# -------------------------------------------------
st.markdown("## 🎓 Placement Eligibility Checker")
st.caption("Check eligibility, identify gaps, and plan your next steps")

st.divider()

# -------------------------------------------------
# INPUT FORM (VISIBLE LOGIC)
# -------------------------------------------------
show_full_form = (
    not st.session_state.evaluated
    or st.session_state.eligible is True
)

if show_full_form:
    st.subheader("Your Details")

    name = st.text_input(
        "Your Name",
        value=st.session_state.get("name", "")
    )
    cgpa = st.number_input(
        "Current CGPA",
        0.0, 10.0,
        step=0.1,
        value=st.session_state.get("cgpa", 0.0)
    )
    backlogs = st.number_input(
        "Active Backlogs",
        0, 10,
        value=st.session_state.get("backlogs", 0)
    )
    company = st.selectbox(
        "Company",
        company_rules.keys(),
        index=list(company_rules.keys()).index(
            st.session_state.get("company", "TCS")
        )
    )

    st.image(company_rules[company]["logo"], width=120)

    if st.button("Check Eligibility"):
        st.session_state.name = name
        st.session_state.cgpa = cgpa
        st.session_state.backlogs = backlogs
        st.session_state.company = company

        rule = company_rules[company]
        st.session_state.eligible = (
            cgpa >= rule["cgpa"]
            and backlogs <= rule["backlogs"]
        )

        st.session_state.evaluated = True
        st.rerun()

# -------------------------------------------------
# COLLAPSED FORM (ONLY WHEN NOT ELIGIBLE)
# -------------------------------------------------
if st.session_state.evaluated and not st.session_state.eligible:
    with st.expander("Edit Details", expanded=False):
        name = st.text_input("Your Name", st.session_state.name)
        cgpa = st.number_input("Current CGPA", 0.0, 10.0, step=0.1, value=st.session_state.cgpa)
        backlogs = st.number_input("Active Backlogs", 0, 10, value=st.session_state.backlogs)
        company = st.selectbox(
            "Company",
            company_rules.keys(),
            index=list(company_rules.keys()).index(st.session_state.company)
        )

        st.image(company_rules[company]["logo"], width=120)

        if st.button("Re-evaluate"):
            st.session_state.name = name
            st.session_state.cgpa = cgpa
            st.session_state.backlogs = backlogs
            st.session_state.company = company
            st.session_state.evaluated = False
            st.rerun()

# -------------------------------------------------
# RESULT SECTION
# -------------------------------------------------
if st.session_state.evaluated:
    st.divider()

    rule = company_rules[st.session_state.company]

    if st.session_state.eligible:
        st.success(f"✔ You are eligible for {st.session_state.company}")

        st.info(
            "You meet the eligibility criteria. "
            "Continue strengthening your skills and preparing for interviews."
        )

    else:
        st.warning(f"⚠ You are not eligible for {st.session_state.company}")

        st.subheader("Why this didn’t work")

        if st.session_state.cgpa < rule["cgpa"]:
            st.write(f"• Minimum CGPA required: **{rule['cgpa']}**")
        if st.session_state.backlogs > rule["backlogs"]:
            st.write(f"• Maximum allowed backlogs: **{rule['backlogs']}**")

        st.subheader("Skills to Focus On")
        for skill in rule["skills"]:
            st.write(f"✓ {skill}")

        st.subheader("Alternative Best-Fit Companies")

        alternatives = [
            comp for comp, r in company_rules.items()
            if st.session_state.cgpa >= r["cgpa"]
            and st.session_state.backlogs <= r["backlogs"]
        ]

        if alternatives:
            for comp in alternatives:
                st.write(f"→ {comp}")
        else:
            st.info(
                "No matching companies right now. "
                "Improving CGPA and clearing backlogs will open more opportunities."
            )
