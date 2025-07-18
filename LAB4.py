import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page setup
st.set_page_config(
    page_title="MindEase: Wellness Tracker",
    layout="wide"
)

st.title("MindEase: Wellness Tracker")
st.markdown("Track your wellness, screen-free time, and healthy habits with this simple and intuitive app.")

# Constants
EXCEL_FILENAME = "mental_wellness_log.xlsx"
FREQ_OPTIONS = ["Daily", "2-3 times/week", "Once a week", "Rarely"]

# Utility functions
def check_status(minutes):
    return "Healthy" if minutes >= 60 else "Needs Improvement"

# Initialize session state
if "records" not in st.session_state:
    if os.path.exists(EXCEL_FILENAME):
        st.session_state.records = pd.read_excel(EXCEL_FILENAME)
    else:
        st.session_state.records = pd.DataFrame(columns=[
            "Timestamp", "Name", "Wellness Activity", "Me-Time Activity",
            "Offline Time (min)", "Frequency", "Status"
        ])

# Sidebar navigation
st.sidebar.header("Navigation")
menu = st.sidebar.radio("Choose View", [
    "Add Entry",
    "Activity Overview",
    "Export Data",
    "Clear Entries",
    "About App"
])

# Add new entry
if menu == "Add Entry":
    st.subheader("Log a New Wellness Entry")

    with st.form("entry_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Student Name")
            wellness = st.text_input("Wellness Task")
            frequency = st.selectbox("Frequency", FREQ_OPTIONS)

        with col2:
            metime = st.text_input("Relaxing Activity")
            screen_time = st.number_input("Offline Time (in minutes)", min_value=0, step=1)

        submitted = st.form_submit_button("Add Entry")

        if submitted:
            if name and wellness and metime:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                status = check_status(screen_time)
                new_entry = pd.DataFrame([{
                    "Timestamp": timestamp,
                    "Name": name,
                    "Wellness Activity": wellness,
                    "Me-Time Activity": metime,
                    "Offline Time (min)": screen_time,
                    "Frequency": frequency,
                    "Status": status
                }])
                st.session_state.records = pd.concat([st.session_state.records, new_entry], ignore_index=True)
                st.success(f"Entry added! Status: {status}")
            else:
                st.error("Please fill all fields before submitting.")

# Overview page
elif menu == "Activity Overview":
    st.subheader("Wellness Activity Summary")
    df = st.session_state.records

    if df.empty:
        st.warning("No entries yet. Please add some data first.")
    else:
        total_entries = len(df)
        healthy_days = df[df["Status"] == "Healthy"].shape[0]
        total_minutes = df["Offline Time (min)"].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Entries", total_entries)
        col2.metric("Healthy Days", healthy_days)
        col3.metric("Total Offline Time (min)", total_minutes)

        st.markdown("---")
        st.markdown("### All Logged Entries")
        st.dataframe(df, use_container_width=True)

# Export data
elif menu == "Export Data":
    st.subheader("Export Entries to Excel")
    df = st.session_state.records

    if df.empty:
        st.warning("No entries to export.")
    else:
        try:
            if os.path.exists(EXCEL_FILENAME):
                existing = pd.read_excel(EXCEL_FILENAME)
                combined = pd.concat([existing, df], ignore_index=True)
                combined.drop_duplicates(inplace=True)
                combined.to_excel(EXCEL_FILENAME, index=False)
            else:
                df.to_excel(EXCEL_FILENAME, index=False)
            st.success(f"Data exported successfully to {EXCEL_FILENAME}.")
        except Exception as e:
            st.error(f"Failed to export data: {e}")

# Clear data
elif menu == "Clear Entries":
    st.subheader("Clear All Entries")
    if st.button("Clear All Data Now"):
        st.session_state.records = pd.DataFrame(columns=[
            "Timestamp", "Name", "Wellness Activity", "Me-Time Activity",
            "Offline Time (min)", "Frequency", "Status"
        ])
        if os.path.exists(EXCEL_FILENAME):
            os.remove(EXCEL_FILENAME)
        st.success("All entries have been cleared.")

# About section
elif menu == "About App":
    st.subheader("About MindEase")
    st.markdown("""
MindEase is a simple app that helps users log their wellness and screen-free time habits.

**Features:**
- Simple form to log daily activities
- Wellness status based on screen-free time
- Summary of entries and trends
- Data export to Excel
- One-click clear option for data reset

Built using Python, Streamlit, and Pandas.
""")
