
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(
    page_title="MindEase: Wellness Tracker",
    page_icon="💆",
    layout="wide"
)

st.title("💆 MindEase: Wellness Tracker")
st.markdown(
    "Track your wellness, screen-free time, and healthy habits with this simple and intuitive app. 🌿"
)

EXCEL_FILENAME = "mental_wellness_log_20250704_172222.xlsx"
FREQ_OPTIONS = ["Daily", "2-3 times/week", "Once a week", "Rarely"]

def check_status(minutes):
    return "Healthy" if minutes >= 60 else "Needs Improvement"

def get_status_color(status):
    return "green" if status == "Healthy" else "red"

if "records" not in st.session_state:
    if os.path.exists(EXCEL_FILENAME):
        st.session_state.records = pd.read_excel(EXCEL_FILENAME)
    else:
        st.session_state.records = pd.DataFrame(columns=[
            "Timestamp", "Name", "Wellness Activity", "Me-Time Activity",
            "Offline Time (min)", "Frequency", "Status"
        ])

st.sidebar.header("Navigation")
menu = st.sidebar.radio("Choose View", ["➕ Add Entry", "📊 Activity Overview", "📁 Export Data", "🗑️ Clear Entries", "ℹ️ About App"])

if menu == "➕ Add Entry":
    st.subheader("➕ Log a New Wellness Entry")

    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Student Name")
            wellness = st.text_input("🧘 Wellness Task")
            frequency = st.selectbox("📅 Frequency", FREQ_OPTIONS)
        with col2:
            metime = st.text_input("🎨 Relaxing Activity")
            screen_time = st.number_input("📵 Offline Time (in minutes)", min_value=0, step=1)

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
                st.success(f"✅ Entry added! Status: **{status}**")
            else:
                st.error("❌ Please fill all fields before submitting.")

elif menu == "📊 Activity Overview":
    st.subheader("📊 Wellness Activity Summary")
    df = st.session_state.records

    if df.empty:
        st.warning("No entries yet. Add some data from 'Add Entry'.")
    else:
        total_entries = len(df)
        healthy_days = df[df["Status"] == "Healthy"].shape[0]
        total_minutes = df["Offline Time (min)"].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("📋 Total Entries", total_entries)
        col2.metric("💚 Healthy Days", healthy_days)
        col3.metric("🕒 Total Offline Time (min)", total_minutes)

        st.markdown("---")
        st.markdown("### 🧾 All Logged Entries")
        st.dataframe(df, use_container_width=True)

elif menu == "📁 Export Data":
    st.subheader("📁 Export Entries to Excel")
    df = st.session_state.records

    export_filename = "mental_wellness_log_20250704_172222.xlsx"

    if df.empty:
        st.warning("⚠️ No entries to export.")
    else:
        try:
            if os.path.exists(export_filename):
                existing = pd.read_excel(export_filename)
                combined = pd.concat([existing, df], ignore_index=True)
                combined.drop_duplicates(inplace=True)
                combined.to_excel(export_filename, index=False)
            else:
                df.to_excel(export_filename, index=False)
            st.success(f"✅ Data exported to `{export_filename}`.")
        except Exception as e:
            st.error(f"❌ Failed to export data: {e}")

elif menu == "🗑️ Clear Entries":
    st.subheader("⚠️ Clear All Entries")
    if st.button("Clear All Data Now"):
        st.session_state.records = pd.DataFrame(columns=[
            "Timestamp", "Name", "Wellness Activity", "Me-Time Activity",
            "Offline Time (min)", "Frequency", "Status"
        ])
        if os.path.exists(EXCEL_FILENAME):
            os.remove(EXCEL_FILENAME)
        st.success("🗑️ All entries have been cleared.")

elif menu == "ℹ️ About App":
    st.subheader("ℹ️ About MindEase")
    st.markdown("""
**MindEase** is designed to help students and individuals log their mental wellness and screen-free habits.

**Features:**
- ✍️ Easy-to-use form for input
- 💡 Automatic wellness evaluation
- 📊 Summarized activity overview
- 📁 Data export to Excel
- 🧹 Clear history with one click

Built using **Python**, **Streamlit**, and **Pandas**.
""")
