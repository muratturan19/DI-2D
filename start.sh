#!/bin/bash

# DI-2D Startup Script

echo "🚀 Starting DI-2D - 2D Drawing Intelligence System"
echo ""

# Check if .env exists in backend
if [ ! -f "backend/.env" ]; then
    echo "⚠️  .env file not found in backend/"
    echo "Please create backend/.env with your API keys"
    echo "Example:"
    echo "OPENAI_API_KEY=your_key"
    echo "ANTHROPIC_API_KEY=your_key"
    exit 1
fi

# Start Backend
echo "📦 Starting Backend (Port 8001)..."
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start Frontend
echo "🎨 Starting Frontend (Port 3001)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ DI-2D is running!"
echo ""
echo "📍 Frontend: http://localhost:3001"
echo "📍 Backend API: http://localhost:8001"
echo "📍 API Docs: http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
