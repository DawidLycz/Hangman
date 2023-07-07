import json
import pickle

RESOLUTION_800_600_FILENAME =  "databases\\resolution_800_600.db"
RESOLUTION_1200_800_FILENAME =  "databases\\resolution_1200_800.db"
RESOLUTION_1920_1080_FILENAME =  "databases\\resolution_1920_1080.db"
RESOLUTION_1280_720_FILENAME =  "databases\\resolution_1280_720.db"

resolution = (1280,720)


prime_list = { "intro":
            {"text1" : (int(resolution[0]*(80/800)),int(resolution[1]*(30/600))),
            "text2" : (int(resolution[0]*(20/800)),int(resolution[1]*(380/600))),
            "text3" : (int(resolution[0]*(130/800)),int(resolution[1]*(430/600))),
            "font1" : int(resolution[0]*(200/800)), "font2" : int(resolution[0]*(39/800))},
        "outro": 
            {"button_font" : int(resolution[0]*30/800), "button_size" : (int(resolution[0]*150/800), int(resolution[1]*60/600)),
             "description_font" : int(resolution[0]*50/800), "title_font" : int(resolution[0]*150/800) , "name_font": int(resolution[0]*100/800),
             "button_size" : (int(resolution[0]*150/800), int(resolution[1]*60/600)),
             "button1_pos" : (int(resolution[0]*30/800), int(resolution[1]*530/600)),
             "button2_pos" : (int(resolution[0]*620/800), int(resolution[1]*530/600)),
             "title_pos" : (int(resolution[0]*50/800), int(resolution[1]*30/600)),
             "score_pos" : (int(resolution[0]*50/800), int(resolution[1]*220/600)),
             "desc_pos" :  (int(resolution[0]*50/800), int(resolution[1]*300/600)),
             "name_pos" : (int(resolution[0]*50/800), int(resolution[1]*360/600)),
             "button1_text_pos" : (int(resolution[0]*50/800),int(resolution[1]*540/600)),
             "button2_text_pos" : (int(resolution[0]*660/800),int(resolution[1]*540/600))},
        "victory_failure_display":
            {"title" : (int(resolution[0]*(50/800)), int(resolution[1])*(320/800)),
             "title_font" : int(resolution[0]*(200/800))},
        "game_menu":
            {"button_size" : (int((resolution[0])*(500/800)),int(resolution[1])*(80/600)),
             "button1_pos" : (int((resolution[0])*(150/800)),int((resolution[1])*(100/600))),
             "button2_pos" : (int((resolution[0])*(150/800)),int((resolution[1])*(200/600))),
             "button3_pos" : (int((resolution[0])*(150/800)),int((resolution[1])*(300/600))),
             "button4_pos" : (int((resolution[0])*(150/800)),int((resolution[1])*(400/600))),
             "button1_text_pos" : (int((resolution[0])*(310/800)),int((resolution[1])*(110/600))),
             "button2_text_pos" : (int((resolution[0])*(340/800)),int((resolution[1])*(210/600))),
             "button3_text_pos" : (int((resolution[0])*(250/800)),int((resolution[1])*(310/600))),
             "button4_text_pos" : (int((resolution[0])*(330/800)),int((resolution[1])*(410/600))),
             "font" : int((resolution[1])*(45/600))},
        "leaderboard_menu" :
            {"desc_font" : int(resolution[0]*45/800), "text_font" : int(resolution[0]*30/800),
             "button_size" : (int(resolution[0]*150/800), int(resolution[1]*60/600)),
             "button1_pos" : (int(resolution[0]*30/800), int(resolution[1]*530/600)),
             "button2_pos" : (int(resolution[0]*620/800), int(resolution[1]*530/600)),
             "button1_text_pos" : (int(resolution[0]*50/800),int(resolution[1]*540/600)),
             "button2_text_pos" : (int(resolution[0]*660/800),int(resolution[1]*540/600)),
             "desc_pos" : (int(resolution[0]*250/800),int(resolution[1]*10/600)),
             "height" : int(resolution[1]*70/600), "height_change" : int(resolution[1]*40/600), "score_x1" :  int(resolution[0]*50/800),
             "score_x2" : int(resolution[0]*300/800), "score_x3" : int(resolution[0]*550/800)},
        "settings_menu" : 
            {"desk_font" : int(resolution[0]*24/800), "button_font" : int(resolution[0]*22/800),
             "button_size_1" : (int(resolution[0]*180/800),int(resolution[1]*40/600)),
             "button_size_2" : (int(resolution[0]*40/800),int(resolution[1]*40/600)),
             "button_size_3" : (int(resolution[0]*150/800),int(resolution[1]*60/600)),
             "button_size_4" : (int(resolution[0]*600/800),int(resolution[1]*50/600)),
             "button_1" : (int(resolution[0]*100/800), int(resolution[1]*80/600)),
             "button_2" : (int(resolution[0]*310/800), int(resolution[1]*80/600)),
             "button_3" : (int(resolution[0]*520/800), int(resolution[1]*80/600)),
             "button_4" : (int(resolution[0]*100/800), int(resolution[1]*130/600)),
             "button_5" : (int(resolution[0]*310/800), int(resolution[1]*130/600)),
             "button_6" : (int(resolution[0]*520/800), int(resolution[1]*130/600)),
             "button_7" : (int(resolution[0]*100/800), int(resolution[1]*265/600)),
             "button_8" : (int(resolution[0]*280/800), int(resolution[1]*250/600)),
             "button_9" : (int(resolution[0]*280/800), int(resolution[1]*300/600)),
             "button_10" : (int(resolution[0]*400/800), int(resolution[1]*265/600)),
             "button_11" : (int(resolution[0]*580/800), int(resolution[1]*250/600)),
             "button_12" : (int(resolution[0]*580/800), int(resolution[1]*300/600)),
             "button_13" : (int(resolution[0]*100/800), int(resolution[1]*430/600)),
             "button_14" : (int(resolution[0]*325/800), int(resolution[1]*430/600)),
             "button_15" : (int(resolution[0]*30/800), int(resolution[1]*530/600)),
             "button_16" : (int(resolution[0]*620/800), int(resolution[1]*530/600)),
             "desc_button_1" : (int(resolution[0]*100/800),int(resolution[1]*20/600)),
             "desc_button_2" : (int(resolution[0]*100/800),int(resolution[1]*180/600)),
             "desc_button_3" : (int(resolution[0]*100/800),int(resolution[1]*360/600)),
             "desc_text_1" : (int(resolution[0]*330/800),(int(resolution[1]*30/600))),
             "desc_text_2" : (int(resolution[0]*360/800),(int(resolution[1]*190/600))),
             "desc_text_3" : (int(resolution[0]*370/800),(int(resolution[1]*370/600))),
             "text_1" : (int(resolution[0]*155/800),(int(resolution[1]*87/600))),
             "text_2" : (int(resolution[0]*365/800),(int(resolution[1]*87/600))),
             "text_3" : (int(resolution[0]*550/800),(int(resolution[1]*87/600))),
             "text_4" : (int(resolution[0]*155/800),(int(resolution[1]*137/600))),
             "text_5" : (int(resolution[0]*365/800),(int(resolution[1]*137/600))),
             "text_6" : (int(resolution[0]*575/800),(int(resolution[1]*137/600))),
             "text_7" : (int(resolution[0]*120/800),(int(resolution[1]*280/600))),
             "text_8" : (int(resolution[0]*295/800),(int(resolution[1]*255/600))),
             "text_9" : (int(resolution[0]*295/800),(int(resolution[1]*305/600))),
             "text_10" : (int(resolution[0]*420/800),(int(resolution[1]*280/600))),
             "text_11" : (int(resolution[0]*595/800),(int(resolution[1]*255/600))),
             "text_12" : (int(resolution[0]*595/800),(int(resolution[1]*305/600))),
             "text_13" : (int(resolution[0]*140/800),(int(resolution[1]*446/600))),
             "text_14" : (int(resolution[0]*360/800),(int(resolution[1]*446/600))),
             "text_15" : (int(resolution[0]*65/800),(int(resolution[1]*545/600))),
             "text_16" : (int(resolution[0]*665/800),(int(resolution[1]*545/600)))},
        "game_round" :
            {"gallow_background_size" : (int(resolution[0]*(180/800)),(int(resolution[1]*(250/600)))),
             "gallow_background_pos" : (int(resolution[0]*620/800),(int(resolution[1]*350/600))),
             "gallow_size" : (int(resolution[0]*(176/800)),(int(resolution[1]*(246/600)))),
             "gallow_pos" : (int(resolution[0]*622/800),(int(resolution[1]*352/600))),
             "font" : int(resolution[0]*36/800), "height" : int(resolution[1]*(130/600)),
             "category_info" : (int(resolution[0]*(20/800)),int(resolution[1]*(20/600))),
             "score_info" : (int(resolution[0]*(590/800)),int(resolution[1]*(20/600))),}}

res_800_600 = {
'intro': 
    {'text1': (80, 30), 'text2': (20, 380), 'text3': (20, 430), 'font1': 200, 'font2': 39},
'outro': 
    {'button_font': 30, 'button_size': (150, 60), 'description_font': 50, 'title_font': 150, 'name_font': 100, 'button1_pos': (30, 530),
    'button2_pos': (620, 530), 'title_pos': (50, 30), 'score_pos': (50, 220), 'desc_pos': (50, 300),
    'name_pos': (50, 360), 'button1_text_pos': (50, 540), 'button2_text_pos': (660, 540)},
'victory_failure_display': 
   {'title': (50, 240.0), 'title_font': 200}, 
'game_menu': 
    {'button_size': (500, 80), 'button1_pos': (150, 100), 'button2_pos': (150, 200), 'button3_pos': (150, 300),
    'button4_pos': (150, 400), 'button1_text_pos': (310, 109), 'button2_text_pos': (327, 210), 'button3_text_pos': (247, 310),
    'button4_text_pos': (335, 410), 'font': (45)},
'leaderboard_menu': 
    {'desc_font': 45, 'text_font': 30, 'button_size': (150, 60), 'button1_pos': (30, 530), 'button2_pos': (620, 530),
    'button1_text_pos': (50, 540), 'button2_text_pos': (660, 540), 'desc_pos': (250, 10), 'height': 70, 'height_change': 40,
    'score_x1': 50, 'score_x2': 300, 'score_x3': 550},
'settings_menu':
    {'desk_font': 24, 'button_font': 22, 'button_size_1': (180, 40), 'button_size_2': (40, 40), 'button_size_3': (150, 60),
    'button_size_4': (600, 50), 'button_1': (100.0, 80.0), 'button_2': (310, 80.0), 'button_3': (520, 80),
    'button_4': (100, 130), 'button_5': (310, 130), 'button_6': (520, 130), 'button_7': (100, 265),
    'button_8': (280, 250), 'button_9': (280, 300), 'button_10': (400, 265), 'button_11': (580, 250),
    'button_12': (580, 300), 'button_13': (100, 430), 'button_14': (325, 430), 'button_15': (660, 430), 'button_16': (30, 530),
    'button_17': (620, 530), 'desc_button_1': (100, 20), 'desc_button_2': (100, 180), 'desc_button_3': (100, 360),
    'desc_text_1': (330, 30), 'desc_text_2': (360, 190), 'desc_text_3': (370, 370), 'text_1': (155, 87), 'text_2': (365, 87),
    'text_3': (550, 87), 'text_4': (155, 137), 'text_5': (365, 137), 'text_6': (575, 137), 'text_7': (120, 280), 
    'text_8': (295, 255), 'text_9': (295, 305), 'text_10': (420, 280), 'text_11': (595, 255), 'text_12': (595, 305),
    'text_13': (140, 446), 'text_14': (360, 446), 'text_15': (65, 545), 'text_16': (665, 545)},
'game_round': 
   {'gallow_background_size': (180, 250), 'gallow_background_pos': (620, 350), 'gallow_size': (176, 245), 'gallow_pos': (622, 352),
    'font': 36, 'height': 130, 'category_info': (20, 20), 'score_info': (590, 20)}}

res_1200_800 = {
'intro': 
   {'text1': (120, 40), 'text2': (30, 506), 'text3': (195, 573), 'font1': 300, 'font2': 58}, 
'outro': 
   {'button_font': 45, 'button_size': (225, 80), 'description_font': 75, 'title_font': 225, 'name_font': 150,
    'button1_pos': (45, 706), 'button2_pos': (930, 706), 'title_pos': (75, 40), 'score_pos': (75, 293),
    'desc_pos': (75, 400), 'name_pos': (75, 480), 'button1_text_pos': (75, 720), 'button2_text_pos': (990, 720)},
'victory_failure_display':
   {'title': (75, 320.0), 'title_font': 300},
'game_menu': 
   {'button_size': (750, 106), 'button1_pos': (225, 133), 'button2_pos': (225, 266), 'button3_pos': (225, 400), 
    'button4_pos': (225, 533), 'button1_text_pos': (465, 146), 'button2_text_pos': (510, 280), 
    'button3_text_pos': (375, 413), 'button4_text_pos': (495, 546), 'font': 60},
'leaderboard_menu': 
   {'desc_font': 67, 'text_font': 45, 'button_size': (225, 80), 'button1_pos': (45, 706), 
    'button2_pos': (930, 706), 'button1_text_pos': (75, 720), 'button2_text_pos': (990, 720), 
    'desc_pos': (375, 13), 'height': 93, 'height_change': 53, 'score_x1': 75, 'score_x2': 450, 'score_x3': 825},
'settings_menu': 
   {'desk_font': 36, 'button_font': 33, 'button_size_1': (270, 53), 'button_size_2': (60, 53), 'button_size_3': (225, 80), 
    'button_size_4': (900, 66), 'button_1': (150, 106), 'button_2': (465, 106), 'button_3': (780, 106), 'button_4': (150, 173), 
    'button_5': (465, 173), 'button_6': (780, 173), 'button_7': (150, 353), 'button_8': (420, 333), 'button_9': (420, 400), 
    'button_10': (600, 353), 'button_11': (870, 333), 'button_12': (870, 400), 'button_13': (150, 573), 'button_14': (487, 573), 'button_15': (990, 573), 
    'button_16': (45, 706), 'button_17': (930, 706), 'desc_button_1': (150, 26), 'desc_button_2': (150, 240), 'desc_button_3': (150, 480), 
    'desc_text_1': (495, 40), 'desc_text_2': (540, 253), 'desc_text_3': (555, 493), 'text_1': (232, 116), 'text_2': (547, 116), 
    'text_3': (825, 116), 'text_4': (232, 182), 'text_5': (547, 182), 'text_6': (862, 182), 'text_7': (180, 373), 'text_8': (442, 340), 
    'text_9': (442, 406), 'text_10': (630, 373), 'text_11': (892, 340), 'text_12': (892, 406), 'text_13': (210, 594), 
    'text_14': (540, 594), 'text_15': (97, 726), 'text_16': (997, 726)},
'game_round': 
    {'gallow_background_size': (270, 333), 'gallow_background_pos': (930, 466), 'gallow_size': (264, 328), 
    'gallow_pos': (933, 469), 'font': 54, 'height': 173, 'category_info': (30, 26), 'score_info': (885, 26)}}

res_1920_1080 = {
'intro': 
   {'text1': (192, 54), 'text2': (35, 684), 'text3': (312, 774), 'font1': 480, 'font2': 93}, 
'outro': 
   {'button_font': 72, 'button_size': (360, 108), 'description_font': 120, 'title_font': 360, 'name_font': 240, 
    'button1_pos': (72, 954), 'button2_pos': (1488, 954), 'title_pos': (120, 54), 'score_pos': (120, 396), 
    'desc_pos': (120, 540), 'name_pos': (120, 648), 'button1_text_pos': (120, 972), 'button2_text_pos': (1584, 972)}, 
'victory_failure_display': 
   {'title': (120, 432.0), 'title_font': 480}, 
'game_menu': {'button_size': (1200, 144.0), 'button1_pos': (360, 180), 'button2_pos': (360, 360), 'button3_pos': (360, 540), 
    'button4_pos': (360, 720), 'button1_text_pos': (760, 198), 'button2_text_pos': (816, 378), 
    'button3_text_pos': (640, 558), 'button4_text_pos': (792, 738), 'font': 81}, 
'leaderboard_menu': 
   {'desc_font': 108, 'text_font': 72, 'button_size': (360, 108), 'button1_pos': (72, 954), 
    'button2_pos': (1488, 954), 'button1_text_pos': (120, 972), 'button2_text_pos': (1584, 972), 
    'desc_pos': (600, 18), 'height': 126, 'height_change': 72, 'score_x1': 120, 'score_x2': 720, 'score_x3': 1320}, 
'settings_menu': 
   {'desk_font': 57, 'button_font': 52, 'button_size_1': (432, 72), 'button_size_2': (96, 72), 'button_size_3': (360, 108), 
    'button_size_4': (1440, 90), 'button_1': (240, 144), 'button_2': (744, 144), 'button_3': (1248, 144), 'button_4': (240, 234), 
    'button_5': (744, 234), 'button_6': (1248, 234), 'button_7': (240, 477), 'button_8': (672, 450), 'button_9': (672, 540), 
    'button_10': (960, 477), 'button_11': (1392, 450), 'button_12': (1392, 540), 'button_13': (240, 774), 'button_14': (780, 774), 
    'button_15': (1584, 774), 'button_16': (72, 954), 'button_17': (1488, 954),  'desc_button_1': (240, 36), 'desc_button_2': (240, 324), 'desc_button_3': (240, 648), 
    'desc_text_1': (792, 49), 'desc_text_2': (864, 337), 'desc_text_3': (888, 661), 'text_1': (372, 150), 'text_2': (876, 151), 
    'text_3': (1320, 151), 'text_4': (372, 241), 'text_5': (876, 241), 'text_6': (1380, 241), 'text_7': (288, 499), 'text_8': (708, 454), 
    'text_9': (708, 544), 'text_10': (1008, 499), 'text_11': (1428, 454), 'text_12': (1428, 544), 'text_13': (336, 797), 
    'text_14': (864, 797), 'text_15': (156, 976), 'text_16': (1596, 976)}, 
'game_round': 
   {'gallow_background_size': (432, 450), 'gallow_background_pos': (1488, 630), 'gallow_size': (422, 442), 
    'gallow_pos': (1492, 633), 'font': 86, 'height': 234, 'category_info': (48, 36), 'score_info': (1416, 36)}}

res_1280_720 = {
'intro': 
    {'text1': (128, 36), 'text2': (32, 456), 'text3': (208, 516), 'font1': 320, 'font2': 62}, 
'outro': 
    {'button_font': 48, 'button_size': (240, 72), 'description_font': 80, 'title_font': 240, 'name_font': 160, 
     'button1_pos': (48, 636), 'button2_pos': (992, 636), 'title_pos': (80, 36), 'score_pos': (80, 264), 
     'desc_pos': (80, 360), 'name_pos': (80, 432), 'button1_text_pos': (90, 643), 'button2_text_pos': (1050, 643)}, 
'victory_failure_display': 
    {'title': (80, 288), 'title_font': 320}, 
'game_menu': 
    {'button_size': (800, 96), 'button1_pos': (240, 120), 'button2_pos': (240, 240), 'button3_pos': (240, 360), 
     'button4_pos': (240, 480), 'button1_text_pos': (255, 132), 'button2_text_pos': (255, 251), 
     'button3_text_pos': (255, 372), 'button4_text_pos': (255, 492), 'font': 54}, 
'leaderboard_menu': 
    {'desc_font': 72, 'text_font': 48, 'button_size': (240, 72), 'button1_pos': (48, 636), 
     'button2_pos': (992, 636), 'button1_text_pos': (80, 643), 'button2_text_pos': (1056, 643), 
     'desc_pos': (400, 12), 'height': 84, 'height_change': 48, 'score_x1': 80, 'score_x2': 480, 'score_x3': 880}, 
'settings_menu': 
    {'desk_font': 38, 'button_font': 35, 'button_size_1': (288, 48), 'button_size_2': (64, 48), 'button_size_3': (240, 72), 
     'button_size_4': (960, 60), 'button_1': (160, 96), 'button_2': (496, 96), 'button_3': (832, 96), 'button_4': (160, 156), 
     'button_5': (496, 156), 'button_6': (832, 156), 'button_7': (160, 318), 'button_8': (448, 300), 'button_9': (448, 360), 
     'button_10': (640, 318), 'button_11': (928, 300), 'button_12': (928, 360), 'button_13': (160, 516), 'button_14': (520, 516), 
     'button_15': (1056, 516), 'button_16': (48, 636), 'button_17': (992, 636),  'desc_button_1': (160, 24), 'desc_button_2': (160, 216), 'desc_button_3': (160, 432), 
     'desc_text_1': (528, 31), 'desc_text_2': (576, 223), 'desc_text_3': (592, 439), 'text_1': (248, 99), 'text_2': (584, 99), 
     'text_3': (880, 99), 'text_4': (248, 159), 'text_5': (584, 159), 'text_6': (920, 159), 'text_7': (192, 331), 'text_8': (472, 301), 
     'text_9': (472, 361), 'text_10': (672, 331), 'text_11': (952, 301), 'text_12': (952, 361), 'text_13': (230, 530), 
     'text_14': (576, 530), 'text_15': (104, 649), 'text_16': (1064, 649)}, 
'game_round': 
    {'gallow_background_size': (288, 300), 'gallow_background_pos': (992, 420), 'gallow_size': (281, 295), 
     'gallow_pos': (995, 422), 'font': 57, 'height': 156, 'category_info': (32, 24), 'score_info': (944, 24)}}

# with open (RESOLUTION_800_600_FILENAME, "rb") as stream:
#     old_res_800_600 = pickle.load(stream)
# with open (RESOLUTION_1200_800_FILENAME, "rb") as stream:
#     old_res_1200_800 = pickle.load(stream)
# with open (RESOLUTION_1920_1080_FILENAME, "rb") as stream:
#     old_res_1920_1080 = pickle.load(stream)
# with open (RESOLUTION_1280_720_FILENAME, "rb") as stream:
#     old_res_1280_720 = pickle.load(stream)

# if old_res_800_600 == res_800_600:
#     print("No changes were made to the 800:600 resolution parameters")
# else:
#     print("Changes were made to the 800:600 resolution parameters")
#     with open(RESOLUTION_800_600_FILENAME, "wb") as stream:
#         pickle.dump(res_800_600, stream)

# if old_res_1200_800 == res_1200_800:
#     print("No changes were made to the 1200:800 resolution parameters")
# else:
#     print("Changes were made to the 1200:800 resolution parameters")
#     with open(RESOLUTION_1200_800_FILENAME, "wb") as stream:
#         pickle.dump(res_1200_800, stream)

# if old_res_1920_1080 == res_1920_1080:
#     print("No changes were made to the 1920:1080 resolution parameters")
# else:
#     print("Changes were made to the 1920:1080 resolution parameters")
#     with open(RESOLUTION_1920_1080_FILENAME, "wb") as stream:
#         pickle.dump(res_1920_1080, stream)

# if old_res_1280_720 == res_1280_720:
#     print("No changes were made to the 1280:720 resolution parameters")
# else:
#     print("Changes were made to the 1280:720 resolution parameters")
#     with open(RESOLUTION_1280_720_FILENAME, "wb") as stream:
#         pickle.dump(res_1280_720, stream)

with open ("data\\resolutions\\800_600.json", "w", encoding="utf-8") as stream:
    json.dump(res_800_600, stream)
with open ("data\\resolutions\\1200_800.json", "w", encoding="utf-8") as stream:
    json.dump(res_1200_800, stream)
with open ("data\\resolutions\\1920_1080.json", "w", encoding="utf-8") as stream:
    json.dump(res_1920_1080, stream)
with open ("data\\resolutions\\1280_720.json", "w", encoding="utf-8") as stream:
    json.dump(res_1280_720, stream)


