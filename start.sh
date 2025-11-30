#!/bin/bash

# Skill Gap Predictor - Main Startup Script
# This script starts both backend and frontend servers

set -e  # Exit on any error

echo "🎯 Skill Gap Predictor - Full-Stack Startup"
echo "============================================"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is available
port_available() {
    ! lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1
}

# Function to wait for a service to be ready
wait_for_service() {
    local url=$1
    local name=$2
    local timeout=30
    local count=0
    
    echo "⏳ Waiting for $name to be ready..."
    while ! curl -s "$url" >/dev/null 2>&1; do
        sleep 2
        count=$((count + 2))
        if [ $count -ge $timeout ]; then
            echo "❌ Timeout waiting for $name to start"
            return 1
        fi
    done
    echo "✅ $name is ready!"
}

# Check system requirements
echo "🔍 Checking system requirements..."

# Check Python
if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ from https://python.org/"
    exit 1
fi

# Check Node.js
if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ from https://nodejs.org/"
    exit 1
fi

# Check if ports are available
if ! port_available 8000; then
    echo "❌ Port 8000 is already in use. Please stop any services running on port 8000."
    exit 1
fi

if ! port_available 3000; then
    echo "❌ Port 3000 is already in use. Please stop any services running on port 3000."
    exit 1
fi

echo "✅ System requirements check passed!"
echo ""

# Create log directory
mkdir -p logs

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🧹 Shutting down services..."
    
    # Kill background processes
    jobs -p | xargs -r kill 2>/dev/null || true
    
    # Additional cleanup
    pkill -f "uvicorn main:app" 2>/dev/null || true
    pkill -f "react-scripts start" 2>/dev/null || true
    
    echo "👋 Goodbye!"
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM EXIT

# Start backend server
echo "🔧 Starting backend server..."
cd backend

# Setup and start backend in background
(
    if [ ! -d "venv" ]; then
        echo "📦 Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    python -m pip install --upgrade pip >/dev/null 2>&1
    pip install -r requirements.txt >/dev/null 2>&1
    
    # Setup environment
    if [ ! -f ".env" ]; then
        cp .env.example .env
        echo "⚠️  Please update .env file with your API keys!"
    fi
    
    # Setup database
    mkdir -p database
    cd ../database
    python populate_skills.py >/dev/null 2>&1
    cd ../backend
    
    # Start server
    python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
) > logs/backend.log 2>&1 &

BACKEND_PID=$!

# Wait for backend to be ready
sleep 5
wait_for_service "http://localhost:8000/health" "Backend API"

# Start frontend server
echo "🎨 Starting frontend server..."
cd ../frontend

# Setup and start frontend in background
(
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing Node.js dependencies..."
        npm install >/dev/null 2>&1
    fi
    
    # Create environment file
    if [ ! -f ".env.local" ]; then
        echo "REACT_APP_API_URL=http://localhost:8000" > .env.local
    fi
    
    # Start development server
    BROWSER=none npm start
) > logs/frontend.log 2>&1 &

FRONTEND_PID=$!

# Wait for frontend to be ready
sleep 10
wait_for_service "http://localhost:3000" "Frontend App"

# Display success message
echo ""
echo "🎉 Skill Gap Predictor is now running!"
echo "======================================"
echo ""
echo "📱 Frontend Application:"
echo "   URL: http://localhost:3000"
echo "   Status: ✅ Running"
echo ""
echo "🔧 Backend API:"
echo "   URL: http://localhost:8000"
echo "   Status: ✅ Running"
echo "   Docs: http://localhost:8000/docs"
echo ""
echo "📊 Features Available:"
echo "   • PDF syllabus upload and analysis"
echo "   • Text-based syllabus analysis"
echo "   • AI-powered skill extraction"
echo "   • Industry skill gap comparison"
echo "   • Learning recommendations"
echo "   • Interactive data visualizations"
echo ""
echo "📝 Logs:"
echo "   • Backend: logs/backend.log"
echo "   • Frontend: logs/frontend.log"
echo ""
echo "🌐 Open http://localhost:3000 in your browser to get started!"
echo ""
echo "Press Ctrl+C to stop all services"
echo "============================================"

# Keep script running and monitor services
while true; do
    # Check if backend is still running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "❌ Backend server stopped unexpectedly"
        break
    fi
    
    # Check if frontend is still running
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "❌ Frontend server stopped unexpectedly"
        break
    fi
    
    sleep 5
done

# If we get here, one of the services failed
echo "⚠️  One or more services have stopped. Check the logs for details."
cleanup
