"""
API Service Module for KPI Intelligence Frontend

Production-level service for connecting to backend API with:
- Connection pooling
- Error handling and retry logic
- Response caching
- Timeout management
- Graceful fallback to sample data
- Loading states and error messages
- Performance monitoring and optimization
- Environment-based configuration
"""

import requests
from typing import Optional, Dict, List, Any, Union, Tuple
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import time
from utils.performance import performance_timer, DataOptimizer
from services.config import ConfigManager


class APIStatus:
    """Track API request status"""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    NETWORK_ERROR = "network_error"
    NOT_FOUND = "not_found"
    SERVER_ERROR = "server_error"


class APIConfig:
    """Configuration for API connection - loaded from environment"""
    
    @staticmethod
    def get_base_url() -> str:
        """Get base URL from configuration"""
        return ConfigManager.get_backend_url()
    
    @staticmethod
    def get_config():
        """Get full configuration"""
        return ConfigManager.load_config()
    
    # Legacy support - dynamically loaded
    @property
    def BASE_URL(self) -> str:
        return self.get_base_url()
    
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
    - Environment-based configuration
    """
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize API client.
        
        Args:
            base_url: Backend API base URL (default: from environment config)
        """
        config = ConfigManager.load_config()
        self.base_url = base_url or config.backend_url
        self.api_url = f"{self.base_url}/api/{config.api_version}"
        self.timeout = config.timeout
        self.max_retries = config.max_retries
        self.retry_delay = config.retry_delay
        
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
        if 'api_cache' not in st.session_state:
            st.session_state.api_cache = {}
        
        if cache_key in st.session_state.api_cache:
            cached_data, timestamp = st.session_state.api_cache[cache_key]
            if (datetime.now() - timestamp).seconds < APIConfig.CACHE_TTL:
                return cached_data
        return None
    
    def _save_to_cache(self, cache_key: str, data: Dict):
        """Save data to cache with timestamp"""
        if 'api_cache' not in st.session_state:
            st.session_state.api_cache = {}
        st.session_state.api_cache[cache_key] = (data, datetime.now())
    
    def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Tuple[Optional[Dict], str, Optional[str]]:
        """
        Make HTTP request with retry logic and detailed error information.
        
        Args:
            endpoint: API endpoint (without base URL)
            method: HTTP method
            params: Query parameters
            data: Request body data
        
        Returns:
            Tuple of (Response JSON or None, status, error_message)
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        last_error = None
        
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
                    return None, APIStatus.ERROR, f"Unsupported HTTP method: {method}"
                
                # Check status code
                if response.status_code == 404:
                    return None, APIStatus.NOT_FOUND, f"Endpoint not found: {endpoint}"
                elif response.status_code >= 500:
                    return None, APIStatus.SERVER_ERROR, f"Server error (status {response.status_code})"
                
                # Raise exception for other bad status codes
                response.raise_for_status()
                
                return response.json(), APIStatus.SUCCESS, None
            
            except requests.exceptions.Timeout as e:
                last_error = f"Request timeout: {str(e)}"
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                return None, APIStatus.TIMEOUT, last_error
            
            except requests.exceptions.ConnectionError as e:
                last_error = f"Connection error: {str(e)}"
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                return None, APIStatus.NETWORK_ERROR, last_error
            
            except requests.exceptions.RequestException as e:
                last_error = f"Request error: {str(e)}"
                return None, APIStatus.ERROR, last_error
            
            except Exception as e:
                last_error = f"Unexpected error: {str(e)}"
                return None, APIStatus.ERROR, last_error
        
        return None, APIStatus.ERROR, last_error
    
    @performance_timer("api_get_request")
    def get(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        use_cache: bool = True,
        show_error: bool = False
    ) -> Tuple[Optional[Dict], str, Optional[str]]:
        """
        Make GET request with caching support and error handling.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            use_cache: Whether to use cached response
            show_error: Whether to display error in UI
        
        Returns:
            Tuple of (Response data or None, status, error_message)
        """
        # Check cache first
        if use_cache:
            cache_key = self._get_cache_key(endpoint, params)
            cached_data = self._get_from_cache(cache_key)
            if cached_data is not None:
                return cached_data, APIStatus.SUCCESS, None
        
        # Make request
        response, status, error_msg = self._make_request(endpoint, method="GET", params=params)
        
        # Show error in UI if requested
        if show_error and status != APIStatus.SUCCESS:
            self._display_error(status, error_msg, endpoint)
        
        # Cache successful response
        if response and use_cache and status == APIStatus.SUCCESS:
            cache_key = self._get_cache_key(endpoint, params)
            self._save_to_cache(cache_key, response)
        
        return response, status, error_msg
    
    def _display_error(self, status: str, error_msg: Optional[str], endpoint: str):
        """Display error message in Streamlit UI"""
        if status == APIStatus.TIMEOUT:
            st.warning(f"⏱️ Request timeout for {endpoint}. The server might be busy. Using fallback data.")
        elif status == APIStatus.NETWORK_ERROR:
            st.warning(f"🌐 Network error connecting to {endpoint}. Check your connection. Using fallback data.")
        elif status == APIStatus.NOT_FOUND:
            st.error(f"❌ Endpoint not found: {endpoint}")
        elif status == APIStatus.SERVER_ERROR:
            st.error(f"🚨 Server error for {endpoint}. The backend encountered an issue. Using fallback data.")
        elif error_msg:
            st.error(f"❌ Error: {error_msg}")
    
    def check_health(self) -> Tuple[bool, Optional[str]]:
        """
        Check if backend API is healthy.
        
        Returns:
            Tuple of (is_healthy, error_message)
        """
        try:
            response = requests.get(
                f"{self.api_url}/health",
                timeout=5
            )
            if response.status_code == 200:
                return True, None
            return False, f"Server returned status {response.status_code}"
        except requests.exceptions.Timeout:
            return False, "Connection timeout"
        except requests.exceptions.ConnectionError:
            return False, "Cannot connect to server"
        except Exception as e:
            return False, str(e)
    
    def clear_cache(self):
        """Clear all cached API responses"""
        if 'api_cache' not in st.session_state:
            st.session_state.api_cache = {}
        else:
            st.session_state.api_cache = {}


# Global API client instance
api_client = APIClient()


# ==================== UTILITY FUNCTIONS ====================

def is_backend_available() -> Tuple[bool, Optional[str]]:
    """
    Check if backend API is available.
    
    Returns:
        Tuple of (is_available, error_message)
    """
    return api_client.check_health()


def display_connection_status(show_success: bool = False):
    """
    Display connection status banner in Streamlit UI.
    
    Args:
        show_success: Whether to show success message when connected
    """
    is_available, error_msg = api_client.check_health()
    
    if is_available:
        if show_success:
            st.success(f"🟢 Connected to backend API: {api_client.base_url}")
    else:
        if error_msg:
            st.warning(f"🟡 Backend API unavailable ({error_msg}). Using sample data for demonstration.")
        else:
            st.warning(f"🟡 Backend API unavailable. Using sample data for demonstration.")


# ==================== DATA FETCHING FUNCTIONS ====================

@st.cache_data(ttl=300, show_spinner="Loading product performance...")
@performance_timer("fetch_product_performance")
def fetch_product_performance(
    limit: Optional[int] = None,
    category: Optional[str] = None,
    use_cache: bool = True,
    show_errors: bool = False
) -> Tuple[Optional[pd.DataFrame], str]:
    """
    Fetch product performance data from backend with error handling.
    
    Args:
        limit: Maximum number of products to return
        category: Filter by category
        use_cache: Use cached data if available
        show_errors: Whether to display errors in UI
    
    Returns:
        Tuple of (DataFrame or None, status_code)
    """
    params = {}
    if limit:
        params['limit'] = limit
    if category:
        params['category'] = category
    
    response, status, error_msg = api_client.get(
        "products/performance",
        params=params,
        use_cache=use_cache,
        show_error=show_errors
    )
    
    if response and response.get('status') == 'success':
        return pd.DataFrame(response['data']), status
    
    return None, status


def fetch_product_kpi(
    use_cache: bool = True,
    show_errors: bool = False
) -> Tuple[Optional[Dict], str]:
    """
    Fetch aggregated product KPI metrics.
    
    Args:
        use_cache: Use cached data if available
        show_errors: Whether to display errors in UI
    
    Returns:
        Tuple of (Dictionary with product KPIs or None, status)
    """
    response, status, error_msg = api_client.get(
        "products/kpi",
        use_cache=use_cache,
        show_error=show_errors
    )
    
    if response and response.get('status') == 'success':
        return response['data'], status
    
    return None, status


def fetch_sales_summary(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    use_cache: bool = True,
    show_errors: bool = False
) -> Tuple[Optional[Dict], str, Optional[str]]:
    """
    Fetch sales summary data.
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        use_cache: Use cached data if available
        show_errors: Whether to display errors in UI
    
    Returns:
        Tuple of (Dictionary with sales summary or None, status, error_message)
    """
    params = {}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    
    response, status, error_msg = api_client.get(
        "sales/summary",
        params=params,
        use_cache=use_cache,
        show_error=show_errors
    )
    
    if response and response.get('status') == 'success':
        return response['data'], status, None
    
    return None, status, error_msg


def fetch_dashboard_metrics(
    use_cache: bool = True,
    show_errors: bool = False
) -> Tuple[Optional[Dict], str]:
    """
    Fetch comprehensive dashboard metrics.
    
    Args:
        use_cache: Use cached data if available
        show_errors: Whether to display errors in UI
    
    Returns:
        Tuple of (Dictionary with all dashboard metrics or None, status)
    """
    response, status, error_msg = api_client.get(
        "dashboard/metrics",
        use_cache=use_cache,
        show_error=show_errors
    )
    
    if response and response.get('status') == 'success':
        return response['data'], status
    
    return None, status


def fetch_revenue_data(
    period: str = "30d",
    use_cache: bool = True,
    show_errors: bool = False
) -> Tuple[Optional[pd.DataFrame], str]:
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


# ==================== ANOMALY DETECTION ====================

def fetch_anomalies(
    metric: str = "revenue",
    method: str = "zscore",
    threshold: float = 3.0,
    period: str = "30d",
    limit: int = 10,
    use_cache: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Fetch detected anomalies from backend.
    
    Args:
        metric: Metric to analyze (revenue, profit, transactions)
        method: Detection method (zscore, iqr, mad, moving_avg)
        threshold: Anomaly detection threshold
        period: Time period (7d, 30d, 90d)
        limit: Maximum anomalies to return
        use_cache: Whether to use cached results
    
    Returns:
        Dictionary with anomalies, summary, and alerts or None on error
    """
    params = {
        "metric": metric,
        "method": method,
        "threshold": threshold,
        "period": period,
        "limit": limit
    }
    
    response, status, error_msg = api_client.get("/anomalies/detect", params=params, use_cache=use_cache)
    
    if response and status == APIStatus.SUCCESS:
        return response
    
    return None


# ==================== FILE UPLOAD ====================

def upload_file(
    file_content: bytes,
    filename: str,
    process_data: bool = True,
    save_to_raw: bool = True,
    save_to_processed: bool = True,
    validate_schema: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Upload data file to backend for processing.
    
    Args:
        file_content: File content as bytes
        filename: Original filename
        process_data: Whether to process and clean data
        save_to_raw: Save original file to raw directory
        save_to_processed: Save processed file to processed directory
        validate_schema: Perform schema validation
    
    Returns:
        Upload response with file info, validation results, and saved paths
    """
    try:
        url = f"{api_client.api_url}/upload"
        
        files = {
            'file': (filename, file_content)
        }
        
        data = {
            'process_data': str(process_data).lower(),
            'save_to_raw': str(save_to_raw).lower(),
            'save_to_processed': str(save_to_processed).lower(),
            'validate_schema': str(validate_schema).lower()
        }
        
        response = requests.post(
            url,
            files=files,
            data=data,
            timeout=api_client.timeout * 3  # Longer timeout for upload
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            error = response.json().get('detail', 'Upload validation failed')
            st.error(f"Upload Error: {error}")
            return None
        elif response.status_code == 413:
            st.error("File too large. Maximum size: 50 MB")
            return None
        else:
            st.error(f"Upload failed: {response.status_code}")
            return None
    
    except requests.exceptions.Timeout:
        st.error("Upload timeout. Please try a smaller file.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Please ensure server is running.")
        return None
    except Exception as e:
        st.error(f"Upload failed: {str(e)}")
        return None


# ==================== COMPREHENSIVE KPI DATA FETCHING ====================

@st.cache_data(ttl=300, show_spinner="Loading KPI overview...")
@performance_timer("fetch_kpi_overview")
def fetch_kpi_overview(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    use_cache: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Fetch comprehensive KPI overview with all metrics.
    
    Args:
        start_date: Start date (YYYY-MM-DD format)
        end_date: End date (YYYY-MM-DD format)
        use_cache: Use cached data if available
    
    Returns:
        Dictionary with comprehensive KPI metrics including:
        - Revenue metrics (total, average, growth)
        - Customer metrics (total, active, retention)
        - Product metrics (top products, categories)
        - Sales metrics (conversion rate, AOV)
        - Period comparison data
    """
    params = {}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    
    response = api_client.get("kpi/overview", params=params, use_cache=use_cache)
    
    if response and response.get('status') == 'success':
        return response['data']
    
    return None


def fetch_kpi_by_category(
    category: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    use_cache: bool = True
) -> Tuple[Optional[Dict[str, Any]], str, Optional[str]]:
    """
    Fetch KPIs filtered by specific category.
    
    Args:
        category: Category name (e.g., 'revenue', 'sales', 'customer', 'product')
        start_date: Start date (YYYY-MM-DD format)
        end_date: End date (YYYY-MM-DD format)
        use_cache: Use cached data if available
    
    Returns:
        Tuple of (category-specific KPI metrics or None, status, error_message)
    """
    params = {'category': category}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    
    response, status, error_msg = api_client.get(
        f"kpi/category/{category}",
        params=params,
        use_cache=use_cache
    )
    
    if response and response.get('status') == 'success':
        return response['data'], status, None
    
    return None, status, error_msg


def fetch_kpi_time_series(
    metrics: List[str],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    granularity: str = "daily",
    use_cache: bool = True
) -> Optional[pd.DataFrame]:
    """
    Fetch KPI time series data for trend analysis.
    
    Args:
        metrics: List of metric names to fetch (e.g., ['revenue', 'orders', 'customers'])
        start_date: Start date (YYYY-MM-DD format)
        end_date: End date (YYYY-MM-DD format)
        granularity: Time granularity ('daily', 'weekly', 'monthly')
        use_cache: Use cached data if available
    
    Returns:
        DataFrame with time series data for requested metrics
    """
    params = {
        'metrics': ','.join(metrics),
        'granularity': granularity
    }
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    
    response = api_client.get("kpi/timeseries", params=params, use_cache=use_cache)
    
    if response and response.get('status') == 'success':
        return pd.DataFrame(response['data'])
    
    return None


def fetch_all_reports(use_cache: bool = True) -> Optional[List[Dict[str, Any]]]:
    """
    Fetch list of all available reports with metadata.
    
    Args:
        use_cache: Use cached data if available
    
    Returns:
        List of report metadata including:
        - Report ID and name
        - Description
        - Available columns
        - Last updated timestamp
        - Row count estimate
    """
    response = api_client.get("reports/list", use_cache=use_cache)
    
    if response and response.get('status') == 'success':
        return response['data']
    
    return None


def fetch_report_data(
    report_id: str,
    filters: Optional[Dict[str, Any]] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
    page: int = 1,
    page_size: int = 100,
    use_cache: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Fetch report data with advanced filtering, sorting, and pagination.
    
    Args:
        report_id: Unique report identifier
        filters: Dictionary of filter conditions (e.g., {'status': 'active', 'category': 'electronics'})
        sort_by: Column name to sort by
        sort_order: Sort order ('asc' or 'desc')
        page: Page number for pagination (1-indexed)
        page_size: Number of records per page
        use_cache: Use cached data if available
    
    Returns:
        Dictionary with:
        - data: DataFrame with report data
        - total_records: Total number of records
        - page_info: Pagination information
        - applied_filters: Active filters
        - columns: Column definitions
    """
    params = {
        'page': page,
        'page_size': page_size,
        'sort_order': sort_order
    }
    
    if sort_by:
        params['sort_by'] = sort_by
    
    if filters:
        # Encode filters as JSON string
        import json
        params['filters'] = json.dumps(filters)
    
    response = api_client.get(f"reports/{report_id}", params=params, use_cache=use_cache)
    
    if response and response.get('status') == 'success':
        # Convert data array to DataFrame
        data = response['data']
        if 'records' in data:
            data['data'] = pd.DataFrame(data['records'])
        return data
    
    return None


def fetch_kpi_comparison(
    metrics: List[str],
    period1_start: str,
    period1_end: str,
    period2_start: str,
    period2_end: str,
    use_cache: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Compare KPI metrics between two time periods.
    
    Args:
        metrics: List of metric names to compare
        period1_start: Start date of first period (YYYY-MM-DD)
        period1_end: End date of first period (YYYY-MM-DD)
        period2_start: Start date of second period (YYYY-MM-DD)
        period2_end: End date of second period (YYYY-MM-DD)
        use_cache: Use cached data if available
    
    Returns:
        Dictionary with comparison metrics including:
        - period1_values: Metrics for first period
        - period2_values: Metrics for second period
        - changes: Absolute and percentage changes
        - trend: Trend direction (up/down/flat)
    """
    params = {
        'metrics': ','.join(metrics),
        'period1_start': period1_start,
        'period1_end': period1_end,
        'period2_start': period2_start,
        'period2_end': period2_end
    }
    
    response = api_client.get("kpi/compare", params=params, use_cache=use_cache)
    
    if response and response.get('status') == 'success':
        return response['data']
    
    return None


def fetch_top_performers(
    metric: str = "revenue",
    dimension: str = "product",
    limit: int = 10,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    use_cache: bool = True
) -> Optional[pd.DataFrame]:
    """
    Fetch top performers by specific metric and dimension.
    
    Args:
        metric: Metric to rank by (revenue, profit, quantity, growth)
        dimension: Dimension to analyze (product, customer, region, category)
        limit: Number of top performers to return
        start_date: Start date (YYYY-MM-DD format)
        end_date: End date (YYYY-MM-DD format)
        use_cache: Use cached data if available
    
    Returns:
        DataFrame with top performers and their metrics
    """
    params = {
        'metric': metric,
        'dimension': dimension,
        'limit': limit
    }
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    
    response = api_client.get("kpi/top-performers", params=params, use_cache=use_cache)
    
    if response and response.get('status') == 'success':
        return pd.DataFrame(response['data'])
    
    return None


# ==================== SAMPLE DATA GENERATORS FOR FALLBACK ====================

def generate_sample_kpi_overview() -> Dict[str, Any]:
    """Generate realistic sample KPI overview data for demo/fallback"""
    from datetime import datetime, timedelta
    import random
    
    today = datetime.now()
    
    return {
        'period': {
            'start_date': (today - timedelta(days=30)).strftime('%Y-%m-%d'),
            'end_date': today.strftime('%Y-%m-%d')
        },
        'revenue': {
            'total': 1245680.50,
            'average_daily': 41522.68,
            'growth_rate': 12.5,
            'trend': 'up'
        },
        'customers': {
            'total': 15420,
            'active': 12850,
            'new': 2340,
            'retention_rate': 85.2,
            'churn_rate': 14.8
        },
        'sales': {
            'total_orders': 8920,
            'average_order_value': 139.65,
            'conversion_rate': 3.45,
            'items_per_order': 2.8
        },
        'products': {
            'total_products': 450,
            'active_products': 398,
            'top_category': 'Electronics',
            'low_stock_items': 23
        }
    }


def generate_sample_report_list() -> List[Dict[str, Any]]:
    """Generate sample list of available reports"""
    return [
        {
            'report_id': 'sales_overview',
            'name': 'Sales Overview Report',
            'description': 'Comprehensive sales data with product details and customer information',
            'row_count': 8920,
            'columns': ['order_id', 'date', 'customer', 'product', 'quantity', 'revenue', 'profit'],
            'last_updated': datetime.now().isoformat()
        },
        {
            'report_id': 'product_performance',
            'name': 'Product Performance Report',
            'description': 'Detailed product analytics including revenue, units sold, and margins',
            'row_count': 450,
            'columns': ['product_id', 'product_name', 'category', 'revenue', 'units_sold', 'profit_margin'],
            'last_updated': datetime.now().isoformat()
        },
        {
            'report_id': 'customer_analytics',
            'name': 'Customer Analytics Report',
            'description': 'Customer behavior, lifetime value, and segmentation data',
            'row_count': 15420,
            'columns': ['customer_id', 'name', 'segment', 'lifetime_value', 'orders_count', 'last_purchase'],
            'last_updated': datetime.now().isoformat()
        },
        {
            'report_id': 'revenue_breakdown',
            'name': 'Revenue Breakdown Report',
            'description': 'Revenue analysis by product, region, and time period',
            'row_count': 2840,
            'columns': ['date', 'region', 'category', 'revenue', 'cost', 'profit', 'margin'],
            'last_updated': datetime.now().isoformat()
        }
    ]


def generate_sample_report_data(report_id: str, page_size: int = 100) -> Dict[str, Any]:
    """Generate realistic sample report data for demo/fallback"""
    import random
    from datetime import datetime, timedelta
    
    # Generate sample records based on report type
    if report_id == 'sales_overview':
        records = []
        products = ['Laptop Pro', 'Wireless Mouse', 'USB-C Cable', 'Monitor 27"', 'Keyboard RGB']
        customers = [f'Customer-{i:04d}' for i in range(1, 101)]
        
        for i in range(page_size):
            date = datetime.now() - timedelta(days=random.randint(0, 30))
            records.append({
                'order_id': f'ORD-{10000 + i}',
                'date': date.strftime('%Y-%m-%d'),
                'customer': random.choice(customers),
                'product': random.choice(products),
                'quantity': random.randint(1, 5),
                'revenue': round(random.uniform(50, 500), 2),
                'profit': round(random.uniform(10, 150), 2),
                'status': random.choice(['Completed', 'Pending', 'Shipped'])
            })
    
    elif report_id == 'product_performance':
        categories = ['Electronics', 'Accessories', 'Components', 'Peripherals']
        records = []
        
        for i in range(page_size):
            revenue = random.uniform(5000, 50000)
            units = random.randint(100, 1000)
            records.append({
                'product_id': f'PROD-{1000 + i}',
                'product_name': f'Product {i+1}',
                'category': random.choice(categories),
                'revenue': round(revenue, 2),
                'units_sold': units,
                'profit_margin': round(random.uniform(15, 45), 2),
                'stock_level': random.randint(0, 500)
            })
    
    elif report_id == 'customer_analytics':
        segments = ['VIP', 'Regular', 'New', 'Inactive']
        records = []
        
        for i in range(page_size):
            records.append({
                'customer_id': f'CUST-{5000 + i}',
                'name': f'Customer {i+1}',
                'segment': random.choice(segments),
                'lifetime_value': round(random.uniform(500, 10000), 2),
                'orders_count': random.randint(1, 50),
                'last_purchase': (datetime.now() - timedelta(days=random.randint(0, 180))).strftime('%Y-%m-%d'),
                'email': f'customer{i+1}@example.com'
            })
    
    else:  # revenue_breakdown
        regions = ['North', 'South', 'East', 'West']
        categories = ['Electronics', 'Accessories', 'Components']
        records = []
        
        for i in range(page_size):
            revenue = random.uniform(1000, 20000)
            cost = revenue * random.uniform(0.4, 0.7)
            records.append({
                'date': (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d'),
                'region': random.choice(regions),
                'category': random.choice(categories),
                'revenue': round(revenue, 2),
                'cost': round(cost, 2),
                'profit': round(revenue - cost, 2),
                'margin': round((revenue - cost) / revenue * 100, 2)
            })
    
    return {
        'records': records,
        'total_records': page_size * 10,  # Simulate more data exists
        'page_info': {
            'current_page': 1,
            'page_size': page_size,
            'total_pages': 10
        },
        'applied_filters': {},
        'columns': list(records[0].keys()) if records else []
    }
