import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="ProTracker - IEP Management", layout="wide")

# Helper function to get initials
def get_initials(name):
    return "".join([part[0].upper() for part in name.split() if part])

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
        "select_student": "Select Student (Initials)",
        "goal_details": "📋 Goal Specifications",
        "baseline": "Baseline (%)",
        "target": "Target (%)",
        "criteria": "Success Criteria",
        "method": "Measurement Method",
        "save_goal": "Save Goal Specs",
        "add_new_goal": "➕ Add New Goal Name",
        "current_goals": "Current IEP Goals",
        "admin_warn": "Admin Access Required (1234)",
        "no_data": "No data found. Add classes in the Dashboard.",
    },
    "中文": {
        "title": "🎯 ProTracker: IEP 进度管理",
        "hunt": "📝 数据采集 (Data Hunt)",
        "dash": "👩‍🏫 教师后台管理",
        "pass_label": "管理密码",
        "select_class": "选择班级",
        "select_student": "选择学生 (首字母)",
        "goal_details": "📋 目标详细说明",
        "baseline": "基准线 (%)",
        "target": "目标值 (%)",
        "criteria": "评估标准",
        "method": "评估方法",
        "save_goal": "保存目标设置",
        "add_new_goal": "➕ 添加新目标名称",
        "current_goals": "当前年度 IEP 目标",
        "admin_warn": "需要管理员权限 (1234)",
        "no_data": "暂无数据。请前往教师后台添加。",
    },
    "Español": {
        "title": "🎯 ProTracker: Progreso del IEP",
        "hunt": "📝 Data Hunt",
        "dash": "👩‍🏫 Panel del Maestro",
        "pass_label": "Contraseña",
        "select_class": "Seleccionar Clase",
        "select_student": "Seleccionar Estudiante (Iniciales)",
        "goal_details": "📋 Especificaciones de la Meta",
        "baseline": "Línea de Base (%)",
        "target": "Meta Final (%)",
        "criteria": "Criterios de Éxito",
        "method": "Método de Medición",
        "save_goal": "Guardar Detalles",
        "add_new_goal": "➕ Agregar Nueva Meta",
        "current_goals": "Metas Actuales",
        "admin_warn": "Acceso de administrador requerido (1234)",
        "no_data": "No hay datos. Agregue clases en el panel.",
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
    st.title(T["title"])
    classes = list(st.session_state.db.keys())
    if not classes:
        st.info(T["no_data"])
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
