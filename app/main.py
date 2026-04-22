import streamlit as st

# Page configuration
st.set_page_config(
    page_title="KPI Intelligence & Reporting",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main app title
st.title("📊 Business KPI Intelligence & Reporting System")
st.markdown("---")

# Welcome message
st.markdown("""
### Welcome to the KPI Intelligence Platform

This system transforms raw business data into meaningful insights:
- 💰 **Revenue Analytics** - Track and analyze revenue metrics
- 🔄 **Retention Metrics** - Monitor customer retention and churn
- 📈 **Performance Dashboards** - Comprehensive business KPIs

Use the sidebar to navigate between different sections.
""")

# Sidebar navigation info
with st.sidebar:
    st.header("Navigation")
    st.info("Use the pages above to explore different KPI sections.")
