# The Ultimate Guessing Game Challenge 🎮

This project is a comprehensive, menu-driven Python application developed as part of the **EC1451 Fundamentals of Programming** assignment. It showcases structured programming techniques, input validation, and modular function design[cite: 2].

## 🚀 Games Included

### 1. Number Guessing Game
- Features three difficulty levels: **Easy** (1-50, Unlimited tries), **Medium** (1-100, 10 tries), and **Hard** (1-500, 5 tries).
- Provides real-time feedback such as "Too high" or "Too low".

### 2. Word Guessing Game[cite: 1]
- A "Wordman" style game where you guess a hidden word from a random list[cite: 1].
- After each attempt, the system reveals correctly positioned letters and hides the rest using underscores[cite: 1].
- Maximum 5 attempts allowed[cite: 1].

### 3. Code Breaker (Mystery Code Game)[cite: 1]
- Crack a randomly generated 4-digit secret code within 10 tries[cite: 1].
- Advanced hint logic: Tells you if a digit is correct and in the right place, or correct but in the wrong place[cite: 1].

## 📊 Core Features
- **Player Score Management**: Tracks the player's name, total score, and total games won[cite: 1].
- **Dynamic Scoring System**: Awards 10 points for Number Guessing, 20 for Word Guessing, and 30 for Code Breaker[cite: 1].
- **Modular Design**: Built using specific functions like `update_score()` and `display_player()` as per assignment requirements[cite: 1].
- **Robust Input Handling**: Includes error checking for non-numeric inputs and incorrect code/word lengths[cite: 2].

## 🛠️ How to Run
1. Make sure you have **Python 3.x** installed on your system.
2. Download the `guessing_game.py` file.
3. Open your terminal or VS Code.
4. Run the program using:
   ```bash
   python guessing_game.py
