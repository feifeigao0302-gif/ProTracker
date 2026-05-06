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

# 3. Enhanced Translation Dictionary (Added Goal Details)
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
        "save_goal": "Save/Update Goal Details",
        "add_new_goal": "➕ Add New Goal Name",
        "current_goals": "Current IEP Goals",
        "data_entry": "📥 Data Entry",
        "analysis": "📊 Analytics",
    },
    "中文": {
        "title": "🎯 ProTracker: IEP 进度管理",
        "hunt": "📝 Data Hunt (数据采集)",
        "dash": "👩‍🏫 教师后台管理",
        "pass_label": "管理密码",
        "select_class": "选择班级",
        "select_student": "选择学生",
        "goal_details": "📋 目标详细说明",
        "baseline": "基准线 (Baseline %)",
        "target": "目标值 (Target %)",
        "criteria": "达标标准 (Criteria)",
        "method": "评估方法 (Method)",
        "save_goal": "保存/更新目标详情",
        "add_new_goal": "➕ 添加新目标名称",
        "current_goals": "当前年度 IEP 目标",
        "data_entry": "📥 数据记录",
        "analysis": "📊 数据趋势分析",
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
        "save_goal": "Guardar Detalles de la Meta",
        "add_new_goal": "➕ Agregar Nuevo Nombre de Meta",
        "current_goals": "Metas Actuales del IEP",
        "data_entry": "📥 Entrada de Datos",
        "analysis": "📊 Análisis",
    }
}

T = texts[st.session_state.lang]

# 4. Professional Database Structure
if 'db' not in st.session_state:
    # We store goals as a dictionary to hold their specific details
    st.session_state.db = {
        "Class A (DLI)": {
            "Student Alpha": {
                "Grade": "3rd", 
                "Goals": {
                    "Reading Comp": {"baseline": 30, "target": 80, "criteria": "4/5 trials", "method": "Wh- Questions"},
                    "Mandarin Fluency": {"baseline": 20, "target": 70, "criteria": "100 characters", "method": "Oral reading"}
                }
            }
        }
    }

# 5. Sidebar Auth & Navigation
st.sidebar.markdown("---")
password = st.sidebar.text_input(T["pass_label"], type="password")
is_teacher = (password == "1234")

mode = st.sidebar.radio("Navigation", [T["hunt"], T["dash"]])

# --- Logic A: Data Hunt (Public View) ---
if mode == T["hunt"]:
    st.title(T["title"])
    c1, c2 = st.columns(2)
    with c1:
        chosen_class = st.selectbox(T["select_class"], list(st.session_state.db.keys()))
    with c2:
        students = list(st.session_state.db[chosen_class].keys())
        chosen_student = st.selectbox(T["select_student"], students)
    
    st.divider()
    
    # Display Student Info
    student_data = st.session_state.db[chosen_class][chosen_student]
    goal_names = list(student_data["Goals"].keys())
    selected_goal = st.selectbox(T["current_goals"], goal_names)
    
    # Show Specific Goal Info for the Data Collector to see
    details = student_data["Goals"][selected_goal]
    st.info(f"**{T['goal_details']}**: Baseline: {details['baseline']}% | Target: {details['target']}% | Method: {details['method']}")

    with st.form("input_form"):
        score = st.number_input("Performance (%)", 0, 100, 80)
        note = st.text_input("Observations")
        if st.form_submit_button("Submit"):
            st.success("Successfully Recorded!")

# --- Logic B: Teacher Dashboard (Admin View) ---
elif mode == T["dash"]:
    if not is_teacher:
        st.warning("Admin Access Required")
    else:
        st.title(T["dash"])
        
        # Select Student to manage
        t_class = st.selectbox(T["select_class"], list(st.session_state.db.keys()))
        t_student = st.selectbox(T["select_student"], list(st.session_state.db[t_class].keys()))
        
        st.divider()
        
        # 1. Add/Edit Goal Names
        st.subheader(T["add_new_goal"])
        new_g_name = st.text_input("Goal Name")
        if st.button("Add to Student Profile") and new_g_name:
            if new_g_name not in st.session_state.db[t_class][t_student]["Goals"]:
                st.session_state.db[t_class][t_student]["Goals"][new_g_name] = {"baseline": 0, "target": 0, "criteria": "", "method": ""}
                st.rerun()

        st.divider()

        # 2. EDIT GOAL DETAILS
        st.subheader(T["goal_details"])
        edit_goal = st.selectbox("Select Goal to Edit Details", list(st.session_state.db[t_class][t_student]["Goals"].keys()))
        
        g_data = st.session_state.db[t_class][t_student]["Goals"][edit_goal]
        
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                b_line = st.number_input(T["baseline"], value=g_data["baseline"])
                t_line = st.number_input(T["target"], value=g_data["target"])
            with col2:
                crit = st.text_input(T["criteria"], value=g_data["criteria"])
                meth = st.text_input(T["method"], value=g_data["method"])
            
            if st.button(T["save_goal"]):
                st.session_state.db[t_class][t_student]["Goals"][edit_goal] = {
                    "baseline": b_line, "target": t_line, "criteria": crit, "method": meth
                }
                st.success("Goal Details Updated!")

        # 3. Analytics
        st.divider()
        st.subheader(T["analysis"])
        chart_df = pd.DataFrame({'Day': [1,2,3,4,5], 'Score': [b_line, b_line+5, b_line+10, b_line+15, t_line]})
        fig = px.line(chart_df, x='Day', y='Score', markers=True)
        st.plotly_chart(fig, use_container_width=True)
