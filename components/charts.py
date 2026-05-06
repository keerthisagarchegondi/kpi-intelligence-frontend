"""
Chart Components Module

This module provides reusable chart components for the KPI Intelligence Platform.
All functions return Plotly figure objects that can be rendered in Streamlit.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Union, Tuple


# ==================== STATIC SAMPLE DATA GENERATORS ====================

def generate_time_series_data(
    days: int = 30,
    metric_name: str = "value",
    start_value: float = 100,
    trend: float = 0.5,
    noise: float = 10
) -> pd.DataFrame:
    """
    Generate realistic time series data with consistent patterns for demos.
    
    Args:
        days: Number of days of data to generate
        metric_name: Name of the metric column
        start_value: Starting value for the metric
        trend: Daily trend (positive = upward, negative = downward)
        noise: Amount of random noise to add
    
    Returns:
        DataFrame with date and metric columns
    """
    dates = pd.date_range(end=datetime(2026, 5, 2), periods=days, freq='D')
    
    # Create realistic business patterns: weekly seasonality + growth trend
    values = []
    for i in range(days):
        # Base trend
        base = start_value + i * trend
        # Weekly pattern (lower on weekends)
        day_of_week = dates[i].dayofweek
        weekly_factor = 1.0 if day_of_week < 5 else 0.7  # Weekday vs Weekend
        # Add controlled variation
        variation = np.sin(i / 7 * 2 * np.pi) * noise * 0.3
        values.append(base * weekly_factor + variation)
    
    return pd.DataFrame({'date': dates, metric_name: values})


def generate_categorical_data(
    categories: List[str],
    min_value: float = 10,
    max_value: float = 100
) -> pd.DataFrame:
    """
    Generate realistic categorical data with business-appropriate distributions.
    
    Args:
        categories: List of category names
        min_value: Minimum value for data
        max_value: Maximum value for data
    
    Returns:
        DataFrame with category and value columns
    """
    # Create Pareto-like distribution (80/20 rule) for realistic business data
    n = len(categories)
    ranks = np.arange(1, n + 1)
    # Pareto distribution: values decrease exponentially
    values = max_value * (1 / ranks) ** 0.7
    # Ensure minimum value
    values = np.maximum(values, min_value)
    
    return pd.DataFrame({'category': categories, 'value': values})


def generate_multi_series_data(
    days: int = 30,
    series_names: List[str] = None,
    base_value: float = 100
) -> pd.DataFrame:
    """
    Generate realistic multi-series time data with coordinated patterns.
    
    Args:
        days: Number of days of data
        series_names: List of series names
        base_value: Base value for all series
    
    Returns:
        DataFrame with date column and columns for each series
    """
    if series_names is None:
        series_names = ['Series A', 'Series B', 'Series C']
    
    dates = pd.date_range(end=datetime(2026, 5, 2), periods=days, freq='D')
    data = {'date': dates}
    
    # Create coordinated series with realistic relationships
    for idx, name in enumerate(series_names):
        values = []
        phase_shift = idx * np.pi / 4  # Different phases for each series
        trend_factor = 1.0 + (idx * 0.1)  # Slightly different growth rates
        
        for i in range(days):
            # Growth trend
            trend = base_value * trend_factor + i * 0.5
            # Seasonal pattern
            seasonal = 10 * np.sin(i / 7 * 2 * np.pi + phase_shift)
            # Weekly pattern
            day_of_week = dates[i].dayofweek
            weekly_factor = 1.0 if day_of_week < 5 else 0.75
            
            values.append((trend + seasonal) * weekly_factor)
        
        data[name] = values
    
    return pd.DataFrame(data)


# ==================== BUSINESS KPI SAMPLE DATA ====================

def get_revenue_sample_data(period: str = '30d') -> pd.DataFrame:
    """
    Get realistic revenue sample data for demonstrations.
    
    Args:
        period: Time period ('30d', '90d', '12m')
    
    Returns:
        DataFrame with date and revenue metrics
    """
    if period == '12m':
        # Monthly data for 12 months
        dates = pd.date_range(end=datetime(2026, 5, 1), periods=12, freq='MS')
        revenue = [245000, 258000, 267000, 285000, 293000, 310000, 
                  325000, 342000, 338000, 356000, 371000, 385000]
        cost = [r * 0.65 for r in revenue]
        profit = [r - c for r, c in zip(revenue, cost)]
    elif period == '90d':
        # Daily data for 90 days
        dates = pd.date_range(end=datetime(2026, 5, 2), periods=90, freq='D')
        base_revenue = 12000
        revenue = []
        for i, date in enumerate(dates):
            day_factor = 1.0 if date.dayofweek < 5 else 0.6
            trend = base_revenue * (1 + i * 0.002)
            seasonal = 1000 * np.sin(i / 7 * 2 * np.pi)
            revenue.append((trend + seasonal) * day_factor)
        cost = [r * 0.67 for r in revenue]
        profit = [r - c for r, c in zip(revenue, cost)]
    else:  # 30d default
        dates = pd.date_range(end=datetime(2026, 5, 2), periods=30, freq='D')
        base_revenue = 12500
        revenue = []
        for i, date in enumerate(dates):
            day_factor = 1.0 if date.dayofweek < 5 else 0.55
            trend = base_revenue * (1 + i * 0.003)
            revenue.append(trend * day_factor + np.random.uniform(-500, 500))
        cost = [r * 0.66 for r in revenue]
        profit = [r - c for r, c in zip(revenue, cost)]
    
    return pd.DataFrame({
        'date': dates,
        'revenue': revenue,
        'cost': cost,
        'profit': profit
    })


def get_retention_sample_data() -> pd.DataFrame:
    """
    Get realistic customer retention cohort data.
    
    Returns:
        DataFrame with cohort retention percentages
    """
    cohorts = ['Jan 2026', 'Feb 2026', 'Mar 2026', 'Apr 2026', 'May 2026']
    months = ['Month 0', 'Month 1', 'Month 2', 'Month 3', 'Month 4']
    
    # Realistic retention curve data
    retention_patterns = [
        [100, 85, 72, 65, 60],  # Jan cohort
        [100, 87, 75, 68, None],  # Feb cohort
        [100, 89, 78, None, None],  # Mar cohort
        [100, 91, None, None, None],  # Apr cohort
        [100, None, None, None, None],  # May cohort
    ]
    
    return pd.DataFrame(retention_patterns, index=cohorts, columns=months)


def get_customer_segmentation_data() -> pd.DataFrame:
    """
    Get realistic customer segmentation data.
    
    Returns:
        DataFrame with customer segments and metrics
    """
    segments = ['Enterprise', 'Mid-Market', 'Small Business', 'Startup', 'Free Trial']
    customers = [245, 823, 1547, 2103, 3892]
    revenue = [1250000, 1680000, 890000, 425000, 0]
    avg_order = [5102.04, 2041.07, 575.47, 202.09, 0]
    churn_rate = [3.2, 5.8, 12.5, 18.7, 45.3]
    
    return pd.DataFrame({
        'segment': segments,
        'customers': customers,
        'revenue': revenue,
        'avg_order_value': avg_order,
        'churn_rate': churn_rate
    })


def get_product_performance_data() -> pd.DataFrame:
    """
    Get realistic product performance data.
    
    Returns:
        DataFrame with product metrics
    """
    products = ['Premium Plan', 'Professional Plan', 'Standard Plan', 
               'Basic Plan', 'Add-ons', 'Consulting Services']
    revenue = [1850000, 1420000, 980000, 560000, 320000, 745000]
    units_sold = [1847, 3562, 5234, 8901, 12456, 234]
    growth_rate = [15.3, 22.7, 8.4, -3.2, 31.5, 18.9]
    
    return pd.DataFrame({
        'product': products,
        'revenue': revenue,
        'units_sold': units_sold,
        'growth_rate': growth_rate
    })


def get_channel_performance_data() -> pd.DataFrame:
    """
    Get realistic marketing channel performance data.
    
    Returns:
        DataFrame with channel metrics
    """
    channels = ['Direct Sales', 'Organic Search', 'Paid Ads', 'Referral', 
               'Social Media', 'Email Marketing', 'Partner']
    revenue = [2150000, 1820000, 1340000, 890000, 645000, 523000, 407000]
    conversions = [1245, 2876, 3421, 1567, 2134, 1892, 678]
    cac = [325.50, 125.75, 245.30, 89.40, 178.20, 95.60, 412.80]
    roi = [6.6, 14.5, 5.5, 10.0, 3.6, 5.5, 1.0]
    
    return pd.DataFrame({
        'channel': channels,
        'revenue': revenue,
        'conversions': conversions,
        'cac': cac,
        'roi': roi
    })


def get_regional_performance_data() -> pd.DataFrame:
    """
    Get realistic regional performance data.
    
    Returns:
        DataFrame with regional metrics
    """
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East & Africa']
    revenue = [3250000, 2145000, 1680000, 745000, 455000]
    customers = [4523, 3214, 2867, 1456, 892]
    growth_rate = [12.5, 18.3, 28.7, 22.1, 31.4]
    
    return pd.DataFrame({
        'region': regions,
        'revenue': revenue,
        'customers': customers,
        'growth_rate': growth_rate
    })


def get_daily_metrics_data(days: int = 30) -> pd.DataFrame:
    """
    Get realistic daily operational metrics.
    
    Args:
        days: Number of days of data
    
    Returns:
        DataFrame with daily operational metrics
    """
    dates = pd.date_range(end=datetime(2026, 5, 2), periods=days, freq='D')
    
    data = {
        'date': dates,
        'active_users': [],
        'new_signups': [],
        'revenue': [],
        'support_tickets': [],
        'nps_score': []
    }
    
    for i, date in enumerate(dates):
        # Weekly patterns
        is_weekday = date.dayofweek < 5
        day_factor = 1.0 if is_weekday else 0.6
        
        # Active users with growth trend
        base_users = 15000 + i * 50
        data['active_users'].append(int(base_users * day_factor))
        
        # New signups
        base_signups = 125 + i * 2
        data['new_signups'].append(int(base_signups * day_factor + np.random.randint(-20, 30)))
        
        # Daily revenue
        base_revenue = 12000 + i * 80
        data['revenue'].append(base_revenue * day_factor + np.random.uniform(-800, 800))
        
        # Support tickets (inversely related to quality)
        base_tickets = 85
        data['support_tickets'].append(int(base_tickets * day_factor + np.random.randint(-15, 25)))
        
        # NPS score (stable with slight improvement)
        base_nps = 58 + i * 0.1
        data['nps_score'].append(min(100, base_nps + np.random.uniform(-3, 3)))
    
    return pd.DataFrame(data)


# ==================== LINE CHARTS ====================

def create_line_chart(
    data: pd.DataFrame = None,
    x_column: str = 'date',
    y_column: str = 'value',
    title: str = 'Time Series Chart',
    x_label: str = 'Date',
    y_label: str = 'Value',
    color: str = '#1f77b4',
    height: int = 400,
    show_markers: bool = True,
    fill_area: bool = False
) -> go.Figure:
    """
    Create a line chart with customizable options.
    
    Args:
        data: DataFrame containing the data. If None, generates placeholder data
        x_column: Name of the x-axis column
        y_column: Name of the y-axis column
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        color: Line color
        height: Chart height in pixels
        show_markers: Whether to show data point markers
        fill_area: Whether to fill area under the line
    
    Returns:
        Plotly Figure object
    """
    # Use placeholder data if none provided
    if data is None:
        data = generate_time_series_data(metric_name=y_column)
    
    # Create figure
    fig = go.Figure()
    
    # Add line trace
    mode = 'lines+markers' if show_markers else 'lines'
    fill = 'tozeroy' if fill_area else None
    
    fig.add_trace(go.Scatter(
        x=data[x_column],
        y=data[y_column],
        mode=mode,
        name=y_column,
        line=dict(color=color, width=2),
        marker=dict(size=6),
        fill=fill,
        fillcolor=f'rgba{tuple(list(px.colors.hex_to_rgb(color)) + [0.1])}'
        if fill_area and color.startswith('#') else None
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family="Arial, sans-serif")),
        xaxis_title=x_label,
        yaxis_title=y_label,
        height=height,
        hovermode='x unified',
        template='plotly_white',
        showlegend=False,
        margin=dict(l=60, r=40, t=80, b=60)
    )
    
    return fig


def create_multi_line_chart(
    data: pd.DataFrame = None,
    x_column: str = 'date',
    y_columns: List[str] = None,
    title: str = 'Multi-Series Line Chart',
    x_label: str = 'Date',
    y_label: str = 'Value',
    height: int = 400,
    colors: List[str] = None
) -> go.Figure:
    """
    Create a multi-line chart for comparing multiple metrics.
    
    Args:
        data: DataFrame containing the data. If None, generates placeholder data
        x_column: Name of the x-axis column
        y_columns: List of column names to plot. If None, uses all numeric columns
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        height: Chart height in pixels
        colors: List of colors for each line. If None, uses default color palette
    
    Returns:
        Plotly Figure object
    """
    # Use placeholder data if none provided
    if data is None:
        y_columns = y_columns or ['Metric A', 'Metric B', 'Metric C']
        data = generate_multi_series_data(series_names=y_columns)
    
    # Determine columns to plot
    if y_columns is None:
        y_columns = [col for col in data.columns if col != x_column]
    
    # Use default colors if none provided
    if colors is None:
        colors = px.colors.qualitative.Plotly
    
    # Create figure
    fig = go.Figure()
    
    # Add traces for each series
    for idx, col in enumerate(y_columns):
        fig.add_trace(go.Scatter(
            x=data[x_column],
            y=data[col],
            mode='lines+markers',
            name=col,
            line=dict(color=colors[idx % len(colors)], width=2),
            marker=dict(size=5)
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family="Arial, sans-serif")),
        xaxis_title=x_label,
        yaxis_title=y_label,
        height=height,
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=60, r=40, t=100, b=60)
    )
    
    return fig


# ==================== BAR CHARTS ====================

def create_bar_chart(
    data: pd.DataFrame = None,
    x_column: str = 'category',
    y_column: str = 'value',
    title: str = 'Bar Chart',
    x_label: str = 'Category',
    y_label: str = 'Value',
    orientation: str = 'v',
    color: str = '#636EFA',
    height: int = 400,
    show_values: bool = True
) -> go.Figure:
    """
    Create a bar chart with customizable options.
    
    Args:
        data: DataFrame containing the data. If None, generates placeholder data
        x_column: Name of the x-axis column
        y_column: Name of the y-axis column
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        orientation: 'v' for vertical, 'h' for horizontal
        color: Bar color
        height: Chart height in pixels
        show_values: Whether to show values on bars
    
    Returns:
        Plotly Figure object
    """
    # Use realistic business data if none provided
    if data is None:
        product_data = get_product_performance_data()
        data = pd.DataFrame({
            x_column: product_data['product'],
            y_column: product_data['revenue'] / 1000  # Convert to thousands
        })
    
    # Create figure
    if orientation == 'h':
        fig = go.Figure(go.Bar(
            x=data[y_column],
            y=data[x_column],
            orientation='h',
            marker_color=color,
            text=data[y_column].round(1) if show_values else None,
            textposition='auto'
        ))
    else:
        fig = go.Figure(go.Bar(
            x=data[x_column],
            y=data[y_column],
            marker_color=color,
            text=data[y_column].round(1) if show_values else None,
            textposition='outside'
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family="Arial, sans-serif")),
        xaxis_title=x_label if orientation == 'v' else y_label,
        yaxis_title=y_label if orientation == 'v' else x_label,
        height=height,
        template='plotly_white',
        showlegend=False,
        margin=dict(l=60, r=40, t=80, b=60)
    )
    
    return fig


def create_grouped_bar_chart(
    data: pd.DataFrame = None,
    x_column: str = 'category',
    y_columns: List[str] = None,
    title: str = 'Grouped Bar Chart',
    x_label: str = 'Category',
    y_label: str = 'Value',
    height: int = 400,
    colors: List[str] = None
) -> go.Figure:
    """
    Create a grouped bar chart for comparing multiple metrics across categories.
    
    Args:
        data: DataFrame containing the data. If None, generates placeholder data
        x_column: Name of the x-axis column (categories)
        y_columns: List of column names to plot as separate bar groups
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        height: Chart height in pixels
        colors: List of colors for each bar group
    
    Returns:
        Plotly Figure object
    """
    # Use realistic business data if none provided
    if data is None:
        y_columns = y_columns or ['Revenue', 'Cost', 'Profit']
        revenue_data = get_revenue_sample_data('12m')
        # Aggregate by quarter
        revenue_data['quarter'] = pd.PeriodIndex(revenue_data['date'], freq='Q')
        grouped = revenue_data.groupby('quarter').sum(numeric_only=True).reset_index()
        data = pd.DataFrame({
            x_column: [f'Q{i+1} 2025-26' for i in range(min(4, len(grouped)))],
            'Revenue': (grouped['revenue'] / 1000).tolist()[:4],
            'Cost': (grouped['cost'] / 1000).tolist()[:4],
            'Profit': (grouped['profit'] / 1000).tolist()[:4]
        })
    
    # Determine columns to plot
    if y_columns is None:
        y_columns = [col for col in data.columns if col != x_column]
    
    # Use default colors if none provided
    if colors is None:
        colors = px.colors.qualitative.Set2
    
    # Create figure
    fig = go.Figure()
    
    # Add bar traces for each group
    for idx, col in enumerate(y_columns):
        fig.add_trace(go.Bar(
            name=col,
            x=data[x_column],
            y=data[col],
            marker_color=colors[idx % len(colors)],
            text=data[col].round(1),
            textposition='outside'
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family="Arial, sans-serif")),
        xaxis_title=x_label,
        yaxis_title=y_label,
        height=height,
        barmode='group',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=60, r=40, t=100, b=60)
    )
    
    return fig


# ==================== PIE & DONUT CHARTS ====================

def create_pie_chart(
    data: pd.DataFrame = None,
    labels_column: str = 'category',
    values_column: str = 'value',
    title: str = 'Distribution Chart',
    height: int = 400,
    hole: float = 0,
    colors: List[str] = None,
    show_legend: bool = True
) -> go.Figure:
    """
    Create a pie chart or donut chart.
    
    Args:
        data: DataFrame containing the data. If None, generates placeholder data
        labels_column: Name of the column containing labels
        values_column: Name of the column containing values
        title: Chart title
        height: Chart height in pixels
        hole: Size of center hole (0 for pie, 0.4-0.6 for donut)
        colors: List of colors for segments
        show_legend: Whether to show the legend
    
    Returns:
        Plotly Figure object
    """
    # Use realistic business data if none provided
    if data is None:
        segment_data = get_customer_segmentation_data()
        # Select top segments by revenue
        top_segments = segment_data.nlargest(5, 'revenue')
        data = pd.DataFrame({
            labels_column: top_segments['segment'],
            values_column: top_segments['revenue'] / 1000  # Convert to thousands
        })
    
    # Use default colors if none provided
    if colors is None:
        colors = px.colors.qualitative.Set3
    
    # Create figure
    fig = go.Figure(go.Pie(
        labels=data[labels_column],
        values=data[values_column],
        hole=hole,
        marker=dict(colors=colors),
        textposition='inside',
        textinfo='percent+label'
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family="Arial, sans-serif")),
        height=height,
        showlegend=show_legend,
        template='plotly_white',
        margin=dict(l=40, r=40, t=80, b=40)
    )
    
    return fig


# ==================== AREA CHARTS ====================

def create_stacked_area_chart(
    data: pd.DataFrame = None,
    x_column: str = 'date',
    y_columns: List[str] = None,
    title: str = 'Stacked Area Chart',
    x_label: str = 'Date',
    y_label: str = 'Value',
    height: int = 400,
    colors: List[str] = None
) -> go.Figure:
    """
    Create a stacked area chart for showing composition over time.
    
    Args:
        data: DataFrame containing the data. If None, generates placeholder data
        x_column: Name of the x-axis column
        y_columns: List of column names to stack
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        height: Chart height in pixels
        colors: List of colors for each area
    
    Returns:
        Plotly Figure object
    """
    # Use realistic business data if none provided
    if data is None:
        y_columns = y_columns or ['Premium Plan', 'Professional Plan', 'Standard Plan']
        # Generate realistic revenue data for top products
        dates = pd.date_range(end=datetime(2026, 5, 2), periods=30, freq='D')
        data = {'date': dates}
        base_values = [850, 650, 450]  # Daily revenue in thousands
        for idx, name in enumerate(y_columns):
            values = []
            for i, date in enumerate(dates):
                day_factor = 1.0 if date.dayofweek < 5 else 0.65
                trend = base_values[idx] * (1 + i * 0.001)
                seasonal = base_values[idx] * 0.1 * np.sin(i / 7 * 2 * np.pi)
                values.append((trend + seasonal) * day_factor)
            data[name] = values
        data = pd.DataFrame(data)
    
    # Determine columns to plot
    if y_columns is None:
        y_columns = [col for col in data.columns if col != x_column]
    
    # Use default colors if none provided
    if colors is None:
        colors = px.colors.qualitative.Pastel
    
    # Create figure
    fig = go.Figure()
    
    # Add stacked area traces
    for idx, col in enumerate(y_columns):
        fig.add_trace(go.Scatter(
            x=data[x_column],
            y=data[col],
            mode='lines',
            name=col,
            line=dict(width=0.5, color=colors[idx % len(colors)]),
            stackgroup='one',
            fillcolor=colors[idx % len(colors)]
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family="Arial, sans-serif")),
        xaxis_title=x_label,
        yaxis_title=y_label,
        height=height,
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=60, r=40, t=100, b=60)
    )
    
    return fig


# ==================== GAUGE & INDICATOR CHARTS ====================

def create_gauge_chart(
    value: float = None,
    title: str = 'KPI Gauge',
    min_value: float = 0,
    max_value: float = 100,
    target: float = None,
    units: str = '',
    height: int = 300,
    color_ranges: List[Tuple[float, float, str]] = None
) -> go.Figure:
    """
    Create a gauge chart for displaying a single KPI.
    
    Args:
        value: Current value to display. If None, generates random value
        title: Chart title
        min_value: Minimum gauge value
        max_value: Maximum gauge value
        target: Optional target line value
        units: Units to display (e.g., '%', '$', 'users')
        height: Chart height in pixels
        color_ranges: List of (start, end, color) tuples for gauge coloring
    
    Returns:
        Plotly Figure object
    """
    # Use realistic business sample value if none provided
    if value is None:
        # Generate realistic value based on context (e.g., percentage for typical KPIs)
        if max_value == 100:
            value = np.random.uniform(65, 85)  # Typical KPI percentage
        else:
            value = np.random.uniform(min_value + (max_value - min_value) * 0.6, 
                                     min_value + (max_value - min_value) * 0.85)
    
    # Default color ranges if none provided
    if color_ranges is None:
        color_ranges = [
            (min_value, max_value * 0.33, 'red'),
            (max_value * 0.33, max_value * 0.66, 'yellow'),
            (max_value * 0.66, max_value, 'green')
        ]
    
    # Create gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta" if target else "gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20}},
        number={'suffix': f' {units}' if units else ''},
        delta={'reference': target} if target else None,
        gauge={
            'axis': {'range': [min_value, max_value]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [start, end], 'color': color}
                for start, end, color in color_ranges
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': target
            } if target else None
        }
    ))
    
    # Update layout
    fig.update_layout(
        height=height,
        template='plotly_white',
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig


def create_indicator_card(
    value: float = None,
    title: str = 'KPI',
    previous_value: float = None,
    units: str = '',
    height: int = 200
) -> go.Figure:
    """
    Create a simple indicator card showing a KPI value and its change.
    
    Args:
        value: Current value to display. If None, generates random value
        title: Indicator title
        previous_value: Previous value for comparison
        units: Units to display
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object
    """
    # Use realistic business sample values if none provided
    if value is None:
        # Generate realistic business metric values
        if units in ['$', '€', '£']:
            value = np.random.uniform(5000, 15000)  # Revenue-like metric
        elif units == '%':
            value = np.random.uniform(60, 95)  # Percentage metric
        else:
            value = np.random.uniform(1000, 10000)  # Count metric
    
    if previous_value is None:
        # Generate previous value showing realistic growth/decline
        growth_factor = np.random.uniform(0.92, 1.08)  # ±8% change
        previous_value = value / growth_factor
    
    # Create indicator
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=value,
        delta={
            'reference': previous_value,
            'relative': True,
            'valueformat': '.1%'
        },
        title={'text': title, 'font': {'size': 18}},
        number={'prefix': units if units in ['$', '€', '£'] else '', 'suffix': f' {units}' if units not in ['$', '€', '£'] else ''},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    
    # Update layout
    fig.update_layout(
        height=height,
        template='plotly_white',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


# ==================== HEATMAP ====================

def create_heatmap(
    data: pd.DataFrame = None,
    x_column: str = None,
    y_column: str = None,
    z_column: str = 'value',
    title: str = 'Heatmap',
    x_label: str = 'X Axis',
    y_label: str = 'Y Axis',
    height: int = 500,
    colorscale: str = 'Blues'
) -> go.Figure:
    """
    Create a heatmap for showing data intensity across two dimensions.
    
    Args:
        data: DataFrame containing the data. If None, generates placeholder data
        x_column: Column for x-axis categories
        y_column: Column for y-axis categories
        z_column: Column containing values for heatmap intensity
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        height: Chart height in pixels
        colorscale: Plotly colorscale name
    
    Returns:
        Plotly Figure object
    """
    # Use realistic business data if none provided
    if data is None:
        # Create realistic hourly activity heatmap for a business week
        x_cats = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        y_cats = ['6-9am', '9-12pm', '12-3pm', '3-6pm', '6-9pm', '9-12am']
        # Realistic pattern: peak during business hours on weekdays
        z_values = np.array([
            [45, 52, 58, 62, 55, 25, 18],  # 6-9am
            [78, 85, 89, 92, 87, 35, 28],  # 9-12pm
            [62, 68, 72, 75, 70, 42, 32],  # 12-3pm
            [82, 91, 95, 93, 88, 38, 30],  # 3-6pm
            [35, 42, 45, 48, 52, 55, 48],  # 6-9pm
            [15, 18, 20, 22, 28, 38, 35],  # 9-12am
        ])
        
        fig = go.Figure(data=go.Heatmap(
            z=z_values,
            x=x_cats,
            y=y_cats,
            colorscale=colorscale,
            text=z_values,
            texttemplate='%{text}',
            textfont={"size": 10}
        ))
    else:
        # Pivot data for heatmap if columns provided
        if x_column and y_column:
            pivot_data = data.pivot(index=y_column, columns=x_column, values=z_column)
            fig = go.Figure(data=go.Heatmap(
                z=pivot_data.values,
                x=pivot_data.columns,
                y=pivot_data.index,
                colorscale=colorscale
            ))
        else:
            # Assume data is already in matrix form
            fig = go.Figure(data=go.Heatmap(
                z=data.values,
                colorscale=colorscale
            ))
    
    # Update layout
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family="Arial, sans-serif")),
        xaxis_title=x_label,
        yaxis_title=y_label,
        height=height,
        template='plotly_white',
        margin=dict(l=80, r=40, t=80, b=60)
    )
    
    return fig


# ==================== COMBO CHARTS ====================

def create_combo_chart(
    data: pd.DataFrame = None,
    x_column: str = 'date',
    bar_columns: List[str] = None,
    line_columns: List[str] = None,
    title: str = 'Combination Chart',
    x_label: str = 'Date',
    y1_label: str = 'Bar Values',
    y2_label: str = 'Line Values',
    height: int = 400
) -> go.Figure:
    """
    Create a combination chart with bars and lines on different y-axes.
    
    Args:
        data: DataFrame containing the data. If None, generates placeholder data
        x_column: Name of the x-axis column
        bar_columns: List of columns to plot as bars
        line_columns: List of columns to plot as lines
        title: Chart title
        x_label: X-axis label
        y1_label: Left y-axis label (for bars)
        y2_label: Right y-axis label (for lines)
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object
    """
    # Use realistic business data if none provided
    if data is None:
        revenue_data = get_revenue_sample_data('12m')
        bar_columns = bar_columns or ['Revenue']
        line_columns = line_columns or ['Growth Rate']
        
        # Calculate month-over-month growth
        revenue_data['growth_rate'] = revenue_data['revenue'].pct_change() * 100
        revenue_data['growth_rate'] = revenue_data['growth_rate'].fillna(0)
        
        data = pd.DataFrame({
            x_column: revenue_data['date'],
            bar_columns[0]: revenue_data['revenue'] / 1000,  # Convert to thousands
            line_columns[0]: revenue_data['growth_rate']
        })
    
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Add bar traces
    for col in bar_columns:
        fig.add_trace(go.Bar(
            name=col,
            x=data[x_column],
            y=data[col],
            yaxis='y',
            marker_color='#636EFA'
        ))
    
    # Add line traces
    for col in line_columns:
        fig.add_trace(go.Scatter(
            name=col,
            x=data[x_column],
            y=data[col],
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='#EF553B', width=2),
            marker=dict(size=6)
        ))
    
    # Update layout with dual y-axes
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family="Arial, sans-serif")),
        xaxis_title=x_label,
        yaxis=dict(title=y1_label, side='left'),
        yaxis2=dict(title=y2_label, overlaying='y', side='right'),
        height=height,
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=60, r=60, t=100, b=60)
    )
    
    return fig


# ==================== UTILITY FUNCTIONS ====================

def apply_custom_theme(
    fig: go.Figure,
    theme: str = 'light',
    font_family: str = 'Arial, sans-serif'
) -> go.Figure:
    """
    Apply a custom theme to a figure.
    
    Args:
        fig: Plotly Figure object
        theme: 'light', 'dark', or 'custom'
        font_family: Font family to use
    
    Returns:
        Modified Figure object
    """
    if theme == 'dark':
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='#1e1e1e',
            plot_bgcolor='#1e1e1e',
            font=dict(family=font_family, color='#e0e0e0')
        )
    elif theme == 'light':
        fig.update_layout(
            template='plotly_white',
            font=dict(family=font_family)
        )
    
    return fig


def add_annotations(
    fig: go.Figure,
    annotations: List[Dict[str, Union[str, float]]],
) -> go.Figure:
    """
    Add text annotations to a figure.
    
    Args:
        fig: Plotly Figure object
        annotations: List of annotation dictionaries with keys:
            - text: Annotation text
            - x: X coordinate
            - y: Y coordinate
            - showarrow: Whether to show arrow (default True)
            - arrowhead: Arrow style (default 2)
    
    Returns:
        Modified Figure object
    """
    for ann in annotations:
        fig.add_annotation(
            text=ann.get('text', ''),
            x=ann.get('x', 0),
            y=ann.get('y', 0),
            showarrow=ann.get('showarrow', True),
            arrowhead=ann.get('arrowhead', 2)
        )
    
    return fig


# ==================== DEMO & CONVENIENCE FUNCTIONS ====================

def create_revenue_trend_chart(period: str = '30d', height: int = 400) -> go.Figure:
    """
    Create a revenue trend chart with realistic sample data.
    
    Args:
        period: Time period ('30d', '90d', '12m')
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object showing revenue trend
    """
    data = get_revenue_sample_data(period)
    return create_line_chart(
        data=data,
        x_column='date',
        y_column='revenue',
        title=f'Revenue Trend - Last {period.upper()}',
        x_label='Date',
        y_label='Revenue ($)',
        color='#2E7D32',
        height=height,
        show_markers=True,
        fill_area=True
    )


def create_revenue_breakdown_chart(period: str = '12m', height: int = 400) -> go.Figure:
    """
    Create a multi-line chart showing revenue, cost, and profit.
    
    Args:
        period: Time period ('30d', '90d', '12m')
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object showing revenue breakdown
    """
    data = get_revenue_sample_data(period)
    return create_multi_line_chart(
        data=data,
        x_column='date',
        y_columns=['revenue', 'cost', 'profit'],
        title='Revenue, Cost & Profit Analysis',
        x_label='Date',
        y_label='Amount ($)',
        height=height,
        colors=['#2E7D32', '#D32F2F', '#1976D2']
    )


def create_product_revenue_chart(height: int = 400, orientation: str = 'v') -> go.Figure:
    """
    Create a bar chart showing revenue by product.
    
    Args:
        height: Chart height in pixels
        orientation: 'v' for vertical, 'h' for horizontal
    
    Returns:
        Plotly Figure object showing product revenue
    """
    data = get_product_performance_data()
    return create_bar_chart(
        data=data,
        x_column='product',
        y_column='revenue',
        title='Revenue by Product',
        x_label='Product',
        y_label='Revenue ($)',
        orientation=orientation,
        color='#1976D2',
        height=height,
        show_values=True
    )


def create_segment_revenue_chart(height: int = 400) -> go.Figure:
    """
    Create a pie chart showing revenue by customer segment.
    
    Args:
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object showing segment distribution
    """
    data = get_customer_segmentation_data()
    return create_pie_chart(
        data=data,
        labels_column='segment',
        values_column='revenue',
        title='Revenue Distribution by Customer Segment',
        height=height,
        hole=0.4,  # Donut chart
        show_legend=True
    )


def create_channel_performance_chart(height: int = 400) -> go.Figure:
    """
    Create a horizontal bar chart showing channel performance.
    
    Args:
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object showing channel performance
    """
    data = get_channel_performance_data()
    # Sort by revenue descending
    data = data.sort_values('revenue', ascending=True)
    return create_bar_chart(
        data=data,
        x_column='channel',
        y_column='revenue',
        title='Revenue by Marketing Channel',
        x_label='Channel',
        y_label='Revenue ($)',
        orientation='h',
        color='#7B1FA2',
        height=height,
        show_values=True
    )


def create_regional_performance_chart(height: int = 400) -> go.Figure:
    """
    Create a grouped bar chart comparing regional metrics.
    
    Args:
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object showing regional performance
    """
    data = get_regional_performance_data()
    # Normalize revenue for better visualization
    data['revenue_normalized'] = data['revenue'] / 1000
    
    return create_grouped_bar_chart(
        data=data,
        x_column='region',
        y_columns=['revenue_normalized', 'customers'],
        title='Regional Performance: Revenue & Customers',
        x_label='Region',
        y_label='Value',
        height=height
    )


def create_activity_heatmap_chart(height: int = 500) -> go.Figure:
    """
    Create a heatmap showing user activity patterns.
    
    Args:
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object showing activity heatmap
    """
    return create_heatmap(
        data=None,  # Uses built-in realistic sample data
        title='User Activity by Time & Day',
        x_label='Day of Week',
        y_label='Time of Day',
        height=height,
        colorscale='Blues'
    )


def create_customer_satisfaction_gauge(height: int = 300) -> go.Figure:
    """
    Create a gauge chart showing customer satisfaction score.
    
    Args:
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object showing satisfaction gauge
    """
    return create_gauge_chart(
        value=78.5,
        title='Customer Satisfaction Score',
        min_value=0,
        max_value=100,
        target=75,
        units='%',
        height=height,
        color_ranges=[
            (0, 50, '#EF5350'),
            (50, 75, '#FFA726'),
            (75, 100, '#66BB6A')
        ]
    )


def create_mrr_indicator(height: int = 200) -> go.Figure:
    """
    Create an indicator card showing MRR (Monthly Recurring Revenue).
    
    Args:
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object showing MRR indicator
    """
    return create_indicator_card(
        value=385420,
        title='Monthly Recurring Revenue',
        previous_value=371340,
        units='$',
        height=height
    )


def create_revenue_growth_combo_chart(height: int = 400) -> go.Figure:
    """
    Create a combination chart showing revenue bars with growth rate line.
    
    Args:
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object showing revenue and growth
    """
    return create_combo_chart(
        data=None,  # Uses built-in realistic sample data
        title='Monthly Revenue & Growth Rate',
        x_label='Month',
        y1_label='Revenue ($K)',
        y2_label='Growth Rate (%)',
        height=height
    )


def get_churn_prediction_data() -> pd.DataFrame:
    """
    Get realistic churn prediction data by customer segment.
    
    Returns:
        DataFrame with segment churn predictions
    """
    segments = ['Enterprise', 'Mid-Market', 'Small Business', 'Startup', 'Free Trial']
    at_risk = [12, 48, 194, 391, 1756]
    low_risk = [198, 623, 987, 1245, 1523]
    healthy = [35, 152, 366, 467, 613]
    
    return pd.DataFrame({
        'segment': segments,
        'high_risk': at_risk,
        'medium_risk': low_risk,
        'low_risk': healthy
    })


def get_cohort_retention_data() -> pd.DataFrame:
    """
    Get realistic cohort retention data over time.
    
    Returns:
        DataFrame with cohort retention percentages
    """
    cohorts = ['Jan 2026', 'Feb 2026', 'Mar 2026', 'Apr 2026', 'May 2026']
    data = {
        'Month 0': [100, 100, 100, 100, 100],
        'Month 1': [85.3, 87.1, 89.2, 90.8, None],
        'Month 2': [72.4, 75.8, 78.3, None, None],
        'Month 3': [65.2, 68.9, None, None, None],
        'Month 4': [60.1, None, None, None, None],
        'Month 5': [57.3, None, None, None, None]
    }
    
    return pd.DataFrame(data, index=cohorts)


def get_retention_trend_data(days: int = 90) -> pd.DataFrame:
    """
    Get retention rate trend over time.
    
    Args:
        days: Number of days of data
    
    Returns:
        DataFrame with daily retention metrics
    """
    dates = pd.date_range(end=datetime(2026, 5, 2), periods=days, freq='D')
    
    retention_rates = []
    churn_rates = []
    
    for i in range(days):
        # Improving trend with some fluctuation
        base_retention = 82 + (i * 0.05)
        seasonal = 2 * np.sin(i / 14 * 2 * np.pi)
        retention = min(95, base_retention + seasonal + np.random.uniform(-1, 1))
        
        retention_rates.append(retention)
        churn_rates.append(100 - retention)
    
    return pd.DataFrame({
        'date': dates,
        'retention_rate': retention_rates,
        'churn_rate': churn_rates
    })


def get_segment_retention_data() -> pd.DataFrame:
    """
    Get retention metrics by customer segment.
    
    Returns:
        DataFrame with segment retention data
    """
    segments = ['Enterprise', 'Mid-Market', 'Small Business', 'Startup', 'Free Trial']
    retention_30d = [96.8, 92.4, 87.3, 81.2, 54.7]
    retention_90d = [92.1, 85.7, 72.8, 65.4, 32.1]
    avg_ltv = [52000, 18500, 4200, 1850, 0]
    
    return pd.DataFrame({
        'segment': segments,
        '30_day_retention': retention_30d,
        '90_day_retention': retention_90d,
        'avg_ltv': avg_ltv
    })


def get_churn_reasons_data() -> pd.DataFrame:
    """
    Get data on reasons for customer churn.
    
    Returns:
        DataFrame with churn reasons and counts
    """
    reasons = [
        'Price Too High',
        'Poor Product Fit',
        'Lack of Features',
        'Customer Service',
        'Moved to Competitor',
        'Technical Issues',
        'Other'
    ]
    counts = [145, 98, 87, 65, 112, 43, 56]
    percentages = [c / sum(counts) * 100 for c in counts]
    
    return pd.DataFrame({
        'reason': reasons,
        'count': counts,
        'percentage': percentages
    })


# ==================== RETENTION-SPECIFIC CHARTS ====================

def create_cohort_retention_heatmap(height: int = 500) -> go.Figure:
    """
    Create a cohort retention heatmap showing retention rates over time.
    
    Args:
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object with cohort heatmap
    """
    data = get_cohort_retention_data()
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale=[
            [0, '#ef5350'],      # Red for low retention
            [0.5, '#ffa726'],    # Orange for medium
            [0.7, '#ffee58'],    # Yellow for good
            [1, '#66bb6a']       # Green for excellent
        ],
        text=[[f'{val:.1f}%' if pd.notna(val) else 'N/A' for val in row] for row in data.values],
        texttemplate='%{text}',
        textfont={"size": 12},
        colorbar=dict(
            title='Retention %',
            ticksuffix='%'
        ),
        hoverongaps=False,
        hovertemplate='<b>%{y}</b><br>%{x}: %{z:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='Cohort Retention Analysis',
            font=dict(size=20, family="Arial, sans-serif")
        ),
        xaxis_title='Months Since First Purchase',
        yaxis_title='Cohort',
        height=height,
        template='plotly_white',
        margin=dict(l=100, r=120, t=80, b=60)
    )
    
    return fig


def create_retention_trend_chart(days: int = 90, height: int = 400) -> go.Figure:
    """
    Create a line chart showing retention rate trends over time.
    
    Args:
        days: Number of days of data
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object
    """
    data = get_retention_trend_data(days)
    
    fig = go.Figure()
    
    # Add retention rate line
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['retention_rate'],
        name='Retention Rate',
        mode='lines+markers',
        line=dict(color='#66bb6a', width=3),
        marker=dict(size=4),
        fill='tozeroy',
        fillcolor='rgba(102, 187, 106, 0.1)'
    ))
    
    # Add churn rate line
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['churn_rate'],
        name='Churn Rate',
        mode='lines+markers',
        line=dict(color='#ef5350', width=2, dash='dash'),
        marker=dict(size=4)
    ))
    
    # Add target line
    fig.add_hline(
        y=85,
        line_dash="dot",
        line_color="gray",
        annotation_text="Target: 85%",
        annotation_position="right"
    )
    
    fig.update_layout(
        title=dict(
            text='Retention & Churn Rate Trends',
            font=dict(size=20, family="Arial, sans-serif")
        ),
        xaxis_title='Date',
        yaxis_title='Rate (%)',
        yaxis=dict(range=[0, 100]),
        height=height,
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=60, r=40, t=100, b=60)
    )
    
    return fig


def create_segment_retention_comparison(height: int = 450) -> go.Figure:
    """
    Create a grouped bar chart comparing retention across segments.
    
    Args:
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object
    """
    data = get_segment_retention_data()
    
    fig = go.Figure()
    
    # Add 30-day retention bars
    fig.add_trace(go.Bar(
        x=data['segment'],
        y=data['30_day_retention'],
        name='30-Day Retention',
        marker_color='#42a5f5',
        text=[f'{val:.1f}%' for val in data['30_day_retention']],
        textposition='outside'
    ))
    
    # Add 90-day retention bars
    fig.add_trace(go.Bar(
        x=data['segment'],
        y=data['90_day_retention'],
        name='90-Day Retention',
        marker_color='#ab47bc',
        text=[f'{val:.1f}%' for val in data['90_day_retention']],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=dict(
            text='Retention Rate by Customer Segment',
            font=dict(size=20, family="Arial, sans-serif")
        ),
        xaxis_title='Customer Segment',
        yaxis_title='Retention Rate (%)',
        yaxis=dict(range=[0, 110]),
        barmode='group',
        height=height,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=60, r=40, t=100, b=60)
    )
    
    return fig


def create_churn_reasons_chart(height: int = 400) -> go.Figure:
    """
    Create a horizontal bar chart showing reasons for churn.
    
    Args:
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object
    """
    data = get_churn_reasons_data()
    
    # Sort by count
    data = data.sort_values('count', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=data['reason'],
        x=data['count'],
        orientation='h',
        marker=dict(
            color=data['percentage'],
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title='%')
        ),
        text=[f'{count} ({pct:.1f}%)' for count, pct in zip(data['count'], data['percentage'])],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Count: %{x}<br>Percentage: %{marker.color:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='Top Reasons for Customer Churn',
            font=dict(size=20, family="Arial, sans-serif")
        ),
        xaxis_title='Number of Customers',
        yaxis_title='',
        height=height,
        template='plotly_white',
        showlegend=False,
        margin=dict(l=150, r=100, t=80, b=60)
    )
    
    return fig


def create_churn_risk_distribution(height: int = 400) -> go.Figure:
    """
    Create a stacked bar chart showing churn risk distribution by segment.
    
    Args:
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object
    """
    data = get_churn_prediction_data()
    
    fig = go.Figure()
    
    # Add stacked bars for each risk level
    fig.add_trace(go.Bar(
        x=data['segment'],
        y=data['high_risk'],
        name='High Risk',
        marker_color='#ef5350',
        text=data['high_risk'],
        textposition='inside'
    ))
    
    fig.add_trace(go.Bar(
        x=data['segment'],
        y=data['medium_risk'],
        name='Medium Risk',
        marker_color='#ffa726',
        text=data['medium_risk'],
        textposition='inside'
    ))
    
    fig.add_trace(go.Bar(
        x=data['segment'],
        y=data['low_risk'],
        name='Low Risk',
        marker_color='#66bb6a',
        text=data['low_risk'],
        textposition='inside'
    ))
    
    fig.update_layout(
        title=dict(
            text='Customer Churn Risk Distribution',
            font=dict(size=20, family="Arial, sans-serif")
        ),
        xaxis_title='Customer Segment',
        yaxis_title='Number of Customers',
        barmode='stack',
        height=height,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=60, r=40, t=100, b=60)
    )
    
    return fig


def create_ltv_by_segment_chart(height: int = 400) -> go.Figure:
    """
    Create a chart showing customer lifetime value by segment.
    
    Args:
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object
    """
    data = get_segment_retention_data()
    
    # Sort by LTV
    data = data.sort_values('avg_ltv', ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=data['segment'],
        y=data['avg_ltv'],
        marker=dict(
            color=data['avg_ltv'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='LTV ($)')
        ),
        text=[f'${val:,.0f}' for val in data['avg_ltv']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>LTV: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='Average Customer Lifetime Value by Segment',
            font=dict(size=20, family="Arial, sans-serif")
        ),
        xaxis_title='Customer Segment',
        yaxis_title='Average LTV ($)',
        height=height,
        template='plotly_white',
        showlegend=False,
        margin=dict(l=60, r=120, t=80, b=60)
    )
    
    return fig


# ==================== PRODUCT KPI CHARTS ====================

def create_product_performance_overview(
    data: pd.DataFrame,
    top_n: int = 10,
    height: int = 500
) -> go.Figure:
    """
    Create comprehensive product performance overview chart.
    
    Args:
        data: DataFrame with product performance data
        top_n: Number of top products to display
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object with product performance visualization
    """
    # Get top N products by revenue
    top_products = data.nlargest(top_n, 'total_revenue')
    
    fig = go.Figure()
    
    # Add revenue bars
    fig.add_trace(go.Bar(
        x=top_products['product'],
        y=top_products['total_revenue'],
        name='Revenue',
        marker_color='#42a5f5',
        text=[f'${val/1000:.1f}K' for val in top_products['total_revenue']],
        textposition='outside',
        yaxis='y',
        hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
    ))
    
    # Add profit margin line on secondary axis
    fig.add_trace(go.Scatter(
        x=top_products['product'],
        y=top_products['profit_margin'],
        name='Profit Margin %',
        mode='lines+markers',
        line=dict(color='#66bb6a', width=3),
        marker=dict(size=8),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Margin: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=f'Top {top_n} Products by Revenue & Profit Margin',
            font=dict(size=20, family="Arial, sans-serif")
        ),
        xaxis_title='Product',
        yaxis=dict(
            title='Total Revenue ($)',
            side='left'
        ),
        yaxis2=dict(
            title='Profit Margin (%)',
            side='right',
            overlaying='y',
            range=[0, max(top_products['profit_margin']) * 1.2]
        ),
        height=height,
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=60, r=60, t=100, b=120)
    )
    
    # Rotate x-axis labels for better readability
    fig.update_xaxes(tickangle=-45)
    
    return fig


def create_product_category_distribution(
    data: pd.DataFrame,
    height: int = 400
) -> go.Figure:
    """
    Create pie chart showing revenue distribution by product category.
    
    Args:
        data: DataFrame with product performance data
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object with category distribution
    """
    # Aggregate by category
    category_data = data.groupby('category').agg({
        'total_revenue': 'sum',
        'total_quantity': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=category_data['category'],
        values=category_data['total_revenue'],
        hole=0.4,
        marker=dict(
            colors=px.colors.qualitative.Set3,
            line=dict(color='white', width=2)
        ),
        textinfo='label+percent',
        textposition='outside',
        hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.2f}<br>Share: %{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='Revenue Distribution by Product Category',
            font=dict(size=20, family="Arial, sans-serif")
        ),
        height=height,
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        ),
        margin=dict(l=40, r=150, t=80, b=40)
    )
    
    return fig


def create_product_profitability_matrix(
    data: pd.DataFrame,
    height: int = 500
) -> go.Figure:
    """
    Create bubble chart showing product profitability (Revenue vs Profit Margin).
    
    Args:
        data: DataFrame with product performance data
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object with profitability matrix
    """
    fig = go.Figure()
    
    # Create bubble chart
    fig.add_trace(go.Scatter(
        x=data['total_revenue'],
        y=data['profit_margin'],
        mode='markers+text',
        marker=dict(
            size=data['transaction_count'] / 2,  # Size based on transaction volume
            color=data['roi'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='ROI %'),
            line=dict(color='white', width=1)
        ),
        text=data['product'],
        textposition='top center',
        textfont=dict(size=9),
        hovertemplate='<b>%{text}</b><br>' +
                     'Revenue: $%{x:,.2f}<br>' +
                     'Profit Margin: %{y:.1f}%<br>' +
                     'ROI: %{marker.color:.1f}%<extra></extra>'
    ))
    
    # Add quadrant lines
    median_revenue = data['total_revenue'].median()
    median_margin = data['profit_margin'].median()
    
    fig.add_vline(x=median_revenue, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_hline(y=median_margin, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Add quadrant annotations
    max_revenue = data['total_revenue'].max()
    max_margin = data['profit_margin'].max()
    
    annotations = [
        dict(x=median_revenue + (max_revenue - median_revenue) / 2, 
             y=median_margin + (max_margin - median_margin) / 2,
             text="Stars<br>(High Revenue, High Margin)", showarrow=False, 
             font=dict(color="green", size=10), opacity=0.7),
        dict(x=median_revenue / 2, 
             y=median_margin + (max_margin - median_margin) / 2,
             text="Question Marks<br>(Low Revenue, High Margin)", showarrow=False,
             font=dict(color="orange", size=10), opacity=0.7),
        dict(x=median_revenue + (max_revenue - median_revenue) / 2,
             y=median_margin / 2,
             text="Cash Cows<br>(High Revenue, Low Margin)", showarrow=False,
             font=dict(color="blue", size=10), opacity=0.7),
        dict(x=median_revenue / 2,
             y=median_margin / 2,
             text="Dogs<br>(Low Revenue, Low Margin)", showarrow=False,
             font=dict(color="red", size=10), opacity=0.7)
    ]
    
    fig.update_layout(
        title=dict(
            text='Product Profitability Matrix',
            font=dict(size=20, family="Arial, sans-serif")
        ),
        xaxis_title='Total Revenue ($)',
        yaxis_title='Profit Margin (%)',
        height=height,
        template='plotly_white',
        annotations=annotations,
        margin=dict(l=60, r=40, t=80, b=60)
    )
    
    return fig


def create_product_roi_ranking(
    data: pd.DataFrame,
    top_n: int = 10,
    height: int = 400
) -> go.Figure:
    """
    Create horizontal bar chart showing top products by ROI.
    
    Args:
        data: DataFrame with product performance data
        top_n: Number of top products to display
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object with ROI ranking
    """
    # Get top N products by ROI
    top_roi = data.nlargest(top_n, 'roi').sort_values('roi', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=top_roi['product'],
        x=top_roi['roi'],
        orientation='h',
        marker=dict(
            color=top_roi['roi'],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title='ROI %')
        ),
        text=[f'{val:.1f}%' for val in top_roi['roi']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>ROI: %{x:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=f'Top {top_n} Products by Return on Investment',
            font=dict(size=20, family="Arial, sans-serif")
        ),
        xaxis_title='ROI (%)',
        yaxis_title='',
        height=height,
        template='plotly_white',
        showlegend=False,
        margin=dict(l=150, r=100, t=80, b=60)
    )
    
    return fig


def create_product_quantity_revenue_comparison(
    data: pd.DataFrame,
    top_n: int = 10,
    height: int = 450
) -> go.Figure:
    """
    Create grouped bar chart comparing quantity sold vs revenue.
    
    Args:
        data: DataFrame with product performance data
        top_n: Number of products to display
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object with quantity-revenue comparison
    """
    # Get top N products by revenue
    top_products = data.nlargest(top_n, 'total_revenue')
    
    fig = go.Figure()
    
    # Normalize values for better comparison
    max_quantity = top_products['total_quantity'].max()
    max_revenue = top_products['total_revenue'].max()
    
    # Add quantity bars (normalized)
    fig.add_trace(go.Bar(
        x=top_products['product'],
        y=top_products['total_quantity'],
        name='Quantity Sold',
        marker_color='#ffa726',
        text=top_products['total_quantity'],
        textposition='outside',
        yaxis='y',
        hovertemplate='<b>%{x}</b><br>Quantity: %{y:,}<extra></extra>'
    ))
    
    # Add revenue bars on secondary axis
    fig.add_trace(go.Bar(
        x=top_products['product'],
        y=top_products['total_revenue'],
        name='Revenue ($)',
        marker_color='#42a5f5',
        text=[f'${val/1000:.0f}K' for val in top_products['total_revenue']],
        textposition='outside',
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='Product Performance: Quantity vs Revenue',
            font=dict(size=20, family="Arial, sans-serif")
        ),
        xaxis_title='Product',
        yaxis=dict(
            title='Quantity Sold',
            side='left'
        ),
        yaxis2=dict(
            title='Revenue ($)',
            side='right',
            overlaying='y'
        ),
        barmode='group',
        height=height,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=60, r=60, t=100, b=120)
    )
    
    fig.update_xaxes(tickangle=-45)
    
    return fig


def create_product_kpi_summary_cards(
    kpi_data: Dict
) -> Dict[str, go.Figure]:
    """
    Create KPI indicator cards for product metrics.
    
    Args:
        kpi_data: Dictionary with product KPI data from API
    
    Returns:
        Dictionary of Plotly figures for each KPI
    """
    summary = kpi_data.get('summary', {})
    
    cards = {}
    
    # Total Revenue Card
    cards['total_revenue'] = create_indicator_card(
        value=summary.get('total_revenue', 0),
        title='Total Product Revenue',
        previous_value=summary.get('total_revenue', 0) / (1 + summary.get('revenue_growth', 15) / 100),
        units='$',
        height=180
    )
    
    # Total Profit Card
    cards['total_profit'] = create_indicator_card(
        value=summary.get('total_profit', 0),
        title='Total Profit',
        previous_value=summary.get('total_profit', 0) / (1 + summary.get('profit_growth', 12) / 100),
        units='$',
        height=180
    )
    
    # Average Profit Margin Card
    cards['avg_margin'] = create_gauge_chart(
        value=summary.get('avg_profit_margin', 0),
        title='Avg Profit Margin',
        min_value=0,
        max_value=100,
        threshold_low=15,
        threshold_high=25,
        units='%',
        height=180
    )
    
    # Average ROI Card
    cards['avg_roi'] = create_gauge_chart(
        value=summary.get('avg_roi', 0),
        title='Average ROI',
        min_value=0,
        max_value=100,
        threshold_low=20,
        threshold_high=35,
        units='%',
        height=180
    )
    
    return cards


def get_all_sample_charts() -> Dict[str, go.Figure]:
    """
    Generate all sample charts with realistic data for demonstration purposes.
    
    Returns:
        Dictionary mapping chart names to Plotly Figure objects
    """
    return {
        'revenue_trend': create_revenue_trend_chart(),
        'revenue_breakdown': create_revenue_breakdown_chart(),
        'product_revenue': create_product_revenue_chart(),
        'segment_distribution': create_segment_revenue_chart(),
        'channel_performance': create_channel_performance_chart(),
        'regional_performance': create_regional_performance_chart(),
        'activity_heatmap': create_activity_heatmap_chart(),
        'satisfaction_gauge': create_customer_satisfaction_gauge(),
        'mrr_indicator': create_mrr_indicator(),
        'revenue_growth_combo': create_revenue_growth_combo_chart(),
        'cohort_retention_heatmap': create_cohort_retention_heatmap(),
        'retention_trend': create_retention_trend_chart(),
        'segment_retention': create_segment_retention_comparison(),
        'churn_reasons': create_churn_reasons_chart(),
        'churn_risk': create_churn_risk_distribution(),
        'ltv_by_segment': create_ltv_by_segment_chart()
    }

