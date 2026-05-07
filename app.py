import streamlit as st

# 1. 页面基本配置
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

# 2. 初始化
if 'lang' not in st.session_state: st.session_state.lang = "English"
if 'db' not in st.session_state: st.session_state.db = {}

# 侧边栏：语言与导航
st.sidebar.title("🌐 语言 / Language")
st.session_state.lang = st.sidebar.selectbox("Select", ["中文", "English", "Español"])

texts = {
    "中文": {"hunt": "📝 数据采集", "dash": "👩‍🏫 教师后台", "pass": "管理密码", "save": "更新此目标", "del": "删除", "add": "添加新目标", "current": "当前所有目标列表"},
    "English": {"hunt": "📝 Data Hunt", "dash": "👩‍🏫 Dashboard", "pass": "Password", "save": "Update", "del": "Delete", "add": "Add New Goal", "current": "Current Goals List"},
    "Español": {"hunt": "📝 Data Hunt", "dash": "👩‍🏫 Panel", "pass": "Contraseña", "save": "Actualizar", "del": "Eliminar", "add": "Nueva Meta", "current": "Lista de Metas"}
}
T = texts[st.session_state.lang]

st.sidebar.divider()
password = st.sidebar.text_input(T["pass"], type="password")
is_teacher = (password == "1234")
mode = st.sidebar.radio("导航", [T["hunt"], T["dash"]])

# --- 模式 1: 数据采集 (Data Hunt) ---
if mode == T["hunt"]:
    st.title("🎯 ProTracker")
    # (此处保留之前的 10 格 Trial 逻辑，为节省篇幅略过，请在 GitHub 替换时确保完整)
    # ... 之前的 Data Hunt 代码 ...

# --- 模式 2: 教师后台 (全能编辑页面) ---
elif mode == T["dash"]:
    if not is_teacher:
        st.warning("请输入管理员密码。")
    else:
        st.title(T["dash"])
        tab_struct, tab_goals = st.tabs(["📂 结构管理", "🎯 目标编辑"])
        
        with tab_struct:
            # 班级/学生添加逻辑
            col_a, col_b = st.columns(2)
            with col_a:
                nc = st.text_input("新建班级名称")
                if st.button("创建班级") and nc: st.session_state.db[nc] = {}; st.rerun()
            with col_b:
                if st.session_state.db:
                    tc = st.selectbox("分配至班级", list(st.session_state.db.keys()))
                    fn = st.text_input("学生全名 (将转为首字母)")
                    av = st.selectbox("卡通头像", list(avatars.keys()))
                    if st.button("添加学生") and fn:
                        pn = get_privacy_name(fn)
                        st.session_state.db[tc][pn] = {"avatar": avatars[av], "Goals": {}}
                        st.rerun()

        with tab_goals:
            if st.session_state.db:
                c1, c2 = st.columns(2)
                with c1: ec = st.selectbox("选择班级", list(st.session_state.db.keys()), key="ec")
                with c2: 
                    s_list = list(st.session_state.db[ec].keys())
                    es = st.selectbox("选择学生", s_list, key="es") if s_list else None
                
                if es:
                    st.divider()
                    st.subheader(f"{st.session_state.db[ec][es]['avatar']} {es} 的目标管理")
                    
                    # 1. 顶部：添加新目标项
                    with st.expander(T["add"], expanded=True):
                        c_add1, c_add2, c_add3 = st.columns([3, 1, 1])
                        new_g_title = c_add1.text_input("输入新目标标题 (例如: Reading Comprehension)")
                        new_b = c_add2.number_input("基准线 %", 0, 100, 0, key="new_b")
                        new_t = c_add3.number_input("目标值 %", 0, 100, 80, key="new_t")
                        if st.button("确认添加此目标"):
                            if new_g_title:
                                st.session_state.db[ec][es]["Goals"][new_g_title] = {"baseline": new_b, "target": new_t}
                                st.success("已添加！")
                                st.rerun()

                    st.markdown(f"#### {T['current']}")
                    
                    # 2. 下方：所有 Goal 的呈现与修改项
                    current_goals = st.session_state.db[ec][es]["Goals"]
                    if not current_goals:
                        st.info("该学生目前没有目标。")
                    else:
                        for g_name, g_info in list(current_goals.items()):
                            # 使用 container 和 divider 模拟卡片感
                            with st.container():
                                col_edit1, col_edit2, col_edit3, col_edit4 = st.columns([3, 1, 1, 1])
                                
                                # 显示并允许修改目标名称、基准和目标
                                # 注意：如果需要修改名字，通常建议删除再加，这里先提供数值修改
                                col_edit1.markdown(f"**目标：{g_name}**")
                                edit_b = col_edit2.number_input("基准 %", 0, 100, int(g_info['baseline']), key=f"eb_{g_name}")
                                edit_t = col_edit3.number_input("目标 %", 0, 100, int(g_info['target']), key=f"et_{g_name}")
                                
                                # 修改项：更新和删除按钮
                                if col_edit4.button(T["save"], key=f"sv_{g_name}"):
                                    st.session_state.db[ec][es]["Goals"][g_name] = {"baseline": edit_b, "target": edit_t}
                                    st.success("已更新")
                                    st.rerun()
                                
                                if col_edit4.button(T["del"], key=f"dl_{g_name}"):
                                    del st.session_state.db[ec][es]["Goals"][g_name]
                                    st.rerun()
                                st.divider()
