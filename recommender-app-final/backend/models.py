from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime

def hash_password(password):
    """Hash a password for storing."""
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

def verify_password(hash, password):
    """Verify a stored password hash against provided password."""
    return check_password_hash(hash, password)

def validate_username(username):
    """Validate username format"""
    if not username or len(username.strip()) < 3:
        return False, "Username must be at least 3 characters long."

    if len(username.strip()) > 50:
        return False, "Username must be less than 50 characters."

    # Allow alphanumeric, underscore, and hyphen
    if not re.match("^[a-zA-Z0-9_-]+$", username.strip()):
        return False, "Username can only contain letters, numbers, underscores, and hyphens."

    return True, "Valid username"

def validate_password(password):
    """Validate password strength"""
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."

    if len(password) > 128:
        return False, "Password must be less than 128 characters."

    return True, "Valid password"

def create_user_document(username, password, channel_name="", channel_api=""):
    """Create a standardized user document"""
    return {
        "username": username.strip(),
        "channel_name": channel_name.strip(),
        "channel_api": channel_api.strip(),
        "password": hash_password(password),
        "interests": {},  # Updated to store hierarchical interests
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "last_login": None,
        "is_active": True,
        "profile_completed": False
    }
