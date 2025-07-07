#!/bin/bash

# AI Insight Startup Script

echo "🚀 Starting AI Insight Application..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    echo "Run: python -m venv .venv && .venv/Scripts/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment (Windows)
if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "❌ Cannot find virtual environment activation script"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys and configuration"
fi

# Start FastAPI backend
echo "🔧 Starting FastAPI backend on port 8001..."
python run_server.py &
FASTAPI_PID=$!

# Wait a moment for backend to start
sleep 3

# Start Streamlit frontend
echo "🎨 Starting Streamlit frontend on port 8501..."
streamlit run app_ui/streamlit_app.py --server.port 8501 &
STREAMLIT_PID=$!

echo ""
echo "✅ AI Insight is running!"
echo "📊 Frontend: http://localhost:8501"
echo "🔧 Backend API: http://localhost:8001"
echo "📖 API Docs: http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo 'Stopping services...'; kill $FASTAPI_PID $STREAMLIT_PID; exit" INT
wait
