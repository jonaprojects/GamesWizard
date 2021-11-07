import pygame
import pygame_widgets as pw
from pygame_widgets import TextBox, Slider
import pygame_gui
import socket
import json
import re
import random
import datetime
import time
import pandas as pd
from matplotlib import pyplot as plt
from Board import Board
from gui_page import GuiPage
from Form import Form
from User import User
from weapon import Weapon
import threading
from target import Target
import bisect
# ******************************************************* DATA SEGMENT **********************************************
# NETWORKING
IP = '127.0.0.1'
PORT = 45122
MAX_BYTES = 1024
# GRAPHICS
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000
REFRESH_RATE = 100
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0,)
# BACKGROUNDS
SPACE_BACKGROUND = 'space_backgrounds.png'
WOOD_BACKGROUND = 'wood_background.jpg'
GRASS_BACKGROUND = 'grass.jpg'
SKY_BACKGROUND = 'sky.jpg'
FLOWERS_BACKGROUND = 'flowers.jpg'
gui_background = "#3B5189"
current_index = 0
BACKGROUNDS = [SPACE_BACKGROUND, WOOD_BACKGROUND, GRASS_BACKGROUND, SKY_BACKGROUND, FLOWERS_BACKGROUND]
OPENING_SCREEN = True
SETTING_SCREEN = False
GAME_SCREEN = False
LAST_SCREEN_INDEX = 0
SCREENS = [OPENING_SCREEN, SETTING_SCREEN, GAME_SCREEN]
# GAMEPLAY
heart = pygame.image.load("heart.png")
heart = pygame.transform.scale(heart, (int(heart.get_width() / 15), int(heart.get_height() / 15)))
option_buttons = []
LAST_PLACE = 10
SCORE = 0
LIVES = 5
PLAYER_NAME = ""
current_question = ""
current_json_question = None
# SOUNDS
pygame.mixer.init()
CORRECT_SOUND = pygame.mixer.Sound('correct.mp3')
WRONG_SOUND = pygame.mixer.Sound('wrong.mp3')
BUTTON_CLICK = pygame.mixer.Sound('button_click.mp3')
DISABLED = pygame.mixer.Sound('disabled.mp3')
SECOND_BUTTON_CLICK = pygame.mixer.Sound('third_button.mp3')
JSON_CHARS = {
    "&quot;": '"',
    "&#039;": "'",
    "&rsquo;": "'",

}

CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT_SOCKET.connect((IP, PORT))
CLIENT_SOCKET.send("weather".encode())
TEMPERATURE = CLIENT_SOCKET.recv(MAX_BYTES).decode()
current_user = None  # the current user that passed the login stage.
time_start = time.time()
time_end = time.time()

# PAINTER
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (127, 0, 255)
ORANGE = (255, 128, 0)
BACKGROUND = WHITE  # in order to change it sometimes
CURRENT_X = 0
CURRENT_Y = 0
CURRENT_COLOR = BLACK
# CLOCK RELATED CONSTANTS
# OTHERS
sound_on = True
music_on = True
RADIUS = 8
PAINTER_WIDTH = 1000
PAINTER_HEIGHT = 800
my_multiplayer_turn = ''
opponent_move = ''
taken_squares = []
# GUN GAME CONSTANTS

WIDTH = 1000
HEIGHT = 800
aim_color = "#F1310A"
aim_size = 15
TARGET_IMAGE = pygame.image.load("target.png")
creation_frequency = 500
game_finished = False
targets = []
max_targets = 5
total_targets = 0
targets_hit = 0
background_color = "#CDCFD5"
aim_mode = 0
SNIPER_SHOT = pygame.mixer.Sound("gunshot.mp3")
SHOTGUN_SHOT = pygame.mixer.Sound("shotgun.mp3")
max_seconds = 50
seconds = 50
full_ammo = [40, 60, 35]
ammo = [40, 60, 35]
images = ["sniper.png", "rifle.png", "shotgun.png"]
scales = [0.7, 0.6, 0.6]
max_grenades = 3
current_grenades = 1
sniper = Weapon(name="sniper", image_path="sniper.png", size_factor=0.7, ammo=40, current_ammo=40,
                sound_effect=SNIPER_SHOT)
rifle = Weapon(name='rifle', image_path="rifle.png", size_factor=0.6, ammo=60, current_ammo=60,
               sound_effect=SNIPER_SHOT)  # same sound as the sniper, but repeats 3 times.
shotgun = Weapon(name="shotgun", image_path="shotgun.png", size_factor=0.6, ammo=35, current_ammo=35,
                 sound_effect=SHOTGUN_SHOT)
weapons = [None, None, None]
current_weapon_index = 0


def change_color(color):
    global CURRENT_COLOR
    CURRENT_COLOR = color


def fade(window, width, height):
    surface = pygame.Surface((width, height))
    for alpha in range(0, 300):
        surface.set_alpha(alpha)
        redraw_window(window)
        window.blit(surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)


def redraw_window(window):
    window.fill((255, 255, 255))


def draw_aim(window, mouse_x, mouse_y, length=20, gun_mode=0, radius=5):
    """ DRAWS THE AIM"""
    if gun_mode == 0:
        """ NORMAL AIM """
        pygame.draw.line(window, aim_color, (mouse_x, mouse_y), (mouse_x + length, mouse_y), width=5)
        pygame.draw.line(window, aim_color, (mouse_x, mouse_y), (mouse_x - length, mouse_y), width=5)
        pygame.draw.line(window, aim_color, (mouse_x, mouse_y), (mouse_x, mouse_y + length), width=5)
        pygame.draw.line(window, aim_color, (mouse_x, mouse_y), (mouse_x, mouse_y - length), width=5)
    elif gun_mode == 1:
        """ AUTOMATIC GUN AIM ( NEEDS TO BE PURCHASED )"""
        pygame.draw.circle(surface=window, color="#E8401E", center=(mouse_x, mouse_y), radius=radius)
    elif gun_mode == 2:
        """ SHOTGUN """
        pygame.draw.circle(surface=window, color="#E8401E", center=(mouse_x, mouse_y), radius=20, width=5)
        pygame.draw.circle(surface=window, color="#E8401E", center=(mouse_x, mouse_y), radius=30, width=5)
        pygame.draw.line(window, aim_color, (mouse_x + 5, mouse_y + 10), (mouse_x + 20, mouse_y + 20), width=5)
        pygame.draw.line(window, aim_color, (mouse_x - 5, mouse_y - 10), (mouse_x - 20, mouse_y - 20), width=5)
        pygame.draw.line(window, aim_color, (mouse_x + 5, mouse_y - 10), (mouse_x + 20, mouse_y - 20), width=5)
        pygame.draw.line(window, aim_color, (mouse_x - 5, mouse_y + 10), (mouse_x - 20, mouse_y + 20), width=5)


def gun_sound():
    """ gun sound """
    print("gun sound")
    for i in range(3):
        SNIPER_SHOT.play()
        time.sleep(0.1)


def update_timer(timer_label):
    minutes = "0" + str(seconds // 60) if seconds < 600 else str(seconds // 60)
    secs = seconds % 60
    secs = "0" + str(secs) if secs < 10 else str(secs)
    timer_label.set_text(f"{minutes}:{secs}")


def finishing_screen(page, score):
    global current_user
    pygame.mixer.music.stop()
    if current_user is not None:
        current_user['_User__cash'] += int(score)
        CLIENT_SOCKET.send(f"replace{json.dumps(current_user)}".encode())
    page.clear_all()
    fade(page.get_window(), WIDTH, HEIGHT)
    page.add_label(y=250, x1=400, text=f"Success:{round(targets_hit / total_targets * 100, 2)}%", centered=True,
                   object_id="rating_label")
    page.add_label(y=450, x1=400, text=f"Score:{score}", centered=True, object_id="rating_label")
    page.add_button(x=750, y=650, text="Back", object_id="gui_button")


def update_ammo(ammo_label):
    """ Updates the label that keeps track of the ammunition """
    ammo_label.set_text(f"{weapons[current_weapon_index].get_current_ammo()}/"
                        f"{weapons[current_weapon_index].get_ammo()}")


def update_weapon_image(page, old_image):
    """ switches between the images of the guns """
    old_image.kill()
    return page.add_image(path=weapons[current_weapon_index].get_image_path(), x=40, y=600,
                          size_factor=weapons[current_weapon_index].get_size_factor())


def update_grenade_label(grenade_label):
    """updates the number of grenades remaining"""
    grenade_label.set_text(f"{current_grenades}/{max_grenades}")


def run_painter():
    """Displays a pygame window"""
    global CURRENT_X, CURRENT_Y, RADIUS, CURRENT_COLOR
    pygame.init()
    page = GuiPage(title="Painter", width=PAINTER_WIDTH, height=PAINTER_HEIGHT, hex_color="#FFFFFF",
                   theme='theme.json')
    page.add_button(x=PAINTER_WIDTH * 0.85, y=PAINTER_HEIGHT * 0.85, width=PAINTER_WIDTH / 10,
                    height=PAINTER_HEIGHT / 15, text="Back")
    page.add_slider(y=PAINTER_HEIGHT * 0.85, min_value=1,
                    max_value=50,
                    start_value=25, centered=True)
    page.add_button(y=PAINTER_HEIGHT * 0.85, x=PAINTER_WIDTH / 10, text="Choose Color")
    page.get_window().blit(page.background, (0, 0))
    screen = page.get_window()
    pygame.display.flip()
    running = True
    isPressed = False
    redraw = False
    color_picker = 0
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("reached button down")
                isPressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                print("reached button up")
                isPressed = False
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    button = event.ui_element
                    if button.text == "Back":
                        games_gui()
                    elif button.text == "Choose Color":
                        color_picker = page.add_color_picker()
                        redraw = True
                elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    slider = event.ui_element
                    RADIUS = slider.get_current_value()
                elif event.user_type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                    if event.ui_element == color_picker:
                        RADIUS = 25
                        SECOND_BUTTON_CLICK.play()
                        CURRENT_COLOR = pygame.Color(event.colour)
                        redraw = False
            elif event.type == pygame.MOUSEMOTION and isPressed:
                CURRENT_X, CURRENT_Y = pygame.mouse.get_pos()
                if 90 < CURRENT_X < WINDOW_WIDTH * 0.95 and 0.05 * WINDOW_HEIGHT < CURRENT_Y < WINDOW_HEIGHT * 0.9:
                    pygame.draw.circle(screen, CURRENT_COLOR, [CURRENT_X, CURRENT_Y], RADIUS)
            page.manager.process_events(event)
        if redraw:
            page.get_window().blit(page.background, (0, 0))
        page.manager.update(0)
        page.manager.draw_ui(page.get_window())
        pygame.display.update()
    pygame.quit()


# *********************************************************************************************************************
# TODO
# GET A COOL-DOWN FOR THE GRENADE AND THE AMMO SWITCH
# FIX THE LEADERBOARD - TURN IT TO JSON FORMAT, AND SORT ACCORDINGLY.


def request_leaderboard():
    """ request the leaderboard in json from the server"""
    CLIENT_SOCKET.send("leader".encode())
    leaderboard = json.loads(CLIENT_SOCKET.recv(MAX_BYTES))
    return [json.loads(player) for player in leaderboard]


def disconnect():
    """ disconnecting from the server"""
    CLIENT_SOCKET.close()


def play_music(music):
    """ playing music using pygame's mixer ( not the same as playing sounds ) """
    if music_on:
        pygame.mixer.music.load(music)
        pygame.mixer.music.play()


def get_question(client_socket):
    """ gets question json obj from server"""
    client_socket.send("question".encode('utf-8'))
    content = client_socket.recv(MAX_BYTES).decode()
    p = re.compile('(?<!\\\\)\'')
    content = p.sub('\"', content)
    json_question = json.loads(content)
    return json_question


def get_player_json(name, score):
    """ convert the player's relevant data to json format , so later it will be sent to the server """
    player = {"name": name,
              "score": score,
              "date": datetime.datetime.now().strftime("%A / %d / %Y")
              }
    return json.dumps(player)


def add_to_leaderboard(name, score):
    """ request the server to add the player's json to the leaderboard"""
    print(f'sending add{get_player_json(name, score)}')
    CLIENT_SOCKET.send(f'add{get_player_json(name, score)}'.encode())


def change_background(screen, image_path):
    """ change the background to the specified image in the specified window """
    img = pygame.image.load(image_path)
    img = pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(img, (0, 0))
    pygame.display.flip()


def refresh(screen):
    """ refresh the page to delete unnecessary widgets """
    print("refreshed the trivia screen !")
    change_background(screen, BACKGROUNDS[current_index])


def set_name(screen, text):
    """ set the player's name ( in the trivia game )"""
    global PLAYER_NAME
    PLAYER_NAME = text
    print("called")
    start_game(screen)


def settings_screen(screen):
    """ Switches the boolean variables necessary to switch to settings page"""
    pygame.mixer.music.pause()
    BUTTON_CLICK.play()
    global SETTING_SCREEN, OPENING_SCREEN, GAME_SCREEN, LAST_SCREEN_INDEX
    LAST_SCREEN_INDEX = 0 if OPENING_SCREEN else 1 if GAME_SCREEN else 2
    SETTING_SCREEN = True
    OPENING_SCREEN = False
    GAME_SCREEN = False


def opening_screen(screen):
    """ Switches the boolean variables necessary to switch to opening page"""
    global SETTING_SCREEN, OPENING_SCREEN, GAME_SCREEN, LAST_SCREEN_INDEX
    pygame.mixer.music.unpause()
    LAST_SCREEN_INDEX = 0 if OPENING_SCREEN else 1 if SETTING_SCREEN else 2
    SETTING_SCREEN = False
    OPENING_SCREEN = True
    GAME_SCREEN = False


def game_screen(screen):
    """ Switches the boolean variables necessary to switch to game page"""
    global SETTING_SCREEN, OPENING_SCREEN, GAME_SCREEN, LAST_SCREEN_INDEX
    LAST_SCREEN_INDEX = 0 if OPENING_SCREEN else 1 if SETTING_SCREEN else 2
    SETTING_SCREEN = False
    OPENING_SCREEN = False
    GAME_SCREEN = True
    pygame.mixer.music.unpause()
    refresh(screen)
    add_text(screen, "THE TRIVIA GAME!", (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 10), 60)
    for button in option_buttons:
        button.draw()


def do_nothing(nothing):
    """ does nothing. beautiful, and simple """
    pass


def new_button(screen, content, width, height, step_width, step_height, func=do_nothing("nothing")):
    """ creates a new button of pygame_widgets gui module """
    font = pygame.font.SysFont("comicsansms", 30)
    button = pw.Button(
        screen, int(width), int(height), int(step_width),
        int(step_height),
        text=content, font=font, margin=10,
        inactiveColour=GREEN, pressedColour=(255, 255, 255), radius=0, onClick=lambda: func(screen))
    return button


def display_current_question(current_window):
    """ display the current trivia question in the specified window. text is from pygame_widgets """
    font_size = 40 if len(current_question) < 90 else 30
    add_text(current_window, current_question, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), font_size)


def new_question(screen, client_socket):
    global time_start, option_buttons, current_question
    """f etches a new question and options and displays them """
    time.sleep(0.3)
    print("fetching a new question !")
    option_buttons = []
    json_question = get_question(client_socket)
    for key, value in JSON_CHARS.items():
        json_question['question'] = json_question['question'].replace(key, value)
    refresh(screen)
    add_text(screen, "THE TRIVIA GAME!", (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 10), 60)
    current_question = json_question["question"]
    display_current_question(screen)
    buttons = generate_option_buttons(screen, json_question)
    for button in buttons:
        option_buttons.append(button)
    time_start = time.time()  # start timer
    print("started timer")


def start_game(screen):
    """start the trivia game"""
    pygame.mixer.music.stop()
    if music_on:
        pygame.mixer.music.load("game_on.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()
    BUTTON_CLICK.play()
    game_screen(screen)
    refresh(screen)
    new_question(screen, CLIENT_SOCKET)


def correct_index(questions, correct_answer):
    """ finds the index of the question that has the right answer ( it was randomly shuffled before .. )  """
    return questions.index(correct_answer)


def add_score(score=100):
    """ add to the score """
    global SCORE
    SCORE += score
    print(f"THE SCORE IS {SCORE} ")


def add_and_next(screen):
    """ If the answer is correct, then add 100 to the score, and move on to the next question """
    global time_end
    time_end = time.time()
    print(f"{time_end - time_start} seconds elapsed")
    if time_end - time_start < 10:
        add_score(int(time_end - time_start) * random.randint(5, 10))
    add_score()
    CORRECT_SOUND.play()
    new_question(screen, CLIENT_SOCKET)


def wrong_and_next(screen):
    global time_end, LIVES
    time_end = time.time()
    print(f"{time_end - time_start} seconds elapsed")
    LIVES -= 1
    WRONG_SOUND.play()
    new_question(screen, CLIENT_SOCKET)


def cmp_indices(index, true_index):
    "RETURNING A FUNCTION"
    if index == true_index:
        return add_and_next

    return wrong_and_next


def generate_option_buttons(screen, json_question):
    questions = [json_question['correct_answer']] + json_question['incorrect_answers']
    random.shuffle(questions)
    index = correct_index(questions, json_question["correct_answer"])
    buttons = [
        new_button(screen, questions[0], WINDOW_WIDTH / 4 + 25, WINDOW_HEIGHT / 3 * 1.8, WINDOW_WIDTH / 5,
                   WINDOW_HEIGHT / 7,
                   cmp_indices(0, index)),
        new_button(screen, questions[1], WINDOW_WIDTH / 2 + 25, WINDOW_HEIGHT / 3 * 1.8, WINDOW_WIDTH / 5,
                   WINDOW_HEIGHT / 7,
                   cmp_indices(1, index)),
        new_button(screen, questions[2], WINDOW_WIDTH / 4 + 25, WINDOW_HEIGHT / 6 * 4.5, WINDOW_WIDTH / 5,
                   WINDOW_HEIGHT / 7,
                   cmp_indices(2, index)),
        new_button(screen, questions[3], WINDOW_WIDTH / 2 + 25, WINDOW_HEIGHT / 6 * 4.5, WINDOW_WIDTH / 5,
                   WINDOW_HEIGHT / 7,
                   cmp_indices(3, index)),

    ]
    return buttons


def switch_backgrounds(screen):
    BUTTON_CLICK.play()
    global current_index
    current_index += 1
    if current_index == len(BACKGROUNDS):
        current_index = 0
    change_background(screen, BACKGROUNDS[current_index])


def go_back(screen):
    BUTTON_CLICK.play()
    if LAST_SCREEN_INDEX == 0:
        change_background(screen, BACKGROUNDS[current_index])
        opening_screen(screen)
    elif LAST_SCREEN_INDEX == 1:
        change_background(screen, BACKGROUNDS[current_index])
        settings_screen(screen)
    elif LAST_SCREEN_INDEX == 2:
        change_background(screen, BACKGROUNDS[current_index])
        game_screen(screen)


def get_buttons(screen):
    font = pygame.font.SysFont("comicsansms", 30)
    settings_button = pw.Button(
        screen, int(WINDOW_WIDTH / 10), int(WINDOW_HEIGHT / 5), int(WINDOW_WIDTH / 5), int(WINDOW_HEIGHT / 20),
        text='SETTINGS',
        font=font, margin=10,
        inactiveColour=WHITE, pressedColour=(255, 255, 255), radius=0, onClick=lambda: settings_screen(screen)
    )
    background_button = pw.Button(
        screen, int(WINDOW_WIDTH / 15), int(WINDOW_HEIGHT / 5), int(WINDOW_WIDTH / 3), int(WINDOW_HEIGHT / 15),
        text='Change Background', font=font, margin=10,
        inactiveColour=WHITE, pressedColour=(255, 255, 255), radius=0, onClick=lambda: switch_backgrounds(screen)
    )
    back = pw.Button(
        screen, int(WINDOW_WIDTH / 15), int(WINDOW_HEIGHT / 4 * 3), int(WINDOW_WIDTH / 10), int(WINDOW_HEIGHT / 10),
        text='BACK', font=font, margin=10,
        inactiveColour=WHITE, pressedColour=(255, 255, 255), radius=0, onClick=lambda: go_back(screen))
    start_button = pw.Button(
        screen, int(WINDOW_WIDTH / 2) - int(WINDOW_HEIGHT / 6), int(WINDOW_HEIGHT / 4 * 3), int(WINDOW_HEIGHT / 3),
        int(WINDOW_HEIGHT / 15),
        text='START!', font=font, margin=10,
        inactiveColour=GREEN, pressedColour=(255, 255, 255), radius=0, onClick=lambda: start_game(screen))

    return [settings_button, back], [background_button, back], [settings_button, back]
    # START BUTTON WAS REMOVED ! PUT IN THE FIRST LIST IN CASE THAT IT'S REQUIRED !
    # RETURNS THE BUTTONS LIKE THIS: OPENING BUTTONS, SETTINGS BUTTONS, GAMEPLAY BUTTONS


def draw_leaderboard(top_scores):
    fig, ax = plt.subplots()
    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    plt.suptitle("Leaderboard\n", fontsize=18, y=0.95)
    plt.title(f"Our current winner is {top_scores[0]['name']}", color="grey", style='italic', y=0.85)
    print(len(top_scores))
    df = pd.DataFrame(([top_scores[0]["name"], top_scores[0]["score"]],
                       [top_scores[1]["name"], top_scores[1]["score"]], [top_scores[2]["name"], top_scores[2]["score"]],
                       [top_scores[3]["name"], top_scores[3]["score"]], [top_scores[4]["name"], top_scores[4]["score"]],
                       [top_scores[5]["name"], top_scores[5]["score"]],
                       [top_scores[6]["name"], top_scores[6]["score"]], [top_scores[7]["name"], top_scores[7]["score"]],
                       [top_scores[7]["name"], top_scores[7]["score"]], [top_scores[8]["name"], top_scores[8]["score"]],
                       [top_scores[9]["name"], top_scores[9]["score"]]
                       ),
                      columns=['Top Players', 'Top Scores'])

    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center',
                     cellLoc='center')
    table.auto_set_font_size(False)

    table.set_fontsize(15)
    table.scale(1.5, 1.5)
    fig.tight_layout()
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.show()


def create_window():
    pygame.init()
    size = WINDOW_WIDTH, WINDOW_HEIGHT
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    screen.fill(WHITE)
    change_background(screen, 'space_backgrounds.png')
    pygame.display.set_caption("Trivia")
    pygame.display.flip()
    return screen


def main_loop(screen, opening_buttons=(), settings_buttons=(), gameplay_buttons=()):
    global WINDOW_HEIGHT, WINDOW_WIDTH
    pygame.font.init()
    play_music('opening_music.mp3')
    clock = pygame.time.Clock()
    running = True
    textbox = TextBox(screen, int(WINDOW_WIDTH / 2) - int(WINDOW_HEIGHT / 2.2), int(WINDOW_HEIGHT / 4 * 3),
                      int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 10), fontSize=65,
                      borderColour=(255, 0, 0), textColour=(0, 200, 0),
                      onSubmit=lambda: set_name(screen, textbox.getText()), radius=10, borderThickness=5)
    # Do a real opening screen with the text box
    while running:
        if OPENING_SCREEN:
            add_text(screen, "THE TRIVIA GAME!", (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 10)), 60)
            add_text(screen, "ENTER YOUR NAME!", (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT * 0.5)), 45)
            add_text(screen, f"{TEMPERATURE}", (int(WINDOW_WIDTH * 0.9), int(WINDOW_HEIGHT / 10)), 30)
        elif SETTING_SCREEN:
            change_background(screen, BACKGROUNDS[current_index])
            add_text(screen, "SETTINGS", (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 13), 50)
        elif GAME_SCREEN:
            display_current_question(screen)
            add_text(screen, f"SCORE:{SCORE}", (int(WINDOW_WIDTH / 10), int(WINDOW_HEIGHT / 10)), 30)
            # add_text(screen, f"LIVES:{LIVES}", (WINDOW_WIDTH / 5.5, WINDOW_HEIGHT / 10), 30)
            x_distance = 45
            for i in range(LIVES):
                screen.blit(heart, (WINDOW_WIDTH / 10 + x_distance * (i + 2), WINDOW_HEIGHT / 11))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                change_background(screen, BACKGROUNDS[current_index])
                WINDOW_HEIGHT = event.h
                WINDOW_WIDTH = event.w
        if OPENING_SCREEN:
            for button in opening_buttons:
                button.listen(events)
                button.draw()
            textbox.draw()
            textbox.listen(events)
        elif SETTING_SCREEN:
            for button in settings_buttons:
                button.listen(events)
                button.draw()
        elif GAME_SCREEN:
            for button in gameplay_buttons:
                button.listen(events)
                button.draw()
            for button in option_buttons:
                button.listen(events)
                button.draw()
        clock.tick(REFRESH_RATE)
        pygame.display.flip()
        if LIVES < 1:
            running = False
    add_to_leaderboard(PLAYER_NAME, SCORE)
    print("requesting leaderboard...")
    leaderboard = request_leaderboard()
    draw_leaderboard(leaderboard)
    rating_gui()


def add_text(screen, text, position, font_size):
    font = pygame.font.SysFont('comicsansms', font_size)
    text = font.render(text, True, (0, 0, 0), WHITE)

    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()

    # set the center of the rectangular object.
    textRect.center = position
    screen.blit(text, textRect)
    pygame.display.flip()


def run_main_loop():
    screen = create_window()
    opening_buttons, settings_buttons, gameplay_buttons = get_buttons(screen)
    main_loop(screen, opening_buttons, settings_buttons, gameplay_buttons)


mode = 0


def change_mode(win, num):
    global mode
    mode = num
    change_background(win, BACKGROUNDS[current_index])


def get_avg_rating():
    """ fetches the average rating the game gets from the players, from the server"""
    CLIENT_SOCKET.send("avg".encode('utf-8'))
    return CLIENT_SOCKET.recv(MAX_BYTES).decode('utf-8')


average_rating = get_avg_rating()


def send_rating(rating):
    global average_rating
    print(f"rate{rating}")
    json_obj = json.dumps({"player": PLAYER_NAME, "rating": f"{rating}"})
    CLIENT_SOCKET.send(f"rate{json_obj}".encode())

    average_rating = get_avg_rating()


def update_label_text(label, value):
    """ updates label's text"""
    label.set_text(value)


def rating_gui():
    global WINDOW_WIDTH, WINDOW_HEIGHT, average_rating
    pygame.init()
    pygame.mixer.stop()
    page = GuiPage(title="Options", width=800, height=800, hex_color=gui_background, theme="theme.json")
    rating_title = page.add_label(y=60, x1=400, text="Rate Our Game", centered=True, object_id="rating_title")
    rating_slider = page.add_slider(y=400, centered=True)
    rating_label = page.add_label(y=450, x1=90, y1=90, text=f"{rating_slider.current_value}", centered=True,
                                  object_id="rating_label")
    average_rating_label = page.add_label(y=300, x1=500, text=f"Average Rating: {average_rating}", centered=True,
                                          object_id="average_rating")
    page.add_button(y=600, width=150, height=70, text="Submit", centered=True)
    running = True
    while running:
        time_delta = page.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    button = event.ui_element
                    if button.text == "Submit":
                        SECOND_BUTTON_CLICK.play()
                        print(f"AVERAGE RATING: {average_rating}")
                        send_rating(rating_slider.get_current_value())
                        page.clear_all()
                        average_rating_label = page.add_label(y=300, x1=300, text=f"Average Rating:{average_rating}",
                                                              centered=True, object_id="average_rating")
                        page.add_label(y=300, x1=600,
                                       centered=True, text="Thank You !", object_id="rating_title")
                    elif button.text == "Exit":
                        disconnect()
                        running = False
                elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == rating_slider:
                        update_label_text(label=rating_label, value=f"{rating_slider.current_value}")

            if event.type == pygame.VIDEORESIZE:
                pass

            page.manager.process_events(event)
        page.manager.update(time_delta)
        page.get_window().blit(page.background, (0, 0))
        page.manager.draw_ui(page.get_window())
        pygame.display.update()


def get_coordinates_by_move(index, window_width, window_height):
    """ gets an index of a move in tic tac toe, and returns the matching x,y coordinates ."""
    x, y = -1, -1
    if 0 <= index <= 2:  # FIRST ROW
        y = 0.25 * window_height
    elif 3 <= index <= 5:  # SECOND ROW
        y = 0.5 * window_height
    elif 6 <= index <= 8:  # THIRD ROW
        y = 0.75 * window_height

    if index % 3 == 0:  # FIRST COLUMN
        x = window_width * 0.25
    elif (index - 1) % 3 == 0:  # SECOND COLUMN
        x = window_width * 0.5
    elif (index - 2) % 3 == 0:  # THIRD COLUMN
        x = window_width * 0.75
    return x, y


def get_drawing_pos(screen, x, y, window_width, window_height):
    """getting the place to draw the circle or x from the mouse coordinates """
    index = 0
    width = -1
    if window_width * 0.15 < x < window_width * 0.33:
        width = 0.25 * window_width
    elif window_width * 0.33 < x < window_width * 0.66:
        index += 1
        width = 0.5 * window_width
    elif window_width * 2 / 3 < x < window_width * 0.85:
        index += 2
        width = 0.75 * window_width
    height = -1
    if 0.2 < y < window_height / 3:
        height = 0.25 * window_height
    elif window_height / 3 < y < window_height / 3 * 2:
        height = 0.5 * window_height
        index += 3
    elif window_height / 3 * 2 < y < window_height * 0.85:
        index += 6
        height = 0.75 * window_height
    return width, height, index


def draw_circle(screen, x, y, radius, board, window_width, window_height):
    """ drawing a red circle """
    width, height, index = get_drawing_pos(screen, x, y, window_width, window_height)
    if height != -1 and width != -1 and board.is_empty_square(index):
        pygame.draw.circle(screen, RED, (width, height), radius, 15)
        board.fill_empty_square(index, 'o')
        return index, True
    return -1, False


def draw_x(screen, x, y, board, window_width, window_height):
    width, height, index = get_drawing_pos(screen, x, y, window_width, window_height)
    if board.is_empty_square(index):
        if height != -1 and width != -1:
            pygame.draw.line(screen, (0, 0, 0), (width - 30, height - 30), (width + 20, height + 30), width=30)
            pygame.draw.line(screen, (0, 0, 0), (width - 30, height + 30), (width + 20, height - 30), width=30)
            print(f"x index is {index}")
        board.fill_empty_square(index, 'x')
        return index, True
    DISABLED.play()
    return -1, False


def tic_tac_toe(difficulty="easy", multiplayer=False, my_turn='x'):
    global opponent_move
    pygame.mixer.init()
    opponent_wait_thread = threading.Thread(target=wait_for_move)
    board = Board()  # creating an empty board
    window_width, window_height = 800, 800
    pygame.init()
    win = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    win.fill(gui_background)
    font = pygame.font.SysFont("comicsansms", 45)
    running = True
    clock = pygame.time.Clock()
    btns = []
    x_turn = True
    game_mode = 0
    winner = 'e'
    if my_turn == 'x':
        current_turn = True
    elif my_turn == 'o':
        current_turn = False
    else:
        current_turn = ""
        print("BUG. UNKNOWN TURN !")
    while running:
        events = pygame.event.get()
        for event in events:
            for i in range(int(window_width / 3), int(window_width) - 50, int(window_width / 3)):
                pygame.draw.line(win, (0, 0, 0), (i, int(window_height / 5)), (i, int(window_height * 4 / 5)), width=30)
            for i in range(int(window_height / 3), int(window_height) - 50, int(window_height / 3)):
                pygame.draw.line(win, (0, 0, 0), (int(window_width / 7), i), (int(window_width * 6 / 7), i), width=30)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                window_height = event.h
                window_width = event.w
                win.fill(gui_background)
            if not multiplayer:
                if game_mode == 0:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if x_turn:
                            index, res = draw_x(win, x, y, board, window_width, window_height)
                            time.sleep(0.1)
                            if board.check_full_board():
                                game_mode = 1
                                winner = board.check_winning()
                            elif res:
                                computer_move = board.basic_find_move(
                                    'o') if difficulty == "easy" else board.medium_find_move('o')
                                if computer_move == "resign":
                                    print("The computer has resigned the game !")
                                    add_text(win, "The computer has resigned the game !",
                                             (int(window_width / 2), int(window_height / 8)), 35)
                                    game_mode = 1
                                    winner = "x"
                                elif computer_move is not None:
                                    x, y = get_coordinates_by_move(computer_move, window_width, window_height)
                                    if x != -1 and y != -1:
                                        index, res = draw_circle(win, x, y, 50, board, window_width, window_height)
                                        if res and board.check_full_board() or board.check_winning() != 'e':
                                            game_mode = 1
                                            winner = board.check_winning()
                                            print("ended")
                                    else:
                                        res = False
                                        print("AN ERROR HAS OCCURRED !!!")
                elif game_mode == 1:
                    if winner == 'o':
                        add_text(win, "The computer won", (int(window_width / 2), int(window_height / 8)), 50)
                    elif winner == 'e':
                        add_text(win, "Tie !", (int(window_width / 2), int(window_height / 8)), 50)
            else:
                if game_mode == 0:
                    winner = board.check_winning()
                    if board.check_full_board() or winner != 'e':
                        game_mode = 1
                        add_text(win, f"The winner is {winner}",
                                 (int(window_width / 2), int(window_height / 8)), 50)
                    if not current_turn:
                        print(f"{my_turn}: waiting for the other opponent")
                        if not opponent_wait_thread.is_alive():
                            opponent_wait_thread = threading.Thread(target=wait_for_move)
                            opponent_wait_thread.start()
                        if opponent_move != "" and opponent_move not in taken_squares:
                            print(f"displaying the opponent's move: {opponent_move}")
                            x, y = get_coordinates_by_move(opponent_move, window_width, window_height)
                            if my_turn == 'x':
                                index, res = draw_circle(win, x, y, 50, board, window_width, window_height)
                            else:
                                index, res = draw_x(win, x, y, board, window_width, window_height)
                            taken_squares.append(opponent_move)
                            current_turn = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if current_turn:
                            print("going for my turn!")
                            if my_turn == 'x':
                                index, res = draw_x(win, x, y, board, window_width, window_height)
                            elif my_turn == 'o':
                                index, res = draw_circle(win, x, y, 50, board, window_width, window_height)
                            else:
                                print(f"Bug! My turn is {my_turn}")
                            if res:
                                print("sending")
                                CLIENT_SOCKET.send(f"ticmove{index}".encode())
                                current_turn = False

                else:
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            running = False

            for btn in btns:
                btn.draw()
                btn.listen(events)
        clock.tick(REFRESH_RATE)
        pygame.display.flip()
    global mode  # change the game mode back to initial
    mode = 0
    tic_tac_toe_difficulty()


def initial_gui():
    global current_user
    pygame.init()
    pygame.mixer.init()
    page = GuiPage(title="Options", width=800, height=800, hex_color=gui_background, theme="theme.json")
    page.add_button(y=page.get_height() / 4.5, width=150, height=75, text="Settings", object_id="gui_button",
                    centered=True)
    page.add_button(y=page.get_height() / 2.6, width=150, height=75, text="Play", object_id="gui_button", centered=True)
    page.add_button(y=page.get_height() / 1.8, width=150, height=75, text="Other Games", object_id="gui_button",
                    centered=True)
    page.add_button(x=page.get_width() * 0.8, y=page.get_height() * 0.8, width=100, height=50, text="Exit",
                    object_id="gui_button")
    if current_user is not None:
        page.add_text_box(x=50, y=50, x1=150, y1=75, text=f'Welcome, <b>{current_user["_User__user_name"]}</b>')
        page.add_label(x=250, y=55, x1=70, y1=45, text=f'{current_user["_User__cash"]}$')
        page.add_button(page.get_width() * 0.8 + 20, page.get_height() / 15, 100, 50, "Logout")
    else:
        page.add_text_box(x=50, y=50, x1=150, y1=75, text=f'Welcome, <b>Guest</b>')
        page.add_button(page.get_width() * 0.8 + 20, page.get_height() / 15, 100, 50, "Register",
                        object_id="gui_button")
        page.add_button(page.get_width() * 0.8 + 20, page.get_height() / 15 + 60, 100, 50, "Login",
                        object_id="gui_button")
    text = r"""<body> Welcome! By pressing <b>PLAY</b> you will be directed to the trivia game.</br> We do recommend"""
    text += """ checking our other small games.</br> Have fun !</body> """
    # speak(text) # FIND A WAY TO SPEAK THIS IN A PARALLEL WAY

    main_text_box = page.add_text_box(page.get_width() / 10, page.get_height() / 4, 200, 200, text)
    for text_box in page.textboxes:
        page.animate_text_box(text_box, "typing")
    running = True
    next_loop = 0
    while running:
        time_delta = page.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    button = event.ui_element
                    if button.text == "Settings":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = 0
                    elif button.text == "Play":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = 1
                    elif button.text == "Other Games":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = 2
                    elif button.text == "Register":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = 3
                    elif button.text == "Login":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = 4
                    elif button.text == "Logout":
                        print(f"sending {json.dumps(current_user)}")
                        CLIENT_SOCKET.send(f"logout{json.dumps(current_user)}".encode('utf-8'))
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = 5
                        current_user = None
                    elif button.text == "Exit":
                        disconnect()
                        running = False
                        next_loop = -1

            if event.type == pygame.VIDEORESIZE:
                pass

            page.manager.process_events(event)
        page.manager.update(time_delta)
        page.get_window().blit(page.background, (0, 0))
        page.manager.draw_ui(page.get_window())
        pygame.display.update()
    if next_loop == -1:
        pygame.quit()
    elif next_loop == 0:
        settings_gui()
    elif next_loop == 1:
        run_main_loop()
    elif next_loop == 2:
        games_gui()
    elif next_loop == 3:
        register_gui()
    elif next_loop == 4:
        login_gui()
    elif next_loop == 5:
        initial_gui()  # refresh


def games_gui():
    global seconds, game_finished
    pygame.init()
    pygame.mixer.init()
    page = GuiPage(title="Games", width=800, height=800, hex_color=gui_background, theme="theme.json")
    page.add_button(y=page.get_height() / 4.5, text="Tic Tac Toe", centered=True)
    page.add_button(page.get_width() / 2 - 75, page.get_height() / 2.6, 150, 75, "Painter")
    page.add_button(page.get_width() / 2 - 75, page.get_height() / 1.8, 150, 75, "Shooting Range")
    page.add_button(x=page.get_window().get_width() - 250, y=page.get_window().get_height() - 150, width=150, height=75,
                    text="Back")
    running = True
    next_loop = 0
    while running:
        time_delta = page.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    button = event.ui_element
                    if button.text == "Tic Tac Toe":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = 0
                    elif button.text == "Painter":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = 1
                    elif button.text == "Shooting Range":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = 2
                    elif button.text == "Back":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = -1
            if event.type == pygame.VIDEORESIZE:
                pass

            page.manager.process_events(event)
        page.manager.update(time_delta)
        page.get_window().blit(page.background, (0, 0))
        page.manager.draw_ui(page.get_window())
        pygame.display.update()
    if next_loop == -1:
        print("going to the initial loop")
        initial_gui()
    elif next_loop == 0:
        tic_tac_toe_difficulty()
    elif next_loop == 1:
        run_painter()
        games_gui()
    elif next_loop == 2:
        seconds = max_seconds
        game_finished = False
        shooting_game()


game_started = False


def wait_for_players():
    global game_started, my_multiplayer_turn
    data = CLIENT_SOCKET.recv(MAX_BYTES).decode()
    print("RECEIVED!")
    my_multiplayer_turn = data
    print(my_multiplayer_turn)
    game_started = True


def wait_for_move():
    global opponent_move
    print("waiting for opponent move ...")
    opponent_move = int(CLIENT_SOCKET.recv(MAX_BYTES).decode().strip())
    print(f"Opponent:{opponent_move}")


def run_waiting_room():
    global game_started
    print("sending messages to the server...")
    CLIENT_SOCKET.send("<tictac>".encode())
    waiting_thread = threading.Thread(target=wait_for_players)
    waiting_thread.start()
    print("setting up waiting room... ")
    pygame.init()
    pygame.mixer.init()
    page = GuiPage(title="Games", width=800, height=800, hex_color=gui_background, theme="theme.json")
    page.add_label(y=50, x1=150, y1=50, text="Waiting..", centered=True)
    next_loop = 0
    while not game_started:
        time_delta = page.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_started = True

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    button = event.ui_element

            if event.type == pygame.VIDEORESIZE:
                pass

            page.manager.process_events(event)
        page.manager.update(time_delta)
        page.get_window().blit(page.background, (0, 0))
        page.manager.draw_ui(page.get_window())
        pygame.display.update()
    print("The game should start now!")
    tic_tac_toe(multiplayer=True, my_turn=my_multiplayer_turn)


def tic_tac_toe_difficulty():
    pygame.init()
    pygame.mixer.init()
    page = GuiPage(title="Games", width=800, height=800, hex_color=gui_background, theme="theme.json")
    page.add_button(y=page.get_height() / 4.5, text="Go Easy On Me", centered=True)
    page.add_button(page.get_width() / 2 - 75, page.get_height() / 2.6, 150, 75, "Play Casual")
    page.add_button(page.get_width() / 2 - 75, page.get_height() / 1.8, 150, 75, "Multiplayer")
    page.add_button(x=page.get_window().get_width() - 250, y=page.get_window().get_height() - 150, width=150, height=75,
                    text="Back")
    running = True
    next_loop = 0
    difficulty = "easy"
    while running:
        time_delta = page.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    button = event.ui_element
                    if button.text == "Go Easy On Me":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = 0
                    elif button.text == "Play Casual":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = 1
                        difficulty = "medium"
                    elif button.text == "Multiplayer":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = 2
                    elif button.text == "Back":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = -1
            if event.type == pygame.VIDEORESIZE:
                pass

            page.manager.process_events(event)
        page.manager.update(time_delta)
        page.get_window().blit(page.background, (0, 0))
        page.manager.draw_ui(page.get_window())
        pygame.display.update()
    if next_loop == -1:
        games_gui()
    elif next_loop == 0 or next_loop == 1:
        tic_tac_toe(difficulty=difficulty, my_turn='x')
    elif next_loop == 2:
        print("next loop is 2")
        run_waiting_room()


def settings_gui():
    global gui_background
    global sound_on
    global music_on
    pygame.init()
    pygame.mixer.init()
    page = GuiPage(title="Games", width=800, height=800, hex_color=gui_background, theme="theme.json")
    page.add_button(y=page.get_height() / 4.5, width=200, height=75, text="Change Background", centered=True)
    page.add_button(y=page.get_height() / 1.8, width=200, height=75, text="Music:ON", centered=True)
    page.add_button(x=page.get_window().get_width() - 250, y=page.get_window().get_height() - 150, width=150, height=75,
                    text="Back")
    running = True
    next_loop = 0
    color_picker = page.add_color_picker(visible=False)
    while running:
        time_delta = page.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    button = event.ui_element
                    if button.text == "Change Background":
                        color_picker = page.add_color_picker()
                        SECOND_BUTTON_CLICK.play()
                    elif button.text == "Music:ON":
                        SECOND_BUTTON_CLICK.play()
                        music_on = False
                        button.text = "Music:OFF"
                        button.rebuild()
                        pass
                    elif button.text == "Music:OFF":
                        SECOND_BUTTON_CLICK.play()
                        music_on = True
                        button.text = "Music:ON"
                        button.rebuild()
                    elif button.text == "Back":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = -1
                elif event.user_type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                    if event.ui_element == color_picker:
                        SECOND_BUTTON_CLICK.play()
                        page.background.fill(pygame.Color(event.colour))
                        gui_background = event.colour
            if event.type == pygame.VIDEORESIZE:
                pass

            page.manager.process_events(event)
        page.manager.update(time_delta)
        page.get_window().blit(page.background, (0, 0))
        page.manager.draw_ui(page.get_window())
        pygame.display.update()

    if next_loop == -1:
        initial_gui()
    elif next_loop == 0:
        pass
    elif next_loop == 1:
        pass  # Not implemented yet ..


def register_gui():
    global gui_background
    pygame.init()
    pygame.mixer.init()
    page = GuiPage(title="Register", width=800, height=800, hex_color=gui_background, theme="theme.json")
    page.add_button(x=page.get_width() / 3, y=page.get_height() * 0.8, width=200, height=75, text="Submit")
    page.add_button(x=page.get_window().get_width() - 250, y=page.get_window().get_height() * 0.8, width=150, height=75,
                    text="Back")
    page.add_label(x=page.get_width() * 0.6, y=page.get_height() * 0.7, x1=200, y1=40, text="Password Strength:0.00%")
    label_text = ["UserName:", "E-mail:", "Password:"]
    i = 0
    for y in range(int(page.get_height() * 0.2), int(page.get_height() * 0.5), int(page.get_height() * 0.1)):
        page.add_entry_box(x=page.get_width() / 3, y=y, width=250)
        page.add_label(x=page.get_width() / 15, y=y - 6, x1=125, y1=40, text=label_text[i], object_id="normal_label")
        i += 1
    running = True
    next_loop = 0
    password_strength = 0
    while running:
        time_delta = page.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    button = event.ui_element
                    if button.text == "Submit":
                        valid_user_name = Form.valid_user_name(page.entry_boxes[0].text)
                        valid_email = Form.valid_email(page.entry_boxes[1].text)
                        password_violations = Form.valid_password(page.entry_boxes[2].text)
                        password_strength = Form.evaluate_password_strength(page.entry_boxes[2].text)
                        print(f"password strength : {password_strength}")
                        if not valid_email:
                            page.add_popup(x=400, y=400, html_message="Invalid E-mail Address", title="Invalid E-mail",
                                           centered_x=True
                                           , centered_y=True)
                        elif len(password_violations) > 0 or password_strength < 0.2:
                            if str(password_violations[0]).startswith('Length'):
                                html_message = "The password should contain at least <b>8</b> characters."
                            elif str(password_violations[0]).startswith('Upper'):
                                html_message = "The password should contain at least <b>1</b> capital letter."
                            elif str(password_violations[0]).startswith('Number'):
                                html_message = "The password should contain at least <b>1</b> number."
                            elif password_strength < 0.2:
                                html_message = "Your password is too <b>weak</b>!<br/> Try adding more characters and " \
                                               "special characters. "
                            else:
                                html_message = "Password not valid: Unknown Error"

                            page.add_popup(x=400, y=400, html_message=html_message, title="Invalid Password",
                                           centered_x=True
                                           , centered_y=True)

                        elif not valid_user_name:
                            if not valid_email:
                                page.add_popup(x=400, y=400, html_message="Invalid UserName",
                                               title="Your user name is invalid!",
                                               centered_x=True
                                               , centered_y=True)
                        else:
                            print("first validation passed successfully!")
                            user = User(user_name=page.entry_boxes[0].text, email=page.entry_boxes[1].text,
                                        password=page.entry_boxes[2].text)
                            # print(json.dumps(user.__dict__))
                            print(f"user dict is {user.__dict__}")
                            CLIENT_SOCKET.send(f'user{json.dumps(user.__dict__, indent=4)}'.encode('utf-8'))
                            response_from_server = CLIENT_SOCKET.recv(MAX_BYTES).decode('utf-8').strip()
                            if response_from_server == "0":
                                print("registration was successful!")
                            elif response_from_server == '1':
                                print("user name was taken")
                            elif response_from_server == "2":
                                print("email was taken")
                            elif response_from_server == "3":
                                print("password was taken")
                            print("sent user to server !")

                        SECOND_BUTTON_CLICK.play()
                    elif button.text == "Back":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = -1
                elif event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_element is page.entry_boxes[2]:
                    password_strength = round(Form.evaluate_password_strength(page.entry_boxes[2].text) * 100, 2)
                    print(f"password strength : {password_strength}")
                    page.labels[0].set_text(f"Password Strength:{password_strength}%")
                elif event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    print("finished")
            if event.type == pygame.VIDEORESIZE:
                pass

            page.manager.process_events(event)
        page.manager.update(time_delta)
        page.get_window().blit(page.background, (0, 0))
        page.manager.draw_ui(page.get_window())
        pygame.display.update()

    if next_loop == -1:
        initial_gui()
    elif next_loop == 0:
        pass
    elif next_loop == 1:
        pass  # Not implemented yet ..


def login_gui():
    global gui_background, current_user
    pygame.init()
    pygame.mixer.init()
    page = GuiPage(title="Login", width=800, height=800, hex_color=gui_background, theme="theme.json")
    page.add_button(x=page.get_width() / 3, y=page.get_height() * 0.8, width=200, height=75, text="Login")
    page.add_button(x=page.get_window().get_width() - 250, y=page.get_window().get_height() * 0.8, width=150, height=75,
                    text="Back")
    label_text = ["E-mail:", "Password:"]
    i = 0
    for y in range(int(page.get_height() * 0.2), int(page.get_height() * 0.4), int(page.get_height() * 0.1)):
        page.add_entry_box(x=page.get_width() / 3, y=y, width=250, height=100)
        page.add_label(x=page.get_width() / 15, y=y - 6, x1=125, y1=45, text=label_text[i], object_id="normal_label")
        i += 1
    running = True
    next_loop = 0
    while running:
        time_delta = page.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    button = event.ui_element
                    if button.text == "Login":
                        SECOND_BUTTON_CLICK.play()
                        CLIENT_SOCKET.send(
                            f"verify[{page.entry_boxes[0].text, page.entry_boxes[1].text}]".encode('utf-8'))
                        # Send the server a verification request
                        response = CLIENT_SOCKET.recv(MAX_BYTES).decode('utf-8')
                        if response.strip() == '0':
                            page.add_popup(x=400, y=400, html_message="Login Failed!", title="Oops...", centered_x=True
                                           , centered_y=True)

                        elif response.strip() == '1':
                            print("the user is already online")
                        else:  # Here the server will send the json object representing the user.
                            print(f'response is {response}')
                            current_user = json.loads(response)
                            running = False
                            next_loop = -1  # going back to the initial loop
                    elif button.text == "Back":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = -1

            if event.type == pygame.VIDEORESIZE:
                pass

            page.manager.process_events(event)
        page.manager.update(time_delta)
        page.get_window().blit(page.background, (0, 0))
        page.manager.draw_ui(page.get_window())
        pygame.display.update()

    if next_loop == -1:
        initial_gui()
    elif next_loop == 0:
        pass
    elif next_loop == 1:
        pass  # Not implemented yet ..


def shooting_game():
    global targets, targets_hit, total_targets, game_finished, aim_mode, seconds, current_grenades, current_weapon_index
    global weapons, full_ammo
    weapons[0] = sniper
    if current_user is not None:
        if 1 in current_user['_User__guns']:
            weapons[1] = rifle
        if 2 in current_user['_User__guns']:
            weapons[2] = shotgun
        for i in range(len(current_user['_User__max_ammo'])):
            full_ammo[i] = current_user['_User__max_ammo'][i]
    pygame.init()
    targets = []
    page = GuiPage(width=WIDTH, height=HEIGHT, title="Shooting Range", hex_color=background_color, theme='theme.json')
    page.get_window().blit(page.background, (0, 0))
    window = page.get_window()
    score = 0
    score_label = page.add_label(x=30, y=30, text="Score:0", object_id="score")
    success_rate = page.add_label(x=200, y=30, text="Success:100.0%")
    timer_label = page.add_label(x=370, y=30, text="")
    update_timer(timer_label)
    current_weapon = page.add_image(path=weapons[current_weapon_index].get_image_path(), x=40, y=600,
                                    size_factor=weapons[current_weapon_index].get_size_factor())
    grenade = page.add_image(path="grenade.png", x=800, y=600, size_factor=0.22)
    grenade_label = page.add_label(x=800, y=720, text=f"{current_grenades}/{max_grenades}", object_id="grenade")
    ammo_label = page.add_label(x=100, y=720, text=f"{weapons[current_weapon_index].get_current_ammo()}/"
                                                   f"{weapons[current_weapon_index].get_ammo()}", object_id="ammo")
    store_button = page.add_button(x=600, y=30, text="Store", object_id="gui_button")
    #  exit_button = page.add_button(x=600, y=600, text="EXIT")
    running = True
    pygame.time.set_timer(pygame.USEREVENT + 1, creation_frequency)  # creating new targets
    pygame.time.set_timer(pygame.USEREVENT + 2, 1000)  # timer
    play_music("game_analysis.mp3")
    pygame.mixer.music.set_volume(0.4)
    while running:
        time_delta = page.clock.tick(100) / 1000.0
        mouse_x, mouse_y = pygame.mouse.get_pos()
        page.get_window().blit(page.background, (0, 0))
        if not game_finished:
            draw_aim(window=window, mouse_x=mouse_x, mouse_y=mouse_y, length=aim_size, gun_mode=current_weapon_index)
            for index, target in enumerate(targets):
                if total_targets != 0:  # prevent division by 0 in any case whatsoever
                    success_rate.set_text(f"Success:{round(targets_hit / total_targets * 100, 2)}%")
                mouse_x, mouse_y = pygame.mouse.get_pos()
                collision = target.rect.colliderect(
                    pygame.rect.Rect(mouse_x - 25, mouse_y - 25, mouse_x + 25, mouse_y + 25))
                if -target.image.get_width() < target.x < window.get_width() and 0 < target.y < window.get_height():
                    target.draw(window)
                    target.move(target.velocity)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_finished = True
                    finishing_screen(page, score)

                if event.type == pygame.MOUSEMOTION:
                    draw_aim(window=window, mouse_x=mouse_x, mouse_y=mouse_y, length=aim_size,
                             gun_mode=current_weapon_index)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]:
                    print("detected right key press")
                    if current_weapon_index == len(weapons) - 1:
                        if weapons[0] is not None:
                            current_weapon_index = 0
                            update_ammo(ammo_label)
                            current_weapon = update_weapon_image(page, current_weapon)

                    else:
                        if weapons[current_weapon_index + 1] is not None:
                            current_weapon_index += 1
                            update_ammo(ammo_label)
                            current_weapon = update_weapon_image(page, current_weapon)
                elif keys[pygame.K_LEFT]:
                    print("detected left key press")

                    if current_weapon_index == 0:
                        if weapons[len(weapons) - 1] is None:
                            if weapons[len(weapons) - 2] is not None:
                                current_weapon_index = len(weapons) - 2
                            else:
                                current_weapon_index = 0
                        else:
                            current_weapon_index = len(weapons) - 1
                        update_ammo(ammo_label)
                        current_weapon = update_weapon_image(page, current_weapon)
                    else:
                        if weapons[current_weapon_index - 1] is None:
                            current_weapon_index = 0
                        else:
                            current_weapon_index -= 1
                            update_ammo(ammo_label)
                            current_weapon = update_weapon_image(page, current_weapon)

                elif keys[pygame.K_g]:
                    print("GRENADE INCOMING")
                    score += 5 * len(targets)
                    score_label.set_text(f"Score:{score}")
                    targets = []
                    current_grenades -= 1
                    update_grenade_label(grenade_label)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if current_weapon_index == 0 and weapons[0].get_current_ammo() > 0:
                        print("playing sniper sound ")
                        weapons[current_weapon_index].decrease_ammo(1)
                        update_ammo(ammo_label)
                        SNIPER_SHOT.play()
                    elif current_weapon_index == 1 and weapons[1].get_current_ammo() > 2:
                        weapons[1].decrease_ammo(3)
                        update_ammo(ammo_label)
                        gun_thread = threading.Thread(target=gun_sound)
                        gun_thread.start()

                    elif current_weapon_index == 2 and weapons[current_weapon_index].get_current_ammo() > 0:
                        weapons[2].decrease_ammo(1)
                        print(weapons[2].get_current_ammo())
                        update_ammo(ammo_label)
                        SHOTGUN_SHOT.play()

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for index, target in enumerate(targets):
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        collision = target.rect.colliderect(
                            pygame.rect.Rect(mouse_x - 25, mouse_y - 25, mouse_x + 25, mouse_y + 25))
                        if collision and weapons[current_weapon_index].get_current_ammo() > 0:
                            targets_hit += 1
                            score += 5
                            update_label_text(score_label, f"Score:{score}")
                            targets.pop(index)
                            print("destroyed an object !")
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        button = event.ui_element
                        if button.text == "Store":
                            pygame.mixer.music.pause()
                            page.clear_all()
                            store_gui()
                elif event.type == pygame.USEREVENT + 1:
                    print("adding a new target")
                    if not game_finished:
                        targets.append(
                            Target(x=random.randint(int(window.get_width() * 0.2), int(window.get_width() * 0.7)),
                                   y=random.randint(int(window.get_height() * 0.2), int(window.get_height() * 0.7))
                                   , size_factor=random.uniform(0.1, 0.3),
                                   velocity=
                                   random.randint(-4, 4)))
                        total_targets += 1
                elif event.type == pygame.USEREVENT + 2:
                    if seconds == 0:
                        game_finished = True
                        finishing_screen(page, score)
                    else:
                        seconds -= 1
                        update_timer(timer_label)
                page.manager.process_events(event)
        else:
            page.refresh()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()  # Or move to another loop.
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        button = event.ui_element
                        if button.text == "Back":
                            running = False
                            games_gui()
                page.manager.process_events(event)

        page.manager.update(time_delta)
        # page.get_window().blit(page.background, (0, 0))
        page.manager.draw_ui(page.get_window())
        pygame.display.update()


def add_gun_to_user(gun_index):
    """adds a gun to a user, then updates the users json file, and returns the updated user, so it'll be sent back
    to the client """
    if current_user is not None:
        if gun_index not in current_user["_User__guns"]:
            bisect.insort(current_user["_User__guns"], gun_index)


def store_gui():
    """The Store Gui- Here a registered user can buy things such as new guns and extra hearts and clues in trivia"""
    pygame.init()
    pygame.mixer.init()
    page = GuiPage(title="Games", width=WIDTH, height=HEIGHT, hex_color=background_color, theme="theme.json")
    page.add_label(y=50, text="Store", x1=300, centered=True, object_id="rating_title")
    page.add_image(path="sniper.png", x=40, y=150, size_factor=scales[0])
    page.add_image(path="rifle.png", x=40, y=350, size_factor=scales[1])
    page.add_image(path="shotgun.png", x=40, y=550, size_factor=scales[2])
    buying_prices = [40, 60, 50]
    i = 0
    if current_user is None:  # in a case a guest has entered.
        for y in range(150, 551, 200):
            page.add_button(y=y + 40, text=f"{buying_prices[i]}$", object_id="gui_button", centered=True)
            i += 1
    else:
        i = 0
        guns = ["sniper", "rifle", "shotgun"]
        for y in range(150, 551, 200):
            if i in current_user["_User__guns"]:
                page.add_button(y=y + 40, width=250, text=f"Maximize {guns[i]} ammo", object_id="gui_button",
                                centered=True)
            else:
                page.add_button(y=y + 40, text=f"{buying_prices[i]}$", object_id="gui_button", centered=True)
            i += 1
    running = True
    next_loop = 0
    while running:
        time_delta = page.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                next_loop = -1
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    button = event.ui_element
                    if button.text == "Back":
                        SECOND_BUTTON_CLICK.play()
                        running = False
                        next_loop = -1
                    for i in range(len(buying_prices)):
                        if button.text == f"{buying_prices[i]}$":
                            print("buying this weapon")
                            if current_user is None:
                                page.add_popup(html_message="Login to purchase items at the store", title="Login",
                                               centered_x=True, centered_y=True)
                            elif current_user['_User__cash'] < buying_prices[i]:
                                page.add_popup(
                                    html_message=f"Acquire more {buying_prices[i] - current_user['_User__cash']}$"
                                                 f"to purchase this item", title="Login", centered_x=True,
                                    centered_y=True)
                            else:
                                # BUYING A NEW SHOTGUN
                                add_gun_to_user(i)
                                current_user['_User__cash'] -= buying_prices[i]
                                CLIENT_SOCKET.send(f"replace{json.dumps(current_user)}".encode())
                                page.add_popup(
                                    html_message=f"<b>{buying_prices[i]}$</b> was withdrawn from your account"
                                    , title="Transaction Successful!", centered_x=True, centered_y=True)
                                button.set_text("Buy Ammo!")
                        elif button.text == "Maximize sniper ammo":
                            if weapons[0].get_current_ammo() == full_ammo[0]:
                                page.add_popup(
                                    html_message=f"The sniper is fully loaded"
                                    , title="Full!", centered_x=True, centered_y=True)
                            else:
                                weapons[0].set_current_ammo(full_ammo[0])
                                current_user['_User__cash'] -= 25
                                CLIENT_SOCKET.send(f"replace{json.dumps(current_user)}".encode())
                                button.set_text("Full Ammo!")
                                page.add_popup(
                                    html_message=f"<b>25$</b> was withdrawn from your account"
                                    , title="Transaction Successful!", centered_x=True, centered_y=True)
                        elif button.text == "Maximize rifle ammo":
                            if weapons[1].get_current_ammo() == full_ammo[1]:
                                page.add_popup(
                                    html_message=f"The rifle is fully loaded"
                                    , title="Full!", centered_x=True, centered_y=True)
                            else:
                                weapons[1].set_current_ammo(full_ammo[1])
                                current_user['_User__cash'] -= 25
                                CLIENT_SOCKET.send(f"replace{json.dumps(current_user)}".encode())
                                button.set_text("Full Ammo!")
                                page.add_popup(
                                    html_message=f"<b>25$</b> was withdrawn from your account"
                                    , title="Transaction Successful!", centered_x=True, centered_y=True)
                        elif button.text == "Maximize shotgun ammo":
                            if weapons[2].get_current_ammo() == full_ammo[2]:
                                page.add_popup(
                                    html_message=f"The shotgun is fully loaded"
                                    , title="Full!", centered_x=True, centered_y=True)
                            else:
                                weapons[2].set_current_ammo(full_ammo[2])
                                current_user['_User__cash'] -= 25
                                CLIENT_SOCKET.send(f"replace{json.dumps(current_user)}".encode())
                                button.set_text("Full Ammo!")
                                page.add_popup(
                                    html_message=f"<b>25$</b> was withdrawn from your account"
                                    , title="Transaction Successful!", centered_x=True, centered_y=True)

            if event.type == pygame.VIDEORESIZE:
                pass

            page.manager.process_events(event)
        page.manager.update(time_delta)
        page.get_window().blit(page.background, (0, 0))
        page.manager.draw_ui(page.get_window())
        pygame.display.update()
    if next_loop == -1:
        shooting_game()
    elif next_loop == 0 or next_loop == 1:
        pass
    elif next_loop == 2:
        pass


def main():
    initial_gui()
    # initial_loop()
    print("got here")


if __name__ == '__main__':
    main()
