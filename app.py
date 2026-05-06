import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 设置页面标题
st.set_page_config(page_title="ProTracker - IEP Progress", layout="wide")

# 2. 简易登录逻辑 (在侧边栏)
st.sidebar.title("🔐 教师管理后台")
password = st.sidebar.text_input("请输入管理密码", type="password")

# 预设密码 (你可以自己修改这个字符串)
ADMIN_PASSWORD = "123" 

# 3. 初始化模拟数据 (如果想要永久保存，以后我们需要接 Google Sheets)
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        'Date': pd.to_datetime(['2026-05-01', '2026-05-02', '2026-05-03']),
        'Reading': [70, 75, 80],
        'Social': [50, 60, 55]
    })

st.title("🎯 ProTracker: 学生进度跟踪")

# --- 模式 A: 老师管理模式 ---
if password == ADMIN_PASSWORD:
    st.sidebar.success("已进入管理模式")
    st.header("📝 输入新数据")
    
    with st.form("data_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            new_date = st.date_input("选择日期")
        with col2:
            new_reading = st.slider("阅读理解准确率 (%)", 0, 100, 80)
        with col3:
            new_social = st.slider("社交技巧得分", 0, 100, 60)
            
        submitted = st.form_submit_button("提交数据")
        if submitted:
            new_row = {'Date': pd.to_datetime(new_date), 'Reading': new_reading, 'Social': new_social}
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
            st.success("数据已更新！")

# --- 模式 B: 数据展示模式 (所有人可见) ---
st.header("📊 进度可视化")
tab1, tab2 = st.tabs(["阅读理解", "社交技巧"])

with tab1:
    fig_read = px.line(st.session_state.data, x='Date', y='Reading', title="Reading Goal Progress", markers=True)
    st.plotly_chart(fig_read, use_container_width=True)

with tab2:
    fig_social = px.line(st.session_state.data, x='Date', y='Social', title="Social Skills Progress", markers=True)
    st.plotly_chart(fig_social, use_container_width=True)
