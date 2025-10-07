# Enhanced Content Recommender - Smart Trending Analysis

A comprehensive full-stack application that combines regional trending analysis with personalized content recommendations. Built with Flask (Python) backend and React frontend, featuring interactive statistics dashboards and multi-level interest selection.

## 🌟 Enhanced Features

### 🎯 Smart Content Recommendations
- **Regional Trending Analysis**: Real-time trending topics from user's nationality
- **Personalized Suggestions**: AI-powered recommendations based on interests
- **Content Strategy Insights**: Difficulty levels, monetization potential, keyword analysis
- **Multiple Content Angles**: Various approaches for each recommended topic

### 📊 Interactive Statistics Dashboard
- **Visual Charts**: Bar charts and doughnut charts using Chart.js
- **Trending Keywords**: Real-time keyword analysis with frequency data
- **Regional Insights**: Category-wise content distribution
- **Skippable Interface**: Users can skip or continue through dashboard

### 🌍 Nationality-Based Personalization
- **Country Selection**: Dropdown with 80+ countries
- **Regional Content**: Trending topics specific to user's region
- **Cultural Relevance**: Content suggestions tailored to regional preferences

### 🎭 Multi-Level Interest Selection
- **14 Main Genres**: Comprehensive content categories with icons
- **Entertainment Deep-Dive**: 7 subgenres with 35+ detailed sub-categories
- **Education Focus**: 6 subgenres with 25+ specialized areas
- **Simultaneous Selection**: Choose multiple items at all levels

## 🗃️ Database Configuration

- **Connection Name**: Recommender
- **Database Name**: Recommend  
- **Collection Name**: system
- **MongoDB URL**: `mongodb://localhost:27017/`

## ✨ User Journey

1. **Login/Register** → Nationality selection with dropdown
2. **Statistics Dashboard** → Interactive charts and trending analysis (skippable)
3. **Interest Selection** → Multi-level genre and subgenre selection
4. **Smart Recommendations** → Personalized content suggestions with insights

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **MongoDB** - NoSQL database with optimized indexes
- **PyMongo** - MongoDB driver with connection pooling
- **Requests** - API calls for trending data
- **Pandas/NumPy** - Data analysis and processing
- **Regional Topic Suggester** - Custom trending analysis system

### Frontend
- **React.js** - Modern UI framework
- **Chart.js + React-Chartjs-2** - Interactive data visualizations
- **Axios** - HTTP client for API communication
- **React Icons** - Comprehensive icon library
- **CSS3** - Advanced styling with animations and responsive design

## 📋 Prerequisites

1. **Python 3.7+** installed
2. **Node.js 14+** and npm installed
3. **MongoDB** running locally on `mongodb://localhost:27017/`
4. **YouTube Data API key** (optional for real trending data)

## 🚀 Quick Start

### Method 1: Complete Application
```bash
# Clone/extract the project
cd recommender-app-enhanced

# Start everything at once
./start.sh
```

### Method 2: Individual Services
```bash
# Backend
cd backend
./start.sh

# Frontend (in new terminal)
cd frontend
./start.sh
```

### Method 3: Manual Setup
```bash
# Backend setup
cd backend
pip install -r requirements.txt
python app.py

# Frontend setup (in new terminal)
cd frontend
npm install
npm start
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Enhanced API health check |
| `GET` | `/countries` | List of supported countries |
| `POST` | `/register` | User registration with nationality |
| `POST` | `/login` | User authentication |
| `GET` | `/statistics/<username>` | Regional trending statistics |
| `GET` | `/recommendations/<username>` | Smart content recommendations |
| `POST` | `/set_interests` | Save hierarchical interests |
| `GET` | `/user/<username>` | Get user information |
| `GET` | `/analytics` | Platform analytics |

## 📊 Smart Recommendations Features

### Content Analysis
- **Trending Factor**: 0-100 score based on virality potential
- **Difficulty Assessment**: Easy/Medium/Hard creation complexity
- **Monetization Potential**: Revenue generation likelihood
- **Estimated Views**: Potential reach prediction
- **Keywords**: SEO-optimized keyword suggestions

### Content Angles
- **Multiple Approaches**: 5+ different angles per topic
- **Beginner to Advanced**: Content for all skill levels
- **Trending Integration**: Current events and viral topics
- **Regional Adaptation**: Culturally relevant suggestions

## 📈 Statistics Dashboard Features

### Interactive Charts
- **Category Distribution**: Doughnut chart of trending categories
- **Keyword Analysis**: Bar chart of popular keywords
- **Real-time Data**: Updated trending information
- **Regional Focus**: Country-specific insights

### Trending Insights
- **Hot Keywords**: Most mentioned terms with frequency
- **Content Categories**: Popular types by region
- **Creator Tips**: Actionable insights for content strategy

## 🎭 Interest Selection System

### Main Categories (14)
Film & Animation, Autos & Vehicles, Music, Pets & Animals, Sports, Travel & Events, Gaming, People & Blogs, Comedy, Entertainment, News & Politics, How to & Style, Education, Science & Technology

### Entertainment Subgenres (7 categories, 35+ options)
1. **Movies & TV**: Reviews, Behind Scenes, Trailers, Interviews, Analysis
2. **Music & Performance**: Videos, Live Shows, Tutorials, Covers, Dance, Lyrics
3. **Gaming & Esports**: Walkthroughs, Streams, Reviews, Tournaments, Lore
4. **Comedy & Humor**: Sketches, Stand-up, Pranks, Memes, Parody
5. **Pop Culture & Celebrities**: Gossip, Red Carpet, Influencers, Fan Theories
6. **Lifestyle & Vlogs**: Daily Vlogs, Challenges, Family, Unboxing, BTS
7. **Fictional & Storytelling**: Films, Audio Dramas, Animation, Web Series, Podcasts

### Education Subgenres (6 categories, 32+ options)
1. **Academic Learning**: Math, Science, Programming, History, Languages, Economics
2. **Skill Development**: Communication, Leadership, Critical Thinking, EQ
3. **Career & Professional**: Resume Building, Certifications, Productivity
4. **Higher Education**: College Reviews, Research, MOOCs, EdTech
5. **Educational Entertainment**: Science Experiments, Animated Learning, Fun Facts
6. **Motivation & Self-Improvement**: Study Motivation, Habits, Mindset, Stories

## 📁 Project Structure

```
recommender-app-enhanced/
├── README.md
├── .env.example
├── .gitignore
├── start.sh                    # Complete app startup
├── backend/
│   ├── app.py                 # Enhanced Flask API
│   ├── models.py              # User models with nationality
│   ├── topic_suggester.py     # Regional trending system
│   ├── requirements.txt       # Python dependencies
│   └── start.sh              # Backend startup
└── frontend/
    ├── package.json           # React + Chart.js dependencies
    ├── start.sh              # Frontend startup
    ├── public/
    │   └── index.html        # Enhanced HTML template
    └── src/
        ├── App.js            # Main app with enhanced flow
        ├── App.css           # Comprehensive styling
        ├── index.js          # React entry point
        └── components/
            ├── Login.js              # Enhanced login
            ├── Register.js           # Nationality registration
            ├── StatisticsDashboard.js # Interactive charts
            ├── GenreSelector.js      # Multi-level selection
            └── Recommendations.js    # Smart suggestions
```

## 🌍 Supported Regions

**Major Regions**: India, United States, United Kingdom, Canada, Australia, Germany, France, Japan, South Korea, Brazil, Mexico, Singapore, UAE, Thailand, Philippines, Indonesia, Vietnam, Malaysia, Pakistan, Bangladesh

**Additional Countries**: 60+ countries with localized trending analysis

## 🔧 Configuration

### YouTube API Setup (Optional)
1. Get YouTube Data API v3 key from Google Cloud Console
2. Replace `API_KEY` in `backend/topic_suggester.py`
3. Restart backend for real trending data

### Database Customization
- MongoDB connection string in `backend/app.py`
- Database name: "Recommend"
- Collection name: "system"
- Indexes automatically created for performance

## 🎯 Advanced Features

### Regional Topic Suggester
- **Mock Data Mode**: Demo trending topics for development
- **Real API Mode**: Live YouTube trending data
- **Content Categorization**: Automatic topic classification
- **Keyword Extraction**: Smart keyword identification
- **Viral Potential Scoring**: Algorithm-based trend prediction

### User Flow Optimization
- **Smart Routing**: Based on profile completion status
- **Skip Options**: Flexible user experience
- **Progress Tracking**: User journey analytics
- **Personalization**: Interest-based customization

## 🐛 Troubleshooting

### Common Issues
1. **Charts not loading**: Ensure Chart.js dependencies installed
2. **API connection failed**: Check MongoDB status and backend logs
3. **Countries not loading**: Verify backend `/countries` endpoint
4. **No recommendations**: Check user interests and regional data

### Development Mode
```bash
# Enable debug logging
export FLASK_DEBUG=1

# Check API endpoints
curl http://localhost:5000/
curl http://localhost:5000/countries
```

## 🔜 Future Enhancements

- **Real-time Trend Tracking**: Live trending topic updates
- **Creator Analytics**: Performance tracking and insights
- **Collaboration Features**: Connect with other creators
- **Advanced Filtering**: More sophisticated recommendation filters
- **Mobile App**: React Native implementation
- **Social Integration**: Share recommendations across platforms

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your enhancement
4. Test thoroughly with all features
5. Submit a pull request

## 📞 Support

For technical support:
1. Check the troubleshooting section
2. Verify MongoDB and API configurations
3. Review console logs for detailed error messages
4. Test individual components step by step

---

**Perfect for content creators who want data-driven, regional insights for their content strategy!**
