import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from services.monitor import initialize_services, display_service_info
from components.help import display_onboarding_guide, create_help_sidebar

# Page configuration
st.set_page_config(
    page_title="KPI Intelligence & Reporting",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services on startup
initialize_services()

# Display onboarding guide for new users
display_onboarding_guide()

# Main app title with improved styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
        text-align: center;
        background: linear-gradient(135deg, #1f77b4 0%, #2ca02c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .welcome-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .feature-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .quick-action-btn {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        background-color: white;
        color: #1f77b4;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        margin-right: 1rem;
        margin-top: 1rem;
        transition: all 0.3s ease;
    }
    .quick-action-btn:hover {
        background-color: #f0f0f0;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📊 Business KPI Intelligence & Reporting System</h1>', unsafe_allow_html=True)
st.markdown("---")

# Welcome card with quick actions
st.markdown("""
<div class="welcome-card">
    <h2>👋 Welcome to KPI Intelligence Platform</h2>
    <p style="font-size: 1.1rem; margin-bottom: 1rem;">
        Transform your raw business data into actionable insights with powerful analytics and visualization tools.
    </p>
    <div>
        <span style="font-size: 0.9rem;">Quick Actions:</span><br>
        View Reports | 📊 Dashboard | 💰 Revenue | 🔄 Retention | 🔗 Service Status
    </div>
</div>
""", unsafe_allow_html=True)

# Feature overview in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💰</div>
        <h3>Revenue Analytics</h3>
        <p>Track and analyze revenue metrics across products, segments, and time periods. 
        Monitor growth trends and identify opportunities.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Interactive Reports</h3>
        <p>Generate comprehensive reports with advanced filtering, sorting, and export capabilities. 
        Explore your data dynamically.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔄</div>
        <h3>Retention Metrics</h3>
        <p>Monitor customer retention, analyze churn patterns, and optimize lifetime value. 
        Identify at-risk customers proactively.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <h3>Performance Dashboard</h3>
        <p>View real-time KPIs with interactive visualizations. Track key metrics 
        and get instant insights.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔗</div>
        <h3>Service Integration</h3>
        <p>Monitor API connectivity and data synchronization. Verify backend integration 
        and troubleshoot issues.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📥</div>
        <h3>Data Export</h3>
        <p>Export reports in multiple formats (CSV, Excel, JSON). Download filtered 
        data for offline analysis.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Getting started section
st.markdown("### 🚀 Getting Started")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    **New to the platform?** Here's how to get started:
    
    1. **Navigate** - Use the sidebar menu to access different sections
    2. **Filter** - Apply date ranges and filters to focus your analysis
    3. **Explore** - Interact with charts and tables for deeper insights
    4. **Export** - Download reports in your preferred format
    
    💡 **Tip**: Start with the Dashboard for a high-level overview, then dive into specific sections.
    """)

with col_b:
    st.markdown("""
    **Key Features at a Glance:**
    
    - ✅ Real-time data synchronization with backend API
    - ✅ Graceful fallback to sample data when offline
    - ✅ Advanced filtering and search capabilities
    - ✅ Interactive visualizations with drill-down
    - ✅ Multi-format export (CSV, Excel, JSON)
    - ✅ Comprehensive error handling and recovery
    """)

st.markdown("---")

# Quick links section
st.markdown("### 🔗 Quick Links")

link_col1, link_col2, link_col3, link_col4 = st.columns(4)

with link_col1:
    st.info("**📊 Dashboard**\n\nView comprehensive KPIs and metrics")

with link_col2:
    st.info("**📋 Reports**\n\nGenerate detailed data reports")

with link_col3:
    st.info("**💰 Revenue**\n\nAnalyze revenue trends")

with link_col4:
    st.info("**🔄 Retention**\n\nMonitor customer retention")

# Display service status in sidebar
display_service_info()

# Create help sidebar
create_help_sidebar()

# Sidebar navigation info
with st.sidebar:
    st.markdown("---")
    st.header("📍 Navigation")
    st.info("""
    **Use the pages above to explore different sections:**
    
    - 📊 Dashboard - KPI overview
    - 📋 Reports - Data tables
    - 💰 Revenue - Revenue analytics
    - 🔄 Retention - Retention metrics
    - 🔗 Service Status - API integration
    
    💡 Need help? Check the Quick Help section below!
    """)

