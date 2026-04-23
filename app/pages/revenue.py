import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from components.filters import render_date_range_filter, get_filter_summary, render_comparison_filter

# Page configuration
st.set_page_config(
    page_title="Revenue Analytics - KPI Intelligence",
    page_icon="💰",
    layout="wide"
)

# Page title
st.title("💰 Revenue Analytics")
st.markdown("---")

# Render filters in sidebar
with st.sidebar:
    st.header("⚙️ Revenue Filters")
    
    # Date range filter
    start_date, end_date, filters_applied = render_date_range_filter(
        key_prefix="revenue",
        default_range="Last 90 Days",
        show_apply_button=False  # Auto-apply for revenue page
    )
    
    st.markdown("---")
    
    # Comparison filter
    enable_comparison, comparison_period = render_comparison_filter(
        key_prefix="revenue"
    )

# Main content area
if filters_applied:
    # Display active filter summary
    st.markdown(f"**📅 Active Period:** {get_filter_summary(start_date, end_date)}")
    
    if enable_comparison:
        st.info(f"🔄 Comparing with: {comparison_period}")
    
    st.markdown("---")
    
    # Revenue metrics
    st.subheader("💵 Key Revenue Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Revenue",
            value="$482,350",
            delta="+15.3%",
            help="Total revenue for selected period"
        )
    
    with col2:
        st.metric(
            label="Average Revenue Per User",
            value="$142.50",
            delta="+8.7%",
            help="Average revenue per active user"
        )
    
    with col3:
        st.metric(
            label="Revenue Growth Rate",
            value="15.3%",
            delta="+2.1%",
            help="Month-over-month revenue growth"
        )
    
    with col4:
        st.metric(
            label="Total Transactions",
            value="3,384",
            delta="+12.4%",
            help="Number of transactions in period"
        )
    
    st.markdown("---")
    
    # Revenue breakdown sections
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📊 Revenue by Category")
        st.info("Connect data source to display revenue breakdown charts")
    
    with col_right:
        st.subheader("📈 Revenue Trend")
        st.info("Connect data source to display revenue trend analysis")
    
    st.markdown("---")
    
    # Additional insights
    st.subheader("💡 Revenue Insights")
    st.markdown("""
    - **Top Performing Period:** Revenue shows consistent growth trend
    - **Opportunity:** Focus on high-value customer segments
    - **Action Item:** Analyze revenue drivers for optimization
    """)
    
else:
    st.info("👆 Configure filters in the sidebar to view revenue analytics.")
