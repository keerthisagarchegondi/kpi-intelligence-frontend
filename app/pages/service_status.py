"""
Service Status Page

Production-level service status and integration verification dashboard.
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.integration import display_service_status

# Page configuration
st.set_page_config(
    page_title="Service Status - KPI Intelligence",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Display service status dashboard
display_service_status()

# Additional information
st.markdown("---")
st.markdown("""
### 📚 About This Dashboard

This dashboard provides comprehensive monitoring of the frontend-backend integration:

- **Configuration Validation**: Ensures environment variables and settings are correct
- **Health Check**: Quick verification that the backend API is reachable
- **Integration Tests**: Comprehensive testing of all API endpoints
- **Performance Metrics**: Response time monitoring for each endpoint
- **Error Diagnosis**: Detailed error information for failed tests

### 🔧 Configuration Sources

Configuration is loaded from multiple sources in priority order:
1. **Environment Variables**: `BACKEND_URL`, `API_VERSION`, `TIMEOUT`, etc.
2. **Streamlit Secrets**: `.streamlit/secrets.toml`
3. **Default Values**: Fallback defaults for development

### 🚀 Usage

1. Click **Run Health Check** for a quick API status verification
2. Click **Run All Integration Tests** for comprehensive endpoint testing
3. Review results and export as JSON if needed
4. Check configuration details in the expandable sections

### ❗ Troubleshooting

If tests fail:
- Verify backend service is running
- Check `BACKEND_URL` environment variable
- Review network connectivity
- Check backend API logs for errors
""")
