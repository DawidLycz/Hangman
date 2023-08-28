import pygame
from hangman.hangman import check_mouse
from hangman.hangman import Inscription, Button, Gallow, Text_box

screen = pygame.display.set_mode((800,600), 0)
sound_channel = pygame.mixer.Channel(0)

TEST_INSCRIPTION = Inscription("test", (200, 0, 0), (0, 200), 30, screen)
TEST_BUTTON = Button("test", (100, 100), (100, 100), screen, "test", 8)
TEST_GALLOW = Gallow((100,100), (100,100), (98,98), (101, 101), screen)
TEST_TEXT_BOX = Text_box((0, 0), 8, screen, sound_channel)

def test_inscription_center_x():

    insc = TEST_INSCRIPTION
    insc.text_size = (100, 50)
    insc.center_x()
    x_position = insc.position[0]
    assert x_position == 350

def test_inscription_center_y():
    
    insc = TEST_INSCRIPTION
    insc.text_size = (100, 50)
    insc.center_y()
    y_position = insc.position[1]
    assert y_position == 275

def test_button_check_mouse_over_if_in_button():

    button = TEST_BUTTON
    mouse_pos = (130, 130)
    got = button.check_mouse_over(mouse_pos)
    assert got

def test_button_check_mouse_if_only_x_in_button():
    button = TEST_BUTTON
    mouse_pos = (130,300)
    got = button.check_mouse_over(mouse_pos)
    assert not got

def test_button_check_mouse_if_only_y_in_button():
    button = TEST_BUTTON
    mouse_pos = (300,130)
    got = button.check_mouse_over(mouse_pos)
    assert not got 

def test_button_check_mouse_if_out_of_button():
    button = TEST_BUTTON
    mouse_pos = (300,300)
    got = button.check_mouse_over(mouse_pos)
    assert not got

def test_gallow_increasing():
    gallow = TEST_GALLOW
    for i in range(5):
        gallow.increase()
    got = gallow.stage
    assert got == 5 

def test_text_box_input_letter():
    text_box = Text_box((0, 0), 8, screen, sound_channel)
    for i in range(5):
        text_box.modify("r")
    got = text_box.text
    assert got == "Rrrrr"

def test_text_box_input_multiple_letters():
    text_box = Text_box((0, 0), 8, screen, sound_channel)
    text_box.modify("rrr")
    got = text_box.text
    assert got == ""

def test_text_box_input_above_char_limit():
    text_box = Text_box((0, 0), 8, screen, sound_channel)
    text_box.char_limit = 3
    for i in range(5):
        text_box.modify("r")
    got = text_box.text
    assert got == "Rrr"

def test_text_box_backspace():
    text_box = Text_box((0, 0), 8, screen, sound_channel, text="Test")
    text_box.backspace()
    got = text_box.text
    assert got == "Tes"

def test_text_box_backspace_if_no_text():
    text_box = Text_box((0, 0), 8, screen, sound_channel, text="")
    text_box.backspace()
    got = text_box.text
    assert got == ""