import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="ProTracker - IEP Management", layout="wide")

# Helper function to get initials/privacy name
def get_privacy_name(name):
    parts = name.split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[-1][0]}".upper() # First and Last initial
    return name[:2].upper() # First two letters if only one name

# Cartoon Avatar Library (Using Emojis as lightweight avatars)
avatars = {
    "Robot": "🤖", "Panda": "🐼", "Tiger": "🐯", "Fox": "🦊", 
    "Koala": "🐨", "Frog": "🐸", "Unicorn": "🦄", "Dragon": "🐲",
    "Wizard": "🧙", "Rocket": "🚀", "Star": "⭐", "Alien": "👽"
}

# 2. Prompt Levels Definition
prompt_options = {
    "I": "Independent", "V": "Verbal Prompt", "Vi/G": "Visual / Gestural",
    "PP": "Partial Physical", "M": "Modeling", "FP": "Full Physical"
}

# 3. Database Initialization
if 'db' not in st.session_state:
    st.session_state.db = {}

# 4. Sidebar Navigation
st.sidebar.title("🌐 ProTracker")
password = st.sidebar.text_input("Password", type="password")
is_teacher = (password == "1234")
mode = st.sidebar.radio("Navigation", ["📝 Data Hunt", "👩‍🏫 Teacher Dashboard"])

# --- MODE 1: DATA HUNT ---
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
            student_ids = list(st.session_state.db[sel_class].keys())
            sel_student = st.selectbox("Select Student (ID)", student_ids) if student_ids else None
        
        if sel_student:
            s_data = st.session_state.db[sel_class][sel_student]
            st.markdown(f"### {s_data['avatar']} Student: {sel_student}")
            
            goals = list(s_data["Goals"].keys())
            if goals:
                sel_goal = st.selectbox("Select IEP Goal", goals)
                st.divider()
                
                # 10-Trial Logic
                session_key = f"hunt_{sel_student}_{sel_goal}"
                if session_key not in st.session_state:
                    st.session_state[session_key] = ["-"] * 10

                st.write("Record Prompt Levels:")
                for row in range(2):
                    cols = st.columns(5)
                    for col in range(5):
                        idx = (row * 5) + col
                        with cols[col]:
                            curr = st.session_state[session_key][idx]
                            with st.expander(f"Trial {idx+1}: **{curr}**"):
                                for code, label in prompt_options.items():
                                    if st.button(f"{code} - {label}", key=f"btn_{idx}_{code}"):
                                        st.session_state[session_key][idx] = code
                                        st.rerun()

                st.divider()
                trial_results = st.session_state[session_key]
                ind_count = trial_results.count("I")
                total = 10 - trial_results.count("-")
                
                if total > 0:
                    st.metric("Independent Score", f"{(ind_count/10)*100}%")
                    if st.button("✅ Submit Session"):
                        st.success("Session saved!")
                        st.session_state[session_key] = ["-"] * 10
                        st.rerun()
            else:
                st.warning("No goals assigned.")

# --- MODE 2: TEACHER DASHBOARD ---
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
                st.subheader("Add Student (Private)")
                if st.session_state.db:
                    tc = st.selectbox("To Class", list(st.session_state.db.keys()))
                    raw_name = st.text_input("Name (Will be stored as Initials)")
                    sel_avatar = st.selectbox("Choose Cartoon Avatar", list(avatars.keys()))
                    
                    if st.button("Add Student"):
                        if raw_name:
                            p_name = get_privacy_name(raw_name)
                            st.session_state.db[tc][p_name] = {
                                "avatar": avatars[sel_avatar],
                                "Goals": {}
                            }
                            st.success(f"Added as {p_name} {avatars[sel_avatar]}")
                            st.rerun()

        with tab_goals:
            if st.session_state.db:
                e_c = st.selectbox("Class", list(st.session_state.db.keys()), key="ec")
                e_s = st.selectbox("Student", list(st.session_state.db[e_c].keys()), key="es")
                if e_s:
                    ng = st.text_input("New Goal Name")
                    if st.button("Assign Goal"):
                        st.session_state.db[e_c][e_s]["Goals"][ng] = {"baseline":0}
                        st.rerun()
