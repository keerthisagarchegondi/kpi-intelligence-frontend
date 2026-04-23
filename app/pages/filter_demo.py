import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from components.filters import (
    render_date_range_filter, 
    get_filter_summary,
    render_metric_filters,
    render_comparison_filter
)

# Page configuration
st.set_page_config(
    page_title="Filter Demo - KPI Intelligence",
    page_icon="🎨",
    layout="wide"
)

# Page title
st.title("🎨 Filter Components Demo")
st.markdown("---")

st.markdown("""
This page demonstrates all available production-level filter components.
These components are reusable across all dashboard pages.
""")

st.markdown("---")

# Demo 1: Date Range Filter with Apply Button
st.header("1️⃣ Date Range Filter (with Apply Button)")
st.code("""
start_date, end_date, filters_applied = render_date_range_filter(
    key_prefix="demo1",
    default_range="Last 30 Days",
    show_apply_button=True
)
""", language="python")

start_date1, end_date1, filters_applied1 = render_date_range_filter(
    key_prefix="demo1",
    default_range="Last 30 Days",
    show_apply_button=True
)

if filters_applied1:
    st.success(f"✅ Filters Applied! Date range: {start_date1.date()} to {end_date1.date()}")

st.markdown("---")

# Demo 2: Date Range Filter (Auto-apply)
st.header("2️⃣ Date Range Filter (Auto-apply)")
st.code("""
start_date, end_date, filters_applied = render_date_range_filter(
    key_prefix="demo2",
    default_range="Last 7 Days",
    show_apply_button=False
)
""", language="python")

start_date2, end_date2, filters_applied2 = render_date_range_filter(
    key_prefix="demo2",
    default_range="Last 7 Days",
    show_apply_button=False
)

st.info(f"📅 Auto-applied: {start_date2.date()} to {end_date2.date()}")

st.markdown("---")

# Demo 3: Comparison Filter
st.header("3️⃣ Comparison Filter")
st.code("""
enable_comparison, comparison_period = render_comparison_filter(
    key_prefix="demo3"
)
""", language="python")

enable_comparison, comparison_period = render_comparison_filter(
    key_prefix="demo3"
)

if enable_comparison:
    st.success(f"📊 Comparison enabled with: {comparison_period}")
else:
    st.info("Comparison is disabled")

st.markdown("---")

# Demo 4: Metric Filters
st.header("4️⃣ Metric Filters")
st.code("""
metric_filters = render_metric_filters(
    key_prefix="demo4",
    available_metrics=["Revenue", "Retention", "Churn", "Active Users", "Conversion Rate"]
)
""", language="python")

metric_filters = render_metric_filters(
    key_prefix="demo4",
    available_metrics=["Revenue", "Retention", "Churn", "Active Users", "Conversion Rate"]
)

st.success(f"✅ Selected Metrics: {', '.join(metric_filters['selected_metrics'])}")

st.markdown("---")

# Demo 5: Filter Summary
st.header("5️⃣ Filter Summary Helper")
st.code("""
summary = get_filter_summary(
    start_date, 
    end_date, 
    additional_info="Segment: Enterprise | Region: APAC"
)
""", language="python")

summary = get_filter_summary(
    start_date1, 
    end_date1, 
    additional_info="Segment: Enterprise | Region: APAC"
)

st.markdown(summary)

st.markdown("---")

# Integration Example
st.header("🔧 Full Integration Example")
st.markdown("""
Here's how to integrate filters in your dashboard pages:

```python
# In your dashboard page (e.g., dashboard.py)
from components.filters import render_date_range_filter, get_filter_summary

# Render filters
with st.expander("🔧 Filters", expanded=True):
    start_date, end_date, filters_applied = render_date_range_filter(
        key_prefix="my_page",
        default_range="Last 30 Days"
    )

# Use filter values
if filters_applied:
    st.markdown(get_filter_summary(start_date, end_date))
    
    # Your data fetching with date range
    data = fetch_data(start_date, end_date)
    
    # Your visualizations
    st.line_chart(data)
```
""")

st.markdown("---")

# Features Summary
st.header("✨ Key Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🎯 Smart Defaults**
    - Predefined date ranges
    - Sensible default values
    - Auto-validation
    """)

with col2:
    st.markdown("""
    **🔄 State Management**
    - Session persistence
    - Unique key prefixes
    - Apply/Reset functionality
    """)

with col3:
    st.markdown("""
    **✅ Production-Ready**
    - Type hints
    - Error handling
    - Documentation
    """)
