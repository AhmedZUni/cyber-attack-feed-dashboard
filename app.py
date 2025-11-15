import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# ---- LIVE DATA SOURCE: Google Sheet (CSV) ----
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQrv8gnjuOaENz6YYG2VQUo5ULubTVRpYKCe9TsgqvPYYt2bnbbmJo2J7ZhBN5oKpSVrJIc9HYh48_o/pub?output=csv"

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Basic normalization/cleaning
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')
        if 'estimated_cost' in df.columns:
            df['estimated_cost'] = pd.to_numeric(df['estimated_cost'], errors='coerce').fillna(0)
        # Ensure all expected columns exist for dashboard
        cols_needed = ['date','attack_method','impact_target','attacker_group','estimated_cost','remediation']
        for col in cols_needed:
            if col not in df.columns:
                df[col] = ""
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=['date','attack_method','impact_target','attacker_group','estimated_cost','remediation'])

df = get_data()

# ---- PAGE DESIGN ----
st.set_page_config(page_title="Cyber Attack Feed Dashboard", layout="wide")
st.markdown("<h1 style='color:#ff5858;'>🚨 Cyber Attack Feed Dashboard 🚨</h1>", unsafe_allow_html=True)
st.markdown("> _Live cyber incident dashboard: trending attacks, impacted targets, losses, and more (auto updates)._")

# ---- SIDEBAR FILTERS ----
with st.sidebar:
    st.header("Filters")
    method_list = list(df['attack_method'].dropna().unique())
    picked_method = st.multiselect("Attack Method", options=method_list)
    target_list = list(df['impact_target'].dropna().unique())
    picked_target = st.text_input("Target Name (partial match ok)")
    if not df.empty and df['date'].notna().any():
        date_min = pd.to_datetime(df['date'], errors='coerce').min().date()
        date_max = pd.to_datetime(df['date'], errors='coerce').max().date()
        picked_date = st.date_input("Attack Date", value=None, min_value=date_min, max_value=date_max)
    else:
        picked_date = None

mask = pd.Series(True, index=df.index)
if picked_method:
    mask &= df['attack_method'].isin(picked_method)
if picked_target:
    mask &= df['impact_target'].str.contains(picked_target, case=False)
if picked_date:
    mask &= df['date'] == picked_date.strftime("%Y-%m-%d")

filtered = df[mask].copy() if mask.any() else df.copy()

# ---- DASHBOARD TOP METRICS ----
col1, col2, col3 = st.columns(3)
col1.metric("Total Attacks", f"{filtered.shape[0]}")
top_attack = filtered['attack_method'].mode()[0] if not filtered.empty else "N/A"
col2.metric("Top Method", f"{top_attack}")
col3.metric("Estimated Total Loss", f"${filtered['estimated_cost'].sum():,}")

# ---- BAR CHART: ATTACKS BY METHOD ----
st.subheader("🦠 Attack Methods Frequency")
by_method = filtered.groupby('attack_method').size().reset_index(name='Count')
if not by_method.empty:
    fig1 = px.bar(
        by_method,
        x='attack_method', y='Count',
        color='attack_method',
        title='Attacks per Method',
        template='plotly_dark'
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("No data for chart.")

# ---- PIE CHART: ATTACK METHOD DISTRIBUTION ----
st.subheader("📊 Attack Method Share (by Financial Impact)")
if not filtered.empty and filtered['estimated_cost'].sum() > 0:
    fig2 = px.pie(
        filtered,
        names='attack_method',
        values='estimated_cost',
        title='Attack Method Proportion (by losses)',
        template='plotly_dark'
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No data for pie chart.")

# ---- BAR CHART: TOTAL LOSS BY METHOD ----
st.subheader("💸 Estimated Loss by Attack Method")
loss_by_method = filtered.groupby('attack_method')['estimated_cost'].sum().reset_index()
if not loss_by_method.empty:
    fig3 = px.bar(
        loss_by_method,
        x='attack_method', y='estimated_cost',
        color='attack_method',
        title='Total Estimated Loss per Method',
        template='plotly_dark'
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No data for loss chart.")

# ---- TOP LOSSES TABLE ----
st.subheader("⚠️ Highest Impacted Targets")
top_losses = filtered.sort_values(by='estimated_cost', ascending=False)[
    ['date','impact_target','attack_method','attacker_group','estimated_cost','remediation']
].reset_index(drop=True)
try:
    st.dataframe(
        top_losses.style.background_gradient(subset=['estimated_cost'], cmap='autumn'),
        height=300
    )
except Exception:
    st.dataframe(top_losses, height=300)

# ---- SEARCH ACROSS TABLE ----
st.subheader("🔍 Quick Search")
search_text = st.text_input("Search for anything (target, attacker, remediation...):")
if search_text.strip():
    st.write("Search results:")
    mask2 = filtered.apply(lambda row: search_text.lower() in str(row).lower(), axis=1)
    st.dataframe(filtered[mask2])

st.caption("© 2025 Cyber Attack Feed Dashboard | Made with Streamlit")

