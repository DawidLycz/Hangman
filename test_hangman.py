from Hangman import check_mouse

def test_check_mouse_if_in_button():
    position = (10,10)
    button_type = (100,100)
    mouse_pos = (21,33)
    got = check_mouse(position, button_type, mouse_pos)
    assert got == True

def test_check_mouse_if_only_x_in_button():
    position = (10,10)
    button_type = (100,100)
    mouse_pos = (21,300)
    got = check_mouse(position, button_type, mouse_pos)
    assert got == False

def test_check_mouse_if_only_y_in_button():
    position = (10,10)
    button_type = (100,100)
    mouse_pos = (200,30)
    got = check_mouse(position, button_type, mouse_pos)
    assert got == False

def test_check_mouse_if_out_of_button():
    position = (10,10)
    button_type = (100,100)
    mouse_pos = (200,300)    
    got = check_mouse(position, button_type, mouse_pos)
    assert got == False