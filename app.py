import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Peer Analyzer", layout="wide")
st.title("📊 Student Placement Peer Analyzer")
st.markdown("Search your profile, update your stats, and save them to the live dataset.")

# --- 1. NUMPY: GENERATE THE DATASET ---
@st.cache_data
def load_generated_data():
    np.random.seed(42)
    num_students = 100
    
    roll_numbers = [f"BTECH{str(i).zfill(3)}" for i in range(1, num_students + 1)]
    cgpa = np.random.uniform(5.5, 9.8, num_students).round(2)
    projects = np.random.randint(0, 6, num_students)
    internships = np.random.randint(0, 4, num_students)
    prog_score = np.random.randint(40, 98, num_students)
    backlogs = np.random.choice([0, 1, 2, 3], num_students, p=[0.7, 0.15, 0.1, 0.05])
    
    df = pd.DataFrame({
        'Roll_No': roll_numbers,
        'Name': [f"Student_{i}" for i in range(1, num_students + 1)],
        'CGPA': cgpa,
        'Projects': projects,
        'Internships': internships,
        'Prog_Score': prog_score,
        'Backlogs': backlogs
    })
    
    # Inject your profile
    df.loc[0, 'Name'] = "Anshika"
    df.loc[0, 'CGPA'] = 7.5
    df.loc[0, 'Projects'] = 2
    df.loc[0, 'Internships'] = 1
    df.loc[0, 'Prog_Score'] = 70
    df.loc[0, 'Backlogs'] = 0
    
    return df

# --- 2. SESSION STATE (THE MEMORY VAULT) ---
# Check if the dataset is already in memory. If not, load it and save it.
if 'live_dataset' not in st.session_state:
    st.session_state.live_dataset = load_generated_data()

# Read the current dataset from memory
df = st.session_state.live_dataset

# --- VECTORIZED MATH ---
weights = {'CGPA': 0.4, 'Proj': 0.3, 'Int': 0.2, 'Prog': 0.1, 'Backlog': 0.5}

def calculate_base_score(dataframe):
    score = (
        (dataframe['CGPA'] * weights['CGPA']) +
        (dataframe['Projects'] * weights['Proj']) +
        (dataframe['Internships'] * weights['Int']) +
        ((dataframe['Prog_Score'] / 10) * weights['Prog']) -
        (dataframe['Backlogs'] * weights['Backlog'])
    )
    return np.maximum(0, score).round(2)

df['Base_Score'] = calculate_base_score(df)

# --- 3. SEARCH YOUR PROFILE ---
st.divider()
st.subheader("🔍 Find Your Profile")

search_name = st.selectbox("Search by Name:", df['Name'].tolist())
my_data = df[df['Name'] == search_name].iloc[0]

# --- 4. MODIFY YOUR DETAILS ---
st.subheader("✏️ Update Your Stats (What-If Analysis)")

col1, col2 = st.columns(2)
with col1:
    new_cgpa = st.number_input("CGPA", 0.0, 10.0, float(my_data['CGPA']), step=0.1)
    new_proj = st.number_input("Projects", 0, 10, int(my_data['Projects']))
    new_backlogs = st.number_input("Active Backlogs", 0, 5, int(my_data['Backlogs']))
with col2:
    new_int = st.number_input("Internships", 0, 5, int(my_data['Internships']))
    new_prog = st.slider("Programming Score", 0, 100, int(my_data['Prog_Score']))

# --- NEW: SAVE BUTTON ---
# This button takes your inputs and permanently overwrites your row in the dataset
if st.button("💾 Save Changes to Dataset"):
    # Locate the row index of the searched name
    row_idx = st.session_state.live_dataset.index[st.session_state.live_dataset['Name'] == search_name].tolist()[0]
    
    # Update the values in the memory vault
    st.session_state.live_dataset.at[row_idx, 'CGPA'] = new_cgpa
    st.session_state.live_dataset.at[row_idx, 'Projects'] = new_proj
    st.session_state.live_dataset.at[row_idx, 'Internships'] = new_int
    st.session_state.live_dataset.at[row_idx, 'Prog_Score'] = new_prog
    st.session_state.live_dataset.at[row_idx, 'Backlogs'] = new_backlogs
    
    st.success("✅ Dataset successfully updated!")
    # Instantly refresh the page to show the new data everywhere
    st.rerun()

# --- 5. RECALCULATE & RANK ---
my_new_score = (
    (new_cgpa * weights['CGPA']) +
    (new_proj * weights['Proj']) +
    (new_int * weights['Int']) +
    ((new_prog / 10) * weights['Prog']) -
    (new_backlogs * weights['Backlog'])
)
my_new_score = max(0, round(my_new_score, 2))

st.divider()
st.subheader("🏆 Batch Analysis: Where Do You Stand?")

df_updated = df.copy()
df_updated.loc[df_updated['Name'] == search_name, 'Base_Score'] = my_new_score
df_updated = df_updated.sort_values(by='Base_Score', ascending=False).reset_index(drop=True)

my_rank = df_updated[df_updated['Name'] == search_name].index[0] + 1
batch_avg = np.mean(df_updated['Base_Score']).round(2)

colA, colB, colC = st.columns(3)
colA.metric("Your Score", f"{my_new_score} / 10", f"{round(my_new_score - my_data['Base_Score'], 2)} vs original")
colB.metric("Batch Rank", f"#{my_rank} out of 100")
colC.metric("Batch Average", f"{batch_avg} / 10")

# Show Leaderboard
st.write("**Live Batch Leaderboard:**")
st.dataframe(df_updated[['Roll_No', 'Name', 'CGPA', 'Projects', 'Internships', 'Prog_Score', 'Backlogs', 'Base_Score']].head(10), use_container_width=True)