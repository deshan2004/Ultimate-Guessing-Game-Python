import random

# 3.4 Player Score Management Functions
def update_score(current_score, new_score):
    """Updates and returns the player's total score."""
    return current_score + new_score

def display_player(name, score, wins):
    """Displays the current player's statistics."""
    print("\n" + "=" * 30)
    print(f"PLAYER PROFILE: {name}")
    print(f"Total Score: {score}")
    print(f"Games Won  : {wins}")
    print("=" * 30)

# 3.1 Number Guessing Game
def number_guessing_game(difficulty):
    """A game where the player guesses a random number based on difficulty."""
    # Set parameters based on the chosen difficulty
    if difficulty == "easy":
        low, high, attempts = 1, 50, float('inf')
    elif difficulty == "medium":
        low, high, attempts = 1, 100, 10
    else: # Hard
        low, high, attempts = 1, 500, 5

    secret_number = random.randint(low, high)
    tries = 0

    print(f"\n--- Number Guessing ({difficulty.capitalize()} Level) ---")
    print(f"Guess the number between {low} and {high}")

    while tries < attempts:
        try:
            guess = int(input(f"Enter your guess (Attempt {tries + 1}): "))
            tries += 1

            if guess == secret_number:
                print(f"Correct! You guessed it in {tries} tries.")
                return True # Indicates a win
            elif guess < secret_number:
                print("Too low!")
            else:
                print("Too high!")

            # Show remaining attempts for Medium and Hard
            if attempts != float('inf'):
                print(f"Attempts left: {attempts - tries}")

        except ValueError:
            print("Invalid input! Please enter a valid whole number.")

    print(f"Game Over! The secret number was {secret_number}.")
    return False # Indicates a loss

# 3.2 Word Guessing Game
def word_guessing_game():
    """A Wordman style game where the player guesses a hidden word."""
    word_list = ["PYTHON", "ALGORITHM", "VARIABLE", "FUNCTION", "COMPILER"]
    secret_word = random.choice(word_list)
    attempts = 5

    print("\n--- Word Guessing Game ---")
    print("The hidden word has", len(secret_word), "letters.")
    
    # Display initial underscores
    print("Word: " + "_ " * len(secret_word))

    while attempts > 0:
        guess = input(f"\nAttempts left ({attempts}) - Enter your full word guess: ").upper().strip()

        # Input validation
        if len(guess) != len(secret_word):
            print(f"Error: You must enter exactly {len(secret_word)} letters.")
            continue

        if guess == secret_word:
            print(f"Success! The word was {secret_word}.")
            return True # Indicates a win

        attempts -= 1
        
        # Reveal correctly positioned letters
        reveal = []
        for i in range(len(secret_word)):
            if guess[i] == secret_word[i]:
                reveal.append(secret_word[i])
            else:
                reveal.append("_")

        print("Progress: " + " ".join(reveal))

    print(f"Game Over! The word was {secret_word}.")
    return False # Indicates a loss

# 3.3 Code Breaker Game
def code_breaker_game():
    """A game where the player guesses a 4-digit code using hints."""
    # Generate a 4-digit code as a list of string characters
    secret_code = [str(random.randint(0, 9)) for _ in range(4)]
    attempts = 10

    print("\n--- Code Breaker Game ---")
    print("Crack the 4-digit code. You have 10 tries.")

    while attempts > 0:
        guess_input = input(f"\nTry {11 - attempts}/10 - Enter 4 digits: ").strip()

        # Input validation: must be exactly 4 digits
        if len(guess_input) != 4 or not guess_input.isdigit():
            print("Invalid input. Please enter exactly 4 digits (e.g., 1234).")
            continue

        guess_list = list(guess_input)

        if guess_list == secret_code:
            print("Access Granted! Code broken successfully.")
            return True # Win

        attempts -= 1
        right_place = 0
        wrong_place = 0

        # Create temporary lists to avoid duplicate matching issues
        temp_code = secret_code[:]
        temp_guess = guess_list[:]

        # 1st Pass: Check for correct digits in the CORRECT place
        for i in range(4):
            if temp_guess[i] == temp_code[i]:
                right_place += 1
                temp_code[i] = None # Mark as used
                temp_guess[i] = None

        # 2nd Pass: Check for correct digits in the WRONG place
        for i in range(4):
            if temp_guess[i] is not None and temp_guess[i] in temp_code:
                wrong_place += 1
                temp_code[temp_code.index(temp_guess[i])] = None # Mark as used

        # Display Hints
        if right_place > 0:
            print(f"Hint: {right_place} digit(s) correct and in the right place.")
        if wrong_place > 0:
            print(f"Hint: {wrong_place} digit(s) correct but in the wrong place.")
        if right_place == 0 and wrong_place == 0:
            print("Hint: No digits match.")

    print(f"System Locked! The code was {''.join(secret_code)}.")
    return False # Loss

# 3.5 Menu System & Main Execution
def main():
    """Main function to handle the menu and game flow."""
    print("*" * 40)
    print(" Welcome to the Ultimate Guessing Game! ")
    print("*" * 40)
    
    player_name = input("Please enter your name: ").strip()
    
    # Initialize player stats
    total_score = 0
    games_won = 0

    while True:
        print("\n--- MAIN MENU ---")
        print("1. Number Guessing Game")
        print("2. Word Guessing Game")
        print("3. Mystery Code Game (Code Breaker)")
        print("4. View Player Stats")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            print("\nSelect Difficulty: 1. Easy | 2. Medium | 3. Hard")
            lvl = input("Choice: ").strip()
            diff = "easy" if lvl == '1' else "medium" if lvl == '2' else "hard"
            
            # If function returns True (Win), update stats
            if number_guessing_game(diff):
                games_won += 1
                total_score = update_score(total_score, 10) # 10 points for Number game
                
        elif choice == '2':
            if word_guessing_game():
                games_won += 1
                total_score = update_score(total_score, 20) # 20 points for Word game
                
        elif choice == '3':
            if code_breaker_game():
                games_won += 1
                total_score = update_score(total_score, 30) # 30 points for Code Breaker
                
        elif choice == '4':
            display_player(player_name, total_score, games_won)
            
        elif choice == '5':
            print(f"\nGoodbye {player_name}! Thanks for playing.")
            print(f"Final Score: {total_score} | Total Wins: {games_won}")
            break
            
        else:
            print("Invalid selection. Please enter a number between 1 and 5.")

# Run the program
if __name__ == "__main__":
    main()