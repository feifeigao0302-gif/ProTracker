import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="ProTracker - IEP Management", layout="wide")

# Helper: Privacy Name (Initials)
def get_privacy_name(name):
    parts = name.split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[-1][0]}".upper()
    return name[:2].upper()

# Cartoon Avatars
avatars = {"Robot": "🤖", "Panda": "🐼", "Tiger": "🐯", "Fox": "🦊", "Koala": "🐨", "Frog": "🐸", "Unicorn": "🦄", "Dragon": "🐲"}

# Prompt Levels (Minimal for Grid)
prompt_minimal = {"I": "✅ I", "V": "🗣️ V", "Vi/G": "👁️ Vi/G", "PP": "🖐️ PP", "M": "🎭 M", "FP": "🤝 FP"}

# 2. Initialization - Set Default to English
if 'lang' not in st.session_state: 
    st.session_state.lang = "English"
if 'db' not in st.session_state: 
    st.session_state.db = {}

# Sidebar: Language & Navigation
st.sidebar.title("🌐 Language / 语言")
st.session_state.lang = st.sidebar.selectbox("Select", ["English", "中文", "Español"])

texts = {
    "English": {
        "hunt": "📝 Data Hunt", 
        "dash": "👩‍🏫 Dashboard", 
        "pass": "Password", 
        "save": "Update Goal", 
        "del": "Delete", 
        "add": "Add New Goal", 
        "current": "Current Goals List",
        "nav": "Navigation"
    },
    "中文": {
        "hunt": "📝 数据采集", 
        "dash": "👩‍🏫 教师后台", 
        "pass": "管理密码", 
        "save": "更新此目标", 
        "del": "删除", 
        "add": "添加新目标", 
        "current": "当前所有目标列表",
        "nav": "导航"
    },
    "Español": {
        "hunt": "📝 Data Hunt", 
        "dash": "👩‍🏫 Panel", 
        "pass": "Contraseña", 
        "save": "Actualizar", 
        "del": "Eliminar", 
        "add": "Nueva Meta", 
        "current": "Lista de Metas",
        "nav": "Navegación"
    }
}
T = texts[st.session_state.lang]

st.sidebar.divider()
password = st.sidebar.text_input(T["pass"], type="password")
is_teacher = (password == "1234")
mode = st.sidebar.radio(T["nav"], [T["hunt"], T["dash"]])

# --- MODE 1: DATA HUNT ---
if mode == T["hunt"]:
    st.title("🎯 ProTracker")
    classes = list(st.session_state.db.keys())
    if not classes:
        st.info(T.get("no_data", "No data. Please add classes in Dashboard."))
    else:
        c1, c2 = st.columns(2)
        with c1: sel_class = st.selectbox("Select Class", classes)
        with c2: 
            s_list = list(st.session_state.db[sel_class].keys())
            sel_student = st.selectbox("Select Student", s_list) if s_list else None
        
        if sel_student:
            student_data = st.session_state.db[sel_class][sel_student]
            st.markdown(f"### {student_data['avatar']} Student: {sel_student}")
            goal_names = list(student_data["Goals"].keys())
            
            if goal_names:
                sel_goal = st.selectbox("Select Goal", goal_names)
                st.divider()
                # (10 Trial Grid Logic Here - Ensure you keep the logic from previous version)
                session_key = f"hunt_{sel_student}_{sel_goal}"
                if session_key not in st.session_state: st.session_state[session_key] = ["-"] * 10
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
                # Stats & Submit button...

# --- MODE 2: TEACHER DASHBOARD ---
elif mode == T["dash"]:
    if not is_teacher:
        st.warning("Admin access required.")
    else:
        st.title(T["dash"])
        tab_struct, tab_goals = st.tabs(["📂 Structure", "🎯 Goal Editor"])
        
        with tab_struct:
            col_a, col_b = st.columns(2)
            with col_a:
                nc = st.text_input("New Class Name")
                if st.button("Create Class") and nc: 
                    st.session_state.db[nc] = {}
                    st.rerun()
            with col_b:
                if st.session_state.db:
                    tc = st.selectbox("Assign to Class", list(st.session_state.db.keys()))
                    fn = st.text_input("Full Name (Will be initials)")
                    av = st.selectbox("Avatar", list(avatars.keys()))
                    if st.button("Add Student") and fn:
                        pn = get_privacy_name(fn)
                        st.session_state.db[tc][pn] = {"avatar": avatars[av], "Goals": {}}
                        st.rerun()

        with tab_goals:
            if st.session_state.db:
                c1, c2 = st.columns(2)
                with c1: ec = st.selectbox("Select Class", list(st.session_state.db.keys()), key="ec")
                with c2: 
                    s_list = list(st.session_state.db[ec].keys())
                    es = st.selectbox("Select Student", s_list, key="es") if s_list else None
                
                if es:
                    st.divider()
                    st.subheader(f"{st.session_state.db[ec][es]['avatar']} {es} - Goal Management")
                    
                    with st.expander(T["add"], expanded=True):
                        c_add1, c_add2, c_add3 = st.columns([3, 1, 1])
                        new_g_title = c_add1.text_input("New Goal Title")
                        new_b = c_add2.number_input("Baseline %", 0, 100, 0, key="new_b")
                        new_t = c_add3.number_input("Target %", 0, 100, 80, key="new_t")
                        if st.button("Confirm Add"):
                            if new_g_title:
                                st.session_state.db[ec][es]["Goals"][new_g_title] = {"baseline": new_b, "target": new_t}
                                st.rerun()

                    st.markdown(f"#### {T['current']}")
                    current_goals = st.session_state.db[ec][es]["Goals"]
                    for g_name, g_info in list(current_goals.items()):
                        with st.container():
                            col_edit1, col_edit2, col_edit3, col_edit4 = st.columns([3, 1, 1, 1])
                            col_edit1.markdown(f"**Goal: {g_name}**")
                            edit_b = col_edit2.number_input("Base %", 0, 100, int(g_info['baseline']), key=f"eb_{g_name}")
                            edit_t = col_edit3.number_input("Target %", 0, 100, int(g_info['target']), key=f"et_{g_name}")
                            
                            if col_edit4.button(T["save"], key=f"sv_{g_name}"):
                                st.session_state.db[ec][es]["Goals"][g_name] = {"baseline": edit_b, "target": edit_t}
                                st.success("Updated")
                                st.rerun()
                            if col_edit4.button(T["del"], key=f"dl_{g_name}"):
                                del st.session_state.db[ec][es]["Goals"][g_name]
                                st.rerun()
                            st.divider()
