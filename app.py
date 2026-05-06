import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="ProTracker - IEP Management", layout="wide")

# 2. Language Selection Logic
if 'lang' not in st.session_state:
    st.session_state.lang = "English"

st.sidebar.title("🌐 Language / 语言")
st.session_state.lang = st.sidebar.selectbox("Select Language", ["English", "中文", "Español"])

# Translation Dictionary
texts = {
    "English": {
        "title": "🎯 ProTracker: IEP Progress",
        "hunt": "📝 Data Hunt",
        "dash": "👩‍🏫 Teacher Dashboard",
        "pass_label": "Password",
        "select_class": "Select Class",
        "select_student": "Select Student",
        "goal_details": "📋 Goal Specifications",
        "baseline": "Baseline (%)",
        "target": "Target (%)",
        "criteria": "Success Criteria",
        "method": "Measurement Method",
        "save_goal": "Save Goal Specs",
        "add_new_goal": "➕ Add New Goal Name",
        "current_goals": "Current IEP Goals",
        "admin_warn": "Admin Access Required (Password: 1234)",
    },
    "中文": {
        "title": "🎯 ProTracker: IEP 进度管理",
        "hunt": "📝 Data Hunt (数据采集)",
        "dash": "👩‍🏫 教师后台管理",
        "pass_label": "管理密码",
        "select_class": "选择班级",
        "select_student": "选择学生",
        "goal_details": "📋 目标详细说明",
        "baseline": "基准线 (%)",
        "target": "目标值 (%)",
        "criteria": "评估标准",
        "method": "评估方法",
        "save_goal": "保存目标设置",
        "add_new_goal": "➕ 添加新目标名称",
        "current_goals": "当前年度 IEP 目标",
        "admin_warn": "需要管理员权限 (密码: 1234)",
    },
    "Español": {
        "title": "🎯 ProTracker: Progreso del IEP",
        "hunt": "📝 Data Hunt",
        "dash": "👩‍🏫 Panel del Maestro",
        "pass_label": "Contraseña",
        "select_class": "Seleccionar Clase",
        "select_student": "Seleccionar Estudiante",
        "goal_details": "📋 Especificaciones de la Meta",
        "baseline": "Línea de Base (%)",
        "target": "Meta Final (%)",
        "criteria": "Criterios de Éxito",
        "method": "Método de Medición",
        "save_goal": "Guardar Detalles",
        "add_new_goal": "➕ Agregar Nueva Meta",
        "current_goals": "Metas Actuales",
        "admin_warn": "Acceso de administrador requerido (Contraseña: 1234)",
    }
}
T = texts[st.session_state.lang]

# 3. Database Initialization
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

# 4. Sidebar Auth & Navigation
st.sidebar.divider()
password = st.sidebar.text_input(T["pass_label"], type="password")
is_teacher = (password == "1234")

mode = st.sidebar.radio("Navigation", [T["hunt"], T["dash"]])

# --- MODE 1: DATA HUNT ---
if mode == T["hunt"]:
    st.title(T["title"])
    classes = list(st.session_state.db.keys())
    if not classes:
        st.info("No classes found. Access the Teacher Dashboard to add one.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            sel_class = st.selectbox(T["select_class"], classes)
        with c2:
            students = list(st.session_state.db[sel_class].keys())
            sel_student = st.selectbox(T["select_student"], students) if students else None
        
        if sel_student:
            st.divider()
            student_data = st.session_state.db[sel_class][sel_student]
            goal_names = list(student_data["Goals"].keys())
            if goal_names:
                sel_goal = st.selectbox(T["current_goals"], goal_names)
                details = student_data["Goals"][sel_goal]
                st.info(f"**{T['goal_details']}**: Baseline: {details['baseline']}% | Target: {details['target']}% | Method: {details['method']}")
                
                with st.form("data_entry_form", clear_on_submit=True):
                    val = st.number_input("Performance (%)", 0, 100, 80)
                    note = st.text_input("Observation Notes")
                    if st.form_submit_button("Submit"):
                        st.success("Recorded!")
            else:
                st.warning("No goals found.")

# --- MODE 2: TEACHER DASHBOARD ---
elif mode == T["dash"]:
    if not is_teacher:
        st.warning(T["admin_warn"])
    else:
        st.title(T["dash"])
        tab_struct, tab_goals = st.tabs(["📂 Structure", "🎯 Goal Editor"])
        
        with tab_struct:
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Add Class")
                new_c = st.text_input("New Class Name")
                if st.button("Create Class") and new_c:
                    if new_c not in st.session_state.db:
                        st.session_state.db[new_c] = {}
                        st.rerun()
            with col_b:
                st.subheader("Add Student")
                if st.session_state.db:
                    target_c = st.selectbox("To Class", list(st.session_state.db.keys()))
                    new_s = st.text_input("Student Name")
                    if st.button("Add Student") and new_s:
                        st.session_state.db[target_c][new_s] = {"Grade": "N/A", "Goals": {}}
                        st.rerun()

        with tab_goals:
            if st.session_state.db:
                e_class = st.selectbox(T["select_class"], list(st.session_state.db.keys()), key="e_c")
                e_students_list = list(st.session_state.db[e_class].keys())
                if e_students_list:
                    e_student = st.selectbox(T["select_student"], e_students_list, key="e_s")
                    st.divider()
                    new_g_name = st.text_input(T["add_new_goal"])
                    if st.button("Add Goal") and new_g_name:
                        st.session_state.db[e_class][e_student]["Goals"][new_g_name] = {"baseline":0, "target":0, "criteria":"", "method":""}
                        st.rerun()
                    
                    goals_dict = st.session_state.db[e_class][e_student]["Goals"]
                    if goals_dict:
                        target_g = st.selectbox("Select Goal to Edit", list(goals_dict.keys()))
                        g_info = goals_dict[target_g]
                        with st.expander(f"Editing: {target_g}", expanded=True):
                            c1, c2 = st.columns(2)
                            with c1:
                                b_val = st.number_input(T["baseline"], value=int(g_info['baseline']))
                                t_val = st.number_input(T["target"], value=int(g_info['target']))
                            with c2:
                                c_val = st.text_input(T["criteria"], value=g_info['criteria'])
                                m_val = st.text_input(T["method"], value=g_info['method'])
                            if st.button(T["save_goal"]):
                                st.session_state.db[e_class][e_student]["Goals"][target_g] = {"baseline": b_val, "target": t_val, "criteria": c_val, "method": m_val}
                                st.success("Updated!")
