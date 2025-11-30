#!/bin/bash

# Skill Gap Predictor - Backend Startup Script
# This script sets up and starts the FastAPI backend server

set -e  # Exit on any error

echo "🚀 Starting Skill Gap Predictor Backend..."

# Navigate to backend directory
cd "$(dirname "$0")"

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Set up NLP dependencies
echo "🧠 Setting up NLP models and data..."
python setup_nlp.py

# Set up environment variables if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "✅ Environment configuration created!"
    echo "   The application now uses free, local NLP processing - no API keys needed!"
    echo ""
fi

# Create database directory
mkdir -p database

# Populate database with industry skills
echo "🗄️  Setting up database..."
cd ../database
python populate_skills.py
cd ../backend

# Start the FastAPI server
echo "🌐 Starting FastAPI server on http://localhost:8000"
echo ""
echo "API Documentation will be available at:"
echo "  • Swagger UI: http://localhost:8000/docs"
echo "  • ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run with auto-reload for development
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
