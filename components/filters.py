"""
Filter Components Module
Provides reusable filter UI components for the KPI Intelligence Platform
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Tuple, Optional


def render_date_range_filter(
    key_prefix: str = "default",
    default_range: str = "Last 30 Days",
    show_apply_button: bool = True
) -> Tuple[datetime, datetime, bool]:
    """
    Render a production-ready date range filter with predefined and custom options.
    
    Args:
        key_prefix: Unique prefix for session state keys to avoid conflicts
        default_range: Default date range option
        show_apply_button: Whether to show an apply button for filters
        
    Returns:
        Tuple of (start_date, end_date, filters_applied)
    """
    
    # Define predefined date range options
    date_range_options = {
        "Last 7 Days": 7,
        "Last 30 Days": 30,
        "Last 90 Days": 90,
        "Last 6 Months": 180,
        "Last Year": 365,
        "Custom Range": None
    }
    
    # Initialize session state for filter persistence
    if f"{key_prefix}_filters_applied" not in st.session_state:
        st.session_state[f"{key_prefix}_filters_applied"] = False
    
    # Create filter container with styling
    with st.container():
        st.markdown("### 📅 Date Range Filter")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Date range selection
            selected_range = st.selectbox(
                "Select Date Range",
                options=list(date_range_options.keys()),
                index=list(date_range_options.keys()).index(default_range),
                key=f"{key_prefix}_date_range_select",
                help="Choose a predefined date range or select 'Custom Range' for specific dates"
            )
        
        # Calculate date range based on selection
        today = datetime.now()
        
        if selected_range == "Custom Range":
            # Custom date picker
            col_start, col_end = st.columns(2)
            
            with col_start:
                start_date = st.date_input(
                    "Start Date",
                    value=today - timedelta(days=30),
                    max_value=today,
                    key=f"{key_prefix}_start_date",
                    help="Select the start date for your analysis"
                )
            
            with col_end:
                end_date = st.date_input(
                    "End Date",
                    value=today,
                    max_value=today,
                    key=f"{key_prefix}_end_date",
                    help="Select the end date for your analysis"
                )
            
            # Convert date to datetime
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())
            
            # Validate date range
            if start_date > end_date:
                st.error("⚠️ Start date cannot be after end date. Please adjust your selection.")
                # Use safe default
                end_datetime = start_datetime + timedelta(days=1)
        else:
            # Calculate dates for predefined ranges
            days_back = date_range_options[selected_range]
            start_datetime = today - timedelta(days=days_back)
            end_datetime = today
            
            # Display selected range info
            st.info(f"📊 Showing data from **{start_datetime.strftime('%B %d, %Y')}** to **{end_datetime.strftime('%B %d, %Y')}**")
        
        # Apply button and filter state management
        filters_applied = False
        
        if show_apply_button:
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
            
            with col_btn1:
                if st.button("🔍 Apply Filters", key=f"{key_prefix}_apply_btn", type="primary"):
                    st.session_state[f"{key_prefix}_filters_applied"] = True
                    filters_applied = True
                    st.success("✅ Filters applied successfully!")
            
            with col_btn2:
                if st.button("🔄 Reset", key=f"{key_prefix}_reset_btn"):
                    st.session_state[f"{key_prefix}_filters_applied"] = False
                    filters_applied = False
                    st.rerun()
            
            filters_applied = st.session_state[f"{key_prefix}_filters_applied"]
        else:
            # Auto-apply filters without button
            filters_applied = True
        
        st.markdown("---")
    
    return start_datetime, end_datetime, filters_applied


def render_metric_filters(
    key_prefix: str = "default",
    available_metrics: Optional[list] = None
) -> dict:
    """
    Render metric-specific filters (optional enhancement for future use).
    
    Args:
        key_prefix: Unique prefix for session state keys
        available_metrics: List of available metrics to filter by
        
    Returns:
        Dictionary of selected filter values
    """
    if available_metrics is None:
        available_metrics = ["Revenue", "Retention", "Churn", "Active Users"]
    
    st.markdown("### 🎯 Metric Filters")
    
    selected_metrics = st.multiselect(
        "Select Metrics to Display",
        options=available_metrics,
        default=available_metrics,
        key=f"{key_prefix}_metric_select",
        help="Choose which metrics to display in your dashboard"
    )
    
    return {
        "selected_metrics": selected_metrics
    }


def render_comparison_filter(key_prefix: str = "default") -> Tuple[bool, str]:
    """
    Render period comparison filter for trend analysis.
    
    Args:
        key_prefix: Unique prefix for session state keys
        
    Returns:
        Tuple of (enable_comparison, comparison_period)
    """
    st.markdown("### 📊 Comparison Options")
    
    enable_comparison = st.checkbox(
        "Enable Period Comparison",
        value=False,
        key=f"{key_prefix}_enable_comparison",
        help="Compare current period with a previous period"
    )
    
    comparison_period = "Previous Period"
    if enable_comparison:
        comparison_period = st.selectbox(
            "Compare With",
            options=["Previous Period", "Previous Year", "Previous Quarter"],
            key=f"{key_prefix}_comparison_period",
            help="Select the comparison period for trend analysis"
        )
    
    return enable_comparison, comparison_period


def get_filter_summary(start_date: datetime, end_date: datetime, additional_info: str = "") -> str:
    """
    Generate a summary string of applied filters for display.
    
    Args:
        start_date: Filter start date
        end_date: Filter end date
        additional_info: Additional filter information
        
    Returns:
        Formatted filter summary string
    """
    days_diff = (end_date - start_date).days
    summary = f"**Date Range:** {start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')} ({days_diff} days)"
    
    if additional_info:
        summary += f" | {additional_info}"
    
    return summary
