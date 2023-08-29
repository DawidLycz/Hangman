import os
from pathlib import Path
import pygame
from typing import Dict, Tuple

pygame.init()

DIRNAME = Path(os.path.dirname(__file__))

COMMON_FONT_PATH = DIRNAME / "data/fonts/font.ttf"

BUTTON_TYPE_FREE = pygame.image.load(DIRNAME / "data/images/button_1.png")
BUTTON_TYPE_AIMED = pygame.image.load(DIRNAME / "data/images/button_2.png")
BUTTON_TYPE_LOCKED = pygame.image.load(DIRNAME / "data/images/button_3.png")
GALLOW_BACKGROUND = pygame.image.load(DIRNAME / "data/images/gallow_background.jpg")

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


class Inscription:
    '''Class represents various not interactive texts displayed on the screen.
    It has ability to change its color, font, and possibliy of background'''
    def __init__(
        self,
        text: str,
        color: RGB_Color,
        position: Coordinates,
        font_size: int,
        screen: pygame.surface.Surface,
        font_path: str=None,
        background: pygame.surface.Surface=None,
        background_size: Coordinates=None,
    ):
        self.text = text
        self.color = color
        self.position = position
        self.font_size = font_size
        self.screen = screen
        self.font_path = font_path
        self.background = background

        font = pygame.font.Font(font_path, font_size)
        self.rendered_text = font.render(text, True, color)
        self.text_size = self.rendered_text.get_size()

        self.text_rect = self.rendered_text.get_rect()

        if background_size:
            self.background_size = background_size
        else:
            self.background_size = self.text_size

        self.text_rect.center = (
            self.position[0] + (self.text_size[0] // 2),
            self.position[1] + (self.text_size[1] // 2),
        )
        if background:
            self.scaled_background_image = pygame.transform.scale(
                self.background, self.background_size
            )
            self.background_rect = self.scaled_background_image.get_rect()
            self.background_rect.center = self.text_rect.center


    def __str__(self) -> str:
        return f"Text: {self.name}"

    def draw(self):
        if self.background:
            self.screen.blit(self.scaled_background_image, self.background_rect)
        self.screen.blit(self.rendered_text, self.position)

    def center_x(self) -> None:
        '''Adjust text directly in to middle of screen in x axis, helpfull when text is changable'''
        resolution = self.screen.get_size()
        middle_width = resolution[0] // 2
        new_width = middle_width - self.text_size[0] // 2 
        self.position = (new_width, self.position[1])
        if self.background:
            self.background_rect.center = (middle_width, self.position[1] + self.text_size[1] // 2)

    def center_y(self) -> None:
        '''Adjust text directly in to middle of screen in y axis, helpfull when text is changable'''
        resolution = self.screen.get_size()
        middle_height = resolution[1] // 2
        new_height = middle_height - self.text_size[1] // 2
        self.position = (self.position[0], new_height)
        if self.background:
            self.background_rect.center = (self.position[0] + self.text_size[0] // 2, middle_height)


class Button:
    '''Class represents GUI buttons in game. Main feature is "callback" argument, which takes function.
    This function can be later executed by "execute" method'''
    def __init__(
        self,
        button_name: str,
        position: Coordinates,
        size: Coordinates,
        screen: pygame.surface.Surface,
        text: str,
        font_size: int,
        arguments=None,
        callback: callable = None,
        text_color: RGB_Color = RGB_COLORS["black"],
        mouse_over: bool = False,
        disabled: bool = False,
    ):
        self.button_name = button_name
        self.position = position
        self.size = size
        self.mouse_over = mouse_over
        self.screen = screen
        self.disabled = disabled
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.callback = callback
        self.arguments = arguments

        font = pygame.font.Font(COMMON_FONT_PATH, font_size)
        self.rendered_text = font.render(text, True, text_color)

        if self.arguments and not self.callback:
            raise ValueError

        
        
    def check_mouse_over(self, mouse_position: Coordinates) -> bool:
        return (
            self.position[0] <= mouse_position[0] <= self.position[0] + self.size[0]
            and self.position[1] <= mouse_position[1] <= self.position[1] + self.size[1]
        )

    def react(self) -> str:
        if self.mouse_over:
            return self.button_name

    def draw(self) ->  None:
        if self.disabled:
            image = BUTTON_TYPE_LOCKED
        else:
            if self.mouse_over:
                image = BUTTON_TYPE_AIMED
            else:
                image = BUTTON_TYPE_FREE
        image = pygame.transform.scale(image, (self.size))
        self.text_rect = self.rendered_text.get_rect()
        self.text_rect.center = (
            self.position[0] + (self.size[0] // 2),
            self.position[1] + (self.size[1] // 2),)
        self.screen.blit(image, self.position)
        self.screen.blit(self.rendered_text, self.text_rect)

    def execute(self) -> any:
        if callable(self.callback) and self.callback is not None:
            if self.arguments:
                return self.callback(*self.arguments)
            else:
                return self.callback()


class Gallow:
    '''Class represents gallow used in actuall game, it has ability to represent player progress by displaing correct image'''
    def __init__(
            self,
            background_size : Coordinates,
            background_position : Coordinates,
            gallow_size: Coordinates,
            gallow_position: Coordinates,
            screen: pygame.surface.Surface,
            stage: int = 0
            ):
        self.background_size = background_size
        self.background_position = background_position
        self.gallow_size = gallow_size
        self.gallow_position = gallow_position
        self.screen = screen
        self.stage = stage
        self.images = []
        for num in range(13):
            gallow_image = pygame.image.load(DIRNAME / f"data/images/gallow_{num}.png")
            gallow_image = pygame.transform.scale(gallow_image, (self.gallow_size))
            self.images.append(gallow_image)
        self.background_image = pygame.transform.scale(GALLOW_BACKGROUND, (self.background_size))

    def draw(self) -> None:
        self.screen.blit(self.background_image, self.background_position)
        try:
            self.screen.blit(self.images[self.stage], self.gallow_position)
        except:
            self.screen.blit(self.images[-1], self.gallow_position)
    
    def increase(self) -> None:
        self.stage += 1


class Text_box:
    '''Class provide possibility to provide text, for example name, which can be used by script later'''
    def __init__(
            self,
            position: Coordinates,
            font_size: int,
            screen: pygame.surface.Surface,
            sound_channel: pygame.mixer.Channel,
            color: RGB_Color=RGB_COLORS["green"],
            text: str="",
            font_path: str=None,
            char_limit: int=12,
    ):
        self.position = position
        self.font_size = font_size
        self.screen = screen
        self.sound_channel = sound_channel
        self.color = color
        self.text = text
        self.font_path = font_path
        self.char_limit = char_limit
        self.font = pygame.font.Font(font_path, font_size)
        self.rendered_text = self.font.render(text, True, color)

    def __str__(self) -> None:
        return f"{self.text.capitalize()}"   
    
    def draw(self) -> None:
        self.screen.blit(self.rendered_text, self.position)
    
    def modify(self, new_letter: str) -> None:
        if len(new_letter) == 1:
            if len(self.text) < self.char_limit:
                self.sound_channel.play(SOUND_EFFECTS["beep"])
                self.text = self.text.capitalize() + new_letter
                self.rendered_text = self.font.render(self.text, True, self.color)
            else:
                self.sound_channel.play(SOUND_EFFECTS["error"])

    def backspace(self) -> None:
        try:
            self.text = self.text[:-1].capitalize()
            self.rendered_text = self.font.render(self.text, True, self.color)
            self.sound_channel.play(SOUND_EFFECTS["wrong"])
        except:
            self.sound_channel.play(SOUND_EFFECTS["error"])


class Background:
    '''Class provides ability to blit background image in to screen. 
    Its usefull becouse it has "draw" method, just like other custom classes, so it can be blit alltogheter in "for" loop.'''
    def __init__(self, screen: pygame.surface.Surface, resolution: Coordinates , image:pygame.surface.Surface) -> None:
        self.screen = screen
        self.resolution = resolution
        self.image = pygame.transform.scale(image, (resolution))
    
    def draw(self) -> None:
        self.screen.blit(self.image, (0, 0))
