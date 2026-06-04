import os
import datetime
import random
import csv
import tkinter as tk
from tkinter import messagebox
# from typing import List, Dict
from typing import Dict, List
import pygame
# import urllib.request
from PIL import Image, ImageTk
# from tkinter import PhotoImage

high_score_file = "high_score.csv"

# cSpell:words pady wraplength
# cSpell:words pady wraplength relx rely

# ---------------------------
# High Score
# ---------------------------
def save_high_score(name: str, points: int):
    if points <= 0:
        return
    now = datetime.datetime.now()
    date = now.strftime("%B %d, %Y")
    time_stamp = now.strftime("%I:%M %p")
    file_exists = os.path.exists(high_score_file)
    with open(high_score_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Score", "Date", "Time"])
        writer.writerow([name, points, date, time_stamp])

def read_high_scores() -> List[List[str]]:
    if not os.path.exists(high_score_file):
        return []
    with open(high_score_file, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    if len(reader) <= 1:
        return []
    data = reader[1:]
    data.sort(key=lambda row: int(row[1]) if row[1].isdigit() else 0, reverse=True)
    return data[:10]

# ---------------------------
# Load Questions
# ---------------------------
def load_questions_from_csv(filename: str) -> List[Dict[str, str]]:
    if not os.path.exists(filename):
        return []

    with open(filename, "r", encoding="utf-8") as f:
        return [dict(row) for row in csv.DictReader(f)]
# # ---------------------------
# def download_music():
#     filename = "theme.mp3"
#     if not os.path.exists(filename):
#         url = "https://youtube.com/clip/UgkxGAz5h_xEEG2CDtMGSNaIAJlSmxTNejxP?si=hmeTUIdmZg6azqYM"
#         urllib.request.urlretrieve(url, filename)

class TriviaApp:
    def __init__(self, root: tk.Tk):
        # ---------------------------
        # Basic setup
        # ---------------------------
        self.root: tk.Tk = root
        self.root.title("Sound of Music Trivia")
        self.root.geometry("500x400")

        # Game state
        self.name: str = ""
        self.points: int = 0
        self.questions: List[Dict[str, str]] = []
        self.current_q: int = 0
        self.correct_letter: str = ""
        self.answer_map: Dict[str, str] = {}

        # Colors
        self.bg_color: str = "#f4e4c1"
        self.button_color: str = "#8b0000"
        self.text_color: str = "#2c2c2c"

        # ---------------------------
        # Background Image
        # ---------------------------
        bg_image: Image.Image = Image.open("SoMAPic.jpg")
        # bg_image = bg_image.resize((500, 400))

        self.bg_photo: ImageTk.PhotoImage = ImageTk.PhotoImage(bg_image)

        self.bg_label: tk.Label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # self.bg_label.image_types: PhotoImage = self.bg_photo() -> tuple[str[str]]

        # ---------------------------
        # Main Frame (on top of image)
        # ---------------------------
        self.main_frame: tk.Frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # ---------------------------
        # Tkinter variables
        # ---------------------------
        self.selected: tk.StringVar = tk.StringVar(value="")

        # ---------------------------
        # Music setup
        # ---------------------------
        try:
            pygame.mixer.init()

            if os.path.exists("SoMASong.mp3"):
                pygame.mixer.music.load("SoMASong.mp3")
                pygame.mixer.music.play(-1)

        except Exception as e:
            print("Music error:", e)

    # ---------------------------
    # Start UI
    # ---------------------------
        self.show_welcome()
    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ---------------------------
    # Welcome Screen
    # ---------------------------
    def show_welcome(self):
        self.clear_screen()
        tk.Label(
            self.main_frame, 
            text="Sound of Music Trivia", 
            font=("Arial", 18),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(pady=20)
        tk.Label(
            self.main_frame, 
            text="Enter your name:"
        ).pack()
        self.name_entry = tk.Entry(self.main_frame)
        self.name_entry.pack(pady=5)
        tk.Button(
            self.main_frame, 
            text="Start",
            bg=self.button_color,
            fg="white",
            command=self.start_game
        ).pack(pady=10)
        tk.Button(
            self.main_frame, 
            text="High Scores", 
            command=self.show_high_scores
        ).pack(pady=5)

    # ---------------------------
    # Start Game
    # ---------------------------
    def start_game(self):
        self.name = self.name_entry.get().strip()
        if not self.name:
            messagebox.showwarning("Error", "Please enter your name")
            return
        self.questions = load_questions_from_csv("questions.csv") or []
        
        print("Questions loaded:", len(self.questions))
        print(self.questions[:2])
        if not self.questions:
            messagebox.showerror("Error", "No questions found!")
            return

        random.shuffle(self.questions)
        self.questions = self.questions[:10]
        self.current_q = 0
        self.points = 0
        self.show_question()

    # ---------------------------
    # Question Screen
    # ---------------------------
    def show_question(self):
        self.clear_screen()
        if self.current_q >= len(self.questions):
            self.show_results()
            return
        
        self.selected.set("")
        self.correct_letter = "A"
        q = self.questions[self.current_q]

        tk.Label(
            self.main_frame,
            text=f"Question {self.current_q + 1} of {len(self.questions)}",
            font=("Arial", 10)
        ).pack()

        question_text = q.get("question") or q.get("Question") or "Missing question"        
        tk.Label(
            self.main_frame,
            text=question_text,
            wraplength=400,
            font=("Arial", 14)
        ).pack(pady=20)

        options = [
            ("A", q.get("A", "N/A")),
            ("B", q.get("B", "N/A")),
            ("C", q.get("C", "N/A")),
            ("D", q.get("D", "N/A")),
        ]

        random.shuffle(options)

        correct_key = q.get("correct", "").strip().upper()

        if correct_key not in ("A", "B", "C", "D"):
            correct_key = "A"

        correct_text = q.get(correct_key, "") or ""

        self.correct_letter = "A"
        self.answer_map = {}

        for i, (_, text) in enumerate(options):
            new_letter = chr(65 + i)
            self.answer_map[new_letter] = text

            if text == correct_text:
                self.correct_letter = new_letter

            tk.Radiobutton(
                self.main_frame,
                text=f"{new_letter}) {text}",
                variable=self.selected,
                value=new_letter
            ).pack(anchor="w")
        
            tk.Button(
                self.main_frame,
                text="Submit",
                command=self.check_answer
            ).pack(pady=10)

    # ---------------------------
    # Check Answer
    # ---------------------------
    def check_answer(self):
        answer = self.selected.get()

        if not answer:
            messagebox.showwarning("Pick one", "Please select an answer")
            return

        if answer == self.correct_letter:
            self.points += 1
            messagebox.showinfo("Result", "Correct! 🎉")
        else:
            correct_text = self.answer_map.get(self.correct_letter, "Unknown")          
            messagebox.showinfo(
            "Result",
            f"Incorrect!\nCorrect: {self.correct_letter}) {correct_text}"
            )

        self.current_q += 1
        self.show_question()

    # ---------------------------
    # Results
    # ---------------------------
    def show_results(self):
        self.clear_screen()

        save_high_score(self.name, self.points)

        total = len(self.questions)
        percent = int((self.points / total) * 100)

        tk.Label(
            self.main_frame,
            text=f"{self.name}, Score: {self.points}/{total}",
            font=("Arial", 16)
        ).pack(pady=20)

        if percent == 100:
            msg = "Perfect! 🎉"
        elif percent >= 70:
            msg = "Great job! 👏"
        else:
            msg = "Nice try! 😊"

        tk.Label(self.main_frame, text=msg).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Play Again",
            command=self.show_welcome
        ).pack(pady=5)

    # ---------------------------
    # High Scores
    # ---------------------------
    def show_high_scores(self):
        data = read_high_scores()

        if not data:
            messagebox.showinfo("High Scores", "No scores yet!")
            return

        text = "\n".join([f"{row[0]} - {row[1]}" for row in data])
        messagebox.showinfo("Top Scores", text)

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TriviaApp(root)
    root.mainloop()