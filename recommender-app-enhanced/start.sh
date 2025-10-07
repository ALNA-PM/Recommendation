#!/bin/bash
echo "🚀 Enhanced Content Recommender - Complete Setup"
echo "================================================================"
echo "📊 Database: Recommend → Collection: system"
echo "🔗 Connection: Recommender (mongodb://localhost:27017/)"
echo "🌟 Enhanced Features:"
echo "   📈 Interactive statistics dashboard"
echo "   🎯 Smart content recommendations"
echo "   🌍 Regional trending analysis"
echo "   🎭 Multi-level interest selection"
echo "================================================================"
echo ""

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "❌ MongoDB is not running!"
    echo ""
    echo "Please start MongoDB first:"
    echo "   sudo systemctl start mongod"
    echo "   or"
    echo "   mongod --dbpath /path/to/your/data/directory"
    echo ""
    exit 1
fi

echo "✅ MongoDB is running"
echo ""

# Function to start backend
start_backend() {
    echo "🔧 Starting Enhanced Backend (Flask + Trending Analysis)..."
    cd backend
    pip install -r requirements.txt > /dev/null 2>&1
    python app.py &
    BACKEND_PID=$!
    cd ..
    echo "✅ Backend started (PID: $BACKEND_PID)"
}

# Function to start frontend
start_frontend() {
    echo "🎨 Starting Enhanced Frontend (React + Chart.js)..."
    cd frontend
    npm install > /dev/null 2>&1
    npm start &
    FRONTEND_PID=$!
    cd ..
    echo "✅ Frontend started (PID: $FRONTEND_PID)"
}

# Start both services
start_backend
sleep 5
start_frontend

echo ""
echo "🎉 Enhanced Application started successfully!"
echo "================================================================"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000"
echo "📊 Database: Recommend → system"
echo "🌟 Features: Statistics Dashboard + Smart Recommendations"
echo "================================================================"
echo ""
echo "🎯 User Journey:"
echo "   1. Login/Register → 2. Statistics Dashboard (skippable)"
echo "   3. Interest Selection → 4. Smart Recommendations"
echo ""
echo "Press Ctrl+C to stop both services..."

# Wait for interrupt
trap 'echo ""; echo "🛑 Stopping enhanced services..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit' INT
wait
