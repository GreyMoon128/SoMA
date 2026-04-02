# Sound Of Music trivia game for mom
# Created by Henry Sanchez @GreyMoon128
import os
import time
import sys
import datetime
import random
import csv

# ---------------------------
# Utilities
# ---------------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")
    
welcome_message = [
    "************************",
    "** Sound Of Music App **",
    "************************"
]

menu_options = [
    "\n--- Sound of Music Trivia Game ---",
    "1. Play Game",
    "2. View High Scores",
    "3. Exit"
]

high_score_file = "high_score.csv"

# ---------------------------
# Player
# ---------------------------
def get_player_name() -> str:
    name = input("\nPlease enter your name: ")
    print(f"\nWelcome, {name}!")
    time.sleep(1)
    return name

# ---------------------------
# Display
# ---------------------------
def display_welcome():
    clear()
    print("\n".join(welcome_message))
    time.sleep(2)

def display_menu():
    clear()
    print("\n".join(menu_options))

# ---------------------------
# Scoring
# ---------------------------
def scoring_points(is_correct: bool, points: int) -> int:
    return points + 1 if is_correct else points

# ---------------------------
# High Score
# ---------------------------
def save_high_score(name: str, points: int) -> None:
    now = datetime.datetime.now()
    date = now.strftime("%B %d, %Y")
    time_stamp = now.strftime("%I:%M %p")

    file_exists = os.path.exists(high_score_file)

    with open(high_score_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Name", "Score", "Date", "Time"])
            
        writer.writerow([name, points, date, time_stamp])

    print(f"\nScore saved! Your current score is: {points}")
    time.sleep(1)
    
def read_high_scores() -> list[list[str]]:
    if not os.path.exists(high_score_file):
        input("\nNo high score yet! Press Enter to return to menu")
        return []

    with open(high_score_file, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    if len(reader) <= 1:
        print("\nNo high scores yet!")
        input("\nPress Enter to return to menu")
        return []

    data = reader[1:]

    # Sort by score (index 1)
    data.sort(key=lambda row: int(row[1]), reverse=True)

    print("\nTop 10 High Scores:\n")
    print(f"{'Name':<10} | {'Score':<5} | {'Date':<15} | Time")
    print("-" * 45)    
    for row in data[:10]:
        print(f"{row[0]:<10} | {row[1]:<5} | {row[2]} | {row[3]}")

    input("\nPress Enter to return to menu...")
    clear()
    return data

# ---------------------------
# Game Logic
# ---------------------------
def _play_round(name: str):
    clear()
    print("\nStarting game for mom")
    time.sleep(1)

    questions = load_questions_from_csv("questions.csv")
    random.shuffle(questions)
    questions = list[dict[str, str]](questions[:10])

    points = 0

    for question in questions:
        is_correct = _ask_single_question(question)
        points = scoring_points(is_correct, points)

    print(f"\n{name}, your final score is {points}.")
    save_high_score(name, points)
    return questions

def load_questions_from_csv(filename: str) -> list[dict[str, str]]:
    questions: list[dict[str, str]] = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        questions.extend(reader)
    return questions

def _ask_single_question(q: dict[str, str]) -> bool:
    print(f"\n{q['question']}")

    # Build list of (letter, answer)
    options = [
        ("A", q["A"]),
        ("B", q["B"]),
        ("C", q["C"]),
        ("D", q["D"]),
    ]

    # Find correct answer text
    correct_text = q[q["correct"]]

    # Shuffle options
    random.shuffle(options)

    # Display shuffled options + track new correct letter
    letter_map = {}
    new_correct_letter = ""

    for i, (_, text) in enumerate(options):
        letter = chr(65 + i)  # A, B, C, D
        letter_map[letter] = text
        print(f"{letter}) {text}")

        if text == correct_text:
            new_correct_letter = letter

    # Get user input
    answer = ""
    while answer not in ("a", "b", "c", "d"):
        answer = input("Your answer (A/B/C/D): ").lower()

    is_correct = answer.upper() == new_correct_letter

    if is_correct:
        print("Correct! 🎉")
    else:
        print(f"Incorrect! Answer: {new_correct_letter}) {letter_map[new_correct_letter]}")

    time.sleep(1)
    return is_correct

def _ask_play_again() -> bool:
    choice = ""
    while choice not in ("y", "n"):
        choice = input("\nPlay again? (y/n): ").lower()
    return choice == "y"

def play_game(name: str):
    while True:
        _play_round(name)
        if not _ask_play_again():
            break

# ---------------------------
# Main Menu
# ---------------------------
def main_menu_loop(name: str):
    while True:
        display_menu()
        try:
            choice = int(input("\nEnter choice: "))
        except ValueError:
            print("Invalid input!")
            time.sleep(1)
            continue
        if choice == 1:
            play_game(name)
        elif choice == 2:
            read_high_scores()
        elif choice == 3:
            print(f"\nThanks {name}, for playing!")
            time.sleep(1)
            sys.exit()
        else:
            print("Choose 1, 2, or 3")
            time.sleep(1)

# ---------------------------
# Main
# ---------------------------
def main():
    display_welcome()
    name = get_player_name()
    main_menu_loop(name)

if __name__ == "__main__":
    main()