"""
Components Package

Reusable UI components for the KPI Intelligence Platform.
"""

from .charts import *
from .filters import *
from .alerts import *
from .tables import *
from .loading import *
from .errors import *

__all__ = [
    # Chart components
    'create_revenue_trend_chart',
    'create_revenue_breakdown_chart',
    'create_product_revenue_chart',
    # Filter components
    'render_date_range_filter',
    'get_filter_summary',
    # Alert components
    'display_compact_anomaly_banner',
    'display_anomaly_alerts',
    # Table components
    'create_interactive_table',
    'create_summary_table',
    'create_comparison_table',
    'create_pivot_table',
    # Loading components
    'loading_spinner',
    'show_loading_card',
    'show_data_loading_placeholder',
    'show_skeleton_loader',
    'LoadingState',
    'MultiStageLoader',
    # Error components
    'error_handler',
    'show_error_message',
    'show_error_card',
    'handle_api_error',
    'ErrorMessage',
    'ErrorCategory',
    'ErrorSeverity',
    'safe_execute'
]
