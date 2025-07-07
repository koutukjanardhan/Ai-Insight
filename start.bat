@echo off
REM AI Insight Startup Script for Windows

echo 🚀 Starting AI Insight Application...

REM Check if virtual environment exists
if not exist ".venv" (
    echo ❌ Virtual environment not found. Please run setup first.
    echo Run: python -m venv .venv ^&^& .venv\Scripts\activate ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if database exists
if not exist "%DATABASE_PATH%" (
    if not exist "sakila.db" (
        echo ⚠️  No database found. Please set up a database first.
        echo See README.md for database setup instructions.
        pause
        exit /b 1
    )
)

REM Build vector index if it doesn't exist
if not exist "retriever\faiss_index\schema.index" (
    echo 🔧 Building vector index...
    python retriever\build_index.py
    if errorlevel 1 (
        echo ❌ Failed to build vector index
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found. Copying from .env.example...
    copy .env.example .env
    echo 📝 Please edit .env file with your API keys and configuration
)

REM Start FastAPI backend
echo 🔧 Starting FastAPI backend on port 8001...
start "FastAPI Backend" python app\main.py

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start Streamlit frontend
echo 🎨 Starting Streamlit frontend on port 8501...
start "Streamlit Frontend" streamlit run app_ui/streamlit_app.py --server.port 8501

echo.
echo ✅ AI Insight is running!
echo 📊 Frontend: http://localhost:8501
echo 🔧 Backend API: http://localhost:8001
echo 📖 API Docs: http://localhost:8001/docs
echo.
echo Press any key to stop all services
pause > nul

REM Kill background processes (simplified)
taskkill /f /im python.exe > nul 2>&1
taskkill /f /im streamlit.exe > nul 2>&1
