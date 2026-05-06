import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="ProTracker - IEP Management", layout="wide")

# 2. Language Selection
if 'lang' not in st.session_state:
    st.session_state.lang = "English"

st.sidebar.title("🌐 Language")
st.session_state.lang = st.sidebar.selectbox("Select Language", ["English", "中文", "Español"])

# 3. Translation Dictionary
texts = {
    "English": {
        "title": "🎯 ProTracker: IEP Progress",
        "hunt": "📝 Data Hunt",
        "dash": "👩‍🏫 Teacher Dashboard",
        "pass_label": "Password",
        "select_class": "Select Class",
        "select_student": "Select Student",
        "add_class": "➕ Add New Class",
        "add_student": "👤 Add New Student",
        "save": "Save Changes",
        "admin_warn": "Admin Access Required (Password: 1234)",
    },
    "中文": {
        "title": "🎯 ProTracker: IEP 进度管理",
        "hunt": "📝 Data Hunt (数据采集)",
        "dash": "👩‍🏫 教师后台管理",
        "pass_label": "管理密码",
        "select_class": "选择班级",
        "select_student": "选择学生",
        "add_class": "➕ 添加新班级",
        "add_student": "👤 添加新学生",
        "save": "保存修改",
        "admin_warn": "需要管理员权限 (密码: 1234)",
    },
    "Español": {
        "title": "🎯 ProTracker: Progreso del IEP",
        "hunt": "📝 Data Hunt",
        "dash": "👩‍🏫 Panel del Maestro",
        "pass_label": "Contraseña",
        "select_class": "Seleccionar Clase",
        "select_student": "Seleccionar Estudiante",
        "add_class": "➕ Agregar Nueva Clase",
        "add_student": "👤 Agregar Nuevo Estudiante",
        "save": "Guardar Cambios",
        "admin_warn": "Acceso de administrador requerido (Contraseña: 1234)",
    }
}
T = texts[st.session_state.lang]

# 4. Database Initialization
if 'db' not in st.session_state:
    st.session_state.db = {
        "Class A (DLI)": {
            "Student Alpha": {"Grade": "3rd", "Goals": {}}
        }
    }

# 5. Sidebar Auth
st.sidebar.markdown("---")
password = st.sidebar.text_input(T["pass_label"], type="password")
is_teacher = (password == "1234")
mode = st.sidebar.radio("Navigation", [T["hunt"], T["dash"]])

# --- Logic A: Data Hunt (Public View) ---
if mode == T["hunt"]:
    st.title(T["title"])
    classes = list(st.session_state.db.keys())
    if not classes:
        st.info("No classes added yet.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            sel_class = st.selectbox(T["select_class"], classes)
        with c2:
            students = list(st.session_state.db[sel_class].keys())
            sel_student = st.selectbox(T["select_student"], students) if students else None
        
        if sel_student:
            st.success(f"Ready to collect data for {sel_student}")
            # (Goal collection logic here...)

# --- Logic B: Teacher Dashboard (Admin View) ---
elif mode == T["dash"]:
    if not is_teacher:
        st.warning(T["admin_warn"])
    else:
        st.title(T["dash"])
        
        # 1. Manage Classes & Students
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(T["add_class"])
            new_c = st.text_input("New Class Name")
            if st.button("Create Class") and new_c:
                if new_c not in st.session_state.db:
                    st.session_state.db[new_c] = {}
                    st.rerun()
        
        with col2:
            st.subheader(T["add_student"])
            if list(st.session_state.db.keys()):
                target_c = st.selectbox("To Class", list(st.session_state.db.keys()))
                new_s = st.text_input("New Student Name")
                if st.button("Add Student") and new_s:
                    st.session_state.db[target_c][new_s] = {"Grade": "N/A", "Goals": {}}
                    st.rerun()

        st.divider()
        st.write("Current Classes in Database:", list(st.session_state.db.keys()))
