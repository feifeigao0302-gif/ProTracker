# ProTracker
(Special Education) IEP Data Collection & Analysis Tool
## Project Vision
ProTracker is designed to leverage business analytics to transform complex Special Education data into actionable insights, aiming to:
- Streamline the tracking process for Individualized Education Program (IEP) goals.
- Utilize data-driven decision-making to optimize instructional interventions.
- Reduce administrative burden for special education teachers, enhancing teaching efficiency.
## Core Features
- **IEP Goal Management**: Quantify abstract teaching goals into measurable metrics.
- **Progress Trend Analysis**: Visualize student progress trajectories through dynamic charts.
- **Automated Data Collection**: Simplify daily data entry workflows.
-## 🚀 Core Features & Workflow

ProTracker is designed with a **3-tier navigation logic** to minimize cognitive load and maximize classroom efficiency:

1. **Dashboard (L1) - Student Overview**: 
   - Provides an at-a-glance summary of all student profiles.
   - Highlighting data-collection status and urgent alerts (e.g., goals with missing data).

2. **Goal Management (L2) - IEP Tracking**: 
   - Displays a comprehensive list of Individualized Education Program (IEP) goals for the selected student.
   - Categorizes goals by domain (Academic, Social, Behavioral) for quick access.

3. **Action Hub (L3) - Data Interaction**:
   - **Data Hunt**: A "zero-typing" entry interface optimized for rapid, real-time data collection in busy classroom environments.
   - **Data Analyst**: Instant visualization of student progress. It transforms raw data into trend lines and achievement curves using Python-based analytics to support data-driven instruction.
   - ### 🚀 系统工作流 (Workflow Logic)

| 级别 | 模块名称 | 设计目的 (Purpose) |
| :--- | :--- | :--- |
| **L1** | **Dashboard** | **快速索引**：概览所有学生信息及数据采集提醒（Urgent Alerts）。 |
| **L2** | **Goal Management** | **目标管理**：展示选定学生的所有 IEP 目标列表，支持分类查看。 |
| **L3** | **Action Hub** | **核心中心**：在 **Data Hunt**（数据录入）与 **Analyst**（数据可视化）间切换。 |
## Tech Stack
- **Frontend**: Streamlit / Flask (Planned for rapid prototyping)
- **Data Management**: SQL (SQLite for local storage, PostgreSQL for cloud)
- **Analytics**: Python (Pandas, NumPy for data processing)
- **Visualization**: Plotly (In-app) / Tableau (Strategic reporting)
## Business Analytics Goals
- Improve the precision and efficacy of special education interventions.
- Provide a clear ROI (Return on Investment) model for pedagogical management.
*Created by Feifei Gao - Master of Science in Business Analytics Student*
