import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# --- Real world cyber attacks data: Oct 20, 2025 onward ---
sampsample_data = [
    # Existing incidents...

    {"date": "2025-10-01", "attack_method": "Social engineering→data breach", "impact_target": "WestJet", "attacker_group": "Unknown", "estimated_cost": 250000, "remediation": "Review access protocols, client notification"},
    {"date": "2025-10-02", "attack_method": "Third-party breach (cloud CRM)", "impact_target": "Allianz Life Insurance", "attacker_group": "Unknown", "estimated_cost": 900000, "remediation": "Vendor controls, security audit"},
    {"date": "2025-10-02", "attack_method": "Ransomware (data theft & extortion)", "impact_target": "Motility Software Solutions", "attacker_group": "PEAR group", "estimated_cost": 450000, "remediation": "Restore backups, law enforcement"},
    {"date": "2025-10-07", "attack_method": "Email Account Compromise", "impact_target": "Williams & Connolly", "attacker_group": "Unknown", "estimated_cost": 90000, "remediation": "Change credentials, enhance email security"},
    {"date": "2025-10-13", "attack_method": "Vulnerability Exploitation (Oracle EBS)", "impact_target": "Harvard University", "attacker_group": "Unknown", "estimated_cost": 130000, "remediation": "Patch Oracle, audit systems"},,
    {
        "date": "2025-10-20",
        "attack_method": "F5 BIG-IP Exploit",
        "impact_target": "Global Enterprises (Financial/Cloud)",
        "attacker_group": "Unknown",
        "estimated_cost": 120000,
        "remediation": "Urgent update of all F5 appliances, threat hunting, CISA guidance"
    },
    {
        "date": "2025-10-20",
        "attack_method": "Credential Compromise",
        "impact_target": "Prosper Marketplace (USA, Fintech)",
        "attacker_group": "Unknown",
        "estimated_cost": 17600000,
        "remediation": "Credential reset, user notification, IAM audit"
    },
    {
        "date": "2025-10-21",
        "attack_method": "SIM Swapping & Account Takeover",
        "impact_target": "Dodo & iPrimus (Australia, Telecom)",
        "attacker_group": "Unknown cyber-criminals",
        "estimated_cost": 85000,
        "remediation": "Notification to affected users, SIM protection steps, forensic investigation"
    },
    {
        "date": "2025-10-21",
        "attack_method": "Cloud Misconfiguration (Data Exposure)",
        "impact_target": "Dukaan (India, eCommerce)",
        "attacker_group": "Unknown",
        "estimated_cost": 5000000,
        "remediation": "Secure cloud streams, review exposure, notify parties"
    },
    {
        "date": "2025-10-23",
        "attack_method": "Data Breach & Leak",
        "impact_target": "Toys “R” Us Canada",
        "attacker_group": "Unknown",
        "estimated_cost": 90000,
        "remediation": "Contact affected clients, digital forensics, legal update"
    },
    {
        "date": "2025-10-27",
        "attack_method": "Alleged Data Leak",
        "impact_target": "GCash (Philippines)",
        "attacker_group": "Dark Web actors",
        "estimated_cost": 150000,
        "remediation": "Enhance endpoint security, customer caution campaign"
    },
    {
        "date": "2025-10-29",
        "attack_method": "Cyber Espionage",
        "impact_target": "Ribbon Communications (USA, Telecom)",
        "attacker_group": "Nation-state APT",
        "estimated_cost": 470000,
        "remediation": "National incident notification, strict access review"
    },
    {
        "date": "2025-11-13",
        "attack_method": "Third-party Cloud Breach",
        "impact_target": "Allianz Life Insurance (USA)",
        "attacker_group": "Unknown (CRM compromise)",
        "estimated_cost": 900000,
        "remediation": "Vendor controls, cloud security audit, affected client contact"
    },
    {
        "date": "2025-11-15",
        "attack_method": "Ransomware",
        "impact_target": "Michigan City, Indiana",
        "attacker_group": "Obscura Ransomware",
        "estimated_cost": 750000,
        "remediation": "Systems separation, backup restoration, law enforcement"
    }
]

df = pd.DataFrame(sample_data)

# --- PAGE DESIGN ---
st.set_page_config(page_title="Cyber Attack Feed Dashboard", layout="wide")
st.markdown("<h1 style='color:#ff5858;'>🚨 Cyber Attack Feed Dashboard 🚨</h1>", unsafe_allow_html=True)
st.markdown("> _Real-world global cyber incidents: trending attacks, impacted targets, losses, and more (from Oct 20, 2025 onwards)._")

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.header("Filters")
    method_list = list(df['attack_method'].unique())
    picked_method = st.multiselect("Attack Method", options=method_list)
    target_list = list(df['impact_target'].unique())
    picked_target = st.text_input("Target Name (partial match ok)")
    date_min = datetime.strptime(df['date'].min(), "%Y-%m-%d").date()
    date_max = datetime.strptime(df['date'].max(), "%Y-%m-%d").date()
    picked_date = st.date_input("Attack Date", value=None, min_value=date_min, max_value=date_max)

mask = pd.Series(True, index=df.index)
if picked_method:
    mask &= df['attack_method'].isin(picked_method)
if picked_target:
    mask &= df['impact_target'].str.contains(picked_target, case=False)
if picked_date:
    mask &= df['date'] == picked_date.strftime("%Y-%m-%d")

filtered = df[mask].copy() if mask.any() else df.copy()

# --- DASHBOARD TOP METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Attacks", f"{filtered.shape[0]}")
top_attack = filtered['attack_method'].mode()[0] if not filtered.empty else "N/A"
col2.metric("Top Method", f"{top_attack}")
col3.metric("Estimated Total Loss", f"${filtered['estimated_cost'].sum():,}")

# --- BAR CHART: ATTACKS BY METHOD ---
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

# --- PIE CHART: ATTACK METHOD DISTRIBUTION ---
st.subheader("📊 Attack Method Share (by Financial Impact)")
if not filtered.empty:
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

# --- BAR CHART: TOTAL LOSS BY METHOD ---
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

# --- TOP LOSSES TABLE ---
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

# --- SEARCH ACROSS TABLE ---
st.subheader("🔍 Quick Search")
search_text = st.text_input("Search for anything (target, attacker, remediation...):")
if search_text.strip():
    st.write("Search results:")
    mask2 = filtered.apply(lambda row: search_text.lower() in str(row).lower(), axis=1)
    st.dataframe(filtered[mask2])

st.caption("© 2025 Cyber Attack Feed Dashboard | Made with Streamlit")
