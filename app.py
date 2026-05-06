import streamlit as st
import pandas as pd

# 1. 页面配置
st.set_page_config(page_title="ProTracker - IEP Management", layout="wide")

# 辅助函数：生成隐私姓名（首字母）
def get_privacy_name(name):
    parts = name.split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[-1][0]}".upper() # First and Last initial
    return name[:2].upper() # First two letters if only one name

# 卡通头像库
avatars = {
    "Robot": "🤖", "Panda": "🐼", "Tiger": "🐯", "Fox": "🦊", 
    "Koala": "🐨", "Frog": "🐸", "Unicorn": "🦄", "Dragon": "🐲",
    "Wizard": "🧙", "Rocket": "🚀", "Star": "⭐", "Alien": "👽"
}

# 2. 提示层级定义 (极简代码 + 图像图标)
prompt_minimal = {
    "I": "✅ I", 
    "V": "🗣️ V", 
    "Vi/G": "👁️ Vi/G", 
    "PP": "🖐️ PP", 
    "M": "🎭 M", 
    "FP": "🤝 FP"
}

# 3. 数据库初始化
if 'db' not in st.session_state:
    st.session_state.db = {}

# 4. 侧边栏导航
st.sidebar.title("🌐 ProTracker")
mode = st.sidebar.radio("Navigation", ["📝 Data Hunt", "👩‍🏫 Teacher Dashboard"])

# --- MODE 1: DATA HUNT (UI 优化版) ---
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
            student_ids = list(st.session_state.db[sel_class].keys())
            sel_student = st.selectbox("Select Student (ID)", student_ids) if student_ids else None
        
        if sel_student:
            student_data = st.session_state.db[sel_class][sel_student]
            
            # 显示隐私姓名和头像
            st.markdown(f"### {student_data['avatar']} Student: {sel_student}")
            
            goal_names = list(student_data["Goals"].keys())
            
            if goal_names:
                sel_goal = st.selectbox("Select IEP Goal", goal_names)
                st.divider()
                
                # 10 格 Grid 逻辑
                session_key = f"hunt_{sel_student}_{sel_goal}"
                if session_key not in st.session_state:
                    st.session_state[session_key] = ["-"] * 10

                st.write("Record Prompt Levels (use minimal options):")
                
                # 绘制 5x2 的网格
                for row in range(2):
                    cols = st.columns(5)
                    for col in range(5):
                        idx = (row * 5) + col
                        with cols[col]:
                            # 显示格子状态
                            current_val = st.session_state[session_key][idx]
                            
                            # 1. 极简点开选项：st.expander 只包含图标简写
                            with st.expander(f"Trial {idx+1}: **{current_val}**", expanded=False):
                                for code, mini_label in prompt_minimal.items():
                                    if st.button(mini_label, key=f"btn_{idx}_{code}"):
                                        # 保存简写代码
                                        st.session_state[session_key][idx] = code
                                        st.rerun()

                st.divider()
                
                # 实时统计
                results = st.session_state[session_key]
                ind_count = results.count("I")
                total_taken = 10 - results.count("-")
                
                if total_taken > 0:
                    score = (ind_count / 10) * 100
                    st.metric("Independent Score", f"{score}%")
                    if st.button("✅ Submit Final Session Data"):
                        st.success("Session saved!")
                        st.session_state[session_key] = ["-"] * 10
                        st.rerun()
                
                # 2. 下方具体说明 (全局图例)
                with st.expander("❓ View Details - Prompt Level Legend", expanded=True):
                    legend_data = {
                        "✅ I": "Independent (No Prompts)",
                        "🗣️ V": "Verbal Prompt",
                        "👁️ Vi/G": "Visual / Gestural Prompt",
                        "🖐️ PP": "Gestural / Partial Physical",
                        "🎭 M": "Modeling",
                        "🤝 FP": "Physical Guidance / Full Physical"
                    }
                    for mini, detail in legend_data.items():
                        st.write(f"**{mini}** : {detail}")

# --- MODE 2: TEACHER DASHBOARD (保持不变) ---
elif mode == "👩‍🏫 Teacher Dashboard":
    st.title("⚙️ Teacher Administration")
    # ... (保留你之前的后台添加班级/隐私学生/卡通头像/目标的逻辑)
