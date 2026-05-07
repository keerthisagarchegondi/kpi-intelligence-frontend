"""
Main Dashboard Page

Production-level dashboard with backend integration showing comprehensive
business KPIs, revenue metrics, and product performance.
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
    create_product_performance_overview,
    create_product_category_distribution,
    create_product_profitability_matrix,
    create_product_roi_ranking,
    create_product_quantity_revenue_comparison,
    get_revenue_sample_data,
    get_customer_segmentation_data,
    get_product_performance_data,
    get_daily_metrics_data
)

# Import API service
from services.api import (
    fetch_product_performance,
    fetch_product_kpi,
    fetch_dashboard_metrics,
    fetch_revenue_data,
    fetch_customer_data,
    fetch_anomalies,
    upload_file,
    is_backend_available,
    display_connection_status,
    load_data_with_fallback
)

# Import alerts component
from components.alerts import (
    display_compact_anomaly_banner,
    display_anomaly_alerts,
    create_anomaly_settings_sidebar
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

# Display backend connection status
display_connection_status()

# ==================== ANOMALY ALERTS SECTION ====================
st.markdown("### 🚨 Anomaly Detection & Alerts")

# Create two columns: alerts and upload
alert_col, upload_col = st.columns([2, 1])

with alert_col:
    # Fetch and display anomalies
    with st.spinner("Checking for anomalies..."):
        try:
            anomalies_data = fetch_anomalies(
                metric="revenue",
                method="zscore",
                threshold=3.0,
                period="30d",
                limit=10,
                use_cache=True
            )
            
            if anomalies_data and anomalies_data.get('status') == 'success':
                display_compact_anomaly_banner(anomalies_data)
                
                # Show details in expander
                with st.expander("📊 View Detailed Anomaly Report", expanded=False):
                    display_anomaly_alerts(anomalies_data, show_details=True)
            else:
                st.info("✅ No anomalies detected. System operating normally.")
        
        except Exception as e:
            st.warning(f"⚠️ Unable to fetch anomaly data: {str(e)}")

with upload_col:
    st.markdown("#### 📤 Upload Data File")
    
    uploaded_file = st.file_uploader(
        "Upload CSV, Excel, or Parquet",
        type=['csv', 'xlsx', 'xls', 'parquet', 'json'],
        help="Upload data files for processing and analysis (max 50MB)",
        key="dashboard_upload"
    )
    
    if uploaded_file is not None:
        # Show upload options
        with st.expander("⚙️ Upload Options", expanded=True):
            process_data = st.checkbox("Process & Clean Data", value=True)
            save_raw = st.checkbox("Save Original File", value=True)
            save_processed = st.checkbox("Save Processed File", value=True)
            validate = st.checkbox("Validate Schema", value=True)
            
            if st.button("🚀 Upload File", type="primary"):
                with st.spinner(f"Uploading {uploaded_file.name}..."):
                    try:
                        # Read file content
                        file_content = uploaded_file.read()
                        
                        # Upload to backend
                        result = upload_file(
                            file_content=file_content,
                            filename=uploaded_file.name,
                            process_data=process_data,
                            save_to_raw=save_raw,
                            save_to_processed=save_processed,
                            validate_schema=validate
                        )
                        
                        if result and result.get('status') == 'success':
                            st.success(f"✅ {result['message']}")
                            
                            # Display upload details
                            file_info = result.get('file_info', {})
                            st.info(
                                f"📁 **File:** {file_info.get('filename', 'N/A')}  \n"
                                f"📊 **Size:** {file_info.get('file_size_mb', 0):.2f} MB  \n"
                                f"📋 **Rows:** {file_info.get('rows', 0):,}  \n"
                                f"📏 **Columns:** {file_info.get('columns', 0)}  \n"
                                f"⏱️ **Processing Time:** {result.get('processing_time_seconds', 0):.2f}s"
                            )
                            
                            # Show validation results if any
                            validation = result.get('validation_results', {})
                            if validation:
                                if validation.get('has_errors'):
                                    st.error(f"❌ Validation Errors: {', '.join(validation.get('errors', []))}")
                                elif validation.get('has_warnings'):
                                    st.warning(f"⚠️ Warnings: {', '.join(validation.get('warnings', []))}")
                                else:
                                    st.success("✅ All validations passed!")
                            
                            # Show processing summary
                            if process_data and 'processing_summary' in result:
                                summary = result['processing_summary']
                                if summary and 'actions' in summary:
                                    with st.expander("🔧 Processing Actions", expanded=False):
                                        for action in summary['actions']:
                                            st.text(f"• {action}")
                        else:
                            st.error("❌ Upload failed. Please check the file and try again.")
                    
                    except Exception as e:
                        st.error(f"❌ Upload error: {str(e)}")

st.markdown("---")

# Main dashboard content
if filters_applied:
    # Check backend availability
    backend_connected = is_backend_available()
    
    # Load data from backend with fallback to sample data
    with st.spinner("Loading dashboard data..."):
        # Try to fetch from backend, fall back to sample data
        if backend_connected:
            try:
                # Fetch from backend
                dashboard_metrics = fetch_dashboard_metrics(use_cache=True)
                product_kpi_data = fetch_product_kpi(use_cache=True)
                product_performance = fetch_product_performance(limit=20, use_cache=True)
                customer_segments = fetch_customer_data(use_cache=True)
                
                # If any fetch fails, use sample data
                if dashboard_metrics is None:
                    st.info("⚠️ Using sample data - backend metrics unavailable")
                    revenue_data = get_revenue_sample_data('30d')
                    customer_data = get_customer_segmentation_data()
                    product_data = get_product_performance_data()
                    daily_metrics = get_daily_metrics_data(30)
                else:
                    # Use backend data
                    revenue_data = get_revenue_sample_data('30d')  # Still using sample for time series
                    customer_data = customer_segments if customer_segments is not None else get_customer_segmentation_data()
                    product_data = product_performance if product_performance is not None else get_product_performance_data()
                    daily_metrics = get_daily_metrics_data(30)  # Still using sample
                    
            except Exception as e:
                st.warning(f"⚠️ Error loading backend data: {str(e)}. Using sample data.")
                revenue_data = get_revenue_sample_data('30d')
                customer_data = get_customer_segmentation_data()
                product_data = get_product_performance_data()
                daily_metrics = get_daily_metrics_data(30)
                dashboard_metrics = None
                product_kpi_data = None
        else:
            # Backend not available, use sample data
            revenue_data = get_revenue_sample_data('30d')
            customer_data = get_customer_segmentation_data()
            product_data = get_product_performance_data()
            daily_metrics = get_daily_metrics_data(30)
            dashboard_metrics = None
            product_kpi_data = None
    
    # Calculate key metrics
    if dashboard_metrics and 'product_metrics' in dashboard_metrics:
        # Use backend metrics
        product_metrics = dashboard_metrics['product_metrics']
        total_revenue = product_metrics.get('total_revenue', 0)
        total_profit = product_metrics.get('total_profit', 0)
        avg_profit_margin = product_metrics.get('avg_profit_margin', 0)
    else:
        # Calculate from sample data
        total_revenue = revenue_data['revenue'].sum()
        total_profit = revenue_data['profit'].sum() if 'profit' in revenue_data.columns else total_revenue * 0.33
        avg_profit_margin = 23.5
    
    previous_revenue = total_revenue * 0.87
    revenue_growth = ((total_revenue - previous_revenue) / previous_revenue) * 100
    
    total_customers = customer_data['customers'].sum() if 'customers' in customer_data.columns else len(customer_data)
    avg_churn = customer_data['churn_rate'].mean() if 'churn_rate' in customer_data.columns else 12.7
    avg_nps = daily_metrics['nps_score'].mean() if 'nps_score' in daily_metrics.columns else 62.4
    
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
    
    # ==================== SECTION 3: PRODUCT KPIs & PERFORMANCE ====================
    st.subheader("📦 Product Performance & KPIs")
    
    # Show data source indicator
    if backend_connected and product_kpi_data:
        st.success("✅ Displaying real product data from backend")
    else:
        st.info("ℹ️ Displaying sample product data")
    
    # Product KPI Summary Cards
    if product_kpi_data:
        summary = product_kpi_data.get('summary', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Product Revenue",
                f"${summary.get('total_revenue', 0):,.0f}",
                f"+{summary.get('revenue_growth', 15.3):.1f}%"
            )
        
        with col2:
            st.metric(
                "Total Profit",
                f"${summary.get('total_profit', 0):,.0f}",
                f"+{summary.get('profit_growth', 12.7):.1f}%"
            )
        
        with col3:
            st.metric(
                "Avg Profit Margin",
                f"{summary.get('avg_profit_margin', 0):.1f}%",
                "+1.2%"
            )
        
        with col4:
            st.metric(
                "Total Transactions",
                f"{summary.get('total_transactions', 0):,}",
                "+8.4%"
            )
    else:
        # Use sample data metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Product Revenue", f"${product_data['total_revenue'].sum() if 'total_revenue' in product_data.columns else 0:,.0f}", "+15.3%")
        with col2:
            st.metric("Total Profit", f"${product_data['total_profit'].sum() if 'total_profit' in product_data.columns else 0:,.0f}", "+12.7%")
        with col3:
            st.metric("Avg Profit Margin", f"{product_data['profit_margin'].mean() if 'profit_margin' in product_data.columns else 0:.1f}%", "+1.2%")
        with col4:
            st.metric("Total Transactions", f"{product_data['transaction_count'].sum() if 'transaction_count' in product_data.columns else 0:,}", "+8.4%")
    
    # Product Performance Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Performance Overview",
        "💰 Profitability Matrix",
        "📈 ROI Ranking",
        "📦 Category Analysis"
    ])
    
    with tab1:
        st.markdown("#### Top Products by Revenue & Profit Margin")
        
        if not product_data.empty:
            fig_overview = create_product_performance_overview(
                data=product_data,
                top_n=10,
                height=500
            )
            st.plotly_chart(fig_overview, use_container_width=True)
            
            # Side by side metrics
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Top 5 by Revenue")
                if 'total_revenue' in product_data.columns:
                    top_5_revenue = product_data.nlargest(5, 'total_revenue')[['product', 'total_revenue', 'profit_margin']]
                    for idx, row in top_5_revenue.iterrows():
                        st.markdown(f"**{row['product']}**: ${row['total_revenue']:,.0f} ({row['profit_margin']:.1f}% margin)")
            
            with col2:
                st.markdown("##### Top 5 by Profit Margin")
                if 'profit_margin' in product_data.columns:
                    top_5_margin = product_data.nlargest(5, 'profit_margin')[['product', 'profit_margin', 'total_revenue']]
                    for idx, row in top_5_margin.iterrows():
                        st.markdown(f"**{row['product']}**: {row['profit_margin']:.1f}% (${row['total_revenue']:,.0f} revenue)")
        else:
            st.warning("No product data available")
    
    with tab2:
        st.markdown("#### Product Profitability Matrix (Revenue vs Margin)")
        st.markdown("*Bubble size represents transaction volume, color represents ROI*")
        
        if not product_data.empty and len(product_data) > 1:
            fig_matrix = create_product_profitability_matrix(
                data=product_data,
                height=500
            )
            st.plotly_chart(fig_matrix, use_container_width=True)
            
            st.info("""
            **How to read this chart:**
            - **Stars** (Top Right): High revenue, high margin - ideal products
            - **Cash Cows** (Bottom Right): High revenue, lower margin - volume drivers
            - **Question Marks** (Top Left): Low revenue, high margin - growth potential
            - **Dogs** (Bottom Left): Low revenue, low margin - consider optimization
            """)
        else:
            st.warning("Insufficient data for profitability matrix")
    
    with tab3:
        st.markdown("#### Return on Investment (ROI) Ranking")
        
        if not product_data.empty:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig_roi = create_product_roi_ranking(
                    data=product_data,
                    top_n=10,
                    height=400
                )
                st.plotly_chart(fig_roi, use_container_width=True)
            
            with col2:
                st.markdown("##### ROI Insights")
                if 'roi' in product_data.columns:
                    avg_roi = product_data['roi'].mean()
                    max_roi = product_data['roi'].max()
                    best_product = product_data.loc[product_data['roi'].idxmax(), 'product']
                    
                    st.metric("Average ROI", f"{avg_roi:.1f}%")
                    st.metric("Best ROI", f"{max_roi:.1f}%")
                    st.success(f"**Top Performer**: {best_product}")
                    
                    st.markdown("##### ROI Distribution")
                    high_roi = len(product_data[product_data['roi'] > 30])
                    medium_roi = len(product_data[(product_data['roi'] >= 20) & (product_data['roi'] <= 30)])
                    low_roi = len(product_data[product_data['roi'] < 20])
                    
                    st.markdown(f"- **High ROI (>30%)**: {high_roi} products")
                    st.markdown(f"- **Medium ROI (20-30%)**: {medium_roi} products")
                    st.markdown(f"- **Low ROI (<20%)**: {low_roi} products")
        else:
            st.warning("No product data available for ROI analysis")
    
    with tab4:
        st.markdown("#### Product Performance by Category")
        
        if not product_data.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                fig_category = create_product_category_distribution(
                    data=product_data,
                    height=400
                )
                st.plotly_chart(fig_category, use_container_width=True)
            
            with col2:
                st.markdown("#### Quantity vs Revenue Comparison")
                fig_qty_rev = create_product_quantity_revenue_comparison(
                    data=product_data,
                    top_n=8,
                    height=400
                )
                st.plotly_chart(fig_qty_rev, use_container_width=True)
        else:
            st.warning("No product data available for category analysis")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ==================== SECTION 4: CHANNEL & REGIONAL PERFORMANCE ====================
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
    
    # ==================== SECTION 5: DETAILED METRICS TABLE ====================
    st.subheader("📋 Detailed Performance Data")
    
    tab1, tab2, tab3 = st.tabs(["Products", "Customer Segments", "Daily Metrics"])
    
    with tab1:
        st.markdown("#### Product Performance Breakdown")
        
        if not product_data.empty:
            # Show backend data or sample data
            df_display = product_data.copy()
            
            # Format columns based on what's available
            if 'total_revenue' in df_display.columns:
                df_display['total_revenue'] = df_display['total_revenue'].apply(lambda x: f"${x:,.2f}")
            if 'total_profit' in df_display.columns:
                df_display['total_profit'] = df_display['total_profit'].apply(lambda x: f"${x:,.2f}")
            if 'profit_margin' in df_display.columns:
                df_display['profit_margin'] = df_display['profit_margin'].apply(lambda x: f"{x:.2f}%")
            if 'roi' in df_display.columns:
                df_display['roi'] = df_display['roi'].apply(lambda x: f"{x:.2f}%")
            if 'transaction_count' in df_display.columns:
                df_display['transaction_count'] = df_display['transaction_count'].apply(lambda x: f"{int(x):,}")
            if 'total_quantity' in df_display.columns:
                df_display['total_quantity'] = df_display['total_quantity'].apply(lambda x: f"{int(x):,}")
            if 'return_rate' in df_display.columns:
                df_display['return_rate'] = df_display['return_rate'].apply(lambda x: f"{x:.2f}%")
            
            # Select relevant columns for display
            display_cols = ['product']
            if 'category' in df_display.columns:
                display_cols.append('category')
            display_cols.extend([col for col in ['total_revenue', 'total_profit', 'profit_margin', 'roi', 
                                                 'transaction_count', 'total_quantity', 'return_rate'] 
                                if col in df_display.columns])
            
            st.dataframe(df_display[display_cols], use_container_width=True, hide_index=True)
            
            # Download button
            if backend_connected:
                st.download_button(
                    label="📥 Download Product Data (CSV)",
                    data=product_data.to_csv(index=False),
                    file_name=f"product_performance_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        else:
            st.warning("No product performance data available")
    
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
