import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="ProTracker - Professional IEP Tracking", layout="wide")

# 2. Language Selection Logic
if 'lang' not in st.session_state:
    st.session_state.lang = "English"

# Sidebar Language Toggle
st.sidebar.title("🌐 Language / 语言 / Idioma")
st.session_state.lang = st.sidebar.selectbox("Select Interface Language", ["English", "中文", "Español"])

# Translation Dictionary
texts = {
    "English": {
        "title": "🎯 ProTracker: Progress Monitoring",
        "nav": "🚀 Navigation",
        "hunt": "📝 Data Hunt (Quick Entry)",
        "dash": "👩‍🏫 Teacher Dashboard",
        "pass_label": "Enter Teacher Password",
        "select_class": "Select Class",
        "select_student": "Select Student",
        "select_goal": "Select IEP Goal",
        "grade": "Current Grade",
        "submit": "Submit Data",
        "success": "Data saved successfully!",
        "admin_warn": "⚠️ Admin access required. Please enter password in the sidebar.",
        "edit_info": "🛠 Edit Student Background",
        "analysis": "📊 Data Analytics",
    },
    "中文": {
        "title": "🎯 ProTracker: 进度跟踪系统",
        "nav": "🚀 导航菜单",
        "hunt": "📝 Data Hunt (数据采集)",
        "dash": "👩‍🏫 教师后台",
        "pass_label": "请输入管理密码",
        "select_class": "选择班级",
        "select_student": "选择学生",
        "select_goal": "选择 IEP 目标",
        "grade": "当前年级",
        "submit": "提交数据",
        "success": "数据保存成功！",
        "admin_warn": "⚠️ 需要管理员权限。请在侧边栏输入密码。",
        "edit_info": "🛠 编辑学生基本信息",
        "analysis": "📊 数据深度分析",
    },
    "Español": {
        "title": "🎯 ProTracker: Monitoreo de Progreso",
        "nav": "🚀 Navegación",
        "hunt": "📝 Data Hunt (Entrada Rápida)",
        "dash": "👩‍🏫 Panel del Maestro",
        "pass_label": "Ingrese la contraseña del maestro",
        "select_class": "Seleccionar Clase",
        "select_student": "Seleccionar Estudiante",
        "select_goal": "Seleccionar Meta del IEP",
        "grade": "Grado Actual",
        "submit": "Enviar Datos",
        "success": "¡Datos guardados con éxito!",
        "admin_warn": "⚠️ Se requiere acceso de administrador. Ingrese la contraseña en la barra lateral.",
        "edit_info": "🛠 Editar Información del Estudiante",
        "analysis": "📊 Análisis de Datos",
    }
}

T = texts[st.session_state.lang]

# 3. Mock Database
if 'db' not in st.session_state:
    st.session_state.db = {
        "Class A (DLI)": {
            "Student Alpha": {"Grade": "3rd", "Info": "Dual Language Immersion", "Goals": ["Reading Comp", "Mandarin Fluency"]},
            "Student Beta": {"Grade": "3rd", "Info": "Resource Support", "Goals": ["Math Fluency"]}
        },
        "Class B": {
            "Student Gamma": {"Grade": "4th", "Info": "General Ed", "Goals": ["Social Skills"]}
        }
    }

# 4. Sidebar Navigation
st.sidebar.markdown("---")
# Password updated to 1234
password = st.sidebar.text_input(T["pass_label"], type="password")
is_teacher = (password == "1234")

st.sidebar.title(T["nav"])
mode = st.sidebar.radio("Go to:", [T["hunt"], T["dash"]])

# --- Logic A: Data Hunt (Public Access) ---
if mode == T["hunt"]:
    st.title(T["title"])
    
    col1, col2 = st.columns(2)
    with col1:
        chosen_class = st.selectbox(T["select_class"], list(st.session_state.db.keys()))
    with col2:
        students = list(st.session_state.db[chosen_class].keys())
        chosen_student = st.selectbox(T["select_student"], students)
    
    st.info(f"**{T['grade']}**: {st.session_state.db[chosen_class][chosen_student]['Grade']}")
    
    goal = st.selectbox(T["select_goal"], st.session_state.db[chosen_class][chosen_student]['Goals'])
    
    with st.form("quick_input"):
        score = st.number_input("Score (%) / Puntaje (%)", 0, 100, 80)
        note = st.text_input("Observation Notes / Observaciones")
        if st.form_submit_button(T["submit"]):
            st.success(T["success"])

# --- Logic B: Teacher Dashboard (Password Protected) ---
elif mode == T["dash"]:
    if not is_teacher:
        st.warning(T["admin_warn"])
    else:
        st.title(T["dash"])
        active_class = st.selectbox(T["select_class"], list(st.session_state.db.keys()))
        active_student = st.selectbox(T["select_student"], list(st.session_state.db[active_class].keys()))
        
        st.subheader(T["edit_info"])
        st.text_area("Background Info", st.session_state.db[active_class][active_student]['Info'])
        
        st.markdown("---")
        st.subheader(T["analysis"])
        df = pd.DataFrame({'Day': [1,2,3,4,5], 'Score': [70,72,75,78,85]})
        fig = px.line(df, x='Day', y='Score', title=f"Progress Trend for {active_student}")
        st.plotly_chart(fig, use_container_width=True)
