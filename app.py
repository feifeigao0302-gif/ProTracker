import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="ProTracker - IEP Management", layout="wide")

# 2. Professional Database Initialization
if 'db' not in st.session_state:
    st.session_state.db = {
        "Class A (DLI)": {
            "Student Alpha": {
                "Grade": "3rd", 
                "Goals": {
                    "Reading Comp": {"baseline": 30, "target": 80, "criteria": "4/5 trials", "method": "Wh- Questions"},
                }
            }
        }
    }

# 3. Sidebar Navigation & Auth
st.sidebar.title("🔐 Authorization")
password = st.sidebar.text_input("Teacher Password", type="password")
is_teacher = (password == "1234")

st.sidebar.divider()
st.sidebar.title("🚀 Navigation")
mode = st.sidebar.radio("Go to:", ["📝 Data Hunt", "👩‍🏫 Teacher Dashboard"])

# --- MODE 1: DATA HUNT ---
if mode == "📝 Data Hunt":
    st.title("🎯 ProTracker: Progress Monitoring")
    classes = list(st.session_state.db.keys())
    if not classes:
        st.info("No classes found. Access the Teacher Dashboard to add one.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            sel_class = st.selectbox("Step 1: Select Class", classes)
        with c2:
            students = list(st.session_state.db[sel_class].keys())
            sel_student = st.selectbox("Step 2: Select Student", students) if students else None
        
        if sel_student:
            st.divider()
            student_data = st.session_state.db[sel_class][sel_student]
            goal_names = list(student_data["Goals"].keys())
            if goal_names:
                sel_goal = st.selectbox("Step 3: Select IEP Goal", goal_names)
                details = student_data["Goals"][sel_goal]
                st.info(f"**Goal Specs:** Baseline: {details['baseline']}% | Target: {details['target']}% | Method: {details['method']}")
                
                with st.form("data_entry_form", clear_on_submit=True):
                    val = st.number_input("Current Performance (%)", 0, 100, 80)
                    note = st.text_input("Observation Notes")
                    if st.form_submit_button("Submit Record"):
                        st.success(f"Record saved for {sel_student}!")
            else:
                st.warning("No goals found for this student.")

# --- MODE 2: TEACHER DASHBOARD ---
elif mode == "👩‍🏫 Teacher Dashboard":
    if not is_teacher:
        st.warning("Admin Access Required. Please enter password '1234' in the sidebar.")
    else:
        st.title("⚙️ Teacher Administration")
        tab_struct, tab_goals = st.tabs(["📂 Class Structure", "🎯 Goal Editor"])
        
        with tab_struct:
            st.subheader("Manage Classes & Students")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("### ➕ Add Class")
                new_c = st.text_input("New Class Name")
                if st.button("Create Class") and new_c:
                    if new_c not in st.session_state.db:
                        st.session_state.db[new_c] = {}
                        st.rerun()
            with col_b:
                st.markdown("### 👤 Add Student")
                if st.session_state.db:
                    target_c = st.selectbox("To Class", list(st.session_state.db.keys()))
                    new_s = st.text_input("Student Name")
                    if st.button("Add Student") and new_s:
                        st.session_state.db[target_c][new_s] = {"Grade": "N/A", "Goals": {}}
                        st.rerun()

        with tab_goals:
            st.subheader("IEP Specifications")
            if st.session_state.db:
                e_class = st.selectbox("1. Select Class", list(st.session_state.db.keys()), key="e_c")
                e_student
