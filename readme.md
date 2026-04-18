# 🎓 Student Placement Peer Analyzer

An interactive, data-driven web application designed to evaluate a student's employability and dynamically rank them against a realistic college batch. Built as a responsive dashboard, this tool simulates real-world hiring algorithms by weighting academic and technical skills while applying strict mathematical penalties for active backlogs.

## 🚀 Project Overview
Unlike static calculators, this application acts as a complete **Cohort Analysis Tool**. It uses synthetic data generation to create a batch of 100 realistic student profiles. Users can search for their profile, conduct "What-If" analyses by modifying their stats, and permanently save changes to see how their batch rank shifts in real-time on the live leaderboard.

## ✨ Key Features
* **Dynamic 'What-If' Simulator:** Users can tweak their CGPA, project count, internships, and programming scores to instantly see how future improvements will affect their placement probability.
* **Live Batch Ranking:** Automatically recalculates class averages and re-sorts the 100-student leaderboard the moment a user updates their profile.
* **Persistent Session State:** Utilizes Streamlit's memory vault to ensure that user modifications permanently update the live dataset during the active session.
* **Realistic Hiring Logic:** Implements an industry-aligned mathematical formula that positively weights technical skills and projects, while strictly applying a negative penalty feature for active academic backlogs.

## 🛠️ Technical Stack
This project demonstrates a complete Python data science pipeline:
* **NumPy:** Utilized `np.random` distributions (uniform, randint, choice) to generate a realistic, probabilistically accurate synthetic dataset of 100 students. Used for highly efficient vectorized math operations.
* **Pandas:** Handles the core data structuring. Utilized for extracting specific rows (`iloc`), updating values, dynamically sorting the leaderboard (`sort_values`), and managing the batch dataset.
* **Streamlit:** Powers the frontend UI. Utilizes advanced features like `st.session_state` for database memory and `st.dataframe` for clean tabular data visualization.

## ⚙️ Installation & Setup

**1. Clone the repository**
```bash
git clone [https://github.com/your-username/placement-peer-analyzer.git](https://github.com/your-username/placement-peer-analyzer.git)
cd placement-peer-analyzer