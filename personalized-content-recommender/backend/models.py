from pymongo import MongoClient
from datetime import datetime
import os

class UserModel:
    """User model for MongoDB operations"""

    def __init__(self, db_connection):
        self.collection = db_connection

    def create_user(self, username, password, nationality='India'):
        """Create a new user"""
        user_data = {
            'username': username,
            'password': password,  # In production, hash this
            'nationality': nationality,
            'interests': [],
            'created_at': datetime.now(),
            'profile_completed': False,
            'last_login': None,
            'recommendation_history': [],
            'prediction_history': []
        }

        try:
            result = self.collection.insert_one(user_data)
            return result.inserted_id
        except Exception as e:
            raise Exception(f"Failed to create user: {e}")

    def find_user(self, username):
        """Find user by username"""
        return self.collection.find_one({'username': username})

    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        return self.collection.find_one({'username': username, 'password': password})

    def update_interests(self, username, interests):
        """Update user interests"""
        return self.collection.update_one(
            {'username': username},
            {
                '$set': {
                    'interests': interests,
                    'profile_completed': True,
                    'interests_updated_at': datetime.now()
                }
            }
        )

    def update_last_login(self, username):
        """Update user's last login timestamp"""
        return self.collection.update_one(
            {'username': username},
            {'$set': {'last_login': datetime.now()}}
        )

    def add_recommendation_history(self, username, recommendations):
        """Add recommendation to user history"""
        return self.collection.update_one(
            {'username': username},
            {
                '$push': {
                    'recommendation_history': {
                        'recommendations': recommendations,
                        'timestamp': datetime.now()
                    }
                }
            }
        )

    def add_prediction_history(self, username, predictions):
        """Add prediction to user history"""
        return self.collection.update_one(
            {'username': username},
            {
                '$push': {
                    'prediction_history': {
                        'predictions': predictions,
                        'timestamp': datetime.now()
                    }
                }
            }
        )