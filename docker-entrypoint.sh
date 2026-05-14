#!/bin/bash
# Production startup script for KPI Intelligence Frontend
# This script handles initialization and graceful startup

set -e

echo "=========================================="
echo "KPI Intelligence Frontend - Starting..."
echo "=========================================="

# Print environment info
echo "Python version: $(python --version)"
echo "Streamlit version: $(streamlit --version)"
echo "Working directory: $(pwd)"
echo "User: $(whoami)"

# Check if backend API is reachable (optional)
if [ -n "$BACKEND_API_URL" ]; then
    echo "Checking backend connectivity at $BACKEND_API_URL..."
    # Add health check logic here if needed
fi

# Create necessary directories
mkdir -p /app/data /app/logs /app/.streamlit

# Set permissions
chmod -R 755 /app/data /app/logs

# Start Streamlit
echo "Starting Streamlit application on port ${STREAMLIT_SERVER_PORT:-8501}..."
exec streamlit run app/main.py \
    --server.port="${STREAMLIT_SERVER_PORT:-8501}" \
    --server.address="${STREAMLIT_SERVER_ADDRESS:-0.0.0.0}" \
    --server.headless="${STREAMLIT_SERVER_HEADLESS:-true}" \
    --browser.gatherUsageStats="${STREAMLIT_BROWSER_GATHER_USAGE_STATS:-false}" \
    --server.maxUploadSize="${STREAMLIT_MAX_UPLOAD_SIZE:-50}" \
    --server.enableCORS="${STREAMLIT_ENABLE_CORS:-false}" \
    --server.enableXsrfProtection="${STREAMLIT_ENABLE_XSRF:-true}"
