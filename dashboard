import streamlit as st
import pandas as pd
from datetime import datetime

# Sample data structure for daily cyber attack feed (normally loaded from a database or API)
sample_data = [
    {
        "date": "2025-11-15",
        "attack_method": "Phishing",
        "impact_target": "BankCorp",
        "attacker_group": "Unknown",
        "estimated_cost": "$400K",
        "remediation": "Block sender, reset accounts, train staff"
    },
    {
        "date": "2025-11-15",
        "attack_method": "Ransomware",
        "impact_target": "HealthCare Inc.",
        "attacker_group": "DarkSide",
        "estimated_cost": "$2M",
        "remediation": "Isolate systems, restore backup, notify stakeholders"
    }
    # Add more sample rows or load from your data source!
]

# Convert sample data to DataFrame
df = pd.DataFrame(sample_data)

st.title("Cyber Attack Feed Dashboard")
st.markdown("Daily feed of major cyber attacks worldwide. Search, filter, and view recommended remediation strategies.")

# Filter options
with st.sidebar:
    st.header("Filter Options")
    method = st.multiselect("Attack Method", options=df['attack_method'].unique())
    target = st.text_input("Target Organization (partial name ok)")
    date = st.date_input("Attack Date", value=datetime.today())

# Filtering logic
filtered_df = df.copy()
if method:
    filtered_df = filtered_df[filtered_df['attack_method'].isin(method)]
if target.strip():
    filtered_df = filtered_df[filtered_df['impact_target'].str.contains(target, case=False)]
if date:
    filtered_df = filtered_df[filtered_df['date'] == date.strftime("%Y-%m-%d")]

# Display daily report table
st.subheader("Daily Report")
st.dataframe(filtered_df)

# Search function
search = st.text_input("Quick Search")
if search.strip():
    search_df = filtered_df[
        filtered_df.apply(lambda row: search.lower() in str(row).lower(), axis=1)
    ]
    st.subheader("Search Results")
    st.dataframe(search_df)
