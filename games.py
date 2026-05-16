# games.py
import streamlit as st
import random

def number_guessing_game(difficulty):
    """Number guessing game implementation"""
    if not st.session_state.game_started:
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
    return (st.session_state.number_range[0], st.session_state.number_range[1],
            st.session_state.max_attempts, st.session_state.num_points)

def check_number_guess(guess):
    """Check number guess and return result"""
    st.session_state.num_tries += 1
    if st.session_state.attempts_left != float('inf'):
        st.session_state.attempts_left -= 1
    
    if guess == st.session_state.secret_number:
        return "win", st.session_state.num_tries, st.session_state.num_points
    elif st.session_state.attempts_left == 0:
        return "lose", st.session_state.secret_number, 0
    else:
        hint = "too_low" if guess < st.session_state.secret_number else "too_high"
        diff = abs(guess - st.session_state.secret_number)
        if diff > 100:
            message = "Way off! Keep trying!"
        elif diff > 50:
            message = "Getting warmer!"
        elif diff > 20:
            message = "You're close!"
        else:
            message = "Very close! Almost there!"
        return "continue", hint, message, st.session_state.attempts_left

def word_guessing_game():
    """Word guessing game implementation"""
    word_list = ["PYTHON", "ALGORITHM", "VARIABLE", "FUNCTION", "COMPILER", 
                 "DEBUGGER", "ITERATOR", "DICTIONARY", "MODULE", "PACKAGE"]
    if not st.session_state.game_started:
        st.session_state.secret_word = random.choice(word_list)
        st.session_state.word_attempts = 6
        st.session_state.word_hint = None
        st.session_state.game_started = True
    return st.session_state.secret_word, st.session_state.word_attempts

def check_word_guess(guess):
    """Check word guess and return result"""
    st.session_state.word_attempts -= 1
    if guess == st.session_state.secret_word:
        return "win", st.session_state.secret_word
    elif st.session_state.word_attempts <= 0:
        return "lose", st.session_state.secret_word
    else:
        hint = []
        secret = st.session_state.secret_word
        secret_chars = list(secret)
        guess_chars = list(guess)
        
        for i in range(len(secret)):
            if i < len(guess) and guess[i] == secret[i]:
                hint.append(f"✅ {guess[i]}")
                secret_chars[i] = None
                guess_chars[i] = None
            elif i < len(guess):
                hint.append(None)
            else:
                hint.append("❓ ?")
        
        for i in range(len(secret)):
            if hint[i] is None and i < len(guess) and guess_chars[i] is not None:
                if guess_chars[i] in secret_chars:
                    hint[i] = f"🟡 {guess_chars[i]}"
                    secret_chars[secret_chars.index(guess_chars[i])] = None
                else:
                    hint[i] = "❌ ?"
        
        hint = [h if h is not None else "❌ ?" for h in hint]
        return "continue", " ".join(hint), st.session_state.word_attempts

def code_breaker_game():
    """Code breaker game implementation - Fixed Typos"""
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
        return "win", st.session_state.secret_code
    elif st.session_state.code_attempts <= 0:
        return "lose", st.session_state.secret_code
    else:
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
        
        hint_text = f"✅ {right_place} correct position"
        if wrong_place > 0:
            hint_text += f", 🔄 {wrong_place} wrong position"
        if right_place == 0 and wrong_place == 0:
            hint_text += " ❌ No matches!"
        return "continue", hint_text, st.session_state.code_attempts