from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import logging
import random

# NO MONGODB IMPORTS - PURE IN-MEMORY SOLUTION

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# IN-MEMORY USER STORAGE - READY TO USE
IN_MEMORY_USERS = {
    'testuser1': {
        'username': 'testuser1',
        'password': 'password123',
        'nationality': 'India',
        'interests': ['🎬 Entertainment', '💻 Technology', '⚽ Sports'],
        'created_at': datetime.now(),
        'profile_completed': True
    },
    'creator_usa': {
        'username': 'creator_usa',
        'password': 'test123',
        'nationality': 'United States',
        'interests': ['🎮 Gaming', '💻 Technology', '🎵 Music'],
        'created_at': datetime.now(),
        'profile_completed': True
    },
    'content_uk': {
        'username': 'content_uk',
        'password': 'demo123',
        'nationality': 'United Kingdom',
        'interests': ['📚 Education', '💼 Business', '🏥 Health'],
        'created_at': datetime.now(),
        'profile_completed': True
    },
    'demo_canada': {
        'username': 'demo_canada',
        'password': 'canada123',
        'nationality': 'Canada',
        'interests': ['✈️ Travel', '🍳 Food & Cooking', '🏋️ Fitness'],
        'created_at': datetime.now(),
        'profile_completed': True
    }
}

# Countries list for frontend dropdown
COUNTRIES = [
    'India', 'United States', 'United Kingdom', 'Canada', 'Australia',
    'Germany', 'France', 'Japan', 'South Korea', 'Brazil', 'Mexico',
    'Singapore', 'UAE', 'Thailand', 'Philippines', 'Indonesia', 'Vietnam',
    'Malaysia', 'Pakistan', 'Bangladesh', 'Sri Lanka', 'Nepal', 'Myanmar',
    'Taiwan', 'Hong Kong', 'China', 'Russia', 'Ukraine', 'Poland', 'Spain',
    'Italy', 'Netherlands', 'Belgium', 'Sweden', 'Norway', 'Denmark',
    'Finland', 'Switzerland', 'Austria', 'Czech Republic', 'Hungary',
    'Romania', 'Bulgaria', 'Greece', 'Turkey', 'Israel', 'Saudi Arabia',
    'Egypt', 'Nigeria', 'South Africa', 'Kenya', 'Ghana', 'Morocco',
    'Tunisia', 'Algeria', 'Ethiopia', 'Uganda', 'Tanzania', 'Zambia',
    'Zimbabwe', 'Botswana', 'Namibia', 'Mozambique', 'Madagascar',
    'Argentina', 'Chile', 'Peru', 'Colombia', 'Venezuela', 'Ecuador',
    'Bolivia', 'Paraguay', 'Uruguay', 'Costa Rica', 'Panama', 'Guatemala',
    'Honduras', 'El Salvador', 'Nicaragua', 'Dominican Republic', 'Cuba',
    'Jamaica', 'Trinidad and Tobago', 'Barbados', 'New Zealand', 'Fiji'
]

# Simple AI prediction engine (no external dependencies)
def generate_predictions(region, categories, count=3):
    """Generate AI predictions without external dependencies"""
    predictions = []

    trending_topics = {
        'Entertainment': ['Movie Reviews', 'Celebrity News', 'Music Trends', 'Gaming Updates', 'TV Show Analysis'],
        'Technology': ['AI Revolution', 'Blockchain Future', 'Web3 Development', 'Machine Learning', 'Cybersecurity'],
        'Sports': ['Cricket Updates', 'Football News', 'Olympics', 'Tennis', 'Basketball'],
        'Education': ['Study Tips', 'Online Courses', 'Career Guidance', 'Skill Development', 'Research'],
        'Gaming': ['Game Reviews', 'Gaming Tips', 'Esports News', 'Game Development', 'Hardware'],
        'Health': ['Fitness Tips', 'Nutrition Guide', 'Mental Health', 'Yoga Practices', 'Medical Updates'],
        'Business': ['Startup Ideas', 'Investment Tips', 'Marketing', 'Entrepreneurship', 'Business News'],
        'Travel': ['Travel Guides', 'Budget Travel', 'Adventure Tourism', 'Cultural Exploration', 'Tips'],
        'Food': ['Cooking Recipes', 'Food Reviews', 'Healthy Eating', 'Regional Cuisine', 'Restaurants'],
        'Fashion': ['Fashion Trends', 'Style Tips', 'Brand Reviews', 'Sustainable Fashion', 'Celebrity Fashion']
    }

    for category in categories[:3]:
        clean_category = category.replace('🎬 ', '').replace('💻 ', '').replace('⚽ ', '').replace('🎮 ', '').replace('📚 ', '').replace('🏥 ', '').replace('💼 ', '').replace('✈️ ', '').replace('🍳 ', '').replace('👗 ', '')

        topics = trending_topics.get(clean_category, ['General Content'])

        for i in range(count):
            if i < len(topics):
                topic = topics[i]
            else:
                topic = f"{clean_category} trends"

            viral_score = random.randint(60, 90)
            content_strength = random.randint(65, 95)
            popularity_score = random.randint(55, 85)

            prediction = {
                'title': f"Ultimate Guide to {topic} - {region} Edition",
                'category': category,
                'trend': f"{topic} trending in {region}",
                'region': region,
                'viral_score': viral_score,
                'content_strength': content_strength,
                'popularity_score': popularity_score,
                'competition_level': random.choice(['Low', 'Medium', 'High']),
                'engagement_potential': random.randint(60, 95),
                'estimated_views': random.randint(10000, 100000),
                'difficulty_level': random.choice(['Easy', 'Moderate', 'Challenging']),
                'best_time_to_post': random.choice(['6-8 AM', '12-2 PM', '6-8 PM', '8-10 PM']),
                'target_audience': f"{clean_category} enthusiasts in {region}, age 18-35",
                'content_length': random.choice(['Short (1-3 min)', 'Medium (3-8 min)', 'Long (8-15 min)']),
                'monetization_potential': random.choice(['High', 'Medium', 'Low'])
            }
            predictions.append(prediction)

    return predictions

@app.route('/')
def home():
    """API health check"""
    return jsonify({
        'status': 'success',
        'message': '🚀 Content Recommender API - Working!',
        'storage': 'In-Memory (No Database Required)',
        'features': [
            '📊 Interactive Statistics Dashboard',
            '🎯 Smart Content Recommendations', 
            '🌍 Regional Trending Analysis',
            '🤖 AI-Powered Predictions',
            '🎭 Multi-Level Interest Selection'
        ],
        'version': '2.0.0',
        'test_users': list(IN_MEMORY_USERS.keys())
    })

@app.route('/countries', methods=['GET'])
def get_countries():
    """Get list of supported countries"""
    return jsonify({
        'status': 'success',
        'countries': COUNTRIES,
        'total': len(COUNTRIES)
    })

@app.route('/register', methods=['POST'])
def register():
    """User registration"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        nationality = data.get('nationality', 'India')

        if not username or not password:
            return jsonify({'status': 'error', 'message': 'Username and password required'}), 400

        if username in IN_MEMORY_USERS:
            return jsonify({'status': 'error', 'message': 'Username already exists'}), 400

        IN_MEMORY_USERS[username] = {
            'username': username,
            'password': password,
            'nationality': nationality,
            'interests': [],
            'created_at': datetime.now(),
            'profile_completed': False
        }

        logger.info(f"✅ User registered: {username} from {nationality}")

        return jsonify({
            'status': 'success',
            'message': 'Registration successful',
            'username': username,
            'nationality': nationality
        })

    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'status': 'error', 'message': 'Registration failed'}), 500

@app.route('/login', methods=['POST'])
def login():
    """User authentication"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'status': 'error', 'message': 'Username and password required'}), 400

        user = IN_MEMORY_USERS.get(username)
        if not user or user.get('password') != password:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

        logger.info(f"✅ User logged in: {username}")

        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'username': username,
            'nationality': user.get('nationality', 'India'),
            'profile_completed': user.get('profile_completed', False),
            'interests': user.get('interests', [])
        })

    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'status': 'error', 'message': 'Login failed'}), 500

@app.route('/statistics/<username>', methods=['GET'])
def get_statistics(username):
    """Get regional trending statistics"""
    try:
        user = IN_MEMORY_USERS.get(username)
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

        nationality = user.get('nationality', 'India')

        mock_statistics = {
            'region': nationality,
            'trending_categories': {
                'Entertainment': 35,
                'Technology': 25,
                'Sports': 20,
                'Gaming': 10,
                'Education': 10
            },
            'trending_keywords': [
                {'keyword': 'AI Revolution', 'frequency': 45},
                {'keyword': 'Cricket World Cup', 'frequency': 38},
                {'keyword': 'Bollywood News', 'frequency': 32},
                {'keyword': 'Tech Innovation', 'frequency': 28},
                {'keyword': 'Gaming Tips', 'frequency': 25},
                {'keyword': 'Music Trends', 'frequency': 22},
                {'keyword': 'Food Recipes', 'frequency': 20},
                {'keyword': 'Travel Guide', 'frequency': 18}
            ],
            'total_trending_topics': 156,
            'last_updated': datetime.now().isoformat()
        }

        logger.info(f"📊 Statistics generated for {username} ({nationality})")

        return jsonify({
            'status': 'success',
            'statistics': mock_statistics
        })

    except Exception as e:
        logger.error(f"Statistics error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to fetch statistics'}), 500

@app.route('/set_interests', methods=['POST'])
def set_interests():
    """Save user interests"""
    try:
        data = request.get_json()
        username = data.get('username')
        interests = data.get('interests', [])

        if not username:
            return jsonify({'status': 'error', 'message': 'Username required'}), 400

        user = IN_MEMORY_USERS.get(username)
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

        user['interests'] = interests
        user['profile_completed'] = True
        user['interests_updated_at'] = datetime.now()

        logger.info(f"🎯 Interests updated for {username}: {len(interests)} categories")

        return jsonify({
            'status': 'success',
            'message': 'Interests saved successfully',
            'interests_count': len(interests)
        })

    except Exception as e:
        logger.error(f"Set interests error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to save interests'}), 500

@app.route('/recommendations/<username>', methods=['GET'])
def get_recommendations(username):
    """Get smart content recommendations"""
    try:
        user = IN_MEMORY_USERS.get(username)
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

        nationality = user.get('nationality', 'India')
        interests = user.get('interests', [])

        if not interests:
            return jsonify({'status': 'error', 'message': 'No interests found. Please complete profile.'}), 400

        mock_recommendations = []
        for i, interest in enumerate(interests[:5]):
            mock_recommendations.append({
                'title': f"Latest {interest} Trends You Should Know",
                'category': interest,
                'trend': f"{interest} in {nationality}",
                'viral_score': 75 + (i * 5),
                'content_strength': 80 - (i * 2),
                'popularity_score': 70 + (i * 3),
                'difficulty_level': ['Easy', 'Medium', 'Hard'][i % 3],
                'estimated_views': f"{(50 + i * 10)}K",
                'monetization_potential': ['High', 'Medium', 'High'][i % 3],
                'best_time_to_post': '7-9 PM IST',
                'target_audience': f"{interest} enthusiasts, 18-35 years",
                'content_angles': [
                    f"Complete beginner's guide to {interest}",
                    f"Advanced {interest} techniques revealed",
                    f"Common {interest} mistakes to avoid"
                ]
            })

        logger.info(f"📋 Recommendations generated for {username}: {len(mock_recommendations)} items")

        return jsonify({
            'status': 'success',
            'recommendations': mock_recommendations,
            'user_profile': {
                'username': username,
                'nationality': nationality,
                'interests_count': len(interests)
            }
        })

    except Exception as e:
        logger.error(f"Recommendations error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to fetch recommendations'}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """AI-powered content predictions"""
    try:
        data = request.get_json()
        username = data.get('username')
        region = data.get('region', 'India')
        categories = data.get('categories', [])

        if not username or not categories:
            return jsonify({
                'status': 'error', 
                'message': 'Username and categories required'
            }), 400

        user = IN_MEMORY_USERS.get(username)
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

        logger.info(f"🤖 Generating AI predictions for {username}: {categories}")

        predictions = generate_predictions(region, categories, count=3)

        formatted_predictions = []
        for prediction in predictions:
            formatted_predictions.append({
                'title': prediction['title'],
                'category': prediction['category'],
                'trend': prediction['trend'],
                'region': prediction['region'],
                'viral_score': prediction['viral_score'],
                'content_strength': prediction['content_strength'],
                'popularity_score': prediction['popularity_score'],
                'competition_level': prediction['competition_level'],
                'engagement_potential': prediction['engagement_potential'],
                'estimated_views': prediction['estimated_views'],
                'difficulty_level': prediction['difficulty_level'],
                'best_time_to_post': prediction['best_time_to_post'],
                'target_audience': prediction['target_audience'],
                'content_length': prediction['content_length'],
                'monetization_potential': prediction['monetization_potential'],
                'confidence_score': (prediction['viral_score'] + prediction['content_strength']) / 2,
                'description': f"AI-powered content suggestion based on {prediction['trend']}"
            })

        logger.info(f"✅ AI predictions generated: {len(formatted_predictions)} items")

        return jsonify({
            'status': 'success',
            'predictions': formatted_predictions,
            'metadata': {
                'username': username,
                'region': region,
                'categories': categories,
                'prediction_count': len(formatted_predictions),
                'generated_at': datetime.now().isoformat()
            }
        })

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({
            'status': 'error', 
            'message': f'Prediction failed: {str(e)}'
        }), 500

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    """Get user information"""
    try:
        user = IN_MEMORY_USERS.get(username)
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

        user_data = {
            'username': user['username'],
            'nationality': user.get('nationality', 'India'),
            'interests': user.get('interests', []),
            'profile_completed': user.get('profile_completed', False),
            'created_at': user.get('created_at').isoformat() if user.get('created_at') else None
        }

        return jsonify({
            'status': 'success',
            'user': user_data
        })

    except Exception as e:
        logger.error(f"Get user error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to fetch user'}), 500

@app.route('/analytics', methods=['GET'])
def get_analytics():
    """Get platform analytics"""
    try:
        total_users = len(IN_MEMORY_USERS)
        completed_profiles = sum(1 for u in IN_MEMORY_USERS.values() if u.get('profile_completed', False))

        nationality_counts = {}
        for user in IN_MEMORY_USERS.values():
            nationality = user.get('nationality', 'Unknown')
            nationality_counts[nationality] = nationality_counts.get(nationality, 0) + 1

        nationality_stats = [{'_id': k, 'count': v} for k, v in sorted(nationality_counts.items(), key=lambda x: x[1], reverse=True)]

        analytics_data = {
            'total_users': total_users,
            'completed_profiles': completed_profiles,
            'completion_rate': (completed_profiles / total_users * 100) if total_users > 0 else 0,
            'nationality_distribution': nationality_stats,
            'last_updated': datetime.now().isoformat()
        }

        return jsonify({
            'status': 'success',
            'analytics': analytics_data
        })

    except Exception as e:
        logger.error(f"Analytics error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to fetch analytics'}), 500

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'production') == 'development'

    logger.info(f"🚀 Starting Content Recommender Backend on port {port}")
    logger.info("💾 Storage: In-Memory (No Database Required)")
    logger.info(f"👥 Pre-loaded test users: {list(IN_MEMORY_USERS.keys())}")
    logger.info("🌟 Features: AI Predictions + Smart Recommendations + Statistics")

    app.run(host='0.0.0.0', port=port, debug=debug)
