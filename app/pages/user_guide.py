"""
User Guide Page

Comprehensive user guide and documentation for the KPI Intelligence Platform.
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from components.help import display_user_guide_page

# Page configuration
st.set_page_config(
    page_title="User Guide - KPI Intelligence",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the guide
st.markdown("""
<style>
    .guide-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .guide-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #1f77b4;
    }
    .tip-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Display the comprehensive user guide
display_user_guide_page()

# Add quick links in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("## 📑 Quick Navigation")
    st.markdown("""
    - [Getting Started](#getting-started)
    - [Dashboard](#dashboard-overview)
    - [Reports & Tables](#reports-tables)
    - [Revenue Analytics](#revenue-analytics)
    - [Retention Analysis](#retention-analysis)
    - [Data Export](#data-export)
    - [Tips & Tricks](#tips-tricks)
    - [Troubleshooting](#troubleshooting)
    """)
    
    st.markdown("---")
    st.markdown("## 💡 Need More Help?")
    st.info("""
    - Check the help section on each page
    - Review tooltips on UI elements
    - Visit the Service Status page for connectivity issues
    """)
    
    st.markdown("---")
    st.markdown("## 🔗 Related Pages")
    st.markdown("""
    - 📊 Dashboard
    - 📋 Reports
    - 💰 Revenue Analytics
    - 🔄 Retention Metrics
    - 🔗 Service Status
    """)
