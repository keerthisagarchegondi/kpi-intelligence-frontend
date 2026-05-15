"""
Service Configuration and Environment Management

Production-level configuration management for frontend-backend integration:
- Environment-based configuration
- Service discovery
- Configuration validation
- Multi-environment support
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
import streamlit as st


@dataclass
class ServiceConfig:
    """Service configuration dataclass"""
    backend_url: str
    api_version: str
    timeout: int
    max_retries: int
    retry_delay: int
    cache_ttl: int
    environment: str
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        if not self.backend_url:
            raise ValueError("Backend URL cannot be empty")
        
        if not self.backend_url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid backend URL: {self.backend_url}")
        
        if self.timeout <= 0:
            raise ValueError(f"Invalid timeout: {self.timeout}")
        
        if self.max_retries < 0:
            raise ValueError(f"Invalid max_retries: {self.max_retries}")


class ConfigManager:
    """
    Manage application configuration from multiple sources.
    
    Priority order:
    1. Environment variables
    2. Streamlit secrets
    3. Default values
    """
    
    # Default configuration
    DEFAULTS = {
        'BACKEND_URL': 'http://localhost:8000',
        'API_VERSION': 'v1',
        'TIMEOUT': '10',
        'MAX_RETRIES': '3',
        'RETRY_DELAY': '1',
        'CACHE_TTL': '300',
        'ENVIRONMENT': 'development'
    }
    
    @staticmethod
    def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get configuration value from environment.
        
        Args:
            key: Configuration key
            default: Default value if not found
        
        Returns:
            Configuration value or default
        """
        # Try environment variable
        value = os.getenv(key)
        if value:
            return value
        
        # Try Streamlit secrets
        try:
            if key.lower() in st.secrets:
                return st.secrets[key.lower()]
        except Exception:
            pass
        
        # Return default
        return default or ConfigManager.DEFAULTS.get(key)
    
    @staticmethod
    def load_config() -> ServiceConfig:
        """
        Load service configuration from environment.
        
        Returns:
            ServiceConfig instance
        """
        return ServiceConfig(
            backend_url=ConfigManager.get_env('BACKEND_URL', 'http://localhost:8000'),
            api_version=ConfigManager.get_env('API_VERSION', 'v1'),
            timeout=int(ConfigManager.get_env('TIMEOUT', '10')),
            max_retries=int(ConfigManager.get_env('MAX_RETRIES', '3')),
            retry_delay=int(ConfigManager.get_env('RETRY_DELAY', '1')),
            cache_ttl=int(ConfigManager.get_env('CACHE_TTL', '300')),
            environment=ConfigManager.get_env('ENVIRONMENT', 'development')
        )
    
    @staticmethod
    def get_backend_url() -> str:
        """Get backend URL from configuration"""
        return ConfigManager.get_env('BACKEND_URL', 'http://localhost:8000')
    
    @staticmethod
    def is_production() -> bool:
        """Check if running in production environment"""
        env = ConfigManager.get_env('ENVIRONMENT', 'development')
        return env.lower() in ['production', 'prod']
    
    @staticmethod
    def is_development() -> bool:
        """Check if running in development environment"""
        env = ConfigManager.get_env('ENVIRONMENT', 'development')
        return env.lower() in ['development', 'dev']
    
    @staticmethod
    def display_config(show_sensitive: bool = False):
        """
        Display current configuration in Streamlit.
        
        Args:
            show_sensitive: Whether to show sensitive values
        """
        config = ConfigManager.load_config()
        
        st.subheader("🔧 Service Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Environment", config.environment.upper())
            st.metric("Backend URL", config.backend_url if show_sensitive else "***")
            st.metric("API Version", config.api_version)
            st.metric("Timeout", f"{config.timeout}s")
        
        with col2:
            st.metric("Max Retries", config.max_retries)
            st.metric("Retry Delay", f"{config.retry_delay}s")
            st.metric("Cache TTL", f"{config.cache_ttl}s")
            
            if config.environment.lower() == 'production':
                st.success("✅ Production Mode")
            else:
                st.info("🔧 Development Mode")


class EnvironmentValidator:
    """Validate environment configuration"""
    
    @staticmethod
    def validate() -> Dict[str, Any]:
        """
        Validate all environment configuration.
        
        Returns:
            Dictionary with validation results
        """
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'config': {}
        }
        
        try:
            config = ConfigManager.load_config()
            results['config'] = {
                'backend_url': config.backend_url,
                'api_version': config.api_version,
                'timeout': config.timeout,
                'environment': config.environment
            }
        except ValueError as e:
            results['valid'] = False
            results['errors'].append(str(e))
            return results
        
        # Check backend URL format
        if not config.backend_url.startswith(('http://', 'https://')):
            results['valid'] = False
            results['errors'].append(f"Invalid backend URL format: {config.backend_url}")
        
        # Warn about localhost in production
        if config.environment.lower() == 'production' and 'localhost' in config.backend_url:
            results['warnings'].append("Using localhost in production environment")
        
        # Check timeout values
        if config.timeout > 30:
            results['warnings'].append(f"Timeout is very high: {config.timeout}s")
        
        if config.timeout < 5:
            results['warnings'].append(f"Timeout is very low: {config.timeout}s")
        
        # Check cache TTL
        if config.cache_ttl > 3600:
            results['warnings'].append(f"Cache TTL is very high: {config.cache_ttl}s")
        
        return results
    
    @staticmethod
    def display_validation_results():
        """Display validation results in Streamlit"""
        results = EnvironmentValidator.validate()
        
        st.subheader("✅ Configuration Validation")
        
        if results['valid']:
            st.success("✅ Configuration is valid")
        else:
            st.error("❌ Configuration has errors")
        
        if results['errors']:
            st.error("**Errors:**")
            for error in results['errors']:
                st.error(f"  • {error}")
        
        if results['warnings']:
            st.warning("**Warnings:**")
            for warning in results['warnings']:
                st.warning(f"  • {warning}")
        
        # Display configuration details
        with st.expander("📋 Configuration Details"):
            st.json(results['config'])


# Global configuration instance
config = ConfigManager.load_config()


def get_config() -> ServiceConfig:
    """Get global configuration instance"""
    return config


def reload_config() -> ServiceConfig:
    """Reload configuration from environment"""
    global config
    config = ConfigManager.load_config()
    return config
