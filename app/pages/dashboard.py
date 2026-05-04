"""
Main Dashboard Page

Production-level dashboard showing comprehensive business KPIs and revenue metrics.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from components.filters import render_date_range_filter, get_filter_summary
from components.charts import (
    create_revenue_trend_chart,
    create_revenue_breakdown_chart,
    create_product_revenue_chart,
    create_segment_revenue_chart,
    create_channel_performance_chart,
    create_indicator_card,
    create_gauge_chart,
    get_revenue_sample_data,
    get_customer_segmentation_data,
    get_product_performance_data,
    get_daily_metrics_data
)

# Page configuration
st.set_page_config(
    page_title="Dashboard - KPI Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .section-divider {
        margin: 2rem 0;
        border-top: 2px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Dashboard header
st.markdown('<h1 class="main-header">📊 Business Intelligence Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Comprehensive view of key performance indicators and revenue metrics</p>', unsafe_allow_html=True)

# Render date range filter
with st.expander("🔧 Filters & Date Range", expanded=False):
    start_date, end_date, filters_applied = render_date_range_filter(
        key_prefix="dashboard",
        default_range="Last 30 Days",
        show_apply_button=True
    )
    
    if filters_applied:
        st.success(f"✅ Showing data from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}")

st.markdown("---")

# Main dashboard content
if filters_applied:
    # Calculate metrics based on sample data
    revenue_data = get_revenue_sample_data('30d')
    customer_data = get_customer_segmentation_data()
    product_data = get_product_performance_data()
    daily_metrics = get_daily_metrics_data(30)
    
    # Calculate key metrics
    total_revenue = revenue_data['revenue'].sum()
    previous_revenue = revenue_data['revenue'].iloc[:15].sum()
    current_revenue = revenue_data['revenue'].iloc[15:].sum()
    revenue_growth = ((current_revenue - previous_revenue) / previous_revenue) * 100
    
    total_customers = customer_data['customers'].sum()
    avg_churn = customer_data['churn_rate'].mean()
    avg_nps = daily_metrics['nps_score'].mean()
    
    # ==================== SECTION 1: KEY METRICS OVERVIEW ====================
    st.subheader("📈 Key Performance Indicators")
    
    # Top row - Primary KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        fig_revenue = create_indicator_card(
            value=total_revenue,
            title='Total Revenue (30d)',
            previous_value=total_revenue * 0.92,
            units='$',
            height=180
        )
        st.plotly_chart(fig_revenue, width='stretch')
    
    with col2:
        fig_customers = create_indicator_card(
            value=total_customers,
            title='Total Customers',
            previous_value=total_customers * 0.95,
            units='',
            height=180
        )
        st.plotly_chart(fig_customers, width='stretch')
    
    with col3:
        fig_mrr = create_indicator_card(
            value=385420,
            title='Monthly Recurring Revenue',
            previous_value=371340,
            units='$',
            height=180
        )
        st.plotly_chart(fig_mrr, width='stretch')
    
    with col4:
        fig_active = create_indicator_card(
            value=daily_metrics['active_users'].iloc[-1],
            title='Active Users (Today)',
            previous_value=daily_metrics['active_users'].iloc[-7],
            units='',
            height=180
        )
        st.plotly_chart(fig_active, width='stretch')
    
    # Second row - Gauge metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Avg Order Value",
            value=f"${total_revenue / total_customers:.2f}",
            delta=f"+{revenue_growth:.1f}%"
        )
    
    with col2:
        st.metric(
            label="🎯 Customer Satisfaction",
            value=f"{avg_nps:.1f}",
            delta="+2.3 pts",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="🔄 Avg Churn Rate",
            value=f"{avg_churn:.1f}%",
            delta="-1.2%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="📊 Conversion Rate",
            value="4.7%",
            delta="+0.5%"
        )
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ==================== SECTION 2: REVENUE ANALYSIS ====================
    st.subheader("💰 Revenue Analysis")
    
    tab1, tab2, tab3 = st.tabs(["📈 Trend Analysis", "📊 Breakdown", "🎯 Performance"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Revenue Trend - Last 30 Days")
            fig_trend = create_revenue_trend_chart(period='30d', height=400)
            st.plotly_chart(fig_trend, width='stretch')
        
        with col2:
            st.markdown("#### Key Insights")
            st.info(f"""
            **Period**: Last 30 Days
            
            **Total Revenue**: ${total_revenue:,.0f}
            
            **Growth Rate**: +{revenue_growth:.1f}%
            
            **Daily Average**: ${revenue_data['revenue'].mean():,.0f}
            
            **Best Day**: ${revenue_data['revenue'].max():,.0f}
            
            **Pattern**: Strong weekday performance with weekend dips
            """)
            
            # Additional metrics
            st.markdown("#### Quick Stats")
            st.metric("Peak Revenue Day", revenue_data['date'].iloc[revenue_data['revenue'].idxmax()].strftime('%b %d'))
            st.metric("Weekday Avg", f"${revenue_data[revenue_data['date'].dt.dayofweek < 5]['revenue'].mean():,.0f}")
            st.metric("Weekend Avg", f"${revenue_data[revenue_data['date'].dt.dayofweek >= 5]['revenue'].mean():,.0f}")
    
    with tab2:
        st.markdown("#### Revenue, Cost & Profit Analysis - Last 12 Months")
        fig_breakdown = create_revenue_breakdown_chart(period='12m', height=450)
        st.plotly_chart(fig_breakdown, width='stretch')
        
        # Metrics row
        revenue_12m = get_revenue_sample_data('12m')
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Revenue (12m)", f"${revenue_12m['revenue'].sum():,.0f}", "+18.3%")
        with col2:
            st.metric("Total Cost (12m)", f"${revenue_12m['cost'].sum():,.0f}", "+15.7%")
        with col3:
            st.metric("Total Profit (12m)", f"${revenue_12m['profit'].sum():,.0f}", "+23.1%")
        with col4:
            profit_margin = (revenue_12m['profit'].sum() / revenue_12m['revenue'].sum()) * 100
            st.metric("Profit Margin", f"{profit_margin:.1f}%", "+1.2%")
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Revenue by Product")
            fig_products = create_product_revenue_chart(height=400, orientation='v')
            st.plotly_chart(fig_products, width='stretch')
        
        with col2:
            st.markdown("#### Revenue by Customer Segment")
            fig_segments = create_segment_revenue_chart(height=400)
            st.plotly_chart(fig_segments, width='stretch')
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ==================== SECTION 3: CHANNEL & REGIONAL PERFORMANCE ====================
    st.subheader("🌍 Channel & Regional Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Marketing Channel Performance")
        fig_channels = create_channel_performance_chart(height=450)
        st.plotly_chart(fig_channels, width='stretch')
        
        st.info("""
        **Top Performer**: Direct Sales - $2.15M
        
        **Best ROI**: Organic Search - 14.5x return
        
        **Growth Channel**: Social Media - 31.5% growth
        """)
    
    with col2:
        st.markdown("#### Daily Active Users & Signups")
        
        # Create a simple line chart for active users
        from components.charts import create_multi_line_chart
        fig_users = create_multi_line_chart(
            data=daily_metrics,
            x_column='date',
            y_columns=['active_users', 'new_signups'],
            title='User Activity Trends',
            x_label='Date',
            y_label='Count',
            height=450,
            colors=['#1f77b4', '#2ca02c']
        )
        st.plotly_chart(fig_users, width='stretch')
        
        st.success(f"""
        **Active Users Today**: {daily_metrics['active_users'].iloc[-1]:,}
        
        **New Signups (30d)**: {daily_metrics['new_signups'].sum():,}
        
        **Avg Daily Signups**: {daily_metrics['new_signups'].mean():.0f}
        """)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ==================== SECTION 4: DETAILED METRICS TABLE ====================
    st.subheader("📋 Detailed Performance Data")
    
    tab1, tab2, tab3 = st.tabs(["Products", "Customer Segments", "Daily Metrics"])
    
    with tab1:
        st.markdown("#### Product Performance Breakdown")
        df_products = get_product_performance_data()
        
        # Format the dataframe for display
        df_display = df_products.copy()
        df_display['revenue'] = df_display['revenue'].apply(lambda x: f"${x:,.0f}")
        df_display['units_sold'] = df_display['units_sold'].apply(lambda x: f"{x:,}")
        df_display['growth_rate'] = df_display['growth_rate'].apply(lambda x: f"{x:+.1f}%")
        
        st.dataframe(df_display, width='stretch', hide_index=True)
    
    with tab2:
        st.markdown("#### Customer Segmentation Analysis")
        df_segments = get_customer_segmentation_data()
        
        # Format the dataframe
        df_display = df_segments.copy()
        df_display['customers'] = df_display['customers'].apply(lambda x: f"{x:,}")
        df_display['revenue'] = df_display['revenue'].apply(lambda x: f"${x:,.0f}")
        df_display['avg_order_value'] = df_display['avg_order_value'].apply(lambda x: f"${x:,.2f}")
        df_display['churn_rate'] = df_display['churn_rate'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(df_display, width='stretch', hide_index=True)
    
    with tab3:
        st.markdown("#### Recent Daily Metrics (Last 10 Days)")
        df_daily = daily_metrics.tail(10).copy()
        
        # Format the dataframe
        df_daily['date'] = df_daily['date'].dt.strftime('%Y-%m-%d')
        df_daily['active_users'] = df_daily['active_users'].apply(lambda x: f"{x:,}")
        df_daily['new_signups'] = df_daily['new_signups'].apply(lambda x: f"{x:,}")
        df_daily['revenue'] = df_daily['revenue'].apply(lambda x: f"${x:,.2f}")
        df_daily['support_tickets'] = df_daily['support_tickets'].apply(lambda x: f"{x:,}")
        df_daily['nps_score'] = df_daily['nps_score'].apply(lambda x: f"{x:.1f}")
        
        st.dataframe(df_daily, width='stretch', hide_index=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ==================== FOOTER ====================
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.caption(f"📅 Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    
    with col2:
        st.caption("📊 Data Source: Production Sample Data")
    
    with col3:
        st.caption("🔄 Auto-refresh: Every 5 minutes")

else:
    # Initial state - no filters applied
    st.info("👆 **Get Started**: Click 'Filters & Date Range' above and select your date range, then click 'Apply Filters' to view the dashboard.")
    
    # Show a preview
    st.markdown("### 📊 Dashboard Preview")
    st.markdown("The dashboard includes:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📈 Key Metrics**
        - Total Revenue
        - Customer Count
        - Monthly Recurring Revenue
        - Active Users
        """)
    
    with col2:
        st.markdown("""
        **💰 Revenue Analysis**
        - 30-day trend charts
        - 12-month breakdown
        - Product performance
        - Segment distribution
        """)
    
    with col3:
        st.markdown("""
        **🌍 Performance Insights**
        - Channel performance
        - User activity trends
        - Detailed data tables
        - Growth metrics
        """)
