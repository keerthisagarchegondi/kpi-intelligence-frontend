"""
API Integration Verification and Testing

Production-level utilities for verifying API integration:
- Endpoint availability testing
- Response validation
- Performance benchmarking
- Integration health monitoring
"""

import requests
import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import time
from services.config import ConfigManager


class EndpointTest:
    """Represents a single endpoint test"""
    
    def __init__(
        self,
        name: str,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        expected_status: int = 200,
        timeout: int = 10
    ):
        self.name = name
        self.endpoint = endpoint
        self.method = method
        self.params = params or {}
        self.expected_status = expected_status
        self.timeout = timeout
        self.result = None
    
    def run(self, base_url: str) -> Dict[str, Any]:
        """
        Run the endpoint test.
        
        Args:
            base_url: Base URL of the API
        
        Returns:
            Test result dictionary
        """
        url = f"{base_url}{self.endpoint}"
        start_time = time.time()
        
        result = {
            'name': self.name,
            'endpoint': self.endpoint,
            'url': url,
            'method': self.method,
            'passed': False,
            'status_code': None,
            'response_time': None,
            'error': None,
            'response_data': None,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            if self.method == "GET":
                response = requests.get(url, params=self.params, timeout=self.timeout)
            elif self.method == "POST":
                response = requests.post(url, json=self.params, timeout=self.timeout)
            else:
                result['error'] = f"Unsupported method: {self.method}"
                return result
            
            result['status_code'] = response.status_code
            result['response_time'] = time.time() - start_time
            
            # Check if status matches expected
            if response.status_code == self.expected_status:
                result['passed'] = True
                try:
                    result['response_data'] = response.json()
                except:
                    result['response_data'] = response.text[:200]
            else:
                result['error'] = f"Expected status {self.expected_status}, got {response.status_code}"
        
        except requests.exceptions.Timeout:
            result['error'] = f"Request timeout after {self.timeout}s"
            result['response_time'] = time.time() - start_time
        
        except requests.exceptions.ConnectionError:
            result['error'] = "Connection error - service may be down"
            result['response_time'] = time.time() - start_time
        
        except Exception as e:
            result['error'] = str(e)
            result['response_time'] = time.time() - start_time
        
        self.result = result
        return result


class APIIntegrationVerifier:
    """
    Verify API integration with comprehensive endpoint testing.
    """
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize verifier.
        
        Args:
            base_url: Base URL of the API (default: from config)
        """
        self.base_url = base_url or ConfigManager.get_backend_url()
        self.api_url = f"{self.base_url}/api/v1"
        self.tests = []
        self._setup_tests()
    
    def _setup_tests(self):
        """Setup all endpoint tests"""
        
        # Health check
        self.tests.append(EndpointTest(
            name="Health Check",
            endpoint="/api/v1/health",
            method="GET",
            expected_status=200,
            timeout=5
        ))
        
        # KPI endpoints
        self.tests.append(EndpointTest(
            name="KPI Overview",
            endpoint="/api/v1/kpi/overview",
            method="GET",
            expected_status=200
        ))
        
        self.tests.append(EndpointTest(
            name="KPI By Category",
            endpoint="/api/v1/kpi/category",
            method="GET",
            params={'category': 'sales'},
            expected_status=200
        ))
        
        # Product endpoints
        self.tests.append(EndpointTest(
            name="Product Performance",
            endpoint="/api/v1/products/performance",
            method="GET",
            expected_status=200
        ))
        
        self.tests.append(EndpointTest(
            name="Product KPI",
            endpoint="/api/v1/products/kpi",
            method="GET",
            expected_status=200
        ))
        
        # Sales endpoints
        self.tests.append(EndpointTest(
            name="Sales Summary",
            endpoint="/api/v1/sales/summary",
            method="GET",
            expected_status=200
        ))
        
        # Revenue endpoints
        self.tests.append(EndpointTest(
            name="Revenue Data",
            endpoint="/api/v1/revenue",
            method="GET",
            expected_status=200
        ))
        
        # Customer endpoints
        self.tests.append(EndpointTest(
            name="Customer Data",
            endpoint="/api/v1/customers",
            method="GET",
            expected_status=200
        ))
        
        # Dashboard endpoints
        self.tests.append(EndpointTest(
            name="Dashboard Metrics",
            endpoint="/api/v1/dashboard/metrics",
            method="GET",
            expected_status=200
        ))
        
        # Report endpoints
        self.tests.append(EndpointTest(
            name="Reports List",
            endpoint="/api/v1/reports",
            method="GET",
            expected_status=200
        ))
        
        self.tests.append(EndpointTest(
            name="Report Data",
            endpoint="/api/v1/reports/sales",
            method="GET",
            expected_status=200
        ))
        
        # Anomaly detection
        self.tests.append(EndpointTest(
            name="Anomaly Detection",
            endpoint="/api/v1/anomalies",
            method="GET",
            params={'metric': 'revenue', 'period': '30d'},
            expected_status=200
        ))
        
        # Top performers
        self.tests.append(EndpointTest(
            name="Top Performers",
            endpoint="/api/v1/reports/top-performers",
            method="GET",
            expected_status=200
        ))
    
    def run_all_tests(self) -> Dict[str, Any]:
        """
        Run all endpoint tests.
        
        Returns:
            Dictionary with test results summary
        """
        results = []
        passed = 0
        failed = 0
        total_time = 0
        
        for test in self.tests:
            result = test.run(self.base_url)
            results.append(result)
            
            if result['passed']:
                passed += 1
            else:
                failed += 1
            
            if result['response_time']:
                total_time += result['response_time']
        
        return {
            'total_tests': len(self.tests),
            'passed': passed,
            'failed': failed,
            'success_rate': (passed / len(self.tests)) * 100 if self.tests else 0,
            'total_time': total_time,
            'average_time': total_time / len(self.tests) if self.tests else 0,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
    
    def run_quick_check(self) -> Tuple[bool, Optional[str]]:
        """
        Run quick health check.
        
        Returns:
            Tuple of (is_healthy, error_message)
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/health",
                timeout=5
            )
            if response.status_code == 200:
                return True, None
            return False, f"Health check returned status {response.status_code}"
        
        except requests.exceptions.Timeout:
            return False, "Health check timeout"
        
        except requests.exceptions.ConnectionError:
            return False, "Cannot connect to API service"
        
        except Exception as e:
            return False, str(e)


def display_integration_test_results(results: Dict[str, Any]):
    """
    Display integration test results in Streamlit.
    
    Args:
        results: Test results dictionary from run_all_tests()
    """
    st.subheader("🔗 API Integration Test Results")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tests", results['total_tests'])
    
    with col2:
        st.metric(
            "Passed", 
            results['passed'],
            delta=f"{results['success_rate']:.1f}%"
        )
    
    with col3:
        st.metric("Failed", results['failed'])
    
    with col4:
        st.metric(
            "Avg Response Time",
            f"{results['average_time']*1000:.0f}ms"
        )
    
    # Success rate indicator
    if results['success_rate'] == 100:
        st.success("✅ All tests passed! API integration is healthy.")
    elif results['success_rate'] >= 80:
        st.warning(f"⚠️ {results['failed']} test(s) failed. API integration has issues.")
    else:
        st.error(f"❌ {results['failed']} test(s) failed. API integration is unhealthy.")
    
    # Detailed results
    st.markdown("---")
    st.markdown("### 📋 Detailed Test Results")
    
    # Create DataFrame for results
    test_data = []
    for result in results['results']:
        test_data.append({
            'Test': result['name'],
            'Endpoint': result['endpoint'],
            'Status': '✅ Pass' if result['passed'] else '❌ Fail',
            'Status Code': result.get('status_code', 'N/A'),
            'Response Time': f"{result.get('response_time', 0)*1000:.0f}ms" if result.get('response_time') else 'N/A',
            'Error': result.get('error', '-')
        })
    
    df = pd.DataFrame(test_data)
    
    # Display with filtering
    show_failed_only = st.checkbox("Show failed tests only", value=False)
    
    if show_failed_only:
        df = df[df['Status'] == '❌ Fail']
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Detailed error information
    failed_tests = [r for r in results['results'] if not r['passed']]
    if failed_tests:
        with st.expander(f"❌ Failed Test Details ({len(failed_tests)})"):
            for test in failed_tests:
                st.markdown(f"**{test['name']}**")
                st.code(f"URL: {test['url']}\nError: {test['error']}")
                st.markdown("---")


def display_service_status():
    """Display service status dashboard"""
    st.title("🔗 Service Integration Status")
    
    # Configuration section
    with st.expander("🔧 Configuration", expanded=False):
        from services.config import ConfigManager, EnvironmentValidator
        ConfigManager.display_config(show_sensitive=False)
        st.markdown("---")
        EnvironmentValidator.display_validation_results()
    
    # Quick health check
    st.markdown("### 🏥 Quick Health Check")
    
    if st.button("🔍 Run Health Check", type="primary"):
        with st.spinner("Checking API health..."):
            verifier = APIIntegrationVerifier()
            is_healthy, error = verifier.run_quick_check()
            
            if is_healthy:
                st.success(f"✅ API is healthy and reachable at {verifier.base_url}")
            else:
                st.error(f"❌ API health check failed: {error}")
    
    st.markdown("---")
    
    # Full integration test
    st.markdown("### 🧪 Full Integration Test")
    
    if st.button("🚀 Run All Integration Tests", type="secondary"):
        with st.spinner("Running integration tests..."):
            verifier = APIIntegrationVerifier()
            results = verifier.run_all_tests()
            
            # Cache results in session state
            st.session_state['integration_test_results'] = results
    
    # Display cached results if available
    if 'integration_test_results' in st.session_state:
        results = st.session_state['integration_test_results']
        display_integration_test_results(results)
        
        # Export results option
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export Results as JSON"):
                import json
                json_str = json.dumps(results, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name=f"api_integration_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("🔄 Clear Results"):
                del st.session_state['integration_test_results']
                st.rerun()


def verify_api_integration() -> bool:
    """
    Quick verification that API integration is working.
    
    Returns:
        True if API is accessible, False otherwise
    """
    verifier = APIIntegrationVerifier()
    is_healthy, _ = verifier.run_quick_check()
    return is_healthy
