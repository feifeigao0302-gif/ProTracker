import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# --- SETTINGS & CONFIG ---
st.set_page_config(page_title="ProTracker", layout="centered")

# --- INITIALIZATION ---
# Initialize session state for navigation and security
if 'level' not in st.session_state:
    st.session_state.level = 'L1'
if 'selected_student' not in st.session_state:
    st.session_state.selected_student = None
if 'selected_goal' not in st.session_state:
    st.session_state.selected_goal = None
if 'auth_passed' not in st.session_state:
    st.session_state.auth_passed = False

# Mock Data (In production, replace with SQL queries)
students = ["Student A", "Student B", "Student C"]
goals_db = {
    "Student A": ["Reading Comprehension", "Social Skills: Turn Taking", "On-Task Behavior"],
    "Student B": ["Math: Addition", "Self-Regulation"],
    "Student C": ["Handwriting", "Following Directions"]
}

# --- NAVIGATION LOGIC ---
def nav_to(level, student=None, goal=None):
    st.session_state.level = level
    if student: st.session_state.selected_student = student
    if goal: st.session_state.selected_goal = goal
    # Reset security when moving away from Analyst
    if level != 'L3':
        st.session_state.auth_passed = False

# --- UI LAYOUT ---

# LEVEL 1: DASHBOARD
if st.session_state.level == 'L1':
    st.title("🏫 ProTracker Dashboard")
    st.subheader("Student Overview")
    st.write("Quick access to student profiles and data status.")
    
    for student in students:
        with st.container():
            col1, col2 = st.columns([3, 1])
            col1.info(f"👤 **{student}**")
            if col2.button(f"View Goals", key=f"btn_{student}"):
                nav_to('L2', student=student)

# LEVEL 2: GOAL MANAGEMENT
elif st.session_state.level == 'L2':
    st.title(f"🎯 {st.session_state.selected_student}'s Goals")
    if st.button("⬅ Back to Dashboard"):
        nav_to('L1')
    
    st.divider()
    st.write("Select a specific goal to record data or view progress:")
    
    current_goals = goals_db.get(st.session_state.selected_student, [])
    for goal in current_goals:
        if st.button(goal, use_container_width=True, key=f"goal_{goal}"):
            nav_to('L3', goal=goal)

# LEVEL 3: ACTION HUB (Data Hunt & Analyst)
elif st.session_state.level == 'L3':
    st.title("⚡ Action Hub")
    st.caption(f"Current Target: {st.session_state.selected_goal} | Student: {st.session_state.selected_student}")
    
    if st.button("⬅ Back to Goals"):
        nav_to('L2', student=st.session_state.selected_student)

    # Creating Tabs for different roles
    tab1, tab2 = st.tabs(["🎯 Data Hunt (Public)", "📈 Data Analyst (Restricted)"])

    # --- TAB 1: DATA HUNT ---
    with tab1:
        st.subheader("Quick Data Collection")
        st.write("Tap to record today's achievement level (0-100%).")
        
        # Zero-typing Buttons
        cols = st.columns(5)
        scores = [20, 40, 60, 80, 100]
        for idx, score in enumerate(scores):
            if cols[idx].button(f"{score}%"):
                st.success(f"Successfully recorded {score}% for {st.session_state.selected_goal}!")
                # Add SQL Save Logic Here
        
        st.text_area("Observations / Notes (Optional)", placeholder="Enter classroom notes here...")

    # --- TAB 2: DATA ANALYST ---
    with tab2:
        st.subheader("Progress Analytics")
        
        if not st.session_state.auth_passed:
            st.warning("🔒 This section is restricted to Lead Teachers.")
            pin = st.text_input("Enter 4-digit PIN to unlock", type="password")
            if pin == "1234": # <--- You can change your password here
                st.session_state.auth_passed = True
                st.rerun()
            elif pin != "":
                st.error("Invalid PIN. Access Denied.")
        
        else:
            st.success("✅ Teacher Access Granted")
            if st.button("Logout/Lock"):
                st.session_state.auth_passed = False
                st.rerun()
            
            # Analytics Visualization
            st.divider()
            # Mock Data for Chart
            chart_data = pd.DataFrame({
                'Date': pd.date_range(start='2026-05-01', periods=5),
                'Success_Rate': [25, 45, 40, 65, 80],
                'Baseline': [50] * 5
            })
            
            fig = px.line(chart_data, x='Date', y='Success_Rate', title="Achievement Trend")
            fig.add_scatter(x=chart_data['Date'], y=chart_data['Baseline'], name="IEP Goal Line", line=dict(color='red', dash='dash'))
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("**Insight:** Student is showing a positive upward trend and has exceeded the baseline in the last 2 sessions.")
