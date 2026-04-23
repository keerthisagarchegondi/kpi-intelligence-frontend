import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from components.filters import render_date_range_filter, get_filter_summary

# Page configuration
st.set_page_config(
    page_title="Dashboard - KPI Intelligence",
    page_icon="📊",
    layout="wide"
)

# Dashboard title
st.title("📊 Main Dashboard")
st.markdown("---")

# Render date range filter
with st.expander("🔧 Filters & Settings", expanded=True):
    start_date, end_date, filters_applied = render_date_range_filter(
        key_prefix="dashboard",
        default_range="Last 30 Days",
        show_apply_button=True
    )

# Main content
st.header("Overview Dashboard")

if filters_applied:
    # Display active filter summary
    st.markdown(get_filter_summary(start_date, end_date))
    st.markdown("---")
    
    # Placeholder sections with metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Revenue", value="$125,430", delta="+12.5%")
    
    with col2:
        st.metric(label="Active Customers", value="1,247", delta="+8.2%")
    
    with col3:
        st.metric(label="Retention Rate", value="87.3%", delta="+2.1%")
    
    st.markdown("---")
    
    # Additional dashboard sections
    st.subheader("📈 Performance Overview")
    st.info("📊 Displaying data for the selected date range. Connect to data source to show real metrics.")
    
else:
    st.info("👆 Please apply filters to view dashboard data.")
