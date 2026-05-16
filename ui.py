import streamlit as st
import time
from utils import show_toast, reset_game_state, record_game_result
from games import (
    number_guessing_game, check_number_guess,
    word_guessing_game, check_word_guess,
    code_breaker_game, check_code_breaker
)

def apply_modern_theme():
    """Apply clean, professional styling"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
        }
        
        /* Main container */
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        /* Page title */
        .page-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 2rem;
            letter-spacing: -0.5px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Modern card */
        .modern-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 1.8rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid rgba(0,0,0,0.05);
        }
        
        .modern-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }
        
        /* Stats card */
        .stats-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            padding: 1.5rem;
            color: white;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .stats-card h2, .stats-card h3, .stats-card p {
            color: white;
            margin: 0.5rem 0;
        }
        
        /* Buttons */
        .stButton > button {
            background: #4f46e5;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.2s;
            width: 100%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stButton > button:hover {
            background: #4338ca;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* Input fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            padding: 0.75rem 1rem;
            font-size: 1rem;
            transition: border-color 0.2s;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: #4f46e5;
            box-shadow: 0 0 0 3px rgba(79,70,229,0.1);
        }
        
        /* Metrics */
        .stMetric {
            background: #f9fafb;
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #e5e7eb;
        }
        
        .stMetric label {
            font-weight: 600;
            color: #374151;
        }
        
        .stMetric div {
            font-size: 1.5rem;
            font-weight: 700;
            color: #4f46e5;
        }
        
        /* Success/Error messages */
        .success-message {
            background: #10b981;
            color: white;
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            font-weight: 600;
            margin: 1rem 0;
            animation: slideIn 0.3s;
        }
        
        .error-message {
            background: #ef4444;
            color: white;
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            font-weight: 600;
            margin: 1rem 0;
            animation: slideIn 0.3s;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Info boxes */
        .info-box {
            background: #eff6ff;
            border-left: 4px solid #4f46e5;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            color: #1e293b;
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background: linear-gradient(90deg, #4f46e5, #818cf8);
            border-radius: 20px;
        }
        
        /* Radio buttons */
        .stRadio > div {
            background: #f9fafb;
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
        }
        
        /* Achievement badges */
        .achievement-badge {
            background: linear-gradient(135deg, #fef3c7, #fde68a);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem;
            text-align: center;
            font-weight: 600;
            color: #92400e;
            transition: all 0.2s;
            border: 1px solid #fcd34d;
        }
        
        .achievement-locked {
            background: #f3f4f6;
            border: 1px solid #d1d5db;
            color: #6b7280;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #ffffff;
            margin-top: 3rem;
            padding: 1.5rem;
            font-size: 0.875rem;
            opacity: 0.9;
        }
        
        /* Sidebar */
        .css-1d391kg, .css-12oz5g0 {
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
        }
        
        hr {
            margin: 1rem 0;
            border: none;
            border-top: 1px solid #e5e7eb;
        }
        
        /* Game hint area */
        .game-hint {
            background: #f0fdf4;
            padding: 1rem;
            border-radius: 12px;
            font-family: monospace;
            font-size: 1.1rem;
            text-align: center;
            margin: 1rem 0;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .page-title {
                font-size: 1.8rem;
            }
            .modern-card {
                padding: 1.2rem;
            }
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
            st.markdown("### Welcome, Adventurer!")
            st.markdown("---")
            st.markdown("#### Enter your name to begin:")
            name = st.text_input("", key="login_name", placeholder="Your name...", label_visibility="collapsed")
            if st.button("Start Game", use_container_width=True):
                if name and name.strip():
                    st.session_state.player_name = name.strip()
                    st.session_state.page = "main_menu"
                    show_toast(f"Welcome, {name}! Let the games begin! ✨", "success")
                    st.rerun()
                else:
                    show_toast("Please enter your name to continue!", "warning")
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
        
        with st.form(key="number_form"):
            guess = st.number_input("Enter your guess:", min_value=low, max_value=high, step=1, key="num_guess")
            submitted = st.form_submit_button("Submit Guess", use_container_width=True)
            
            if submitted:
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
        
        if st.button("Give Up", use_container_width=True):
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
    
    with st.form(key="word_form"):
        guess = st.text_input("Enter your guess:", max_chars=len(secret_word), key="word_guess", 
                             placeholder=f"Enter {len(secret_word)} letters").upper()
        submitted = st.form_submit_button("Check Word", use_container_width=True)
        
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
    
    if st.button("Give Up", use_container_width=True):
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
    
    with st.form(key="code_form"):
        guess = st.text_input("Enter 4-digit code:", max_chars=4, key="code_guess", placeholder="e.g., 1234")
        submitted = st.form_submit_button("Crack Code", use_container_width=True)
        
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
    
    if st.button("Give Up", use_container_width=True):
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