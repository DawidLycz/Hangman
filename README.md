# Hangman - Word Guessing Game
Hangman is a classic and highly popular word guessing game. The objective is to guess a word by providing individual letters. At the beginning of the game, certain letters of the word are hidden behind "_" signs. The player must guess a letter, and if the word contains that letter, it will be revealed on the screen. If the guessed letter is not part of the word, the player loses a turn. The game continues until the player either successfully guesses the word or runs out of turns.
![ Alt text](gameplay_gif. gif) / ! []gameplay_gif. gif)
## Game Description
Hangman is implemented using Pygame, an open-source library for creating video games and multimedia applications in Python. Pygame provides powerful functionality for handling graphics, sound, and user input, making it an excellent choice for game development.

For more information about Pygame, visit: pygame.org

## Installation
To play the game, you can choose one of the following options:

Game Installer: Download the game installer from the link below and run it to install the game.

# [DOWNLOAD](https://github.com/DawidLycz/Hangman/releases/download/game/Hangman-setup.exe)

Pip Installation: If you prefer installing the game using pip, run the following command in your terminal or command prompt:

```bash
pip install git+https://github.com/DawidLycz/Hangman
```
After installation, you can initiate the game by executing the following command:

```bash
python -m hangman
```

There is also option to clone whole reposytory, to have full source code. In order to do that, please input following command:

```bash
git clone https://github.com/DawidLycz/Hangman
```
## How to Play
When you launch the game, an introduction message is displayed, followed by the main menu with four options:

New Game: Start a new game where you need to guess the word by providing letters via the keyboard. If you correctly guess a letter in the word, it will be revealed. Otherwise, you lose a turn. The game ends if you run out of turns (12 attempts). Successfully guessing the word rewards you with points, and a new round begins. You can quit the game anytime by pressing the "ESC" key. At the end of the game, you have the option to save your score on the leaderboard by providing your name.

Options: Open the "Options" menu to customize game settings. You can change the window resolution, enable fullscreen mode, adjust music and sound volume, and select the game language. After making your preferred settings, click the "Save" button to apply the changes. The game will restart with your chosen settings.

Top Scores: View the leaderboard by loading the "scoreboard.db" file. It displays scores sorted by the highest points. If desired, you can reset the leaderboard, which clears all previous scores.

Exit: End the game altogether.

## Code Description
The game script is "hangman.py," comprising 13 functions, each thoroughly documented within the script.

The "resolution" directory contains files with coordinates for various screen surfaces. You can modify these files using a text editor to adjust the display elements.

The "text" directory contains strings used in the game, translated into multiple languages. Similarly, you can modify these files to customize in-game text.

The "settings.db" file stores various user settings that can be adjusted from within the game's "Options" menu.

## For recruitment
In the case that you are reviewing this repository for recruitment purposes, I would like to efficiently highlight the most advanced features of the entire project.

Executable File (exe)
The game includes a generated executable file (exe), enabling easy execution on various operating systems. This means that players can quickly launch the game without the need for any additional setup.

Pygame Framework
Hangman is built on the Pygame library, a versatile tool that allows for the creation of interactive and graphical games using Python. Pygame provides a range of functionalities to manage graphics, sound, and user input, contributing to the immersive gaming experience.

Microframework for GUI
The script functions as a microframework for the game's graphical user interface (GUI). This approach simplifies the creation of user interactions within the game. By offering a lightweight GUI solution, players can engage with the game's interface seamlessly.

Event-Driven Programming
The game mechanics are driven by event-based programming. This methodology enables the game to respond dynamically to player actions in real time. Events trigger reactions, allowing for an engaging and interactive gameplay experience.

Intro with PyMovie
Hangman features an engaging intro sequence that enhances the player's experience. This intro is played using the PyMovie library, allowing for the playback of video content within the game. The intro sets the tone for the game and adds an extra layer of excitement.

Adherence to Best Practices
Throughout the development process, the project followed industry best practices. These practices include writing readable and maintainable code, designing modular components, and providing comprehensive documentation. By adhering to these standards, the project is structured for both efficient development and potential future enhancements.

Thank you for your interest in the Hangman game and its underlying technologies!

## License
This project is licensed under the MIT License. For detailed information, refer to the LICENSE.txt file.

Enjoy playing Hangman, and have fun guessing words!
