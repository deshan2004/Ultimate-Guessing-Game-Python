# database.py
import hashlib
import streamlit as st
from pymongo import MongoClient

@st.cache_resource
def get_database():
    """
    Establish connection to MongoDB Atlas safely.
    Handles network timeouts and SSL certificate validation issues automatically.
    """
    if "MONGO_URI" not in st.secrets:
        st.error("❌ MONGO_URI not found in .streamlit/secrets.toml")
        return None
        
    try:
        # tlsAllowInvalidCertificates=True යෙදීමෙන් SSL/Certificate errors මඟහැරේ
        # admin.command('ping') එක ඉවත් කර ඇති නිසා Permissions (Role) දෝෂ ඇති නොවේ
        client = MongoClient(
            st.secrets["MONGO_URI"], 
            tlsAllowInvalidCertificates=True,
            serverSelectionTimeoutMS=5000
        )
        
        # කෙලින්ම අපගේ Database එක තෝරාගෙන ඉදිරියට යයි
        db = client["guessing_game_db"]
        return db
    except Exception as e:
        st.error(f"❌ Database Connection Error: {e}")
        return None

# Database එක සම්බන්ධ කරගැනීම
db = get_database()

def hash_password(password):
    """Securely hash the password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    """Register a new user inside MongoDB"""
    if db is None:
        return False, "Database connection error! Please check your network or credentials."
        
    users_collection = db["users"]
    
    # දැනටමත් මේ නමින් කෙනෙක් ඉන්නවාදැයි බැලීම
    if users_collection.find_one({"username": username}):
        return False, "Username already exists!"
    
    hashed_pass = hash_password(password)
    user_data = {
        "username": username,
        "password": hashed_pass,
        "total_score": 0,
        "games_won": 0,
        "total_games_played": 0,
        "game_history": []
    }
    users_collection.insert_one(user_data)
    return True, "Registration successful!"

def authenticate_user(username, password):
    """Validate user credentials and return user stats if valid"""
    if db is None:
        return None
        
    users_collection = db["users"]
    user = users_collection.find_one({"username": username})
    if user and user["password"] == hash_password(password):
        return user
    return None

def update_user_stats(username, win, points_earned, game_name):
    """Update player metrics inside MongoDB permanently"""
    if db is None:
        return
        
    users_collection = db["users"]
    update_query = {
        "$inc": {
            "total_games_played": 1,
            "games_won": 1 if win else 0,
            "total_score": points_earned if win else 0
        }
    }
    if win:
        update_query["$push"] = {"game_history": game_name}
        
    users_collection.update_one({"username": username}, update_query)