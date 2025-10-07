# Personalized Content Recommender - AI Powered

🚀 An AI-powered content recommendation system that provides personalized content suggestions based on user preferences and regional trends.

## Features

- 📊 Interactive Statistics Dashboard
- 🎯 Smart Content Recommendations  
- 🌍 Regional Trending Analysis
- 🤖 AI-Powered Predictions
- 🎭 Multi-Level Interest Selection

## Project Structure

```
personalized-content-recommender/
├── README.md
├── start.sh
├── requirements.txt
├── .env
├── backend/
│   ├── app.py
│   ├── enhanced_regional_suggester.py
│   ├── models.py
│   └── requirements.txt
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js
│       ├── App.css
│       ├── index.js
│       └── components/
│           ├── Login.js
│           ├── Register.js
│           ├── StatisticsDashboard.js
│           ├── GenreSelector.js
│           ├── Recommendations.js
│           └── PredictionResults.js
```

## Quick Start

1. **Prerequisites**
   - Python 3.9+
   - Node.js 16+
   - MongoDB 4.4+

2. **Start MongoDB**
   ```bash
   sudo systemctl start mongod
   # or
   mongod --dbpath /path/to/your/data/directory
   ```

3. **Run the application**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## User Journey

1. **Login/Register** → Create account with nationality
2. **Statistics Dashboard** (skippable) → View regional trending data  
3. **Interest Selection** → Choose content categories
4. **Smart Recommendations** → Get personalized content suggestions
5. **AI Predictions** → Receive AI-powered content predictions

## Technologies Used

### Backend
- Flask (Python web framework)
- MongoDB (Database)
- YouTube Data API
- Pandas/NumPy (Data processing)

### Frontend  
- React.js
- Chart.js (Statistics visualization)
- Axios (HTTP client)
- CSS3 with modern styling

## Configuration

Update `.env` file with your configurations:
- `YOUTUBE_API_KEY`: Your YouTube Data API key
- `MONGODB_URL`: MongoDB connection string
- `DATABASE_NAME`: Database name (default: Recommend)
- `COLLECTION_NAME`: Collection name (default: system)

## License

© 2025 Personalized Content Recommender - AI Powered
