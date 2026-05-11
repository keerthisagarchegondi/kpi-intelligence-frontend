"""
Loading States Component Module

Production-level loading indicators and progress displays:
- Spinners with custom messages
- Progress bars
- Skeleton loaders
- Loading overlays
- Multi-stage loading indicators
"""

import streamlit as st
import time
from typing import Optional, List, Callable, Any
from contextlib import contextmanager
from datetime import datetime
import threading


class LoadingState:
    """
    Global loading state manager using session state.
    """
    
    @staticmethod
    def is_loading(key: str = "global") -> bool:
        """Check if a loading operation is in progress"""
        return st.session_state.get(f"loading_{key}", False)
    
    @staticmethod
    def start_loading(key: str = "global", message: str = "Loading..."):
        """Start a loading operation"""
        st.session_state[f"loading_{key}"] = True
        st.session_state[f"loading_message_{key}"] = message
        st.session_state[f"loading_start_{key}"] = datetime.now()
    
    @staticmethod
    def stop_loading(key: str = "global"):
        """Stop a loading operation"""
        st.session_state[f"loading_{key}"] = False
        if f"loading_start_{key}" in st.session_state:
            duration = (datetime.now() - st.session_state[f"loading_start_{key}"]).total_seconds()
            st.session_state[f"loading_duration_{key}"] = duration
    
    @staticmethod
    def get_message(key: str = "global") -> str:
        """Get current loading message"""
        return st.session_state.get(f"loading_message_{key}", "Loading...")
    
    @staticmethod
    def get_duration(key: str = "global") -> Optional[float]:
        """Get duration of last loading operation"""
        return st.session_state.get(f"loading_duration_{key}")


@contextmanager
def loading_spinner(message: str = "Loading...", key: str = "operation"):
    """
    Context manager for showing loading spinner during operations.
    
    Usage:
        with loading_spinner("Fetching data..."):
            data = fetch_data()
    
    Args:
        message: Loading message to display
        key: Unique key for this loading operation
    """
    LoadingState.start_loading(key, message)
    with st.spinner(message):
        try:
            yield
        finally:
            LoadingState.stop_loading(key)


def show_loading_spinner(
    message: str = "Loading...",
    spinner_type: str = "default"
) -> None:
    """
    Show a loading spinner with custom message.
    
    Args:
        message: Message to display
        spinner_type: Type of spinner ('default', 'dots', 'circle')
    """
    st.spinner(message)


def show_progress_bar(
    progress: float,
    message: str = "Processing...",
    key: str = "progress"
) -> None:
    """
    Show a progress bar with message.
    
    Args:
        progress: Progress value (0.0 to 1.0)
        message: Message to display above progress bar
        key: Unique key for this progress bar
    """
    st.markdown(f"**{message}**")
    st.progress(progress, text=f"{int(progress * 100)}%")


def show_skeleton_loader(
    num_rows: int = 5,
    num_cols: int = 4,
    height: int = 30
) -> None:
    """
    Show skeleton loader for table data.
    
    Args:
        num_rows: Number of skeleton rows
        num_cols: Number of skeleton columns
        height: Height of each skeleton element
    """
    st.markdown("""
    <style>
        .skeleton {
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: loading 1.5s ease-in-out infinite;
            border-radius: 4px;
            margin: 8px 0;
        }
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
    </style>
    """, unsafe_allow_html=True)
    
    for _ in range(num_rows):
        cols = st.columns(num_cols)
        for col in cols:
            with col:
                st.markdown(f'<div class="skeleton" style="height: {height}px;"></div>', unsafe_allow_html=True)


def show_loading_overlay(
    message: str = "Loading...",
    show_spinner: bool = True
) -> None:
    """
    Show a full-screen loading overlay.
    
    Args:
        message: Message to display
        show_spinner: Whether to show spinner
    """
    st.markdown("""
    <style>
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.9);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            flex-direction: column;
        }
        .loading-message {
            font-size: 1.5rem;
            font-weight: 600;
            color: #333;
            margin-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        if show_spinner:
            st.spinner(message)
        st.markdown(f'<div class="loading-message">{message}</div>', unsafe_allow_html=True)


class MultiStageLoader:
    """
    Multi-stage loading indicator for complex operations.
    """
    
    def __init__(self, stages: List[str], key: str = "multistage"):
        """
        Initialize multi-stage loader.
        
        Args:
            stages: List of stage descriptions
            key: Unique key for this loader
        """
        self.stages = stages
        self.key = key
        self.current_stage = 0
        self.total_stages = len(stages)
        
        if f"{key}_container" not in st.session_state:
            st.session_state[f"{key}_container"] = st.empty()
    
    def update_stage(self, stage_index: int, message: Optional[str] = None):
        """
        Update to a specific stage.
        
        Args:
            stage_index: Index of the stage (0-based)
            message: Optional custom message for this stage
        """
        self.current_stage = stage_index
        progress = (stage_index + 1) / self.total_stages
        
        display_message = message or self.stages[stage_index]
        
        with st.session_state[f"{self.key}_container"].container():
            st.markdown(f"**Step {stage_index + 1} of {self.total_stages}**: {display_message}")
            st.progress(progress)
            
            # Show stage checklist
            st.markdown("---")
            for idx, stage in enumerate(self.stages):
                if idx < stage_index:
                    st.markdown(f"✅ {stage}")
                elif idx == stage_index:
                    st.markdown(f"⏳ {stage}")
                else:
                    st.markdown(f"⭕ {stage}")
    
    def complete(self, success_message: str = "All steps completed!"):
        """
        Mark all stages as complete.
        
        Args:
            success_message: Success message to display
        """
        with st.session_state[f"{self.key}_container"].container():
            st.success(success_message)
            for stage in self.stages:
                st.markdown(f"✅ {stage}")
    
    def clear(self):
        """Clear the loader display"""
        if f"{self.key}_container" in st.session_state:
            st.session_state[f"{self.key}_container"].empty()


def show_data_loading_placeholder(
    data_type: str = "table",
    message: str = "Loading data..."
) -> None:
    """
    Show appropriate loading placeholder for different data types.
    
    Args:
        data_type: Type of data being loaded ('table', 'chart', 'metric', 'text')
        message: Loading message
    """
    st.info(f"⏳ {message}")
    
    if data_type == "table":
        show_skeleton_loader(num_rows=5, num_cols=4)
    
    elif data_type == "chart":
        st.markdown("""
        <div style="width: 100%; height: 400px; background: #f5f5f5; 
                    border-radius: 8px; display: flex; justify-content: center; 
                    align-items: center; color: #999;">
            <div style="text-align: center;">
                <div style="font-size: 3rem;">📊</div>
                <div style="margin-top: 1rem;">Loading chart...</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif data_type == "metric":
        cols = st.columns(4)
        for col in cols:
            with col:
                st.markdown("""
                <div style="padding: 1rem; background: #f5f5f5; border-radius: 8px; height: 100px;">
                    <div class="skeleton" style="height: 20px; margin-bottom: 10px;"></div>
                    <div class="skeleton" style="height: 30px;"></div>
                </div>
                """, unsafe_allow_html=True)
    
    elif data_type == "text":
        st.markdown("""
        <div class="skeleton" style="height: 20px; margin: 10px 0;"></div>
        <div class="skeleton" style="height: 20px; margin: 10px 0; width: 80%;"></div>
        <div class="skeleton" style="height: 20px; margin: 10px 0; width: 90%;"></div>
        """, unsafe_allow_html=True)


def async_operation_wrapper(
    operation: Callable,
    loading_message: str = "Processing...",
    success_message: str = "Operation completed!",
    key: str = "async_op",
    show_duration: bool = True
) -> Any:
    """
    Wrapper for async operations with loading states.
    
    Args:
        operation: Function to execute
        loading_message: Message during operation
        success_message: Message on success
        key: Unique key for this operation
        show_duration: Whether to show operation duration
    
    Returns:
        Result of the operation
    """
    LoadingState.start_loading(key, loading_message)
    
    with st.spinner(loading_message):
        try:
            result = operation()
            LoadingState.stop_loading(key)
            
            duration = LoadingState.get_duration(key)
            if show_duration and duration:
                st.success(f"{success_message} (took {duration:.2f}s)")
            else:
                st.success(success_message)
            
            return result
        
        except Exception as e:
            LoadingState.stop_loading(key)
            st.error(f"Operation failed: {str(e)}")
            raise


class LoadingTimer:
    """
    Timer for tracking loading durations.
    """
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Start the timer"""
        self.start_time = datetime.now()
    
    def stop(self):
        """Stop the timer"""
        self.end_time = datetime.now()
    
    def duration(self) -> float:
        """Get duration in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    def format_duration(self) -> str:
        """Format duration as human-readable string"""
        duration = self.duration()
        if duration < 1:
            return f"{int(duration * 1000)}ms"
        elif duration < 60:
            return f"{duration:.2f}s"
        else:
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            return f"{minutes}m {seconds}s"


def show_loading_card(
    title: str = "Loading",
    message: str = "Please wait...",
    show_progress: bool = False,
    progress_value: float = 0.0
) -> None:
    """
    Show a styled loading card.
    
    Args:
        title: Card title
        message: Loading message
        show_progress: Whether to show progress bar
        progress_value: Progress value (0.0 to 1.0)
    """
    st.markdown("""
    <style>
        .loading-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 12px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
        }
        .loading-card h3 {
            color: white;
            margin-bottom: 1rem;
        }
        .loading-card p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="loading-card">
        <h3>⏳ {title}</h3>
        <p>{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if show_progress:
        st.progress(progress_value)


def show_batch_loading(
    items: List[str],
    current_index: int,
    item_name: str = "item"
) -> None:
    """
    Show loading state for batch processing.
    
    Args:
        items: List of items being processed
        current_index: Index of current item
        item_name: Name of item type (singular)
    """
    total = len(items)
    progress = current_index / total if total > 0 else 0
    
    st.markdown(f"**Processing {item_name} {current_index + 1} of {total}**")
    st.progress(progress, text=f"{int(progress * 100)}%")
    
    if current_index < len(items):
        st.info(f"Current: {items[current_index]}")


# Convenience functions for common use cases

def loading_data():
    """Show data loading indicator"""
    return loading_spinner("Loading data...", key="data_load")


def loading_report():
    """Show report loading indicator"""
    return loading_spinner("Generating report...", key="report_load")


def loading_export():
    """Show export loading indicator"""
    return loading_spinner("Exporting data...", key="export_load")


def loading_api_call():
    """Show API call loading indicator"""
    return loading_spinner("Fetching from API...", key="api_call")


def loading_processing():
    """Show data processing indicator"""
    return loading_spinner("Processing data...", key="data_process")
