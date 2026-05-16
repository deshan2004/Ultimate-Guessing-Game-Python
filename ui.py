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
    """Apply clean, professional styling with black background & animations"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Animated black background with subtle moving stars */
        .stApp {
            background: #000000;
            position: relative;
            overflow-x: hidden;
        }
        
        /* Stars animation */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(2px 2px at 20px 30px, #ffffff, rgba(0,0,0,0)),
                        radial-gradient(1px 1px at 80px 150px, #ffffff, rgba(0,0,0,0));
            background-repeat: no-repeat;
            background-size: 200px 200px;
            opacity: 0.3;
            pointer-events: none;
            animation: starsMove 40s linear infinite;
            z-index: 0;
        }
        
        @keyframes starsMove {
            0% { background-position: 0 0, 0 0; }
            100% { background-position: 500px 500px, 300px 400px; }
        }
        
        /* Main container */
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }
        
        /* Page title with glow animation */
        .page-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 2rem;
            letter-spacing: -0.5px;
            text-shadow: 0 0 10px rgba(255,255,255,0.5);
            animation: fadeInDown 0.8s ease-out, glowPulse 3s infinite;
        }
        
        @keyframes glowPulse {
            0% { text-shadow: 0 0 5px rgba(255,255,255,0.3); }
            50% { text-shadow: 0 0 20px rgba(255,255,255,0.8); }
            100% { text-shadow: 0 0 5px rgba(255,255,255,0.3); }
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Modern card – dark glassmorphism */
        .modern-card {
            background: rgba(30, 30, 46, 0.85);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 1.8rem;
            margin: 1rem 0;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            transition: all 0.4s cubic-bezier(0.2, 0.9, 0.4, 1.1);
            border: 1px solid rgba(255,255,255,0.1);
            animation: fadeInUp 0.6s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .modern-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.5);
            border-color: rgba(255,255,255,0.3);
            background: rgba(40, 40, 60, 0.9);
        }
        
        /* Stats card gradient with animation */
        .stats-card {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 24px;
            padding: 1.5rem;
            color: white;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            transition: transform 0.3s, box-shadow 0.3s;
            animation: fadeInScale 0.5s ease-out;
            border: 1px solid rgba(255,255,255,0.15);
        }
        
        .stats-card:hover {
            transform: scale(1.02);
            box-shadow: 0 20px 35px rgba(0,0,0,0.6);
        }
        
        @keyframes fadeInScale {
            from {
                opacity: 0;
                transform: scale(0.95);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        .stats-card h2, .stats-card h3, .stats-card p {
            color: white;
            margin: 0.5rem 0;
        }
        
        /* Buttons with neon pulse effect */
        .stButton > button {
            background: linear-gradient(90deg, #4f46e5, #7c3aed);
            color: white;
            border: none;
            border-radius: 40px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            width: 100%;
            box-shadow: 0 4px 15px rgba(79,70,229,0.3);
            animation: fadeInUp 0.5s;
        }
        
        .stButton > button:hover {
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(79,70,229,0.5);
        }
        
        .stButton > button:active {
            transform: translateY(1px);
        }
        
        /* Input fields – dark style */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            border-radius: 40px;
            border: 1px solid #333;
            background: #1e1e2f;
            color: white;
            padding: 0.75rem 1rem;
            font-size: 1rem;
            transition: all 0.2s;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: #7c3aed;
            box-shadow: 0 0 0 3px rgba(124,58,237,0.2);
            background: #2a2a3e;
        }
        
        /* Metrics cards */
        .stMetric {
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(5px);
            padding: 1rem;
            border-radius: 20px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.2s;
        }
        
        .stMetric:hover {
            border-color: #7c3aed;
            box-shadow: 0 0 12px rgba(124,58,237,0.3);
        }
        
        .stMetric label {
            font-weight: 600;
            color: #e2e8f0;
        }
        
        .stMetric div {
            font-size: 1.8rem;
            font-weight: 700;
            color: #a78bfa;
        }
        
        /* Success/Error messages with slide & pulse */
        .success-message {
            background: linear-gradient(95deg, #10b981, #059669);
            color: white;
            padding: 1rem;
            border-radius: 20px;
            text-align: center;
            font-weight: 600;
            margin: 1rem 0;
            animation: slideIn 0.4s, pulse 1s ease-out;
        }
        
        .error-message {
            background: linear-gradient(95deg, #ef4444, #dc2626);
            color: white;
            padding: 1rem;
            border-radius: 20px;
            text-align: center;
            font-weight: 600;
            margin: 1rem 0;
            animation: slideIn 0.4s, shake 0.5s;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-15px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        
        @keyframes shake {
            0%,100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        
        /* Info box */
        .info-box {
            background: #1e293b;
            border-left: 4px solid #a78bfa;
            padding: 1rem;
            border-radius: 16px;
            margin: 1rem 0;
            color: #f1f5f9;
            transition: 0.2s;
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background: linear-gradient(90deg, #a78bfa, #c084fc);
            border-radius: 20px;
        }
        
        /* Radio buttons */
        .stRadio > div {
            background: #1e1e2f;
            padding: 1rem;
            border-radius: 20px;
            border: 1px solid #333;
            color: white;
        }
        
        /* Achievement badges with hover scale */
        .achievement-badge {
            background: linear-gradient(135deg, #fef3c7, #fde68a);
            border-radius: 20px;
            padding: 1rem;
            margin: 0.5rem;
            text-align: center;
            font-weight: 600;
            color: #92400e;
            transition: all 0.2s;
            border: 1px solid #fcd34d;
            animation: fadeInUp 0.3s;
        }
        
        .achievement-badge:hover {
            transform: scale(1.05) rotate(1deg);
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        }
        
        .achievement-locked {
            background: #2d2d3f;
            border: 1px solid #4b5563;
            color: #9ca3af;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #a1a1aa;
            margin-top: 3rem;
            padding: 1.5rem;
            font-size: 0.875rem;
            animation: fadeInUp 0.8s;
        }
        
        /* Sidebar dark */
        .css-1d391kg, .css-12oz5g0 {
            background: rgba(0,0,0,0.7);
            backdrop-filter: blur(12px);
        }
        
        hr {
            margin: 1rem 0;
            border: none;
            border-top: 1px solid #2d3748;
        }
        
        /* Game hint area */
        .game-hint {
            background: #0f172a;
            padding: 1rem;
            border-radius: 20px;
            font-family: monospace;
            font-size: 1.2rem;
            text-align: center;
            margin: 1rem 0;
            color: #e2e8f0;
            letter-spacing: 2px;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .page-title {
                font-size: 1.8rem;
            }
            .modern-card {
                padding: 1.2rem;
            }
        }
        
        /* Additional animation for sidebar stats */
        .stats-card {
            animation: glowPulse 4s infinite;
        }
    </style>
    """, unsafe_allow_html=True)

def login_page():
    apply_modern_theme()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<h1 class="page-title">Ultimate Guessing Game</h1>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            
            # Login & Sign Up Tabs
            tab1, tab2 = st.tabs(["🔐 Player Login", "📝 Create Account"])
            
            # --- TAB 1: LOGIN ---
            with tab1:
                st.markdown("### Welcome, Adventurer!")
                st.markdown("---")
                with st.form(key="login_form"):
                    username = st.text_input("Username:", placeholder="Enter username...", key="l_username").strip()
                    password = st.text_input("Password:", type="password", placeholder="Enter password...", key="l_password")
                    submit_login = st.form_submit_button("Enter Arena", use_container_width=True)
                    
                if submit_login:
                    if username and password:
                        from database import authenticate_user
                        user_record = authenticate_user(username, password)
                        if user_record:
                            # MongoDB data to Session State
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
            
            # --- TAB 2: SIGN UP ---
            with tab2:
                st.markdown("### Register Account")
                st.markdown("---")
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
    
    # Sidebar stats
    st.sidebar.markdown(f"""
    <div class='stats-card'>
        <h2>{st.session_state.player_name}</h2>
        <hr>
        <h1 style='font-size: 3rem; margin: 0.5rem 0;'>{st.session_state.total_score}</h1>
        <p>Total Score</p>
        <h3>{st.session_state.games_won}</h3>
        <p>Games Won</p>
        <p>{st.session_state.total_games_played}</p>
        <p>Total Games</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.total_games_played > 0:
        win_rate = (st.session_state.games_won / st.session_state.total_games_played) * 100
        st.sidebar.markdown(f"""
        <div class='info-box'>
            <strong>📈 Win Rate:</strong> {win_rate:.1f}%<br>
            <strong>⭐ Level:</strong> {min(99, st.session_state.total_score // 100 + 1)}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="page-title">Choose Your Challenge</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("### 🔢 Number Guessing")
            st.markdown("*Test your intuition and guessing skills*")
            st.markdown("**Points:** 5-20 | **Difficulty:** Selectable")
            if st.button("Play Number Game", use_container_width=True, key="num_btn"):
                reset_game_state()
                st.session_state.page = "number_game"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("### 🔐 Code Breaker")
            st.markdown("*Crack the secret 4-digit code*")
            st.markdown("**Points:** 30 | **Attempts:** 10")
            if st.button("Play Code Breaker", use_container_width=True, key="code_btn"):
                reset_game_state()
                st.session_state.page = "code_breaker"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("### 📝 Word Guessing")
            st.markdown("*Expand your vocabulary*")
            st.markdown("**Points:** 20 | **Attempts:** 6")
            if st.button("Play Word Game", use_container_width=True, key="word_btn"):
                reset_game_state()
                st.session_state.page = "word_game"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Statistics")
            st.markdown("*View your progress and achievements*")
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
        st.markdown("### Select Difficulty")
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
        st.markdown(f"### Current Progress")
        st.markdown(f'<div class="game-hint">{st.session_state.word_hint}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"### Current Progress")
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
        st.markdown("### Guess History")
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
        st.markdown(f"### 👤 {st.session_state.player_name}")
        st.markdown(f"### 🏆 Total Score: {st.session_state.total_score}")
        st.markdown(f"### 🎮 Games Won: {st.session_state.games_won}")
        st.markdown(f"### 📊 Total Games: {st.session_state.total_games_played}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        if st.session_state.total_games_played > 0:
            win_rate = (st.session_state.games_won / st.session_state.total_games_played) * 100
            st.markdown(f"### 📈 Win Rate: {win_rate:.1f}%")
            level = st.session_state.total_score // 100 + 1
            next_level_points = 100 - (st.session_state.total_score % 100)
            st.markdown(f"### ⭐ Level: {min(99, level)}")
            st.markdown(f"### 🎯 Next level in {next_level_points} points")
        else:
            st.markdown("### 🎯 Play your first game!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🏅 Achievements")
    
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
                    <small>{description}</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='achievement-badge achievement-locked'>
                    🔒 {achievement}<br>
                    <small>{description}</small>
                </div>
                """, unsafe_allow_html=True)
    
    if st.button("Back to Main Menu", use_container_width=True):
        st.session_state.page = "main_menu"
        st.rerun()