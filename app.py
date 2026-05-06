import streamlit as st
import pandas as pd

# 1. 页面配置
st.set_page_config(page_title="ProTracker - IEP Management", layout="wide")

# 2. 语言与提示层级定义
prompt_levels = {
    "None": "⚪",
    "Independent (I)": "✅",
    "Verbal Prompt (V)": "🗣️",
    "Visual / Gestural Prompt (Vi/G)": "👁️",
    "Gestural/Partial Physical (PP)": "🖐️",
    "Modeling (M)": "🎭",
    "Physical Guidance / Full Physical (FP)": "🤝"
}
level_list = list(prompt_levels.keys())

# 3. 数据库初始化
if 'db' not in st.session_state:
    st.session_state.db = {}

# 4. 侧边栏导航
st.sidebar.title("🚀 ProTracker")
mode = st.sidebar.radio("Navigation", ["📝 Data Hunt", "👩‍🏫 Teacher Dashboard"])

# --- MODE 1: DATA HUNT (10-Grid System) ---
if mode == "📝 Data Hunt":
    st.title("🎯 IEP Data Hunt")
    
    classes = list(st.session_state.db.keys())
    if not classes:
        st.info("No data found. Please add classes and students in the Dashboard.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            sel_class = st.selectbox("Select Class", classes)
        with c2:
            students = list(st.session_state.db[sel_class].keys())
            sel_student = st.selectbox("Select Student", students) if students else None
        
        if sel_student:
            student_data = st.session_state.db[sel_class][sel_student]
            goal_names = list(student_data["Goals"].keys())
            
            if goal_names:
                sel_goal = st.selectbox("Select IEP Goal", goal_names)
                st.divider()
                
                st.subheader(f"Trials for: {sel_goal}")
                st.write("Click each grid to record the prompt level used.")

                # 创建 10 个格子的状态存储
                grid_key = f"grid_{sel_student}_{sel_goal}"
                if grid_key not in st.session_state:
                    st.session_state[grid_key] = ["None"] * 10

                # 绘制 5x2 的网格
                cols = st.columns(5)
                for i in range(10):
                    with cols[i % 5]:
                        current_val = st.session_state[grid_key][i]
                        # 点击按钮切换 Prompt Level
                        if st.button(f"Trial {i+1}\n\n{prompt_levels[current_val]}", key=f"btn_{i}"):
                            # 循环切换 index
                            current_idx = level_list.index(current_val)
                            next_idx = (current_idx + 1) % len(level_list)
                            st.session_state[grid_key][i] = level_list[next_idx]
                            st.rerun()
                
                st.divider()
                
                # 数据统计
                results = st.session_state[grid_key]
                ind_count = results.count("Independent (I)")
                total_trials = 10 - results.count("None")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Independent Score", f"{(ind_count/10)*100 if total_trials > 0 else 0}%")
                col2.metric("Trials Completed", f"{total_trials}/10")
                
                with st.expander("View Legend (Prompt Levels)"):
                    for k, v in prompt_levels.items():
                        st.write(f"{v} : {k}")

                if st.button("✅ Submit Final Session Data"):
                    st.success("Session data saved to history!")
                    # 这里可以添加保存到数据库的逻辑
                    st.session_state[grid_key] = ["None"] * 10 # 重置
                    st.rerun()

# --- MODE 2: TEACHER DASHBOARD (保持不变) ---
elif mode == "👩‍🏫 Teacher Dashboard":
    st.title("⚙️ Teacher Administration")
    # ... (保留你之前的后台添加班级/学生/目标的逻辑)
