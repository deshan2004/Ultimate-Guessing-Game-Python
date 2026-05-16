# check_users.py
import streamlit as st
from pymongo import MongoClient

st.set_page_config(page_title="Registered Users", page_icon="👤", layout="wide")

# Theme synchronization for Admin Dashboard
st.markdown("""
<style>
    .stApp {
        background-color: #030303 !important;
        background-image: radial-gradient(rgba(255,255,255,0.08) 1px, transparent 0);
        background-size: 24px 24px;
    }
    h1, h3, label, p { font-family: 'Space Grotesk', sans-serif !important; color: white !important; }
    div[data-testid="stDataFrame"] {
        background-color: rgba(13,13,23,0.7) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏆 Registered Users Dashboard")
st.subheader("MongoDB Cloud එකේ සේව් වී ඇති සියලුම ක්‍රීඩකයින්ගේ ලැයිස්තුව")

try:
    client = MongoClient(st.secrets["MONGO_URI"], tlsAllowInvalidCertificates=True)
    db = client["guessing_game_db"]
    users_collection = db["users"]
    
    users_list = list(users_collection.find())
    
    if not users_list:
        st.info("තවමත් කිසිදු පරිශීලකයෙකු ලියාපදිංචි වී නොමැත.")
    else:
        table_data = []
        for index, user in enumerate(users_list, 1):
            table_data.append({
                "No": index,
                "👤 Username": user.get("username", "N/A"),
                "🏆 Total Score": user.get("total_score", 0),
                "🎮 Games Played": user.get("total_games_played", 0),
                "🥇 Games Won": user.get("games_won", 0)
            })
            
        st.dataframe(table_data, use_container_width=True)
        st.success(f"සම්පූර්ණ පරිශීලකයින් සංඛ්‍යාව: {len(users_list)}")
        
except Exception as e:
    st.error(f"Error connecting to database: {e}")