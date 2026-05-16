# check_users.py
import streamlit as st
from pymongo import MongoClient

st.set_page_config(page_title="Registered Users", page_icon="👤", layout="wide")

# Apply the same black space theme + animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: #030303;
        background-image: radial-gradient(1px 1px at 25px 35px, #ffffff, rgba(0,0,0,0)),
                          radial-gradient(1.5px 1.5px at 60px 120px, #ffffff, rgba(0,0,0,0));
        background-size: 300px 300px;
        animation: starsMove 40s linear infinite;
    }
    
    @keyframes starsMove {
        0% { background-position: 0 0; }
        100% { background-position: 300px 600px; }
    }
    
    h1, h2, h3, p, label {
        font-family: 'Space Grotesk', sans-serif;
        color: white;
    }
    
    h1 {
        text-align: center;
        font-size: 2.8rem;
        background: linear-gradient(135deg, #ffffff, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .stSubheader {
        text-align: center;
        color: #94a3b8 !important;
        margin-bottom: 2rem;
        animation: fadeInUp 0.6s;
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Dataframe styling */
    div[data-testid="stDataFrame"] {
        background: rgba(13, 13, 23, 0.7) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 24px;
        padding: 1rem;
        animation: fadeInScale 0.5s;
    }
    
    @keyframes fadeInScale {
        from { opacity: 0; transform: scale(0.98); }
        to { opacity: 1; transform: scale(1); }
    }
    
    /* Success and info alerts */
    .stAlert {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 16px;
        color: #34d399;
        font-weight: 500;
    }
    
    .stException, .stError {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 16px;
    }
    
    /* Sidebar (if any) */
    [data-testid="stSidebar"] {
        background: #050507;
        border-right: 1px solid rgba(255,255,255,0.03);
    }
    
    hr {
        border-color: rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

st.title("🏆 Registered Users Dashboard")
st.subheader("Complete list of all players currently stored in MongoDB Cloud")

try:
    # Database connection
    client = MongoClient(st.secrets["MONGO_URI"], tlsAllowInvalidCertificates=True)
    db = client["guessing_game_db"]
    users_collection = db["users"]
    
    # Fetch all users
    users_list = list(users_collection.find())
    
    if not users_list:
        st.info("📭 No users have registered yet. Be the first to play!")
    else:
        # Prepare clean English table data
        table_data = []
        for index, user in enumerate(users_list, 1):
            table_data.append({
                "No": index,
                "👤 Username": user.get("username", "N/A"),
                "🏆 Total Score": user.get("total_score", 0),
                "🎮 Games Played": user.get("total_games_played", 0),
                "🥇 Games Won": user.get("games_won", 0)
            })
            
        # Display the table
        st.dataframe(table_data, use_container_width=True)
        
        # Summary message
        st.success(f"✅ Total registered players: {len(users_list)}")
        
except Exception as e:
    st.error(f"❌ Database connection error: {e}")