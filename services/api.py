"""
API Service Module for KPI Intelligence Frontend

Production-level service for connecting to backend API with:
- Connection pooling
- Error handling and retry logic
- Response caching
- Timeout management
- Graceful fallback to sample data
"""

import requests
from typing import Optional, Dict, List, Any, Union
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import time


class APIConfig:
    """Configuration for API connection"""
    BASE_URL = "http://localhost:8000"
    API_VERSION = "v1"
    TIMEOUT = 10  # seconds
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    CACHE_TTL = 300  # 5 minutes


class APIClient:
    """
    Production-level API client for backend communication.
    
    Features:
    - Automatic retry with exponential backoff
    - Response caching using Streamlit session state
    - Comprehensive error handling
    - Fallback to sample data on connection failure
    """
    
    def __init__(self, base_url: str = APIConfig.BASE_URL):
        """
        Initialize API client.
        
        Args:
            base_url: Backend API base URL
        """
        self.base_url = base_url
        self.api_url = f"{base_url}/api/{APIConfig.API_VERSION}"
        self.timeout = APIConfig.TIMEOUT
        self.max_retries = APIConfig.MAX_RETRIES
        self.retry_delay = APIConfig.RETRY_DELAY
        
        # Initialize cache in session state
        if 'api_cache' not in st.session_state:
            st.session_state.api_cache = {}
    
    def _get_cache_key(self, endpoint: str, params: Optional[Dict] = None) -> str:
        """Generate cache key from endpoint and parameters"""
        param_str = str(sorted(params.items())) if params else ""
        return f"{endpoint}:{param_str}"
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict]:
        """
        Get data from cache if not expired.
        
        Args:
            cache_key: Cache key
        
        Returns:
            Cached data or None if expired/not found
        """
        if cache_key in st.session_state.api_cache:
            cached_data, timestamp = st.session_state.api_cache[cache_key]
            if (datetime.now() - timestamp).seconds < APIConfig.CACHE_TTL:
                return cached_data
        return None
    
    def _save_to_cache(self, cache_key: str, data: Dict):
        """Save data to cache with timestamp"""
        st.session_state.api_cache[cache_key] = (data, datetime.now())
    
    def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Make HTTP request with retry logic.
        
        Args:
            endpoint: API endpoint (without base URL)
            method: HTTP method
            params: Query parameters
            data: Request body data
        
        Returns:
            Response JSON or None on failure
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(self.max_retries):
            try:
                if method == "GET":
                    response = requests.get(
                        url,
                        params=params,
                        timeout=self.timeout
                    )
                elif method == "POST":
                    response = requests.post(
                        url,
                        json=data,
                        params=params,
                        timeout=self.timeout
                    )
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                # Raise exception for bad status codes
                response.raise_for_status()
                
                return response.json()
            
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                print(f"Request timeout after {self.max_retries} attempts: {url}")
                return None
            
            except requests.exceptions.ConnectionError:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                print(f"Connection error after {self.max_retries} attempts: {url}")
                return None
            
            except requests.exceptions.RequestException as e:
                print(f"Request error: {str(e)}")
                return None
        
        return None
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        use_cache: bool = True
    ) -> Optional[Dict]:
        """
        Make GET request with caching support.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            use_cache: Whether to use cached response
        
        Returns:
            Response data or None
        """
        # Check cache first
        if use_cache:
            cache_key = self._get_cache_key(endpoint, params)
            cached_data = self._get_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        
        # Make request
        response = self._make_request(endpoint, method="GET", params=params)
        
        # Cache successful response
        if response and use_cache:
            cache_key = self._get_cache_key(endpoint, params)
            self._save_to_cache(cache_key, response)
        
        return response
    
    def check_health(self) -> bool:
        """
        Check if backend API is healthy.
        
        Returns:
            True if API is accessible, False otherwise
        """
        try:
            response = requests.get(
                f"{self.api_url}/health",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def clear_cache(self):
        """Clear all cached API responses"""
        st.session_state.api_cache = {}


# Global API client instance
api_client = APIClient()


# ==================== DATA FETCHING FUNCTIONS ====================

def fetch_product_performance(
    limit: Optional[int] = None,
    category: Optional[str] = None,
    use_cache: bool = True
) -> Optional[pd.DataFrame]:
    """
    Fetch product performance data from backend.
    
    Args:
        limit: Maximum number of products to return
        category: Filter by category
        use_cache: Use cached data if available
    
    Returns:
        DataFrame with product performance data or None
    """
    params = {}
    if limit:
        params['limit'] = limit
    if category:
        params['category'] = category
    
    response = api_client.get("products/performance", params=params, use_cache=use_cache)
    
    if response and response.get('status') == 'success':
        return pd.DataFrame(response['data'])
    
    return None


def fetch_product_kpi(use_cache: bool = True) -> Optional[Dict]:
    """
    Fetch aggregated product KPI metrics.
    
    Args:
        use_cache: Use cached data if available
    
    Returns:
        Dictionary with product KPIs or None
    """
    response = api_client.get("products/kpi", use_cache=use_cache)
    
    if response and response.get('status') == 'success':
        return response['data']
    
    return None


def fetch_sales_summary(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    use_cache: bool = True
) -> Optional[Dict]:
    """
    Fetch sales summary data.
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        use_cache: Use cached data if available
    
    Returns:
        Dictionary with sales summary or None
    """
    params = {}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    
    response = api_client.get("sales/summary", params=params, use_cache=use_cache)
    
    if response and response.get('status') == 'success':
        return response['data']
    
    return None


def fetch_dashboard_metrics(use_cache: bool = True) -> Optional[Dict]:
    """
    Fetch comprehensive dashboard metrics.
    
    Args:
        use_cache: Use cached data if available
    
    Returns:
        Dictionary with all dashboard metrics or None
    """
    response = api_client.get("dashboard/metrics", use_cache=use_cache)
    
    if response and response.get('status') == 'success':
        return response['data']
    
    return None


def fetch_revenue_data(
    period: str = "30d",
    use_cache: bool = True
) -> Optional[pd.DataFrame]:
    """
    Fetch revenue time-series data.
    
    Args:
        period: Time period (7d, 30d, 90d, 12m)
        use_cache: Use cached data if available
    
    Returns:
        DataFrame with revenue data or None
    """
    params = {'period': period}
    
    response = api_client.get("dashboard/revenue", params=params, use_cache=use_cache)
    
    if response and response.get('status') == 'success':
        return pd.DataFrame(response['data'])
    
    return None


def fetch_customer_data(use_cache: bool = True) -> Optional[pd.DataFrame]:
    """
    Fetch customer segmentation data.
    
    Args:
        use_cache: Use cached data if available
    
    Returns:
        DataFrame with customer segments or None
    """
    response = api_client.get("dashboard/customers", use_cache=use_cache)
    
    if response and response.get('status') == 'success':
        return pd.DataFrame(response['data'])
    
    return None


# ==================== UTILITY FUNCTIONS ====================

def is_backend_available() -> bool:
    """
    Check if backend API is available.
    
    Returns:
        True if backend is accessible
    """
    return api_client.check_health()


def get_connection_status() -> Dict[str, Any]:
    """
    Get detailed connection status.
    
    Returns:
        Dictionary with connection status information
    """
    is_available = api_client.check_health()
    
    return {
        "connected": is_available,
        "backend_url": api_client.base_url,
        "status": "Connected" if is_available else "Disconnected",
        "timestamp": datetime.now().isoformat()
    }


def clear_api_cache():
    """Clear all API response caches"""
    api_client.clear_cache()


def display_connection_status():
    """Display connection status banner in Streamlit UI"""
    status = get_connection_status()
    
    if status['connected']:
        st.success(f"🟢 Connected to backend API: {status['backend_url']}")
    else:
        st.warning(f"🟡 Backend API unavailable. Using sample data. ({status['backend_url']})")


# ==================== DATA LOADING WITH FALLBACK ====================

def load_data_with_fallback(
    fetch_function,
    fallback_function,
    data_name: str = "data",
    show_status: bool = True
) -> Any:
    """
    Load data from backend with automatic fallback to sample data.
    
    Args:
        fetch_function: Function to fetch data from backend
        fallback_function: Function to generate sample data
        data_name: Name of data for status messages
        show_status: Whether to show status messages
    
    Returns:
        Data from backend or fallback sample data
    """
    try:
        # Try fetching from backend
        data = fetch_function()
        
        if data is not None:
            if show_status:
                st.success(f"✅ Loaded {data_name} from backend")
            return data
        else:
            if show_status:
                st.info(f"ℹ️ Backend unavailable. Using sample {data_name}")
            return fallback_function()
    
    except Exception as e:
        if show_status:
            st.warning(f"⚠️ Error loading {data_name}: {str(e)}. Using sample data.")
        return fallback_function()
