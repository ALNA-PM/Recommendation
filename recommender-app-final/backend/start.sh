#!/bin/bash
echo "🚀 Starting Content Recommender Backend..."
echo "================================================================"
echo "📊 Database Configuration:"
echo "   Database Name: Recommend"
echo "   Collection Name: system" 
echo "   Connection: Recommender"
echo "   MongoDB URL: mongodb://localhost:27017/"
echo "================================================================"
echo ""

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB is not running. Please start MongoDB first:"
    echo "   sudo systemctl start mongod"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "🌐 Starting Flask server on http://localhost:5000"
echo "================================================================"
python app.py
