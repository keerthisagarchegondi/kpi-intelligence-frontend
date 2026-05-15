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

# Check if backend API is reachable
if [ -n "$BACKEND_URL" ]; then
    echo "Checking backend connectivity at $BACKEND_URL..."
    
    # Wait for backend to be available (with timeout)
    timeout=30
    elapsed=0
    while [ $elapsed -lt $timeout ]; do
        if curl -f -s "$BACKEND_URL/api/v1/health" > /dev/null 2>&1; then
            echo "✓ Backend API is reachable"
            break
        else
            echo "⏳ Waiting for backend API... ($elapsed/$timeout)"
            sleep 2
            elapsed=$((elapsed + 2))
        fi
    done
    
    if [ $elapsed -ge $timeout ]; then
        echo "⚠️  Backend API not reachable after ${timeout}s. Starting anyway (will use sample data)"
    fi
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
