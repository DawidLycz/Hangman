import pygame
import pytest
from hangman.hangman import check_mouse
from hangman.hangman import Inscription, Button, Gallow, Text_box

screen = pygame.display.set_mode((800,600), 0)
sound_channel = pygame.mixer.Channel(0)

@pytest.fixture
def inscription_fixture():
    return Inscription("test", (200, 0, 0), (0, 200), 30, screen)

@pytest.fixture
def button_fixture():
    return Button("test", (100, 100), (100, 100), screen, "test", 8)

@pytest.fixture
def text_box_fixture():
    return Text_box((0, 0), 8, screen, sound_channel)

def test_inscription_center_x(inscription_fixture):

    inscription_fixture.text_size = (100, 50)
    inscription_fixture.center_x()
    x_position = inscription_fixture.position[0]
    assert x_position == 350

def test_inscription_center_y(inscription_fixture):

    inscription_fixture.text_size = (100, 50)
    inscription_fixture.center_y()
    y_position = inscription_fixture.position[1]
    assert y_position == 275

def test_button_check_mouse_over_if_in_button(button_fixture):

    mouse_pos = (130, 130)
    got = button_fixture.check_mouse_over(mouse_pos)
    assert got

def test_button_check_mouse_if_only_x_in_button(button_fixture):

    mouse_pos = (130,300)
    got = button_fixture.check_mouse_over(mouse_pos)
    assert not got

def test_button_check_mouse_if_only_y_in_button(button_fixture):

    mouse_pos = (300,130)
    got = button_fixture.check_mouse_over(mouse_pos)
    assert not got 

def test_button_check_mouse_if_out_of_button(button_fixture):

    mouse_pos = (300,300)
    got = button_fixture.check_mouse_over(mouse_pos)
    assert not got

def test_gallow_increasing():

    gallow = Gallow((100,100), (100,100), (98,98), (101, 101), screen)
    for i in range(5):
        gallow.increase()
    got = gallow.stage
    assert got == 5 

def test_text_box_input_letter(text_box_fixture):

    for i in range(5):
        text_box_fixture.modify("r")
    got = text_box_fixture.text
    assert got == "Rrrrr"

def test_text_box_input_multiple_letters(text_box_fixture):

    text_box_fixture.modify("rrr")
    got = text_box_fixture.text
    assert got == ""

def test_text_box_input_above_char_limit(text_box_fixture):

    text_box_fixture.char_limit = 3
    for i in range(5):
        text_box_fixture.modify("r")
    got = text_box_fixture.text
    assert got == "Rrr"

def test_text_box_backspace(text_box_fixture):

    text_box_fixture.text = "Test"
    text_box_fixture.backspace()
    got = text_box_fixture.text
    assert got == "Tes"

def test_text_box_backspace_if_no_text(text_box_fixture):

    text_box_fixture.text=""
    text_box_fixture.backspace()
    got = text_box_fixture.text
    assert got == ""