import random
import os
import sys
import time
import pickle

import pygame

pygame.init()

TOTAL_ATTEMTPS = 12

SETTINGS_FILE = "settings.db"
SCOREBOARD_FILE = "scoreboard.db"
STRINGS_FILE = "strings.db"

KEYBOARD_INPUT = {
    pygame.K_a: ["a","ą"], pygame.K_b: ["b"], pygame.K_c: ["c","ć"], pygame.K_d: ["d"], pygame.K_e: ["e","ę"], pygame.K_f: ["f"],
    pygame.K_g: ["g"], pygame.K_h: ["h"], pygame.K_i: ["i"], pygame.K_j: ["j"], pygame.K_k: ["k"], pygame.K_l: ["l","ł"],
    pygame.K_m: ["m"], pygame.K_n: ["n","ń"], pygame.K_o: ["o","ó"], pygame.K_p: ["p"], pygame.K_q: ["q"], pygame.K_r: ["r"],
    pygame.K_s: ["s","ś"], pygame.K_t: ["t"], pygame.K_u: ["u"], pygame.K_v: ["v"], pygame.K_w: ["w"], pygame.K_x: ["x"],
    pygame.K_y: ["y"], pygame.K_z: ["z","ź","ż"],}

SOUND_EFFECTS = {"wrong": pygame.mixer.Sound("efekty dźwiękowe\\wrong.mp3"),
                 "correct": pygame.mixer.Sound("efekty dźwiękowe\\correct.mp3"),
                 "error": pygame.mixer.Sound("efekty dźwiękowe\\error.mp3"),
                 "success": pygame.mixer.Sound("efekty dźwiękowe\\success.mp3"),
                 "failure": pygame.mixer.Sound("efekty dźwiękowe\\game_over.mp3"),
                 "beep": pygame.mixer.Sound("efekty dźwiękowe\\beep.mp3")}

def play_intro(screen: pygame.surface.Surface, resolution: tuple[int], pos: dict, strings: list[str]) -> None:

    background_image = pygame.transform.scale(pygame.image.load("pliki obrazów\\intro_background.jpg"),(resolution))
    screen.blit(background_image, (0, 0))
    clock = pygame.time.Clock()
    ticks = 0        
    pygame.mixer.music.load("efekty dźwiękowe\\intro.mp3")
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
            main_title = title_font.render("Hung Man", True, (0,255,255))
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

    pygame.mixer.music.load("efekty dźwiękowe\\outro.mp3")
    pygame.mixer.music.play()

    with open(SCOREBOARD_FILE,"rb") as stream:
        scoreboard = pickle.load(stream)


    button_free = pygame.image.load("pliki obrazów\\button_1.png")
    button_aimed = pygame.image.load("pliki obrazów\\button_2.png")

    button_font = pygame.font.Font("font.ttf", pos["outro"]["button_font"])  

    button_1_text = button_font.render(f"{strings[2]}", True, (0,0,0))
    button_2_text = button_font.render(f"{strings[3]}", True, (0,0,0))

    background_image = pygame.transform.scale(pygame.image.load("pliki obrazów\\intro_background.jpg"),(resolution))

    is_mouse_over_button = [False] * 2

    description_font = pygame.font.Font("font.ttf", pos["outro"]["description_font"]) 
    title_font = pygame.font.Font("font.ttf", pos["outro"]["title_font"])
    name_font = pygame.font.Font("font.ttf", pos["outro"]["name_font"])

    main_title = title_font.render(strings[24], True, (0,0,255)) 
    description_score = description_font.render(f"{strings[4]} {score} ",True,(255,255,255))
    description_name = description_font.render(f"{strings[5]}",True,(255,255,255))

    button_size = pos["outro"]["button_size"]

    name_latters = [] 
    while True:

        screen.blit(background_image, (0, 0)) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            elif event.type == pygame.KEYDOWN and len(name_latters) < 11:
                    for key in KEYBOARD_INPUT:
                        if key == event.key:
                            sound_channel.play(SOUND_EFFECTS["beep"])
                            name_latters.append(KEYBOARD_INPUT[key][0])
                    if event.key == pygame.K_BACKSPACE:
                        try:
                            del name_latters[-1]
                        except:
                            sound_channel.play(SOUND_EFFECTS["error"])

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
              
        if is_mouse_over_button[0]:
            button_1 = button_aimed
        else:
            button_1 = button_free
        button_1 = pygame.transform.scale(button_1, button_size)

        if is_mouse_over_button[1]:
            button_2 = button_aimed
        else:
            button_2 = button_free
        button_2 = pygame.transform.scale(button_2, button_size) 


        screen.blit(button_1, pos["outro"]["button1_pos"])
        screen.blit(button_2, pos["outro"]["button2_pos"])

        screen.blit(main_title, pos["outro"]["title_pos"])
        screen.blit(description_score, pos["outro"]["score_pos"])
        screen.blit(description_name, pos["outro"]["desc_pos"])
        screen.blit(name_title, pos["outro"]["name_pos"])

        screen.blit(button_1_text, pos["outro"]["button1_text_pos"])
        screen.blit(button_2_text, pos["outro"]["button2_text_pos"])        
    
        pygame.display.flip()

def display_letters(word: str, provided_letters: list[str], screen: pygame.surface.Surface, height: int, resolution: tuple[int]) -> None:

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
    
    x, y = position[0], position[1]
    x_end = x + button_type[0]
    y_end = y + button_type[1]
    if int(x) <= mouse_pos[0] <= x_end and int(y) <= mouse_pos[1] <= y_end:
        return True
    else:
        return False

def get_random_word(words_base) -> tuple[str]:

    category = random.choice(words_base)
    category_name = category[0]
    word_base = category[1:]
    the_word = random.choice(word_base)
    return the_word, category_name

def create_screen(resolution: tuple[int], fullscreen: bool) -> pygame.surface.Surface:

    if fullscreen:
        return pygame.display.set_mode((resolution),pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode((resolution))

def game_menu(screen: pygame.surface.Surface, sound_channel: pygame.mixer.Channel, resolution: tuple[int], pos: dict, strings: list[str]) -> str:

    background_image = pygame.transform.scale(pygame.image.load("pliki obrazów\\menu_background.jpg"), resolution)
    button_free = pygame.image.load("pliki obrazów\\button_1.png")
    button_aimed = pygame.image.load("pliki obrazów\\button_2.png")
    button_font = pygame.font.Font("font.ttf", pos["game_menu"]["font"])    

    button_positions = [pos["game_menu"]["button1_pos"],pos["game_menu"]["button2_pos"],pos["game_menu"]["button3_pos"],pos["game_menu"]["button4_pos"]]
    buttons = [button_free] * 4    
    button_texts = [(strings[8], pos["game_menu"]["button1_text_pos"]),(strings[9], pos["game_menu"]["button2_text_pos"]),
    (strings[10], pos["game_menu"]["button3_text_pos"]),(strings[11], pos["game_menu"]["button4_text_pos"])]
    options = ["new_game", "settings", "scoreboard", "exit"]
    button_size = pos["game_menu"]["button_size"]
    is_mouse_over_button = [False] * 4
    screen.blit(background_image, (0, 0))
 
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                counter = 0
                for mouse_over, position, button, button_text in zip(is_mouse_over_button, button_positions, buttons, button_texts):
                    mouse_over = check_mouse(position, button_size, mouse_pos)
                    button = button_aimed if mouse_over else button_free
                    screen.blit(button, position)
                    screen.blit(button_font.render(f"{button_text[0]}",True,(0,0,0)), button_text[1])
                    if mouse_over:
                        is_mouse_over_button[counter] = True
                        counter += 1
                    else:
                        is_mouse_over_button[counter] = False
                        counter += 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for button, option in zip(is_mouse_over_button, options):
                        if button:
                            sound_channel.play(SOUND_EFFECTS["beep"])
                            return option

        pygame.display.flip()

def leaderboard_menu(screen: pygame.surface.Surface, sound_channel: pygame.mixer.Channel, resolution: tuple[int], pos: dict, strings: list[str]) -> None: 

    background_image = pygame.transform.scale(pygame.image.load("pliki obrazów\\intro_background.jpg"), resolution)
    screen.blit(background_image, (0, 0))

    button_free = pygame.image.load("pliki obrazów\\button_1.png")
    button_aimed = pygame.image.load("pliki obrazów\\button_2.png")

    description_font = pygame.font.Font("font.ttf", pos["leaderboard_menu"]["desc_font"])
    text_font = pygame.font.Font("font.ttf", pos["leaderboard_menu"]["text_font"])

    description_text = description_font.render(f"{strings[10]}",True,(255,100,0))
    button_1_text = text_font.render(f"{strings[2]}",True,(0,0,0))
    button_2_text = text_font.render(f"{strings[12]}",True,(0,0,0))

    with open(SCOREBOARD_FILE,"rb") as stream:
        scoreboard = pickle.load(stream)
    scoreboard = sorted(scoreboard, key=lambda x: x[1], reverse=True)
    
    scoreboard_part_1 = scoreboard[:10]
    scoreboard_part_2 = scoreboard[10:20]
    scoreboard_part_3 = scoreboard[20:30]

    button_size = (pos["leaderboard_menu"]["button_size"])
  
    is_mouse_over_button_1 = False
    is_mouse_over_button_2 = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                is_mouse_over_button_1 = check_mouse(pos["leaderboard_menu"]["button1_pos"], button_size, mouse_pos)
                is_mouse_over_button_2 = check_mouse(pos["leaderboard_menu"]["button2_pos"], button_size, mouse_pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if is_mouse_over_button_1:
                        sound_channel.play(SOUND_EFFECTS["beep"])
                        return None
                    if is_mouse_over_button_2:
                        sound_channel.play(SOUND_EFFECTS["beep"])
                        scoreboard = []
                        with open(SCOREBOARD_FILE,"wb") as stream:
                            pickle.dump(scoreboard, stream)
                        return None
    
        button_1 = button_aimed if is_mouse_over_button_1 else button_free
        button_1 = pygame.transform.scale(button_1, button_size)
        button_2 = button_aimed if is_mouse_over_button_2 else button_free 
        button_2 = pygame.transform.scale(button_2, button_size)

        screen.blit(button_1,pos["leaderboard_menu"]["button1_pos"])
        screen.blit(button_2,pos["leaderboard_menu"]["button2_pos"])

        screen.blit(button_1_text, pos["leaderboard_menu"]["button1_text_pos"])
        screen.blit(button_2_text, pos["leaderboard_menu"]["button2_text_pos"])
        screen.blit(description_text, pos["leaderboard_menu"]["desc_pos"])
        
        position = 1
        height = pos["leaderboard_menu"]["height"]
        for score in scoreboard_part_1:
            name = score[0].capitalize()
            score_text = text_font.render(f"{position:2}. {name:<12}{score[1]}",True,(255,255,255))
            screen.blit(score_text,(pos["leaderboard_menu"]["score_x1"],height))
            height += pos["leaderboard_menu"]["height_change"]
            position += 1
        
        height = pos["leaderboard_menu"]["height"]
        for score in scoreboard_part_2:
            name = score[0].capitalize()
            score_text = text_font.render(f"{position:2}. {name:<12}{score[1]}",True,(255,255,255))
            screen.blit(score_text, (pos["leaderboard_menu"]["score_x2"],height))
            height += pos["leaderboard_menu"]["height_change"]
            position += 1

        height = pos["leaderboard_menu"]["height"]
        for score in scoreboard_part_3:
            name = score[0].capitalize()
            score_text = text_font.render(f"{position:2}. {name:<12}{score[1]}",True,(255,255,255))
            screen.blit(score_text,(pos["leaderboard_menu"]["score_x3"],height))
            height += pos["leaderboard_menu"]["height_change"]
            position += 1

        pygame.display.flip()

def settings_menu(screen: pygame.surface.Surface, settings: dict, sound_channel: pygame.mixer.Channel, resolution: tuple[int], music_channel: pygame.mixer.Channel, pos: dict, strings: list[str]) -> bool:

    background_image = pygame.image.load("pliki obrazów\\menu_background.jpg")
    background_image = pygame.transform.scale(background_image,(resolution))
    button_free = pygame.image.load("pliki obrazów\\button_1.png")
    button_aimed = pygame.image.load("pliki obrazów\\button_2.png")
    button_lock = pygame.image.load("pliki obrazów\\button_3.png")
    description_button_font = pygame.font.Font("font.ttf", pos["settings_menu"]["desk_font"])
    button_font = pygame.font.Font("font.ttf", pos["settings_menu"]["button_font"])
    new_settings = settings.copy()
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
        for button, mouse_over, standard, text in zip(buttons, is_mouse_over_button, button_standards, rendered_text[:16]):
            if button == None:
                if mouse_over:
                    buttons[counter] = button = button_aimed
                else:
                    buttons[counter] = button = button_free
            button = pygame.transform.scale(button, pos["settings_menu"][f"button_size_{standard}"])
            screen.blit(button, pos["settings_menu"][f"button_{counter+1}"])
            screen.blit(text, pos["settings_menu"][f"text_{counter+1}"])
            counter += 1

        pygame.display.flip()

def game_round(screen: pygame.surface.Surface, the_word: str, category_name: str, score: int, sound_channel: pygame.mixer.Channel, resolution: tuple[int], pos: dict, strings: list[str]) -> int:

    background_image = pygame.image.load("pliki obrazów\\background_2.jpg")
    background_image = pygame.transform.scale(background_image, resolution)
    gallow_background_image = pygame.image.load("pliki obrazów\\gallow_background.jpg")
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
                    pygame.quit()
                    exit()

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

        gallow_image = pygame.image.load(f"pliki obrazów\\gallow_{attempts}.png")
        gallow_image = pygame.transform.scale(gallow_image, pos["game_round"]["gallow_size"])

        screen.blit(gallow_background_image, pos["game_round"]["gallow_background_pos"])
        screen.blit(gallow_image, pos["game_round"]["gallow_pos"])
        screen.blit(score_description, pos["game_round"]["score_info"])
        screen.blit(category, pos["game_round"]["category_info"])

        height = pos["game_round"]["height"]

        for word in password_words:
            display_letters(word, provided_letters, screen, height, resolution)
            height += 130
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
    
    show_intro = True
    while True:
        with open(SETTINGS_FILE, "rb") as stream:
            settings = pickle.load(stream)

        resolution, wide_resolution = settings["resolution"], settings["wide_screen"]
        resolution_x, resolution_y = (resolution)
        file_with_numbers = f"resolution_{resolution_x}_{resolution_y}.db"

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
        music = pygame.mixer.Sound("efekty dźwiękowe\\music.mp3")
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


