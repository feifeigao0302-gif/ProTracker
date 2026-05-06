import streamlit as st

# 1. 页面配置
st.set_page_config(page_title="ProTracker - IEP Management", layout="wide")

# 辅助函数：隐私姓名
def get_privacy_name(name):
    parts = name.split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[-1][0]}".upper()
    return name[:2].upper()

# 卡通头像库
avatars = {"Robot": "🤖", "Panda": "🐼", "Tiger": "🐯", "Fox": "🦊", "Koala": "🐨", "Frog": "🐸", "Unicorn": "🦄", "Dragon": "🐲"}

# 提示层级简写
prompt_minimal = {"I": "✅ I", "V": "🗣️ V", "Vi/G": "👁️ Vi/G", "PP": "🖐️ PP", "M": "🎭 M", "FP": "🤝 FP"}

# 2. 语言与数据库初始化
if 'lang' not in st.session_state: st.session_state.lang = "English"
if 'db' not in st.session_state: st.session_state.db = {}

st.sidebar.title("🌐 Language")
st.session_state.lang = st.sidebar.selectbox("Select Language", ["English", "中文", "Español"])

texts = {
    "English": {"hunt": "📝 Data Hunt", "dash": "👩‍🏫 Dashboard", "pass": "Password", "sel_c": "Select Class", "sel_s": "Select Student", "add_g": "➕ Add New Goal", "manage_g": "🎯 Manage Goals", "save": "Save Changes", "del": "Delete Goal"},
    "中文": {"hunt": "📝 数据采集", "dash": "👩‍🏫 教师后台", "pass": "管理密码", "sel_c": "选择班级", "sel_s": "选择学生", "add_g": "➕ 添加新目标", "manage_g": "🎯 目标管理列表", "save": "保存修改", "del": "删除目标"},
    "Español": {"hunt": "📝 Data Hunt", "dash": "👩‍🏫 Panel", "pass": "Contraseña", "sel_c": "Clase", "sel_s": "Estudiante", "add_g": "➕ Nueva Meta", "manage_g": "🎯 Gestionar Metas", "save": "Guardar", "del": "Eliminar"}
}
T = texts[st.session_state.lang]

# 3. 导航逻辑
st.sidebar.divider()
password = st.sidebar.text_input(T["pass"], type="password")
is_teacher = (password == "1234")
mode = st.sidebar.radio("Navigation", [T["hunt"], T["dash"]])

# --- MODE 1: DATA HUNT (略，保持之前的逻辑) ---
if mode == T["hunt"]:
    st.title("🎯 ProTracker")
    # ... (保持之前的 10 格 Trial 逻辑)
    # 为了节省空间，这里略过重复部分，请确保合并时保留这块代码

# --- MODE 2: TEACHER DASHBOARD (增强版目标编辑) ---
elif mode == T["dash"]:
    if not is_teacher:
        st.warning("Admin Access Required.")
    else:
        st.title(T["dash"])
        tab_struct, tab_goals = st.tabs(["📂 结构管理 (Structure)", "🎯 目标编辑 (Goal Editor)"])
        
        with tab_struct:
            # (班级和学生添加逻辑保持不变...)
            c1, c2 = st.columns(2)
            with c1:
                nc = st.text_input("New Class Name")
                if st.button("Create Class") and nc:
                    if nc not in st.session_state.db: st.session_state.db[nc] = {}; st.rerun()
            with c2:
                if st.session_state.db:
                    tc = st.selectbox("Assign to Class", list(st.session_state.db.keys()))
                    fn = st.text_input("Student Full Name")
                    av = st.selectbox("Avatar", list(avatars.keys()))
                    if st.button("Add Student") and fn:
                        pn = get_privacy_name(fn)
                        st.session_state.db[tc][pn] = {"avatar": avatars[av], "Goals": {}}
                        st.rerun()

        with tab_goals:
            if not st.session_state.db:
                st.info("Please create a class first.")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    e_c = st.selectbox(T["sel_c"], list(st.session_state.db.keys()), key="edit_c")
                with col2:
                    e_s_list = list(st.session_state.db[e_c].keys())
                    e_s = st.selectbox(T["sel_s"], e_s_list, key="edit_s") if e_s_list else None
                
                if e_s:
                    st.divider()
                    st.subheader(f"{T['manage_g']}: {st.session_state.db[e_c][e_s]['avatar']} {e_s}")
                    
                    # 1. 添加新目标部分
                    with st.expander(T["add_g"], expanded=False):
                        new_g_name = st.text_input("Goal Title (e.g., Reading Comprehension)")
                        c_base, c_tar = st.columns(2)
                        b_val = c_base.number_input("Baseline (%)", 0, 100, 0)
                        t_val = c_tar.number_input("Target (%)", 0, 100, 80)
                        if st.button("Confirm Add Goal"):
                            if new_g_name:
                                st.session_state.db[e_c][e_s]["Goals"][new_g_name] = {"baseline": b_val, "target": t_val}
                                st.success(f"Goal '{new_g_name}' added!")
                                st.rerun()

                    # 2. 已有目标修改列表
                    current_goals = st.session_state.db[e_c][e_s]["Goals"]
                    if not current_goals:
                        st.write("No goals yet.")
                    else:
                        for g_name, g_info in list(current_goals.items()):
                            with st.container
