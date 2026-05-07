"""
Anomaly Alerts Component

Production-level alert system for displaying anomalies and warnings
in business metrics with interactive UI elements.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime


def display_anomaly_alerts(
    anomalies_data: Dict[str, Any],
    show_details: bool = True,
    max_alerts: int = 5
):
    """
    Display anomaly alerts in an attractive banner format.
    
    Args:
        anomalies_data: Anomaly data from API containing alerts, anomalies, and summary
        show_details: Whether to show detailed anomaly list
        max_alerts: Maximum number of alerts to display in banner
    """
    if not anomalies_data or 'data' not in anomalies_data:
        return
    
    data = anomalies_data['data']
    alerts = data.get('alerts', [])
    anomalies = data.get('anomalies', [])
    summary = data.get('summary', {})
    
    # Display critical alerts in prominent banner
    if alerts:
        st.markdown("### 🚨 Alert Dashboard")
        
        # Show critical alerts
        critical_alerts = [a for a in alerts if a.get('type') == 'critical']
        
        for i, alert in enumerate(critical_alerts[:max_alerts]):
            severity_color = "#ff4b4b"  # Red for critical
            
            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(135deg, {severity_color}15 0%, {severity_color}05 100%);
                        border-left: 5px solid {severity_color};
                        padding: 1rem;
                        border-radius: 5px;
                        margin-bottom: 1rem;
                    ">
                        <h4 style="margin: 0 0 0.5rem 0; color: {severity_color};">
                            {alert['title']}
                        </h4>
                        <p style="margin: 0 0 0.5rem 0; font-size: 0.95rem;">
                            {alert['message']}
                        </p>
                        <p style="margin: 0; font-size: 0.85rem; color: #666;">
                            <b>Recommended Action:</b> {alert['action']}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    # Display summary statistics
    if summary and show_details:
        st.markdown("### 📊 Detection Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Anomalies",
                summary.get('anomalies_detected', 0),
                delta=f"{summary.get('anomaly_rate', 0):.1f}% rate"
            )
        
        with col2:
            st.metric(
                "Data Points",
                summary.get('total_data_points', 0)
            )
        
        with col3:
            st.metric(
                "Method",
                summary.get('method', 'N/A').upper()
            )
        
        with col4:
            st.metric(
                "Threshold",
                f"{summary.get('threshold', 0):.1f}"
            )
    
    # Display detailed anomaly list
    if anomalies and show_details:
        st.markdown("### 📋 Detected Anomalies")
        
        # Convert to DataFrame for better display
        df_anomalies = pd.DataFrame(anomalies)
        
        # Reorder and format columns
        if not df_anomalies.empty:
            display_cols = ['date', 'value', 'type', 'severity', 'deviation_pct', 'anomaly_score']
            df_display = df_anomalies[display_cols].copy()
            
            # Format value column
            df_display['value'] = df_display['value'].apply(lambda x: f"${x:,.2f}")
            
            # Format deviation
            df_display['deviation_pct'] = df_display['deviation_pct'].apply(
                lambda x: f"{x:+.1f}%"
            )
            
            # Format score
            df_display['anomaly_score'] = df_display['anomaly_score'].apply(
                lambda x: f"{x:.2f}"
            )
            
            # Rename columns for display
            df_display.columns = ['Date', 'Value', 'Type', 'Severity', 'Deviation', 'Score']
            
            # Apply styling based on severity
            def highlight_severity(row):
                if row['Severity'] == 'critical':
                    return ['background-color: #ffebee'] * len(row)
                else:
                    return ['background-color: #fff8e1'] * len(row)
            
            styled_df = df_display.style.apply(highlight_severity, axis=1)
            
            st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Download button
            csv = df_anomalies.to_csv(index=False)
            st.download_button(
                label="📥 Download Anomalies Report",
                data=csv,
                file_name=f"anomalies_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )


def display_compact_anomaly_banner(anomalies_data: Dict[str, Any]):
    """
    Display a compact anomaly alert banner for dashboard header.
    
    Args:
        anomalies_data: Anomaly data from API
    """
    if not anomalies_data or 'data' not in anomalies_data:
        return
    
    data = anomalies_data['data']
    alerts = data.get('alerts', [])
    summary = data.get('summary', {})
    
    if not alerts:
        # No critical alerts - show green status
        st.info(
            f"✅ No critical anomalies detected. "
            f"Monitoring {summary.get('total_data_points', 0)} data points "
            f"using {summary.get('method', 'unknown').upper()} method."
        )
        return
    
    # Show alert count and top critical alert
    num_critical = len([a for a in alerts if a.get('type') == 'critical'])
    
    if num_critical > 0:
        top_alert = alerts[0]
        
        with st.container():
            st.error(
                f"⚠️ **{num_critical} Critical Alert{'s' if num_critical > 1 else ''}:** "
                f"{top_alert['title']} | {top_alert['message']}"
            )
            
            # Show expand button
            if num_critical > 1:
                st.caption(f"+ {num_critical - 1} more alert{'s' if num_critical > 1 else ''}")


def create_anomaly_settings_sidebar():
    """
    Create sidebar controls for anomaly detection configuration.
    
    Returns:
        Dictionary with selected settings
    """
    st.sidebar.markdown("### 🔧 Anomaly Detection Settings")
    
    metric = st.sidebar.selectbox(
        "Metric to Analyze",
        options=["revenue", "profit", "transactions", "customers"],
        index=0,
        help="Select which business metric to analyze for anomalies"
    )
    
    method = st.sidebar.selectbox(
        "Detection Method",
        options=["zscore", "iqr", "mad", "moving_avg"],
        index=0,
        format_func=lambda x: {
            "zscore": "Z-Score (Standard)",
            "iqr": "IQR (Interquartile Range)",
            "mad": "MAD (Median Absolute Deviation)",
            "moving_avg": "Moving Average"
        }[x],
        help="Statistical method for detecting anomalies"
    )
    
    threshold = st.sidebar.slider(
        "Sensitivity Threshold",
        min_value=1.0,
        max_value=5.0,
        value=3.0,
        step=0.5,
        help="Higher = less sensitive (fewer alerts). Lower = more sensitive (more alerts)"
    )
    
    period = st.sidebar.selectbox(
        "Analysis Period",
        options=["7d", "30d", "90d"],
        index=1,
        format_func=lambda x: {
            "7d": "Last 7 Days",
            "30d": "Last 30 Days",
            "90d": "Last 90 Days"
        }[x],
        help="Time period to analyze"
    )
    
    limit = st.sidebar.number_input(
        "Max Anomalies to Display",
        min_value=5,
        max_value=50,
        value=10,
        step=5,
        help="Maximum number of anomalies to show"
    )
    
    auto_refresh = st.sidebar.checkbox(
        "Auto-refresh detection",
        value=False,
        help="Automatically refresh anomaly detection every page reload"
    )
    
    return {
        'metric': metric,
        'method': method,
        'threshold': threshold,
        'period': period,
        'limit': limit,
        'auto_refresh': auto_refresh
    }


def display_anomaly_insights(summary: Dict[str, Any]):
    """
    Display insights and recommendations based on detected anomalies.
    
    Args:
        summary: Summary statistics from anomaly detection
    """
    anomaly_rate = summary.get('anomaly_rate', 0)
    
    st.markdown("### 💡 Insights & Recommendations")
    
    if anomaly_rate < 2:
        st.success(
            "**Stable Performance**: Very low anomaly rate indicates consistent, "
            "predictable business metrics. Continue monitoring for any changes."
        )
    elif anomaly_rate < 10:
        st.info(
            "**Normal Variability**: Moderate anomaly rate is typical for most businesses. "
            "Review individual anomalies to identify opportunities or issues."
        )
    else:
        st.warning(
            "**High Variability**: Elevated anomaly rate suggests significant fluctuations. "
            "Consider investigating root causes and implementing stabilization measures."
        )
    
    # Method-specific recommendations
    method = summary.get('method', '')
    
    with st.expander("📚 About This Detection Method"):
        if method == 'zscore':
            st.markdown("""
            **Z-Score Method**
            
            Identifies data points that are unusual compared to the mean and standard deviation.
            
            - **Best for:** Normally distributed data, identifying extreme outliers
            - **Threshold:** Values beyond 3 standard deviations (99.7% confidence)
            - **Sensitivity:** Adjustable via threshold parameter
            """)
        elif method == 'iqr':
            st.markdown("""
            **Interquartile Range (IQR) Method**
            
            Identifies outliers based on the spread between 25th and 75th percentiles.
            
            - **Best for:** Skewed distributions, robust to outliers
            - **Threshold:** 1.5× IQR beyond Q1/Q3 (standard outlier definition)
            - **Sensitivity:** Less affected by extreme values
            """)
        elif method == 'mad':
            st.markdown("""
            **Median Absolute Deviation (MAD) Method**
            
            Robust method using median instead of mean for outlier detection.
            
            - **Best for:** Heavy-tailed distributions, resistant to outliers
            - **Threshold:** Based on modified Z-scores using median
            - **Sensitivity:** Very robust to extreme values
            """)
        elif method == 'moving_avg':
            st.markdown("""
            **Moving Average Method**
            
            Detects anomalies based on deviation from rolling average trend.
            
            - **Best for:** Time-series data, trend detection
            - **Threshold:** Deviations from moving average ± standard deviation
            - **Sensitivity:** Good for detecting sudden changes
            """)
