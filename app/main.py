import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from services.monitor import initialize_services, display_service_info

# Page configuration
st.set_page_config(
    page_title="KPI Intelligence & Reporting",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services on startup
initialize_services()

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
- 📊 **Reports** - Detailed interactive reports with export capabilities
- 🔗 **Service Status** - API integration monitoring and verification

Use the sidebar to navigate between different sections.
""")

# Display service status in sidebar
display_service_info()

# Sidebar navigation info
with st.sidebar:
    st.markdown("---")
    st.header("📍 Navigation")
    st.info("Use the pages above to explore different KPI sections.")
