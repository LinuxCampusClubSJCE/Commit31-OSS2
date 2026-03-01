#!/bin/bash

echo "🚀 Ghost Labs - Quick Start Script"
echo "=================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo "✅ Docker found: $(docker --version)"
echo ""

# Build workspace image
echo "📦 Building workspace Docker image..."
docker build -t ghost-labs-workspace:latest -f docker/workspace/Dockerfile docker/workspace

if [ $? -ne 0 ]; then
    echo "❌ Failed to build workspace image"
    exit 1
fi

echo "✅ Workspace image built successfully"
echo ""

# Ask user for setup preference
echo "Choose setup method:"
echo "1) Docker Compose (Recommended - runs everything)"
echo "2) Manual setup (Development - run services individually)"
read -p "Enter your choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "🐳 Starting all services with Docker Compose..."
    docker-compose up -d
    
    echo ""
    echo "✅ All services started!"
    echo ""
    echo "Access the application at:"
    echo "  Frontend:    http://localhost:3000"
    echo "  Backend API: http://localhost:8000"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
    
elif [ "$choice" = "2" ]; then
    echo ""
    echo "📝 Manual setup selected. Follow these steps:"
    echo ""
    echo "Terminal 1 - Backend:"
    echo "  cd backend"
    echo "  pip install -r requirements.txt"
    echo "  uvicorn main:socket_app --reload --port 8000"
    echo ""
    echo "Terminal 2 - Frontend:"
    echo "  cd frontend"
    echo "  npm install"
    echo "  npm run dev"
    echo ""
else
    echo "Invalid choice. Exiting."
    exit 1
fi

echo ""
echo "🎉 Setup complete! Happy coding!"
