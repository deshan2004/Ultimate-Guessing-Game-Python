import streamlit as st
import random
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Ultimate Guessing Game",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card styling */
    .game-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        transition: transform 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        animation: fadeIn 0.5s;
    }
    
    /* Error message */
    .error-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        color: white;
    }
    
    /* Title animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .title-text {
        animation: fadeIn 0.8s ease-out;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px;
        font-weight: bold;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(255, 255, 255, 0.9);
        border-left: 4px solid #667eea;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    /* Achievement badges */
    .achievement-badge {
        background: linear-gradient(135deg, #f5af19 0%, #f12711 100%);
        border-radius: 20px;
        padding: 10px;
        margin: 5px;
        color: white;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'player_name' not in st.session_state:
        st.session_state.player_name = ""
    if 'total_score' not in st.session_state:
        st.session_state.total_score = 0
    if 'games_won' not in st.session_state:
        st.session_state.games_won = 0
    if 'game_history' not in st.session_state:
        st.session_state.game_history = []
    if 'page' not in st.session_state:
        st.session_state.page = "login"
    if 'current_game' not in st.session_state:
        st.session_state.current_game = None
    if 'secret_number' not in st.session_state:
        st.session_state.secret_number = None
    if 'attempts_left' not in st.session_state:
        st.session_state.attempts_left = 0
    if 'num_tries' not in st.session_state:
        st.session_state.num_tries = 0
    if 'secret_word' not in st.session_state:
        st.session_state.secret_word = None
    if 'word_attempts' not in st.session_state:
        st.session_state.word_attempts = 0
    if 'secret_code' not in st.session_state:
        st.session_state.secret_code = None
    if 'code_attempts' not in st.session_state:
        st.session_state.code_attempts = 0
    if 'code_history' not in st.session_state:
        st.session_state.code_history = []
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = None
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

init_session_state()

# Helper functions
def update_stats():
    """Update player statistics display"""
    st.session_state.total_score = st.session_state.total_score
    st.session_state.games_won = st.session_state.games_won

def show_toast(message, type="success"):
    """Show a toast notification"""
    if type == "success":
        st.success(message)
    elif type == "error":
        st.error(message)
    elif type == "warning":
        st.warning(message)
    else:
        st.info(message)
    time.sleep(0.5)

# Game functions
def number_guessing_game(difficulty):
    """Number guessing game implementation"""
    if not st.session_state.game_started:
        # Set game parameters based on difficulty
        if difficulty == "easy":
            low, high, max_att, points = 1, 50, float('inf'), 5
        elif difficulty == "medium":
            low, high, max_att, points = 1, 100, 10, 10
        else:  # hard
            low, high, max_att, points = 1, 500, 5, 20
        
        st.session_state.secret_number = random.randint(low, high)
        st.session_state.attempts_left = max_att
        st.session_state.num_tries = 0
        st.session_state.num_points = points
        st.session_state.game_started = True
        st.session_state.number_range = (low, high)
        st.session_state.max_attempts = max_att
        
        return low, high, max_att, points
    
    return st.session_state.number_range[0], st.session_state.number_range[1], st.session_state.max_attempts, st.session_state.num_points

def check_number_guess(guess):
    """Check number guess and return result"""
    st.session_state.num_tries += 1
    
    if st.session_state.attempts_left != float('inf'):
        st.session_state.attempts_left -= 1
    
    if guess == st.session_state.secret_number:
        st.session_state.total_score += st.session_state.num_points
        st.session_state.games_won += 1
        st.session_state.game_history.append("Number Game")
        return "win", st.session_state.num_tries, st.session_state.num_points
    elif st.session_state.attempts_left == 0:
        return "lose", st.session_state.secret_number, 0
    else:
        hint = "too_low" if guess < st.session_state.secret_number else "too_high"
        diff = abs(guess - st.session_state.secret_number)
        
        if diff > 100:
            message = "Way off! 🎯"
        elif diff > 50:
            message = "Getting warmer 🌡️"
        elif diff > 20:
            message = "You're close! 🎯"
        else:
            message = "Very close! 🔥"
        
        return "continue", hint, message, st.session_state.attempts_left

def word_guessing_game():
    """Word guessing game implementation"""
    word_list = ["PYTHON", "ALGORITHM", "VARIABLE", "FUNCTION", "COMPILER", 
                 "DEBUGGER", "ITERATOR", "DICTIONARY", "MODULE", "PACKAGE"]
    
    if not st.session_state.game_started:
        st.session_state.secret_word = random.choice(word_list)
        st.session_state.word_attempts = 6
        st.session_state.game_started = True
    
    return st.session_state.secret_word, st.session_state.word_attempts

def check_word_guess(guess):
    """Check word guess and return result"""
    st.session_state.word_attempts -= 1
    
    if guess == st.session_state.secret_word:
        st.session_state.total_score += 20
        st.session_state.games_won += 1
        st.session_state.game_history.append("Word Game")
        return "win", st.session_state.secret_word
    elif st.session_state.word_attempts <= 0:
        return "lose", st.session_state.secret_word
    else:
        # Generate hint with correct positions
        hint = []
        for i in range(len(st.session_state.secret_word)):
            if i < len(guess) and guess[i] == st.session_state.secret_word[i]:
                hint.append(f"✅{guess[i]}")
            elif i < len(guess) and guess[i] in st.session_state.secret_word:
                hint.append(f"🟡{guess[i]}")
            else:
                hint.append("❓")
        return "continue", " ".join(hint), st.session_state.word_attempts

def code_breaker_game():
    """Code breaker game implementation"""
    if not st.session_state.game_started:
        st.session_state.secret_code = "".join([str(random.randint(0, 9)) for _ in range(4)])
        st.session_state.code_attempts = 10
        st.session_state.code_history = []
        st.session_state.game_started = True
    
    return st.session_state.secret_code, st.session_state.code_attempts

def check_code_breaker(guess):
    """Check code breaker guess and return result"""
    st.session_state.code_attempts -= 1
    
    if guess == st.session_state.secret_code:
        st.session_state.total_score += 30
        st.session_state.games_won += 1
        st.session_state.game_history.append("Code Breaker")
        return "win", st.session_state.secret_code
    elif st.session_state.code_attempts <= 0:
        return "lose", st.session_state.secret_code
    else:
        # Calculate hints
        right_place = sum(1 for i in range(4) if guess[i] == st.session_state.secret_code[i])
        wrong_place = 0
        temp_code = list(st.session_state.secret_code)
        temp_guess = list(guess)
        
        for i in range(4):
            if temp_guess[i] == temp_code[i]:
                temp_code[i] = None
                temp_guess[i] = None
        
        for i in range(4):
            if temp_guess[i] is not None and temp_guess[i] in temp_code:
                wrong_place += 1
                temp_code[temp_code.index(temp_guess[i])] = None
        
        hint_text = f"✅ {right_place} correct spot"
        if wrong_place > 0:
            hint_text += f", 🔄 {wrong_place} wrong spot"
        if right_place == 0 and wrong_place == 0:
            hint_text += " (No matches!)"
        
        return "continue", hint_text, st.session_state.code_attempts

# UI Pages
def login_page():
    """Login/Signup page"""
    st.markdown('<p class="title-text">🎮 ULTIMATE GUESSING GAME 🎮</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.container():
            st.markdown('<div class="game-card">', unsafe_allow_html=True)
            st.markdown("### 🌟 Welcome, Adventurer! 🌟")
            st.markdown("---")
            
            name = st.text_input("Enter your name to begin:", key="login_name", placeholder="Your awesome name here...")
            
            colb1, colb2, colb3 = st.columns([1,2,1])
            with colb2:
                if st.button("🚀 START ADVENTURE", use_container_width=True):
                    if name and name.strip():
                        st.session_state.player_name = name.strip()
                        st.session_state.page = "main_menu"
                        show_toast(f"✨ Welcome, {name}! Let the games begin! ✨")
                        st.rerun()
                    else:
                        show_toast("Please enter your name!", "warning")
            st.markdown('</div>', unsafe_allow_html=True)

def main_menu():
    """Main menu page"""
    st.sidebar.markdown(f"""
    <div class='stats-card'>
        <h3>👤 {st.session_state.player_name}</h3>
        <hr>
        <h2>🏆 {st.session_state.total_score}</h2>
        <p>Total Score</p>
        <h3>🎮 {st.session_state.games_won}</h3>
        <p>Games Won</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate win rate
    if st.session_state.games_won > 0:
        win_rate = (st.session_state.games_won / (st.session_state.games_won + 5)) * 100
        st.sidebar.markdown(f"""
        <div class='info-box'>
            📈 Win Rate: {win_rate:.1f}%
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<p class="title-text">🎯 CHOOSE YOUR CHALLENGE 🎯</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown('<div class="game-card">', unsafe_allow_html=True)
            st.markdown("### 🔢 NUMBER GUESSING")
            st.markdown("Test your intuition and guessing skills!")
            st.markdown("**Points:** 5-20 | **Difficulty:** Selectable")
            if st.button("🎲 Play Number Game", use_container_width=True):
                st.session_state.page = "number_game"
                st.session_state.game_started = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="game-card">', unsafe_allow_html=True)
            st.markdown("### 🔐 CODE BREAKER")
            st.markdown("Crack the secret 4-digit code!")
            st.markdown("**Points:** 30 | **Attempts:** 10")
            if st.button("🔓 Play Code Breaker", use_container_width=True):
                st.session_state.page = "code_breaker"
                st.session_state.game_started = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="game-card">', unsafe_allow_html=True)
            st.markdown("### 📝 WORD GUESSING")
            st.markdown("Expand your vocabulary!")
            st.markdown("**Points:** 20 | **Attempts:** 6")
            if st.button("📖 Play Word Game", use_container_width=True):
                st.session_state.page = "word_game"
                st.session_state.game_started = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="game-card">', unsafe_allow_html=True)
            st.markdown("### 📊 STATISTICS & ACHIEVEMENTS")
            st.markdown("View your progress and earned badges!")
            if st.button("🏆 View Stats", use_container_width=True):
                st.session_state.page = "stats"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Bottom buttons
    colb1, colb2, colb3 = st.columns(3)
    with colb2:
        if st.button("🚪 Exit Game", use_container_width=True):
            st.balloons()
            st.markdown('<div class="success-message">Thanks for playing! Come back soon! 👋</div>', unsafe_allow_html=True)
            time.sleep(2)
            st.session_state.page = "login"
            st.rerun()

def number_game_page():
    """Number guessing game page"""
    st.markdown('<p class="title-text">🔢 NUMBER GUESSING CHALLENGE</p>', unsafe_allow_html=True)
    
    if not st.session_state.game_started:
        # Difficulty selection
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.markdown("### Select Difficulty")
        
        difficulty = st.radio(
            "Choose your challenge level:",
            ["🌿 Easy (1-50, ∞ attempts, 5 pts)", 
             "⚡ Medium (1-100, 10 attempts, 10 pts)", 
             "🔥 Hard (1-500, 5 attempts, 20 pts)"],
            horizontal=True
        )
        
        if "Easy" in difficulty:
            diff = "easy"
        elif "Medium" in difficulty:
            diff = "medium"
        else:
            diff = "hard"
        
        if st.button("🎯 Start Game", use_container_width=True):
            low, high, max_att, points = number_guessing_game(diff)
            show_toast(f"Game started! Guess between {low} and {high}")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        low, high, max_att, points = number_guessing_game(None)
        
        # Game info
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
        
        # Progress bar for limited attempts
        if max_att != float('inf'):
            progress = ((max_att - st.session_state.attempts_left) / max_att) * 100
            st.progress(progress / 100)
        
        # Guess input
        guess = st.number_input("Enter your guess:", min_value=low, max_value=high, step=1, key="num_guess")
        
        colb1, colb2 = st.columns(2)
        with colb1:
            if st.button("🔍 Submit Guess", use_container_width=True):
                result = check_number_guess(guess)
                
                if result[0] == "win":
                    st.balloons()
                    st.markdown(f"""
                    <div class='success-message'>
                        🎉 PERFECT! You guessed it in {result[1]} tries!<br>
                        +{result[2]} points added!<br>
                        Total Score: {st.session_state.total_score}
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    st.session_state.game_started = False
                    st.session_state.page = "main_menu"
                    st.rerun()
                elif result[0] == "lose":
                    st.markdown(f"""
                    <div class='error-message'>
                        💀 GAME OVER! The number was {result[1]} 💀
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    st.session_state.game_started = False
                    st.session_state.page = "main_menu"
                    st.rerun()
                else:
                    if result[1] == "too_low":
                        st.warning(f"📉 Too Low! {result[2]}")
                    else:
                        st.warning(f"📈 Too High! {result[2]}")
                    st.rerun()
        
        with colb2:
            if st.button("🏳️ Give Up", use_container_width=True):
                st.session_state.game_started = False
                st.session_state.page = "main_menu"
                st.rerun()

def word_game_page():
    """Word guessing game page"""
    st.markdown('<p class="title-text">📝 WORD GUESSING CHALLENGE</p>', unsafe_allow_html=True)
    
    if not st.session_state.game_started:
        word_guessing_game()
        st.rerun()
    
    secret_word, attempts = word_guessing_game()
    
    # Game info
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Word Length", len(secret_word))
    with col2:
        st.metric("Attempts Left", attempts)
    
    # Display word progress
    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    if hasattr(st.session_state, 'word_hint'):
        st.markdown(f"### Current Progress:\n{st.session_state.word_hint}")
    else:
        st.markdown(f"### Current Progress:\n{'❓ ' * len(secret_word)}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Guess input
    guess = st.text_input("Enter your guess:", max_chars=len(secret_word), key="word_guess").upper()
    
    colb1, colb2 = st.columns(2)
    with colb1:
        if st.button("📝 Check Word", use_container_width=True):
            if len(guess) != len(secret_word):
                st.warning(f"Please enter exactly {len(secret_word)} letters!")
            elif not guess.isalpha():
                st.warning("Please enter only letters!")
            else:
                result = check_word_guess(guess)
                
                if result[0] == "win":
                    st.balloons()
                    st.markdown(f"""
                    <div class='success-message'>
                        🎉 EXCELLENT! The word was {result[1]}!<br>
                        +20 points!<br>
                        Total Score: {st.session_state.total_score}
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    st.session_state.game_started = False
                    st.session_state.page = "main_menu"
                    st.rerun()
                elif result[0] == "lose":
                    st.markdown(f"""
                    <div class='error-message'>
                        💀 GAME OVER! The word was {result[1]} 💀
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    st.session_state.game_started = False
                    st.session_state.page = "main_menu"
                    st.rerun()
                else:
                    st.session_state.word_hint = result[1]
                    st.info(f"HINT: {result[1]}")
                    st.warning(f"Attempts left: {result[2]}")
                    st.rerun()
    
    with colb2:
        if st.button("🏳️ Give Up", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.page = "main_menu"
            st.rerun()

def code_breaker_page():
    """Code breaker game page"""
    st.markdown('<p class="title-text">🔐 CODE BREAKER CHALLENGE</p>', unsafe_allow_html=True)
    
    if not st.session_state.game_started:
        code_breaker_game()
        st.rerun()
    
    secret_code, attempts = code_breaker_game()
    
    # Game info
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Code Length", "4 digits")
    with col2:
        st.metric("Attempts Left", attempts)
    
    # Guess input
    guess = st.text_input("Enter 4-digit code:", max_chars=4, key="code_guess", placeholder="e.g., 1234")
    
    # Display history
    if st.session_state.code_history:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.markdown("### 📜 Guess History")
        for item in st.session_state.code_history[-5:]:  # Show last 5
            st.text(item)
        st.markdown('</div>', unsafe_allow_html=True)
    
    colb1, colb2 = st.columns(2)
    with colb1:
        if st.button("🔐 Crack Code", use_container_width=True):
            if len(guess) != 4 or not guess.isdigit():
                st.warning("Please enter exactly 4 digits (0-9)!")
            else:
                result = check_code_breaker(guess)
                
                if result[0] == "win":
                    st.balloons()
                    st.markdown(f"""
                    <div class='success-message'>
                        🎉 ACCESS GRANTED! The code was {result[1]}!<br>
                        +30 points!<br>
                        Total Score: {st.session_state.total_score}
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    st.session_state.game_started = False
                    st.session_state.page = "main_menu"
                    st.rerun()
                elif result[0] == "lose":
                    st.markdown(f"""
                    <div class='error-message'>
                        🔒 SYSTEM LOCKED! The code was {result[1]} 🔒
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
                    st.session_state.game_started = False
                    st.session_state.page = "main_menu"
                    st.rerun()
                else:
                    st.session_state.code_history.append(f"{guess} → {result[1]}")
                    st.info(f"HINT: {result[1]}")
                    st.warning(f"Attempts left: {result[2]}")
                    st.rerun()
    
    with colb2:
        if st.button("🏳️ Give Up", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.page = "main_menu"
            st.rerun()

def stats_page():
    """Statistics and achievements page"""
    st.markdown('<p class="title-text">📊 PLAYER STATISTICS</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.markdown(f"### 👤 {st.session_state.player_name}")
        st.markdown(f"### 🏆 Total Score: {st.session_state.total_score}")
        st.markdown(f"### 🎮 Games Won: {st.session_state.games_won}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        if st.session_state.games_won > 0:
            win_rate = (st.session_state.games_won / (st.session_state.games_won + 5)) * 100
            st.markdown(f"### 📈 Win Rate: {win_rate:.1f}%")
            next_level = 50 - (st.session_state.total_score % 50)
            st.markdown(f"### ⭐ Next level in {next_level} points")
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
                <div class='achievement-badge' style='background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);'>
                    ✅ {achievement}<br>
                    <small>{description}</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='achievement-badge' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); opacity: 0.5;'>
                    🔒 {achievement}<br>
                    <small>{description}</small>
                </div>
                """, unsafe_allow_html=True)
    
    if st.button("◀ Back to Main Menu", use_container_width=True):
        st.session_state.page = "main_menu"
        st.rerun()

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