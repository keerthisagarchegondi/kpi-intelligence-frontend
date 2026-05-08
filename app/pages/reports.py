"""
Reports Page

Production-level reports page with comprehensive KPI data tables.
Features:
- Multiple report types (Sales, Products, Customers, Revenue)
- Advanced filtering and search
- Real-time data from API with fallback
- Export capabilities
- Interactive visualizations
- Drill-down analysis
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from components.tables import (
    create_interactive_table,
    create_summary_table,
    create_comparison_table,
    create_pivot_table,
    format_currency,
    format_percentage,
    format_number,
    color_negative_red
)

from components.filters import render_date_range_filter

# Import API service
from services.api import (
    fetch_kpi_overview,
    fetch_report_data,
    fetch_all_reports,
    fetch_top_performers,
    generate_sample_kpi_overview,
    generate_sample_report_list,
    generate_sample_report_data,
    display_connection_status,
    load_data_with_fallback
)

# Page configuration
st.set_page_config(
    page_title="Reports - KPI Intelligence",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
    .report-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .report-card:hover {
        transform: translateY(-5px);
    }
    .metric-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .info-banner {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown('<h1 class="main-header">📋 KPI Reports & Data Tables</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Comprehensive business intelligence reports with advanced analytics</p>', unsafe_allow_html=True)

# Connection status
display_connection_status()

st.markdown("---")

# Sidebar for report selection and filters
with st.sidebar:
    st.header("📊 Report Configuration")
    
    # Report type selector
    report_type = st.selectbox(
        "Select Report Type",
        options=[
            "📈 Sales Overview",
            "📦 Product Performance",
            "👥 Customer Analytics",
            "💰 Revenue Breakdown",
            "🏆 Top Performers",
            "📊 KPI Summary"
        ],
        help="Choose the type of report to view"
    )
    
    st.markdown("---")
    
    # Date range filter
    st.subheader("📅 Date Range")
    start_date, end_date, filters_applied = render_date_range_filter(
        key_prefix="reports",
        default_range="Last 30 Days",
        show_apply_button=False
    )
    
    st.markdown("---")
    
    # Additional filters based on report type
    st.subheader("🔧 Advanced Filters")
    
    if "Sales" in report_type:
        status_filter = st.multiselect(
            "Order Status",
            options=["Completed", "Pending", "Shipped", "Cancelled"],
            default=["Completed", "Pending", "Shipped"]
        )
        
        min_revenue = st.number_input(
            "Minimum Order Value",
            min_value=0.0,
            value=0.0,
            step=10.0
        )
    
    elif "Product" in report_type:
        category_filter = st.multiselect(
            "Product Category",
            options=["Electronics", "Accessories", "Components", "Peripherals"],
            default=["Electronics", "Accessories", "Components", "Peripherals"]
        )
        
        min_stock = st.number_input(
            "Minimum Stock Level",
            min_value=0,
            value=0,
            step=10
        )
    
    elif "Customer" in report_type:
        segment_filter = st.multiselect(
            "Customer Segment",
            options=["VIP", "Regular", "New", "Inactive"],
            default=["VIP", "Regular", "New"]
        )
        
        min_ltv = st.number_input(
            "Minimum Lifetime Value",
            min_value=0.0,
            value=0.0,
            step=100.0
        )
    
    elif "Revenue" in report_type:
        region_filter = st.multiselect(
            "Region",
            options=["North", "South", "East", "West"],
            default=["North", "South", "East", "West"]
        )
    
    st.markdown("---")
    
    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()


# Main content area
def load_report_data(report_type: str) -> pd.DataFrame:
    """Load data based on selected report type"""
    
    if "Sales" in report_type:
        # Try to fetch from API, fallback to sample data
        try:
            data = fetch_report_data('sales_overview', page_size=500)
            if data and 'data' in data:
                df = data['data']
            else:
                sample_data = generate_sample_report_data('sales_overview', page_size=200)
                df = pd.DataFrame(sample_data['records'])
        except:
            sample_data = generate_sample_report_data('sales_overview', page_size=200)
            df = pd.DataFrame(sample_data['records'])
        
        # Apply filters
        if 'status_filter' in locals() and status_filter:
            df = df[df['status'].isin(status_filter)]
        if 'min_revenue' in locals() and min_revenue > 0:
            df = df[df['revenue'] >= min_revenue]
    
    elif "Product" in report_type:
        try:
            data = fetch_report_data('product_performance', page_size=500)
            if data and 'data' in data:
                df = data['data']
            else:
                sample_data = generate_sample_report_data('product_performance', page_size=150)
                df = pd.DataFrame(sample_data['records'])
        except:
            sample_data = generate_sample_report_data('product_performance', page_size=150)
            df = pd.DataFrame(sample_data['records'])
        
        # Apply filters
        if 'category_filter' in locals() and category_filter:
            df = df[df['category'].isin(category_filter)]
        if 'min_stock' in locals() and min_stock > 0:
            df = df[df['stock_level'] >= min_stock]
    
    elif "Customer" in report_type:
        try:
            data = fetch_report_data('customer_analytics', page_size=500)
            if data and 'data' in data:
                df = data['data']
            else:
                sample_data = generate_sample_report_data('customer_analytics', page_size=200)
                df = pd.DataFrame(sample_data['records'])
        except:
            sample_data = generate_sample_report_data('customer_analytics', page_size=200)
            df = pd.DataFrame(sample_data['records'])
        
        # Apply filters
        if 'segment_filter' in locals() and segment_filter:
            df = df[df['segment'].isin(segment_filter)]
        if 'min_ltv' in locals() and min_ltv > 0:
            df = df[df['lifetime_value'] >= min_ltv]
    
    elif "Revenue" in report_type:
        try:
            data = fetch_report_data('revenue_breakdown', page_size=500)
            if data and 'data' in data:
                df = data['data']
            else:
                sample_data = generate_sample_report_data('revenue_breakdown', page_size=180)
                df = pd.DataFrame(sample_data['records'])
        except:
            sample_data = generate_sample_report_data('revenue_breakdown', page_size=180)
            df = pd.DataFrame(sample_data['records'])
        
        # Apply filters
        if 'region_filter' in locals() and region_filter:
            df = df[df['region'].isin(region_filter)]
    
    elif "Top Performers" in report_type:
        try:
            df = fetch_top_performers(
                metric='revenue',
                dimension='product',
                limit=50,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d')
            )
            if df is None:
                sample_data = generate_sample_report_data('product_performance', page_size=50)
                df = pd.DataFrame(sample_data['records']).sort_values('revenue', ascending=False)
        except:
            sample_data = generate_sample_report_data('product_performance', page_size=50)
            df = pd.DataFrame(sample_data['records']).sort_values('revenue', ascending=False)
    
    else:  # KPI Summary
        try:
            kpi_data = fetch_kpi_overview(
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d')
            )
            if kpi_data is None:
                kpi_data = generate_sample_kpi_overview()
        except:
            kpi_data = generate_sample_kpi_overview()
        
        # Convert KPI data to DataFrame
        records = []
        for category, metrics in kpi_data.items():
            if isinstance(metrics, dict) and category != 'period':
                for metric, value in metrics.items():
                    records.append({
                        'Category': category.capitalize(),
                        'Metric': metric.replace('_', ' ').title(),
                        'Value': value
                    })
        
        df = pd.DataFrame(records)
    
    return df


# Load data
with st.spinner("Loading report data..."):
    report_data = load_report_data(report_type)

# Display report-specific visualizations and summary
if not report_data.empty:
    
    # Summary metrics at the top
    st.markdown("### 📊 Quick Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Records",
            f"{len(report_data):,}",
            help="Total number of records in this report"
        )
    
    with col2:
        if "revenue" in report_data.columns:
            total_revenue = report_data["revenue"].sum()
            st.metric(
                "Total Revenue",
                f"${total_revenue:,.2f}",
                help="Sum of all revenue in the filtered data"
            )
        elif "lifetime_value" in report_data.columns:
            total_ltv = report_data["lifetime_value"].sum()
            st.metric(
                "Total LTV",
                f"${total_ltv:,.2f}",
                help="Sum of customer lifetime values"
            )
        else:
            st.metric("Data Points", f"{len(report_data.columns)}")
    
    with col3:
        if "profit" in report_data.columns:
            total_profit = report_data["profit"].sum()
            st.metric(
                "Total Profit",
                f"${total_profit:,.2f}",
                help="Sum of all profit in the filtered data"
            )
        elif "units_sold" in report_data.columns:
            total_units = report_data["units_sold"].sum()
            st.metric(
                "Total Units",
                f"{total_units:,.0f}",
                help="Total units sold"
            )
        else:
            st.metric("Unique Values", f"{report_data.iloc[:, 0].nunique()}")
    
    with col4:
        if "revenue" in report_data.columns:
            avg_revenue = report_data["revenue"].mean()
            st.metric(
                "Average Revenue",
                f"${avg_revenue:,.2f}",
                help="Average revenue per record"
            )
        elif "profit_margin" in report_data.columns:
            avg_margin = report_data["profit_margin"].mean()
            st.metric(
                "Avg Margin",
                f"{avg_margin:.2f}%",
                help="Average profit margin"
            )
        else:
            st.metric("Categories", f"{report_data.iloc[:, 0].nunique()}")
    
    st.markdown("---")
    
    # Visualization based on report type
    st.markdown("### 📈 Visual Analysis")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        if "Sales" in report_type and "date" in report_data.columns and "revenue" in report_data.columns:
            # Revenue trend
            daily_revenue = report_data.groupby("date")["revenue"].sum().reset_index()
            fig = px.line(
                daily_revenue,
                x="date",
                y="revenue",
                title="Revenue Trend Over Time",
                labels={"revenue": "Revenue ($)", "date": "Date"}
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        elif "Product" in report_type and "category" in report_data.columns:
            # Category distribution
            category_revenue = report_data.groupby("category")["revenue"].sum().reset_index()
            fig = px.bar(
                category_revenue,
                x="category",
                y="revenue",
                title="Revenue by Category",
                labels={"revenue": "Revenue ($)", "category": "Category"}
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        elif "Customer" in report_type and "segment" in report_data.columns:
            # Segment distribution
            segment_counts = report_data["segment"].value_counts().reset_index()
            segment_counts.columns = ["segment", "count"]
            fig = px.pie(
                segment_counts,
                values="count",
                names="segment",
                title="Customer Segment Distribution"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        elif "Revenue" in report_type and "region" in report_data.columns:
            # Regional revenue
            regional_revenue = report_data.groupby("region")["revenue"].sum().reset_index()
            fig = px.bar(
                regional_revenue,
                x="region",
                y="revenue",
                title="Revenue by Region",
                labels={"revenue": "Revenue ($)", "region": "Region"}
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with viz_col2:
        if "profit" in report_data.columns and "revenue" in report_data.columns:
            # Profit vs Revenue scatter
            fig = px.scatter(
                report_data.head(100),
                x="revenue",
                y="profit",
                title="Profit vs Revenue Analysis",
                labels={"revenue": "Revenue ($)", "profit": "Profit ($)"},
                trendline="ols"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        elif "Product" in report_type and "profit_margin" in report_data.columns:
            # Profit margin distribution
            fig = px.histogram(
                report_data,
                x="profit_margin",
                title="Profit Margin Distribution",
                labels={"profit_margin": "Profit Margin (%)"}
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        elif "Customer" in report_type and "orders_count" in report_data.columns:
            # Orders distribution
            fig = px.histogram(
                report_data,
                x="orders_count",
                title="Customer Order Frequency",
                labels={"orders_count": "Number of Orders"}
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        elif "Revenue" in report_type and "margin" in report_data.columns:
            # Margin trend
            margin_by_date = report_data.groupby("date")["margin"].mean().reset_index()
            fig = px.line(
                margin_by_date,
                x="date",
                y="margin",
                title="Average Margin Trend",
                labels={"margin": "Margin (%)", "date": "Date"}
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Interactive data table
    st.markdown("### 📋 Detailed Data Table")
    
    # Configure custom formatters
    formatters = {}
    conditional_formatting = {}
    
    if "revenue" in report_data.columns:
        formatters["revenue"] = lambda x: f"${x:,.2f}"
    if "profit" in report_data.columns:
        formatters["profit"] = lambda x: f"${x:,.2f}"
        conditional_formatting["profit"] = color_negative_red
    if "profit_margin" in report_data.columns:
        formatters["profit_margin"] = lambda x: f"{x:.2f}%"
    if "lifetime_value" in report_data.columns:
        formatters["lifetime_value"] = lambda x: f"${x:,.2f}"
    
    # Display interactive table
    filtered_data, metadata = create_interactive_table(
        data=report_data,
        key_prefix=f"report_{report_type.replace(' ', '_')}",
        title=None,
        page_size=25,
        show_search=True,
        show_filters=True,
        show_export=True,
        show_column_selector=True,
        sortable=True,
        custom_formatters=formatters,
        conditional_formatting=conditional_formatting,
        summary_stats=True
    )
    
    # Display table metadata
    st.markdown("---")
    st.markdown("### ℹ️ Table Information")
    
    info_col1, info_col2, info_col3 = st.columns(3)
    
    with info_col1:
        st.info(f"**Total Rows:** {metadata['total_rows']:,}")
    
    with info_col2:
        st.info(f"**Filtered Rows:** {metadata['filtered_rows']:,}")
    
    with info_col3:
        st.info(f"**Visible Columns:** {len(metadata['visible_columns'])}")

else:
    st.warning("⚠️ No data available for the selected filters. Please adjust your filter settings.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>KPI Intelligence & Reporting Platform</strong></p>
    <p>Production-level business intelligence with real-time data analysis</p>
    <p style='font-size: 0.9rem;'>Last updated: {}</p>
</div>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)
