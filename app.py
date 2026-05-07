import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="ProTracker - IEP Management", layout="wide")

# Helper: Privacy Name (Initials)
def get_privacy_name(name):
    parts = name.split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[-1][0]}".upper()
    return name[:2].upper()

# Cartoon Avatars
avatars = {
    "Robot": "🤖", "Panda": "🐼", "Tiger": "🐯", "Fox": "🦊", 
    "Koala": "🐨", "Frog": "🐸", "Unicorn": "🦄", "Dragon": "🐲",
    "Wizard": "🧙", "Rocket": "🚀", "Star": "⭐", "Alien": "👽"
}

# Prompt Levels (Minimal for Grid)
prompt_minimal = {
    "I": "✅ I", "V": "🗣️ V", "Vi/G": "👁️ Vi/G", 
    "PP": "🖐️ PP", "M": "🎭 M", "FP": "🤝 FP"
}

# 2. Language Selection Logic
if 'lang' not in st.session_state:
    st.session_state.lang = "English"

st.sidebar.title("🌐 Language / 语言")
st.session_state.lang = st.sidebar.selectbox("Select Language", ["English", "中文", "Español"])

# Translation Dictionary
texts = {
    "English": {
        "hunt": "📝 Data Hunt", "dash": "👩‍🏫 Teacher Dashboard",
        "pass_label": "Password", "select_class": "Select Class",
        "select_student": "Select Student", "goal_details": "📋 Specifications",
        "baseline": "Baseline (%)", "target": "Target (%)",
        "save_goal": "Save Specs", "add_new_goal": "➕ Add Goal Name",
        "admin_warn": "Admin Access Required (1234)",
        "no_data": "No data. Please use Dashboard to add classes.",
        "legend_title": "❓ Prompt Level Legend"
    },
    "中文": {
        "hunt": "📝 数据采集 (Data Hunt)", "dash": "👩‍🏫 教师后台管理",
        "pass_label": "管理密码", "select_class": "选择班级",
        "select_student": "选择学生", "goal_details": "📋 目标说明",
        "baseline": "基准线 (%)", "target": "目标值 (%)",
        "save_goal": "保存设置", "add_new_goal": "➕ 添加目标名称",
        "admin_warn": "需要管理员权限 (1234)",
        "no_data": "暂无数据。请前往教师后台添加。",
        "legend_title": "❓ 提示层级说明 (Legend)"
    },
    "Español": {
        "hunt": "📝 Data Hunt", "dash": "👩‍🏫 Panel del Maestro",
        "pass_label": "Contraseña", "select_class": "Seleccionar Clase",
        "select_student": "Seleccionar Estudiante", "goal_details": "📋 Especificaciones",
        "baseline": "Línea de Base (%)", "target": "Meta (%)",
        "save_goal": "Guardar", "add_new_goal": "➕ Nueva Meta",
        "admin_warn": "Acceso requerido (1234)",
        "no_data": "No hay datos. Use el Panel.",
        "legend_title": "❓ Leyenda de Niveles"
    }
}
T = texts[st.session_state.lang]

# 3. Database Initialization
if 'db' not in st.session_state:
    st.session_state.db = {}

# 4. Sidebar Auth & Navigation
st.sidebar.divider()
password = st.sidebar.text_input(T["pass_label"], type="password")
is_teacher = (password == "1234")
mode = st.sidebar.radio("Navigation", [T["hunt"], T["dash"]])

# --- MODE 1: DATA HUNT ---
if mode == T["hunt"]:
    st.title("🎯 ProTracker")
    classes = list(st.session_state.db.keys())
    if not classes:
        st.info(T["no_data"])
    else:
        c1, c2 = st.columns(2)
        with c1:
            sel_class = st.selectbox(T["select_class"], classes)
        with c2:
            student_ids = list(st.session_state.db[sel_class].keys())
            sel_student = st.selectbox(T["select_student"], student_ids) if student_ids else None
        
        if sel_student:
            student_data = st.session_state.db[sel_class][sel_student]
            st.markdown(f"### {student_data['avatar']} Student: {sel_student}")
            goal_names = list(student_data["Goals"].keys())
            
            if goal_names:
                sel_goal = st.selectbox("Goal", goal_names)
                st.divider()
                
                session_key = f"hunt_{sel_student}_{sel_goal}"
                if session_key not in st.session_state:
                    st.session_state[session_key] = ["-"] * 10

                for row in range(2):
                    cols = st.columns(5)
                    for col in range(5):
                        idx = (row * 5) + col
                        with cols[col]:
                            curr = st.session_state[session_key][idx]
                            with st.expander(f"Trial {idx+1}: **{curr}**"):
                                for code, mini in prompt_minimal.items():
                                    if st.button(mini, key=f"btn_{idx}_{code}"):
                                        st.session_state[session_key][idx] = code
                                        st.rerun()

                st.divider()
                results = st.session_state[session_key]
                ind_count = results.count("I")
                total = 10 - results.count("-")
                if total > 0:
                    st.metric("Independent Score", f"{(ind_count/10)*100}%")
                    if st.button("✅ Submit"):
                        st.success("Saved!")
                        st.session_state[session_key] = ["-"] * 10
                        st.rerun()
                
                with st.expander(T["legend_title"], expanded=True):
                    legend_data = {"✅ I": "Independent", "🗣️ V": "Verbal", "👁️ Vi/G": "Visual", "🖐️ PP": "Partial Physical", "🎭 M": "Modeling", "🤝 FP": "Full Physical"}
                    for m, d in legend_data.items(): st.write(f"**{m}** : {d}")

# --- MODE 2: TEACHER DASHBOARD ---
elif mode == T["dash"]:
    if not is_teacher:
        st.warning(T["admin_warn"])
    else:
        st.title(T["dash"])
        tab1, tab2 = st.tabs(["📂 Structure", "🎯 Goal Editor"])
        with tab1:
            col_a, col_b = st.columns(2)
            with col_a:
                nc = st.text_input("New Class")
                if st.button("Create") and nc:
                    st.session_state.db[nc] = {}; st.rerun()
            with col_b:
                if st.session_state.db:
                    tc = st.selectbox("To Class", list(st.session_state.db.keys()))
                    fn = st.text_input("Full Name (Initial Only)")
                    av = st.selectbox("Avatar", list(avatars.keys()))
                    if st.button("Add Student") and fn:
                        pn = get_privacy_name(fn)
                        st.session_state.db[tc][pn] = {"avatar": avatars[av], "Goals": {}}
                        st.rerun()
        with tab2:
            if st.session_state.db:
                ec = st.selectbox(T["select_class"], list(st.session_state.db.keys()), key="ec")
                es = st.selectbox(T["select_student"], list(st.session_state.db[ec].keys()), key="es")
                if es:
                    ng = st.text_input(T["add_new_goal"])
                    if st.button("Assign") and ng:
                        st.session_state.db[ec][es]["Goals"][ng] = {"baseline":0, "target":0}
                        st.rerun()
