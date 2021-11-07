import socket
import pygame
import pygame_widgets as pw
import pygame_gui
import gui_page
import TriviaClient
# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
# COLORS
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (127, 0, 255)
ORANGE = (255, 128, 0)
BACKGROUND = WHITE  # in order to change it sometimes
CURRENT_X = 0
CURRENT_Y = 0
CURRENT_COLOR = BLACK
# CLOCK RELATED CONSTANTS
# OTHERS
RADIUS = 8


def change_color(color):
    global CURRENT_COLOR
    CURRENT_COLOR = color


def create_buttons(screen):
    black_button = pw.Button(
        screen, 0, 50, 40, 40, text='',
        fontSize=30, margin=10,
        inactiveColour=BLACK,
        pressedColour=(255, 255, 255), radius=0,
        onClick=lambda: change_color(BLACK)
    )
    red_button = pw.Button(
        screen, 0, 100, 40, 40, text='',
        fontSize=30, margin=10,
        inactiveColour=RED,
        pressedColour=(255, 255, 255), radius=0,
        onClick=lambda: change_color(RED)
    )
    orange_button = pw.Button(
        screen, 0, 150, 40, 40, text='',
        fontSize=30, margin=10,
        inactiveColour=ORANGE,
        pressedColour=(255, 255, 255), radius=0,
        onClick=lambda: change_color(ORANGE)
    )
    green_button = pw.Button(
        screen, 0, 200, 40, 40, text='',
        fontSize=30, margin=10,
        inactiveColour=GREEN,
        pressedColour=(255, 255, 255), radius=0,
        onClick=lambda: change_color(GREEN)
    )
    yellow_button = pw.Button(
        screen, 0, 250, 40, 40, text='',
        fontSize=30, margin=10,
        inactiveColour=YELLOW,
        pressedColour=(255, 255, 255), radius=0,
        onClick=lambda: change_color(YELLOW))
    blue_button = pw.Button(
        screen, 0, 300, 40, 40, text='',
        fontSize=30, margin=10,
        inactiveColour=BLUE,
        pressedColour=(255, 255, 255), radius=0,
        onClick=lambda: change_color(BLUE))
    purple_button = pw.Button(
        screen, 0, 350, 40, 40, text='',
        fontSize=30, margin=10,
        inactiveColour=(127, 0, 255),
        pressedColour=(255, 255, 255), radius=0,
        onClick=lambda: change_color(PURPLE))
    return [black_button, red_button, orange_button, green_button, yellow_button, blue_button, purple_button]


def run_painter():
    """Displays a pygame window"""
    global CURRENT_X
    global CURRENT_Y
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    pygame.init()
    size = WINDOW_WIDTH, WINDOW_HEIGHT
    page = gui_page.GuiPage(title="Painter", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, hex_color="#FFFFFF", theme=None)
    page.add_button(x=WINDOW_WIDTH*0.85,y=WINDOW_HEIGHT*0.85,width=WINDOW_WIDTH/10,height=WINDOW_HEIGHT/15,text="Back")
    page.get_window().blit(page.background, (0, 0))
    screen = page.get_window()
    pygame.display.flip()
    buttons = create_buttons(screen)
    running = True
    isPressed = False
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
            elif event.type == pygame.MOUSEMOTION and isPressed:
                CURRENT_X, CURRENT_Y = pygame.mouse.get_pos()
                if 90 < CURRENT_X < WINDOW_WIDTH * 0.95 and 0.05*WINDOW_HEIGHT< CURRENT_Y < WINDOW_HEIGHT * 0.9:
                    pygame.draw.circle(screen, CURRENT_COLOR, [CURRENT_X, CURRENT_Y], RADIUS)
                    print(CURRENT_X, CURRENT_Y)
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    button = event.ui_element
                    if button.text == "Back":
                        TriviaClient.games_gui()
            page.manager.process_events(event)
        for button in buttons:
            button.listen(events)
            button.draw()

        page.manager.update(0)
        page.manager.draw_ui(page.get_window())
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    run_painter()
