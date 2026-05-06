import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 页面配置
st.set_page_config(page_title="ProTracker - IEP Management", layout="wide")

# 2. 语言选择
if 'lang' not in st.session_state:
    st.session_state.lang = "English"

st.sidebar.title("🌐 Language")
st.session_state.lang = st.sidebar.selectbox("Select Language", ["English", "中文", "Español"])

# 3. 翻译字典（增加了班级和学生管理的词条）
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
        "edit_goal": "🎯 Manage IEP Goals",
        "save": "Save Changes",
        "delete": "Delete",
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
        "edit_goal": "🎯 管理 IEP 目标",
        "save": "保存修改",
        "delete": "删除",
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
        "edit_goal": "🎯 Gestionar Metas del IEP",
        "save": "Guardar Cambios",
        "delete": "Eliminar",
    }
}

T = texts[st.session_state.lang]

# 4. 数据库初始化逻辑
def initialize_db():
    return {
        "Class A (DLI)": {
            "Student Alpha": {
                "Grade": "3rd", 
                "Goals": {
                    "Reading Comp": {"baseline": 30, "target": 80, "criteria": "4/5 trials", "method": "Wh- Questions"}
                }
            }
        }
    }

if 'db' not in st.session_state:
    st.session_state.db = initialize_db()

# 5. 侧边栏
st.sidebar.markdown("---")
password = st.sidebar.text_input(T["pass_label"], type="password")
is_teacher = (password == "1234")
mode = st.sidebar.radio("Navigation", [T["hunt"], T["dash"]])

# --- 逻辑 A: Data Hunt (采集页面) ---
if mode == T["hunt"]:
    st.title(T["title"])
    class_list = list(st.session_state.db.keys())
    if not class_list:
        st.warning("No classes found. Please ask teacher to add a class.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            chosen_class = st.selectbox(T["select_class"], class_list)
        with c2:
            student_list = list(st.session_state.db[chosen_class].keys())
            chosen_student = st.selectbox(T["select_student"], student_list) if student_list else None
        
        if chosen_student:
            st.divider()
            student_data = st.session_state.db[chosen_class][chosen_student]
            goal_names = list(student_data["Goals"].keys())
            if goal_names:
                selected_goal = st.selectbox("Goal", goal_names)
                details = student_data["Goals"][selected_goal]
                st.info(f"Baseline: {details['baseline']}% | Target: {details['target']}%")
                with st.form("input_form"):
                    score = st.number_input("Score (%)", 0, 100, 80)
                    if st.form_submit_button("Submit"):
                        st.success("Recorded!")
            else:
                st.write("No goals set for this student.")

# --- 逻辑 B: Teacher Dashboard (管理页面) ---
elif mode == T["dash"]:
    if not is_teacher:
        st.warning("Admin Access Required (Password: 1234)")
    else:
        st.title(T["dash"])
        
        # --- 第一部分：班级与学生管理 ---
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader(T["add_class"])
            new_class = st.text_input("New Class Name")
            if st.button("Create Class") and new_class:
                if new_class not in st.session_state.db:
                    st.session_state.db[new_class] = {}
                    st.success(f"Class '{new_class}' added!")
                    st.rerun()

        with col_b:
            st.subheader(T["add_student"])
            target_class = st.selectbox("To Class", list(st.session_state.db.keys()))
            new_student = st.text_input("Student Name")
            if st.button("Add Student") and new_student:
                if new_student not in st.session_state.db[target_class]:
                    st.session_state.db[target_class][new_student] = {"Grade": "N/A", "Goals": {}}
                    st.success(f"Student '{new_student}' added to {target_class}!")
                    st.rerun()

        st.divider()
        
        # --- 第二部分：具体信息编辑 ---
        st.subheader("📝 Edit Details")
        all_classes = list(st.session_state.db.keys())
        if all_classes:
            edit_class = st.selectbox("Select Class to Manage", all_classes)
            all_students = list(st.session_state.db[edit_class].keys())
            
            if all_students:
                edit_student = st.selectbox("Select Student to Edit", all_students)
                
                # 修改基本信息
                curr_grade = st.session_state.db[edit_class][edit_student]["Grade"]
                new_grade = st.text_input("Grade", value=curr_grade)
                
                # 管理 IEP Goals
                st.write("---")
                st
