import pygame
import pygame_gui

WIDTH = 800
HEIGHT = 600


class TestSprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.health_capacity = 100
        self.current_health = 95
        self.rect = pygame.Rect(0, 0, 50, 75)


pygame.init()
pygame.display.set_caption('title')
window_surface = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#13C2AA'))
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH / 2 - 50, HEIGHT / 4), (150, 75)),
                                               text="Settings",
                                               manager=manager)
play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH / 2 - 50, HEIGHT / 8 * 3.5), (150, 75)),
                                           text='Play',
                                           manager=manager)
other_games = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH / 2 - 50, HEIGHT / 8 * 5), (150, 75)),
                                           text='Other Games',
                                           manager=manager)
test_sprite = TestSprite()
pygame_gui.elements.UIWorldSpaceHealthBar(relative_rect=pygame.Rect((350, 280), (150, 35)),
                                          sprite_to_monitor=test_sprite,
                                          manager=manager)
color_picker = pygame_gui.windows.UIColourPickerDialog(rect=pygame.Rect(100, 100, 390, 390),
                                                       manager=manager, visible=True)
slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((150, 280), (250, 40)),
                                                start_value=50,
                                                value_range=(0, 100),
                                                manager=manager)
textBox = pygame_gui.elements.UITextBox(
    html_text=f"{slider.get_current_value()}.This is a trivia game and this is a <a href='none'>link</a>",
    relative_rect=pygame.Rect((50, 150), (200, 150)),
    manager=manager)
textEntry = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((200, 200), (150, 75)),
                                                                   manager=manager)
# pygame_gui.elements.UIWorldSpaceHealthBar(relative_rect=pygame.Rect((350, 280), (150, 35)),
#                                           sprite_to_monitor=test_sprite,
#                                           manager=manager)
option_list = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=["First", "Second", "Third"],
                                                                   starting_option="First",
                                                                   relative_rect=pygame.Rect((400, 400), (150, 60)),
                                                                   manager=manager)
horizontal_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(relative_rect=pygame.Rect((200, 200),
                                                                                                          (100, 100)),
                                                                                start_value=50, value_range=(0, 100),
                                                                                manager=manager)
img = pygame.image.load("heart.png")
img = pygame.transform.scale(img, (int(img.get_width() / 10), int(img.get_height() / 10)))
image = pygame_gui.elements.ui_image.UIImage(relative_rect=pygame.Rect((100, 100), (img.get_width(), img.get_height())),
                                             image_surface=img, manager=manager,visible=True)
clock = pygame.time.Clock()
is_running = True
textBox.set_active_effect('typing_appear')
while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == settings_button:
                    print('went into settings')

        if event.type == pygame.VIDEORESIZE:
            pass
        test_sprite.current_health -= 1

        manager.process_events(event)
    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
