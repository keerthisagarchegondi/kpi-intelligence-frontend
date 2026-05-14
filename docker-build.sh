#!/bin/bash
# Docker build and run scripts for KPI Intelligence Frontend

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}KPI Intelligence Frontend - Docker Build${NC}"
echo -e "${BLUE}========================================${NC}"

# Build production image
build_prod() {
    echo -e "${GREEN}Building production image...${NC}"
    docker build -t kpi-intelligence-frontend:latest -f Dockerfile .
    echo -e "${GREEN}✓ Production image built successfully${NC}"
}

# Build development image
build_dev() {
    echo -e "${GREEN}Building development image...${NC}"
    docker build -t kpi-intelligence-frontend:dev -f Dockerfile.dev .
    echo -e "${GREEN}✓ Development image built successfully${NC}"
}

# Run production container
run_prod() {
    echo -e "${GREEN}Starting production container...${NC}"
    docker run -d \
        --name kpi-frontend \
        -p 8501:8501 \
        -v $(pwd)/data:/app/data \
        -v $(pwd)/logs:/app/logs \
        -e BACKEND_API_URL=http://localhost:8000 \
        kpi-intelligence-frontend:latest
    echo -e "${GREEN}✓ Container started on http://localhost:8501${NC}"
}

# Run development container
run_dev() {
    echo -e "${GREEN}Starting development container...${NC}"
    docker run -d \
        --name kpi-frontend-dev \
        -p 8501:8501 \
        -v $(pwd):/app \
        -e BACKEND_API_URL=http://localhost:8000 \
        kpi-intelligence-frontend:dev
    echo -e "${GREEN}✓ Dev container started on http://localhost:8501${NC}"
}

# Stop containers
stop() {
    echo -e "${GREEN}Stopping containers...${NC}"
    docker stop kpi-frontend kpi-frontend-dev 2>/dev/null || true
    docker rm kpi-frontend kpi-frontend-dev 2>/dev/null || true
    echo -e "${GREEN}✓ Containers stopped${NC}"
}

# View logs
logs() {
    echo -e "${GREEN}Viewing logs...${NC}"
    docker logs -f kpi-frontend
}

# Docker compose commands
compose_up() {
    echo -e "${GREEN}Starting services with Docker Compose...${NC}"
    docker-compose up -d
    echo -e "${GREEN}✓ Services started${NC}"
}

compose_down() {
    echo -e "${GREEN}Stopping Docker Compose services...${NC}"
    docker-compose down
    echo -e "${GREEN}✓ Services stopped${NC}"
}

# Main command handler
case "$1" in
    build-prod)
        build_prod
        ;;
    build-dev)
        build_dev
        ;;
    run-prod)
        run_prod
        ;;
    run-dev)
        run_dev
        ;;
    stop)
        stop
        ;;
    logs)
        logs
        ;;
    compose-up)
        compose_up
        ;;
    compose-down)
        compose_down
        ;;
    *)
        echo "Usage: $0 {build-prod|build-dev|run-prod|run-dev|stop|logs|compose-up|compose-down}"
        exit 1
        ;;
esac
