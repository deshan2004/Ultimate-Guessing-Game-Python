# check_users.py
import streamlit as st
from pymongo import MongoClient

st.set_page_config(page_title="Registered Users", page_icon="👤", layout="wide")

st.title("🏆 Registered Users Dashboard")
st.subheader("MongoDB Cloud එකේ සේව් වී ඇති සියලුම ක්‍රීඩකයින්ගේ ලැයිස්තුව")

try:
    # ඩේටාබේස් සම්බන්ධතාවය
    client = MongoClient(st.secrets["MONGO_URI"], tlsAllowInvalidCertificates=True)
    db = client["guessing_game_db"]
    users_collection = db["users"]
    
    # සියලුම දත්ත ලබා ගැනීම
    users_list = list(users_collection.find())
    
    if not users_list:
        st.info("තවමත් කිසිදු පරිශීලකයෙකු ලියාපදිංචි වී නොමැත.")
    else:
        # දත්ත ටික ලස්සන table එකකට සකස් කිරීම
        table_data = []
        for index, user in enumerate(users_list, 1):
            table_data.append({
                "No": index,
                "👤 Username": user.get("username", "N/A"),
                "🏆 Total Score": user.get("total_score", 0),
                "🎮 Games Played": user.get("total_games_played", 0),
                "🥇 Games Won": user.get("games_won", 0)
            })
            
        # Streamlit Table එකක් ලෙස පෙන්වීම
        st.dataframe(table_data, use_container_width=True)
        st.success(f"සම්පූර්ණ පරිශීලකයින් සංඛ්‍යාව: {len(users_list)}")
        
except Exception as e:
    st.error(f"Error connecting to database: {e}")