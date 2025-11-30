#!/bin/bash

# Skill Gap Predictor - Frontend Startup Script
# This script sets up and starts the React development server

set -e  # Exit on any error

echo "🚀 Starting Skill Gap Predictor Frontend..."

# Navigate to frontend directory
cd "$(dirname "$0")"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ from https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm or use yarn."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "⚠️  Warning: Node.js version $NODE_VERSION detected. Node.js 16+ is recommended."
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
else
    echo "🔍 Checking for dependency updates..."
    npm install
fi

# Create .env.local file if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "⚙️  Creating .env.local file..."
    cat > .env.local << EOF
# React App Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=development

# Optional: Analytics configuration
# REACT_APP_GA_TRACKING_ID=your_google_analytics_id

# Optional: Error monitoring
# REACT_APP_SENTRY_DSN=your_sentry_dsn
EOF
    echo "✅ Created .env.local with default configuration"
fi

# Build Tailwind CSS
echo "🎨 Building Tailwind CSS..."
npx tailwindcss build -i ./src/index.css -o ./src/tailwind-output.css --watch &
TAILWIND_PID=$!

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🧹 Cleaning up..."
    kill $TAILWIND_PID 2>/dev/null || true
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Start the React development server
echo "🌐 Starting React development server on http://localhost:3000"
echo ""
echo "The app will automatically open in your default browser."
echo "The page will reload if you make edits."
echo ""
echo "Make sure the backend server is running on http://localhost:8000"
echo "Press Ctrl+C to stop the development server"
echo ""

# Set environment variable to suppress browser opening (optional)
# export BROWSER=none

# Start React development server
BROWSER=default npm start

# Wait for background processes
wait
