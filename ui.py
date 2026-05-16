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
    """Apply an elite, ultra-modern black space theme with fluid animations + gaming media"""
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
                radial-gradient(2px 2px at 220px 60px, rgba(167, 139, 250, 0.4), rgba(0,0,0,0)),
                radial-gradient(1.5px 1.5px at 300px 180px, rgba(96, 165, 250, 0.4), rgba(0,0,0,0));
            background-size: 350px 350px;
            background-repeat: repeat;
            animation: spaceFloat 120s linear infinite;
            font-family: 'Inter', sans-serif !important;
            position: relative;
            overflow-x: hidden;
        }
        
        /* BACKGROUND VIDEO - Gaming montage */
        .bg-video {
            position: fixed;
            top: 0;
            left: 0;
            min-width: 100%;
            min-height: 100%;
            width: auto;
            height: auto;
            z-index: -2;
            object-fit: cover;
            opacity: 0.25;
            pointer-events: none;
        }
        
        /* Floating game character images */
        .game-character {
            position: fixed;
            z-index: -1;
            width: 80px;
            opacity: 0.2;
            pointer-events: none;
            animation: floatAround 25s infinite ease-in-out;
        }
        
        .char1 { bottom: 10%; left: 2%; width: 100px; animation-duration: 20s; }
        .char2 { top: 15%; right: 3%; width: 90px; animation-duration: 28s; animation-delay: -5s; }
        .char3 { bottom: 20%; right: 8%; width: 110px; animation-duration: 22s; animation-delay: -10s; }
        .char4 { top: 40%; left: 5%; width: 70px; animation-duration: 30s; animation-delay: -2s; }
        
        @keyframes floatAround {
            0% { transform: translate(0, 0) rotate(0deg); }
            25% { transform: translate(20px, -30px) rotate(5deg); }
            50% { transform: translate(-15px, -50px) rotate(-5deg); }
            75% { transform: translate(10px, -20px) rotate(3deg); }
            100% { transform: translate(0, 0) rotate(0deg); }
        }
        
        @keyframes spaceFloat {
            from { background-position: 0 0; }
            to { background-position: 350px 700px; }
        }
        
        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif !important;
            color: #ffffff !important;
            font-weight: 700 !important;
        }
        
        .hero-title {
            text-align: center;
            font-size: 3.5rem !important;
            font-weight: 700;
            background: linear-gradient(135deg, #ffffff 30%, #a78bfa 70%, #60a5fa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem !important;
            letter-spacing: -1.5px;
            animation: pulseTitle 4s ease-in-out infinite;
        }
        
        @keyframes pulseTitle {
            0%, 100% { filter: drop-shadow(0 0 10px rgba(167,139,250,0.1)); }
            50% { filter: drop-shadow(0 0 25px rgba(167,139,250,0.35)); }
        }
        
        .game-card {
            background: rgba(13, 13, 18, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 24px !important;
            padding: 2.2rem !important;
            backdrop-filter: blur(20px) saturate(160%) !important;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5) !important;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
            margin-bottom: 1.5rem;
        }
        
        .game-card:hover {
            transform: translateY(-5px);
            border-color: rgba(167, 139, 250, 0.3) !important;
            box-shadow: 0 30px 60px rgba(124, 58, 237, 0.15) !important;
        }
        
        .stat-block {
            background: linear-gradient(145deg, rgba(20,20,30,0.4) 0%, rgba(10,10,15,0.6) 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-radius: 20px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        div[data-testid="stForm"] {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }
        
        .stTextInput input, .stNumberInput input {
            background-color: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important;
            color: #ffffff !important;
            padding: 0.75rem 1.2rem !important;
            font-size: 1.05rem !important;
            transition: all 0.3s !important;
        }
        
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: #a78bfa !important;
            background-color: rgba(167, 139, 250, 0.05) !important;
            box-shadow: 0 0 20px rgba(167, 139, 250, 0.2) !important;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #6366f1 0%, #a78bfa 50%, #4f46e5 100%) !important;
            background-size: 200% auto !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 0.8rem 1.8rem !important;
            font-weight: 600 !important;
            font-size: 1.05rem !important;
            letter-spacing: -0.3px;
            transition: all 0.4s ease-in-out;
            width: 100%;
            box-shadow: 0 10px 25px rgba(99, 102, 241, 0.25) !important;
        }
        
        .stButton > button:hover {
            background-position: right center !important;
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(167, 139, 250, 0.4) !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            background-color: rgba(255, 255, 255, 0.02) !important;
            border-radius: 16px;
            padding: 6px;
            border: 1px solid rgba(255,255,255,0.03);
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #94a3b8 !important;
            font-weight: 500 !important;
            padding: 0.6rem 1.5rem !important;
            border-radius: 12px;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: rgba(167, 139, 250, 0.15) !important;
            color: #ffffff !important;
        }
        
        .success-banner {
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, rgba(4, 120, 87, 0.2) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 1.2rem; border-radius: 16px; color: #34d399; text-align: center;
            font-weight: 600; font-size: 1.1rem; margin: 1.5rem 0;
        }
        
        .error-banner {
            background: linear-gradient(90deg, rgba(239, 68, 68, 0.1) 0%, rgba(185, 28, 28, 0.2) 100%);
            border: 1px solid rgba(239, 68, 68, 0.3);
            padding: 1.2rem; border-radius: 16px; color: #f87171; text-align: center;
            font-weight: 600; font-size: 1.1rem; margin: 1.5rem 0;
        }
        
        .hint-banner {
            background: rgba(255, 255, 255, 0.02);
            border: 1px dashed rgba(255, 255, 255, 0.1);
            padding: 1.5rem; border-radius: 16px; font-family: 'Space Grotesk', monospace;
            font-size: 1.8rem; font-weight: 700; text-align: center; color: #a78bfa;
            letter-spacing: 6px; margin: 1.5rem 0; box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
        }
        
        .achievement-badge {
            background: linear-gradient(135deg, rgba(167, 139, 250, 0.08) 0%, rgba(99, 102, 241, 0.03) 100%);
            border: 1px solid rgba(167, 139, 250, 0.2);
            border-radius: 16px; padding: 1.2rem; text-align: center; font-weight: 600;
            color: #ffffff; box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .achievement-locked {
            background: rgba(255,255,255,0.01) !important;
            border: 1px solid rgba(255,255,255,0.04) !important;
            color: #475569 !important;
            box-shadow: none !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: #050507 !important;
            border-right: 1px solid rgba(255,255,255,0.03) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <video autoplay muted loop playsinline class="bg-video">
        <source src="https://assets.mixkit.co/videos/preview/mixkit-game-controller-close-up-32812-large.mp4" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <img class="game-character char1" src="https://i.imgur.com/3KpR8QF.png" alt="Mario">
    <img class="game-character char2" src="https://i.imgur.com/sE8jL7l.png" alt="Sonic">
    <img class="game-character char3" src="https://i.imgur.com/MqJqZ3x.png" alt="Master Chief">
    <img class="game-character char4" src="https://i.imgur.com/9eJQ3uL.png" alt="Kratos">
    """, unsafe_allow_html=True)

def login_page():
    apply_modern_theme()
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown('<h1 class="hero-title">🔮 GAME ZONE ACCESS</h1>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#94a3b8; margin-bottom:2rem;'>Please log in or register to start playing.</p>", unsafe_allow_html=True)
        
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            with st.form(key="login_identity_form"):
                username = st.text_input("Username:", placeholder="Enter your username...").strip()
                password = st.text_input("Password:", type="password", placeholder="••••••••")
                submit_login = st.form_submit_button("LOG IN NOW")
                
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
                        st.slots = {}  
                        st.sidebar.empty()
                        st.rerun()
                    else:
                        show_toast("Login Failed: Incorrect username or password", "error")
                else:
                    show_toast("Please fill in all fields", "warning")
                        
        with tab2:
            with st.form(key="register_identity_form"):
                reg_username = st.text_input("Choose Username:", placeholder="e.g. Player_One").strip()
                reg_password = st.text_input("Choose Password:", type="password", placeholder="Min 4 characters")
                reg_password_conf = st.text_input("Confirm Password:", type="password", placeholder="Retype password")
                submit_register = st.form_submit_button("CREATE ACCOUNT")
                
            if submit_register:
                if reg_username and reg_password and reg_password_conf:
                    if reg_password != reg_password_conf:
                        show_toast("Passwords do not match", "error")
                    elif len(reg_password) < 4:
                        show_toast("Password must be at least 4 characters long", "warning")
                    else:
                        from database import create_user
                        success, msg = create_user(reg_username, reg_password)
                        if success:
                            show_toast(f"Account created! You can now log in.", "success")
                        else:
                            show_toast(msg, "error")
                else:
                    show_toast("Please fill in all fields to register", "warning")
        st.markdown('</div>', unsafe_allow_html=True)

def main_menu():
    apply_modern_theme()
    
    st.sidebar.markdown(f"""
    <div class='stat-block' style='margin-bottom: 1.5rem; border-color: rgba(167, 139, 250, 0.15);'>
        <p style='color: #a78bfa; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px; margin:0;'>Player Profile</p>
        <h3 style='margin: 0.3rem 0 0.8rem 0; font-size:1.6rem;'>{st.session_state.player_name}</h3>
        <hr style='border-color: rgba(255,255,255,0.05); margin: 0.5rem 0;'>
        <h1 style='font-size: 3.2rem; background: linear-gradient(135deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0;'>{st.session_state.total_score}</h1>
        <p style='color: #64748b; font-size: 0.85rem; margin:0;'>Total Score</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="hero-title">🎮 SELECT YOUR GAME</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8; margin-bottom:3rem;'>Choose a game mode from below and test your skills!</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="game-card">
            <h2 style='margin-top:0;'>🔢 Number Guessing Game</h2>
            <p style='color:#94a3b8; font-size:0.95rem; line-height:1.5;'>Guess the secret number within a given range. Choose your difficulty level to earn more bonus points.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("PLAY NUMBER GUESSING", key="btn_num"):
            reset_game_state()
            st.session_state.page = "number_game"
            st.rerun()
            
        st.markdown("""
        <div class="game-card" style='margin-top: 1.8rem;'>
            <h2 style='margin-top:0;'>🔐 Code Breaker</h2>
            <p style='color:#94a3b8; font-size:0.95rem; line-height:1.5;'>Crack the secret 4-digit combination. Use the position feedback clues to find the correct pattern.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("PLAY CODE BREAKER", key="btn_code"):
            reset_game_state()
            st.session_state.page = "code_breaker"
            st.rerun()
            
    with col2:
        st.markdown("""
        <div class="game-card">
            <h2 style='margin-top:0;'>📝 Word Guessing Game</h2>
            <p style='color:#94a3b8; font-size:0.95rem; line-height:1.5;'>Find the hidden word. Type words with the same length and get hints on correctly placed letters.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("PLAY WORD GUESSING", key="btn_word"):
            reset_game_state()
            st.session_state.page = "word_game"
            st.rerun()
            
        st.markdown("""
        <div class="game-card" style='margin-top: 1.8rem;'>
            <h2 style='margin-top:0;'>📊 Player Statistics</h2>
            <p style='color:#94a3b8; font-size:0.95rem; line-height:1.5;'>Check your total games played, total wins, performance history, and unlocked game achievements.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("VIEW STATISTICS", key="btn_stats"):
            st.session_state.page = "stats"
            st.rerun()

def number_game_page():
    apply_modern_theme()
    st.markdown('<h1 class="hero-title">🔢 NUMBER GUESSING GAME</h1>', unsafe_allow_html=True)
    
    if not st.session_state.game_started:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>Select Difficulty Level</h3>", unsafe_allow_html=True)
        difficulty = st.radio(
            "Options:",
            ["Easy Range (1-50) | 5x Multiplier", "Medium Range (1-100) | 10x Multiplier", "Hard Range (1-500) | 20x Multiplier"],
            horizontal=False
        )
        diff_map = {
            "Easy Range (1-50) | 5x Multiplier": "easy",
            "Medium Range (1-100) | 10x Multiplier": "medium",
            "Hard Range (1-500) | 20x Multiplier": "hard"
        }
        
        if st.button("START GAME"):
            number_guessing_game(diff_map[difficulty])
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        low, high, max_att, points = number_guessing_game(None)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>NUMBER RANGE</small><h2 style='margin:0.2rem 0 0 0;'>{low} to {high}</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>ATTEMPTS LEFT</small><h2 style='margin:0.2rem 0 0 0;'>{'Unlimited' if max_att == float('inf') else st.session_state.attempts_left}</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>SCORE VALUE</small><h2 style='margin:0.2rem 0 0 0; color:#a78bfa;'>{points} Points</h2></div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.form(key="num_game_submission_form", clear_on_submit=False):
            guess = st.number_input("Enter your guess:", min_value=low, max_value=high, step=1, key="num_specimen_input")
            submit = st.form_submit_button("SUBMIT GUESS")
            
        if submit:
            result = check_number_guess(guess)
            if result[0] == "win":
                record_game_result(True, result[2], "Number Game")
                st.balloons()
                st.markdown(f"<div class='success-banner'>🎉 CONGRATULATIONS! You guessed it right. Earned {result[2]} points.</div>", unsafe_allow_html=True)
                time.sleep(1)
                reset_game_state()
                st.session_state.page = "main_menu"
                st.rerun()
            elif result[0] == "lose":
                record_game_result(False, 0, "Number Game")
                st.markdown(f"<div class='error-banner'>💀 GAME OVER! You ran out of attempts. The correct number was: {result[1]}</div>", unsafe_allow_html=True)
                time.sleep(1)
                reset_game_state()
                st.session_state.page = "main_menu"
                st.rerun()
            else:
                if result[1] == "too_low":
                    st.warning(f"📉 TOO LOW: Try a higher number! {result[2]}")
                else:
                    st.warning(f"📈 TOO HIGH: Try a lower number! {result[2]}")
                    
        if st.button("QUIT TO MAIN MENU", use_container_width=True):
            reset_game_state()
            st.session_state.page = "main_menu"
            st.rerun()

def word_game_page():
    apply_modern_theme()
    st.markdown('<h1 class="hero-title">📝 WORD GUESSING GAME</h1>', unsafe_allow_html=True)
    
    secret_word, attempts = word_guessing_game()
    
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>WORD LENGTH</small><h2 style='margin:0.2rem 0 0 0;'>{len(secret_word)} Letters</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>ATTEMPTS REMAINING</small><h2 style='margin:0.2rem 0 0 0;'>{attempts} Left</h2></div>", unsafe_allow_html=True)
    
    st.markdown('<div class="game-card" style="margin-top:1.5rem;">', unsafe_allow_html=True)
    st.markdown(f'<div class="hint-banner">{st.session_state.word_hint if st.session_state.word_hint else "• " * len(secret_word)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.form(key="word_game_submission_form"):
        guess = st.text_input("Type your word here:", max_chars=len(secret_word), key="word_character_input").upper()
        submit = st.form_submit_button("SUBMIT WORD")
        
    if submit:
        if len(guess) != len(secret_word) or not guess.isalpha():
            st.error(f"Invalid input: Your guess must be exactly {len(secret_word)} letters long.")
        else:
            result = check_word_guess(guess)
            if result[0] == "win":
                record_game_result(True, 20, "Word Game")
                st.balloons()
                st.markdown("<div class='success-banner'>🎉 EXCELLENT! You found the hidden word. (+20 Score).</div>", unsafe_allow_html=True)
                time.sleep(1)
                reset_game_state()
                st.session_state.page = "main_menu"
                st.rerun()
            elif result[0] == "lose":
                record_game_result(False, 0, "Word Game")
                st.markdown(f"<div class='error-banner'>💀 GAME OVER! Out of moves. The correct word was: {result[1]}</div>", unsafe_allow_html=True)
                time.sleep(1)
                reset_game_state()
                st.session_state.page = "main_menu"
                st.rerun()
            else:
                st.session_state.word_hint = result[1]
                st.rerun()

    if st.button("QUIT TO MAIN MENU", use_container_width=True):
        reset_game_state()
        st.session_state.page = "main_menu"
        st.rerun()

def code_breaker_page():
    apply_modern_theme()
    st.markdown('<h1 class="hero-title">🔐 CODE BREAKER PROTOCOL</h1>', unsafe_allow_html=True)
    
    secret_code, attempts = code_breaker_game()
    st.markdown(f"<div class='stat-block' style='max-width:300px; margin:0 auto 1.5rem auto;'><small style='color:#64748b;'>ATTEMPTS USED</small><h2 style='margin:0;'>{attempts} / 10</h2></div>", unsafe_allow_html=True)
    
    if st.session_state.code_history:
        st.markdown("<p style='color:#64748b; margin-bottom:0.3rem; font-weight:600; font-size:0.85rem;'>PREVIOUS GUESS CLUES:</p>", unsafe_allow_html=True)
        for log in st.session_state.code_history[-4:]:
            st.markdown(f"<div style='font-family:monospace; padding:0.5rem 1rem; background:rgba(255,255,255,0.02); border-radius:8px; margin-bottom:0.4rem; border:1px solid rgba(255,255,255,0.03); color:#cbd5e1;'>{log}</div>", unsafe_allow_html=True)
            
    with st.form(key="code_breaker_submission_form"):
        guess = st.text_input("Enter a 4-Digit Code:", max_chars=4, key="code_sequence_input")
        submit = st.form_submit_button("BREAK CODE")
        
    if submit:
        if len(guess) != 4 or not guess.isdigit():
            st.error("Invalid input: Please enter a combination of exactly 4 numbers.")
        else:
            result = check_code_breaker(guess)
            if result[0] == "win":
                record_game_result(True, 30, "Code Breaker")
                st.balloons()
                st.markdown("<div class='success-banner'>🔑 ACCESS GRANTED! You successfully broke the combination code (+30 Score).</div>", unsafe_allow_html=True)
                time.sleep(1)
                reset_game_state()
                st.session_state.page = "main_menu"
                st.rerun()
            elif result[0] == "lose":
                record_game_result(False, 0, "Code Breaker")
                st.markdown(f"<div class='error-banner'>💀 ACCESS DENIED! Lockout triggered. The secret combination code was: {result[1]}</div>", unsafe_allow_html=True)
                time.sleep(1)
                reset_game_state()
                st.session_state.page = "main_menu"
                st.rerun()
            else:
                st.session_state.code_history.append(f"Guess [{guess}] ➡️ {result[1]}")
                st.rerun()

    if st.button("QUIT TO MAIN MENU", use_container_width=True):
        reset_game_state()
        st.session_state.page = "main_menu"
        st.rerun()

def stats_page():
    apply_modern_theme()
    st.markdown('<h1 class="hero-title">📊 PERFORMANCE STATISTICS</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; color:#a78bfa;'>Player Dashboard Summary</h3>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>TOTAL SCORE</small><h2 style='margin:0; color:#60a5fa;'>{st.session_state.total_score}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>GAMES PLAYED</small><h2 style='margin:0;'>{st.session_state.total_games_played}</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>TOTAL WINS</small><h2 style='margin:0; color:#34d399;'>{st.session_state.games_won}</h2></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h3 style="margin-left:0.5rem; margin-bottom:1rem;">🏆 Unlocked Achievements</h3>', unsafe_allow_html=True)
    
    achievements = [
        ("First Blood", st.session_state.games_won >= 1, "Win your very first game"),
        ("Rising Star", st.session_state.games_won >= 3, "Win 3 games successfully"),
        ("Veteran", st.session_state.games_won >= 10, "Win 10 games successfully"),
        ("Point Master", st.session_state.total_score >= 100, "Reach a score of 100+ points"),
        ("Elite Player", st.session_state.total_score >= 500, "Reach a score of 500+ points"),
        ("Number Guru", "Number Game" in st.session_state.game_history, "Win a number guessing game"),
        ("Word Master", "Word Game" in st.session_state.game_history, "Win a word guessing game"),
        ("Code Breaker Elite", "Code Breaker" in st.session_state.game_history, "Win a code breaker game")
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
    
    st.markdown("<div style='margin-top:2.5rem;'></div>", unsafe_allow_html=True)
    if st.button("BACK TO MAIN MENU"):
        st.session_state.page = "main_menu"
        st.rerun()