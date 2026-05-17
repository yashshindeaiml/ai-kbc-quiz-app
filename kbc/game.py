import random
import threading
import pyttsx3
import speech_recognition as sr
from tkinter import *
from tkinter import messagebox

from api import fetch_questions
from utils import get_high_score, save_high_score

# Optional sound
try:
    import pygame
    pygame.mixer.init()
    correct_sound = pygame.mixer.Sound("assets/correct.wav")
    wrong_sound = pygame.mixer.Sound("assets/wrong.wav")
except:
    correct_sound = wrong_sound = None

engine = pyttsx3.init()
recognizer = sr.Recognizer()


class KBCGame:
    def __init__(self, root):
        self.root = root

        # Game state
        self.questions = fetch_questions()
        self.current_q = 0
        self.money = 0
        self.high_score = get_high_score()
        self.lifeline_used = False

        self.rewards = [1000, 2000, 5000, 10000, 20000, 50000,
                        100000, 200000, 500000, 1000000]

        # UI Setup
        self.setup_ui()
        self.load_question()

    def setup_ui(self):
        self.frame = Frame(self.root)
        self.frame.pack(expand=True)

        self.q_label = Label(self.frame, font=("Arial", 14), wraplength=600)
        self.q_label.pack(pady=10)

        self.option_buttons = []
        for i in range(4):
            btn = Button(self.frame, font=("Arial", 12),
                         command=lambda i=i: self.check_answer(i + 1),
                         width=40)
            btn.pack(pady=5)
            self.option_buttons.append(btn)

        self.timer_label = Label(self.frame, fg="blue")
        self.timer_label.pack()

        self.result_label = Label(self.frame, font=("Arial", 12))
        self.result_label.pack(pady=10)

        Button(self.frame, text="50-50 Lifeline",
               command=self.use_5050, bg="orange").pack(pady=5)

        Button(self.frame, text="Audience Poll",
               command=self.audience_poll).pack(pady=5)

        Button(self.frame, text="🎤 Speak",
               command=self.start_voice).pack(pady=5)

        Button(self.frame, text="Quit",
               command=self.quit_game, bg="red").pack(pady=5)

    def load_question(self):
        if self.current_q >= len(self.questions):
            self.game_over()
            return

        q = self.questions[self.current_q]

        self.q_label.config(text=q["question"])
        for i, opt in enumerate(q["options"]):
            self.option_buttons[i].config(text=f"{i+1}. {opt}", state=NORMAL)

        self.start_timer()
        self.speak(q)

    def speak(self, q):
        def run():
            engine.say(q["question"])
            engine.runAndWait()
        threading.Thread(target=run).start()

    # TIMER
    def start_timer(self):
        self.time_left = 15
        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"Time: {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.result_label.config(text="Time's up!", fg="red")
            self.game_over()

    def check_answer(self, choice):
        correct = self.questions[self.current_q]["answer"]

        if choice == correct:
            if correct_sound:
                correct_sound.play()

            self.money = self.rewards[self.current_q]
            self.result_label.config(text=f"Correct! ₹{self.money}", fg="green")
            self.current_q += 1
            self.root.after(1500, self.load_question)
        else:
            if wrong_sound:
                wrong_sound.play()

            self.result_label.config(text="Wrong Answer!", fg="red")
            self.game_over()

    # LIFELINES
    def use_5050(self):
        if self.lifeline_used:
            return

        correct = self.questions[self.current_q]["answer"]
        wrong = [i for i in range(1, 5) if i != correct]
        remove = random.sample(wrong, 2)

        for i in remove:
            self.option_buttons[i-1].config(state=DISABLED)

        self.lifeline_used = True

    def audience_poll(self):
        correct = self.questions[self.current_q]["answer"] - 1
        votes = [random.randint(10, 30) for _ in range(4)]
        votes[correct] += 40

        result = "\n".join([f"Option {i+1}: {votes[i]}%" for i in range(4)])
        messagebox.showinfo("Audience Poll", result)

    # VOICE
    def start_voice(self):
        def listen():
            try:
                with sr.Microphone() as source:
                    audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)

                if "1" in text:
                    self.check_answer(1)
                elif "2" in text:
                    self.check_answer(2)
                elif "3" in text:
                    self.check_answer(3)
                elif "4" in text:
                    self.check_answer(4)

            except:
                pass

        threading.Thread(target=listen).start()

    def quit_game(self):
        messagebox.showinfo("Quit", f"You won ₹{self.money}")
        self.root.quit()

    def game_over(self):
        if self.money > self.high_score:
            save_high_score(self.money)

        messagebox.showinfo("Game Over",
                            f"You won ₹{self.money}\nHigh Score: ₹{self.high_score}")
        self.root.quit()