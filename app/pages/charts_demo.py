"""
Charts Demo Page

This page demonstrates all available chart components with realistic sample data.
Perfect for testing and showcasing the charting capabilities of the platform.
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.charts import (
    create_revenue_trend_chart,
    create_revenue_breakdown_chart,
    create_product_revenue_chart,
    create_segment_revenue_chart,
    create_channel_performance_chart,
    create_regional_performance_chart,
    create_activity_heatmap_chart,
    create_customer_satisfaction_gauge,
    create_mrr_indicator,
    create_revenue_growth_combo_chart,
    get_revenue_sample_data,
    get_customer_segmentation_data,
    get_product_performance_data,
    get_channel_performance_data
)

# Page configuration
st.set_page_config(
    page_title="Charts Demo - KPI Intelligence",
    page_icon="📊",
    layout="wide"
)

# Page header
st.title("📊 Chart Components Demo")
st.markdown("---")
st.markdown("""
This page demonstrates all available chart types with **realistic static sample data**.
All charts are production-ready and can be integrated into your dashboards.
""")

# ==================== SECTION 1: KPI INDICATORS ====================
st.header("🎯 KPI Indicators")
st.markdown("Real-time metrics and gauge charts for monitoring key performance indicators.")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Monthly Recurring Revenue")
    fig_mrr = create_mrr_indicator(height=250)
    st.plotly_chart(fig_mrr, use_container_width=True)

with col2:
    st.subheader("Customer Satisfaction")
    fig_csat = create_customer_satisfaction_gauge(height=300)
    st.plotly_chart(fig_csat, use_container_width=True)

with col3:
    st.subheader("Active Users")
    from components.charts import create_indicator_card
    fig_users = create_indicator_card(
        value=15847,
        title='Active Users',
        previous_value=14923,
        units='users',
        height=250
    )
    st.plotly_chart(fig_users, use_container_width=True)

st.markdown("---")

# ==================== SECTION 2: TREND ANALYSIS ====================
st.header("📈 Trend Analysis")
st.markdown("Time series charts for tracking metrics over different periods.")

# Revenue Trend
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Revenue Trend - Last 30 Days")
    fig_trend = create_revenue_trend_chart(period='30d', height=400)
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.markdown("#### Key Insights")
    st.info("""
    - **Steady Growth**: Revenue shows consistent upward trend
    - **Weekday Pattern**: Higher activity Monday-Friday
    - **Current MRR**: $385,420 (+3.8% MoM)
    """)

# Multi-line chart
st.subheader("Revenue, Cost & Profit Analysis - Last 12 Months")
fig_breakdown = create_revenue_breakdown_chart(period='12m', height=400)
st.plotly_chart(fig_breakdown, use_container_width=True)

st.markdown("---")

# ==================== SECTION 3: COMPARATIVE ANALYSIS ====================
st.header("📊 Comparative Analysis")
st.markdown("Bar charts and comparisons across different dimensions.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Product")
    fig_products = create_product_revenue_chart(height=450, orientation='v')
    st.plotly_chart(fig_products, use_container_width=True)

with col2:
    st.subheader("Revenue by Marketing Channel")
    fig_channels = create_channel_performance_chart(height=450)
    st.plotly_chart(fig_channels, use_container_width=True)

st.markdown("---")

# ==================== SECTION 4: DISTRIBUTION & COMPOSITION ====================
st.header("🥧 Distribution Analysis")
st.markdown("Pie and donut charts showing composition and distribution.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Customer Segment")
    fig_segments = create_segment_revenue_chart(height=450)
    st.plotly_chart(fig_segments, use_container_width=True)

with col2:
    st.subheader("Regional Performance")
    fig_regional = create_regional_performance_chart(height=450)
    st.plotly_chart(fig_regional, use_container_width=True)

st.markdown("---")

# ==================== SECTION 5: ADVANCED VISUALIZATIONS ====================
st.header("🔥 Advanced Visualizations")
st.markdown("Complex charts for detailed analysis.")

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("User Activity Heatmap")
    fig_heatmap = create_activity_heatmap_chart(height=450)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    st.caption("Peak activity: Tuesday-Thursday, 3-6pm")

with col2:
    st.subheader("Revenue & Growth Rate")
    fig_combo = create_revenue_growth_combo_chart(height=450)
    st.plotly_chart(fig_combo, use_container_width=True)
    st.caption("Monthly revenue with growth rate overlay")

st.markdown("---")

# ==================== SECTION 6: DATA TABLES ====================
st.header("📋 Sample Data Tables")
st.markdown("View the underlying data used in the charts above.")

tab1, tab2, tab3 = st.tabs(["Product Performance", "Customer Segments", "Marketing Channels"])

with tab1:
    st.subheader("Product Performance Metrics")
    df_products = get_product_performance_data()
    st.dataframe(df_products, use_container_width=True)
    
    st.markdown("**Summary Statistics:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Revenue", f"${df_products['revenue'].sum():,.0f}")
    with col2:
        st.metric("Total Units Sold", f"{df_products['units_sold'].sum():,}")
    with col3:
        st.metric("Avg Growth Rate", f"{df_products['growth_rate'].mean():.1f}%")

with tab2:
    st.subheader("Customer Segmentation Data")
    df_segments = get_customer_segmentation_data()
    st.dataframe(df_segments, use_container_width=True)
    
    st.markdown("**Key Metrics:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Customers", f"{df_segments['customers'].sum():,}")
    with col2:
        st.metric("Total Revenue", f"${df_segments['revenue'].sum():,.0f}")
    with col3:
        st.metric("Avg Churn Rate", f"{df_segments['churn_rate'].mean():.1f}%")

with tab3:
    st.subheader("Marketing Channel Performance")
    df_channels = get_channel_performance_data()
    st.dataframe(df_channels, use_container_width=True)
    
    st.markdown("**Channel Insights:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Revenue", f"${df_channels['revenue'].sum():,.0f}")
    with col2:
        st.metric("Total Conversions", f"{df_channels['conversions'].sum():,}")
    with col3:
        st.metric("Avg ROI", f"{df_channels['roi'].mean():.1f}x")

st.markdown("---")

# ==================== FOOTER ====================
st.markdown("""
### 💡 Implementation Notes

All charts above use **realistic static sample data** that's perfect for:
- Development and testing
- Demo presentations
- UI/UX design validation
- Training and documentation

**To use in your pages:**
```python
from components.charts import create_revenue_trend_chart

# Simple usage with default sample data
fig = create_revenue_trend_chart(period='30d')
st.plotly_chart(fig, use_container_width=True)

# Or with your own data
from components.charts import create_line_chart
fig = create_line_chart(data=your_dataframe, x_column='date', y_column='revenue')
st.plotly_chart(fig, use_container_width=True)
```

📚 **See** `components/charts.py` for complete documentation and all available functions.
""")
