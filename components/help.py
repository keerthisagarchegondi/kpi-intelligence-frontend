"""
Help and Usage Instructions Component Module

Provides reusable help components, user guides, and tooltips for the KPI Intelligence Platform.
"""

import streamlit as st
from typing import Optional, Dict, List


class HelpContent:
    """Centralized help content for the application"""
    
    DASHBOARD_HELP = {
        "title": "📊 Dashboard Guide",
        "overview": "The Dashboard provides a comprehensive view of your business KPIs and metrics.",
        "sections": [
            {
                "title": "Key Metrics",
                "content": "View high-level KPIs including revenue, retention, churn rate, and active users. Click on any metric card for detailed insights."
            },
            {
                "title": "Date Filters",
                "content": "Use the date range selector to analyze data for specific periods. Choose from predefined ranges or set a custom date range."
            },
            {
                "title": "Data Upload",
                "content": "Upload CSV files with your business data. The system validates and processes files automatically."
            },
            {
                "title": "Anomaly Detection",
                "content": "Automatically identifies unusual patterns in your metrics. Click on anomaly alerts for more details."
            }
        ],
        "tips": [
            "Use the comparison toggle to see period-over-period changes",
            "Export any chart by hovering and clicking the download icon",
            "Set up custom alerts in the sidebar settings"
        ]
    }
    
    REPORTS_HELP = {
        "title": "📋 Reports Guide",
        "overview": "Generate and explore comprehensive reports with advanced filtering and export capabilities.",
        "sections": [
            {
                "title": "Report Types",
                "content": "Choose from Sales Overview, Product Performance, Customer Analytics, Revenue Breakdown, and more. Each report type offers unique insights."
            },
            {
                "title": "Interactive Tables",
                "content": "Tables support global search, column sorting, filtering, and pagination. Click column headers to sort, use the search box to find specific data."
            },
            {
                "title": "Data Export",
                "content": "Export reports in CSV, Excel, or JSON format. Select 'Export' from the menu and choose your preferred format."
            },
            {
                "title": "Filters & Search",
                "content": "Apply advanced filters to narrow down data. Use global search to find across all columns, or use column-specific filters."
            }
        ],
        "tips": [
            "Use column selection to show/hide specific fields",
            "Pagination controls appear for datasets with >10 rows",
            "Download filtered results - only visible data is exported"
        ]
    }
    
    REVENUE_HELP = {
        "title": "💰 Revenue Analytics Guide",
        "overview": "Analyze revenue trends, breakdowns, and performance across different dimensions.",
        "sections": [
            {
                "title": "Revenue Metrics",
                "content": "Track total revenue, average revenue per user (ARPU), growth rate, and transaction volume."
            },
            {
                "title": "Revenue Breakdown",
                "content": "View revenue distribution by product, customer segment, channel, or time period."
            },
            {
                "title": "Trend Analysis",
                "content": "Identify revenue patterns over time with interactive time-series charts."
            },
            {
                "title": "Segment Comparison",
                "content": "Compare revenue performance across different customer segments or product categories."
            }
        ],
        "tips": [
            "Enable comparison mode to see period-over-period changes",
            "Hover over charts for detailed tooltips",
            "Use date filters to zoom into specific time periods"
        ]
    }
    
    RETENTION_HELP = {
        "title": "🔄 Retention Analysis Guide",
        "overview": "Monitor customer retention, analyze churn, and identify at-risk customers.",
        "sections": [
            {
                "title": "Retention Metrics",
                "content": "Track retention rate, churn rate, and customer lifetime value (LTV) across cohorts."
            },
            {
                "title": "Cohort Analysis",
                "content": "View retention heatmaps grouped by monthly, weekly, or quarterly cohorts."
            },
            {
                "title": "Churn Prediction",
                "content": "Identify customers at risk of churning based on behavior patterns and engagement metrics."
            },
            {
                "title": "Churn Reasons",
                "content": "Analyze common reasons for customer churn to inform retention strategies."
            }
        ],
        "tips": [
            "Focus on early cohort retention as a leading indicator",
            "Monitor high-risk churn segments for proactive intervention",
            "Compare retention across different customer acquisition channels"
        ]
    }


def display_help_modal(help_content: Dict, key: str = "help_modal"):
    """
    Display a help modal with comprehensive usage instructions.
    
    Args:
        help_content: Dictionary containing help content (from HelpContent class)
        key: Unique key for the modal
    """
    with st.expander("❓ Need Help? Click here for usage guide", expanded=False):
        st.markdown(f"## {help_content['title']}")
        st.markdown(f"**{help_content['overview']}**")
        st.markdown("---")
        
        # Display sections
        for section in help_content['sections']:
            st.markdown(f"### {section['title']}")
            st.markdown(section['content'])
            st.markdown("")
        
        # Display tips
        if 'tips' in help_content and help_content['tips']:
            st.markdown("### 💡 Pro Tips")
            for tip in help_content['tips']:
                st.markdown(f"- {tip}")


def display_quick_help(message: str, tooltip: Optional[str] = None):
    """
    Display a quick help icon with tooltip.
    
    Args:
        message: Main help message
        tooltip: Optional tooltip text for additional context
    """
    help_text = tooltip if tooltip else message
    st.markdown(f"ℹ️ {message}", help=help_text)


def display_feature_tooltip(feature_name: str, description: str):
    """
    Display a feature tooltip/help text.
    
    Args:
        feature_name: Name of the feature
        description: Description/help text
    """
    st.info(f"**{feature_name}**: {description}")


def create_help_sidebar():
    """Create a comprehensive help sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.markdown("## 📚 Quick Help")
        
        with st.expander("🚀 Getting Started", expanded=False):
            st.markdown("""
            **Welcome to KPI Intelligence!**
            
            1. **Navigate**: Use the sidebar to access different sections
            2. **Filter Data**: Apply date ranges and filters to focus your analysis
            3. **Explore Reports**: View interactive tables and charts
            4. **Export Data**: Download reports in CSV, Excel, or JSON
            5. **Get Insights**: Review automated insights and anomalies
            """)
        
        with st.expander("⌨️ Keyboard Shortcuts", expanded=False):
            st.markdown("""
            - `R` - Rerun the app
            - `Ctrl/Cmd + K` - Focus search
            - `Ctrl/Cmd + Shift + F` - Toggle fullscreen
            - `Ctrl/Cmd + S` - Save/screenshot
            """)
        
        with st.expander("🔧 Troubleshooting", expanded=False):
            st.markdown("""
            **Common Issues:**
            
            - **Data not loading?** Check your backend connection in Service Status
            - **Filters not working?** Click 'Apply Filters' button
            - **Export failed?** Try reducing the date range
            - **Slow performance?** Enable data sampling in settings
            
            For more help, check the full documentation.
            """)


def display_onboarding_guide():
    """Display a one-time onboarding guide for new users"""
    if "onboarding_complete" not in st.session_state:
        st.session_state.onboarding_complete = False
    
    if not st.session_state.onboarding_complete:
        st.info("""
        ### 👋 Welcome to KPI Intelligence Platform!
        
        This is your first time here. Let's take a quick tour:
        
        1. **Dashboard** - View your key business metrics at a glance
        2. **Reports** - Generate detailed reports with interactive tables
        3. **Revenue** - Analyze revenue trends and breakdowns
        4. **Retention** - Monitor customer retention and churn
        5. **Service Status** - Check API integration status
        
        Click below to dismiss this message.
        """)
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("✅ Got it!", key="dismiss_onboarding"):
                st.session_state.onboarding_complete = True
                st.rerun()
        with col2:
            if st.button("📚 Show Guide", key="show_full_guide"):
                st.session_state.show_user_guide = True
                st.session_state.onboarding_complete = True
                st.rerun()


def display_user_guide_page():
    """Display a comprehensive user guide page"""
    st.title("📚 KPI Intelligence - User Guide")
    st.markdown("---")
    
    # Table of contents
    st.markdown("## 📖 Table of Contents")
    st.markdown("""
    1. [Getting Started](#getting-started)
    2. [Dashboard Overview](#dashboard-overview)
    3. [Reports & Tables](#reports-tables)
    4. [Revenue Analytics](#revenue-analytics)
    5. [Retention Analysis](#retention-analysis)
    6. [Data Export](#data-export)
    7. [Tips & Tricks](#tips-tricks)
    8. [Troubleshooting](#troubleshooting)
    """)
    
    st.markdown("---")
    
    # Getting Started
    st.markdown("## 🚀 Getting Started")
    st.markdown("""
    Welcome to the KPI Intelligence Platform! This guide will help you make the most of the application.
    
    ### Navigation
    Use the **sidebar** (left side) to navigate between different sections:
    - **Dashboard**: High-level KPI overview
    - **Reports**: Detailed data tables and reports
    - **Revenue**: Revenue analytics and trends
    - **Retention**: Customer retention and churn analysis
    - **Service Status**: Backend integration monitoring
    
    ### Basic Workflow
    1. Select a section from the sidebar
    2. Apply date filters to focus your analysis
    3. Explore interactive visualizations
    4. Export data as needed
    """)
    
    st.markdown("---")
    
    # Dashboard Overview
    st.markdown("## 📊 Dashboard Overview")
    st.markdown("""
    The Dashboard provides a real-time view of your key business metrics.
    
    ### Key Features
    - **Metric Cards**: High-level KPIs with trend indicators
    - **Charts**: Interactive visualizations of revenue, products, and segments
    - **Date Filters**: Analyze specific time periods
    - **Anomaly Detection**: Automatic identification of unusual patterns
    - **Data Upload**: Import your own CSV data files
    
    ### Using Date Filters
    1. Click on the date range dropdown
    2. Choose a predefined range (Last 7/30/90 days) or select "Custom Range"
    3. For custom ranges, pick start and end dates
    4. Click "Apply Filters" to update the dashboard
    """)
    
    st.markdown("---")
    
    # Reports & Tables
    st.markdown("## 📋 Reports & Tables")
    st.markdown("""
    The Reports section offers detailed data tables with advanced features.
    
    ### Report Types
    - **Sales Overview**: Comprehensive sales metrics
    - **Product Performance**: Product-level analytics
    - **Customer Analytics**: Customer behavior and segmentation
    - **Revenue Breakdown**: Revenue analysis by dimensions
    - **Top Performers**: Rankings by various metrics
    - **KPI Summary**: Aggregated business metrics
    
    ### Table Features
    - **Search**: Use the global search box to filter across all columns
    - **Sort**: Click any column header to sort ascending/descending
    - **Filter**: Apply column-specific filters via "Advanced Filters"
    - **Columns**: Show/hide specific columns using the column selector
    - **Pagination**: Navigate large datasets with page controls
    - **Export**: Download filtered data in CSV, Excel, or JSON
    
    ### How to Filter Data
    1. Enter search terms in the global search box, OR
    2. Click "Advanced Filters" to set column-specific filters
    3. Select columns to display using the "Columns" menu
    4. Use pagination controls to navigate through results
    """)
    
    st.markdown("---")
    
    # Export section
    st.markdown("## 📥 Data Export")
    st.markdown("""
    Export your data in multiple formats for further analysis.
    
    ### Export Formats
    - **CSV**: Plain text, compatible with Excel and most tools
    - **Excel**: Full formatting with proper column types
    - **JSON**: Structured data for programmatic use
    
    ### How to Export
    1. Apply any filters you want (exported data includes only filtered results)
    2. Click the "Export" menu or button
    3. Select your preferred format
    4. The file will download automatically
    
    ### Export Tips
    - Exported files include only the currently filtered/visible data
    - For large datasets, apply filters first to reduce file size
    - Excel exports preserve formatting and data types
    """)
    
    st.markdown("---")
    
    # Tips & Tricks
    st.markdown("## 💡 Tips & Tricks")
    st.markdown("""
    ### Power User Tips
    - **Quick Refresh**: Press `R` to reload the current page
    - **Compare Periods**: Enable comparison mode to see period-over-period changes
    - **Drill Down**: Click on chart elements to see detailed breakdowns
    - **Bookmark Views**: Use browser bookmarks to save specific filtered views
    
    ### Best Practices
    - Start with the Dashboard for a high-level overview
    - Use date filters to focus on relevant time periods
    - Export filtered data for offline analysis
    - Check Service Status if data isn't loading
    - Review anomaly alerts regularly for unusual patterns
    
    ### Performance
    - For better performance with large datasets, use shorter date ranges
    - Enable data sampling for very large reports
    - Clear browser cache if experiencing slowness
    """)
    
    st.markdown("---")
    
    # Troubleshooting
    st.markdown("## 🔧 Troubleshooting")
    st.markdown("""
    ### Common Issues and Solutions
    
    **Problem: Data not loading**
    - Check the Service Status page for backend connectivity
    - Verify your network connection
    - Try refreshing the page (press `R`)
    
    **Problem: Filters not applying**
    - Ensure you clicked the "Apply Filters" button
    - Check that your date range is valid (start before end)
    - Try resetting filters with the "Reset" button
    
    **Problem: Export not working**
    - Try reducing your date range to limit data size
    - Check browser console for errors
    - Ensure popup blockers aren't preventing downloads
    
    **Problem: Slow performance**
    - Use shorter date ranges
    - Apply filters to reduce dataset size
    - Close other browser tabs to free up memory
    - Clear browser cache and reload
    
    **Problem: Charts not displaying**
    - Ensure JavaScript is enabled in your browser
    - Try a different browser (Chrome, Firefox, Edge recommended)
    - Check browser console for errors
    
    ### Still Need Help?
    If you continue experiencing issues:
    - Check the system status and error messages
    - Review the backend logs for API errors
    - Contact your system administrator
    """)
    
    st.markdown("---")
    st.success("📚 You've reached the end of the guide! Happy analyzing! 🎉")


def add_inline_help(text: str, help_text: str = ""):
    """
    Add inline help icon with tooltip.
    
    Args:
        text: Main text to display
        help_text: Help tooltip text
    """
    col1, col2 = st.columns([0.95, 0.05])
    with col1:
        st.markdown(text)
    with col2:
        st.markdown("ℹ️", help=help_text)
