from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError, PyMongoError
from models import (
    hash_password, verify_password, validate_username, 
    validate_password, create_user_document, COUNTRIES
)
from topic_suggester import get_regional_suggestions
import os
import logging
from datetime import datetime
import atexit

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MongoDBManager:
    """Efficient MongoDB connection and management class"""

    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.is_connected = False
        self.connect()

    def connect(self):
        """Establish MongoDB connection with proper configuration"""
        try:
            connection_string = "mongodb://localhost:27017/"

            self.client = MongoClient(
                connection_string,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=20000,
                maxPoolSize=50,
                minPoolSize=5,
                maxIdleTimeMS=30000,
                retryWrites=True,
                retryReads=True,
                w='majority',
                journal=True
            )

            self.client.admin.command('ping')
            self.db = self.client["Recommend"]
            self.collection = self.db["system"]
            self._create_indexes()
            self.is_connected = True
            logger.info("✅ Successfully connected to MongoDB!")
            logger.info(f"📊 Database: {self.db.name}")
            logger.info(f"📋 Collection: {self.collection.name}")

        except ConnectionFailure as e:
            self.is_connected = False
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            self.is_connected = False
            logger.error(f"❌ Unexpected error during MongoDB connection: {e}")
            raise

    def _create_indexes(self):
        """Create database indexes for optimal performance"""
        try:
            self.collection.create_index("username", unique=True)
            self.collection.create_index([("username", 1), ("is_active", 1)])
            self.collection.create_index("nationality")
            self.collection.create_index("created_at")
            self.collection.create_index("last_login")
            logger.info("📈 Database indexes created successfully")
        except Exception as e:
            logger.warning(f"⚠️ Could not create indexes: {e}")

    def check_connection(self):
        """Check if MongoDB connection is still alive"""
        try:
            self.client.admin.command('ping')
            return True
        except:
            self.is_connected = False
            return False

    def reconnect(self):
        """Reconnect to MongoDB if connection is lost"""
        if not self.check_connection():
            logger.info("🔄 Reconnecting to MongoDB...")
            try:
                self.connect()
                return True
            except Exception as e:
                logger.error(f"❌ Reconnection failed: {e}")
                return False
        return True

    def get_collection(self):
        """Get the collection with automatic reconnection"""
        if not self.reconnect():
            raise Exception("Database connection is not available")
        return self.collection

    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            self.is_connected = False
            logger.info("🔌 MongoDB connection closed")

# Initialize MongoDB manager
db_manager = MongoDBManager()

@app.route("/", methods=["GET"])
def home():
    """API health check and database status"""
    try:
        collection = db_manager.get_collection()
        user_count = collection.count_documents({"is_active": True})
        interests_count = collection.count_documents({
            "is_active": True, 
            "interests": {"$exists": True, "$ne": {}}
        })

        return jsonify({
            "message": "Enhanced Content Recommender API is running!",
            "database_config": {
                "database": "Recommend",
                "collection": "system",
                "connection": "Recommender"
            },
            "stats": {
                "total_active_users": user_count,
                "users_with_interests": interests_count
            },
            "features": [
                "Regional trending analysis",
                "Smart content recommendations",
                "Multi-level interest selection",
                "Interactive statistics dashboard"
            ],
            "status": "connected",
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "message": "API is running but database connection failed",
            "error": str(e),
            "status": "disconnected",
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route("/countries", methods=["GET"])
def get_countries():
    """Get list of supported countries for nationality selection"""
    return jsonify({
        "success": True,
        "countries": COUNTRIES
    })

@app.route("/register", methods=["POST"])
def register():
    """Enhanced user registration with nationality"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided."}), 400

        username = data.get("username", "").strip()
        password = data.get("password", "")
        confirm_password = data.get("confirm_password", "")
        channel_name = data.get("channel_name", "").strip()
        channel_api = data.get("channel_api", "").strip()
        nationality = data.get("nationality", "").strip()

        # Validation
        username_valid, username_msg = validate_username(username)
        if not username_valid:
            return jsonify({"success": False, "message": username_msg}), 400

        password_valid, password_msg = validate_password(password)
        if not password_valid:
            return jsonify({"success": False, "message": password_msg}), 400

        if password != confirm_password:
            return jsonify({"success": False, "message": "Passwords do not match."}), 400

        if not nationality:
            return jsonify({"success": False, "message": "Please select your nationality."}), 400

        if nationality not in COUNTRIES:
            return jsonify({"success": False, "message": "Invalid nationality selection."}), 400

        collection = db_manager.get_collection()

        if collection.find_one({"username": username}):
            return jsonify({"success": False, "message": "This username is already taken."}), 409

        user_document = create_user_document(username, password, channel_name, channel_api, nationality)
        result = collection.insert_one(user_document)

        if result.inserted_id:
            logger.info(f"👤 New user registered: {username} from {nationality}")
            return jsonify({
                "success": True, 
                "message": "User registered successfully!",
                "user_id": str(result.inserted_id),
                "show_statistics": True  # Flag to show statistics page
            })
        else:
            return jsonify({"success": False, "message": "Failed to create user."}), 500

    except DuplicateKeyError:
        return jsonify({"success": False, "message": "This username is already taken."}), 409
    except PyMongoError as e:
        logger.error(f"Database error during registration: {e}")
        return jsonify({"success": False, "message": "Database error occurred. Please try again."}), 500
    except Exception as e:
        logger.error(f"Unexpected error during registration: {e}")
        return jsonify({"success": False, "message": "Registration failed. Please try again."}), 500

@app.route("/login", methods=["POST"])
def login():
    """Enhanced user authentication"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided."}), 400

        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            return jsonify({"success": False, "message": "Username and password are required."}), 400

        collection = db_manager.get_collection()
        user = collection.find_one({"username": username, "is_active": True})

        if user and verify_password(user["password"], password):
            update_data = {
                "last_login": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }

            collection.update_one({"_id": user["_id"]}, {"$set": update_data})

            logger.info(f"🔐 User logged in: {username}")
            return jsonify({
                "success": True, 
                "message": "Login successful!",
                "user": {
                    "username": user["username"],
                    "nationality": user.get("nationality", ""),
                    "channel_name": user.get("channel_name", ""),
                    "interests": user.get("interests", {}),
                    "profile_completed": user.get("profile_completed", False),
                    "viewed_statistics": user.get("viewed_statistics", False),
                    "created_at": user.get("created_at", "").isoformat() if user.get("created_at") else ""
                }
            })
        else:
            logger.warning(f"🚫 Failed login attempt for username: {username}")
            return jsonify({"success": False, "message": "Username and password didn't match."}), 401

    except PyMongoError as e:
        logger.error(f"Database error during login: {e}")
        return jsonify({"success": False, "message": "Database error occurred. Please try again."}), 500
    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        return jsonify({"success": False, "message": "Login failed. Please try again."}), 500

@app.route("/statistics/<username>", methods=["GET"])
def get_statistics(username):
    """Get trending statistics for user's region"""
    try:
        collection = db_manager.get_collection()
        user = collection.find_one({"username": username, "is_active": True})

        if not user:
            return jsonify({"success": False, "message": "User not found."}), 404

        nationality = user.get("nationality", "United States")

        # Get regional suggestions and statistics
        regional_data = get_regional_suggestions(nationality)

        # Mark that user has viewed statistics
        collection.update_one(
            {"username": username},
            {"$set": {"viewed_statistics": True, "updated_at": datetime.utcnow()}}
        )

        return jsonify({
            "success": True,
            "statistics": regional_data['statistics'],
            "trending_keywords": regional_data['trending_keywords'][:10],
            "region": nationality
        })

    except Exception as e:
        logger.error(f"Error fetching statistics: {e}")
        return jsonify({"success": False, "message": "Failed to fetch statistics."}), 500

@app.route("/recommendations/<username>", methods=["GET"])
def get_recommendations(username):
    """Get personalized content recommendations"""
    try:
        collection = db_manager.get_collection()
        user = collection.find_one({"username": username, "is_active": True})

        if not user:
            return jsonify({"success": False, "message": "User not found."}), 404

        nationality = user.get("nationality", "United States")
        user_interests = user.get("interests", {})

        # Get regional suggestions
        regional_data = get_regional_suggestions(nationality, user_interests)

        return jsonify({
            "success": True,
            "recommendations": regional_data['suggestions'],
            "region": nationality,
            "total_suggestions": len(regional_data['suggestions'])
        })

    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        return jsonify({"success": False, "message": "Failed to generate recommendations."}), 500

@app.route("/set_interests", methods=["POST"])
def set_interests():
    """Update user interests with hierarchical structure"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided."}), 400

        username = data.get("username", "").strip()
        interests = data.get("interests", {})

        if not username:
            return jsonify({"success": False, "message": "Username is required."}), 400

        if not isinstance(interests, dict):
            return jsonify({"success": False, "message": "Interests must be a valid structure."}), 400

        collection = db_manager.get_collection()

        update_data = {
            "interests": interests,
            "updated_at": datetime.utcnow(),
            "profile_completed": True
        }

        result = collection.update_one(
            {"username": username, "is_active": True}, 
            {"$set": update_data}
        )

        if result.matched_count == 0:
            return jsonify({"success": False, "message": "User not found."}), 404

        if result.modified_count > 0:
            logger.info(f"📋 Interests updated for user: {username}")
            return jsonify({"success": True, "message": "Interests updated successfully!"})
        else:
            return jsonify({"success": True, "message": "No changes made to interests."})

    except PyMongoError as e:
        logger.error(f"Database error during interest update: {e}")
        return jsonify({"success": False, "message": "Database error occurred. Please try again."}), 500
    except Exception as e:
        logger.error(f"Unexpected error during interest update: {e}")
        return jsonify({"success": False, "message": "Failed to update interests. Please try again."}), 500

@app.route("/user/<username>", methods=["GET"])
def get_user(username):
    """Get user information (excluding sensitive data)"""
    try:
        if not username.strip():
            return jsonify({"success": False, "message": "Username is required."}), 400

        collection = db_manager.get_collection()
        user = collection.find_one(
            {"username": username.strip(), "is_active": True}, 
            {
                "password": 0,
                "channel_api": 0
            }
        )

        if user:
            user["_id"] = str(user["_id"])

            for date_field in ["created_at", "updated_at", "last_login"]:
                if user.get(date_field):
                    user[date_field] = user[date_field].isoformat()

            return jsonify({"success": True, "user": user})
        else:
            return jsonify({"success": False, "message": "User not found."}), 404

    except PyMongoError as e:
        logger.error(f"Database error during user fetch: {e}")
        return jsonify({"success": False, "message": "Database error occurred."}), 500
    except Exception as e:
        logger.error(f"Unexpected error during user fetch: {e}")
        return jsonify({"success": False, "message": "Failed to get user information."}), 500

@app.route("/analytics", methods=["GET"])
def get_analytics():
    """Get platform analytics"""
    try:
        collection = db_manager.get_collection()

        # User statistics
        total_users = collection.count_documents({"is_active": True})
        completed_profiles = collection.count_documents({
            "is_active": True, 
            "profile_completed": True
        })

        # Nationality distribution
        nationality_pipeline = [
            {"$match": {"is_active": True, "nationality": {"$exists": True, "$ne": ""}}},
            {"$group": {"_id": "$nationality", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        nationality_stats = list(collection.aggregate(nationality_pipeline))

        return jsonify({
            "success": True,
            "analytics": {
                "total_users": total_users,
                "completed_profiles": completed_profiles,
                "completion_rate": round((completed_profiles / total_users * 100), 2) if total_users > 0 else 0,
                "nationality_distribution": nationality_stats
            }
        })

    except Exception as e:
        logger.error(f"Error fetching analytics: {e}")
        return jsonify({"success": False, "message": "Failed to fetch analytics."}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "message": "Endpoint not found",
        "available_endpoints": ["/", "/countries", "/register", "/login", "/statistics/<username>", 
                               "/recommendations/<username>", "/set_interests", "/user/<username>", "/analytics"]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"success": False, "message": "Internal server error"}), 500

def cleanup():
    """Cleanup function for graceful shutdown"""
    logger.info("🔄 Shutting down server...")
    db_manager.close_connection()

atexit.register(cleanup)

if __name__ == "__main__":
    print("🚀 Starting Enhanced Content Recommender Backend...")
    print("=" * 70)
    print("📊 Database Configuration:")
    print(f"   Database Name: Recommend")
    print(f"   Collection Name: system")
    print(f"   Connection: Recommender")
    print(f"   MongoDB URL: mongodb://localhost:27017/")
    print("=" * 70)
    print("🌟 Enhanced Features:")
    print("   ✨ Regional trending analysis")
    print("   📈 Interactive statistics dashboard")
    print("   🎯 Smart content recommendations")
    print("   🌍 Nationality-based personalization")
    print("   📊 Real-time analytics")
    print("=" * 70)
    print("🌐 API Configuration:")
    print(f"   API URL: http://localhost:5000")
    print("=" * 70)

    try:
        app.run(debug=True, port=5000, host='0.0.0.0')
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        cleanup()
