import streamlit as st
import time

def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'player_name': "",
        'total_score': 0,
        'games_won': 0,
        'total_games_played': 0,
        'game_history': [],
        'page': "login",
        'current_game': None,
        'secret_number': None,
        'attempts_left': 0,
        'num_tries': 0,
        'secret_word': None,
        'word_attempts': 0,
        'secret_code': None,
        'code_attempts': 0,
        'code_history': [],
        'difficulty': None,
        'game_started': False,
        'word_hint': None,
        'number_range': (1, 100),
        'max_attempts': 10,
        'num_points': 10
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def record_game_result(win, points_earned, game_name):
    """Record game result and update statistics"""
    st.session_state.total_games_played += 1
    if win:
        st.session_state.games_won += 1
        st.session_state.total_score += points_earned
        st.session_state.game_history.append(game_name)
        return True
    return False

def show_toast(message, type="success"):
    """Show a styled notification"""
    icons = {"success": "✨", "error": "💀", "warning": "⚠️", "info": "ℹ️"}
    if type == "success":
        st.success(f"{icons[type]} {message} {icons[type]}")
    elif type == "error":
        st.error(f"{icons[type]} {message} {icons[type]}")
    elif type == "warning":
        st.warning(f"{icons[type]} {message} {icons[type]}")
    else:
        st.info(f"{icons[type]} {message} {icons[type]}")
    time.sleep(0.5)

def reset_game_state():
    """Reset current game state"""
    st.session_state.game_started = False
    st.session_state.secret_number = None
    st.session_state.secret_word = None
    st.session_state.secret_code = None
    st.session_state.code_history = []
    st.session_state.word_hint = None
    st.session_state.num_tries = 0
    st.session_state.word_attempts = 0
    st.session_state.code_attempts = 0