#!/bin/bash
# Dynamic YAML Form Generator - Run Script

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Dynamic YAML Form Generator${NC}"
echo -e "${BLUE}=================================${NC}"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ Error: uv is not installed${NC}"
    echo -e "Please install uv first: ${BLUE}curl -LsSf https://astral.sh/uv/install.sh | sh${NC}"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "src/app.py" ]; then
    echo -e "${RED}❌ Error: src/app.py not found${NC}"
    echo -e "Please run this script from the project root directory"
    exit 1
fi

# Set PYTHONPATH to include src directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

echo -e "${GREEN}✅ Starting application...${NC}"
echo -e "📁 Working directory: $(pwd)"
echo -e "🐍 Python path: $PYTHONPATH"
echo -e ""

# Run the Streamlit app
cd src
uv run streamlit run app.py

echo -e "\n${GREEN}✅ Application stopped${NC}"