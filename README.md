# 🎮 The Ultimate Guessing Game Challenge

A feature-rich, menu-driven Python application featuring three unique mini-games designed to test your logic and intuition. Built with clean code practices, robust input validation, and a modular architecture.

---

## 🚀 Featured Games

### 1. Number Guessing 🎯
- **Levels**: Choose from **Easy** (1-50), **Medium** (1-100), or **Hard** (1-500)[cite: 1].
- **Adaptive Tries**: Attempts vary by difficulty—from unlimited to just 5 tries for the ultimate challenge[cite: 1].
- **Smart Feedback**: Real-time "Too high" or "Too low" hints to guide your next move[cite: 1].

### 2. Word Scramble (Wordman Style) 🔠
- Guess a hidden word selected randomly from an internal library[cite: 1].
- **Visual Progress**: After each guess, correctly positioned letters are revealed while others remain hidden (e.g., `P _ T _ O _`)[cite: 1].
- **Constraint**: You have a maximum of 5 attempts to save the word[cite: 1].

### 3. Code Breaker (Mystery Code) 🔐
- Crack a randomly generated **4-digit secret code** within 10 attempts[cite: 1].
- **Logic-Based Hints**:
  - Tells you if a digit is correct and in the **right place**[cite: 1].
  - Tells you if a digit is correct but in the **wrong place**[cite: 1].

---

## 📊 Core Functionality
*   **Persistent Scoring**: Tracks your name, total points, and games won throughout the session[cite: 1].
*   **Dynamic Rewards**: Points are awarded based on game complexity: 10 for Number Guess, 20 for Word Guess, and 30 for Code Breaker[cite: 1].
*   **Error-Proof Input**: Built-in safeguards against invalid characters, symbols, or incorrect input lengths to ensure a smooth experience[cite: 2].
*   **Modular Architecture**: Organized into specific functions for high readability and easy maintenance[cite: 1, 2].

---

## 🛠️ Getting Started

### Prerequisites
*   **Python 3.x** must be installed on your machine.

### Installation & Execution
1.  **Download** the `guessing_game.py` file.
2.  Open your **Terminal** or **VS Code**.
3.  Navigate to the file directory and run:
    ```bash
    python guessing_game.py
    ```

---

## 🧠 Technical Highlights
*   **Structured Programming**: Employs function-based modularity for clean logic separation[cite: 2].
*   **Algorithm Efficiency**: Implements a two-pass logic check for the Code Breaker hints to ensure accurate matching[cite: 1].
*   **Input Sanitization**: Uses `try-except` blocks and string methods to handle edge cases and prevent crashes[cite: 2].

---
*Created with ❤️ by [DESHAN SIRIWARDHANA]*
