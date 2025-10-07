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

def create_user_document(username, password, channel_name="", channel_api="", nationality=""):
    """Create a standardized user document"""
    return {
        "username": username.strip(),
        "channel_name": channel_name.strip(),
        "channel_api": channel_api.strip(),
        "nationality": nationality.strip(),
        "password": hash_password(password),
        "interests": {},
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "last_login": None,
        "is_active": True,
        "profile_completed": False,
        "viewed_statistics": False
    }

# Country list for nationality dropdown
COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan",
    "Bahrain", "Bangladesh", "Belarus", "Belgium", "Bolivia", "Bosnia and Herzegovina", "Brazil", "Bulgaria",
    "Cambodia", "Canada", "Chile", "China", "Colombia", "Croatia", "Czech Republic", "Denmark",
    "Ecuador", "Egypt", "Estonia", "Finland", "France", "Georgia", "Germany", "Ghana", "Greece",
    "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy",
    "Japan", "Jordan", "Kazakhstan", "Kenya", "Kuwait", "Latvia", "Lebanon", "Lithuania", "Luxembourg",
    "Malaysia", "Mexico", "Morocco", "Netherlands", "New Zealand", "Nigeria", "Norway",
    "Pakistan", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia",
    "Saudi Arabia", "Singapore", "Slovakia", "Slovenia", "South Africa", "South Korea", "Spain", "Sri Lanka",
    "Sweden", "Switzerland", "Thailand", "Turkey", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Vietnam"
]
