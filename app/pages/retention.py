import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from components.filters import render_date_range_filter, get_filter_summary

# Page configuration
st.set_page_config(
    page_title="Retention Metrics - KPI Intelligence",
    page_icon="🔄",
    layout="wide"
)

# Page title
st.title("🔄 Customer Retention & Churn Analysis")
st.markdown("---")

# Render filters
with st.expander("🔧 Analysis Filters", expanded=True):
    start_date, end_date, filters_applied = render_date_range_filter(
        key_prefix="retention",
        default_range="Last 6 Months",
        show_apply_button=True
    )
    
    # Additional retention-specific filters
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        cohort_type = st.selectbox(
            "Cohort Type",
            options=["Monthly", "Weekly", "Quarterly"],
            help="Select cohort grouping for retention analysis"
        )
    
    with col_f2:
        segment = st.selectbox(
            "Customer Segment",
            options=["All Customers", "New Customers", "Existing Customers", "Enterprise", "SMB"],
            help="Filter by customer segment"
        )

# Main content
if filters_applied:
    # Display active filter summary
    st.markdown(get_filter_summary(
        start_date, 
        end_date, 
        f"Cohort: {cohort_type} | Segment: {segment}"
    ))
    st.markdown("---")
    
    # Key retention metrics
    st.subheader("🎯 Key Retention Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Retention Rate",
            value="87.3%",
            delta="+2.1%",
            help="Percentage of customers retained in period"
        )
    
    with col2:
        st.metric(
            label="Churn Rate",
            value="12.7%",
            delta="-2.1%",
            delta_color="inverse",
            help="Percentage of customers lost in period"
        )
    
    with col3:
        st.metric(
            label="Customer Lifetime Value",
            value="$2,450",
            delta="+5.8%",
            help="Average customer lifetime value"
        )
    
    with col4:
        st.metric(
            label="Active Customers",
            value="1,247",
            delta="+94",
            help="Total active customers in period"
        )
    
    st.markdown("---")
    
    # Retention analysis sections
    tab1, tab2, tab3 = st.tabs(["📊 Cohort Analysis", "📉 Churn Analysis", "💎 Customer Segments"])
    
    with tab1:
        st.subheader("Cohort Retention Analysis")
        st.info(f"📊 {cohort_type} cohort analysis will be displayed here when connected to data source")
        st.markdown("""
        **Cohort Analysis Insights:**
        - Track customer retention across different cohorts
        - Identify trends in customer behavior over time
        - Measure the effectiveness of retention strategies
        """)
    
    with tab2:
        st.subheader("Churn Analysis & Predictions")
        st.info("📉 Churn patterns and predictions will be displayed here")
        st.markdown("""
        **Churn Insights:**
        - Identify high-risk customer segments
        - Analyze churn reasons and patterns
        - Predict potential churners for proactive intervention
        """)
    
    with tab3:
        st.subheader("Customer Segment Performance")
        st.info(f"💎 Performance metrics for {segment} will be displayed here")
        st.markdown("""
        **Segment Analysis:**
        - Compare retention across different segments
        - Identify high-value customer groups
        - Optimize strategies for each segment
        """)
    
    st.markdown("---")
    
    # Action items
    st.subheader("⚡ Recommended Actions")
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.success("""
        **✅ Strong Performers:**
        - Retention rate above target (85%)
        - Continue current engagement strategies
        - Identify and replicate success factors
        """)
    
    with col_a2:
        st.warning("""
        **⚠️ Areas for Improvement:**
        - Monitor high-risk customer segments
        - Implement targeted retention campaigns
        - Enhance customer success initiatives
        """)

else:
    st.info("👆 Please apply filters to view retention and churn analysis.")
