import random
import os
import sys
import time
import pickle

import pygame

pygame.init()

TOTAL_ATTEMTPS = 12

SETTINGS_FILE = "databases\\settings.db"
SCOREBOARD_FILE = "databases\\scoreboard.db"
STRINGS_FILE = "databases\\strings.db"

KEYBOARD_INPUT = {
    pygame.K_a: ["a","ą"], pygame.K_b: ["b"], pygame.K_c: ["c","ć"], pygame.K_d: ["d"], pygame.K_e: ["e","ę"], pygame.K_f: ["f"],
    pygame.K_g: ["g"], pygame.K_h: ["h"], pygame.K_i: ["i"], pygame.K_j: ["j"], pygame.K_k: ["k"], pygame.K_l: ["l","ł"],
    pygame.K_m: ["m"], pygame.K_n: ["n","ń"], pygame.K_o: ["o","ó"], pygame.K_p: ["p"], pygame.K_q: ["q"], pygame.K_r: ["r"],
    pygame.K_s: ["s","ś"], pygame.K_t: ["t"], pygame.K_u: ["u"], pygame.K_v: ["v"], pygame.K_w: ["w"], pygame.K_x: ["x"],
    pygame.K_y: ["y"], pygame.K_z: ["z","ź","ż"],}

SOUND_EFFECTS = {"wrong": pygame.mixer.Sound("soundeffects\\wrong.mp3"),
                 "correct": pygame.mixer.Sound("soundeffects\\correct.mp3"),
                 "error": pygame.mixer.Sound("soundeffects\\error.mp3"),
                 "success": pygame.mixer.Sound("soundeffects\\success.mp3"),
                 "failure": pygame.mixer.Sound("soundeffects\\game_over.mp3"),
                 "beep": pygame.mixer.Sound("soundeffects\\beep.mp3")}

def play_intro(screen: pygame.surface.Surface, resolution: tuple[int], pos: dict, strings: list[str]) -> None:
    '''Initial function for whole game. Displays welcome messege in the surface provided in argument'''

    background_image = pygame.transform.scale(pygame.image.load("images\\intro_background.jpg"),(resolution))
    screen.blit(background_image, (0, 0))
    clock = pygame.time.Clock()
    ticks = 0        
    pygame.mixer.music.load("soundeffects\\intro.mp3")
    pygame.mixer.music.play()
    pygame.display.flip()

    while True:
        ticks += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                pygame.mixer.music.stop()
                return None
  
        if ticks == 55:
            title_font = pygame.font.Font("font.ttf", pos["intro"]["font1"])
            main_title = title_font.render("Hangman", True, (0,255,255))
            screen.blit(main_title, pos["intro"]["text1"])
            pygame.display.flip()
        
        if ticks == 110:
            description_font = pygame.font.Font(None,pos["intro"]["font2"])    
            description_text_1 = description_font.render(f"{strings[0]}",True,(255,255,255))
            screen.blit(description_text_1, pos["intro"]["text2"])
            pygame.display.flip()

        if ticks == 160:
            description_text_2 = description_font.render(f"{strings[1]}",True,(255,255,255))
            screen.blit(description_text_2, pos["intro"]["text3"])
            pygame.display.flip()

        if ticks == 500:

            return None
        clock.tick(60)

def play_outro(screen: pygame.surface.Surface, score: int, resolution: tuple[int], pos: dict, sound_channel: pygame.mixer.Channel, strings: list[str]) -> None:
    
    '''Display the game outro screen and handle user interactions.
    Parameters:
        - screen (pygame.surface.Surface): The surface on which the outro screen is displayed.
        - score (int): The player's score.
        - resolution (tuple[int]): A tuple containing the screen resolution in pixels (width, height).
        - pos (dict): A dictionary containing the positions of elements on the screen.
        - sound_channel (pygame.mixer.Channel): The sound channel used to play sound effects.
        - strings (list[str]): A list containing text strings used for displaying texts on the screen.
    Description:
        The `play_outro` function is responsible for displaying the game outro screen and handling user interactions on that screen. It displays the background, texts, buttons, and handles events such as key presses, mouse movement, and button clicks.
        Provides user possibility to save his game score in the "scoreboard.db" file.
    '''

    pygame.mixer.music.load("soundeffects\\outro.mp3")
    pygame.mixer.music.play()

    with open(SCOREBOARD_FILE,"rb") as stream:
        scoreboard = pickle.load(stream)

    button_free = pygame.image.load("images\\button_1.png")
    button_aimed = pygame.image.load("images\\button_2.png")
    button_size = pos["outro"]["button_size"]
    button_font = pygame.font.Font("font.ttf", pos["outro"]["button_font"])  

    button_1_text = button_font.render(f"{strings[2]}", True, (0,0,0))
    button_2_text = button_font.render(f"{strings[3]}", True, (0,0,0))
    button_1_text_rect = button_1_text.get_rect()
    button_2_text_rect = button_2_text.get_rect()
    button_1_text_rect.center = (pos["outro"]["button1_pos"][0]+(button_size[0]//2), pos["outro"]["button1_pos"][1]+(button_size[1]//2))
    button_2_text_rect.center = (pos["outro"]["button2_pos"][0]+(button_size[0]//2), pos["outro"]["button2_pos"][1]+(button_size[1]//2))

    background_image = pygame.transform.scale(pygame.image.load("images\\intro_background.jpg"),(resolution))

    is_mouse_over_button = [False] * 2

    description_font = pygame.font.Font("font.ttf", pos["outro"]["description_font"]) 
    title_font = pygame.font.Font("font.ttf", pos["outro"]["title_font"])
    name_font = pygame.font.Font("font.ttf", pos["outro"]["name_font"])

    main_title = title_font.render(strings[24], True, (0,0,255)) 
    description_score = description_font.render(f"{strings[4]} {score} ",True,(255,255,255))
    description_name = description_font.render(f"{strings[5]}",True,(255,255,255))



    name_latters = [] 
    while True:

        screen.blit(background_image, (0, 0)) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            elif event.type == pygame.KEYDOWN:
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
                if event.key == pygame.K_ESCAPE:
                    return None

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                is_mouse_over_button[0] = check_mouse(pos["outro"]["button1_pos"], button_size, mouse_pos)
                is_mouse_over_button[1] = check_mouse(pos["outro"]["button2_pos"], button_size, mouse_pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    if is_mouse_over_button[0]:
                        sound_channel.play(SOUND_EFFECTS["beep"])
                        return None
                    if is_mouse_over_button[1]:
                        if len(name_latters) > 0:
                            sound_channel.play(SOUND_EFFECTS["beep"])
                            to_save = (name,score)
                            scoreboard.append(to_save)
                            scoreboard = sorted(scoreboard, key=lambda x: x[1], reverse=True)
                            del scoreboard[30:]
                            with open(SCOREBOARD_FILE,"wb") as stream:
                                pickle.dump(scoreboard, stream)
                            return None
                        else:
                            sound_channel.play(SOUND_EFFECTS["error"])

        name = "".join(name_latters)
        name_title = name_font.render(f"{name.upper()}", True, (0,255,0))
              
        
        button_1 = button_aimed if is_mouse_over_button[0] else button_free
        button_1 = pygame.transform.scale(button_1, button_size)
        button_2 = button_aimed if is_mouse_over_button[1] else button_free
        button_2 = pygame.transform.scale(button_2, button_size) 


        screen.blit(button_1, pos["outro"]["button1_pos"])
        screen.blit(button_2, pos["outro"]["button2_pos"])

        screen.blit(main_title, pos["outro"]["title_pos"])
        screen.blit(description_score, pos["outro"]["score_pos"])
        screen.blit(description_name, pos["outro"]["desc_pos"])
        screen.blit(name_title, pos["outro"]["name_pos"])

        screen.blit(button_1_text, button_1_text_rect)
        screen.blit(button_2_text, button_2_text_rect)        
    
        pygame.display.flip()

def display_letters(word: str, provided_letters: list[str], screen: pygame.surface.Surface, height: int, resolution: tuple[int]) -> None:
    
    '''Render and display letters of a word on the screen.
    Parameters:
        - resolution (tuple[int]): A tuple containing the screen resolution in pixels (width, height).
        - word (str): The word to be displayed.
        - provided_letters (set[str]): A set of letters that are already provided.
        - screen (pygame.surface.Surface): The surface on which the letters are displayed.
        - height (int): The vertical position at which the letters are displayed.

    Description:
        The code iterates over each letter in the word. If the letter is not in the provided_letters set, it is replaced with an underscore ('_'). If the letter is a space, it is replaced with a hyphen ('-'). The letter is then rendered using the specified font and displayed on the screen at the current distance and height. The distance is incremented based on the screen resolution, ensuring proper spacing between letters.
    '''

    letter_font = pygame.font.Font("font.ttf",int(resolution[0]*80/800))
    distance = int(10)
    for letter in word:
        if letter.upper() not in provided_letters:
            letter = "_"
        if letter == " ":
            letter = "-"
        letter_for_print = letter_font.render(f"{letter.upper()}",True,(0,255,0))
        screen.blit(letter_for_print,(int(distance), height))
        distance += int(resolution[0]*60/800)

def victory_failure_display(screen: pygame.surface.Surface, sound_channel: pygame.mixer.Channel,  pos: dict, success: bool, strings: list[str]) -> None:
    '''
    Display victory or failure message on the screen.

    Parameters:
        - screen (pygame.surface.Surface): The surface on which the message is displayed.
        - sound_channel (pygame.mixer.Channel): The sound channel used to play sound effects.
        - pos (dict): A dictionary containing the positions of elements on the screen.
        - success (bool): A boolean indicating whether it is a victory (True) or failure (False).
        - strings (list[str]): A list containing text strings used for displaying texts on the screen.

    Description:
        The `victory_failure_display` function displays a victory or failure message on the screen based on the value of the `success` parameter. It renders the main title text using the specified font and color, plays the corresponding sound effect, blits the text onto the screen, updates the display, waits for a specified duration, and then returns.
    '''
    title_font = pygame.font.Font("font.ttf", pos["victory_failure_display"]["title_font"])
    if success:
        text, time_to_wait, color = f"{strings[6]}", 3, (0,0,255)
        sound_channel.play(SOUND_EFFECTS["success"])
    else:
        text, time_to_wait, color = f"{strings[7]}", 9, (255,0,0)
        sound_channel.play(SOUND_EFFECTS["failure"]), 
    main_title = title_font.render(text, True, color)
    screen.blit(main_title, (pos["victory_failure_display"]["title"]))
    pygame.display.flip()
    time.sleep(time_to_wait)

def check_mouse(position: tuple[int], button_type: tuple [int], mouse_pos: tuple[int]) -> bool:
    '''
    Check if the mouse position is within the specified button area.

    Parameters:
        - position (tuple[int]): The position of the top-left corner of the button area (x, y).
        - button_type (tuple[int]): The size of the button area (width, height).
        - mouse_pos (tuple[int]): The current position of the mouse (x, y).

    Returns:
        bool: True if the mouse position is within the button area, False otherwise.

    Description:
        The `check_mouse` function checks if the current mouse position is within the specified button area. It compares the x and y coordinates of the mouse position with the boundaries of the button area. If the mouse position is within the button area, it returns True; otherwise, it returns False.
    '''

    x, y = position[0], position[1]
    x_end = x + button_type[0]
    y_end = y + button_type[1]
    if int(x) <= mouse_pos[0] <= x_end and int(y) <= mouse_pos[1] <= y_end:
        return True
    else:
        return False

def get_random_word(words_base) -> tuple[str]:
    '''
    Get a random word from the given words_base.

    Parameters:
        - words_base (list[tuple[str]]): A list of word categories, where each category is represented by a list containing the category name as the first element, followed by the words in that category.

    Returns:
        tuple[str]: A tuple containing the randomly selected word and its category name.

    Description:
        The `get_random_word` function selects a random word from the given words_base. It first chooses a random category from the words_base and assigns its name to the `category_name` variable. Then, it retrieves the word_base for that category. Finally, it selects a random word from the word_base and returns a tuple containing the randomly selected word and its category name.
    '''

    category = random.choice(words_base)
    category_name = category[0]
    word_base = category[1:]
    the_word = random.choice(word_base)
    return the_word, category_name

def create_screen(resolution: tuple[int], fullscreen: bool) -> pygame.surface.Surface:
    '''
    Create a Pygame screen surface with the specified resolution and fullscreen mode.

    Parameters:
        - resolution (tuple[int]): A tuple containing the screen resolution in pixels (width, height).
        - fullscreen (bool): A boolean indicating whether the screen should be created in fullscreen mode.

    Returns:
        pygame.surface.Surface: The new created Pygame screen surface.

    Description:
        The `create_screen` function creates a Pygame screen surface with the specified resolution and fullscreen mode. If the `fullscreen` parameter is True, it creates the screen in fullscreen mode using `pygame.FULLSCREEN` flag; otherwise, it creates the screen in windowed mode. The function then returns the created screen surface.
    '''

    if fullscreen:
        return pygame.display.set_mode((resolution),pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode((resolution))

def game_menu(screen: pygame.surface.Surface, sound_channel: pygame.mixer.Channel, resolution: tuple[int], pos: dict, strings: list[str]) -> str:
    '''
    Display the game menu and handle user interactions.

    Parameters:
        - screen (pygame.surface.Surface): The Pygame screen surface to display the menu on.
        - sound_channel (pygame.mixer.Channel): The Pygame mixer channel for playing sound effects.
        - resolution (tuple[int]): A tuple containing the screen resolution in pixels (width, height).
        - pos (dict): A dictionary containing the position coordinates for different elements in the menu.
        - strings (list[str]): A list of string values for different menu options and texts.

    Returns:
        str: The selected option from the game menu. One of : "new_game", "settings", "scoreboard", "exit"

    Description:
        The `game_menu` function displays the game menu on the provided screen surface and handles user interactions. It loads the background image, button images, and button text. It also initializes variables for tracking mouse movements and button states.
        The function enters a loop where it continuously checks for user events. It handles the QUIT event to exit the game if the user closes the window. It handles MOUSEMOTION events to track mouse movements. It handles MOUSEBUTTONDOWN events to check for button clicks. If the left mouse button is clicked on a button, the corresponding option is returned.
        The function updates the button states based on mouse movements and displays the updated buttons on the screen surface. It also displays the button text centered on each button. The function keeps track of which button the mouse is currently over using the `check_mouse` function.
        The function continues this loop until a button option is selected and returned.
    '''

    background_image = pygame.transform.scale(pygame.image.load("images\\menu_background.jpg"), resolution)
    button_free = pygame.image.load("images\\button_1.png")
    button_aimed = pygame.image.load("images\\button_2.png")
    button_font = pygame.font.Font("font.ttf", pos["game_menu"]["font"])    

    button_positions = [pos["game_menu"]["button1_pos"],pos["game_menu"]["button2_pos"],pos["game_menu"]["button3_pos"],pos["game_menu"]["button4_pos"]]
    buttons = [button_free] * 4    
    button_texts = [(strings[8], pos["game_menu"]["button1_text_pos"]),(strings[9], pos["game_menu"]["button2_text_pos"]),
    (strings[10], pos["game_menu"]["button3_text_pos"]),(strings[11], pos["game_menu"]["button4_text_pos"])]
    options = ["new_game", "settings", "scoreboard", "exit"]
    button_size = pos["game_menu"]["button_size"]
    is_mouse_over_button = [False] * 4
    screen.blit(background_image, (0, 0))
    init, mouse_movement = True, False
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEMOTION:

                mouse_movement = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for button, option in zip(is_mouse_over_button, options):
                        if button:
                            sound_channel.play(SOUND_EFFECTS["beep"])
                            return option
                        
        mouse_pos = pygame.mouse.get_pos()
        counter = 0
        if mouse_movement or init:
            init, mouse_movement = False, False
            for mouse_over, position, button, button_text in zip(is_mouse_over_button, button_positions, buttons, button_texts):
                mouse_over = check_mouse(position, button_size, mouse_pos)
                button = button_aimed if mouse_over else button_free
                button = pygame.transform.scale(button, button_size)
                screen.blit(button, position)
                text = (button_font.render(f"{button_text[0]}",True,(0,0,0)))
                text_rect = text.get_rect()
                text_rect.center = (position[0]+(button_size[0]//2), position[1]+(button_size[1]//2))
                screen.blit(text, text_rect)

                if mouse_over:
                    is_mouse_over_button[counter] = True
                    counter += 1
                else:
                    is_mouse_over_button[counter] = False
                    counter += 1

        pygame.display.flip()

def leaderboard_menu(screen: pygame.surface.Surface, sound_channel: pygame.mixer.Channel, resolution: tuple[int], pos: dict, strings: list[str]) -> None: 
    '''
    Display the leaderboard menu and handle user interactions.

    Parameters:
        - screen (pygame.surface.Surface): The Pygame screen surface to display the menu on.
        - sound_channel (pygame.mixer.Channel): The Pygame mixer channel for playing sound effects.
        - resolution (tuple[int]): A tuple containing the screen resolution in pixels (width, height).
        - pos (dict): A dictionary containing the position coordinates for different elements in the menu.
        - strings (list[str]): A list of string values for different menu options and texts.

    Description:

        The function enters a loop where it continuously checks for user events. It handles the QUIT event to exit the game if the user closes the window. It handles MOUSEMOTION events to track mouse movements over buttons. It handles KEYDOWN events to check for the ESCAPE key press, which returns None and exits the menu.
        If the left mouse button is clicked on a button, the corresponding action is performed. Clicking on the first button returns None and exits the menu. Clicking on the second button clears the scoreboard data and returns None, exiting the menu.
        The function continues this loop until an action is performed and the menu is exited.
    '''
    background_image = pygame.transform.scale(pygame.image.load("images\\intro_background.jpg"), resolution)
    screen.blit(background_image, (0, 0))

    button_free = pygame.image.load("images\\button_1.png")
    button_aimed = pygame.image.load("images\\button_2.png")

    description_font = pygame.font.Font("font.ttf", pos["leaderboard_menu"]["desc_font"])
    text_font = pygame.font.Font("font.ttf", pos["leaderboard_menu"]["text_font"])

    description_text = description_font.render(f"{strings[10]}",True,(255,100,0))
    description_text_rect = description_text.get_rect()
    description_text_rect.center = (resolution[0] // 2, pos["leaderboard_menu"]["desc_pos"][1] * 3)
    button_texts = [text_font.render(f"{strings[2]}",True,(0,0,0)), text_font.render(f"{strings[12]}",True,(0,0,0))]


    with open(SCOREBOARD_FILE,"rb") as stream:
        scoreboard = pickle.load(stream)
    scoreboard = sorted(scoreboard, key=lambda x: x[1], reverse=True)
    
    scoreboard_list =  [scoreboard[:10],scoreboard[10:20],scoreboard[20:30]]

    button_size = (pos["leaderboard_menu"]["button_size"])
  
    is_mouse_over_button = [False] *2
    screen.blit(description_text, description_text_rect)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                is_mouse_over_button[0] = check_mouse(pos["leaderboard_menu"]["button1_pos"], button_size, mouse_pos)
                is_mouse_over_button[1] = check_mouse(pos["leaderboard_menu"]["button2_pos"], button_size, mouse_pos)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sound_channel.play(SOUND_EFFECTS["beep"])
                    return None
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if is_mouse_over_button[0]:
                        sound_channel.play(SOUND_EFFECTS["beep"])
                        return None
                    if is_mouse_over_button[1]:
                        sound_channel.play(SOUND_EFFECTS["beep"])
                        scoreboard = []
                        with open(SCOREBOARD_FILE,"wb") as stream:
                            pickle.dump(scoreboard, stream)
                        return None
                elif event.button == 3:
                    print (mouse_pos)

        counter = 0
        for mouse_over, text in zip(is_mouse_over_button, button_texts):
            button = button_aimed if mouse_over else button_free
            button = pygame.transform.scale(button, button_size)
            position = pos["leaderboard_menu"][f"button{counter+1}_pos"]
            screen.blit(button, position)
            text_rect = text.get_rect()
            text_rect.center = (position[0]+(button_size[0]//2), position[1]+(button_size[1]//2))
            screen.blit(text, text_rect)
            counter+=1
        
        counter = 0
        position = 1
        height = pos["leaderboard_menu"]["height"]
        for token in scoreboard_list:
            height = pos["leaderboard_menu"]["height"]
            counter += 1
            for score in token:
                name = score[0].capitalize()
                score_text = text_font.render(f"{position:2}. {name:<12}{score[1]}",True,(255,255,255))
                screen.blit(score_text,(pos["leaderboard_menu"][f"score_x{counter}"],height))
                height += pos["leaderboard_menu"]["height_change"]
                position += 1

        pygame.display.flip()

def settings_menu(screen: pygame.surface.Surface, settings: dict, sound_channel: pygame.mixer.Channel, resolution: tuple[int], music_channel: pygame.mixer.Channel, pos: dict, strings: list[str]) -> bool:
    '''
    Display and handle the settings menu screen.

    Parameters:
        - screen (pygame.surface.Surface): The surface representing the game screen.
        - settings (dict): The current settings of the game.
        - sound_channel (pygame.mixer.Channel): The sound channel for playing sound effects.
        - resolution (tuple[int]): The current resolution of the game screen.
        - music_channel (pygame.mixer.Channel): The music channel for playing background music.
        - pos (dict): The position dictionary containing the positions of various elements on the screen.
        - strings (list[str]): The list of strings containing text for localization.

    Returns:
        bool: Returns True if the settings were successfully saved, False if the user chose to exit without saving, or None if the user pressed the escape key to return to the previous menu.

    Description:
        Function allows user to change certain parameters of game, i allows to change screen resolution, sound and music volume, language.
        It works very similar to "game_menu" function'''

    new_settings = settings.copy()
    background_image = pygame.image.load("images\\menu_background.jpg")
    background_image = pygame.transform.scale(background_image,(resolution))
    button_free = pygame.image.load("images\\button_1.png")
    button_aimed = pygame.image.load("images\\button_2.png")
    button_lock = pygame.image.load("images\\button_3.png")
    description_button_font = pygame.font.Font("font.ttf", pos["settings_menu"]["desk_font"])
    button_font = pygame.font.Font("font.ttf", pos["settings_menu"]["button_font"])
    is_mouse_over_button = [False] * 16    
    texts_to_display = ["800:600", "1200:800", f"{strings[13]}", "1920:1080", "1280:720", f"{strings[14]}", f"{strings[15]}", "+", "-", 
                        f"{strings[16]}", "+", "-",f"{strings[17]}", f"{strings[18]}", f"{strings[2]}", f"{strings[3]}"]
    rendered_text = [] 
    button_standards = [1,1,1,1,1,1,3,2,2,3,2,2,3,3,3,3]
    description_texts= [strings[19],strings[16],strings[20]]

    for text in texts_to_display:
        text = button_font.render(text,True,(0,0,0))
        rendered_text.append(text)

    description_button = pygame.transform.scale(button_lock, pos["settings_menu"]["button_size_4"])    
    
    screen.blit(background_image, (0, 0))

    counter = 1
    for text in description_texts:
        text = description_button_font.render(f"{text}",True,(255,100,0))
        screen.blit(description_button, pos["settings_menu"][f"desc_button_{counter}"])
        screen.blit(text, pos["settings_menu"][f"desc_text_{counter}"])
        counter += 1

    while True:
        
        if new_settings["play_music"] == True:
            music_volume = str(new_settings["music_volume"]) + "%"
        else:
            music_volume = f"{strings[21]}" 

        if new_settings["play_sound"] == True:
            sound_volume = str(new_settings["sound_volume"]) + "%"
        else:
            sound_volume = f"{strings[21]}" 

        rendered_text[6] = button_font.render(f"{strings[15]}: {music_volume}",True,(0,0,0))
        rendered_text[9] = button_font.render(f"{strings[16]}: {sound_volume}",True,(0,0,0))

        if new_settings["play_music"]:
            music_channel.set_volume(new_settings["music_volume"]/200)
        else:
            music_channel.set_volume(0)

        if new_settings["play_sound"]:    
            sound_channel.set_volume(new_settings["sound_volume"]/100)
        else:
            sound_channel.set_volume(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sound_channel.play(SOUND_EFFECTS["beep"])
                    return None
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                counter = 0
                for mouse_over, standard in zip(is_mouse_over_button, button_standards):
                    mouse_over = check_mouse(pos["settings_menu"][f"button_{counter+1}"], pos["settings_menu"][f"button_size_{standard}"], mouse_pos)
                    if mouse_over:
                        is_mouse_over_button[counter] = True
                    else:
                        is_mouse_over_button[counter] = False
                    counter += 1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    if is_mouse_over_button[0]:
                        if new_settings["resolution"] != [800,600]:
                            sound_channel.play(SOUND_EFFECTS["beep"])
                            new_settings["resolution"] = [800,600]
                            new_settings["wide_screen"] = False
                        else:
                            sound_channel.play(SOUND_EFFECTS["error"])
                    if is_mouse_over_button[1]:
                        if new_settings["resolution"] != [1200,800]:
                            sound_channel.play(SOUND_EFFECTS["beep"])
                            new_settings["resolution"] = [1200,800]
                            new_settings["wide_screen"] = False
                        else:
                            sound_channel.play(SOUND_EFFECTS["error"])

                    if is_mouse_over_button[2]:
                        if new_settings["fullscreen"] == False:
                            sound_channel.play(SOUND_EFFECTS["beep"])
                            new_settings["fullscreen"] = True
                        else:
                            sound_channel.play(SOUND_EFFECTS["error"])

                    if is_mouse_over_button[3]:
                        if new_settings["resolution"] != [1920,1080]:
                            sound_channel.play(SOUND_EFFECTS["beep"])
                            new_settings["resolution"] = [1920,1080]
                            new_settings["wide_screen"] = True
                        else:
                            sound_channel.play(SOUND_EFFECTS["error"])

                    if is_mouse_over_button[4]:
                        if new_settings["resolution"] != [1280,720]:
                            sound_channel.play(SOUND_EFFECTS["beep"])
                            new_settings["resolution"] = [1280,720]
                            new_settings["wide_screen"] = True
                        else:
                            sound_channel.play(SOUND_EFFECTS["error"])

                    if is_mouse_over_button[5]:
                        if new_settings["fullscreen"] == True:
                            sound_channel.play(SOUND_EFFECTS["beep"])
                            new_settings["fullscreen"] = False
                        else:
                            sound_channel.play(SOUND_EFFECTS["error"])

                    if is_mouse_over_button[6]:
                        sound_channel.play(SOUND_EFFECTS["beep"])
                        if new_settings["play_music"] == False:
                            new_settings["play_music"] = True
                        elif new_settings["play_music"] == True:
                            new_settings["play_music"] = False

                    if is_mouse_over_button[7]:
                        if new_settings["music_volume"] < 100:
                            sound_channel.play(SOUND_EFFECTS["beep"])
                            new_settings["music_volume"] += 10
                        else:
                            sound_channel.play(SOUND_EFFECTS["error"])

                    if is_mouse_over_button[8]:
                        if new_settings["music_volume"] > 0:
                            sound_channel.play(SOUND_EFFECTS["beep"])
                            new_settings["music_volume"] -= 10
                        else:
                            sound_channel.play(SOUND_EFFECTS["error"])

                    if is_mouse_over_button[9]:
                        sound_channel.play(SOUND_EFFECTS["beep"])
                        if new_settings["play_sound"] == False:
                            new_settings["play_sound"] = True
                        elif new_settings["play_sound"] == True:
                            new_settings["play_sound"] = False

                    if is_mouse_over_button[10]:
                        if new_settings["sound_volume"] < 100:
                            new_settings["sound_volume"] += 10
                            sound_channel.play(SOUND_EFFECTS["beep"])
                        else:
                            sound_channel.play(SOUND_EFFECTS["error"])

                    if is_mouse_over_button[11]:
                        if new_settings["sound_volume"] > 0:
                            new_settings["sound_volume"] -= 10
                            sound_channel.play(SOUND_EFFECTS["beep"])
                        else:
                            sound_channel.play(SOUND_EFFECTS["error"])

                    if is_mouse_over_button[12]:
                        if new_settings["language"] != "polish":
                            sound_channel.play(SOUND_EFFECTS["beep"])
                            new_settings["language"] = "polish"
                        else:
                            sound_channel.play(SOUND_EFFECTS["error"])

                    if is_mouse_over_button[13]:
                        if new_settings["language"] != "english":
                            sound_channel.play(SOUND_EFFECTS["beep"])
                            new_settings["language"] = "english"
                        else:
                            sound_channel.play(SOUND_EFFECTS["error"])

                    if is_mouse_over_button[14]:
                        sound_channel.play(SOUND_EFFECTS["beep"])
                        return False
                    
                    if is_mouse_over_button[15]:
                        sound_channel.play(SOUND_EFFECTS["beep"])
                        try:
                            with open(SETTINGS_FILE, "wb") as stream:
                                pickle.dump(new_settings,stream)
                            return True
                        except:
                            print("Something went wrong")
                elif event.button == 3:
                    print (mouse_pos)

        buttons = [None] * 16
        if new_settings["resolution"] == [800,600]:
            buttons[0] = button_lock   

        if new_settings["resolution"] == [1200,800]:
            buttons[1] = button_lock  

        if new_settings["fullscreen"] == True:
            buttons[2] = button_lock

        if new_settings["resolution"] == [1920,1080]:
            buttons[3] = button_lock  

        if new_settings["resolution"] == [1280,720]:
            buttons[4] = button_lock  

        if new_settings["fullscreen"] == False:
            buttons[5] = button_lock

        if not new_settings["play_music"]:
            buttons[6] = button_lock

        if new_settings["music_volume"] == 100:
            buttons[7] = button_lock

        if new_settings["music_volume"] == 0:
            buttons[8] = button_lock

        if not new_settings["play_sound"]:
            buttons[9] = button_lock

        if new_settings["sound_volume"] == 100:
            buttons[10] = button_lock

        if new_settings["sound_volume"] == 0:
            buttons[11] = button_lock

        if new_settings["language"] == "polish":
            buttons[12] = button_lock
        
        if new_settings["language"] == "english":
            buttons[13] = button_lock
        
        counter = 0
        for button, mouse_over, standard, text in zip(buttons, is_mouse_over_button, button_standards, rendered_text):
            if button == None:
                if mouse_over:
                    buttons[counter] = button = button_aimed
                else:
                    buttons[counter] = button = button_free
            current_standard = pos["settings_menu"][f"button_size_{standard}"]
            position = pos["settings_menu"][f"button_{counter+1}"]
            button = pygame.transform.scale(button, current_standard)
            screen.blit(button, position)
            text_rect = text.get_rect()
            text_rect.center = (position[0]+(current_standard[0]//2), position[1]+(current_standard[1]//2)+2)
            screen.blit(text, text_rect)
            counter += 1

        pygame.display.flip()

def game_round(screen: pygame.surface.Surface, the_word: str, category_name: str, score: int, sound_channel: pygame.mixer.Channel, resolution: tuple[int], pos: dict, strings: list[str]) -> int:
    """
    Run a game round where the player guesses letters to complete a word.

    Parameters:
        screen (pygame.surface.Surface): The surface representing the game screen.
        the_word (str): The word to be guessed.
        category_name (str): The name of the category to which the word belongs.
        score (int): The current score of the game.
        sound_channel (pygame.mixer.Channel): The sound channel for playing sound effects.
        resolution (tuple[int]): The current resolution of the game screen.
        pos (dict): The position dictionary containing the positions of various elements on the screen.
        strings (list[str]): The list of strings containing text for localization.

    Returns:
        int: The score obtained in the game round.

    Description:
        This function runs a game round where the player guesses letters to complete a word. The player is presented with a word and a gallow image representing the number of incorrect attempts made. The player can enter letters using the keyboard to guess the word. If the player guesses a correct letter, it is displayed in the word. If the player guesses an incorrect letter, the gallow image is updated to reflect the number of incorrect attempts.
    """
    background_image = pygame.image.load("images\\background_2.jpg")
    background_image = pygame.transform.scale(background_image, resolution)
    gallow_background_image = pygame.image.load("images\\gallow_background.jpg")
    gallow_background_image = pygame.transform.scale(gallow_background_image, pos["game_round"]["gallow_background_size"])

    screen.blit(background_image, (0, 0))

    provided_letters = set()
    incorrect_letters = set() 
    correct_letters = set()
    password_words = the_word.split()
    password_letters = [letter for letter in the_word.upper()]
    if " " in password_letters:
        provided_letters.add (" ")
        correct_letters.add(" ") 
    clock = pygame.time.Clock()
    attempts = 0

    while True:

        letters_for_print = []
        for letter in password_letters:
            if letter.upper() not in provided_letters:
                letters_for_print.append("_")
            if letter.upper() in provided_letters:
                letters_for_print.append(letter)     

        provided_keys = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                for key in KEYBOARD_INPUT:
                    if key == event.key:
                        provided_keys = (KEYBOARD_INPUT[key])
                        provided_keys = [key.upper() for key in provided_keys]
                if event.key == pygame.K_ESCAPE:
                    return None

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
                    correct_letters.update (provided_keys)
                else: 
                    sound_channel.play(SOUND_EFFECTS["wrong"])
                    incorrect_letters.update(provided_keys)
                    attempts += 1
                provided_letters.update(provided_keys)               

        description_font = pygame.font.Font("font.ttf",int(resolution[0]*36/800))    
        category = description_font.render(f"{strings[22]} {category_name.upper()}",True,(0,255,0))
        score_description = description_font.render(f"{strings[23]} {score}",True,(0,255,0))

        gallow_image = pygame.image.load(f"images\\gallow_{attempts}.png")
        gallow_image = pygame.transform.scale(gallow_image, pos["game_round"]["gallow_size"])

        screen.blit(gallow_background_image, pos["game_round"]["gallow_background_pos"])
        screen.blit(gallow_image, pos["game_round"]["gallow_pos"])
        screen.blit(score_description, pos["game_round"]["score_info"])
        screen.blit(category, pos["game_round"]["category_info"])

        height = pos["game_round"]["height"]

        for word in password_words:
            display_letters(word, provided_letters, screen, height, resolution)
            height += resolution[1] * 130/600
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
    Next, it is initialize function "play_intro", but only once. 
    Than it "initialize" game screen with parameters based on constant mentionet above.
    And at last it enters inner loop. Which is based on "main_menu" function, and based on what this function returns, it runs certain operations.
    """    
    show_intro = True
    while True:
        with open(SETTINGS_FILE, "rb") as stream:
            settings = pickle.load(stream)

        resolution = settings["resolution"]
        resolution_x, resolution_y = (resolution)
        file_with_numbers = f"databases\\resolution_{resolution_x}_{resolution_y}.db"

        with open (file_with_numbers, "rb") as stream:
            pos = pickle.load(stream)
        with open (STRINGS_FILE,"rb") as stream:
            strings_pack = pickle.load(stream)
        if settings["language"] == "polish":
            strings = strings_pack[0][0]
            words_base = strings_pack[0][1]
        if settings["language"] == "english":
            strings = strings_pack[1][0]
            words_base = strings_pack[1][1] 

        screen = create_screen(resolution, settings["fullscreen"])
        if show_intro:
            play_intro(screen, resolution, pos, strings)
            show_intro = False

        music_channel = pygame.mixer.Channel(0)
        music = pygame.mixer.Sound("soundeffects\\music.mp3")
        music_channel.set_volume(settings["music_volume"]/200)
        if settings["play_music"] == True:
            music_channel.play(music)
        else:
            music_channel.stop()

        sound_channel = pygame.mixer.Channel(1)
        if settings["play_sound"] == True:
            sound_channel.set_volume(settings["sound_volume"]/100)
        else:
            sound_channel.set_volume(0)

        while True:
            clicked = game_menu(screen, sound_channel, resolution, pos, strings)
            if clicked == "new_game":
                score = 0
                while True:
                    the_word, category_name = get_random_word(words_base)
                    new_score = game_round(screen, the_word, category_name, score,sound_channel, resolution, pos, strings)
                    if new_score:
                        score += new_score
                    else:
                        break
                play_outro(screen, score, resolution, pos, sound_channel, strings)
            elif clicked == "settings":
                save_changes = settings_menu(screen, settings, sound_channel, resolution, music_channel, pos, strings)
                if save_changes:
                    pygame.display.quit()
                    time.sleep(0.8)
                    break
            elif clicked == "scoreboard":
                leaderboard_menu(screen, sound_channel, resolution, pos, strings)
            elif clicked == "exit":
                break
        if clicked == "exit":
            time.sleep(0.7)
            break

if __name__ == "__main__":
    main()


