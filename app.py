import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="ProTracker - IEP Management", layout="wide")

# Helper function to get initials
def get_initials(name):
    return "".join([part[0].upper() for part in name.split() if part])

# 2. Prompt Levels Definition
prompt_options = {
    "I": "Independent",
    "V": "Verbal Prompt",
    "Vi/G": "Visual / Gestural",
    "PP": "Partial Physical",
    "M": "Modeling",
    "FP": "Full Physical"
}

# 3. Database & Session State Initialization
if 'db' not in st.session_state:
    st.session_state.db = {}

# 4. Sidebar Auth & Navigation
st.sidebar.title("🌐 ProTracker")
password = st.sidebar.text_input("Password", type="password")
is_teacher = (password == "1234")
mode = st.sidebar.radio("Navigation", ["📝 Data Hunt", "👩‍🏫 Teacher Dashboard"])

# --- MODE 1: DATA HUNT (10-Trial Grid) ---
if mode == "📝 Data Hunt":
    st.title("🎯 IEP Data Hunt")
    
    classes = list(st.session_state.db.keys())
    if not classes:
        st.info("No data found. Please add classes and students in the Dashboard.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            sel_class = st.selectbox("Select Class", classes)
        with c2:
            students = list(st.session_state.db[sel_class].keys())
            sel_student = st.selectbox("Select Student", students) if students else None
        
        if sel_student:
            student_data = st.session_state.db[sel_class][sel_student]
            goal_names = list(student_data["Goals"].keys())
            
            if goal_names:
                sel_goal = st.selectbox("Select IEP Goal", goal_names)
                st.divider()
                
                st.subheader(f"Data Collection for: {sel_goal}")
                
                # Unique key for this specific session
                session_key = f"hunt_{sel_student}_{sel_goal}"
                if session_key not in st.session_state:
                    st.session_state[session_key] = ["-"] * 10

                # Render the 10-Trial Grid
                st.write("Click a trial to select the prompt level:")
                
                # We use 5 columns x 2 rows
                for row in range(2):
                    cols = st.columns(5)
                    for col in range(5):
                        idx = (row * 5) + col
                        with cols[col]:
                            # Display current status in the button label
                            current_status = st.session_state[session_key][idx]
                            # Using an expander for each trial to act as a "popup" menu
                            with st.expander(f"Trial {idx+1}: **{current_status}**"):
                                for code, label in prompt_options.items():
                                    if st.button(f"{code} - {label}", key=f"btn_{idx}_{code}"):
                                        st.session_state[session_key][idx] = code
                                        st.rerun()

                st.divider()
                
                # --- Real-time Stats ---
                trial_results = st.session_state[session_key]
                ind_count = trial_results.count("I")
                total_taken = 10 - trial_results.count("-")
                
                s1, s2, s3 = st.columns(3)
                if total_taken > 0:
                    score = (ind_count / 10) * 100
                    s1.metric("Independent Score", f"{score}%")
                    s2.metric("Trials Logged", f"{total_taken}/10")
                    s3.progress(total_taken / 10)
                
                if st.button("✅ Submit and Clear"):
                    st.success("Session saved successfully!")
                    st.session_state[session_key] = ["-"] * 10
                    st.rerun()
            else:
                st.warning("Please add goals for this student first.")

# --- MODE 2: TEACHER DASHBOARD (Admin Logic) ---
elif mode == "👩‍🏫 Teacher Dashboard":
    if not is_teacher:
        st.warning("Admin Access Required.")
    else:
        st.title("⚙️ Teacher Administration")
        tab_struct, tab_goals = st.tabs(["📂 Structure", "🎯 Goal Editor"])
        
        with tab_struct:
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Add Class")
                nc = st.text_input("New Class Name")
                if st.button("Create"):
                    if nc: st.session_state.db[nc] = {}; st.rerun()
            with col_b:
                st.subheader("Add Student")
                if st.session_state.db:
                    tc = st.selectbox("To Class", list(st.session_state.db.keys()))
                    ns = st.text_input("Full Name")
                    if st.button("Add"):
                        ini = get_initials(ns)
                        st.session_state.db[tc][ini] = {"Goals": {}}
                        st.rerun()
        
        with tab_goals:
            if st.session_state.db:
                e_c = st.selectbox("Class", list(st.session_state.db.keys()), key="ec")
                e_s = st.selectbox("Student", list(st.session_state.db[e_c].keys()), key="es")
                if e_s:
                    ng = st.text_input("Add Goal Name")
                    if st.button("Add Goal"):
                        st.session_state.db[e_c][e_s]["Goals"][ng] = {"baseline":0, "target":0}
                        st.rerun()
