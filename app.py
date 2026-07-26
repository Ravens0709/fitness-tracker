import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Fitness & Weight Tracker", page_icon="💪")
st.title("💪 Fitness & Progress Tracker")

DATA_FILE = "fitness_data.csv"

# Load existing data or create template
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Weight (kg)", "Calories (kcal)", "Workout Done", "Notes"])

# Sidebar Form
st.sidebar.header("📝 Log Daily Entry")
date = st.sidebar.date_input("Date", datetime.date.today())
weight = st.sidebar.number_input("Weight (kg)", min_value=30.0, max_value=150.0, value=60.0, step=0.5)
calories = st.sidebar.number_input("Calories Consumed (kcal)", min_value=1000, max_value=6000, value=2500, step=50)
workout = st.sidebar.selectbox("Workout Done?", ["Yes", "No", "Rest Day"])
notes = st.sidebar.text_input("Notes", "e.g., Push day, felt strong")

if st.sidebar.button("Save Entry"):
    new_data = pd.DataFrame([[str(date), weight, calories, workout, notes]], columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True).drop_duplicates(subset=["Date"], keep="last")
    df.to_csv(DATA_FILE, index=False)
    st.sidebar.success("Logged successfully! 🎉")

# Display Dashboard
st.subheader("📊 Your Progress Dashboard")

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Latest Weight", f"{df['Weight (kg)'].iloc[-1]} kg")
    with col2:
        st.metric("Latest Calories", f"{df['Calories (kcal)'].iloc[-1]} kcal")

    st.line_chart(df.set_index("Date")[["Weight (kg)"]])
    st.bar_chart(df.set_index("Date")[["Calories (kcal)"]])

    st.subheader("📋 History Log")
    st.dataframe(df, use_container_width=True)
else:
    st.info("No logs added yet. Use the sidebar to enter your first record!")
