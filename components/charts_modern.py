"""
Enhanced Chart Components with Modern Plotly Configurations

This module provides advanced visualization components with improved aesthetics,
interactivity, and modern design patterns for the KPI Intelligence Platform.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Union


# ==================== MODERN COLOR SCHEMES ====================

MODERN_COLORS = {
    'primary': ['#3b82f6', '#2563eb', '#1d4ed8', '#1e40af', '#1e3a8a'],
    'success': ['#10b981', '#059669', '#047857', '#065f46', '#064e3b'],
    'warning': ['#f59e0b', '#d97706', '#b45309', '#92400e', '#78350f'],
    'danger': ['#ef4444', '#dc2626', '#b91c1c', '#991b1b', '#7f1d1d'],
    'info': ['#06b6d4', '#0891b2', '#0e7490', '#155e75', '#164e63'],
    'purple': ['#8b5cf6', '#7c3aed', '#6d28d9', '#5b21b6', '#4c1d95'],
    'gradient_blue': ['#667eea', '#764ba2'],
    'gradient_green': ['#4facfe', '#00f2fe'],
    'gradient_warm': ['#fa709a', '#fee140'],
    'rainbow': ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444', '#06b6d4', '#ec4899', '#14b8a6']
}

# Modern layout template
MODERN_LAYOUT = dict(
    font=dict(
        family='-apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif',
        size=14,
        color='#1e293b'
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    hovermode='x unified',
    hoverlabel=dict(
        bgcolor='white',
        font_size=13,
        font_family='-apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif',
        bordercolor='#e2e8f0'
    ),
    margin=dict(l=60, r=40, t=80, b=60),
    showlegend=True,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        bgcolor='rgba(255, 255, 255, 0.9)',
        bordercolor='#e2e8f0',
        borderwidth=1
    ),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='#e2e8f0',
        tickfont=dict(size=12, color='#64748b')
    ),
    yaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='#f1f5f9',
        showline=True,
        linewidth=1,
        linecolor='#e2e8f0',
        tickfont=dict(size=12, color='#64748b')
    )
)


# ==================== ENHANCED LINE CHARTS ====================

def create_modern_line_chart(
    data: pd.DataFrame,
    x_column: str,
    y_column: Union[str, List[str]],
    title: str = 'Line Chart',
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    colors: Optional[List[str]] = None,
    height: int = 450,
    show_markers: bool = True,
    fill_area: bool = False,
    show_trend: bool = False,
    animate: bool = False
) -> go.Figure:
    """
    Create a modern, interactive line chart with enhanced styling.
    
    Args:
        data: DataFrame containing the data
        x_column: Name of the x-axis column
        y_column: Name of y-axis column(s) - can be string or list for multiple lines
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        colors: List of colors (uses modern palette if None)
        height: Chart height in pixels
        show_markers: Whether to show data point markers
        fill_area: Whether to fill area under the line
        show_trend: Whether to show trend line
        animate: Whether to animate the chart on load
    
    Returns:
        Plotly Figure object
    """
    # Handle single or multiple y columns
    y_columns = [y_column] if isinstance(y_column, str) else y_column
    
    # Use modern colors if none provided
    if colors is None:
        colors = MODERN_COLORS['rainbow']
    
    fig = go.Figure()
    
    # Add traces for each y column
    for idx, col in enumerate(y_columns):
        color = colors[idx % len(colors)]
        mode = 'lines+markers' if show_markers else 'lines'
        
        fig.add_trace(go.Scatter(
            x=data[x_column],
            y=data[col],
            mode=mode,
            name=col,
            line=dict(color=color, width=3, shape='spline'),
            marker=dict(
                size=8,
                color=color,
                line=dict(width=2, color='white'),
                opacity=0.9
            ),
            fill='tozeroy' if fill_area and len(y_columns) == 1 else None,
            fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1)' if fill_area and color.startswith('#') else None,
            hovertemplate='<b>%{x}</b><br>' + col + ': %{y:,.2f}<extra></extra>'
        ))
        
        # Add trend line if requested
        if show_trend:
            z = np.polyfit(range(len(data)), data[col], 1)
            p = np.poly1d(z)
            fig.add_trace(go.Scatter(
                x=data[x_column],
                y=p(range(len(data))),
                mode='lines',
                name=f'{col} Trend',
                line=dict(color=color, width=2, dash='dash'),
                opacity=0.5,
                showlegend=True,
                hovertemplate='<b>Trend</b><br>%{y:,.2f}<extra></extra>'
            ))
    
    # Update layout with modern styling
    layout_update = MODERN_LAYOUT.copy()
    layout_update.update({
        'title': dict(
            text=f'<b>{title}</b>',
            font=dict(size=20, family=MODERN_LAYOUT['font']['family'], color='#1e293b'),
            x=0.02,
            xanchor='left'
        ),
        'xaxis_title': x_label or x_column,
        'yaxis_title': y_label or y_column if isinstance(y_column, str) else 'Value',
        'height': height,
    })
    
    fig.update_layout(**layout_update)
    
    # Add animation if requested
    if animate:
        fig.update_traces(
            marker=dict(size=8),
            selector=dict(mode='lines+markers')
        )
    
    # Add range slider for time series
    if 'date' in x_column.lower() or 'time' in x_column.lower():
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label='1w', step='day', stepmode='backward'),
                    dict(count=1, label='1m', step='month', stepmode='backward'),
                    dict(count=3, label='3m', step='month', stepmode='backward'),
                    dict(step='all', label='All')
                ]),
                bgcolor='#f8fafc',
                activecolor='#3b82f6',
                font=dict(color='#64748b')
            )
        )
    
    return fig


# ==================== ENHANCED BAR CHARTS ====================

def create_modern_bar_chart(
    data: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str = 'Bar Chart',
    orientation: str = 'v',
    color_column: Optional[str] = None,
    colors: Optional[List[str]] = None,
    height: int = 450,
    show_values: bool = True,
    gradient: bool = True
) -> go.Figure:
    """
    Create a modern bar chart with gradient colors and enhanced interactivity.
    
    Args:
        data: DataFrame containing the data
        x_column: Name of the x-axis column
        y_column: Name of the y-axis column
        title: Chart title
        orientation: 'v' for vertical, 'h' for horizontal
        color_column: Column to use for color mapping
        colors: List of colors (uses modern palette if None)
        height: Chart height in pixels
        show_values: Whether to show value labels on bars
        gradient: Whether to use gradient colors
    
    Returns:
        Plotly Figure object
    """
    # Use modern colors if none provided
    if colors is None:
        colors = MODERN_COLORS['primary'] if not gradient else MODERN_COLORS['rainbow']
    
    # Create color scale based on values if gradient is True
    if gradient and color_column is None:
        color_scale = data[y_column]
    elif color_column:
        color_scale = data[color_column]
    else:
        color_scale = None
    
    if orientation == 'v':
        x, y = data[x_column], data[y_column]
        text_position = 'outside'
    else:
        x, y = data[y_column], data[x_column]
        text_position = 'outside'
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=x if orientation == 'v' else y,
        y=y if orientation == 'v' else x,
        orientation=orientation,
        text=y.apply(lambda v: f'{v:,.0f}') if show_values else None,
        textposition=text_position,
        textfont=dict(size=12, color='#64748b', family=MODERN_LAYOUT['font']['family']),
        marker=dict(
            color=color_scale if color_scale is not None else colors[0],
            colorscale='Blues' if gradient and color_scale is not None else None,
            showscale=False,
            line=dict(width=0),
            opacity=0.9
        ),
        hovertemplate='<b>%{x}</b><br>Value: %{y:,.2f}<extra></extra>' if orientation == 'v' else '<b>%{y}</b><br>Value: %{x:,.2f}<extra></extra>'
    ))
    
    # Update layout
    layout_update = MODERN_LAYOUT.copy()
    layout_update.update({
        'title': dict(
            text=f'<b>{title}</b>',
            font=dict(size=20, family=MODERN_LAYOUT['font']['family'], color='#1e293b'),
            x=0.02,
            xanchor='left'
        ),
        'height': height,
        'showlegend': False,
        'bargap': 0.15,
        'bargroupgap': 0.1
    })
    
    fig.update_layout(**layout_update)
    
    # Add gridlines only for value axis
    if orientation == 'v':
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9')
    else:
        fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9')
        fig.update_yaxes(showgrid=False)
    
    return fig


# ==================== ENHANCED PIE/DONUT CHARTS ====================

def create_modern_donut_chart(
    data: pd.DataFrame,
    values_column: str,
    names_column: str,
    title: str = 'Distribution',
    colors: Optional[List[str]] = None,
    height: int = 450,
    hole_size: float = 0.5,
    show_legend: bool = True
) -> go.Figure:
    """
    Create a modern donut chart with enhanced styling.
    
    Args:
        data: DataFrame containing the data
        values_column: Column containing values
        names_column: Column containing category names
        title: Chart title
        colors: List of colors (uses modern palette if None)
        height: Chart height in pixels
        hole_size: Size of the center hole (0-1)
        show_legend: Whether to show legend
    
    Returns:
        Plotly Figure object
    """
    if colors is None:
        colors = MODERN_COLORS['rainbow']
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=data[names_column],
        values=data[values_column],
        hole=hole_size,
        marker=dict(
            colors=colors,
            line=dict(color='white', width=3)
        ),
        textposition='auto',
        textinfo='label+percent',
        textfont=dict(size=13, color='white', family=MODERN_LAYOUT['font']['family']),
        hovertemplate='<b>%{label}</b><br>Value: %{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
    ))
    
    # Add center annotation
    total = data[values_column].sum()
    fig.add_annotation(
        text=f'<b>Total</b><br>{total:,.0f}',
        x=0.5,
        y=0.5,
        font=dict(size=18, color='#1e293b', family=MODERN_LAYOUT['font']['family']),
        showarrow=False
    )
    
    layout_update = {
        'title': dict(
            text=f'<b>{title}</b>',
            font=dict(size=20, family=MODERN_LAYOUT['font']['family'], color='#1e293b'),
            x=0.02,
            xanchor='left'
        ),
        'height': height,
        'showlegend': show_legend,
        'legend': dict(
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=1.05,
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='#e2e8f0',
            borderwidth=1,
            font=dict(size=12, color='#64748b')
        ),
        'paper_bgcolor': 'white',
        'margin': dict(l=40, r=150, t=80, b=40)
    }
    
    fig.update_layout(**layout_update)
    
    return fig


# ==================== ENHANCED GAUGE CHARTS ====================

def create_modern_gauge(
    value: float,
    max_value: float = 100,
    title: str = 'Performance',
    subtitle: Optional[str] = None,
    thresholds: Optional[Dict[str, float]] = None,
    height: int = 300
) -> go.Figure:
    """
    Create a modern gauge chart with color-coded zones.
    
    Args:
        value: Current value
        max_value: Maximum value for the gauge
        title: Gauge title
        subtitle: Optional subtitle
        thresholds: Dict with 'low', 'medium', 'high' thresholds
        height: Chart height in pixels
    
    Returns:
        Plotly Figure object
    """
    if thresholds is None:
        thresholds = {'low': max_value * 0.3, 'medium': max_value * 0.7, 'high': max_value}
    
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode='gauge+number+delta',
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f'<b>{title}</b>', 'font': {'size': 18, 'color': '#1e293b'}},
        number={'font': {'size': 48, 'color': '#3b82f6'}, 'suffix': '%' if max_value == 100 else ''},
        delta={'reference': thresholds['medium'], 'increasing': {'color': '#10b981'}, 'decreasing': {'color': '#ef4444'}},
        gauge={
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': '#64748b'},
            'bar': {'color': '#3b82f6', 'thickness': 0.75},
            'bgcolor': 'white',
            'borderwidth': 2,
            'bordercolor': '#e2e8f0',
            'steps': [
                {'range': [0, thresholds['low']], 'color': '#fee2e2'},
                {'range': [thresholds['low'], thresholds['medium']], 'color': '#fef3c7'},
                {'range': [thresholds['medium'], thresholds['high']], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': '#ef4444', 'width': 4},
                'thickness': 0.75,
                'value': thresholds['medium']
            }
        }
    ))
    
    fig.update_layout(
        height=height,
        paper_bgcolor='white',
        font={'family': MODERN_LAYOUT['font']['family'], 'color': '#64748b'},
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    if subtitle:
        fig.add_annotation(
            text=subtitle,
            xref='paper',
            yref='paper',
            x=0.5,
            y=-0.1,
            showarrow=False,
            font=dict(size=14, color='#64748b')
        )
    
    return fig


# ==================== HEATMAP CHARTS ====================

def create_modern_heatmap(
    data: pd.DataFrame,
    title: str = 'Heatmap',
    colorscale: str = 'Blues',
    height: int = 500,
    show_values: bool = True
) -> go.Figure:
    """
    Create a modern heatmap with enhanced styling.
    
    Args:
        data: DataFrame where index is y-axis and columns are x-axis
        title: Chart title
        colorscale: Plotly colorscale name
        height: Chart height in pixels
        show_values: Whether to show values in cells
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    fig.add_trace(go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale=colorscale,
        text=data.values if show_values else None,
        texttemplate='%{text:.1f}%' if show_values else None,
        textfont={'size': 12, 'color': 'white'},
        hovertemplate='<b>%{y}</b><br>%{x}: %{z:.1f}%<extra></extra>',
        colorbar=dict(
            title='Value',
            ticksuffix='%',
            thickness=15,
            len=0.7,
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='#e2e8f0',
            borderwidth=1
        )
    ))
    
    fig.update_layout(
        title=dict(
            text=f'<b>{title}</b>',
            font=dict(size=20, family=MODERN_LAYOUT['font']['family'], color='#1e293b'),
            x=0.02,
            xanchor='left'
        ),
        height=height,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'family': MODERN_LAYOUT['font']['family'], 'color': '#64748b'},
        xaxis=dict(side='bottom', tickangle=-45, tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
        margin=dict(l=100, r=80, t=80, b=100)
    )
    
    return fig


# ==================== SCATTER PLOTS ====================

def create_modern_scatter(
    data: pd.DataFrame,
    x_column: str,
    y_column: str,
    size_column: Optional[str] = None,
    color_column: Optional[str] = None,
    title: str = 'Scatter Plot',
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    height: int = 500,
    show_trend: bool = True
) -> go.Figure:
    """
    Create a modern scatter plot with optional sizing and coloring.
    
    Args:
        data: DataFrame containing the data
        x_column: X-axis column name
        y_column: Y-axis column name
        size_column: Optional column for bubble sizes
        color_column: Optional column for color coding
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        height: Chart height in pixels
        show_trend: Whether to show trend line
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    # Determine marker size
    marker_size = data[size_column] if size_column else 10
    
    # Determine marker color
    if color_column:
        marker_color = data[color_column]
        colorscale = 'Viridis'
    else:
        marker_color = MODERN_COLORS['primary'][0]
        colorscale = None
    
    fig.add_trace(go.Scatter(
        x=data[x_column],
        y=data[y_column],
        mode='markers',
        marker=dict(
            size=marker_size,
            color=marker_color,
            colorscale=colorscale,
            showscale=color_column is not None,
            line=dict(width=1, color='white'),
            opacity=0.8,
            colorbar=dict(title=color_column, thickness=15, len=0.7) if color_column else None
        ),
        text=data.index if hasattr(data, 'index') else None,
        hovertemplate='<b>%{text}</b><br>' +
                      f'{x_column}: %{{x:.2f}}<br>' +
                      f'{y_column}: %{{y:.2f}}<extra></extra>'
    ))
    
    # Add trend line
    if show_trend:
        z = np.polyfit(data[x_column], data[y_column], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(data[x_column].min(), data[x_column].max(), 100)
        
        fig.add_trace(go.Scatter(
            x=x_trend,
            y=p(x_trend),
            mode='lines',
            name='Trend',
            line=dict(color='#ef4444', width=2, dash='dash'),
            opacity=0.6,
            showlegend=True
        ))
    
    # Update layout
    layout_update = MODERN_LAYOUT.copy()
    layout_update.update({
        'title': dict(
            text=f'<b>{title}</b>',
            font=dict(size=20, family=MODERN_LAYOUT['font']['family'], color='#1e293b'),
            x=0.02,
            xanchor='left'
        ),
        'xaxis_title': x_label or x_column,
        'yaxis_title': y_label or y_column,
        'height': height,
    })
    
    fig.update_layout(**layout_update)
    
    return fig
