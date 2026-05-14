# Production-level Dockerfile for KPI Intelligence Frontend
# Multi-stage build for optimized image size and security

# Stage 1: Base Python image with dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Dependencies installation
FROM base as dependencies

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Application
FROM base as application

# Copy installed dependencies from previous stage
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Create non-root user for security
RUN useradd -m -u 1000 streamlit && \
    mkdir -p /app/.streamlit && \
    chown -R streamlit:streamlit /app

# Copy application code
COPY --chown=streamlit:streamlit . .

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/.streamlit && \
    chown -R streamlit:streamlit /app/data /app/logs /app/.streamlit

# Switch to non-root user
USER streamlit

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Set entrypoint
ENTRYPOINT ["streamlit", "run", "app/main.py"]

# Default command arguments
CMD ["--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
