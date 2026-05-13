import streamlit as st
import time
from utils import show_toast, reset_game_state, record_game_result
from games import (
    number_guessing_game, check_number_guess,
    word_guessing_game, check_word_guess,
    code_breaker_game, check_code_breaker
)

def apply_dark_theme_css():
    """Apply dark theme with neon accents and glassmorphism"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;600;700&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        .stApp {
            background: radial-gradient(circle at 10% 20%, #0a0a0f 0%, #0f0f1a 100%);
            background-attachment: fixed;
        }
        
        /* Animated neon title */
        @keyframes neonPulse {
            0% { text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 20px #0ff, 0 0 30px #0ff; }
            100% { text-shadow: 0 0 2px #fff, 0 0 5px #fff, 0 0 10px #0ff, 0 0 15px #0ff; }
        }
        
        .title-text {
            text-align: center;
            font-size: 56px;
            font-weight: 900;
            font-family: 'Orbitron', monospace;
            background: linear-gradient(135deg, #ff00cc, #3333ff, #00ffcc);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: neonPulse 1.5s ease-in-out infinite alternate;
            margin-bottom: 30px;
            letter-spacing: 3px;
        }
        
        /* Glassmorphic card */
        .game-card {
            background: rgba(20, 20, 35, 0.7);
            backdrop-filter: blur(12px);
            border-radius: 30px;
            padding: 28px 20px;
            margin: 18px 0;
            border: 1px solid rgba(0, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        
        .game-card:hover {
            transform: translateY(-5px);
            border-color: #0ff;
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.3);
        }
        
        /* Stats card with neon border */
        .stats-card {
            background: rgba(10, 10, 25, 0.8);
            backdrop-filter: blur(8px);
            border-radius: 24px;
            padding: 25px 15px;
            color: #fff;
            text-align: center;
            border: 1px solid #ff00cc;
            box-shadow: 0 0 20px rgba(255, 0, 204, 0.2);
            margin: 10px 0;
        }
        
        /* Buttons - neon style */
        .stButton > button {
            background: linear-gradient(90deg, #ff00cc, #3333ff);
            color: white;
            border: none;
            border-radius: 50px;
            padding: 12px 28px;
            font-weight: bold;
            font-size: 16px;
            transition: 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
            width: 100%;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 20px #0ff, 0 0 30px #ff00cc;
            background: linear-gradient(90deg, #ff3399, #4444ff);
        }
        
        /* Success/Error messages */
        .success-message {
            background: linear-gradient(135deg, #00b4db, #0083b0);
            padding: 18px;
            border-radius: 20px;
            text-align: center;
            font-weight: bold;
            font-size: 18px;
            animation: slideIn 0.5s;
            box-shadow: 0 0 20px #00b4db;
            color: #fff;
        }
        
        .error-message {
            background: linear-gradient(135deg, #ff416c, #ff4b2b);
            padding: 18px;
            border-radius: 20px;
            text-align: center;
            font-weight: bold;
            color: white;
            animation: shake 0.5s;
            box-shadow: 0 0 20px #ff416c;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-50px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes shake {
            0%,100% { transform: translateX(0); }
            25% { transform: translateX(-8px); }
            75% { transform: translateX(8px); }
        }
        
        /* Input fields */
        .stNumberInput input, .stTextInput input {
            background: rgba(20, 20, 40, 0.9);
            border: 1px solid #0ff;
            border-radius: 50px;
            padding: 10px 20px;
            color: #0ff;
            font-size: 16px;
        }
        
        .stNumberInput input:focus, .stTextInput input:focus {
            border-color: #ff00cc;
            box-shadow: 0 0 15px #ff00cc;
        }
        
        /* Metrics */
        .stMetric {
            background: rgba(0,0,0,0.5);
            padding: 15px;
            border-radius: 20px;
            text-align: center;
            border: 1px solid #0ff;
        }
        .stMetric label, .stMetric div {
            color: #0ff !important;
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background: linear-gradient(90deg, #ff00cc, #0ff);
            border-radius: 20px;
        }
        
        /* Sidebar */
        .css-1d391kg, .css-12oz5g0 {
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(16px);
        }
        
        /* Radio buttons */
        .stRadio > div {
            background: rgba(0,0,0,0.5);
            padding: 15px;
            border-radius: 20px;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #888;
            margin-top: 50px;
            padding: 20px;
            font-size: 14px;
        }
        
        /* Achievement badges */
        .achievement-badge {
            background: linear-gradient(135deg, #f5af19, #f12711);
            border-radius: 20px;
            padding: 15px;
            margin: 8px;
            color: white;
            text-align: center;
            font-weight: bold;
            transition: 0.3s;
            box-shadow: 0 0 15px rgba(245,175,25,0.5);
        }
        
        /* Info box */
        .info-box {
            background: rgba(0, 255, 255, 0.1);
            border-left: 5px solid #0ff;
            padding: 15px 20px;
            border-radius: 15px;
            margin: 10px 0;
            color: #fff;
        }
    </style>
    """, unsafe_allow_html=True)

def login_page():
    apply_dark_theme_css()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<p class="title-text">🎮 ULTIMATE GUESSING GAME 🎮</p>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="game-card">', unsafe_allow_html=True)
            st.markdown("### 🌟 Welcome, Adventurer! 🌟")
            st.markdown("---")
            st.markdown("#### Enter your name to begin your quest:")
            name = st.text_input("", key="login_name", placeholder="Your epic name here...", label_visibility="collapsed")
            if st.button("🚀 START ADVENTURE", use_container_width=True):
                if name and name.strip():
                    st.session_state.player_name = name.strip()
                    st.session_state.page = "main_menu"
                    show_toast(f"Welcome, {name}! Your adventure awaits! ✨", "success")
                    st.rerun()
                else:
                    show_toast("Please enter a name to continue!", "warning")
            st.markdown('</div>', unsafe_allow_html=True)

def main_menu():
    apply_dark_theme_css()
    # Sidebar stats
    st.sidebar.markdown(f"""
    <div class='stats-card'>
        <h2>👤 {st.session_state.player_name}</h2>
        <hr>
        <h1 style='font-size: 48px;'>🏆 {st.session_state.total_score}</h1>
        <p>Total Score</p>
        <h3>🎮 {st.session_state.games_won}</h3>
        <p>Games Won</p>
        <p>📊 {st.session_state.total_games_played}</p>
        <p>Total Games</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.total_games_played > 0:
        win_rate = (st.session_state.games_won / st.session_state.total_games_played) * 100
        st.sidebar.markdown(f"""
        <div class='info-box'>
            📈 Win Rate: {win_rate:.1f}%<br>
            ⭐ Level: {min(99, st.session_state.total_score // 100 + 1)}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<p class="title-text">🎯 CHOOSE YOUR CHALLENGE 🎯</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown('<div class="game-card">', unsafe_allow_html=True)
            st.markdown("### 🔢 NUMBER GUESSING")
            st.markdown("*Test your intuition and guessing skills!*")
            st.markdown("**Points:** 5-20 | **Difficulty:** Selectable")
            if st.button("🎲 Play Number Game", use_container_width=True):
                reset_game_state()
                st.session_state.page = "number_game"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="game-card">', unsafe_allow_html=True)
            st.markdown("### 🔐 CODE BREAKER")
            st.markdown("*Crack the secret 4-digit code!*")
            st.markdown("**Points:** 30 | **Attempts:** 10")
            if st.button("🔓 Play Code Breaker", use_container_width=True):
                reset_game_state()
                st.session_state.page = "code_breaker"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="game-card">', unsafe_allow_html=True)
            st.markdown("### 📝 WORD GUESSING")
            st.markdown("*Expand your vocabulary!*")
            st.markdown("**Points:** 20 | **Attempts:** 6")
            if st.button("📖 Play Word Game", use_container_width=True):
                reset_game_state()
                st.session_state.page = "word_game"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="game-card">', unsafe_allow_html=True)
            st.markdown("### 📊 STATISTICS & ACHIEVEMENTS")
            st.markdown("*View your progress and earned badges!*")
            if st.button("🏆 View Stats", use_container_width=True):
                st.session_state.page = "stats"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    colb1, colb2, colb3 = st.columns([1,2,1])
    with colb2:
        if st.button("🚪 Exit Game", use_container_width=True):
            st.balloons()
            st.markdown('<div class="success-message">Thanks for playing! Come back soon! 👋</div>', unsafe_allow_html=True)
            time.sleep(2)
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            from utils import init_session_state
            init_session_state()
            st.rerun()
    
    st.markdown('<div class="footer">🎮 Made with Streamlit | Challenge your mind! 🎮</div>', unsafe_allow_html=True)

def number_game_page():
    apply_dark_theme_css()
    st.markdown('<p class="title-text">🔢 NUMBER GUESSING CHALLENGE</p>', unsafe_allow_html=True)
    
    if not st.session_state.game_started:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.markdown("### Select Your Difficulty")
        difficulty = st.radio(
            "",
            ["🌿 Easy (1-50, ∞ attempts, 5 pts)", 
             "⚡ Medium (1-100, 10 attempts, 10 pts)", 
             "🔥 Hard (1-500, 5 attempts, 20 pts)"],
            horizontal=True,
            label_visibility="collapsed"
        )
        if "Easy" in difficulty:
            diff = "easy"
        elif "Medium" in difficulty:
            diff = "medium"
        else:
            diff = "hard"
        if st.button("🎯 Start Game", use_container_width=True):
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
        
        if max_att != float('inf'):
            progress = ((max_att - st.session_state.attempts_left) / max_att)
            st.progress(progress)
        
        with st.form(key="number_form"):
            guess = st.number_input("Enter your guess:", min_value=low, max_value=high, step=1, key="num_guess")
            submitted = st.form_submit_button("🔍 Submit Guess", use_container_width=True)
            if submitted:
                result = check_number_guess(guess)
                if result[0] == "win":
                    record_game_result(True, result[2], "Number Game")
                    st.balloons()
                    st.markdown(f"""
                    <div class='success-message'>
                        🎉 PERFECT! You guessed it in {result[1]} tries!<br>
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
                        💀 GAME OVER! The number was {result[1]} 💀
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
        
        if st.button("🏳️ Give Up", use_container_width=True):
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
    apply_dark_theme_css()
    st.markdown('<p class="title-text">📝 WORD GUESSING CHALLENGE</p>', unsafe_allow_html=True)
    
    if not st.session_state.game_started:
        word_guessing_game()
        st.rerun()
    
    secret_word, attempts = word_guessing_game()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Word Length", len(secret_word))
    with col2:
        st.metric("Attempts Left", attempts)
    
    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    if st.session_state.word_hint:
        st.markdown(f"### 📍 Current Progress:\n{st.session_state.word_hint}")
    else:
        st.markdown(f"### 📍 Current Progress:\n{'❓ ' * len(secret_word)}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.form(key="word_form"):
        guess = st.text_input("Enter your guess:", max_chars=len(secret_word), key="word_guess", placeholder=f"Enter {len(secret_word)} letters").upper()
        submitted = st.form_submit_button("📝 Check Word", use_container_width=True)
        if submitted:
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
                        🎉 EXCELLENT! The word was {result[1]}!<br>
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
                        💀 GAME OVER! The word was {result[1]} 💀
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    reset_game_state()
                    st.session_state.page = "main_menu"
                    st.rerun()
                else:
                    st.session_state.word_hint = result[1]
                    st.info(f"🔍 HINT: {result[1]}")
                    st.warning(f"📊 Attempts left: {result[2]}")
                    st.rerun()
    
    if st.button("🏳️ Give Up", use_container_width=True):
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
    apply_dark_theme_css()
    st.markdown('<p class="title-text">🔐 CODE BREAKER CHALLENGE</p>', unsafe_allow_html=True)
    
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
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.markdown("### 📜 Guess History")
        for item in st.session_state.code_history[-5:]:
            st.code(item, language="text")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.form(key="code_form"):
        guess = st.text_input("Enter 4-digit code:", max_chars=4, key="code_guess", placeholder="e.g., 1234")
        submitted = st.form_submit_button("🔐 Crack Code", use_container_width=True)
        if submitted:
            if len(guess) != 4 or not guess.isdigit():
                st.warning("Please enter exactly 4 digits (0-9)!")
            else:
                result = check_code_breaker(guess)
                if result[0] == "win":
                    record_game_result(True, 30, "Code Breaker")
                    st.balloons()
                    st.markdown(f"""
                    <div class='success-message'>
                        🎉 ACCESS GRANTED! The code was {result[1]}!<br>
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
                        🔒 SYSTEM LOCKED! The code was {result[1]} 🔒
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    reset_game_state()
                    st.session_state.page = "main_menu"
                    st.rerun()
                else:
                    st.session_state.code_history.append(f"{guess} → {result[1]}")
                    st.info(f"🔍 HINT: {result[1]}")
                    st.warning(f"📊 Attempts left: {result[2]}")
                    st.rerun()
    
    if st.button("🏳️ Give Up", use_container_width=True):
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
    apply_dark_theme_css()
    st.markdown('<p class="title-text">📊 PLAYER STATISTICS</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.markdown(f"### 👤 {st.session_state.player_name}")
        st.markdown(f"### 🏆 Total Score: {st.session_state.total_score}")
        st.markdown(f"### 🎮 Games Won: {st.session_state.games_won}")
        st.markdown(f"### 📊 Total Games: {st.session_state.total_games_played}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
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
    st.markdown("### 🏅 ACHIEVEMENTS")
    
    achievements = [
        ("🎯 First Blood", st.session_state.games_won >= 1, "Win your first game"),
        ("⭐ Rising Star", st.session_state.games_won >= 3, "Win 3 games"),
        ("🏅 Veteran", st.session_state.games_won >= 10, "Win 10 games"),
        ("💰 Point Master", st.session_state.total_score >= 100, "Score 100+ points"),
        ("💎 Elite Player", st.session_state.total_score >= 500, "Score 500+ points"),
        ("🔢 Number Guru", "Number Game" in st.session_state.game_history, "Win number game"),
        ("📝 Word Master", "Word Game" in st.session_state.game_history, "Win word game"),
        ("🔐 Code Breaker Elite", "Code Breaker" in st.session_state.game_history, "Win code breaker")
    ]
    
    cols = st.columns(3)
    for idx, (achievement, unlocked, description) in enumerate(achievements):
        with cols[idx % 3]:
            if unlocked:
                st.markdown(f"""
                <div class='achievement-badge' style='background: linear-gradient(135deg, #00b4db, #0083b0); animation: none;'>
                    ✅ {achievement}<br>
                    <small>{description}</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='achievement-badge' style='background: linear-gradient(135deg, #667eea, #764ba2); opacity: 0.5; animation: none;'>
                    🔒 {achievement}<br>
                    <small>{description}</small>
                </div>
                """, unsafe_allow_html=True)
    
    if st.button("◀ Back to Main Menu", use_container_width=True):
        st.session_state.page = "main_menu"
        st.rerun()