"""
Performance Optimization Utilities

Production-level performance monitoring and optimization tools:
- Performance monitoring and metrics
- Caching strategies
- Lazy loading utilities
- Memoization decorators
- Data pagination optimization
- Component rendering optimization
"""

import streamlit as st
import time
import functools
from typing import Any, Callable, Optional, Dict, List, Tuple
from datetime import datetime, timedelta
import hashlib
import pickle
import pandas as pd


class PerformanceMonitor:
    """
    Monitor and track performance metrics for operations.
    """
    
    def __init__(self):
        if 'performance_metrics' not in st.session_state:
            st.session_state.performance_metrics = []
    
    @staticmethod
    def start_timer(operation_name: str) -> float:
        """Start timing an operation"""
        start_time = time.time()
        if 'timers' not in st.session_state:
            st.session_state.timers = {}
        st.session_state.timers[operation_name] = start_time
        return start_time
    
    @staticmethod
    def end_timer(operation_name: str) -> float:
        """End timing and return duration"""
        if 'timers' not in st.session_state or operation_name not in st.session_state.timers:
            return 0.0
        
        start_time = st.session_state.timers[operation_name]
        duration = time.time() - start_time
        
        # Store metric
        if 'performance_metrics' not in st.session_state:
            st.session_state.performance_metrics = []
        
        st.session_state.performance_metrics.append({
            'operation': operation_name,
            'duration': duration,
            'timestamp': datetime.now()
        })
        
        # Clean up
        del st.session_state.timers[operation_name]
        
        return duration
    
    @staticmethod
    def get_metrics(operation_name: Optional[str] = None) -> List[Dict]:
        """Get performance metrics"""
        if 'performance_metrics' not in st.session_state:
            return []
        
        metrics = st.session_state.performance_metrics
        
        if operation_name:
            return [m for m in metrics if m['operation'] == operation_name]
        
        return metrics
    
    @staticmethod
    def clear_metrics():
        """Clear all performance metrics"""
        st.session_state.performance_metrics = []
    
    @staticmethod
    def get_average_duration(operation_name: str) -> float:
        """Get average duration for an operation"""
        metrics = PerformanceMonitor.get_metrics(operation_name)
        if not metrics:
            return 0.0
        
        total = sum(m['duration'] for m in metrics)
        return total / len(metrics)


def performance_timer(operation_name: str):
    """
    Decorator to automatically time function execution.
    
    Usage:
        @performance_timer("data_loading")
        def load_data():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            PerformanceMonitor.start_timer(operation_name)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = PerformanceMonitor.end_timer(operation_name)
                if duration > 1.0:  # Log slow operations
                    print(f"⚠️ Slow operation '{operation_name}': {duration:.2f}s")
        return wrapper
    return decorator


class CacheManager:
    """
    Advanced caching manager with TTL and size limits.
    """
    
    def __init__(
        self,
        max_size: int = 100,
        default_ttl: int = 300  # 5 minutes
    ):
        self.max_size = max_size
        self.default_ttl = default_ttl
        
        if 'cache_store' not in st.session_state:
            st.session_state.cache_store = {}
        if 'cache_metadata' not in st.session_state:
            st.session_state.cache_metadata = {}
    
    def _generate_key(self, func_name: str, args: Tuple, kwargs: Dict) -> str:
        """Generate cache key from function and arguments"""
        key_data = f"{func_name}:{str(args)}:{str(sorted(kwargs.items()))}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key not in st.session_state.cache_store:
            return None
        
        metadata = st.session_state.cache_metadata.get(key, {})
        expires_at = metadata.get('expires_at')
        
        if expires_at and datetime.now() > expires_at:
            # Expired, remove from cache
            del st.session_state.cache_store[key]
            del st.session_state.cache_metadata[key]
            return None
        
        # Update access time
        metadata['last_accessed'] = datetime.now()
        metadata['access_count'] = metadata.get('access_count', 0) + 1
        
        return st.session_state.cache_store[key]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache with TTL"""
        # Enforce size limit
        if len(st.session_state.cache_store) >= self.max_size:
            self._evict_lru()
        
        st.session_state.cache_store[key] = value
        
        expires_at = None
        if ttl or self.default_ttl:
            expires_at = datetime.now() + timedelta(seconds=ttl or self.default_ttl)
        
        st.session_state.cache_metadata[key] = {
            'created_at': datetime.now(),
            'expires_at': expires_at,
            'last_accessed': datetime.now(),
            'access_count': 0
        }
    
    def _evict_lru(self):
        """Evict least recently used item"""
        if not st.session_state.cache_metadata:
            return
        
        # Find LRU item
        lru_key = min(
            st.session_state.cache_metadata.keys(),
            key=lambda k: st.session_state.cache_metadata[k]['last_accessed']
        )
        
        del st.session_state.cache_store[lru_key]
        del st.session_state.cache_metadata[lru_key]
    
    def clear(self):
        """Clear all cache"""
        st.session_state.cache_store = {}
        st.session_state.cache_metadata = {}
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        return {
            'size': len(st.session_state.cache_store),
            'max_size': self.max_size,
            'total_accesses': sum(
                m.get('access_count', 0)
                for m in st.session_state.cache_metadata.values()
            )
        }


# Global cache manager
cache_manager = CacheManager()


def memoize(ttl: int = 300):
    """
    Memoization decorator with TTL support.
    
    Usage:
        @memoize(ttl=600)
        def expensive_function(x, y):
            return x + y
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = cache_manager._generate_key(func.__name__, args, kwargs)
            
            # Try to get from cache
            cached_result = cache_manager.get(key)
            if cached_result is not None:
                return cached_result
            
            # Compute and cache
            result = func(*args, **kwargs)
            cache_manager.set(key, result, ttl=ttl)
            
            return result
        return wrapper
    return decorator


class LazyLoader:
    """
    Lazy loading utility for efficient data loading.
    """
    
    @staticmethod
    def load_in_chunks(
        data: pd.DataFrame,
        chunk_size: int = 1000
    ) -> List[pd.DataFrame]:
        """Split data into chunks for progressive loading"""
        chunks = []
        for i in range(0, len(data), chunk_size):
            chunks.append(data.iloc[i:i + chunk_size])
        return chunks
    
    @staticmethod
    def load_visible_rows(
        data: pd.DataFrame,
        page_number: int,
        rows_per_page: int = 25
    ) -> pd.DataFrame:
        """Load only visible rows for current page"""
        start_idx = page_number * rows_per_page
        end_idx = start_idx + rows_per_page
        return data.iloc[start_idx:end_idx]


class DataOptimizer:
    """
    Optimize data structures for better performance.
    """
    
    @staticmethod
    def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
        """Optimize DataFrame data types to reduce memory"""
        optimized = df.copy()
        
        for col in optimized.columns:
            col_type = optimized[col].dtype
            
            # Optimize integers
            if col_type in ['int64', 'int32']:
                col_min = optimized[col].min()
                col_max = optimized[col].max()
                
                if col_min >= 0:
                    if col_max < 255:
                        optimized[col] = optimized[col].astype('uint8')
                    elif col_max < 65535:
                        optimized[col] = optimized[col].astype('uint16')
                    elif col_max < 4294967295:
                        optimized[col] = optimized[col].astype('uint32')
                else:
                    if col_min > -128 and col_max < 127:
                        optimized[col] = optimized[col].astype('int8')
                    elif col_min > -32768 and col_max < 32767:
                        optimized[col] = optimized[col].astype('int16')
                    elif col_min > -2147483648 and col_max < 2147483647:
                        optimized[col] = optimized[col].astype('int32')
            
            # Optimize floats
            elif col_type == 'float64':
                optimized[col] = optimized[col].astype('float32')
            
            # Optimize objects to categories if beneficial
            elif col_type == 'object':
                num_unique = optimized[col].nunique()
                num_total = len(optimized[col])
                if num_unique / num_total < 0.5:  # Less than 50% unique
                    optimized[col] = optimized[col].astype('category')
        
        return optimized
    
    @staticmethod
    def reduce_memory_usage(df: pd.DataFrame) -> pd.DataFrame:
        """Reduce DataFrame memory usage"""
        start_mem = df.memory_usage(deep=True).sum() / 1024**2
        
        optimized = DataOptimizer.optimize_dtypes(df)
        
        end_mem = optimized.memory_usage(deep=True).sum() / 1024**2
        reduction = ((start_mem - end_mem) / start_mem) * 100
        
        print(f"Memory reduced by {reduction:.1f}% ({start_mem:.2f}MB -> {end_mem:.2f}MB)")
        
        return optimized


class RenderOptimizer:
    """
    Optimize component rendering performance.
    """
    
    @staticmethod
    def should_rerender(key: str, new_value: Any) -> bool:
        """Check if component should rerender based on value change"""
        cache_key = f"render_cache_{key}"
        
        if cache_key not in st.session_state:
            st.session_state[cache_key] = new_value
            return True
        
        old_value = st.session_state[cache_key]
        
        # Compare values
        if old_value != new_value:
            st.session_state[cache_key] = new_value
            return True
        
        return False
    
    @staticmethod
    def batch_updates(updates: List[Callable]):
        """Batch multiple UI updates together"""
        for update_func in updates:
            update_func()


class QueryOptimizer:
    """
    Optimize data queries and filters.
    """
    
    @staticmethod
    def optimize_filter(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply filters efficiently"""
        result = df
        
        for column, value in filters.items():
            if column not in df.columns:
                continue
            
            if isinstance(value, (list, tuple)):
                # Use isin for list filters (faster than OR conditions)
                result = result[result[column].isin(value)]
            elif isinstance(value, dict):
                # Range filter
                if 'min' in value:
                    result = result[result[column] >= value['min']]
                if 'max' in value:
                    result = result[result[column] <= value['max']]
            else:
                result = result[result[column] == value]
        
        return result
    
    @staticmethod
    def optimize_search(df: pd.DataFrame, search_term: str, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """Optimize text search across columns"""
        if not search_term:
            return df
        
        search_columns = columns or df.columns
        
        # Use vectorized operations
        mask = pd.Series([False] * len(df))
        
        for col in search_columns:
            if col in df.columns:
                mask |= df[col].astype(str).str.contains(search_term, case=False, na=False)
        
        return df[mask]


def debounce(wait_time: float = 0.5):
    """
    Debounce decorator to prevent excessive function calls.
    
    Usage:
        @debounce(wait_time=1.0)
        def expensive_search(query):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"debounce_{func.__name__}"
            
            if key not in st.session_state:
                st.session_state[key] = {'last_call': 0, 'timer': None}
            
            current_time = time.time()
            last_call = st.session_state[key]['last_call']
            
            if current_time - last_call >= wait_time:
                st.session_state[key]['last_call'] = current_time
                return func(*args, **kwargs)
            
            return None
        return wrapper
    return decorator


# Performance monitoring context manager
class performance_context:
    """
    Context manager for performance monitoring.
    
    Usage:
        with performance_context("data_loading"):
            data = load_data()
    """
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
    
    def __enter__(self):
        PerformanceMonitor.start_timer(self.operation_name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = PerformanceMonitor.end_timer(self.operation_name)
        return False


# Utility functions
def get_performance_report() -> Dict[str, Any]:
    """Get comprehensive performance report"""
    metrics = PerformanceMonitor.get_metrics()
    cache_stats = cache_manager.get_stats()
    
    operation_stats = {}
    for metric in metrics:
        op = metric['operation']
        if op not in operation_stats:
            operation_stats[op] = {
                'count': 0,
                'total_time': 0,
                'avg_time': 0,
                'max_time': 0,
                'min_time': float('inf')
            }
        
        stats = operation_stats[op]
        stats['count'] += 1
        stats['total_time'] += metric['duration']
        stats['max_time'] = max(stats['max_time'], metric['duration'])
        stats['min_time'] = min(stats['min_time'], metric['duration'])
    
    # Calculate averages
    for op, stats in operation_stats.items():
        stats['avg_time'] = stats['total_time'] / stats['count']
    
    return {
        'operations': operation_stats,
        'cache': cache_stats,
        'total_operations': len(metrics)
    }


def display_performance_metrics():
    """Display performance metrics in Streamlit UI"""
    report = get_performance_report()
    
    st.subheader("⚡ Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Operations", report['total_operations'])
    
    with col2:
        st.metric("Cache Size", f"{report['cache']['size']}/{report['cache']['max_size']}")
    
    with col3:
        st.metric("Cache Accesses", report['cache']['total_accesses'])
    
    if report['operations']:
        st.markdown("**Operation Timings:**")
        
        for op, stats in report['operations'].items():
            with st.expander(f"🔧 {op}"):
                st.write(f"**Count:** {stats['count']}")
                st.write(f"**Average:** {stats['avg_time']:.3f}s")
                st.write(f"**Min:** {stats['min_time']:.3f}s")
                st.write(f"**Max:** {stats['max_time']:.3f}s")
                st.write(f"**Total:** {stats['total_time']:.3f}s")
