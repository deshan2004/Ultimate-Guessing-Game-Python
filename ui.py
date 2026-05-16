# ui.py
import streamlit as st
import time
from utils import show_toast, reset_game_state, record_game_result
from games import (
    number_guessing_game, check_number_guess,
    word_guessing_game, check_word_guess,
    code_breaker_game, check_code_breaker
)

def apply_modern_theme():
    """Apply an elite, ultra-modern black space theme with fluid animations"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;&display=swap');
        
        /* Root container overrides */
        .stApp {
            background-color: #030303 !important;
            background-image: 
                radial-gradient(1px 1px at 25px 35px, #ffffff, rgba(0,0,0,0)),
                radial-gradient(1.5px 1.5px at 60px 120px, #ffffff, rgba(0,0,0,0)),
                radial-gradient(1px 1px at 150px 240px, #ffffff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 220px 60px, rgba(124, 58, 237, 0.4), rgba(0,0,0,0)),
                radial-gradient(1.5px 1.5px at 300px 320px, #ffffff, rgba(0,0,0,0));
            background-size: 350px 350px;
            animation: spaceDrift 60s linear infinite;
        }

        @keyframes spaceDrift {
            0% { background-position: 0px 0px; }
            100% { background-position: 350px 700px; }
        }

        h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
            font-family: 'Space Grotesk', 'Inter', sans-serif !important;
        }

        /* Premium Glow Page Title */
        .page-title {
            text-align: center;
            font-size: 2.8rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 2.5rem;
            letter-spacing: -1px;
            background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(167, 139, 250, 0.25);
            animation: fadeInDown 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Glassmorphic Cyberpunk Card Matrix */
        .modern-card {
            background: rgba(13, 13, 23, 0.75) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border-radius: 20px !important;
            padding: 2rem !important;
            margin-bottom: 1.5rem !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6) !important;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
            animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .modern-card:hover {
            transform: translateY(-4px) !important;
            border-color: rgba(167, 139, 250, 0.3) !important;
            box-shadow: 0 15px 45px rgba(124, 58, 237, 0.15) !important;
        }

        /* Neon Sidebar Player Panel */
        .stats-card {
            background: linear-gradient(145deg, #0d0d17 0%, #07070c 100%) !important;
            border-radius: 20px !important;
            padding: 1.8rem !important;
            text-align: center !important;
            border: 1px solid rgba(167, 139, 250, 0.15) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5) !important;
            animation: pulseGlow 4s infinite alternate;
        }

        @keyframes pulseGlow {
            0% { box-shadow: 0 0 15px rgba(124, 58, 237, 0.05); border-color: rgba(167, 139, 250, 0.1); }
            100% { box-shadow: 0 0 30px rgba(124, 58, 237, 0.2); border-color: rgba(167, 139, 250, 0.3); }
        }

        /* Dynamic Neon UI Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 30px !important;
            padding: 0.75rem 1.75rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.25) !important;
        }

        .stButton > button:hover {
            background: linear-gradient(90deg, #4f46e5, #7c3aed) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(124, 58, 237, 0.45) !important;
        }

        /* Deep Tech Form Fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            border-radius: 14px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            background-color: rgba(20, 20, 35, 0.6) !important;
            color: #ffffff !important;
            padding: 0.75rem 1.2rem !important;
            transition: all 0.3s !important;
        }

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: #8b5cf6 !important;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
            background-color: rgba(30, 30, 50, 0.8) !important;
        }

        /* Dashboard Metric Widgets */
        .stMetric {
            background: rgba(15, 15, 25, 0.8) !important;
            padding: 1.2rem !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
        }

        .stMetric label { color: #94a3b8 !important; font-weight: 500 !important; }
        .stMetric div { color: #c084fc !important; font-weight: 700 !important; }

        /* Game Progress bar engine */
        .stProgress > div > div {
            background: linear-gradient(90deg, #6366f1, #ec4899) !important;
            border-radius: 10px !important;
        }

        /* Matrix Display Game Hint Blocks */
        .game-hint {
            background: #07070c !important;
            padding: 1.2rem !important;
            border-radius: 14px !important;
            font-family: 'Courier New', monospace !important;
            font-size: 1.4rem !important;
            font-weight: bold !important;
            text-align: center !important;
            color: #38bdf8 !important;
            letter-spacing: 4px !important;
            border: 1px dashed rgba(56, 189, 248, 0.3) !important;
            box-shadow: inset 0 0 15px rgba(0,0,0,0.8);
        }

        /* Success & Error Status Blocks */
        .success-message {
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.25)) !important;
            color: #34d399 !important;
            padding: 1.2rem !important;
            border-radius: 14px !important;
            border: 1px solid rgba(52, 211, 153, 0.3) !important;
            text-align: center;
            font-weight: 600;
            animation: slideIn 0.4s ease;
        }

        .error-message {
            background: linear-gradient(90deg, rgba(239, 68, 68, 0.15), rgba(220, 38, 38, 0.25)) !important;
            color: #f87171 !important;
            padding: 1.2rem !important;
            border-radius: 14px !important;
            border: 1px solid rgba(248, 113, 113, 0.3) !important;
            text-align: center;
            font-weight: 600;
            animation: shake 0.4s ease;
        }

        @keyframes slideIn { from { opacity:0; transform:translateY(-10px); } to { opacity:1; transform:translateY(0); } }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-6px); }
            75% { transform: translateX(6px); }
        }

        .info-box {
            background: rgba(30, 41, 59, 0.4);
            border-left: 4px solid #8b5cf6;
            padding: 1rem;
            border-radius: 12px;
            color: #cbd5e1;
        }

        .achievement-badge {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.1), rgba(236, 72, 153, 0.1)) !important;
            border-radius: 16px !important;
            padding: 1.2rem !important;
            text-align: center !important;
            border: 1px solid rgba(167, 139, 250, 0.3) !important;
            color: #e9d5ff !important;
            transition: all 0.3s !important;
        }

        .achievement-badge:hover {
            transform: scale(1.04) rotate(0.5deg) !important;
            border-color: #ec4899 !important;
        }

        .achievement-locked {
            background: rgba(20, 20, 30, 0.6) !important;
            border: 1px solid rgba(255,255,255,0.05) !important;
            color: #64748b !important;
        }

        .footer { text-align: center; color: #475569; margin-top: 4rem; padding: 1rem; font-size: 0.85rem; }
        .stRadio > div { background-color: rgba(13,13,23,0.6) !important; border: 1px solid rgba(255,255,255,0.05) !important; border-radius: 14px; padding: 0.8rem; }
        
        /* Clean tabs customization */
        .stTabs [data-baseweb="tab-list"] { gap: 10px; }
        .stTabs [data-baseweb="tab"] { background-color: transparent !important; color: #94a3b8 !important; border-radius: 8px; padding: 0.5rem 1rem; }
        .stTabs [aria-selected="true"] { color: #ffffff !important; font-weight: bold; background-color: rgba(124,58,237,0.2) !important; }
    </style>
    """, unsafe_allow_html=True)

def login_page():
    apply_modern_theme()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<h1 class="page-title">Ultimate Guessing Game</h1>', unsafe_allow_html=True)
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Player Login", "📝 Create Account"])
        
        with tab1:
            st.markdown("<h3 style='color:white; margin-top:10px;'>Welcome, Adventurer!</h3>", unsafe_allow_html=True)
            with st.form(key="login_form"):
                username = st.text_input("Username:", placeholder="Enter username...", key="l_username").strip()
                password = st.text_input("Password:", type="password", placeholder="Enter password...", key="l_password")
                submit_login = st.form_submit_button("Enter Arena", use_container_width=True)
                
            if submit_login:
                if username and password:
                    from database import authenticate_user
                    user_record = authenticate_user(username, password)
                    if user_record:
                        st.session_state.player_name = user_record["username"]
                        st.session_state.total_score = user_record.get("total_score", 0)
                        st.session_state.games_won = user_record.get("games_won", 0)
                        st.session_state.total_games_played = user_record.get("total_games_played", 0)
                        st.session_state.game_history = user_record.get("game_history", [])
                        
                        st.session_state.page = "main_menu"
                        show_toast(f"Welcome back, {username}! Let the games begin! ✨", "success")
                        st.rerun()
                    else:
                        show_toast("Invalid Username or Password!", "error")
                else:
                    show_toast("Please enter both username and password!", "warning")
        
        with tab2:
            st.markdown("<h3 style='color:white; margin-top:10px;'>Register Account</h3>", unsafe_allow_html=True)
            with st.form(key="signup_form"):
                reg_username = st.text_input("Choose Username:", placeholder="e.g. GamerX", key="r_username").strip()
                reg_password = st.text_input("Choose Password:", type="password", placeholder="Min 4 characters", key="r_password")
                reg_password_conf = st.text_input("Confirm Password:", type="password", placeholder="Retype password", key="r_password_conf")
                submit_register = st.form_submit_button("Register Account", use_container_width=True)
                
            if submit_register:
                if reg_username and reg_password and reg_password_conf:
                    if reg_password != reg_password_conf:
                        show_toast("Passwords do not match!", "error")
                    elif len(reg_password) < 4:
                        show_toast("Password must be at least 4 characters!", "warning")
                    else:
                        from database import create_user
                        success, msg = create_user(reg_username, reg_password)
                        if success:
                            show_toast(f"{msg} Please log in via Login tab.", "success")
                        else:
                            show_toast(msg, "error")
                else:
                    show_toast("Please fill in all fields!", "warning")
                    
        st.markdown('</div>', unsafe_allow_html=True)

def main_menu():
    apply_modern_theme()
    
    st.sidebar.markdown(f"""
    <div class='stats-card'>
        <h2 style='color:white; margin:0;'>{st.session_state.player_name}</h2>
        <hr style='border-top:1px solid rgba(255,255,255,0.1);'>
        <h1 style='font-size: 3rem; margin: 0.5rem 0; color:#c084fc;'>{st.session_state.total_score}</h1>
        <p style='color:#94a3b8; margin:0;'>Total Score</p>
        <h3 style='color:white; margin:10px 0 0 0;'>{st.session_state.games_won}</h3>
        <p style='color:#94a3b8; margin:0;'>Games Won</p>
        <h3 style='color:white; margin:10px 0 0 0;'>{st.session_state.total_games_played}</h3>
        <p style='color:#94a3b8; margin:0;'>Total Games</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.total_games_played > 0:
        win_rate = (st.session_state.games_won / st.session_state.total_games_played) * 100
        st.sidebar.markdown(f"""
        <div class='info-box' style='margin-top:15px;'>
            <strong>📈 Win Rate:</strong> {win_rate:.1f}%<br>
            <strong>⭐ Level:</strong> {min(99, st.session_state.total_score // 100 + 1)}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="page-title">Choose Your Challenge</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:white;margin:0;'>🔢 Number Guessing</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8;'>Test your intuition and guessing skills</p>", unsafe_allow_html=True)
        st.markdown("<p style='color:#e2e8f0;'><b>Points:</b> 5-20 | <b>Difficulty:</b> Selectable</p>", unsafe_allow_html=True)
        if st.button("Play Number Game", use_container_width=True, key="num_btn"):
            reset_game_state()
            st.session_state.page = "number_game"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:white;margin:0;'>🔐 Code Breaker</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8;'>Crack the secret 4-digit code</p>", unsafe_allow_html=True)
        st.markdown("<p style='color:#e2e8f0;'><b>Points:</b> 30 | <b>Attempts:</b> 10</p>", unsafe_allow_html=True)
        if st.button("Play Code Breaker", use_container_width=True, key="code_btn"):
            reset_game_state()
            st.session_state.page = "code_breaker"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:white;margin:0;'>📝 Word Guessing</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8;'>Expand your vocabulary</p>", unsafe_allow_html=True)
        st.markdown("<p style='color:#e2e8f0;'><b>Points:</b> 20 | <b>Attempts:</b> 6</p>", unsafe_allow_html=True)
        if st.button("Play Word Game", use_container_width=True, key="word_btn"):
            reset_game_state()
            st.session_state.page = "word_game"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:white;margin:0;'>📊 Statistics</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8;'>View your progress and achievements</p>", unsafe_allow_html=True)
        st.markdown("<p style='color:#e2e8f0;'>&nbsp;</p>", unsafe_allow_html=True)
        if st.button("View Stats", use_container_width=True, key="stats_btn"):
            st.session_state.page = "stats"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    colb1, colb2, colb3 = st.columns([1,2,1])
    with colb2:
        if st.button("Exit Game", use_container_width=True):
            st.balloons()
            st.markdown('<div class="success-message">Thanks for playing! Come back soon! 👋</div>', unsafe_allow_html=True)
            time.sleep(2)
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            from utils import init_session_state
            init_session_state()
            st.rerun()
    
    st.markdown('<div class="footer">Made with Streamlit | Challenge your mind</div>', unsafe_allow_html=True)

def number_game_page():
    apply_modern_theme()
    st.markdown('<h1 class="page-title">Number Guessing Challenge</h1>', unsafe_allow_html=True)
    
    if not st.session_state.game_started:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:white; margin:0 0 15px 0;'>Select Difficulty</h3>", unsafe_allow_html=True)
        difficulty = st.radio(
            "",
            ["Easy (1-50, ∞ attempts, 5 pts)", 
             "Medium (1-100, 10 attempts, 10 pts)", 
             "Hard (1-500, 5 attempts, 20 pts)"],
            horizontal=True,
            label_visibility="collapsed"
        )
        if "Easy" in difficulty:
            diff = "easy"
        elif "Medium" in difficulty:
            diff = "medium"
        else:
            diff = "hard"
        
        if st.button("Start Game", use_container_width=True):
            number_guessing_game(diff)
            show_toast("Game started! Make your first guess!", "info")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        low, high, max_att, points = number_guessing_game(None)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Range", f"{low} - {high}")
        with col2:
            if max_att == float('inf'):
                st.metric("Attempts", "∞")
            else:
                st.metric("Attempts Left", st.session_state.attempts_left)
        with col3:
            st.metric("Points at stake", points)
        
        if max_att != float('inf') and max_att > 0:
            progress = (max_att - st.session_state.attempts_left) / max_att
            st.progress(progress)
        
        guess = st.number_input("Enter your guess:", min_value=low, max_value=high, step=1, key="num_guess_input")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Submit Guess", use_container_width=True, key="submit_guess_btn"):
                result = check_number_guess(guess)
                if result[0] == "win":
                    record_game_result(True, result[2], "Number Game")
                    st.balloons()
                    st.markdown(f"""
                    <div class='success-message'>
                        🎉 Perfect! You guessed it in {result[1]} tries!<br>
                        +{result[2]} points!<br>
                        Total Score: {st.session_state.total_score}
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    reset_game_state()
                    st.session_state.page = "main_menu"
                    st.rerun()
                elif result[0] == "lose":
                    record_game_result(False, 0, "Number Game")
                    st.markdown(f"""
                    <div class='error-message'>
                        💀 Game Over! The number was {result[1]} 💀
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    reset_game_state()
                    st.session_state.page = "main_menu"
                    st.rerun()
                else:
                    if result[1] == "too_low":
                        st.warning(f"📉 Too Low! {result[2]}")
                    else:
                        st.warning(f"📈 Too High! {result[2]}")
                    st.rerun()
        
        with col_btn2:
            if st.button("Give Up", use_container_width=True, key="give_up_btn"):
                record_game_result(False, 0, "Number Game")
                st.markdown(f"""
                <div class='error-message'>
                    😔 You gave up! The number was {st.session_state.secret_number}
                </div>
                """, unsafe_allow_html=True)
                time.sleep(2)
                reset_game_state()
                st.session_state.page = "main_menu"
                st.rerun()

def word_game_page():
    apply_modern_theme()
    st.markdown('<h1 class="page-title">Word Guessing Challenge</h1>', unsafe_allow_html=True)
    
    if not st.session_state.game_started:
        word_guessing_game()
        st.rerun()
    
    secret_word, attempts = word_guessing_game()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Word Length", len(secret_word))
    with col2:
        st.metric("Attempts Left", attempts)
    
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    if st.session_state.word_hint:
        st.markdown("<h4 style='color:white; margin:0 0 10px 0;'>Current Progress</h4>", unsafe_allow_html=True)
        st.markdown(f'<div class="game-hint">{st.session_state.word_hint}</div>', unsafe_allow_html=True)
    else:
        st.markdown("<h4 style='color:white; margin:0 0 10px 0;'>Current Progress</h4>", unsafe_allow_html=True)
        st.markdown(f'<div class="game-hint">{"❓ " * len(secret_word)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    guess = st.text_input("Enter your guess:", max_chars=len(secret_word), key="word_guess_input", 
                         placeholder=f"Enter {len(secret_word)} letters").upper()
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Check Word", use_container_width=True, key="check_word_btn"):
            if len(guess) != len(secret_word):
                st.warning(f"Please enter exactly {len(secret_word)} letters!")
            elif not guess.isalpha():
                st.warning("Please enter only letters!")
            else:
                result = check_word_guess(guess)
                if result[0] == "win":
                    record_game_result(True, 20, "Word Game")
                    st.balloons()
                    st.markdown(f"""
                    <div class='success-message'>
                        🎉 Excellent! The word was {result[1]}!<br>
                        +20 points!<br>
                        Total Score: {st.session_state.total_score}
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    reset_game_state()
                    st.session_state.page = "main_menu"
                    st.rerun()
                elif result[0] == "lose":
                    record_game_result(False, 0, "Word Game")
                    st.markdown(f"""
                    <div class='error-message'>
                        💀 Game Over! The word was {result[1]} 💀
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    reset_game_state()
                    st.session_state.page = "main_menu"
                    st.rerun()
                else:
                    st.session_state.word_hint = result[1]
                    st.info(f"Hint: {result[1]}")
                    st.warning(f"Attempts left: {result[2]}")
                    st.rerun()
    
    with col_btn2:
        if st.button("Give Up", use_container_width=True, key="word_give_up_btn"):
            record_game_result(False, 0, "Word Game")
            st.markdown(f"""
            <div class='error-message'>
                😔 The word was {st.session_state.secret_word}
            </div>
            """, unsafe_allow_html=True)
            time.sleep(2)
            reset_game_state()
            st.session_state.page = "main_menu"
            st.rerun()

def code_breaker_page():
    apply_modern_theme()
    st.markdown('<h1 class="page-title">Code Breaker Challenge</h1>', unsafe_allow_html=True)
    
    if not st.session_state.game_started:
        code_breaker_game()
        st.rerun()
    
    secret_code, attempts = code_breaker_game()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Code Length", "4 digits")
    with col2:
        st.metric("Attempts Left", attempts)
    
    if st.session_state.code_history:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:white; margin:0 0 10px 0;'>Guess History</h3>", unsafe_allow_html=True)
        for item in st.session_state.code_history[-5:]:
            st.code(item, language="text")
        st.markdown('</div>', unsafe_allow_html=True)
    
    guess = st.text_input("Enter 4-digit code:", max_chars=4, key="code_guess_input", placeholder="e.g., 1234")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Crack Code", use_container_width=True, key="crack_code_btn"):
            if len(guess) != 4 or not guess.isdigit():
                st.warning("Please enter exactly 4 digits (0-9)!")
            else:
                result = check_code_breaker(guess)
                if result[0] == "win":
                    record_game_result(True, 30, "Code Breaker")
                    st.balloons()
                    st.markdown(f"""
                    <div class='success-message'>
                        🎉 Access Granted! The code was {result[1]}!<br>
                        +30 points!<br>
                        Total Score: {st.session_state.total_score}
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    reset_game_state()
                    st.session_state.page = "main_menu"
                    st.rerun()
                elif result[0] == "lose":
                    record_game_result(False, 0, "Code Breaker")
                    st.markdown(f"""
                    <div class='error-message'>
                        🔒 System Locked! The code was {result[1]} 🔒
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    reset_game_state()
                    st.session_state.page = "main_menu"
                    st.rerun()
                else:
                    st.session_state.code_history.append(f"{guess} → {result[1]}")
                    st.info(f"Hint: {result[1]}")
                    st.warning(f"Attempts left: {result[2]}")
                    st.rerun()
    
    with col_btn2:
        if st.button("Give Up", use_container_width=True, key="code_give_up_btn"):
            record_game_result(False, 0, "Code Breaker")
            st.markdown(f"""
            <div class='error-message'>
                😔 The code was {st.session_state.secret_code}
            </div>
            """, unsafe_allow_html=True)
            time.sleep(2)
            reset_game_state()
            st.session_state.page = "main_menu"
            st.rerun()

def stats_page():
    apply_modern_theme()
    st.markdown('<h1 class="page-title">Player Statistics</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:white; margin:0;'>👤 {st.session_state.player_name}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='color:#e2e8f0;'>🏆 Total Score: {st.session_state.total_score}</h4>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='color:#e2e8f0;'>🎮 Games Won: {st.session_state.games_won}</h4>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='color:#e2e8f0;'>📊 Total Games: {st.session_state.total_games_played}</h4>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        if st.session_state.total_games_played > 0:
            win_rate = (st.session_state.games_won / st.session_state.total_games_played) * 100
            st.markdown(f"<h3 style='color:white; margin:0;'>📈 Win Rate: {win_rate:.1f}%</h3>", unsafe_allow_html=True)
            level = st.session_state.total_score // 100 + 1
            next_level_points = 100 - (st.session_state.total_score % 100)
            st.markdown(f"<h4 style='color:#e2e8f0;'>⭐ Level: {min(99, level)}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='color:#e2e8f0;'>🎯 Next level in {next_level_points} points</h4>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='color:white; margin:0;'>🎯 Play your first game!</h3>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<hr style='border-top:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:white;'>🏅 Achievements</h3>", unsafe_allow_html=True)
    
    achievements = [
        ("First Blood", st.session_state.games_won >= 1, "Win your first game"),
        ("Rising Star", st.session_state.games_won >= 3, "Win 3 games"),
        ("Veteran", st.session_state.games_won >= 10, "Win 10 games"),
        ("Point Master", st.session_state.total_score >= 100, "Score 100+ points"),
        ("Elite Player", st.session_state.total_score >= 500, "Score 500+ points"),
        ("Number Guru", "Number Game" in st.session_state.game_history, "Win number game"),
        ("Word Master", "Word Game" in st.session_state.game_history, "Win word game"),
        ("Code Breaker Elite", "Code Breaker" in st.session_state.game_history, "Win code breaker")
    ]
    
    cols = st.columns(3)
    for idx, (achievement, unlocked, description) in enumerate(achievements):
        with cols[idx % 3]:
            if unlocked:
                st.markdown(f"""
                <div class='achievement-badge'>
                    ✅ {achievement}<br>
                    <small style='color:#cbd5e1;'>{description}</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='achievement-badge achievement-locked'>
                    🔒 {achievement}<br>
                    <small style='color:#64748b;'>{description}</small>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    if st.button("Back to Main Menu", use_container_width=True):
        st.session_state.page = "main_menu"
        st.rerun()