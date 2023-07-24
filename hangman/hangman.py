from enum import Enum, auto
import json
import os
import pickle
import random
import sys
import time
from typing import Dict, Tuple


import pygame

pygame.init()

TOTAL_ATTEMTPS = 12
TOTAL_SCORES_FOR_DISPLAY = 30
CLOCK = 60

SETTINGS_FILE = os.path.join(
    os.path.dirname(__file__), "data", "databases", "settings.db"
)
SCOREBOARD_FILE = os.path.join(
    os.path.dirname(__file__), "data", "databases", "scoreboard.db"
)

BUTTON_TYPE_FREE = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "data", "images", "button_1.png")
)
BUTTON_TYPE_AIMED = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "data", "images", "button_2.png")
)
BUTTON_TYPE_LOCKED = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "data", "images", "button_3.png")
)

BACKGROUND_1 = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "data", "images", "intro_background.jpg")
)
BACKGROUND_2 = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "data", "images", "menu_background.jpg")
)
BACKGROUND_3 = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "data", "images", "background.jpg")
)
BACKGROUND_4 = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "data", "images", "background_2.jpg")
)
BACKGROUND_5 = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "data", "images", "gallow_background.jpg")
)

COMMON_FONT_PATH = os.path.join(os.path.dirname(__file__), "data", "fonts", "font.ttf")

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
    "wrong": pygame.mixer.Sound(
        os.path.join(os.path.dirname(__file__), "data", "soundeffects", "wrong.mp3")
    ),
    "correct": pygame.mixer.Sound(
        os.path.join(os.path.dirname(__file__), "data", "soundeffects", "correct.mp3")
    ),
    "error": pygame.mixer.Sound(
        os.path.join(os.path.dirname(__file__), "data", "soundeffects", "error.mp3")
    ),
    "success": pygame.mixer.Sound(
        os.path.join(os.path.dirname(__file__), "data", "soundeffects", "success.mp3")
    ),
    "failure": pygame.mixer.Sound(
        os.path.join(os.path.dirname(__file__), "data", "soundeffects", "game_over.mp3")
    ),
    "beep": pygame.mixer.Sound(
        os.path.join(os.path.dirname(__file__), "data", "soundeffects", "beep.mp3")
    ),
    "intro": pygame.mixer.Sound(
        os.path.join(os.path.dirname(__file__), "data", "soundeffects", "intro.mp3")
    ),
    "outro": pygame.mixer.Sound(
        os.path.join(os.path.dirname(__file__), "data", "soundeffects", "outro.mp3")
    ),
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


Coordinates = Tuple[int, int]
Position = Dict[str, Coordinates]
Scene = Dict[str, Position]

class Button:
    def __init__(
        self,
        button_name: str,
        button_list: list[any],
        position: Coordinates,
        size: Coordinates,
        mouse_over: bool,
        screen: pygame.surface.Surface,
        lock:  bool,
        text: str,
        text_color: tuple[int, int, int],
        font_size: int
    ):
        self.button_name = button_name
        self.position = position
        self.size = size
        self.mouse_over = mouse_over
        self.screen = screen
        self.lock = lock
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        
        button_list.append(self)
        font = pygame.font.Font(COMMON_FONT_PATH, font_size)
        rendered_text = font.render(text, True, text_color)
        self.rendered_text = rendered_text

    def check_mouse_over(self, mouse_position):
        if (
            self.position[0] <= mouse_position[0] <= self.position[0] + self.size[0]
            and self.position[1] <= mouse_position[1] <= self.position[1] + self.size[1]
        ):
            return True
        return False
    
    def react(self):
        if self.mouse_over:
            return self.button_name

    def draw(self):
        if self.lock:
            image = BUTTON_TYPE_LOCKED
        else:
            if self.mouse_over:
                image = BUTTON_TYPE_AIMED
            else:
                image = BUTTON_TYPE_FREE
        image = pygame.transform.scale(image, (self.size))
        text_rect = self.rendered_text.get_rect()
        text_rect.center = (
                    self.position[0] + (self.size[0] // 2),
                    self.position[1] + (self.size[1] // 2),
                )
        self.screen.blit(image, self.position,)
        self.screen.blit(self.rendered_text, text_rect)


def skip_leave_action(
    event: pygame.event.Event, sound_channel: pygame.mixer.Channel = None
) -> bool:
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


def play_intro(
    screen: pygame.surface.Surface,
    resolution: Coordinates,
    pos: Scene,
    strings: list[str],
    sound_channel: pygame.mixer.Channel,
) -> None:
    """Initial function for whole game. Displays welcome messege in the surface provided in argument"""

    background_image = pygame.transform.scale(BACKGROUND_1, (resolution))
    screen.blit(background_image, (0, 0))
    clock = pygame.time.Clock()
    ticks = 0
    sound_channel.play(SOUND_EFFECTS["intro"])
    running = True
    while running:
        ticks += 1
        for event in pygame.event.get():
            running = skip_leave_action(event, sound_channel)

        if ticks == 55:
            title_font = pygame.font.Font(COMMON_FONT_PATH, pos["intro"]["font1"])
            main_title = title_font.render("Hangman", True, RGB_COLORS["cyan"])
            screen.blit(main_title, pos["intro"]["text1"])

        if ticks == 110:
            description_font = pygame.font.Font(None, pos["intro"]["font2"])
            description_text_1 = description_font.render(
                f"{strings['welcome_1']}", True, RGB_COLORS["white"]
            )
            screen.blit(description_text_1, pos["intro"]["text2"])

        if ticks == 160:
            description_text_2 = description_font.render(
                f"{strings['welcome_2']}", True, RGB_COLORS["white"]
            )
            screen.blit(description_text_2, pos["intro"]["text3"])

        if ticks == 500:
            return None
        clock.tick(CLOCK)
        pygame.display.flip()
    pygame.mixer.music.stop()


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

    clock = pygame.time.Clock()
    pygame.mixer.music.load(
        os.path.join(os.path.dirname(__file__), "data", "soundeffects", "outro.mp3")
    )
    pygame.mixer.music.play()

    with open(SCOREBOARD_FILE, "rb") as stream:
        scoreboard = pickle.load(stream)

    background_image = pygame.transform.scale(BACKGROUND_1, (resolution))
    screen.blit(background_image, (0, 0))

    description_font = pygame.font.Font(COMMON_FONT_PATH, pos["outro"]["description_font"])
    title_font = pygame.font.Font(COMMON_FONT_PATH, pos["outro"]["title_font"])
    name_font = pygame.font.Font(COMMON_FONT_PATH, pos["outro"]["name_font"])

    main_title = title_font.render(strings["game_over"], True, RGB_COLORS["blue"])
    description_score = description_font.render(
        f"{strings['congrats']} {score} ", True, RGB_COLORS["white"]
    )
    description_name = description_font.render(
        f"{strings['enter_name']}", True, RGB_COLORS["white"]
    )
    button_list = []
    button_elements = ["back", "save",]
    counter = 1
    for name in button_elements:
        Button(button_name=name, 
                button_list=button_list, 
                position=pos["outro"][f"button{counter}_pos"],
                size=pos["outro"]["button_size"], 
                mouse_over=False,
                screen=screen,
                lock=False, 
                text=strings[name], 
                text_color=RGB_COLORS["black"], 
                font_size=pos["outro"]["button_font"])
        counter += 1

    name_latters = []
    running = True
    while running:
        clicked = None
        for event in pygame.event.get():
            running = skip_leave_action(event, sound_channel)
            mouse_pos = pygame.mouse.get_pos()
            
            match event.type:
                case pygame.KEYDOWN:
                    if len(name_latters) < 11:
                        for key in KEYBOARD_INPUT:
                            if key == event.key:
                                sound_channel.play(SOUND_EFFECTS["beep"])
                                name_latters.append(KEYBOARD_INPUT[key][0])
                    if event.key == pygame.K_BACKSPACE:
                        try:
                            del name_latters[-1]
                            sound_channel.play(SOUND_EFFECTS["wrong"])
                        except:
                            sound_channel.play(SOUND_EFFECTS["error"])

                case pygame.MOUSEMOTION:
                    for button in button_list:
                        button.mouse_over = button.check_mouse_over(mouse_pos)

                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in button_list:
                            clicked = button.react()
                            if clicked:
                                break

        match clicked:
            case "back":
                sound_channel.play(SOUND_EFFECTS["beep"])
                running = False
            case "save":
                if len(name_latters) > 0:
                    sound_channel.play(SOUND_EFFECTS["beep"])
                    to_save = (name, score)
                    scoreboard.append(to_save)
                    scoreboard = sorted(
                        scoreboard[:30], key=lambda x: x[1], reverse=True
                    )
                    with open(SCOREBOARD_FILE, "wb") as stream:
                        pickle.dump(scoreboard, stream)
                    return None
                else:
                    sound_channel.play(SOUND_EFFECTS["error"])

        name = "".join(name_latters)
        name_title = name_font.render(f"{name.upper()}", True, RGB_COLORS["green"])

        for button in button_list:
            button.draw()
        screen.blit(main_title, pos["outro"]["title_pos"])
        screen.blit(description_score, pos["outro"]["score_pos"])
        screen.blit(description_name, pos["outro"]["desc_pos"])
        screen.blit(name_title, pos["outro"]["name_pos"])

        pygame.display.flip()
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
        - provided_letters : A set of letters that are already provided.
        - height : level on which letters suppose to be displayed on the screen

    Description:
        If the letter is not in the provided_letters set, it is replaced with an underscore ('_').
        If the letter is a space, it is replaced with a ('-').
    """

    letter_font = pygame.font.Font(COMMON_FONT_PATH, pos["display_letters"]["font"])
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
    strings: list[str],
) -> None:
    """
    Display victory or failure message on the screen.

    Parameters:
        - success : A boolean indicating whether it is a victory (True) or failure (False).
        - strings : A list containing text strings used for displaying texts on the screen.

    """
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(
        COMMON_FONT_PATH, pos["victory_failure_display"]["title_font"]
    )
    if success:
        text, ticks_to_wait, color = f"{strings['success']}", 180, RGB_COLORS["blue"]
        sound_channel.play(SOUND_EFFECTS["success"])
    else:
        text, ticks_to_wait, color = f"{strings['failure']}", 450, RGB_COLORS["red"]
        sound_channel.play(SOUND_EFFECTS["failure"]),
    main_title = title_font.render(text, True, color)
    running = True
    ticks = 0
    while running:
        for event in pygame.event.get():
            skip_leave_action(event, sound_channel)
            if event.type == pygame.KEYDOWN:
                running = False
                sound_channel.stop()
        ticks += 1
        screen.blit(main_title, (pos["victory_failure_display"]["title"]))
        pygame.display.flip()
        if ticks == ticks_to_wait:
            running = False
        clock.tick(CLOCK)
        print(ticks)


def check_mouse(
    position: Coordinates, button_type: Coordinates, mouse_pos: Coordinates
) -> bool:
    """
    Check if the mouse position is within the specified button area.

    Parameters:
        - position : The position of the top-left corner of the button area (x, y).
        - button_type : The size of the button area (width, height).
        - mouse_pos : The current position of the mouse (x, y).

    Returns:
        bool: True if the mouse position is within the button area, False otherwise.

    """

    x, y = position[0], position[1]
    x_end = x + button_type[0]
    y_end = y + button_type[1]
    return int(x) <= mouse_pos[0] <= x_end and int(y) <= mouse_pos[1] <= y_end


def get_random_word(words_base: list[list[str]]) -> tuple[str, str]:
    """
    Get a random word from the given words_base.

    Returns:
        tuple[str]: A tuple containing the randomly selected word and its category name.

    """

    category = random.choice(words_base)
    category_name, *word_base = category
    the_word = random.choice(word_base)
    return the_word, category_name


def create_screen(resolution: Coordinates, fullscreen: bool) -> pygame.surface.Surface:
    return pygame.display.set_mode(
        size=(resolution), flags=pygame.FULLSCREEN if fullscreen else 0
    )


def game_menu(
    screen: pygame.surface.Surface,
    sound_channel: pygame.mixer.Channel,
    resolution: Coordinates,
    pos: Scene,
    strings: list[str],
) -> str:
    """
    Display the game menu and handle user interactions.

    Parameters:
        - strings : A list of string values for different menu options and texts.

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
        Button(button_name=name, 
                button_list=button_list, 
                position=pos["game_menu"][f"button{counter}_pos"],
                size=pos["game_menu"]["button_size"], 
                mouse_over=False,
                screen=screen,
                lock=False, 
                text=strings[name], 
                text_color=RGB_COLORS["black"], 
                font_size=pos["game_menu"]["font"])
        counter += 1
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
    strings: list[str],
) -> None:
    """
    Display the leaderboard menu and handle user interactions.

    Parameters:
        - strings : A list of string values for different menu options and texts.

    Description:

        Displays to user content of "scoreboard.db" file and allows to clean it.
    """
    with open(SCOREBOARD_FILE, "rb") as stream:
        scoreboard = pickle.load(stream)
    scoreboard = sorted(scoreboard, key=lambda x: x[1], reverse=True)

    clock = pygame.time.Clock()
    background_image = pygame.transform.scale(BACKGROUND_1, resolution)
    screen.blit(background_image, (0, 0))

    description_font = pygame.font.Font(
        COMMON_FONT_PATH, pos["leaderboard_menu"]["desc_font"]
    )
    text_font = pygame.font.Font(COMMON_FONT_PATH, pos["leaderboard_menu"]["text_font"])

    description_text = description_font.render(
        f"{strings['top_scores']}", True, RGB_COLORS["orange"]
    )
    description_text_rect = description_text.get_rect()
    description_text_rect.center = (
        resolution[0] // 2,
        pos["leaderboard_menu"]["desc_pos"][1] * 3,
    )

    screen.blit(description_text, description_text_rect)
    button_list = []
    button_elements = ["back", "reset",]
    counter = 1
    for name in button_elements:
        Button(button_name=name, 
                button_list=button_list, 
                position=pos["leaderboard_menu"][f"button{counter}_pos"],
                size=pos["leaderboard_menu"]["button_size"], 
                mouse_over=False,
                screen=screen,
                lock=False, 
                text=strings[name], 
                text_color=RGB_COLORS["black"], 
                font_size=pos["leaderboard_menu"]["text_font"])
        counter += 1

    running = True
    while running:
        clicked = None
        for event in pygame.event.get():
            running = skip_leave_action(event, sound_channel)
            mouse_pos = pygame.mouse.get_pos()
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

        match clicked:
            case "back":
                sound_channel.play(SOUND_EFFECTS["beep"])
                running = False
            case "reset":
                sound_channel.play(SOUND_EFFECTS["beep"])
                scoreboard = []
                with open(SCOREBOARD_FILE, "wb") as stream:
                    pickle.dump(scoreboard, stream)
                running = False

        height, counter1, counter2 = pos["leaderboard_menu"]["height"], 0, 1
        for name, score in scoreboard[:TOTAL_SCORES_FOR_DISPLAY]:
            counter1 += 1
            score_text = text_font.render(
                f"{counter1:2}. {name.capitalize():<12}{score}", True, RGB_COLORS["white"]
            )
            screen.blit(
                score_text, (pos["leaderboard_menu"][f"score_x{counter2}"], height)
            )
            height += pos["leaderboard_menu"]["height_change"]
            if counter1 in [10, 20]:
                counter2 += 1
                height = pos["leaderboard_menu"]["height"]
        for button in button_list:
            button.draw()

        pygame.display.flip()
        clock.tick(CLOCK)


def settings_menu(
    screen: pygame.surface.Surface,
    settings: Scene,
    sound_channel: pygame.mixer.Channel,
    resolution: Coordinates,
    music_channel: pygame.mixer.Channel,
    pos: Scene,
    strings: list[str],
) -> bool:
    """
    Display and handle the settings menu screen.

    Parameters:
        - settings : The current settings of the game.
        - strings : The list of strings containing text for localization.

    Returns:
        bool: Returns True if the settings were successfully saved, False if the user chose to exit without saving.

    Description:
        Function allows user to edit "settings.db" via game interface."""
    clock = pygame.time.Clock()
    new_settings = settings.copy()
    background_image = pygame.transform.scale(BACKGROUND_2, (resolution))
    description_button_font = pygame.font.Font(
        COMMON_FONT_PATH, pos["settings_menu"]["desk_font"]
    )
    button_font = pygame.font.Font(
        COMMON_FONT_PATH, pos["settings_menu"]["button_font"]
    )
    languages = ["polish", "english"]

    language_index = 0

    for language in languages:
        if language == new_settings["language"]:
            break
        else:
            language_index += 1

    button_list = []
    button_elements = [
        ("800:600", "800:600", 1),
        ("1200:800", "1200:800", 1),
        (f"{strings['fullscreen']}", "fullscreen", 1),
        ("1920:1080","1920:1080", 1),
        ("1280:720","1280:720", 1),
        (f"{strings['window']}","window", 1),
        (f"{strings['music']}","music", 3),
        ("+", "music_up", 2),
        ("-", "music_down", 2),
        (f"{strings['sound']}", "sound", 3),
        ("+", "sound_up", 2),
        ("-", "sound_down", 2),
        ("<-", "previous_language", 2),
        (None,"language", 3),
        ("->", "next_language", 2),
        (f"{strings['back']}", "back", 3),
        (f"{strings['save']}", "save", 3),
    ]
    counter = 1
    for string, name, size in button_elements:
        Button(button_name=name, 
                button_list=button_list, 
                position=pos["settings_menu"][f"button_{counter}"],
                size=pos["settings_menu"][f"button_size_{size}"], 
                mouse_over=False,
                screen=screen,
                lock=False, 
                text=string, 
                text_color=RGB_COLORS["black"], 
                font_size=pos["settings_menu"]["button_font"])
        counter += 1
    description_texts = [strings["resolution"], strings["sound"], strings["language"]]
    description_button = pygame.transform.scale(
        BUTTON_TYPE_LOCKED, pos["settings_menu"]["button_size_4"]
    )

    screen.blit(background_image, (0, 0))

    counter = 1
    for text in description_texts:
        text = description_button_font.render(f"{text}", True, RGB_COLORS["orange"])
        screen.blit(description_button, pos["settings_menu"][f"desc_button_{counter}"])
        screen.blit(text, pos["settings_menu"][f"desc_text_{counter}"])
        counter += 1

    running = True
    
    while running:
        clicked = None

        if new_settings["play_music"] == True:
            music_volume = str(new_settings["music_volume"]) + "%"
        else:
            music_volume = f"{strings['off']}"

        if new_settings["play_sound"] == True:
            sound_volume = str(new_settings["sound_volume"]) + "%"
        else:
            sound_volume = f"{strings['off']}"

        button_list[6].rendered_text = button_font.render(
            f"{strings['music']}: {music_volume}", True, RGB_COLORS["black"])
        button_list[9].rendered_text = button_font.render(
            f"{strings['sound']}: {sound_volume}", True, RGB_COLORS["black"])
        button_list[13].rendered_text = button_font.render(strings["languages_list"][language_index],True, RGB_COLORS["black"])
        if new_settings["play_music"]:
            music_channel.set_volume(new_settings["music_volume"] / 200)
        else:
            music_channel.set_volume(0)

        if new_settings["play_sound"]:
            sound_channel.set_volume(new_settings["sound_volume"] / 100)
        else:
            sound_channel.set_volume(0)

        for event in pygame.event.get():
            running = skip_leave_action(event, sound_channel)
            mouse_pos = pygame.mouse.get_pos()
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

        match clicked:
            case "800:600":
                if new_settings["resolution"] != [800, 600]:
                    sound_channel.play(SOUND_EFFECTS["beep"])
                    new_settings["resolution"] = [800, 600]
                else:
                    sound_channel.play(SOUND_EFFECTS["error"])
            case "1200:800":
                if new_settings["resolution"] != [1200, 800]:
                    sound_channel.play(SOUND_EFFECTS["beep"])
                    new_settings["resolution"] = [1200, 800]
                else:
                    sound_channel.play(SOUND_EFFECTS["error"])
            case "fullscreen":
                if new_settings["fullscreen"] == False:
                    sound_channel.play(SOUND_EFFECTS["beep"])
                    new_settings["fullscreen"] = True
                else:
                    sound_channel.play(SOUND_EFFECTS["error"])
            case "1920:1080":
                if new_settings["resolution"] != [1920, 1080]:
                    sound_channel.play(SOUND_EFFECTS["beep"])
                    new_settings["resolution"] = [1920, 1080]
                else:
                    sound_channel.play(SOUND_EFFECTS["error"])
            case "1280:720":
                if new_settings["resolution"] != [1280, 720]:
                    sound_channel.play(SOUND_EFFECTS["beep"])
                    new_settings["resolution"] = [1280, 720]
                else:
                    sound_channel.play(SOUND_EFFECTS["error"])
            case "window":
                if new_settings["fullscreen"] == True:
                    sound_channel.play(SOUND_EFFECTS["beep"])
                    new_settings["fullscreen"] = False
                else:
                    sound_channel.play(SOUND_EFFECTS["error"]) 
            case "music":               
                sound_channel.play(SOUND_EFFECTS["beep"])
                if new_settings["play_music"] == False:
                    new_settings["play_music"] = True
                elif new_settings["play_music"] == True:
                    new_settings["play_music"] = False
            case "music_up":
                if new_settings["music_volume"] < 100:
                    sound_channel.play(SOUND_EFFECTS["beep"])
                    new_settings["music_volume"] += 10
                else:
                    sound_channel.play(SOUND_EFFECTS["error"])  
            case "music_down":
                if new_settings["music_volume"] > 0:
                    sound_channel.play(SOUND_EFFECTS["beep"])
                    new_settings["music_volume"] -= 10
                else:
                    sound_channel.play(SOUND_EFFECTS["error"])     
            case "sound":           
                sound_channel.play(SOUND_EFFECTS["beep"])
                if new_settings["play_sound"] == False:
                    new_settings["play_sound"] = True
                elif new_settings["play_sound"] == True:
                    new_settings["play_sound"] = False
            case "sound_up":
                if new_settings["sound_volume"] < 100:
                    new_settings["sound_volume"] += 10
                    sound_channel.play(SOUND_EFFECTS["beep"])
                else:
                    sound_channel.play(SOUND_EFFECTS["error"])
            case "sound_down":
                if new_settings["sound_volume"] > 0:
                    new_settings["sound_volume"] -= 10
                    sound_channel.play(SOUND_EFFECTS["beep"])
                else:
                    sound_channel.play(SOUND_EFFECTS["error"])
            case "previous_language" : 
                if language_index > 0:
                    sound_channel.play(SOUND_EFFECTS["beep"])
                    language_index -= 1
                    new_settings["language"] = languages[language_index]
                else:
                    sound_channel.play(SOUND_EFFECTS["error"])
            case "language":
                pass
            case "next_language":
                if language_index < len(languages) - 1:
                    sound_channel.play(SOUND_EFFECTS["beep"])
                    language_index += 1
                    new_settings["language"] = languages[language_index]
                else:
                    sound_channel.play(SOUND_EFFECTS["error"])
            case "back":
                sound_channel.play(SOUND_EFFECTS["beep"])
                return False
            case "save":
                sound_channel.play(SOUND_EFFECTS["beep"])
                try:
                    with open(SETTINGS_FILE, "wb") as stream:
                        pickle.dump(new_settings, stream)
                    return True
                except:
                    print("Something went wrong")                

        button_lock_condidions = [
            (new_settings["resolution"] == [800, 600]),
            (new_settings["resolution"] == [1200, 800]),
            (new_settings["fullscreen"] == True),
            (new_settings["resolution"] == [1920, 1080]),
            (new_settings["resolution"] == [1280, 720]),
            (new_settings["fullscreen"] == False),
            (new_settings["play_music"] == False),
            (new_settings["music_volume"] == 100),
            (new_settings["music_volume"] == 0),
            (new_settings["play_sound"] == False),
            (new_settings["sound_volume"] == 100),
            (new_settings["sound_volume"] == 0),
            (language_index == 0),
            (True),
            (language_index == len(languages) - 1),
        ]

        counter = 0
        for condition, button in zip(button_lock_condidions, button_list):
            if condition:
                button.lock = True
            else:
                button.lock = False
            counter += 1

        
        for button in button_list:
            button.draw()

        pygame.display.flip()
        clock.tick(CLOCK)


def game_round(
    screen: pygame.surface.Surface,
    the_word: str,
    category_name: str,
    score: int,
    sound_channel: pygame.mixer.Channel,
    resolution: Coordinates,
    pos: Scene,
    strings: list[str],
) -> int:
    """
    Run a game round where the player guesses letters to complete a word.

    Parameters:
        strings : The list of strings containing text for localization.

    Returns:
        int: The score obtained in the game round.

    Description:
        This function runs a game round where the player guesses letters to complete a word.
        If the player guesses an incorrect letter, the gallow image is updated to reflect the number of incorrect attempts.
    """
    background_image = pygame.transform.scale(BACKGROUND_4, resolution)

    gallow_background_image = pygame.transform.scale(
        BACKGROUND_5, pos["game_round"]["gallow_background_size"]
    )

    screen.blit(background_image, (0, 0))

    provided_letters = set()
    incorrect_letters = set()
    correct_letters = set()
    password_words = the_word.split()
    password_letters = [letter for letter in the_word.upper()]
    if " " in password_letters:
        provided_letters.add(" ")
        correct_letters.add(" ")
    clock = pygame.time.Clock()
    attempts = 0
    running = True
    while running:
        # Forms word for print, hides unknown letters
        letters_for_print = []
        for letter in password_letters:
            if letter.upper() not in provided_letters:
                letters_for_print.append("_")
            if letter.upper() in provided_letters:
                letters_for_print.append(letter)

        provided_keys = False
        for event in pygame.event.get():
            running = skip_leave_action(event)
            if event.type == pygame.KEYDOWN:
                for key in KEYBOARD_INPUT:
                    if key == event.key:
                        provided_keys = KEYBOARD_INPUT[key]
                        provided_keys = [key.upper() for key in provided_keys]
        # Check if provided letter is in password. If it is, adds it to correct_letters set
        if provided_keys:
            if any(letter.upper() in provided_letters for letter in provided_keys):
                if any(letter.upper() in password_letters for letter in provided_keys):
                    sound_channel.play(SOUND_EFFECTS["error"])
                else:
                    sound_channel.play(SOUND_EFFECTS["wrong"])
                    attempts += 1
            if any(letter.upper() not in provided_letters for letter in provided_keys):
                if any(letter.upper() in password_letters for letter in provided_keys):
                    sound_channel.play(SOUND_EFFECTS["correct"])
                    correct_letters.update(provided_keys)
                else:
                    sound_channel.play(SOUND_EFFECTS["wrong"])
                    incorrect_letters.update(provided_keys)
                    attempts += 1
                provided_letters.update(provided_keys)
        # Display content on screen
        description_font = pygame.font.Font(COMMON_FONT_PATH, pos["game_round"]["font"])
        category = description_font.render(
            f"{strings['category']} {category_name.upper()}", True, RGB_COLORS["green"]
        )
        score_description = description_font.render(
            f"{strings['score']} {score}", True, RGB_COLORS["green"]
        )
        try:
            gallow_image = pygame.image.load(
                os.path.join(
                    os.path.dirname(__file__),
                    "data",
                    "images",
                    f"gallow_{attempts}.png",
                )
            )
        except FileNotFoundError:
            gallow_image = os.path.join(
                os.path.dirname(__file__), "data", "images", f"gallow_12.png"
            )
        gallow_image = pygame.transform.scale(
            gallow_image, pos["game_round"]["gallow_size"]
        )

        screen.blit(gallow_background_image, pos["game_round"]["gallow_background_pos"])
        screen.blit(gallow_image, pos["game_round"]["gallow_pos"])
        screen.blit(score_description, pos["game_round"]["score_info"])
        screen.blit(category, pos["game_round"]["category_info"])

        height = pos["game_round"]["height"]

        # Check win or lose conditions
        for word in password_words:
            display_letters(word, provided_letters, screen, pos, height)
            height += pos["game_round"]["height"]
        if set(password_letters) <= correct_letters:
            success = True
            victory_failure_display(screen, sound_channel, pos, success, strings)
            score = TOTAL_ATTEMTPS - attempts
            return score
        if attempts == TOTAL_ATTEMTPS:
            success = False
            victory_failure_display(screen, sound_channel, pos, success, strings)
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
    show_intro = True
    while True:
        with open(SETTINGS_FILE, "rb") as stream:
            settings = pickle.load(stream)

        resolution = settings["resolution"]
        resolution_x, resolution_y = resolution
        file_with_numbers = os.path.join(
            os.path.dirname(__file__),
            "data",
            "resolutions",
            f"{resolution_x}_{resolution_y}.json",
        )

        with open(file_with_numbers, "r") as stream:
            pos = json.load(stream)
        language = settings["language"]
        with open(
            os.path.join(
                os.path.dirname(__file__), "data", "text", f"{language}_strings.json"
            ),
            "r",
            encoding="utf-8",
        ) as stream:
            strings = json.load(stream)
        with open(
            os.path.join(
                os.path.dirname(__file__), "data", "text", f"{language}_key_words.json"
            ),
            "r",
            encoding="utf-8",
        ) as stream:
            words_base = json.load(stream)

        screen = create_screen(resolution, settings["fullscreen"])

        music_channel = pygame.mixer.Channel(0)
        music = pygame.mixer.Sound(
            os.path.join(os.path.dirname(__file__), "data", "soundeffects", "music.mp3")
        )
        music_channel.set_volume(settings["music_volume"] / 200)

        sound_channel = pygame.mixer.Channel(1)
        if settings["play_sound"] == True:
            sound_channel.set_volume(settings["sound_volume"] / 100)
        else:
            sound_channel.set_volume(0)
        if show_intro:
            play_intro(screen, resolution, pos, strings, sound_channel)
            show_intro = False
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
                    save_changes = settings_menu(
                        screen,
                        settings,
                        sound_channel,
                        resolution,
                        music_channel,
                        pos,
                        strings,
                    )
                    if save_changes:
                        pygame.display.quit()
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
