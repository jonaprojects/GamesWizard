import pygame
import pygame_gui
from gui_page import GuiPage
import time
import threading
import random

pygame.mixer.init()
# GLOBAL VARIABLES
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
seconds = 50
full_ammo = [40, 60, 35]
ammo = [40, 60, 35]
images = ["sniper.png", "rifle.png", "shotgun.png"]
scales = [0.7, 0.6, 0.6]
max_grenades = 3
current_grenades = 1


class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, size_factor=0.25, velocity=2):
        super().__init__()
        self.x = x
        self.y = y
        self.velocity = velocity
        self.image = pygame.transform.scale(
            TARGET_IMAGE, (int(TARGET_IMAGE.get_width() * size_factor), int(TARGET_IMAGE.get_height() * size_factor)))
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, velocity):
        self.x += velocity
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def __str__(self):
        return f'x:{self.x},y:{self.y},velocity:{self.velocity}'


def play_music(music):  # ALREADY IN CLIENT
    """ playing music using pygame's mixer ( not the same as playing sounds ) """
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()


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


def finishing_screen(page):
    pygame.mixer.music.stop()
    page.clear_labels()
    page.clear_images()
    fade(page.get_window(), WIDTH, HEIGHT)
    page.add_text_box(y=page.get_height() / 2 - 35, x1=200, y1=70, text="You finished the game !",
                      centered=True)


def update_ammo(ammo_label):
    """ Updates the label that keeps track of the ammunition """
    ammo_label.set_text(f"{ammo[aim_mode]}/{full_ammo[aim_mode]}")


def update_weapon_image(page, old_image):
    """ switches between the images of the guns """
    old_image.kill()
    return page.add_image(images[aim_mode], 40, 600, scales[aim_mode])


def update_grenade_label(grenade_label):
    """updates the number of grenades remaining"""
    grenade_label.set_text(f"{current_grenades}/{max_grenades}")


def main():
    global targets
    global targets_hit
    global total_targets
    global game_finished
    global aim_mode
    global seconds
    global current_grenades
    pygame.init()
    page = GuiPage(width=WIDTH, height=HEIGHT, title="Shooting Range", hex_color=background_color, theme='theme.json')
    page.get_window().blit(page.background, (0, 0))
    window = page.get_window()
    score = 0
    score_label = page.add_label(x=30, y=30, text="Score:0", object_id="score")
    success_rate = page.add_label(x=200, y=30, text="Success:100.0%")
    timer_label = page.add_label(x=370, y=30, text="")
    current_weapon = page.add_image(images[aim_mode], 40, 600, scales[aim_mode])
    grenade = page.add_image(path="grenade.png", x=800, y=600, size_factor=0.22)
    grenade_label = page.add_label(x=800, y=720, text=f"{current_grenades}/{max_grenades}", object_id="grenade")
    ammo_label = page.add_label(x=100, y=720, text=f"{ammo[aim_mode]}/{full_ammo[aim_mode]}", object_id="ammo")

    #  exit_button = page.add_button(x=600, y=600, text="EXIT")
    running = True
    # add_targets(window)
    # targets.append(Target(x=200, y=200))
    # targets.append(Target(x=300, y=400, velocity=-2))
    pygame.time.set_timer(pygame.USEREVENT + 1, creation_frequency)  # creating new targets
    pygame.time.set_timer(pygame.USEREVENT + 2, 1000)  # timer
    play_music("game_analysis.mp3")
    pygame.mixer.music.set_volume(0.4)
    while running:
        time_delta = page.clock.tick(100) / 1000.0
        mouse_x, mouse_y = pygame.mouse.get_pos()
        page.get_window().blit(page.background, (0, 0))
        if not game_finished:
            draw_aim(window=window, mouse_x=mouse_x, mouse_y=mouse_y, length=aim_size, gun_mode=aim_mode)
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
                    finishing_screen(page)
                    page.add_text_box(y=page.get_height() / 2 - 35, x1=200, y1=70, text="You finished the game !",
                                      centered=True)
                    page.animate_text_box(page.textboxes[0], "typing")
                if event.type == pygame.MOUSEMOTION:
                    draw_aim(window=window, mouse_x=mouse_x, mouse_y=mouse_y, length=aim_size, gun_mode=aim_mode)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]:
                    print("detected right key press")
                    if aim_mode == 2:
                        aim_mode = 0
                    else:
                        aim_mode += 1
                    update_ammo(ammo_label)
                    current_weapon = update_weapon_image(page, current_weapon)
                elif keys[pygame.K_LEFT]:
                    print("detected left key press")

                    if aim_mode == 0:
                        aim_mode = 2
                    else:
                        aim_mode -= 1
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
                    if aim_mode == 0 and ammo[aim_mode] > 0:
                        print("playing sniper sound ")
                        ammo[aim_mode] -= 1
                        update_ammo(ammo_label)
                        SNIPER_SHOT.play()
                    elif aim_mode == 1 and ammo[aim_mode] > 2:
                        ammo[aim_mode] -= 3
                        update_ammo(ammo_label)
                        gun_thread = threading.Thread(target=gun_sound)
                        gun_thread.start()

                    elif aim_mode == 2 and ammo[aim_mode] > 0:
                        ammo[aim_mode] -= 1
                        update_ammo(ammo_label)
                        SHOTGUN_SHOT.play()

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for index, target in enumerate(targets):
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        collision = target.rect.colliderect(
                            pygame.rect.Rect(mouse_x - 25, mouse_y - 25, mouse_x + 25, mouse_y + 25))
                        if collision and ammo[aim_mode] > 0:
                            targets_hit += 1
                            score += 5
                            targets.pop(index)
                            print("destroyed an object !")
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        button = event.ui_element
                        if button.text == "EXIT":
                            running = False
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
                        finishing_screen(page)
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
        page.manager.update(time_delta)
        # page.get_window().blit(page.background, (0, 0))
        page.manager.draw_ui(page.get_window())
        pygame.display.update()


if __name__ == '__main__':
    main()
