"""
Error Handling Component Module

Production-level error display and handling:
- Categorized error messages
- User-friendly error displays
- Error recovery suggestions
- Error logging
- Retry mechanisms
"""

import streamlit as st
import traceback
from typing import Optional, Dict, Any, Callable, List
from datetime import datetime
from enum import Enum
import logging


class ErrorSeverity(Enum):
    """Error severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for better handling"""
    NETWORK = "network"
    API = "api"
    VALIDATION = "validation"
    DATA = "data"
    PERMISSION = "permission"
    TIMEOUT = "timeout"
    NOT_FOUND = "not_found"
    SERVER = "server"
    CLIENT = "client"
    UNKNOWN = "unknown"


class ErrorMessage:
    """
    Structured error message with metadata.
    """
    
    def __init__(
        self,
        message: str,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        details: Optional[str] = None,
        suggestions: Optional[List[str]] = None,
        technical_details: Optional[str] = None,
        can_retry: bool = False
    ):
        self.message = message
        self.category = category
        self.severity = severity
        self.details = details
        self.suggestions = suggestions or []
        self.technical_details = technical_details
        self.can_retry = can_retry
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'message': self.message,
            'category': self.category.value,
            'severity': self.severity.value,
            'details': self.details,
            'suggestions': self.suggestions,
            'technical_details': self.technical_details,
            'can_retry': self.can_retry,
            'timestamp': self.timestamp.isoformat()
        }


class ErrorHandler:
    """
    Global error handler with logging and recovery.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_history = []
    
    def handle_error(
        self,
        error: Exception,
        context: str = "",
        show_ui: bool = True,
        log_error: bool = True
    ) -> ErrorMessage:
        """
        Handle an error with appropriate logging and UI display.
        
        Args:
            error: Exception to handle
            context: Context where error occurred
            show_ui: Whether to show error in UI
            log_error: Whether to log the error
        
        Returns:
            ErrorMessage object
        """
        error_msg = self._categorize_error(error, context)
        
        if log_error:
            self._log_error(error, error_msg, context)
        
        if show_ui:
            show_error_message(error_msg)
        
        self.error_history.append(error_msg)
        
        return error_msg
    
    def _categorize_error(self, error: Exception, context: str) -> ErrorMessage:
        """Categorize and create error message"""
        error_type = type(error).__name__
        error_str = str(error)
        
        # Network errors
        if "ConnectionError" in error_type or "connection" in error_str.lower():
            return ErrorMessage(
                message="Unable to connect to the server",
                category=ErrorCategory.NETWORK,
                severity=ErrorSeverity.ERROR,
                details=f"Network connection failed: {error_str}",
                suggestions=[
                    "Check your internet connection",
                    "Verify the server is running",
                    "Check if the server URL is correct"
                ],
                technical_details=f"{error_type}: {error_str}",
                can_retry=True
            )
        
        # Timeout errors
        elif "Timeout" in error_type or "timeout" in error_str.lower():
            return ErrorMessage(
                message="Request timed out",
                category=ErrorCategory.TIMEOUT,
                severity=ErrorSeverity.WARNING,
                details="The operation took too long to complete",
                suggestions=[
                    "Try again with a smaller dataset",
                    "Check your network connection",
                    "The server might be busy, try again later"
                ],
                technical_details=f"{error_type}: {error_str}",
                can_retry=True
            )
        
        # API errors
        elif "API" in context or "api" in error_str.lower():
            return ErrorMessage(
                message="API request failed",
                category=ErrorCategory.API,
                severity=ErrorSeverity.ERROR,
                details=f"Failed to fetch data from API: {error_str}",
                suggestions=[
                    "Check API endpoint configuration",
                    "Verify API is accessible",
                    "Using fallback sample data"
                ],
                technical_details=f"{error_type}: {error_str}",
                can_retry=True
            )
        
        # Validation errors
        elif "Validation" in error_type or "invalid" in error_str.lower():
            return ErrorMessage(
                message="Validation error",
                category=ErrorCategory.VALIDATION,
                severity=ErrorSeverity.WARNING,
                details=f"Data validation failed: {error_str}",
                suggestions=[
                    "Check your input data",
                    "Ensure all required fields are filled",
                    "Verify data format is correct"
                ],
                technical_details=f"{error_type}: {error_str}",
                can_retry=False
            )
        
        # Data errors
        elif "KeyError" in error_type or "ValueError" in error_type:
            return ErrorMessage(
                message="Data processing error",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.ERROR,
                details=f"Error processing data: {error_str}",
                suggestions=[
                    "Check if the data format is correct",
                    "Verify all required columns exist",
                    "Try refreshing the data"
                ],
                technical_details=f"{error_type}: {error_str}",
                can_retry=True
            )
        
        # Permission errors
        elif "Permission" in error_type or "Forbidden" in error_str:
            return ErrorMessage(
                message="Permission denied",
                category=ErrorCategory.PERMISSION,
                severity=ErrorSeverity.ERROR,
                details="You don't have permission to perform this action",
                suggestions=[
                    "Contact your administrator",
                    "Check your access rights",
                    "You may need to log in again"
                ],
                technical_details=f"{error_type}: {error_str}",
                can_retry=False
            )
        
        # Not found errors
        elif "NotFound" in error_type or "404" in error_str:
            return ErrorMessage(
                message="Resource not found",
                category=ErrorCategory.NOT_FOUND,
                severity=ErrorSeverity.WARNING,
                details=f"The requested resource was not found: {error_str}",
                suggestions=[
                    "Check if the resource ID is correct",
                    "The resource may have been deleted",
                    "Try searching for the resource"
                ],
                technical_details=f"{error_type}: {error_str}",
                can_retry=False
            )
        
        # Server errors
        elif "500" in error_str or "502" in error_str or "503" in error_str:
            return ErrorMessage(
                message="Server error",
                category=ErrorCategory.SERVER,
                severity=ErrorSeverity.CRITICAL,
                details="The server encountered an error",
                suggestions=[
                    "Try again in a few minutes",
                    "Contact support if the issue persists",
                    "Using fallback data for now"
                ],
                technical_details=f"{error_type}: {error_str}",
                can_retry=True
            )
        
        # Unknown errors
        else:
            return ErrorMessage(
                message="An unexpected error occurred",
                category=ErrorCategory.UNKNOWN,
                severity=ErrorSeverity.ERROR,
                details=f"Error: {error_str}",
                suggestions=[
                    "Try refreshing the page",
                    "Contact support if the issue persists"
                ],
                technical_details=f"{error_type}: {error_str}\n{traceback.format_exc()}",
                can_retry=True
            )
    
    def _log_error(self, error: Exception, error_msg: ErrorMessage, context: str):
        """Log error to logging system"""
        log_message = f"[{context}] {error_msg.message}: {error_msg.details}"
        
        if error_msg.severity == ErrorSeverity.CRITICAL:
            self.logger.critical(log_message, exc_info=True)
        elif error_msg.severity == ErrorSeverity.ERROR:
            self.logger.error(log_message, exc_info=True)
        elif error_msg.severity == ErrorSeverity.WARNING:
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
    
    def get_error_history(self, limit: int = 10) -> List[ErrorMessage]:
        """Get recent error history"""
        return self.error_history[-limit:]
    
    def clear_error_history(self):
        """Clear error history"""
        self.error_history = []


# Global error handler instance
error_handler = ErrorHandler()


def show_error_message(
    error_msg: ErrorMessage,
    show_suggestions: bool = True,
    show_technical: bool = False,
    collapsible: bool = True
) -> None:
    """
    Display error message in Streamlit UI with severity-based styling.
    
    Args:
        error_msg: ErrorMessage object
        show_suggestions: Whether to show recovery suggestions
        show_technical: Whether to show technical details
        collapsible: Whether to make details collapsible
    """
    
    # Enhanced CSS styling for better visual polish
    st.markdown("""
    <style>
        .error-card {
            padding: 1.25rem;
            border-radius: 8px;
            border-left: 4px solid;
            margin: 1rem 0;
            animation: slideIn 0.3s ease-out;
        }
        .error-card.info {
            background-color: #e3f2fd;
            border-color: #2196f3;
            color: #0d47a1;
        }
        .error-card.warning {
            background-color: #fff3e0;
            border-color: #ff9800;
            color: #e65100;
        }
        .error-card.error {
            background-color: #ffebee;
            border-color: #f44336;
            color: #b71c1c;
        }
        .error-card.critical {
            background-color: #fce4ec;
            border-color: #e91e63;
            color: #880e4f;
            font-weight: 600;
        }
        @keyframes slideIn {
            from {
                transform: translateX(-20px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Choose display method based on severity
    if error_msg.severity == ErrorSeverity.INFO:
        st.info(f"ℹ️ {error_msg.message}")
    elif error_msg.severity == ErrorSeverity.WARNING:
        st.warning(f"⚠️ {error_msg.message}")
    elif error_msg.severity == ErrorSeverity.ERROR:
        st.error(f"❌ {error_msg.message}")
    elif error_msg.severity == ErrorSeverity.CRITICAL:
        st.error(f"🚨 CRITICAL: {error_msg.message}")
    
    # Show details in expander or directly
    if error_msg.details or show_suggestions or show_technical:
        if collapsible:
            with st.expander("📋 Error Details", expanded=False):
                _show_error_details(error_msg, show_suggestions, show_technical)
        else:
            _show_error_details(error_msg, show_suggestions, show_technical)


def _show_error_details(
    error_msg: ErrorMessage,
    show_suggestions: bool,
    show_technical: bool
):
    """Show error details content"""
    
    if error_msg.details:
        st.markdown(f"**Details:** {error_msg.details}")
    
    if show_suggestions and error_msg.suggestions:
        st.markdown("**💡 Suggestions:**")
        for suggestion in error_msg.suggestions:
            st.markdown(f"- {suggestion}")
    
    if error_msg.can_retry:
        st.info("🔄 This operation can be retried")
    
    if show_technical and error_msg.technical_details:
        with st.expander("🔧 Technical Details", expanded=False):
            st.code(error_msg.technical_details, language="text")


def show_error_banner(
    message: str,
    error_type: str = "error",
    dismissible: bool = True,
    key: str = "error_banner"
) -> None:
    """
    Show prominent error banner at top of page.
    
    Args:
        message: Error message
        error_type: Type of error ('error', 'warning', 'info')
        dismissible: Whether user can dismiss
        key: Unique key for this banner
    """
    
    # Check if dismissed
    if dismissible and st.session_state.get(f"dismissed_{key}", False):
        return
    
    colors = {
        'error': {'bg': '#fee', 'border': '#f00', 'icon': '❌'},
        'warning': {'bg': '#ffe', 'border': '#f90', 'icon': '⚠️'},
        'info': {'bg': '#eff', 'border': '#09f', 'icon': 'ℹ️'}
    }
    
    color = colors.get(error_type, colors['error'])
    
    st.markdown(f"""
    <div style="background: {color['bg']}; border-left: 4px solid {color['border']}; 
                padding: 1rem; margin: 1rem 0; border-radius: 4px;">
        <strong>{color['icon']} {message}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    if dismissible:
        if st.button("✖ Dismiss", key=f"dismiss_{key}"):
            st.session_state[f"dismissed_{key}"] = True
            st.rerun()


def show_error_card(
    title: str,
    message: str,
    suggestions: Optional[List[str]] = None,
    show_retry: bool = False,
    retry_callback: Optional[Callable] = None,
    key: str = "error_card"
) -> None:
    """
    Show styled error card with actions.
    
    Args:
        title: Error title
        message: Error message
        suggestions: List of suggestions
        show_retry: Whether to show retry button
        retry_callback: Function to call on retry
        key: Unique key
    """
    st.markdown("""
    <style>
        .error-card {
            background: #fff5f5;
            border: 1px solid #fc8181;
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        .error-card h4 {
            color: #c53030;
            margin-bottom: 0.5rem;
        }
        .error-card p {
            color: #742a2a;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="error-card">
        <h4>❌ {title}</h4>
        <p>{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if suggestions:
        st.markdown("**💡 What you can do:**")
        for suggestion in suggestions:
            st.markdown(f"- {suggestion}")
    
    if show_retry and retry_callback:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔄 Retry", key=f"retry_{key}"):
                retry_callback()


def handle_api_error(
    error: Exception,
    context: str = "API call",
    fallback_data: Optional[Any] = None,
    show_fallback_message: bool = True
) -> Any:
    """
    Handle API errors with fallback data option.
    
    Args:
        error: Exception that occurred
        context: Context of the API call
        fallback_data: Optional fallback data to use
        show_fallback_message: Whether to show fallback message
    
    Returns:
        Fallback data if provided, None otherwise
    """
    error_msg = error_handler.handle_error(error, context=context, show_ui=True)
    
    if fallback_data is not None:
        if show_fallback_message:
            st.info("ℹ️ Using sample data as fallback")
        return fallback_data
    
    return None


def show_validation_errors(
    errors: Dict[str, List[str]],
    title: str = "Validation Errors"
) -> None:
    """
    Show validation errors in a structured format.
    
    Args:
        errors: Dictionary mapping field names to error messages
        title: Title for the error display
    """
    st.error(f"❌ {title}")
    
    for field, field_errors in errors.items():
        with st.expander(f"**{field}**", expanded=True):
            for error in field_errors:
                st.markdown(f"- {error}")


def show_error_summary(
    errors: List[str],
    title: str = "Errors Summary",
    max_display: int = 5
) -> None:
    """
    Show summary of multiple errors.
    
    Args:
        errors: List of error messages
        title: Title for the summary
        max_display: Maximum errors to display
    """
    total_errors = len(errors)
    
    st.error(f"❌ {title} ({total_errors} error{'s' if total_errors != 1 else ''})")
    
    displayed_errors = errors[:max_display]
    for idx, error in enumerate(displayed_errors, 1):
        st.markdown(f"{idx}. {error}")
    
    if total_errors > max_display:
        with st.expander(f"Show {total_errors - max_display} more errors"):
            for idx, error in enumerate(errors[max_display:], max_display + 1):
                st.markdown(f"{idx}. {error}")


def safe_execute(
    func: Callable,
    *args,
    error_message: str = "Operation failed",
    default_return: Any = None,
    show_error: bool = True,
    **kwargs
) -> Any:
    """
    Safely execute a function with error handling.
    
    Args:
        func: Function to execute
        *args: Function arguments
        error_message: Error message to show
        default_return: Value to return on error
        show_error: Whether to show error in UI
        **kwargs: Function keyword arguments
    
    Returns:
        Function result or default_return on error
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if show_error:
            error_handler.handle_error(e, context=error_message, show_ui=True)
        return default_return


def create_error_boundary(key: str = "error_boundary"):
    """
    Create an error boundary context for catching errors in a section.
    
    Usage:
        with create_error_boundary():
            risky_operation()
    """
    class ErrorBoundary:
        def __enter__(self):
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is not None:
                error_handler.handle_error(
                    exc_val,
                    context=key,
                    show_ui=True
                )
                return True  # Suppress exception
            return False
    
    return ErrorBoundary()


# Convenience functions for common error scenarios

def show_network_error(retry_callback: Optional[Callable] = None):
    """Show network error with retry option"""
    show_error_card(
        title="Network Error",
        message="Unable to connect to the server. Please check your internet connection.",
        suggestions=[
            "Check your internet connection",
            "Verify the server is running",
            "Try again in a few moments"
        ],
        show_retry=retry_callback is not None,
        retry_callback=retry_callback,
        key="network_error"
    )


def show_data_error(details: str = ""):
    """Show data processing error"""
    st.error(f"❌ Data Processing Error")
    st.markdown(f"Unable to process the data. {details}")
    st.info("💡 Try refreshing the page or contact support if the issue persists.")


def show_permission_error():
    """Show permission denied error"""
    st.error("🚫 Permission Denied")
    st.markdown("You don't have permission to perform this action.")
    st.info("💡 Contact your administrator for access.")


def show_not_found_error(resource: str = "Resource"):
    """Show resource not found error"""
    st.warning(f"⚠️ {resource} Not Found")
    st.markdown(f"The requested {resource.lower()} could not be found.")
    st.info("💡 Check if the ID is correct or try searching again.")
