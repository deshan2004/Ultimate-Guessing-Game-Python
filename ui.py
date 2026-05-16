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
                radial-gradient(2px 2px at 220px 60px, rgba(167, 139, 250, 0.4), rgba(0,0,0,0)),
                radial-gradient(1.5px 1.5px at 300px 180px, rgba(96, 165, 250, 0.4), rgba(0,0,0,0));
            background-size: 350px 350px;
            background-repeat: repeat;
            animation: spaceFloat 120s linear infinite;
            font-family: 'Inter', sans-serif !important;
        }
        
        @keyframes spaceFloat {
            from { background-position: 0 0; }
            to { background-position: 350px 700px; }
        }
        
        /* Typography overrides */
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
        
        /* Modern Cards styling */
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
        
        /* Dynamic Stats Blocks */
        .stat-block {
            background: linear-gradient(145deg, rgba(20,20,30,0.4) 0%, rgba(10,10,15,0.6) 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-radius: 20px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        /* Form, Input elements custom skinning */
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
        
        /* Premium Buttons */
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
            transition: all 0.4s auto;
            width: 100%;
            box-shadow: 0 10px 25px rgba(99, 102, 241, 0.25) !important;
        }
        
        .stButton > button:hover {
            background-position: right center !important;
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(167, 139, 250, 0.4) !important;
        }
        
        /* Tab bar styling overrides */
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
        
        /* Messages banners custom look */
        .success-banner {
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, rgba(4, 120, 87, 0.2) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 1.2rem; border-radius: 16px; color: #34d399; text-align: center;
            font-weight: 600; font-size: 1.1rem; margin: 1.5rem 0;
            animation: zoomIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
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

def login_page():
    apply_modern_theme()
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown('<h1 class="hero-title">🔮 ARENA ACCESS</h1>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#94a3b8; margin-bottom:2rem;'>Decrypt entry credentials to proceed into the grid.</p>", unsafe_allow_html=True)
        
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔐 Authorization", "📝 Establish Identity"])
        
        with tab1:
            with st.form(key="login_identity_form"):
                username = st.text_input("Player Tag:", placeholder="Enter unique alias...").strip()
                password = st.text_input("Access Cipher:", type="password", placeholder="••••••••")
                submit_login = st.form_submit_button("INITIALIZE INFILTRATION")
                
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
                        st.rerun()
                    else:
                        show_toast("Authorization Refused: Cipher invalid", "error")
                else:
                    show_toast("All inputs required for authentication", "warning")
                        
        with tab2:
            with st.form(key="register_identity_form"):
                reg_username = st.text_input("Register Player Tag:", placeholder="e.g. Neo_X").strip()
                reg_password = st.text_input("Secure Access Cipher:", type="password", placeholder="Min 4 characters")
                reg_password_conf = st.text_input("Verify Cipher:", type="password", placeholder="Retype cipher")
                submit_register = st.form_submit_button("PROVISION CORE PROTOCOL")
                
            if submit_register:
                if reg_username and reg_password and reg_password_conf:
                    if reg_password != reg_password_conf:
                        show_toast("Cipher verification failed: mismatch", "error")
                    elif len(reg_password) < 4:
                        show_toast("Cipher entropy insufficient (Min 4 chars)", "warning")
                    else:
                        from database import create_user
                        success, msg = create_user(reg_username, reg_password)
                        if success:
                            show_toast(f"Protocol established. Proceed to Authorization tab.", "success")
                        else:
                            show_toast(msg, "error")
                else:
                    show_toast("Missing operational parameters for database commit", "warning")
        st.markdown('</div>', unsafe_allow_html=True)

def main_menu():
    apply_modern_theme()
    
    st.sidebar.markdown(f"""
    <div class='stat-block' style='margin-bottom: 1.5rem; border-color: rgba(167, 139, 250, 0.15);'>
        <p style='color: #a78bfa; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px; margin:0;'>Active Profile</p>
        <h3 style='margin: 0.3rem 0 0.8rem 0; font-size:1.6rem;'>{st.session_state.player_name}</h3>
        <hr style='border-color: rgba(255,255,255,0.05); margin: 0.5rem 0;'>
        <h1 style='font-size: 3.2rem; background: linear-gradient(135deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0;'>{st.session_state.total_score}</h1>
        <p style='color: #64748b; font-size: 0.85rem; margin:0;'>Global Credits</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="hero-title">🎮 SELECT OPERATION</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8; margin-bottom:3rem;'>Choose an execution algorithm below to compute intelligence test parameters.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="game-card">
            <h2 style='margin-top:0;'>🔢 Quantizer (Numbers)</h2>
            <p style='color:#94a3b8; font-size:0.95rem; line-height:1.5;'>Reverse-engineer an arbitrary matrix integer within bounds. Adaptive difficulty thresholds shift reward output distribution.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("RUN QUANTIZER PROCESS", key="btn_num"):
            reset_game_state()
            st.session_state.page = "number_game"
            st.rerun()
            
        st.markdown("""
        <div class="game-card" style='margin-top: 1.8rem;'>
            <h2 style='margin-top:0;'>🔐 Codebreaker</h2>
            <p style='color:#94a3b8; font-size:0.95rem; line-height:1.5;'>Intercept 4-slot numerical sequence matrix strings. Positional alignment feedback algorithms are online.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("RUN CODEBREAKER PROTOCOL", key="btn_code"):
            reset_game_state()
            st.session_state.page = "code_breaker"
            st.rerun()
            
    with col2:
        st.markdown("""
        <div class="game-card">
            <h2 style='margin-top:0;'>📝 Lexicon (Words)</h2>
            <p style='color:#94a3b8; font-size:0.95rem; line-height:1.5;'>Deduce structural parameters of masked dictionary arrays. Position feedback indices highlight structural matches.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("RUN LEXICON PIPELINE", key="btn_word"):
            reset_game_state()
            st.session_state.page = "word_game"
            st.rerun()
            
        st.markdown("""
        <div class="game-card" style='margin-top: 1.8rem;'>
            <h2 style='margin-top:0;'>📊 Diagnostics Log</h2>
            <p style='color:#94a3b8; font-size:0.95rem; line-height:1.5;'>Evaluate historical transaction logs, computational victory coefficients, and unlocked identity accolades.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("RUN DATALOG SYSTEM", key="btn_stats"):
            st.session_state.page = "stats"
            st.rerun()

def number_game_page():
    apply_modern_theme()
    st.markdown('<h1 class="hero-title">🔢 QUANTIZER PIPELINE</h1>', unsafe_allow_html=True)
    
    if not st.session_state.game_started:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>Set Matrix Bounds</h3>", unsafe_allow_html=True)
        difficulty = st.radio(
            "Difficulty Settings:",
            ["Standard Range (1-50) | 5x Multiplier", "Extended Range (1-100) | 10x Multiplier", "Core Range (1-500) | 20x Multiplier"],
            horizontal=False
        )
        diff_map = {
            "Standard Range (1-50) | 5x Multiplier": "easy",
            "Extended Range (1-100) | 10x Multiplier": "medium",
            "Core Range (1-500) | 20x Multiplier": "hard"
        }
        
        if st.button("INITIALIZE COMPILATION"):
            number_guessing_game(diff_map[difficulty])
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        low, high, max_att, points = number_guessing_game(None)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>BOUNDS</small><h2 style='margin:0.2rem 0 0 0;'>{low}-{high}</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>ATTEMPTS LEFT</small><h2 style='margin:0.2rem 0 0 0;'>{'∞' if max_att == float('inf') else st.session_state.attempts_left}</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>YIELD POTENTIAL</small><h2 style='margin:0.2rem 0 0 0; color:#a78bfa;'>{points} XP</h2></div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 🌟 FIXED: Form structure and clean conditional flow to fix submit bugs
        with st.form(key="num_game_submission_form", clear_on_submit=False):
            guess = st.number_input("Input Matrix Scalar Specimen:", min_value=low, max_value=high, step=1, key="num_specimen_input")
            submit = st.form_submit_button("TRANSMIT MATRIX SPECI")
            
        if submit:
            result = check_number_guess(guess)
            if result[0] == "win":
                record_game_result(True, result[2], "Number Game")
                st.balloons()
                st.markdown(f"<div class='success-banner'>🎉 DECRYPTION SUCCESSFUL. Yielded {result[2]} Global Credits.</div>", unsafe_allow_html=True)
                time.sleep(2)
                reset_game_state()
                st.session_state.page = "main_menu"
                st.rerun()
            elif result[0] == "lose":
                record_game_result(False, 0, "Number Game")
                st.markdown(f"<div class='error-banner'>💀 OPERATION TERMINATED. Identity core vector was: {result[1]}</div>", unsafe_allow_html=True)
                time.sleep(2)
                reset_game_state()
                st.session_state.page = "main_menu"
                st.rerun()
            else:
                if result[1] == "too_low":
                    st.warning(f"📉 SCALAR DEFICIT: Specimen value is lower than target matrix. {result[2]}")
                else:
                    st.warning(f"📈 SCALAR SURPLUS: Specimen value exceeds target matrix. {result[2]}")
                    
        if st.button("TERMINATE PIPELINE", use_container_width=True):
            reset_game_state()
            st.session_state.page = "main_menu"
            st.rerun()

def word_game_page():
    apply_modern_theme()
    st.markdown('<h1 class="hero-title">📝 LEXICON VECTOR</h1>', unsafe_allow_html=True)
    
    if not st.session_state.game_started:
        word_guessing_game()
        st.rerun()
        
    secret_word, attempts = word_guessing_game()
    
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>VECTOR LENGTH</small><h2 style='margin:0.2rem 0 0 0;'>{len(secret_word)} Units</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>INTEGRITY BUFFER</small><h2 style='margin:0.2rem 0 0 0;'>{attempts} Cyc</h2></div>", unsafe_allow_html=True)
    
    st.markdown('<div class="game-card" style="margin-top:1.5rem;">', unsafe_allow_html=True)
    st.markdown(f'<div class="hint-banner">{st.session_state.word_hint if st.session_state.word_hint else "• " * len(secret_word)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 🌟 FIXED: Clear input state routing and submission structure
    with st.form(key="word_game_submission_form"):
        guess = st.text_input("Transmit Array Characters:", max_chars=len(secret_word), key="word_character_input").upper()
        submit = st.form_submit_button("EXECUTE PARSE LOGIC")
        
    if submit:
        if len(guess) != len(secret_word) or not guess.isalpha():
            st.error(f"Execution Error: Payload must contain precisely {len(secret_word)} linear alphabet nodes.")
        else:
            result = check_word_guess(guess)
            if result[0] == "win":
                record_game_result(True, 20, "Word Game")
                st.balloons()
                st.markdown("<div class='success-banner'>🎉 LEXICON ARRAY RESOLVED. Integrity validated (+20 Credits).</div>", unsafe_allow_html=True)
                time.sleep(2)
                reset_game_state()
                st.session_state.page = "main_menu"
                st.rerun()
            elif result[0] == "lose":
                record_game_result(False, 0, "Word Game")
                st.markdown(f"<div class='error-banner'>💀 DECRYPTION FAIL: Memory registers purged. Sequence was: {result[1]}</div>", unsafe_allow_html=True)
                time.sleep(2)
                reset_game_state()
                st.session_state.page = "main_menu"
                st.rerun()
            else:
                st.session_state.word_hint = result[1]
                st.rerun()

    if st.button("TERMINATE PIPELINE", use_container_width=True):
        reset_game_state()
        st.session_state.page = "main_menu"
        st.rerun()

def code_breaker_page():
    apply_modern_theme()
    st.markdown('<h1 class="hero-title">🔐 CODEBREAKER PROTOCOL</h1>', unsafe_allow_html=True)
    
    if not st.session_state.game_started:
        code_breaker_game()
        st.rerun()
        
    secret_code, attempts = code_breaker_game()
    st.markdown(f"<div class='stat-block' style='max-width:300px; margin:0 auto 1.5rem auto;'><small style='color:#64748b;'>CRACK ATTEMPTS</small><h2 style='margin:0;'>{attempts} / 10</h2></div>", unsafe_allow_html=True)
    
    if st.session_state.code_history:
        st.markdown("<p style='color:#64748b; margin-bottom:0.3rem; font-weight:600; font-size:0.85rem;'>SIGNAL INTERCEPT FEED:</p>", unsafe_allow_html=True)
        for log in st.session_state.code_history[-4:]:
            st.markdown(f"<div style='font-family:monospace; padding:0.5rem 1rem; background:rgba(255,255,255,0.02); border-radius:8px; margin-bottom:0.4rem; border:1px solid rgba(255,255,255,0.03); color:#cbd5e1;'>{log}</div>", unsafe_allow_html=True)
            
    # 🌟 FIXED: Standard form state parameters to prevent UI value losses
    with st.form(key="code_breaker_submission_form"):
        guess = st.text_input("Enter 4-Digit Cipher Sequence:", max_chars=4, key="code_sequence_input")
        submit = st.form_submit_button("INJECT CIPHER PACKET")
        
    if submit:
        if len(guess) != 4 or not guess.isdigit():
            st.error("Execution Error: Core packet structures demand an absolute 4-unit integer layout.")
        else:
            result = check_code_breaker(guess)
            if result[0] == "win":
                record_game_result(True, 30, "Code Breaker")
                st.balloons()
                st.markdown("<div class='success-banner'>🔑 SECURITY LAYER VOIDED. Core access nodes accessible (+30 Credits).</div>", unsafe_allow_html=True)
                time.sleep(2)
                reset_game_state()
                st.session_state.page = "main_menu"
                st.rerun()
            elif result[0] == "lose":
                record_game_result(False, 0, "Code Breaker")
                st.markdown(f"<div class='error-banner'>💀 NODE LOCKOUT: Mainframes isolated. Secret Key was: {result[1]}</div>", unsafe_allow_html=True)
                time.sleep(2)
                reset_game_state()
                st.session_state.page = "main_menu"
                st.rerun()
            else:
                st.session_state.code_history.append(f"Intercept packet [{guess}] ➡️ {result[1]}")
                st.rerun()

    if st.button("TERMINATE PIPELINE", use_container_width=True):
        reset_game_state()
        st.session_state.page = "main_menu"
        st.rerun()

def stats_page():
    apply_modern_theme()
    st.markdown('<h1 class="hero-title">📊 SYSTEM DIAGNOSTICS</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; color:#a78bfa;'>Operational Identity Summary</h3>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>NET SCORE</small><h2 style='margin:0; color:#60a5fa;'>{st.session_state.total_score}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>RUNS INITIATED</small><h2 style='margin:0;'>{st.session_state.total_games_played}</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stat-block'><small style='color:#64748b;'>RESOLVED OPERATIONS</small><h2 style='margin:0; color:#34d399;'>{st.session_state.games_won}</h2></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h3 style="margin-left:0.5rem; margin-bottom:1rem;">🏆 Unlocked Identity Accolades</h3>', unsafe_allow_html=True)
    
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
    
    st.markdown("<div style='margin-top:2.5rem;'></div>", unsafe_allow_html=True)
    if st.button("DISCONNECT DATALOG STREAM"):
        st.session_state.page = "main_menu"
        st.rerun()