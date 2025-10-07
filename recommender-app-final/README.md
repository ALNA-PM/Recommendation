# Content Recommender App - Multi-Level Interest Selection

A sophisticated full-stack web application built with Flask (backend) and React (frontend) that enables users to register, login, and select their content creation interests through a comprehensive multi-level selection system.

## 🎯 New Features

### Multi-Level Interest Selection
- **Main Genres**: 14 content categories with icons
- **Entertainment Subgenres**: 7 specialized entertainment categories
- **Education Subgenres**: 6 focused education categories  
- **Sub-Sub-Genres**: Detailed subcategories for Entertainment and Education
- **Multiple Selections**: Choose multiple items at every level

### Entertainment Categories
🎭 **Entertainment Detailed Subgenres**
1. **Movies & TV** - Reviews, Behind the Scenes, Trailers, Interviews, Analysis
2. **Music & Performance** - Music Videos, Live Shows, Tutorials, Covers, Dance
3. **Gaming & Esports** - Walkthroughs, Streams, Reviews, Tournaments, Lore
4. **Comedy & Humor** - Sketches, Stand-up, Pranks, Memes, Parody
5. **Pop Culture & Celebrities** - Gossip, Red Carpet, Influencers, Fan Theories
6. **Lifestyle & Vlogs** - Daily Vlogs, Challenges, Family Content, Unboxing
7. **Fictional & Storytelling** - Short Films, Audio Dramas, Animation, Web Series

### Education Categories  
🎓 **Education Detailed Subgenres**
1. **Academic Learning** - Math, Science, Programming, History, Languages
2. **Skill Development** - Communication, Leadership, Critical Thinking
3. **Career & Professional Growth** - Resume Building, Certifications, Productivity
4. **Higher Education & Research** - College Reviews, Research Tutorials, MOOCs
5. **Educational Entertainment** - Science Experiments, Animated Learning, Fun Facts
6. **Motivation & Self-Improvement** - Study Motivation, Habit Building, Mindset

## 🗃️ Database Configuration

- **Connection Name**: Recommender
- **Database Name**: Recommend  
- **Collection Name**: system
- **MongoDB URL**: `mongodb://localhost:27017/`

## ✨ Key Features

- **Clean User Interface**: No technical database messages in UI
- **Hierarchical Selection**: Genre → Subgenre → Sub-Sub-Genre
- **Multiple Selections**: Select multiple items at any level
- **Always Visible Options**: All subgenres displayed simultaneously
- **Welcome Page**: Simple greeting after interest selection
- **Efficient MongoDB**: Optimized connection management
- **Responsive Design**: Works on all devices

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **MongoDB** - NoSQL database with optimized performance
- **PyMongo** - MongoDB driver with connection pooling
- **Werkzeug** - Secure password hashing
- **Flask-CORS** - Cross-origin request handling

### Frontend
- **React.js** - Modern UI library
- **Axios** - HTTP client for API calls
- **React Icons** - Beautiful icon components
- **CSS3** - Advanced styling with animations

## 📋 Prerequisites

1. **Python 3.7+** installed
2. **Node.js 14+** and npm installed
3. **MongoDB** running locally on `mongodb://localhost:27017/`
4. **MongoDB Compass** (recommended for database visualization)

## 🚀 Quick Start

### Method 1: Individual Services

**Backend:**
```bash
cd backend
./start.sh
```

**Frontend:**
```bash
cd frontend  
./start.sh
```

### Method 2: Complete App
```bash
./start.sh
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API health check |
| `POST` | `/register` | User registration |
| `POST` | `/login` | User authentication |
| `POST` | `/set_interests` | Save hierarchical interests |
| `GET` | `/user/<username>` | Get user information |

## 📊 Interest Data Structure

```javascript
{
  "interests": {
    "genres": ["Entertainment", "Education"],
    "entertainment": {
      "selected": ["Movies & TV", "Gaming & Esports"],
      "subSelected": {
        "Movies & TV": ["Movie Reviews & Reactions", "Behind the Scenes"],
        "Gaming & Esports": ["Gameplay Walkthroughs", "Live Streams"]
      }
    },
    "education": {
      "selected": ["Academic Learning"],
      "subSelected": {
        "Academic Learning": ["Computer Science & Programming", "Mathematics"]
      }
    }
  }
}
```

## 🎨 User Experience Flow

1. **Registration** → Create account with username/password
2. **Login** → Authenticate and access the app  
3. **Genre Selection** → Choose from 14 main content genres
4. **Subgenre Selection** → Select Entertainment/Education subcategories
5. **Sub-Sub-Genre Selection** → Pick specific focus areas
6. **Welcome Page** → Simple greeting with username

## 📁 Project Structure

```
recommender-app-final/
├── README.md
├── .gitignore
├── .env.example
├── start.sh                    # Complete app startup
├── backend/
│   ├── app.py                 # Flask API with MongoDB
│   ├── models.py              # User models & validation
│   ├── requirements.txt       # Python dependencies
│   └── start.sh              # Backend startup
└── frontend/
    ├── package.json           # React dependencies
    ├── start.sh              # Frontend startup
    ├── public/
    │   └── index.html        # HTML template
    └── src/
        ├── App.js            # Main React component
        ├── App.css           # Enhanced styling
        ├── index.js          # React entry point
        └── components/
            ├── Login.js              # Clean login form
            ├── Register.js           # Registration form
            ├── GenreSelector.js      # Multi-level selection
            └── WelcomePage.js        # Simple welcome page
```

## 🔧 MongoDB Features

- **Connection Pooling**: Optimized performance
- **Auto-reconnection**: Handles connection drops
- **Efficient Indexing**: Fast database queries
- **Error Handling**: Comprehensive error management
- **Hierarchical Storage**: Supports complex interest structures

## 🎯 Selection Features

- **Multiple Genres**: Select multiple main content categories
- **Entertainment Focus**: 7 subgenres with 35+ sub-sub-genres
- **Education Focus**: 6 subgenres with 25+ sub-sub-genres
- **Always Visible**: All options displayed simultaneously
- **Selection Counter**: Real-time count of total selections
- **Hierarchical Storage**: Maintains parent-child relationships

## 🐛 Troubleshooting

### Database Connection
```bash
# Check MongoDB status
sudo systemctl status mongod

# Start MongoDB
sudo systemctl start mongod

# View MongoDB logs
sudo journalctl -u mongod
```

### Common Issues
1. **Port 27017 in use**: Check if MongoDB is running
2. **Permission errors**: Ensure proper file permissions
3. **Node modules**: Run `npm install` if dependencies missing

## 🔜 Future Enhancements

- AI-powered content recommendations based on selections
- Trending topics within chosen categories
- Creator collaboration based on shared interests
- Content planning tools for selected niches
- Analytics dashboard for content performance

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch  
3. Implement your changes
4. Test thoroughly
5. Submit a pull request

Perfect for content creators who want granular control over their interest categories!
