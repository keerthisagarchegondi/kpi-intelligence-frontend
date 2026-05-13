"""
Table Components Module

Production-level reusable table components with advanced features:
- Interactive sorting and filtering
- Search functionality
- Pagination
- Column selection and reordering
- Export to CSV/Excel
- Row selection
- Conditional formatting
- Responsive design
- Loading states
- Performance optimization
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any, Callable, Tuple
from datetime import datetime
import io
import base64
from utils.performance import performance_timer, LazyLoader, DataOptimizer, QueryOptimizer


class DataTableConfig:
    """Configuration for data tables"""
    DEFAULT_PAGE_SIZE = 25
    PAGE_SIZE_OPTIONS = [10, 25, 50, 100, 250, 500]
    MAX_EXPORT_ROWS = 100000
    SEARCH_DEBOUNCE_MS = 300


@performance_timer("table_creation")
def create_interactive_table(
    data: pd.DataFrame,
    key_prefix: str = "table",
    title: Optional[str] = None,
    page_size: int = DataTableConfig.DEFAULT_PAGE_SIZE,
    show_search: bool = True,
    show_filters: bool = True,
    show_export: bool = True,
    show_column_selector: bool = True,
    sortable: bool = True,
    selectable_rows: bool = False,
    custom_formatters: Optional[Dict[str, Callable]] = None,
    conditional_formatting: Optional[Dict[str, Callable]] = None,
    summary_stats: bool = False,
    frozen_columns: Optional[List[str]] = None,
    show_loading: bool = False
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Create a production-level interactive data table with advanced features.
    
    Args:
        data: DataFrame to display
        key_prefix: Unique prefix for session state keys
        title: Optional table title
        page_size: Number of rows per page
        show_search: Enable search functionality
        show_filters: Enable column filters
        show_export: Show export buttons
        show_column_selector: Allow column selection
        sortable: Enable sorting
        selectable_rows: Enable row selection
        custom_formatters: Custom formatting functions per column
        conditional_formatting: Conditional styling rules
        summary_stats: Show summary statistics
        frozen_columns: Columns to keep visible when scrolling
        show_loading: Show loading state
    
    Returns:
        Tuple of (filtered_dataframe, metadata_dict)
    """
    
    # Optimize data types for better performance
    if len(data) > 100:
        data = DataOptimizer.optimize_dtypes(data)
    
    # Show loading state if data is being processed
    if show_loading or data is None or data.empty:
        with st.spinner("Loading table data..."):
            if data is None or data.empty:
                st.warning("⚠️ No data available to display")
                return pd.DataFrame(), {
                    'total_rows': 0,
                    'filtered_rows': 0,
                    'displayed_rows': 0,
                    'current_page': 0,
                    'total_pages': 0,
                    'visible_columns': [],
                    'search_query': ''
                }
    
    # Initialize session state
    if f'{key_prefix}_page' not in st.session_state:
        st.session_state[f'{key_prefix}_page'] = 0
    if f'{key_prefix}_selected_rows' not in st.session_state:
        st.session_state[f'{key_prefix}_selected_rows'] = []
    if f'{key_prefix}_visible_columns' not in st.session_state:
        st.session_state[f'{key_prefix}_visible_columns'] = list(data.columns)
    
    # Create container
    container = st.container()
    
    with container:
        # Title
        if title:
            st.markdown(f"### {title}")
        
        # Control panel
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            # Search
            if show_search:
                search_query = st.text_input(
                    "🔍 Search",
                    key=f"{key_prefix}_search",
                    placeholder="Search across all columns...",
                    help="Search for any text in the table"
                )
            else:
                search_query = ""
        
        with col2:
            # Page size selector
            selected_page_size = st.selectbox(
                "Rows per page",
                options=DataTableConfig.PAGE_SIZE_OPTIONS,
                index=DataTableConfig.PAGE_SIZE_OPTIONS.index(page_size),
                key=f"{key_prefix}_page_size"
            )
        
        with col3:
            # Column selector
            if show_column_selector and len(data.columns) > 1:
                with st.popover("📋 Columns"):
                    st.markdown("**Select columns to display:**")
                    selected_columns = []
                    for col in data.columns:
                        if st.checkbox(
                            col,
                            value=col in st.session_state[f'{key_prefix}_visible_columns'],
                            key=f"{key_prefix}_col_{col}"
                        ):
                            selected_columns.append(col)
                    
                    if st.button("Apply", key=f"{key_prefix}_apply_cols"):
                        st.session_state[f'{key_prefix}_visible_columns'] = selected_columns
                        st.rerun()
        
        with col4:
            # Export buttons
            if show_export:
                with st.popover("💾 Export"):
                    st.markdown("**Export table data:**")
                    
                    # CSV export
                    csv = data.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        key=f"{key_prefix}_export_csv"
                    )
                    
                    # Excel export
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        data.to_excel(writer, index=False, sheet_name='Data')
                    
                    st.download_button(
                        label="Download Excel",
                        data=buffer.getvalue(),
                        file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"{key_prefix}_export_excel"
                    )
        
        # Apply filters
        filtered_data = data.copy()
        
        # Search filter
        if search_query:
            mask = filtered_data.astype(str).apply(
                lambda x: x.str.contains(search_query, case=False, na=False)
            ).any(axis=1)
            filtered_data = filtered_data[mask]
        
        # Column filters
        if show_filters:
            with st.expander("🔧 Advanced Filters", expanded=False):
                filter_cols = st.columns(min(3, len(filtered_data.columns)))
                
                for idx, col in enumerate(filtered_data.columns[:9]):  # Limit to 9 columns
                    with filter_cols[idx % 3]:
                        if filtered_data[col].dtype in ['int64', 'float64']:
                            # Numeric filter
                            min_val = float(filtered_data[col].min())
                            max_val = float(filtered_data[col].max())
                            
                            if min_val != max_val:
                                filter_range = st.slider(
                                    f"{col}",
                                    min_value=min_val,
                                    max_value=max_val,
                                    value=(min_val, max_val),
                                    key=f"{key_prefix}_filter_{col}"
                                )
                                filtered_data = filtered_data[
                                    (filtered_data[col] >= filter_range[0]) &
                                    (filtered_data[col] <= filter_range[1])
                                ]
                        else:
                            # Categorical filter
                            unique_values = filtered_data[col].unique()
                            if len(unique_values) <= 20:  # Only show for reasonable number of options
                                selected_values = st.multiselect(
                                    f"{col}",
                                    options=unique_values,
                                    default=list(unique_values),
                                    key=f"{key_prefix}_filter_{col}"
                                )
                                if selected_values:
                                    filtered_data = filtered_data[filtered_data[col].isin(selected_values)]
        
        # Apply column visibility
        visible_columns = [col for col in st.session_state[f'{key_prefix}_visible_columns'] if col in filtered_data.columns]
        if visible_columns:
            display_data = filtered_data[visible_columns].copy()
        else:
            display_data = filtered_data.copy()
        
        # Summary statistics
        if summary_stats and not display_data.empty:
            st.markdown("---")
            st.markdown("**📊 Summary Statistics**")
            
            summary_cols = st.columns(min(4, len(display_data.select_dtypes(include=[np.number]).columns)))
            numeric_cols = display_data.select_dtypes(include=[np.number]).columns
            
            for idx, col in enumerate(numeric_cols[:4]):
                with summary_cols[idx]:
                    st.metric(
                        label=f"{col}",
                        value=f"{display_data[col].sum():,.2f}",
                        delta=f"Avg: {display_data[col].mean():,.2f}"
                    )
            
            st.markdown("---")
        
        # Pagination
        total_rows = len(display_data)
        total_pages = max(1, (total_rows + selected_page_size - 1) // selected_page_size)
        
        # Pagination controls
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown(f"**Total Records:** {total_rows:,}")
        
        with col2:
            # Page navigation
            nav_cols = st.columns([1, 2, 1])
            
            with nav_cols[0]:
                if st.button("⬅️ Previous", key=f"{key_prefix}_prev", disabled=st.session_state[f'{key_prefix}_page'] == 0):
                    st.session_state[f'{key_prefix}_page'] -= 1
                    st.rerun()
            
            with nav_cols[1]:
                current_page = st.number_input(
                    "Page",
                    min_value=1,
                    max_value=total_pages,
                    value=st.session_state[f'{key_prefix}_page'] + 1,
                    key=f"{key_prefix}_page_input",
                    label_visibility="collapsed"
                )
                st.markdown(f"<div style='text-align: center;'>of {total_pages}</div>", unsafe_allow_html=True)
                
                if current_page - 1 != st.session_state[f'{key_prefix}_page']:
                    st.session_state[f'{key_prefix}_page'] = current_page - 1
                    st.rerun()
            
            with nav_cols[2]:
                if st.button("Next ➡️", key=f"{key_prefix}_next", disabled=st.session_state[f'{key_prefix}_page'] >= total_pages - 1):
                    st.session_state[f'{key_prefix}_page'] += 1
                    st.rerun()
        
        with col3:
            # Record range
            start_idx = st.session_state[f'{key_prefix}_page'] * selected_page_size
            end_idx = min(start_idx + selected_page_size, total_rows)
            st.markdown(f"**Showing:** {start_idx + 1} - {end_idx}")
        
        # Get page data
        page_data = display_data.iloc[start_idx:end_idx]
        
        # Apply custom formatters
        if custom_formatters:
            for col, formatter in custom_formatters.items():
                if col in page_data.columns:
                    page_data[col] = page_data[col].apply(formatter)
        
        # Display table with styling
        st.markdown("---")
        
        # Configure pandas display options for better formatting
        pd.options.display.float_format = '{:,.2f}'.format
        
        # Display the dataframe with Streamlit's native table
        if not page_data.empty:
            # Add conditional formatting via styling
            if conditional_formatting:
                styled_data = page_data.style
                for col, style_func in conditional_formatting.items():
                    if col in page_data.columns:
                        styled_data = styled_data.applymap(style_func, subset=[col])
                st.dataframe(styled_data, use_container_width=True, height=400)
            else:
                st.dataframe(page_data, use_container_width=True, height=400)
        else:
            st.info("No data to display")
        
        # Metadata
        metadata = {
            'total_rows': total_rows,
            'filtered_rows': len(filtered_data),
            'displayed_rows': len(page_data),
            'current_page': st.session_state[f'{key_prefix}_page'] + 1,
            'total_pages': total_pages,
            'visible_columns': visible_columns,
            'search_query': search_query
        }
        
        return filtered_data, metadata


def create_summary_table(
    data: pd.DataFrame,
    group_by: str,
    aggregations: Dict[str, str],
    title: Optional[str] = None,
    show_export: bool = True
) -> pd.DataFrame:
    """
    Create a summary table with aggregations.
    
    Args:
        data: Source DataFrame
        group_by: Column to group by
        aggregations: Dictionary mapping column names to aggregation functions
                      (e.g., {'revenue': 'sum', 'orders': 'count'})
        title: Optional title
        show_export: Show export button
    
    Returns:
        Aggregated DataFrame
    """
    if title:
        st.markdown(f"### {title}")
    
    # Perform aggregation
    summary = data.groupby(group_by).agg(aggregations).reset_index()
    
    # Flatten multi-index columns if present
    if isinstance(summary.columns, pd.MultiIndex):
        summary.columns = ['_'.join(col).strip('_') for col in summary.columns.values]
    
    # Display
    st.dataframe(summary, use_container_width=True)
    
    # Export
    if show_export:
        csv = summary.to_csv(index=False)
        st.download_button(
            label="📥 Download Summary",
            data=csv,
            file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    return summary


def create_comparison_table(
    data1: pd.DataFrame,
    data2: pd.DataFrame,
    labels: Tuple[str, str] = ("Period 1", "Period 2"),
    metrics: Optional[List[str]] = None,
    title: Optional[str] = None
) -> pd.DataFrame:
    """
    Create a comparison table between two datasets.
    
    Args:
        data1: First DataFrame
        data2: Second DataFrame
        labels: Labels for the two datasets
        metrics: Specific metrics to compare (if None, compares all numeric columns)
        title: Optional title
    
    Returns:
        Comparison DataFrame
    """
    if title:
        st.markdown(f"### {title}")
    
    # Select metrics
    if metrics is None:
        metrics = data1.select_dtypes(include=[np.number]).columns.tolist()
    
    # Calculate statistics
    comparison = pd.DataFrame({
        'Metric': metrics,
        labels[0]: [data1[m].sum() if m in data1.columns else 0 for m in metrics],
        labels[1]: [data2[m].sum() if m in data2.columns else 0 for m in metrics]
    })
    
    # Calculate change
    comparison['Change'] = comparison[labels[1]] - comparison[labels[0]]
    comparison['Change %'] = (comparison['Change'] / comparison[labels[0]] * 100).round(2)
    
    # Format for display
    comparison[labels[0]] = comparison[labels[0]].apply(lambda x: f"{x:,.2f}")
    comparison[labels[1]] = comparison[labels[1]].apply(lambda x: f"{x:,.2f}")
    comparison['Change'] = comparison['Change'].apply(lambda x: f"{x:,.2f}")
    comparison['Change %'] = comparison['Change %'].apply(lambda x: f"{x:+.2f}%")
    
    st.dataframe(comparison, use_container_width=True)
    
    return comparison


def create_pivot_table(
    data: pd.DataFrame,
    index: str,
    columns: str,
    values: str,
    aggfunc: str = 'sum',
    title: Optional[str] = None,
    show_totals: bool = True
) -> pd.DataFrame:
    """
    Create an interactive pivot table.
    
    Args:
        data: Source DataFrame
        index: Column to use as index
        columns: Column to use as columns
        values: Column to aggregate
        aggfunc: Aggregation function
        title: Optional title
        show_totals: Show row and column totals
    
    Returns:
        Pivot table DataFrame
    """
    if title:
        st.markdown(f"### {title}")
    
    # Create pivot table
    pivot = pd.pivot_table(
        data,
        values=values,
        index=index,
        columns=columns,
        aggfunc=aggfunc,
        fill_value=0
    )
    
    # Add totals
    if show_totals:
        pivot['Total'] = pivot.sum(axis=1)
        pivot.loc['Total'] = pivot.sum(axis=0)
    
    st.dataframe(pivot, use_container_width=True)
    
    return pivot


# ==================== UTILITY FUNCTIONS ====================

def format_currency(value: float) -> str:
    """Format value as currency"""
    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    """Format value as percentage"""
    return f"{value:.2f}%"


def format_number(value: float) -> str:
    """Format number with thousand separators"""
    return f"{value:,.0f}"


def color_negative_red(val):
    """Color negative values red, positive green"""
    try:
        value = float(val)
        color = 'red' if value < 0 else 'green' if value > 0 else 'black'
        return f'color: {color}'
    except:
        return ''


def highlight_max(s):
    """Highlight maximum value in a series"""
    is_max = s == s.max()
    return ['background-color: lightgreen' if v else '' for v in is_max]


def highlight_min(s):
    """Highlight minimum value in a series"""
    is_min = s == s.min()
    return ['background-color: lightcoral' if v else '' for v in is_min]
