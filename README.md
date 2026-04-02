# 🎵 Sound of Music Trivia Game

A fun, command-line trivia game inspired by *The Sound of Music*, built in Python.
Test your knowledge with randomized multiple-choice questions and track high scores!

---

## 📌 Features

* 🎮 Interactive CLI gameplay
* 🔀 Randomized question order
* 🔤 Multiple-choice questions (A/B/C/D)
* 🎯 Answer shuffling (no predictable patterns)
* 🏆 High score tracking (saved to CSV)
* 🔁 Replayable game loop
* 📊 Performance feedback after each round

---

## 🖥️ Demo

```text
--- Sound of Music Trivia Game ---
1. Play Game
2. View High Scores
3. Exit

What is the name of the main character?
A) Elsa
B) Maria
C) Anna
D) Liesl

Your answer (A/B/C/D): b
Correct! 🎉
```

---

## 📂 Project Structure

```
sound-of-music-trivia/
│
├── main.py              # Main game application
├── questions.csv       # Trivia questions database
├── high_score.csv      # Saved high scores
└── README.md           # Project documentation
```

---

## 📄 CSV Format

### `questions.csv`

```csv
question,A,B,C,D,correct
What is Maria's last name?,Rainer,Von Trapp,Schmidt,Keller,B
```

* `A–D` = answer choices
* `correct` = correct letter (A/B/C/D)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/GreyMoon128/sound-of-music-trivia.git
cd sound-of-music-trivia
```

---

### 2. Run the game

```bash
python main.py
```

---

## 🛠️ Requirements

* Python 3.10+

No external libraries required ✅

---

## 🧠 How It Works

* Questions are loaded from a CSV file
* Answers are shuffled each round
* Player input is validated
* Scores are saved with timestamps
* High scores are sorted and displayed

---

## 📈 Future Improvements

* 🎨 Add colored terminal output
* 🖥️ GUI version (Tkinter or PyQt)
* 🌐 Web-based version
* 🎚️ Difficulty levels
* ⏱️ Timed questions

---

## 👨‍💻 Author

**Henry Sanchez**
GitHub: [@GreyMoon128](https://github.com/GreyMoon128)

---

## 📜 License

This project is open source and available under the MIT License.

---

## ⭐ Acknowledgments

Inspired by the classic musical *The Sound of Music* 🎶

---
