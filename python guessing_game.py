import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import math
from threading import Thread

class UltimateGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ The Ultimate Guessing Game - Deluxe Edition ✨")
        self.root.geometry("600x700")
        self.root.configure(bg="#0f0f1a")
        
        # Center the window
        self.center_window()
        
        # Player Stats
        self.player_name = ""
        self.total_score = 0
        self.games_won = 0
        self.game_history = []
        
        # Sound effects (optional - won't error if no sound)
        self.sound_on = True
        
        # Color Scheme
        self.colors = {
            'bg': '#0f0f1a',
            'card': '#1a1a2e',
            'accent': '#16213e',
            'primary': '#e94560',
            'secondary': '#0f3460',
            'success': '#4ecdc4',
            'warning': '#ffd93d',
            'text': '#eeeeee',
            'text_light': '#a0a0b0'
        }
        
        # Animation variables
        self.animation_id = None
        
        # Main Container
        self.main_container = tk.Frame(self.root, bg=self.colors['bg'])
        self.main_container.pack(expand=True, fill="both")
        
        self.show_login_screen()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = 600
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_gradient(self, widget, color1, color2):
        """Create a gradient effect (simplified)"""
        widget.configure(bg=color1)
    
    def animate_button(self, button, original_color):
        """Animate button on hover"""
        def on_enter(e):
            button.configure(bg=self.colors['primary'], fg='white')
        def on_leave(e):
            button.configure(bg=original_color, fg=self.colors['bg'])
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def clear_screen(self):
        """Clear all widgets from main container"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def pulse_effect(self, widget, count=3):
        """Create a pulsing effect on widget"""
        original_bg = widget.cget('bg')
        def pulse(step=0):
            if step < count * 2:
                if step % 2 == 0:
                    widget.configure(bg=self.colors['primary'])
                else:
                    widget.configure(bg=original_bg)
                self.root.after(200, lambda: pulse(step + 1))
            else:
                widget.configure(bg=original_bg)
        pulse()
    
    def show_toast(self, message, duration=2000):
        """Show a toast notification"""
        toast = tk.Toplevel(self.root)
        toast.title("")
        toast.configure(bg=self.colors['card'])
        
        # Position near the top
        x = self.root.winfo_x() + self.root.winfo_width() // 2 - 100
        y = self.root.winfo_y() + 50
        toast.geometry(f"300x50+{x}+{y}")
        toast.overrideredirect(True)
        
        tk.Label(toast, text=message, font=("Arial", 10, "bold"),
                fg=self.colors['success'], bg=self.colors['card']).pack(expand=True, fill='both', padx=20, pady=10)
        
        toast.after(duration, toast.destroy)
    
    # --- 1. Login Screen ---
    def show_login_screen(self):
        self.clear_screen()
        
        # Animated title
        title_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        title_frame.pack(pady=(50, 0))
        
        title = tk.Label(title_frame, text="ULTIMATE GUESSING", 
                        font=("Helvetica", 28, "bold"), 
                        fg=self.colors['primary'], bg=self.colors['bg'])
        title.pack()
        
        title2 = tk.Label(title_frame, text="GAME DELUXE", 
                         font=("Helvetica", 28, "bold"), 
                         fg=self.colors['success'], bg=self.colors['bg'])
        title2.pack()
        
        # Subtitles
        tk.Label(self.main_container, text="🎮 Test Your Skills! 🎮", 
                font=("Arial", 14), fg=self.colors['text_light'], 
                bg=self.colors['bg']).pack(pady=20)
        
        # Player name input frame
        name_frame = tk.Frame(self.main_container, bg=self.colors['card'], padx=20, pady=20)
        name_frame.pack(pady=30, padx=40, fill='x')
        
        tk.Label(name_frame, text="Enter Your Name", 
                font=("Arial", 12, "bold"), 
                fg=self.colors['text'], bg=self.colors['card']).pack()
        
        self.name_entry = tk.Entry(name_frame, font=("Arial", 14, "bold"), 
                                   justify='center', bg='white', fg='black')
        self.name_entry.pack(pady=10, padx=20, fill='x')
        self.name_entry.focus_set()
        
        # Start button with animation
        start_btn = tk.Button(name_frame, text="🎯 START ADVENTURE 🎯", 
                             font=("Arial", 12, "bold"), 
                             bg=self.colors['primary'], fg='white',
                             command=self.start_main_menu, padx=20, pady=10)
        start_btn.pack(pady=10)
        self.animate_button(start_btn, self.colors['primary'])
        
        # Press Enter to start
        self.name_entry.bind('<Return>', lambda e: self.start_main_menu())
    
    def start_main_menu(self):
        name = self.name_entry.get().strip()
        if not name:
            self.animate_warning("Please enter your name!")
            return
        self.player_name = name
        self.show_toast(f"Welcome, {name}! ✨")
        self.show_main_menu()
    
    def animate_warning(self, message):
        """Animated warning message"""
        msg = tk.Label(self.main_container, text=message, fg=self.colors['warning'],
                      bg=self.colors['bg'], font=("Arial", 10, "bold"))
        msg.pack(pady=5)
        self.root.after(2000, msg.destroy)
    
    # --- 2. Main Menu with Stats Card ---
    def show_main_menu(self):
        self.clear_screen()
        
        # Header
        header = tk.Frame(self.main_container, bg=self.colors['card'], height=100)
        header.pack(fill='x', padx=20, pady=(20, 10))
        header.pack_propagate(False)
        
        tk.Label(header, text=f"👤 {self.player_name}", 
                font=("Arial", 14, "bold"), 
                fg=self.colors['primary'], bg=self.colors['card']).pack(pady=(10, 0))
        
        # Stats card with animation
        stats_frame = tk.Frame(self.main_container, bg=self.colors['card'], 
                               relief='ridge', bd=2)
        stats_frame.pack(pady=10, padx=20, fill='x')
        
        # Animated score display
        self.score_var = tk.StringVar()
        self.score_var.set(f"🏆 SCORE: {self.total_score}")
        self.wins_var = tk.StringVar()
        self.wins_var.set(f"🎮 WINS: {self.games_won}")
        
        stats_left = tk.Frame(stats_frame, bg=self.colors['card'])
        stats_left.pack(side='left', expand=True, pady=10)
        
        stats_right = tk.Frame(stats_frame, bg=self.colors['card'])
        stats_right.pack(side='right', expand=True, pady=10)
        
        tk.Label(stats_left, textvariable=self.score_var, 
                font=("Arial", 12, "bold"), 
                fg=self.colors['success'], bg=self.colors['card']).pack()
        
        tk.Label(stats_right, textvariable=self.wins_var, 
                font=("Arial", 12, "bold"), 
                fg=self.colors['warning'], bg=self.colors['card']).pack()
        
        # Show win streak if any
        if self.games_won > 0:
            win_rate = (self.games_won / (self.games_won + 5)) * 100 if self.games_won < 10 else 100
            tk.Label(stats_frame, text=f"📈 WIN RATE: {win_rate:.1f}%", 
                    font=("Arial", 10), fg=self.colors['text_light'], 
                    bg=self.colors['card']).pack(pady=(0, 10))
        
        # Menu buttons with icons and descriptions
        menu_items = [
            ("🔢", "NUMBER GUESSING", "Test your intuition", "#ff6b6b", self.setup_number_game),
            ("📝", "WORD GUESSING", "Expand your vocabulary", "#4ecdc4", self.setup_word_game),
            ("🔐", "CODE BREAKER", "Crack the secret code", "#95e77f", self.setup_code_breaker),
            ("📊", "VIEW STATS", "Check your progress", "#ffd93d", self.show_stats_detailed),
            ("🏆", "ACHIEVEMENTS", "See your awards", "#c9a3e8", self.show_achievements),
            ("🎨", "THEMES", "Change appearance", "#a0a0b0", self.show_themes),
            ("❓", "HELP", "Learn how to play", "#fab387", self.show_help),
            ("🚪", "EXIT", "Quit the game", "#f38ba8", self.root.quit)
        ]
        
        for icon, title, desc, color, cmd in menu_items:
            btn_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
            btn_frame.pack(pady=5, padx=30, fill='x')
            
            btn = tk.Button(btn_frame, text=f"{icon}  {title}", 
                           font=("Arial", 12, "bold"), 
                           bg=color, fg='white', height=2,
                           command=cmd)
            btn.pack(fill='x')
            self.animate_button(btn, color)
            
            # Description label
            tk.Label(btn_frame, text=desc, font=("Arial", 8), 
                    fg=self.colors['text_light'], bg=self.colors['bg']).pack()
    
    # --- 3. Enhanced Number Guessing Game ---
    def setup_number_game(self):
        self.clear_screen()
        
        # Game header
        tk.Label(self.main_container, text="🔢 NUMBER GUESSING CHALLENGE", 
                font=("Arial", 16, "bold"), fg=self.colors['primary'], 
                bg=self.colors['bg']).pack(pady=20)
        
        # Difficulty selection with cards
        difficulties = [
            ("🌿 EASY", "1-50 • ∞ attempts • 5 pts", 1, 50, float('inf'), 5, "#4ecdc4"),
            ("⚡ MEDIUM", "1-100 • 10 attempts • 10 pts", 1, 100, 10, 10, "#ffd93d"),
            ("🔥 HARD", "1-500 • 5 attempts • 20 pts", 1, 500, 5, 20, "#ff6b6b")
        ]
        
        for name, desc, low, high, att, pts, color in difficulties:
            card = tk.Frame(self.main_container, bg=self.colors['card'], 
                           relief='raised', bd=2)
            card.pack(pady=10, padx=40, fill='x')
            
            btn = tk.Button(card, text=name, font=("Arial", 12, "bold"),
                           bg=color, fg='white', height=2,
                           command=lambda l=low, h=high, a=att, p=pts: 
                                   self.start_number_game(l, h, a, p))
            btn.pack(fill='x')
            self.animate_button(btn, color)
            
            tk.Label(card, text=desc, font=("Arial", 9), 
                    fg=self.colors['text_light'], bg=self.colors['card']).pack(pady=(0, 5))
        
        tk.Button(self.main_container, text="◀ BACK", font=("Arial", 10), 
                 bg=self.colors['secondary'], fg='white', 
                 command=self.show_main_menu).pack(pady=20)
    
    def start_number_game(self, low, high, max_att, points):
        self.clear_screen()
        self.secret_num = random.randint(low, high)
        self.attempts_left = max_att
        self.num_points = points
        self.num_tries = 0
        
        # Game info card
        info_frame = tk.Frame(self.main_container, bg=self.colors['card'], padx=20, pady=15)
        info_frame.pack(pady=20, padx=30, fill='x')
        
        tk.Label(info_frame, text="🎯 CURRENT CHALLENGE", 
                font=("Arial", 10, "bold"), fg=self.colors['primary'], 
                bg=self.colors['card']).pack()
        
        tk.Label(info_frame, text=f"Guess a number between {low} and {high}", 
                font=("Arial", 14), fg=self.colors['text'], 
                bg=self.colors['card']).pack(pady=10)
        
        tk.Label(info_frame, text=f"🏆 Points at stake: {points}", 
                font=("Arial", 11, "bold"), fg=self.colors['success'], 
                bg=self.colors['card']).pack()
        
        # Attempts display
        self.att_var = tk.StringVar()
        self.att_var.set(f"💪 Attempts left: {'∞' if max_att == float('inf') else max_att}")
        tk.Label(info_frame, textvariable=self.att_var, 
                font=("Arial", 11), fg=self.colors['warning'], 
                bg=self.colors['card']).pack()
        
        # Guess input
        input_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        input_frame.pack(pady=30)
        
        self.num_input = tk.Entry(input_frame, font=("Arial", 18, "bold"), 
                                  justify='center', width=10)
        self.num_input.pack()
        self.num_input.focus_set()
        
        # Hint label
        self.num_msg = tk.Label(self.main_container, text="", 
                               font=("Arial", 12), fg=self.colors['primary'], 
                               bg=self.colors['bg'])
        self.num_msg.pack(pady=10)
        
        # Progress bar
        if max_att != float('inf'):
            self.progress_bar = ttk.Progressbar(self.main_container, length=300, 
                                                mode='determinate')
            self.progress_bar.pack(pady=10)
            self.update_progress()
        
        # Buttons
        btn_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        btn_frame.pack(pady=20)
        
        guess_btn = tk.Button(btn_frame, text="🔍 SUBMIT GUESS", 
                             font=("Arial", 12, "bold"), 
                             bg=self.colors['primary'], fg='white',
                             command=self.check_number_guess)
        guess_btn.pack(side='left', padx=10)
        self.animate_button(guess_btn, self.colors['primary'])
        
        giveup_btn = tk.Button(btn_frame, text="🏳️ GIVE UP", 
                              font=("Arial", 12), bg=self.colors['secondary'], 
                              fg='white', command=self.show_main_menu)
        giveup_btn.pack(side='left', padx=10)
        
        # Bind Enter key
        self.num_input.bind('<Return>', lambda e: self.check_number_guess())
    
    def update_progress(self):
        """Update progress bar for attempts"""
        if hasattr(self, 'attempts_left') and hasattr(self, 'num_points'):
            if self.attempts_left != float('inf'):
                if self.num_points == 20:  # Hard mode
                    total = 5
                else:  # Medium mode
                    total = 10
                used = total - self.attempts_left
                progress = (used / total) * 100
                self.progress_bar['value'] = progress
    
    def check_number_guess(self):
        try:
            val = int(self.num_input.get())
            self.num_tries += 1
            
            if self.attempts_left != float('inf'):
                self.attempts_left -= 1
                self.update_progress()
            
            # Visual feedback animation
            self.pulse_effect(self.num_msg, 1)
            
            if val == self.secret_num:
                self.total_score += self.num_points
                self.games_won += 1
                self.update_stats_display()
                
                messagebox.showinfo("🎉 VICTORY! 🎉", 
                                   f"Perfect! You guessed it in {self.num_tries} tries!\n\n"
                                   f"+{self.num_points} points added!\n"
                                   f"Total Score: {self.total_score}\n"
                                   f"Games Won: {self.games_won}")
                self.show_main_menu()
                
            elif self.attempts_left == 0:
                messagebox.showerror("💀 GAME OVER 💀", 
                                    f"Out of attempts! The number was {self.secret_num}")
                self.show_main_menu()
                
            else:
                hint = "📉 Too Low!" if val < self.secret_num else "📈 Too High!"
                diff = abs(val - self.secret_num)
                
                if diff > 100:
                    hint += " (Way off! 🎯)"
                elif diff > 50:
                    hint += " (Getting warmer 🌡️)"
                elif diff > 20:
                    hint += " (You're close! 🎯)"
                else:
                    hint += " (Very close! 🔥)"
                
                att_str = f"Attempts left: {self.attempts_left}" if self.attempts_left != float('inf') else "Unlimited attempts"
                self.num_msg.config(text=f"{hint}\n{att_str}")
                self.num_input.delete(0, tk.END)
                self.num_input.focus_set()
                
        except ValueError:
            self.animate_warning("Please enter a valid number!")
            self.num_input.delete(0, tk.END)
    
    # --- 4. Enhanced Word Guessing Game ---
    def setup_word_game(self):
        self.clear_screen()
        
        words = ["PYTHON", "ALGORITHM", "VARIABLE", "FUNCTION", "COMPILER", 
                "DEBUGGER", "ITERATOR", "DICTIONARY", "MODULE", "PACKAGE"]
        self.secret_word = random.choice(words)
        self.word_attempts = 6
        self.word_points = 20
        
        # Game header
        tk.Label(self.main_container, text="📝 WORD GUESSING CHALLENGE", 
                font=("Arial", 16, "bold"), fg=self.colors['primary'], 
                bg=self.colors['bg']).pack(pady=20)
        
        # Info card
        info_frame = tk.Frame(self.main_container, bg=self.colors['card'], padx=20, pady=15)
        info_frame.pack(pady=10, padx=30, fill='x')
        
        tk.Label(info_frame, text=f"📖 The word has {len(self.secret_word)} letters", 
                font=("Arial", 12), fg=self.colors['text'], 
                bg=self.colors['card']).pack()
        
        tk.Label(info_frame, text=f"🏆 Points: {self.word_points}", 
                font=("Arial", 11, "bold"), fg=self.colors['success'], 
                bg=self.colors['card']).pack()
        
        # Word display
        self.word_display = tk.Label(self.main_container, 
                                     text="❓ " * len(self.secret_word), 
                                     font=("Courier", 24, "bold"), 
                                     fg=self.colors['success'], bg=self.colors['bg'])
        self.word_display.pack(pady=30)
        
        # Guess input
        self.word_input = tk.Entry(self.main_container, font=("Arial", 14), 
                                   justify='center', width=20)
        self.word_input.pack(pady=10)
        self.word_input.focus_set()
        
        # Status
        self.word_status = tk.Label(self.main_container, 
                                    text=f"💪 Attempts left: {self.word_attempts}", 
                                    font=("Arial", 11), fg=self.colors['warning'], 
                                    bg=self.colors['bg'])
        self.word_status.pack()
        
        # Buttons
        btn_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        btn_frame.pack(pady=20)
        
        guess_btn = tk.Button(btn_frame, text="📝 CHECK WORD", 
                             font=("Arial", 12, "bold"), 
                             bg=self.colors['primary'], fg='white',
                             command=self.check_word_guess)
        guess_btn.pack(side='left', padx=10)
        self.animate_button(guess_btn, self.colors['primary'])
        
        back_btn = tk.Button(btn_frame, text="◀ BACK", 
                            font=("Arial", 12), bg=self.colors['secondary'], 
                            fg='white', command=self.show_main_menu)
        back_btn.pack(side='left', padx=10)
        
        self.word_input.bind('<Return>', lambda e: self.check_word_guess())
    
    def check_word_guess(self):
        guess = self.word_input.get().upper().strip()
        
        if len(guess) != len(self.secret_word):
            self.animate_warning(f"Enter exactly {len(self.secret_word)} letters!")
            return
        
        if not guess.isalpha():
            self.animate_warning("Please enter only letters!")
            return
        
        if guess == self.secret_word:
            self.total_score += 20
            self.games_won += 1
            self.update_stats_display()
            messagebox.showinfo("🎉 EXCELLENT! 🎉", 
                               f"You cracked the word: {self.secret_word}!\n\n"
                               f"+20 points!\n"
                               f"Total Score: {self.total_score}")
            self.show_main_menu()
        else:
            self.word_attempts -= 1
            
            if self.word_attempts <= 0:
                messagebox.showerror("💀 GAME OVER 💀", 
                                    f"The word was: {self.secret_word}")
                self.show_main_menu()
            else:
                # Better hint system
                hint = []
                for i in range(len(self.secret_word)):
                    if i < len(guess) and guess[i] == self.secret_word[i]:
                        hint.append(f"{self.colors['success']}{guess[i]}{self.colors['end']}")
                    elif i < len(guess) and guess[i] in self.secret_word:
                        hint.append(f"{self.colors['warning']}{guess[i]}{self.colors['end']}")
                    else:
                        hint.append("_")
                
                self.word_display.config(text=" ".join(hint))
                self.word_status.config(text=f"💪 Attempts left: {self.word_attempts}")
                self.word_input.delete(0, tk.END)
                self.word_input.focus_set()
                self.pulse_effect(self.word_display, 1)
    
    # --- 5. Enhanced Code Breaker Game ---
    def setup_code_breaker(self):
        self.clear_screen()
        self.secret_code = "".join([str(random.randint(0, 9)) for _ in range(4)])
        self.code_attempts = 10
        self.code_history = []
        
        # Game header
        tk.Label(self.main_container, text="🔐 CODE BREAKER CHALLENGE", 
                font=("Arial", 16, "bold"), fg=self.colors['primary'], 
                bg=self.colors['bg']).pack(pady=20)
        
        # Info card
        info_frame = tk.Frame(self.main_container, bg=self.colors['card'], padx=20, pady=15)
        info_frame.pack(pady=10, padx=30, fill='x')
        
        tk.Label(info_frame, text="💻 Crack the 4-digit code (0-9)", 
                font=("Arial", 12), fg=self.colors['text'], 
                bg=self.colors['card']).pack()
        
        tk.Label(info_frame, text=f"🏆 Points: 30", 
                font=("Arial", 11, "bold"), fg=self.colors['success'], 
                bg=self.colors['card']).pack()
        
        # Guess input
        self.code_input = tk.Entry(self.main_container, font=("Arial", 20, "bold"), 
                                   justify='center', width=6)
        self.code_input.pack(pady=20)
        self.code_input.focus_set()
        
        # Attempts display
        self.code_att_var = tk.StringVar()
        self.code_att_var.set(f"🔓 Attempts remaining: {self.code_attempts}")
        tk.Label(self.main_container, textvariable=self.code_att_var, 
                font=("Arial", 12, "bold"), fg=self.colors['warning'], 
                bg=self.colors['bg']).pack()
        
        # History display
        history_frame = tk.Frame(self.main_container, bg=self.colors['card'], padx=10, pady=10)
        history_frame.pack(pady=20, padx=30, fill='both', expand=True)
        
        tk.Label(history_frame, text="📜 GUESS HISTORY", font=("Arial", 10, "bold"), 
                fg=self.colors['primary'], bg=self.colors['card']).pack()
        
        self.history_text = tk.Text(history_frame, height=8, width=40, 
                                    bg=self.colors['secondary'], fg=self.colors['text'], 
                                    font=("Courier", 10))
        self.history_text.pack(pady=10, fill='both', expand=True)
        
        # Buttons
        btn_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        btn_frame.pack(pady=10)
        
        guess_btn = tk.Button(btn_frame, text="🔐 CRACK CODE", 
                             font=("Arial", 12, "bold"), 
                             bg=self.colors['primary'], fg='white',
                             command=self.check_code)
        guess_btn.pack(side='left', padx=10)
        self.animate_button(guess_btn, self.colors['primary'])
        
        back_btn = tk.Button(btn_frame, text="◀ BACK", 
                            font=("Arial", 12), bg=self.colors['secondary'], 
                            fg='white', command=self.show_main_menu)
        back_btn.pack(side='left', padx=10)
        
        self.code_input.bind('<Return>', lambda e: self.check_code())
    
    def check_code(self):
        guess = self.code_input.get().strip()
        
        if len(guess) != 4 or not guess.isdigit():
            self.animate_warning("Enter exactly 4 digits (0-9)!")
            return
        
        if guess == self.secret_code:
            self.total_score += 30
            self.games_won += 1
            self.update_stats_display()
            messagebox.showinfo("🎉 ACCESS GRANTED! 🎉", 
                               f"You cracked the code: {self.secret_code}!\n\n"
                               f"+30 points!\n"
                               f"Total Score: {self.total_score}")
            self.show_main_menu()
        else:
            self.code_attempts -= 1
            self.code_att_var.set(f"🔓 Attempts remaining: {self.code_attempts}")
            
            # Calculate hints
            right_place = sum(1 for i in range(4) if guess[i] == self.secret_code[i])
            wrong_place = 0
            temp_code = list(self.secret_code)
            temp_guess = list(guess)
            
            for i in range(4):
                if temp_guess[i] == temp_code[i]:
                    temp_code[i] = None
                    temp_guess[i] = None
            
            for i in range(4):
                if temp_guess[i] is not None and temp_guess[i] in temp_code:
                    wrong_place += 1
                    temp_code[temp_code.index(temp_guess[i])] = None
            
            # Add to history
            hint_text = f"{guess} → ✅ {right_place} correct spot"
            if wrong_place > 0:
                hint_text += f", 🔄 {wrong_place} wrong spot"
            if right_place == 0 and wrong_place == 0:
                hint_text += " (No matches!)"
            
            self.code_history.append(hint_text)
            self.history_text.insert('1.0', f"• {hint_text}\n")
            self.history_text.see('1.0')
            
            if self.code_attempts <= 0:
                messagebox.showerror("🔒 SYSTEM LOCKED 🔒", 
                                    f"The code was: {self.secret_code}")
                self.show_main_menu()
            else:
                self.code_input.delete(0, tk.END)
                self.code_input.focus_set()
                self.pulse_effect(self.history_text, 1)
    
    # --- 6. Enhanced Stats View ---
    def show_stats_detailed(self):
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Player Statistics")
        stats_window.geometry("400x500")
        stats_window.configure(bg=self.colors['bg'])
        
        # Center the window
        stats_window.update_idletasks()
        x = (stats_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (stats_window.winfo_screenheight() // 2) - (500 // 2)
        stats_window.geometry(f'400x500+{x}+{y}')
        
        # Stats content
        tk.Label(stats_window, text="📊 PLAYER STATISTICS", 
                font=("Arial", 16, "bold"), fg=self.colors['primary'], 
                bg=self.colors['bg']).pack(pady=20)
        
        stats_frame = tk.Frame(stats_window, bg=self.colors['card'], padx=20, pady=20)
        stats_frame.pack(pady=10, padx=20, fill='x')
        
        stats_data = [
            ("👤 Player Name", self.player_name),
            ("🏆 Total Score", str(self.total_score)),
            ("🎮 Games Won", str(self.games_won)),
            ("📊 Win Rate", f"{(self.games_won / (self.games_won + 5) * 100) if self.games_won > 0 else 0:.1f}%")
        ]
        
        for label, value in stats_data:
            frame = tk.Frame(stats_frame, bg=self.colors['card'])
            frame.pack(fill='x', pady=5)
            tk.Label(frame, text=label + ":", font=("Arial", 11, "bold"), 
                    fg=self.colors['text'], bg=self.colors['card']).pack(side='left')
            tk.Label(frame, text=value, font=("Arial", 11), 
                    fg=self.colors['success'], bg=self.colors['card']).pack(side='right')
        
        # Progress to next level
        next_level = 50 - (self.total_score % 50)
        if self.total_score > 0:
            tk.Label(stats_frame, text=f"\n⭐ Next level in {next_level} points", 
                    font=("Arial", 10), fg=self.colors['warning'], 
                    bg=self.colors['card']).pack(pady=10)
        
        # Close button
        tk.Button(stats_window, text="CLOSE", font=("Arial", 10), 
                 bg=self.colors['primary'], fg='white', 
                 command=stats_window.destroy).pack(pady=20)
    
    # --- 7. Achievements System ---
    def show_achievements(self):
        achievements_window = tk.Toplevel(self.root)
        achievements_window.title("Achievements")
        achievements_window.geometry("400x500")
        achievements_window.configure(bg=self.colors['bg'])
        
        # Center window
        achievements_window.update_idletasks()
        x = (achievements_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (achievements_window.winfo_screenheight() // 2) - (500 // 2)
        achievements_window.geometry(f'400x500+{x}+{y}')
        
        tk.Label(achievements_window, text="🏆 ACHIEVEMENTS", 
                font=("Arial", 16, "bold"), fg=self.colors['primary'], 
                bg=self.colors['bg']).pack(pady=20)
        
        achievements_frame = tk.Frame(achievements_window, bg=self.colors['card'], 
                                      padx=15, pady=15)
        achievements_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        achievements = [
            ("🎯 First Blood", self.games_won >= 1, "Win your first game"),
            ("⭐ Rising Star", self.games_won >= 3, "Win 3 games"),
            ("🏅 Veteran", self.games_won >= 10, "Win 10 games"),
            ("💰 Point Master", self.total_score >= 100, "Score 100+ points"),
            ("💎 Elite Player", self.total_score >= 500, "Score 500+ points"),
            ("🔢 Number Guru", "Number" in str(self.game_history), "Win number game"),
            ("📝 Word Master", "Word" in str(self.game_history), "Win word game"),
            ("🔐 Code Breaker Elite", "Code" in str(self.game_history), "Win code breaker")
        ]
        
        for achievement, unlocked, description in achievements:
            frame = tk.Frame(achievements_frame, bg=self.colors['secondary'], padx=10, pady=5)
            frame.pack(fill='x', pady=5)
            
            status = "✅" if unlocked else "🔒"
            color = self.colors['success'] if unlocked else self.colors['text_light']
            
            tk.Label(frame, text=f"{status} {achievement}", 
                    font=("Arial", 11, "bold"), fg=color, 
                    bg=self.colors['secondary']).pack(anchor='w')
            tk.Label(frame, text=description, font=("Arial", 8), 
                    fg=self.colors['text_light'], bg=self.colors['secondary']).pack(anchor='w')
        
        tk.Button(achievements_window, text="CLOSE", font=("Arial", 10), 
                 bg=self.colors['primary'], fg='white', 
                 command=achievements_window.destroy).pack(pady=20)
    
    # --- 8. Themes ---
    def show_themes(self):
        theme_window = tk.Toplevel(self.root)
        theme_window.title("Themes")
        theme_window.geometry("350x400")
        theme_window.configure(bg=self.colors['bg'])
        
        themes = [
            ("🌙 Dark Nebula", "#0f0f1a", "#1a1a2e", "#e94560"),
            ("☀️ Sunrise", "#fff4e6", "#ffe0b2", "#ff6b6b"),
            ("🌊 Ocean Deep", "#001f3f", "#003366", "#4ecdc4"),
            ("🌸 Sakura", "#ffe4e1", "#ffb7c5", "#ff69b4"),
            ("🌿 Forest", "#1a3c2c", "#2d5a3f", "#95e77f")
        ]
        
        for name, bg, card, accent in themes:
            btn = tk.Button(theme_window, text=name, font=("Arial", 11),
                           bg=card, fg='white', padx=20, pady=10,
                           command=lambda b=bg, c=card, a=accent: self.apply_theme(b, c, a, theme_window))
            btn.pack(pady=5, padx=20, fill='x')
    
    def apply_theme(self, bg, card, accent, window):
        self.colors['bg'] = bg
        self.colors['card'] = card
        self.colors['primary'] = accent
        self.root.configure(bg=bg)
        window.destroy()
        self.show_toast("Theme applied! Restart game for full effect", 1500)
    
    # --- 9. Help System ---
    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("How to Play")
        help_window.geometry("500x550")
        help_window.configure(bg=self.colors['bg'])
        
        # Create notebook for tabs
        notebook = ttk.Notebook(help_window)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Number game help
        num_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(num_frame, text="🔢 Number Game")
        help_text_num = """HOW TO PLAY NUMBER GUESSING:

1️⃣ Choose difficulty level
   • Easy: Numbers 1-50, unlimited attempts (5 pts)
   • Medium: Numbers 1-100, 10 attempts (10 pts)
   • Hard: Numbers 1-500, 5 attempts (20 pts)

2️⃣ Guess the secret number
   • Enter your guess in the input box
   • Get hints: "Too High" or "Too Low"

3️⃣ Win by guessing correctly
   • Score points based on difficulty
   • Higher difficulty = more points

💡 Tips:
   • Use binary search strategy
   • Start with middle numbers
   • Pay attention to hint feedback"""
        
        tk.Label(num_frame, text=help_text_num, font=("Arial", 10), 
                fg=self.colors['text'], bg=self.colors['bg'], 
                justify='left').pack(padx=20, pady=20, anchor='w')
        
        # Word game help
        word_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(word_frame, text="📝 Word Game")
        help_text_word = """HOW TO PLAY WORD GUESSING:

1️⃣ You have 6 attempts
2️⃣ Guess the hidden word
   • Word length is shown as underscores
   • Enter your full word guess

3️⃣ Get hints after each guess
   • Green: Letter in correct position
   • Yellow: Letter exists but wrong position
   • _: Letter not in word

4️⃣ Win by guessing the word
   • Score 20 points

💡 Tips:
   • Start with common vowels
   • Look for letter patterns
   • Think of programming terms"""
        
        tk.Label(word_frame, text=help_text_word, font=("Arial", 10), 
                fg=self.colors['text'], bg=self.colors['bg'], 
                justify='left').pack(padx=20, pady=20, anchor='w')
        
        # Code breaker help
        code_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(code_frame, text="🔐 Code Breaker")
        help_text_code = """HOW TO PLAY CODE BREAKER:

1️⃣ Crack the 4-digit code (0-9)
2️⃣ You have 10 attempts
3️⃣ Enter 4 digits at a time

4️⃣ Decode the hints:
   • Correct spot: Digit in right position
   • Wrong spot: Digit exists but wrong position
   • No match: Digit not in code

5️⃣ Win by guessing the exact code
   • Score 30 points

💡 Tips:
   • Start with 0000 to see matches
   • Use process of elimination
   • Track your previous guesses"""
        
        tk.Label(code_frame, text=help_text_code, font=("Arial", 10), 
                fg=self.colors['text'], bg=self.colors['bg'], 
                justify='left').pack(padx=20, pady=20, anchor='w')
        
        # Close button
        tk.Button(help_window, text="GOT IT!", font=("Arial", 10, "bold"), 
                 bg=self.colors['primary'], fg='white', 
                 command=help_window.destroy).pack(pady=10)
    
    def update_stats_display(self):
        """Update the stats display in main menu"""
        if hasattr(self, 'score_var'):
            self.score_var.set(f"🏆 SCORE: {self.total_score}")
            self.wins_var.set(f"🎮 WINS: {self.games_won}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateGuessingGame(root)
    root.mainloop()