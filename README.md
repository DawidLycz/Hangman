# Hangman

"Hangman" is a highly popular game where the objective is to guess a word by providing individual letters. Initially, certain letters of the word are hidden behind "_" signs. The user must provide a letter, and if the word contains that letter, it will be revealed on the screen. Otherwise, the user will lose a turn. If the user loses 12 turns, they lose the game.

The game utilizes Pygame, an open-source library for creating video games and multimedia applications in Python. Pygame provides functionality for handling graphics, sound, and user input, making it a powerful tool for game development.

You can find more information about Pygame at: [pygame.org](https://www.pygame.org/wiki/about)

The main script is "hangman.py", which consists of 12 functions that are described in detail in the script's documentation.

The files starting with "resolution" contain coordinates for each surface to be displayed on the screen. These files can be reviewed and modified using "Hangman_numbers_loader.py". To make changes, update the specific data directly in the code and run the script to overwrite the database file. The resolution of the game window is based on certain settings.

The "strings.db" file works similarly, containing lists of words that could appear as passwords in the game. It also includes every string that appears in the game. The reason for using a database file is to support two possible languages: English and Polish. You can review and modify the file using "Hangman_text_handler.py". Again, make changes directly in the code. The language used in the game is based on specific settings.

The "settings.db" file is a dictionary that contains various settings. Users can modify these settings directly in the main script under the "settings" section.

When the main script is executed, an intro message is displayed, followed by the main menu. The menu offers four options:

1. "New Game": Starts a new game where the user must provide letters (via the keyboard) to guess the password. Incorrect letters result in the loss of an attempt, and when the user reaches 12 unsuccessful attempts, they lose the game. If the user correctly guesses all the letters in the password, they win the round, and the remaining attempts are converted into points that are added to the total score. A new round begins. The game continues until the user loses or presses the "ESC" key. After the game ends, the option to save the score appears on the screen. Users can provide their name to save the score to the leaderboard or skip this step. Finally, the main menu appears again.

2. "Options": Opens the "Options" menu where users can modify game settings to their preference. They can change the window resolution, enable fullscreen mode, adjust music and sound volume, and select the game language. To apply changes, users click on their preferred settings and then click the "Save" button in the bottom right corner. This will modify the "settings.db" file, restart the script, and display the main menu with the preferred settings.

3. "Top Scores": Displays the leaderboard by loading the "scoreboard.db" file. The leaderboard shows the contents of "scoreboard.db" sorted by score. There is also an option to reset the leaderboard, which simply overwrites "scoreboard.db" with an empty file.

4. "Exit": Ends the script altogether.

I hope this provides a comprehensive overview of the Hangman game and its functionality. Enjoy playing!