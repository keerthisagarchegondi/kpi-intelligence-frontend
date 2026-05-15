#!/bin/bash
# Service Setup and Verification Script
# Production-level initialization and testing

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}KPI Intelligence Frontend - Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if .env exists
check_env() {
    echo -e "${BLUE}Checking environment configuration...${NC}"
    
    if [ ! -f .env ]; then
        echo -e "${YELLOW}⚠️  No .env file found${NC}"
        echo -e "${YELLOW}Creating .env from template...${NC}"
        
        if [ -f .env.template ]; then
            cp .env.template .env
            echo -e "${GREEN}✓ Created .env file${NC}"
            echo -e "${YELLOW}⚠️  Please edit .env and configure your backend URL${NC}"
        else
            echo -e "${RED}✗ .env.template not found${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✓ .env file exists${NC}"
    fi
    
    # Check backend URL
    if [ -f .env ]; then
        source .env
        echo -e "  Backend URL: ${BACKEND_URL}"
        echo -e "  Environment: ${ENVIRONMENT}"
    fi
    
    echo ""
}

# Install dependencies
install_deps() {
    echo -e "${BLUE}Installing dependencies...${NC}"
    
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python -m venv venv
        echo -e "${GREEN}✓ Virtual environment created${NC}"
    fi
    
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source venv/bin/activate || source venv/Scripts/activate
    
    echo -e "${YELLOW}Installing requirements...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
    echo ""
}

# Verify API connection
verify_api() {
    echo -e "${BLUE}Verifying API connection...${NC}"
    
    if [ -f .env ]; then
        source .env
        
        echo -e "  Testing: ${BACKEND_URL}/api/v1/health"
        
        # Try to connect to API
        if command -v curl &> /dev/null; then
            if curl -f -s "${BACKEND_URL}/api/v1/health" > /dev/null 2>&1; then
                echo -e "${GREEN}✓ API is reachable and healthy${NC}"
            else
                echo -e "${YELLOW}⚠️  API is not reachable${NC}"
                echo -e "${YELLOW}   Make sure backend service is running${NC}"
            fi
        else
            echo -e "${YELLOW}⚠️  curl not found, skipping API check${NC}"
        fi
    fi
    
    echo ""
}

# Run integration tests
run_tests() {
    echo -e "${BLUE}Running integration tests...${NC}"
    
    source venv/bin/activate || source venv/Scripts/activate
    
    if python -m pytest tests/test_integration.py -v; then
        echo -e "${GREEN}✓ Integration tests passed${NC}"
    else
        echo -e "${YELLOW}⚠️  Some integration tests failed${NC}"
    fi
    
    echo ""
}

# Display summary
display_summary() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Setup Summary${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${GREEN}✓ Environment configured${NC}"
    echo -e "${GREEN}✓ Dependencies installed${NC}"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo -e "  1. Edit .env file to configure backend URL"
    echo -e "  2. Start backend service (if not running)"
    echo -e "  3. Run: ${GREEN}streamlit run app/main.py${NC}"
    echo -e "  4. Visit: ${GREEN}http://localhost:8501${NC}"
    echo -e "  5. Check Service Status page for API integration"
    echo ""
}

# Main execution
main() {
    check_env
    install_deps
    verify_api
    
    # Optionally run tests
    if [ "$1" = "--test" ]; then
        run_tests
    fi
    
    display_summary
}

main "$@"
