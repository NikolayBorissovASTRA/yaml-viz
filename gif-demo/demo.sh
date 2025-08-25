#!/bin/bash

show_help() {
    echo "GIF Demo Generator"
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  setup     Install dependencies (Playwright, ffmpeg)"
    echo "  prepare   Create sample YAML templates"  
    echo "  generate  Generate GIF (requires running app)"
    echo "  pipeline  Complete pipeline (setup, start app, generate, cleanup)"
    echo "  status    Check installation and dependencies"
    echo "  help      Show this help"
    echo ""
    echo "Environment Variables (Configuration):"
    echo "  GIF_NAME=demo.gif              # Output GIF filename"
    echo "  VIEWPORT_WIDTH=800             # Recording viewport width"
    echo "  VIEWPORT_HEIGHT=1000           # Recording viewport height"
    echo "  FINAL_WIDTH=500                # Final GIF width"
    echo "  FINAL_HEIGHT=650               # Final GIF height"
    echo "  FPS=6                          # Frames per second"
    echo "  MAX_COLORS=128                 # Color palette size"
    echo "  APP_URL=http://localhost:8501  # Application URL"
    echo "  TEMPLATE_FILE=pp.yml           # YAML template to use"
    echo "  PROJECT_NAME='Highway Demo'    # Form project name"
    echo "  SIZE_LIMIT_MB=1.0              # Size limit for compression"
    echo "  ULTRA_COMPRESS=true            # Enable ultra compression"
    echo ""
    echo "Examples:"
    echo "  $0 pipeline                    # Complete automated workflow"
    echo "  GIF_NAME=custom.gif $0 pipeline  # Custom GIF name"
    echo "  SIZE_LIMIT_MB=0.5 $0 generate    # Smaller size limit"
}

setup_dependencies() {
    echo "Setting up dependencies..."
    
    # Detect package manager preference
    if command -v uv &> /dev/null; then
        echo "Using uv package manager..."
        cd ..
        uv add playwright
        echo "Installing Playwright browsers..."
        uv run playwright install chromium
        cd gif-demo
    elif command -v python3 &> /dev/null; then
        echo "Using pip package manager..."
        cd ..
        
        # Create virtual environment if it doesn't exist
        if [ ! -d ".venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv .venv
        fi
        
        # Activate virtual environment
        source .venv/bin/activate
        
        echo "Installing Python dependencies..."
        pip install --upgrade pip
        pip install -r requirements.txt
        
        echo "Installing Playwright browsers..."
        python -m playwright install chromium
        
        cd gif-demo
    else
        echo "Neither uv nor python3 found. Please install Python 3.10+ or uv"
        exit 1
    fi
    
    echo "Installing ffmpeg..."
    if ! command -v ffmpeg &> /dev/null; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            if command -v brew &> /dev/null; then
                brew install ffmpeg
            else
                echo "Install Homebrew first, then: brew install ffmpeg"
                exit 1
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            if command -v apt &> /dev/null; then
                sudo apt update && sudo apt install -y ffmpeg
            elif command -v yum &> /dev/null; then
                sudo yum install -y ffmpeg
            else
                echo "Install ffmpeg manually"
                exit 1
            fi
        else
            echo "Install ffmpeg manually"
            exit 1
        fi
    fi
    
    chmod +x create-interactive-gif.py
    echo "Setup complete"
}

check_status() {
    echo "🔍 Checking installation status..."
    
    # Check Python
    if python3 --version &> /dev/null; then
        python_version=$(python3 --version)
        echo "✅ $python_version"
    else
        echo "❌ Python 3 not found"
    fi
    
    # Check package manager
    if command -v uv &> /dev/null; then
        uv_version=$(uv --version)
        echo "✅ uv found: $uv_version"
        manager="uv"
    elif command -v pip &> /dev/null; then
        pip_version=$(pip --version | cut -d' ' -f1-2)
        echo "✅ pip found: $pip_version"
        manager="pip"
    else
        echo "❌ No package manager found (uv or pip)"
        manager="none"
    fi
    
    # Check virtual environment for pip setup
    if [ "$manager" = "pip" ] && [ -d "../.venv" ]; then
        echo "✅ Virtual environment found (.venv)"
    elif [ "$manager" = "pip" ]; then
        echo "⚠️  Virtual environment not found (run: ./run-pip.sh)"
    fi
    
    # Check ffmpeg
    if command -v ffmpeg &> /dev/null; then
        ffmpeg_version=$(ffmpeg -version 2>/dev/null | head -1 | cut -d' ' -f3)
        echo "✅ ffmpeg found: $ffmpeg_version"
    else
        echo "❌ ffmpeg not found (needed for GIF conversion)"
    fi
    
    # Check Playwright
    if [ "$manager" = "uv" ]; then
        if uv run python -c "import playwright" &> /dev/null; then
            echo "✅ Playwright installed (uv)"
        else
            echo "❌ Playwright not installed (run: ./gif-demo/demo.sh setup)"
        fi
    elif [ "$manager" = "pip" ] && [ -f "../.venv/bin/activate" ]; then
        source ../.venv/bin/activate
        if python -c "import playwright" &> /dev/null; then
            echo "✅ Playwright installed (pip)"
        else
            echo "❌ Playwright not installed (run: ./gif-demo/demo.sh setup)"
        fi
    fi
    
    echo ""
    echo "💡 Package manager detected: $manager"
    if [ "$manager" = "uv" ]; then
        echo "   Use: ./run.sh to start the app"
    elif [ "$manager" = "pip" ]; then
        echo "   Use: ./run-pip.sh to start the app"
    fi
}

prepare_templates() {
    echo "Preparing demo templates..."
    
    mkdir -p demo-data
    
    cat > demo-data/sample-config.yml << 'EOF'
Application:
  name: "Demo Web App"
  version: "2.0.0"
  environment: "development"
Database:
  host: "localhost"
  port: 5432
  name: "demo_db"
Features:
  - "user-authentication"
  - "api-endpoints"
  - "file-upload"
Deployment:
  auto_deploy: false
  backup_enabled: true
EOF
    
    cat > demo-data/user-profile.yml << 'EOF'
UserProfile:
  name: "Demo User"
  email: "demo@example.com"
  age: 25
  active: true
Preferences:
  theme: "light"
  language: "en"
  notifications:
    - "email"
Permissions:
  admin: false
  editor: true
  viewer: true
EOF
    
    echo "Sample templates created in demo-data/"
}

generate_gif() {
    echo "Starting GIF generation..."
    echo "Ensure Streamlit app is running at http://localhost:8501"
    
    if ! curl -s http://localhost:8501 > /dev/null; then
        echo "App not running at localhost:8501"
        read -p "Start app manually and press Enter to continue..."
    fi
    
    cd "$(dirname "$0")"
    
    # Use appropriate Python execution method
    if command -v uv &> /dev/null && [ -f "../pyproject.toml" ]; then
        uv run python create-interactive-gif.py
    else
        # Activate virtual environment for pip
        if [ -f "../.venv/bin/activate" ]; then
            source ../.venv/bin/activate
        fi
        python create-interactive-gif.py
    fi
}

run_pipeline() {
    echo "Starting complete GIF demo pipeline..."
    
    # Check dependencies and start app if needed
    echo "Checking if Streamlit app is running..."
    if ! curl -s http://localhost:8501 > /dev/null; then
        echo "Starting Streamlit app..."
        cd ..
        
        # Use appropriate execution method
        if command -v uv &> /dev/null && [ -f "pyproject.toml" ]; then
            uv run streamlit run src/app.py &
        else
            # Activate virtual environment for pip
            if [ -f ".venv/bin/activate" ]; then
                source .venv/bin/activate
            fi
            python -m streamlit run src/app.py &
        fi
        
        APP_PID=$!
        cd gif-demo
        
        echo "Waiting for app to start..."
        for i in {1..30}; do
            if curl -s http://localhost:8501 > /dev/null; then
                echo "App is running"
                break
            fi
            sleep 1
        done
        
        if ! curl -s http://localhost:8501 > /dev/null; then
            echo "Failed to start app"
            exit 1
        fi
    fi
    
    echo "Generating enhanced GIF demo..."
    cd "$(dirname "$0")"
    
    # Use appropriate Python execution method
    if command -v uv &> /dev/null && [ -f "../pyproject.toml" ]; then
        uv run python create-interactive-gif.py
    else
        # Activate virtual environment for pip
        if [ -f "../.venv/bin/activate" ]; then
            source ../.venv/bin/activate
        fi
        python create-interactive-gif.py
    fi
    
    if [ $? -eq 0 ]; then
        GIF_NAME=${GIF_NAME:-demo.gif}
        echo "Moving GIF to project root..."
        mv "$GIF_NAME" "../$GIF_NAME" 2>/dev/null || true
        echo "Pipeline completed successfully"
        echo "GIF saved as $GIF_NAME in project root"
    else
        echo "GIF generation failed"
        exit 1
    fi
    
    if [ ! -z "$APP_PID" ]; then
        echo "Stopping Streamlit app..."
        kill $APP_PID 2>/dev/null || true
    fi
}

# Main script logic
case "${1:-help}" in
    setup)
        setup_dependencies
        ;;
    prepare)
        prepare_templates
        ;;
    generate)
        generate_gif
        ;;
    pipeline)
        run_pipeline
        ;;
    status)
        check_status
        ;;
    help|*)
        show_help
        ;;
esac