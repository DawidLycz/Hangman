import json
import os
from pathlib import Path
import random
import sys
import time
from typing import Dict, Tuple

import pygame

try:
    from hangman import intro
    from hangman.hangman_gui import Inscription, Button, Gallow, Text_box, Background
except:
    import intro
    from hangman_gui import Inscription, Button, Gallow, Text_box, Background
    
pygame.init()
TOTAL_ATTEMTPS = 12
TOTAL_SCORES_FOR_DISPLAY = 30
CLOCK = 60
LANGUAGES = ["polish", "english"]
DIRNAME = Path(os.path.dirname(__file__))

COMMON_FONT_PATH = DIRNAME / "data/fonts/font.ttf"
SETTINGS_FILE = DIRNAME / "data/settings.json"
TEMP_SETTING_FILE = DIRNAME / "data/temp_settings.json"
SCOREBOARD_FILE = DIRNAME / "data/scoreboard.json"
BUTTON_TYPE_FREE = pygame.image.load(DIRNAME / "data/images/button_1.png")
BUTTON_TYPE_AIMED = pygame.image.load(DIRNAME / "data/images/button_2.png")
BUTTON_TYPE_LOCKED = pygame.image.load(DIRNAME / "data/images/button_3.png")
BACKGROUND_1 = pygame.image.load(DIRNAME / "data/images/intro_background.jpg")
BACKGROUND_2 = pygame.image.load(DIRNAME / "data/images/menu_background.jpg")
BACKGROUND_3 = pygame.image.load(DIRNAME / "data/images/background.jpg")
BACKGROUND_4 = pygame.image.load(DIRNAME / "data/images/background_2.jpg")

KEYBOARD_INPUT = {
    pygame.K_a: ["a", "ą"],
    pygame.K_b: ["b"],
    pygame.K_c: ["c", "ć"],
    pygame.K_d: ["d"],
    pygame.K_e: ["e", "ę"],
    pygame.K_f: ["f"],
    pygame.K_g: ["g"],
    pygame.K_h: ["h"],
    pygame.K_i: ["i"],
    pygame.K_j: ["j"],
    pygame.K_k: ["k"],
    pygame.K_l: ["l", "ł"],
    pygame.K_m: ["m"],
    pygame.K_n: ["n", "ń"],
    pygame.K_o: ["o", "ó"],
    pygame.K_p: ["p"],
    pygame.K_q: ["q"],
    pygame.K_r: ["r"],
    pygame.K_s: ["s", "ś"],
    pygame.K_t: ["t"],
    pygame.K_u: ["u"],
    pygame.K_v: ["v"],
    pygame.K_w: ["w"],
    pygame.K_x: ["x"],
    pygame.K_y: ["y"],
    pygame.K_z: ["z", "ź", "ż"],
}

SOUND_EFFECTS = {
    "wrong": pygame.mixer.Sound(DIRNAME / "data/soundeffects/wrong.mp3"),
    "correct": pygame.mixer.Sound(DIRNAME / "data/soundeffects/correct.mp3"),
    "error": pygame.mixer.Sound(DIRNAME / "data/soundeffects/error.mp3"),
    "success": pygame.mixer.Sound(DIRNAME / "data/soundeffects/success.mp3"),
    "failure": pygame.mixer.Sound(DIRNAME / "data/soundeffects/game_over.mp3"),
    "beep": pygame.mixer.Sound(DIRNAME / "data/soundeffects/beep.mp3"),
    "intro": pygame.mixer.Sound(DIRNAME / "data/soundeffects/intro.mp3"),
    "outro": pygame.mixer.Sound(DIRNAME / "data/soundeffects/outro.mp3"),
}

RGB_COLORS = {
    "cyan": (0, 255, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "red": (255, 0, 0),
    "orange": (255, 100, 0),
}

RGB_Color = Tuple[int, int, int]
Coordinates = Tuple[int, int]
Position = Dict[str, Coordinates]
Scene = Dict[str, Position]

def skip_leave_action(event: pygame.event.Event, sound_channel: pygame.mixer.Channel = None) -> bool:
    """Function to handle skip or leave actions in a game.
    Parameters:
        event : The event object representing the user input event.
    Returns:
        bool: Returns True if the action should be continued, or False if the loop should be exited.

    """
    match event.type:
        case pygame.QUIT:
            pygame.quit()
            sys.exit()
        case pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if sound_channel:
                    sound_channel.stop()
                    sound_channel.play(SOUND_EFFECTS["beep"])
                return False
            else:
                return True
        case _:
            return True


def roll_the_scene(element_list: list[any]) -> bool:
    ''' Function is designed to work in while loop.
        Handle game events based on a list of interactive elements.

        This function analyzes events generated by the Pygame library and
        responds to various player actions such as key presses, mouse movement,
        and mouse clicks. Depending on the event type and the types of elements
        present in the `element_list`, it performs appropriate actions.

        At the end it displays every element which has "draw" method'''

    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                sys.exit()
            case pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                for element in element_list:
                    if isinstance(element, Text_box):
                        for key in KEYBOARD_INPUT:
                            if key == event.key:
                                element.modify(KEYBOARD_INPUT[key][0])
                        if event.key == pygame.K_BACKSPACE:
                            element.backspace()
            case pygame.MOUSEMOTION:
                for element in element_list:
                    if isinstance(element, Button):
                        element.mouse_over = element.check_mouse_over(mouse_pos)
            case pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for element in element_list:
                        if isinstance(element, Button):
                            if element.mouse_over:
                                return element.execute()

    for element in element_list:
        try:
            element.draw()
        except:
            pass
    pygame.display.flip()


def play_outro(
    screen: pygame.surface.Surface,
    score: int,
    resolution: Coordinates,
    pos: Scene,
    sound_channel: pygame.mixer.Channel,
    strings: dict[str, str],
) -> None:
    """Display the game outro screen and handle user interactions.
    Parameters:
        - strings : A dictionary containing text strings used for displaying texts on the screen.
    Description:
        Displays outro, and provides user possibility to save his game score in the "scoreboard.db" file.
    """

    def button_back() -> bool:
        sound_channel.play(SOUND_EFFECTS["beep"])
        return True

    def button_save(name: Text_box, score: int, scoreboard: list) -> bool:
        if len(name.text) > 0:
            sound_channel.play(SOUND_EFFECTS["beep"])
            object_to_save = (name.text, score)
            scoreboard.append(object_to_save)
            scoreboard = sorted(
                scoreboard[:TOTAL_SCORES_FOR_DISPLAY], key=lambda x: x[1], reverse=True)
            with open(SCOREBOARD_FILE, "w") as stream:
                json.dump(scoreboard, stream)
            return True
        else:
            sound_channel.play(SOUND_EFFECTS["error"])

    clock = pygame.time.Clock()
    pygame.mixer.music.load(DIRNAME / "data/soundeffects/outro.mp3")
    pygame.mixer.music.play()

    with open(SCOREBOARD_FILE, "r") as stream:
        scoreboard = json.load(stream)

    element_list = [Background(screen, resolution, BACKGROUND_1),
                    Text_box(pos["outro"]["text4_pos"],pos["outro"]["font3"], screen, sound_channel, font_path=COMMON_FONT_PATH)]

    button_elements = [
        ("back", button_back, ()),
        ("save", button_save, (element_list[1], score, scoreboard)),
    ]
    inscription_elements = [
        (strings["game_over"], RGB_COLORS["blue"], 2),
        (strings["congrats"] + str(score), RGB_COLORS["white"], 1),
        (strings["enter_name"], RGB_COLORS["white"], 1)
    ]
    
    text_number = 0

    for text, color, font_number in inscription_elements:
        text_number += 1
        inscription = Inscription(
            text=text,
            color=color,
            position=pos["outro"][f"text{text_number}_pos"],
            font_size=pos["outro"][f"font{font_number}"],
            screen=screen,
            font_path=COMMON_FONT_PATH,
        )
        inscription.center_x()
        element_list.append(inscription)
    counter = 1
    for name, callback, arguments in button_elements:
        button = Button(
            button_name=name,
            position=pos["outro"][f"button{counter}_pos"],
            size=pos["outro"]["button_size"],
            screen=screen,
            text=strings[name],
            font_size=pos["outro"]["button_font"],
            callback=callback,
            arguments=arguments,
        )
        counter += 1
        element_list.append(button)
    break_loop, running = False, True
    
    while running:
        break_loop = roll_the_scene(element_list)
        if break_loop:
            running = False
        clock.tick(CLOCK)


def display_letters(
    word: str,
    provided_letters: list[str],
    screen: pygame.surface.Surface,
    pos: Scene,
    height: int,
) -> None:
    """Render and display already provided letters of a word on the screen.
    Parameters:
        - word : The word to be displayed.
        - height : level on which letters suppose to be displayed on the screen

    Description:
        If the letter is not in the provided_letters set, it is replaced with an underscore ('_').
    """

    letter_font = pygame.font.Font(
        COMMON_FONT_PATH, pos["display_letters"]["font"])
    distance = 10
    for letter in word:
        if letter.upper() not in provided_letters:
            letter = "_"
        if letter == " ":
            letter = "-"
        letter_for_print = letter_font.render(
            f"{letter.upper()}", True, RGB_COLORS["green"]
        )
        screen.blit(letter_for_print, (int(distance), height))
        distance += pos["display_letters"]["distance"]


def victory_failure_display(
    screen: pygame.surface.Surface,
    sound_channel: pygame.mixer.Channel,
    pos: Scene,
    success: bool,
    strings: dict[str, str],
) -> None:
    """
    Display victory or failure message on the screen.

    Parameters:
        - success : A boolean indicating whether it is a victory (True) or failure (False).
        - strings : A dictionary containing text strings used for displaying texts on the screen.

    """
    clock = pygame.time.Clock()
    font_size = pos["victory_failure_display"]["title_font"]
    if success:
        text, ticks_to_wait, color = f"{strings['success']}", 180, RGB_COLORS["blue"]
        sound = "success"
    else:
        text, ticks_to_wait, color = f"{strings['failure']}", 450, RGB_COLORS["red"]
        sound = "failure"
    sound_channel.play(SOUND_EFFECTS[sound]),
    message = Inscription(text, color, (0, 0), font_size, screen, COMMON_FONT_PATH)
    message.center_x()
    message.center_y()

    running = True
    ticks = 0
    while running:
        for event in pygame.event.get():
            skip_leave_action(event, sound_channel)
            if event.type == pygame.KEYDOWN:
                sound_channel.stop()
                running = False
        ticks += 1
        message.draw()
        pygame.display.flip()
        if ticks == ticks_to_wait:
            running = False
        clock.tick(CLOCK)


def check_mouse(position: Coordinates, area: Coordinates, mouse_pos: Coordinates) -> bool:
    """
    Check if the mouse position is within the specified button area.

    Parameters:
        - position : The position of the top-left corner of the button area (x, y).
        - button_type : The size of the area (width, height).
        - mouse_pos : The current position of the mouse (x, y).

    Returns:
        bool: True if the mouse position is within the button area, False otherwise.

    """

    x, y = position[0], position[1]
    x_end = x + area[0]
    y_end = y + area[1]
    return int(x) <= mouse_pos[0] <= x_end and int(y) <= mouse_pos[1] <= y_end


def get_random_word(words_base: list[list[str]]) -> tuple[str, str]:
    """
    Get a random word from the given words_base.

    Returns:
        tuple: A tuple containing the randomly selected word and its category name.

    """

    category = random.choice(words_base)
    category_name, *word_base = category
    the_word = random.choice(word_base)
    return the_word, category_name


def create_screen(resolution: Coordinates, fullscreen: bool) -> pygame.surface.Surface:
    screen = pygame.display.set_mode(
        size=resolution, flags=pygame.FULLSCREEN if fullscreen else 0
    )
    pygame.display.set_caption("Hangman")
    return screen


def game_menu(
    screen: pygame.surface.Surface,
    sound_channel: pygame.mixer.Channel,
    resolution: Coordinates,
    pos: Scene,
    strings: dict[str, str],
) -> str:
    """
    Display the game menu and handle user interactions.

    Parameters:
        - strings : A dictionary of string values for different menu options and texts.

    Returns:
        str: The selected option from the game menu. One of : "new_game", "settings", "scoreboard", "exit"

    Description:
        The function continues this loop until a button option is selected.
    """
    clock = pygame.time.Clock()

    background_image = pygame.transform.scale(BACKGROUND_2, resolution)
    screen.blit(background_image, (0, 0))

    button_elements = ["new_game", "options", "top_scores", "exit"]
    button_list = []
    counter = 1
    for name in button_elements:
        button = Button(
            button_name=name,
            position=pos["game_menu"][f"button{counter}_pos"],
            size=pos["game_menu"]["button_size"],
            screen=screen,
            text=strings[name],
            font_size=pos["game_menu"]["font"],
        )
        counter += 1
        button_list.append(button)
    running = True
    while running:
        clicked = None

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            running = skip_leave_action(event)
            match event.type:
                case pygame.MOUSEMOTION:
                    for button in button_list:
                        button.mouse_over = button.check_mouse_over(mouse_pos)

                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in button_list:
                            clicked = button.react()
                            if clicked:
                                break
        if clicked:
            sound_channel.play(SOUND_EFFECTS["beep"])
            return clicked
        for button in button_list:
            button.draw()

        pygame.display.flip()
        clock.tick(CLOCK)


def leaderboard_menu(
    screen: pygame.surface.Surface,
    sound_channel: pygame.mixer.Channel,
    resolution: Coordinates,
    pos: Scene,
    strings: dict[str, str],
) -> None:
    """
    Display the leaderboard menu and handle user interactions.

    Parameters:
        - strings : A dictionary of string values for different menu options and texts.

    Description:

        Displays to user content of "scoreboard.db" file and allows to clean it.
    """

    def button_back() -> bool:
        sound_channel.play(SOUND_EFFECTS["beep"])
        return True

    def button_reset() -> bool:
        sound_channel.play(SOUND_EFFECTS["beep"])
        scoreboard = []
        with open(SCOREBOARD_FILE, "w") as stream:
            json.dump(scoreboard, stream)
        return True

    with open(SCOREBOARD_FILE, "r") as stream:
        scoreboard = json.load(stream)
    scoreboard = sorted(scoreboard, key=lambda x: x[1], reverse=True)

    clock = pygame.time.Clock()
    
    element_list = [
        Background(screen, resolution, BACKGROUND_1),
        Inscription(strings['top_scores'], RGB_COLORS["orange"], pos["leaderboard_menu"]["desc_pos"], pos["leaderboard_menu"]["desc_font"], screen, COMMON_FONT_PATH)
        ]
    element_list[1].center_x()
    button_elements = [("back", button_back),("reset", button_reset),]
    counter = 1
    for name, callback in button_elements:
        button = Button(
            button_name=name,
            position=pos["leaderboard_menu"][f"button{counter}_pos"],
            size=pos["leaderboard_menu"]["button_size"],
            screen=screen,
            text=strings[name],
            font_size=pos["leaderboard_menu"]["text_font"],
            callback=callback,
        )
        counter += 1
        element_list.append(button)
    
    height, height_change = pos["leaderboard_menu"]["height"], pos["leaderboard_menu"]["height_change"]
    height_max = pos["leaderboard_menu"]["height"] + 10 *  pos["leaderboard_menu"]["height_change"]
    score_heights = [height for height in range(height, height_max, height_change)] * 3
    score_widths = [pos["leaderboard_menu"][f"score_x{column + 1}"] for column in range(3) for i in range(10)]
    
    counter = 0
    for height, width, score in zip(score_heights, score_widths, scoreboard):
        counter += 1
        text = f"{counter:>2}. {score[0].capitalize()}: {score[1]}"
        position = (width, height)
        inscription = Inscription(text, RGB_COLORS["white"], position, pos["leaderboard_menu"]["text_font"], screen, COMMON_FONT_PATH)
        element_list.append(inscription)

    break_loop, running = False, True
    while running:
        break_loop = roll_the_scene(element_list)
        if break_loop:
            running = False
        clock.tick(CLOCK)


def settings_menu(
    screen: pygame.surface.Surface,
    settings: Scene,
    sound_channel: pygame.mixer.Channel,
    resolution: Coordinates,
    music_channel: pygame.mixer.Channel,
    pos: Scene,
    strings: dict[str, str],
) -> bool:
    """
    Display and handle the settings menu screen.

    Parameters:
        - settings : The current settings of the game.
        - strings : The dictionary of strings containing text for localization.

    Returns:
        bool: Returns True if the settings were successfully saved, False if the user chose to exit without saving.

    Description:
        Function allows user to edit "settings.db" via game interface."""

    def make_changes(new_settings: dict[str, any]) -> None:
        with open (TEMP_SETTING_FILE, "w") as stream:
            json.dump(new_settings, stream)        

    def button_swich_this_or_other(new_settings: dict[str, any], setting_key: str, setting: any) -> None:
        if new_settings[setting_key] != setting:
            sound_channel.play(SOUND_EFFECTS["beep"])
            new_settings[setting_key] = setting
        else:
            sound_channel.play(SOUND_EFFECTS["error"])
        make_changes(new_settings)

    def button_swich_yes_or_no(new_settings: dict[str, any], setting_key: str) -> None:
        sound_channel.play(SOUND_EFFECTS["beep"])
        if new_settings[setting_key] == False:
            new_settings[setting_key] = True
        elif new_settings[setting_key] == True:
            new_settings[setting_key] = False
        make_changes(new_settings)

    def button_sound_change(new_settings: dict[str, any], setting_key: str, increase: bool) -> None:
        if increase:
            if new_settings[setting_key] < 100:
                new_settings[setting_key] += 10
                sound_channel.play(SOUND_EFFECTS["beep"])
            else:
                sound_channel.play(SOUND_EFFECTS["error"])
        else:
            if new_settings[setting_key] > 0:
                sound_channel.play(SOUND_EFFECTS["beep"])
                new_settings[setting_key] -= 10
            else:
                sound_channel.play(SOUND_EFFECTS["error"])
        make_changes(new_settings)

    def button_language_change(new_settings: dict[str, any], languages: list[str], decrease: bool) -> bool:
        language_index = languages.index(new_settings["language"])
        if decrease:
            if language_index > 0:
                sound_channel.play(SOUND_EFFECTS["beep"])
                language_index -= 1
                new_settings["language"] = languages[language_index]
            else:
                sound_channel.play(SOUND_EFFECTS["error"])
        else:
            if language_index < len(languages) - 1:
                sound_channel.play(SOUND_EFFECTS["beep"])
                language_index += 1
                new_settings["language"] = languages[language_index]
            else:
                sound_channel.play(SOUND_EFFECTS["error"])
        make_changes(new_settings)

    def button_back() -> bool:
        sound_channel.play(SOUND_EFFECTS["beep"])
        os.remove(TEMP_SETTING_FILE)
        return True

    def button_save() -> bool:
        sound_channel.play(SOUND_EFFECTS["beep"])
        try:
            with open(SETTINGS_FILE, "w") as stream:
                json.dump(new_settings, stream)
        except:
            print("Something went wrong")
        return True

    new_settings = settings.copy()
    with open (TEMP_SETTING_FILE, "w") as stream:
        json.dump(new_settings, stream)
    
    button_font = pygame.font.Font(COMMON_FONT_PATH, pos["settings_menu"]["button_font"])
    element_list = [Background(screen, resolution, BACKGROUND_2)]
    button_elements = [
        ("800:600", "800:600", 1, button_swich_this_or_other, (new_settings, "resolution", [800, 600])),
        ("1200:800", "1200:800", 1, button_swich_this_or_other, (new_settings, "resolution", [1200, 800])),
        (f"{strings['fullscreen']}", "fullscreen", 1, button_swich_this_or_other, (new_settings, "fullscreen", True)),
        ("1920:1080", "1920:1080", 1, button_swich_this_or_other, (new_settings, "resolution", [1920, 1080])),
        ("1280:720", "1280:720", 1, button_swich_this_or_other, (new_settings, "resolution", [1280, 720])),
        (f"{strings['window']}", "window", 1, button_swich_this_or_other, (new_settings, "fullscreen", False)),
        (f"{strings['music']}", "music", 3, button_swich_yes_or_no, (new_settings, "play_music")),
        ("+", "music_up", 2, button_sound_change, (new_settings, "music_volume", True)),
        ("-", "music_down", 2, button_sound_change, (new_settings, "music_volume", False)),
        (f"{strings['sound']}", "sound", 3, button_swich_yes_or_no, (new_settings, "play_sound",)),
        ("+", "sound_up", 2, button_sound_change, (new_settings, "sound_volume", True)),
        ("-", "sound_down", 2, button_sound_change, (new_settings, "sound_volume", False)),
        ("<-", "previous_language", 2, button_language_change, (new_settings, LANGUAGES, True)),
        (None, "language", 3, None, None),
        ("->", "next_language", 2, button_language_change, (new_settings, LANGUAGES, False)),
        (f"{strings['back']}", "back", 3, button_back, None),
        (f"{strings['save']}", "save", 3, button_save, None),
    ]
    counter = 1
    for string, name, size, callback, arguments in button_elements:
        button = Button(
            button_name=name,
            position=pos["settings_menu"][f"button_{counter}"],
            size=pos["settings_menu"][f"button_size_{size}"],
            screen=screen,
            text=string,
            font_size=pos["settings_menu"]["button_font"],
            callback=callback,
            arguments=arguments,
        )
        counter += 1
        element_list.append(button)

    description_texts = [strings["resolution"],strings["sound"], strings["language"]]
    counter = 1
    for text in description_texts:
        position = pos["settings_menu"][f"desc_text_{counter}"]
        background_size = pos["settings_menu"]["button_size_4"]
        inscription = Inscription(text, RGB_COLORS["orange"], position, pos["settings_menu"]["desk_font"], screen, COMMON_FONT_PATH, BUTTON_TYPE_LOCKED, background_size)
        inscription.center_x()
        element_list.append(inscription)
        counter += 1

    clock = pygame.time.Clock()
    running = True
    while running:
        try:
            with open(TEMP_SETTING_FILE, "r") as stream:
                new_settings = json.load(stream)
        except:
            pass
        if new_settings["play_music"] == True:
            music_volume = str(new_settings["music_volume"]) + "%"
        else:
            music_volume = f"{strings['off']}"

        if new_settings["play_sound"] == True:
            sound_volume = str(new_settings["sound_volume"]) + "%"
        else:
            sound_volume = f"{strings['off']}"

        language_index = LANGUAGES.index(new_settings["language"])

        element_list[7].rendered_text = button_font.render(
            f"{strings['music']}: {music_volume}", True, RGB_COLORS["black"]
        )
        element_list[10].rendered_text = button_font.render(
            f"{strings['sound']}: {sound_volume}", True, RGB_COLORS["black"]
        )
        element_list[14].rendered_text = button_font.render(
            strings["languages_list"][language_index], True, RGB_COLORS["black"]
        )

        if new_settings["play_music"]:
            music_channel.set_volume(new_settings["music_volume"] / 200)
        else:
            music_channel.set_volume(0)

        if new_settings["play_sound"]:
            sound_channel.set_volume(new_settings["sound_volume"] / 100)
        else:
            sound_channel.set_volume(0)

        button_lock_condidions = [
            new_settings["resolution"] == [800, 600],
            new_settings["resolution"] == [1200, 800],
            new_settings["fullscreen"] == True,
            new_settings["resolution"] == [1920, 1080],
            new_settings["resolution"] == [1280, 720],
            new_settings["fullscreen"] == False,
            new_settings["play_music"] == False,
            new_settings["music_volume"] == 100,
            new_settings["music_volume"] == 0,
            new_settings["play_sound"] == False,
            new_settings["sound_volume"] == 100,
            new_settings["sound_volume"] == 0,
            language_index == 0,
            True,
            language_index == len(LANGUAGES) - 1,
        ]

        for condition, button in zip(button_lock_condidions, element_list[1:16]):
            if condition:
                button.disabled = True
            else:
                button.disabled = False

        break_loop = roll_the_scene(element_list)
        if break_loop:
            return False
        clock.tick(CLOCK)


def game_round(
    screen: pygame.surface.Surface,
    the_word: str,
    category_name: str,
    score: int,
    sound_channel: pygame.mixer.Channel,
    resolution: Coordinates,
    pos: Scene,
    strings: dict[str, str],
) -> int:
    """
    Run a game round where the player guesses letters to complete a word.

    Parameters:
        strings : The dictionary of strings containing text for localization.

    Returns:
        int: The score obtained in the game round.

    Description:
        This function runs a game round where the player guesses letters to complete a word.
        If the player guesses an incorrect letter, the gallow image is updated to reflect the number of incorrect attempts.
    """
    background_image = pygame.transform.scale(BACKGROUND_4, resolution)

    screen.blit(background_image, (0, 0))

    provided_letters = set()
    correct_letters = set()
    password_words = the_word.split()
    password_letters = [letter for letter in the_word.upper()]
    if " " in password_letters:
        provided_letters.add(" ")
        correct_letters.add(" ")
    clock = pygame.time.Clock()
    attempts = 0
    running = True
    inscription_list = []
    inscription_elements = ((f"{strings['category']} {category_name.upper()}", pos["game_round"]["category_info"]),
                            (f"{strings['score']} {score}", pos["game_round"]["score_info"]))
    for text, position in inscription_elements:
        inscription = Inscription(text, RGB_COLORS["green"], position, pos["game_round"]["font"], screen, COMMON_FONT_PATH)
        inscription_list.append(inscription)
    
    gallow = Gallow(pos["game_round"]["gallow_background_size"],
                    pos["game_round"]["gallow_background_pos"],
                    pos["game_round"]["gallow_size"],
                    pos["game_round"]["gallow_pos"],
                    screen)
    while running:

        provided_keys = False
        for event in pygame.event.get():
            running = skip_leave_action(event)
            if event.type == pygame.KEYDOWN:
                for key in KEYBOARD_INPUT:
                    if key == event.key:
                        provided_keys = KEYBOARD_INPUT[key]
                        provided_keys = [key.upper() for key in provided_keys]
                        if any(letter.upper() in provided_letters for letter in provided_keys):
                            sound_channel.play(SOUND_EFFECTS["error"])
                        elif any(letter.upper() in password_letters for letter in provided_keys):
                            sound_channel.play(SOUND_EFFECTS["correct"])
                            correct_letters.update(provided_keys)
                            provided_letters.update(provided_keys)
                        else:
                            sound_channel.play(SOUND_EFFECTS["wrong"])
                            attempts += 1
                            gallow.increase() 

        # Display content on screen
        gallow.draw()

        for insc in inscription_list:
            insc.draw()

        height = pos["game_round"]["height"]
        for word in password_words:
            display_letters(word, provided_letters, screen, pos, height)
            height += pos["game_round"]["height"]

        # Check win or lose conditions
        if set(password_letters) <= correct_letters:
            victory_failure_display(screen, sound_channel, pos, True, strings)
            score = TOTAL_ATTEMTPS - attempts
            return score
        if attempts == TOTAL_ATTEMTPS:
            victory_failure_display(screen, sound_channel, pos, False, strings)
            break

        pygame.display.flip()
        clock.tick(60)


def main() -> False:
    """
    The main function that serves as the entry point of the program.
    Whole function is looped in to "while True" loop.
    Initially it is loading settings file and assing its content to constant.
    Next, it is initialize function "play_intro".
    Than it "initialize" game screen with parameters based on constant mentionet above.
    And at last it enters inner loop. Which is based on "main_menu" function, and based on what this function returns, it runs certain operations.
    """

    while True:
        with open(SETTINGS_FILE, "r") as stream:
            settings = json.load(stream)

        resolution = settings["resolution"]
        res_for_path = f"{resolution[0]}_{resolution[1]}"
        file_with_numbers = DIRNAME / f"data/resolutions/{res_for_path}.json"

        with open(file_with_numbers, "r") as stream:
            pos = json.load(stream)
        language = settings["language"]
        with open(DIRNAME / f"data/text/{language}_strings.json", "r", encoding="utf-8") as stream:
            strings = json.load(stream)
        with open(DIRNAME / f"data/text/{language}_key_words.json", "r", encoding="utf-8") as stream:
            words_base = json.load(stream)

        screen = create_screen(resolution, settings["fullscreen"])

        music_channel = pygame.mixer.Channel(0)
        music = pygame.mixer.Sound(DIRNAME / "data/soundeffects/music.mp3")
        music_channel.set_volume(settings["music_volume"] / 200)

        sound_channel = pygame.mixer.Channel(1)
        if settings["play_sound"] == True:
            sound_channel.set_volume(settings["sound_volume"] / 100)
        else:
            sound_channel.set_volume(0)

        while True:
            if settings["play_music"] == True:
                music_channel.play(music)
            else:
                music_channel.stop()
            clicked = game_menu(screen, sound_channel, resolution, pos, strings)
            match clicked:
                case "new_game":
                    score = 0
                    while True:
                        the_word, category_name = get_random_word(words_base)
                        new_score = game_round(
                            screen,
                            the_word,
                            category_name,
                            score,
                            sound_channel,
                            resolution,
                            pos,
                            strings,
                        )
                        if new_score:
                            score += new_score
                        else:
                            break
                    play_outro(screen, score, resolution, pos, sound_channel, strings)
                case "options":
                    settings_menu(
                        screen,
                        settings,
                        sound_channel,
                        resolution,
                        music_channel,
                        pos,
                        strings,
                    )
                    if Path(TEMP_SETTING_FILE).exists():
                        pygame.display.quit()
                        os.remove(TEMP_SETTING_FILE)
                        time.sleep(SOUND_EFFECTS["beep"].get_length())
                        break
                case "top_scores":
                    leaderboard_menu(screen, sound_channel, resolution, pos, strings)
                case "exit":
                    break
        if clicked == "exit":
            time.sleep(SOUND_EFFECTS["beep"].get_length())
            break


if __name__ == "__main__":
    main()
