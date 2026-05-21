"""
Modern Visualizations Showcase

This page demonstrates enhanced visualization capabilities with modern design patterns,
advanced Plotly configurations, and interactive components.
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import modern chart components
from components.charts_modern import (
    create_modern_line_chart,
    create_modern_bar_chart,
    create_modern_donut_chart,
    create_modern_gauge,
    create_modern_heatmap,
    create_modern_scatter,
    MODERN_COLORS
)

# Page configuration
st.set_page_config(
    page_title="Modern Visualizations - KPI Intelligence",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load modern CSS
with open(Path(__file__).parent.parent.parent / 'assets' / 'modern-ui.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Page header with gradient text
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 class="gradient-text" style="font-size: 3rem; margin-bottom: 0.5rem;">
        🎨 Modern Visualizations Showcase
    </h1>
    <p style="font-size: 1.2rem; color: #64748b; max-width: 800px; margin: 0 auto;">
        Experience enhanced data visualizations with modern design patterns, 
        advanced interactivity, and professional aesthetics
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar controls
with st.sidebar:
    st.markdown("### 🎨 Visualization Controls")
    
    chart_theme = st.selectbox(
        "Color Theme",
        ["Primary Blue", "Success Green", "Gradient", "Rainbow"],
        index=0
    )
    
    show_animations = st.checkbox("Enable Animations", value=True)
    show_trend_lines = st.checkbox("Show Trend Lines", value=True)
    
    st.markdown("---")
    st.markdown("### 📊 Data Settings")
    
    data_points = st.slider("Data Points", 10, 90, 30)
    noise_level = st.slider("Variability", 0, 100, 20)

# Generate sample data based on controls
@st.cache_data
def generate_sample_data(points, noise):
    dates = pd.date_range(end=datetime.now(), periods=points, freq='D')
    
    # Time series data
    base_value = 10000
    trend = np.linspace(0, 2000, points)
    seasonal = 1000 * np.sin(np.arange(points) * 2 * np.pi / 7)
    random_noise = np.random.normal(0, noise * 10, points)
    revenue = base_value + trend + seasonal + random_noise
    
    time_series_df = pd.DataFrame({
        'date': dates,
        'revenue': revenue,
        'costs': revenue * 0.65,
        'profit': revenue * 0.35,
        'users': (revenue / 50).astype(int)
    })
    
    # Category data
    categories = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    category_df = pd.DataFrame({
        'product': categories,
        'revenue': [125000, 98000, 87000, 65000, 43000],
        'units': [2340, 1890, 1650, 1200, 780],
        'growth': [15.3, -2.4, 8.7, 22.1, -5.2]
    })
    
    # Cohort retention data
    cohorts = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5']
    retention_df = pd.DataFrame({
        'Week 0': [100, 100, 100, 100, 100],
        'Week 1': [85, 87, 89, 91, 93],
        'Week 2': [72, 75, 78, 81, None],
        'Week 3': [65, 68, 71, None, None],
        'Week 4': [60, 63, None, None, None]
    }, index=cohorts)
    
    # Scatter data for performance matrix
    scatter_df = pd.DataFrame({
        'product': categories,
        'roi': [8.5, 6.2, 9.1, 7.8, 5.4],
        'market_share': [28, 22, 18, 15, 10],
        'growth_rate': [15.3, -2.4, 8.7, 22.1, -5.2]
    })
    
    return time_series_df, category_df, retention_df, scatter_df

time_series_data, category_data, retention_data, scatter_data = generate_sample_data(data_points, noise_level)

# Select colors based on theme
if chart_theme == "Primary Blue":
    colors = MODERN_COLORS['primary']
elif chart_theme == "Success Green":
    colors = MODERN_COLORS['success']
elif chart_theme == "Gradient":
    colors = MODERN_COLORS['gradient_blue']
else:
    colors = MODERN_COLORS['rainbow']

# ==================== KEY METRICS CARDS ====================

st.markdown("## 📈 Key Performance Indicators")
st.markdown('<div class="stats-grid">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card-enhanced metric-card-primary">
        <div class="metric-label">TOTAL REVENUE</div>
        <div class="metric-value-large">$2.4M</div>
        <div class="metric-change">↑ +15.3% vs last month</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card-enhanced metric-card-success">
        <div class="metric-label">ACTIVE USERS</div>
        <div class="metric-value-large">48.2K</div>
        <div class="metric-change">↑ +8.7% vs last month</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card-enhanced metric-card-info">
        <div class="metric-label">CONVERSION RATE</div>
        <div class="metric-value-large">3.8%</div>
        <div class="metric-change">↑ +0.5% vs last month</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card-enhanced metric-card-warning">
        <div class="metric-label">AVG ORDER VALUE</div>
        <div class="metric-value-large">$156</div>
        <div class="metric-change">↓ -2.1% vs last month</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ==================== ADVANCED LINE CHARTS ====================

st.markdown("## 📊 Revenue Trends & Forecasting")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-header">
        <div>
            <div class="chart-title">📈 Multi-Metric Trend Analysis</div>
            <div class="chart-subtitle">Revenue, Costs, and Profit over time</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    fig_multi_line = create_modern_line_chart(
        data=time_series_data,
        x_column='date',
        y_column=['revenue', 'costs', 'profit'],
        title='',
        colors=MODERN_COLORS['rainbow'][:3],
        height=400,
        show_markers=True,
        show_trend=show_trend_lines
    )
    st.plotly_chart(fig_multi_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-header">
        <div>
            <div class="chart-title">💰 Revenue with Trend Line</div>
            <div class="chart-subtitle">Daily revenue with growth projection</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    fig_single_line = create_modern_line_chart(
        data=time_series_data,
        x_column='date',
        y_column='revenue',
        title='',
        colors=[MODERN_COLORS['primary'][0]],
        height=400,
        fill_area=True,
        show_trend=show_trend_lines
    )
    st.plotly_chart(fig_single_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== BAR CHARTS & DONUT ====================

st.markdown("## 🏆 Product Performance Analysis")

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-header">
        <div>
            <div class="chart-title">📊 Revenue by Product</div>
            <div class="chart-subtitle">Top performing products with gradient visualization</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    fig_bar = create_modern_bar_chart(
        data=category_data,
        x_column='product',
        y_column='revenue',
        title='',
        height=400,
        show_values=True,
        gradient=True
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-header">
        <div>
            <div class="chart-title">🥧 Market Share</div>
            <div class="chart-subtitle">Distribution across products</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    fig_donut = create_modern_donut_chart(
        data=category_data,
        values_column='revenue',
        names_column='product',
        title='',
        colors=MODERN_COLORS['rainbow'],
        height=400,
        hole_size=0.6
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== HEATMAP & GAUGES ====================

st.markdown("## 🔥 Cohort Retention & Performance Metrics")

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-header">
        <div>
            <div class="chart-title">🔥 Cohort Retention Heatmap</div>
            <div class="chart-subtitle">Week-over-week retention rates by cohort</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    fig_heatmap = create_modern_heatmap(
        data=retention_data,
        title='',
        colorscale='Blues',
        height=400,
        show_values=True
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-header">
        <div>
            <div class="chart-title">⚡ Performance Score</div>
            <div class="chart-subtitle">Overall KPI achievement</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    fig_gauge1 = create_modern_gauge(
        value=78.5,
        max_value=100,
        title='',
        subtitle='Target: 85%',
        height=200
    )
    st.plotly_chart(fig_gauge1, use_container_width=True)
    
    fig_gauge2 = create_modern_gauge(
        value=92.3,
        max_value=100,
        title='Customer Satisfaction',
        subtitle='Excellent performance',
        height=200
    )
    st.plotly_chart(fig_gauge2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== SCATTER PLOT ====================

st.markdown("## 🎯 Product Performance Matrix")

st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
st.markdown("""
<div class="chart-header">
    <div>
        <div class="chart-title">🎯 ROI vs Market Share Analysis</div>
        <div class="chart-subtitle">Bubble size represents growth rate</div>
    </div>
</div>
""", unsafe_allow_html=True)

fig_scatter = create_modern_scatter(
    data=scatter_data,
    x_column='market_share',
    y_column='roi',
    size_column='growth_rate',
    title='',
    x_label='Market Share (%)',
    y_label='Return on Investment (%)',
    height=450,
    show_trend=show_trend_lines
)
st.plotly_chart(fig_scatter, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== UI COMPONENTS SHOWCASE ====================

st.markdown("## 🎨 Modern UI Components")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card">
        <h3>📊 Glassmorphism Card</h3>
        <p>Modern card design with frosted glass effect and backdrop blur for a contemporary look.</p>
        <div class="progress-bar-container" style="margin-top: 1rem;">
            <div class="progress-fill" style="width: 75%;"></div>
        </div>
        <p style="margin-top: 0.5rem; font-size: 0.875rem; color: #64748b;">75% Complete</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-card-header">
            <div class="stat-icon stat-icon-primary">📈</div>
        </div>
        <div class="stat-value">$284K</div>
        <div class="stat-label">Monthly Revenue</div>
        <div class="stat-change trend-up">↑ +12.5%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="alert-banner alert-success">
        <div>
            <strong>✅ Success!</strong><br>
            <span style="font-size: 0.875rem;">Your data has been updated successfully with modern styling.</span>
        </div>
    </div>
    <div class="alert-banner alert-info">
        <div>
            <strong>ℹ️ Information</strong><br>
            <span style="font-size: 0.875rem;">New features are now available in the dashboard.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== BADGES & STATUS INDICATORS ====================

st.markdown("### Status Indicators & Badges")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="status-badge status-online">
        <span class="status-dot"></span>
        <span>System Online</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <span class="badge-modern badge-gradient">Premium Feature</span>
    <span class="badge-modern badge-success">Active</span>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <span class="trend-indicator trend-up">↑ 15.3%</span>
    <span class="trend-indicator trend-down">↓ 3.2%</span>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <span class="badge-modern badge-primary">New</span>
    <span class="badge-modern badge-warning">Beta</span>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 16px; margin-top: 2rem;">
    <h3 class="gradient-text">✨ Enhanced Visualization Features</h3>
    <p style="color: #64748b; max-width: 700px; margin: 1rem auto;">
        All visualizations feature modern design patterns, enhanced interactivity, 
        smooth animations, and professional color schemes optimized for data clarity.
    </p>
</div>
""", unsafe_allow_html=True)
