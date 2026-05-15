"""
Service Initialization and Health Monitoring

Utilities for initializing service connections and monitoring health.
"""

import streamlit as st
from typing import Dict, Any, Optional
from datetime import datetime
from services.config import ConfigManager
from services.integration import APIIntegrationVerifier


class ServiceInitializer:
    """Initialize and verify service connections on startup"""
    
    @staticmethod
    def initialize() -> Dict[str, Any]:
        """
        Initialize services and return status.
        
        Returns:
            Dictionary with initialization status
        """
        status = {
            'initialized': False,
            'config_loaded': False,
            'api_available': False,
            'timestamp': datetime.now().isoformat(),
            'errors': []
        }
        
        # Load configuration
        try:
            config = ConfigManager.load_config()
            status['config_loaded'] = True
            status['config'] = {
                'backend_url': config.backend_url,
                'environment': config.environment
            }
        except Exception as e:
            status['errors'].append(f"Configuration error: {str(e)}")
            return status
        
        # Check API availability
        try:
            verifier = APIIntegrationVerifier()
            is_healthy, error = verifier.run_quick_check()
            status['api_available'] = is_healthy
            
            if not is_healthy:
                status['errors'].append(f"API unavailable: {error}")
        except Exception as e:
            status['errors'].append(f"API check error: {str(e)}")
        
        # Set overall status
        status['initialized'] = status['config_loaded'] and len(status['errors']) == 0
        
        # Cache in session state
        st.session_state['service_status'] = status
        
        return status
    
    @staticmethod
    def get_status() -> Optional[Dict[str, Any]]:
        """Get cached service status"""
        return st.session_state.get('service_status')
    
    @staticmethod
    def display_status_banner():
        """Display service status banner in sidebar"""
        status = ServiceInitializer.get_status()
        
        if not status:
            status = ServiceInitializer.initialize()
        
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🔗 Service Status")
            
            if status['api_available']:
                st.success("✅ API Connected")
            else:
                st.warning("⚠️ API Offline")
            
            st.caption(f"Environment: {status.get('config', {}).get('environment', 'unknown').upper()}")
            
            if st.button("🔄 Refresh Status", key="refresh_service_status"):
                ServiceInitializer.initialize()
                st.rerun()


class ServiceMonitor:
    """Monitor service health and performance"""
    
    @staticmethod
    def get_health_metrics() -> Dict[str, Any]:
        """
        Get current health metrics.
        
        Returns:
            Dictionary with health metrics
        """
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'api_status': 'unknown',
            'response_time': None,
            'cache_size': 0,
            'session_info': {}
        }
        
        # Check API status
        try:
            verifier = APIIntegrationVerifier()
            import time
            start = time.time()
            is_healthy, error = verifier.run_quick_check()
            response_time = time.time() - start
            
            metrics['api_status'] = 'healthy' if is_healthy else 'unhealthy'
            metrics['response_time'] = response_time
            
            if error:
                metrics['api_error'] = error
        except Exception as e:
            metrics['api_status'] = 'error'
            metrics['api_error'] = str(e)
        
        # Get cache info
        if 'api_cache' in st.session_state:
            metrics['cache_size'] = len(st.session_state.api_cache)
        
        # Get session info
        metrics['session_info'] = {
            'session_id': st.session_state.get('session_id', 'unknown'),
            'keys_count': len(st.session_state)
        }
        
        return metrics
    
    @staticmethod
    def display_monitoring_dashboard():
        """Display monitoring dashboard"""
        st.subheader("📊 Service Monitoring")
        
        metrics = ServiceMonitor.get_health_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            status_color = {
                'healthy': '🟢',
                'unhealthy': '🟡',
                'error': '🔴',
                'unknown': '⚪'
            }.get(metrics['api_status'], '⚪')
            
            st.metric("API Status", f"{status_color} {metrics['api_status'].upper()}")
        
        with col2:
            if metrics['response_time']:
                st.metric("Response Time", f"{metrics['response_time']*1000:.0f}ms")
            else:
                st.metric("Response Time", "N/A")
        
        with col3:
            st.metric("Cache Size", metrics['cache_size'])
        
        with col4:
            st.metric("Session Keys", metrics['session_info']['keys_count'])
        
        # Error details
        if 'api_error' in metrics:
            st.error(f"**Error:** {metrics['api_error']}")
        
        # Detailed metrics
        with st.expander("📋 Detailed Metrics"):
            st.json(metrics)


def initialize_services():
    """
    Initialize services on app startup.
    
    This should be called at the beginning of the main app.
    """
    if 'services_initialized' not in st.session_state:
        with st.spinner("Initializing services..."):
            status = ServiceInitializer.initialize()
            st.session_state['services_initialized'] = True
            
            # Show initialization result
            if not status['api_available']:
                st.warning(
                    "⚠️ **Backend API Unavailable**\n\n"
                    "The application will use sample data for demonstration. "
                    "Check Service Status page for details."
                )


def display_service_info():
    """Display service information in sidebar"""
    ServiceInitializer.display_status_banner()
