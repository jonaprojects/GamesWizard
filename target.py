import pygame

TARGET_IMAGE = pygame.image.load("target.png")


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
