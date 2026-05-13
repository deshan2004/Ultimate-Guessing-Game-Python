import streamlit as st
from utils import init_session_state
from ui import login_page, main_menu, number_game_page, word_game_page, code_breaker_page, stats_page

# Page config
st.set_page_config(
    page_title="Ultimate Guessing Game",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session_state()

# Page routing
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "main_menu":
    main_menu()
elif st.session_state.page == "number_game":
    number_game_page()
elif st.session_state.page == "word_game":
    word_game_page()
elif st.session_state.page == "code_breaker":
    code_breaker_page()
elif st.session_state.page == "stats":
    stats_page()