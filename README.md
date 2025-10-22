# 🎮 Wordle Game - Individual Project (Pygame)

A minimalist version of the classic Wordle puzzle game developed using Python and the Pygame library.

---

## ✨ Features

This project implements the core mechanics and features of the original Wordle game:

* **Standard Word Length:** Uses 5-letter words for guessing.
* **Limited Attempts:** Allows a maximum of 6 guesses per game.
* **Intuitive Feedback:** Provides standard color feedback (Green, Yellow, Gray) to guide the player.
* **Keyboard Input:** Supports input from the physical keyboard.
* **Visual Grid:** Displays a 6x5 game grid using Pygame graphics.
* **Valid Word Check:** Guesses are checked against a comprehensive list of allowed 5-letter words.
* **Game State Display:** Clearly shows "Win" or "Game Over" messages upon completion.

---

## ⚙️ Prerequisites

To run this game, ensure you have the following installed on your system:

1. **Python 3.x**
2. The required Python libraries (listed in 'requirements.txt').

---

## 🚀 Installation and Setup

Follow these steps in your Terminal or Command Prompt:

### 1. Download the Source Code

If you have cloned the repository, skip this step. If you received the code as a ZIP file, navigate to the extracted directory.

    '''bash
    # Optional: If downloading from GitHub
    git clone https://github.com/Lengoc06/wordle-game-python-pygame.git
    cd wordle-game-python-pygame
    '''

### 2. Install Dependencies
Install all necessary libraries using the requirements.txt file:

    '''bash
    pip install -r requirements.txt
    3. Run the Game
    Start the game using the main Python file:
    '''

    '''bash
    python main.py
    '''

---

## 🕹️ How to Play

Guessing: Type a five-letter word using your physical keyboard.

Submission: Press Enter to submit your guess.

Feedback: The game provides color feedback on your guess:

Green: Correct letter in the correct position.

Yellow: Correct letter, but in the wrong position.

Gray: Letter is not in the secret word at all.

You have 6 attempts to guess the word.

---

## 📂 Project Structure

The project is organized as follows:

.
├── main.py        # Main game loop and Pygame initialization
├── game_logic.py  # Handles core game logic (word checking, state updates)
├── ui_elements.py # Handles drawing UI components (grid, keyboard, text)
├── words.txt      # List of valid 5-letter words
└── requirements.txt # List of project dependencies

---

## 🙏 Acknowledgements
The foundational logic and Pygame structure for this project were implemented based on the concepts and guidance provided by the following tutorial series:

Primary Reference: [YouTube Playlist URL: https://www.youtube.com/playlist?list=PLOcNsDskpOqpeGonGty268I_asI2PncZm]

This implementation is an individual adaptation and application of the learned techniques.