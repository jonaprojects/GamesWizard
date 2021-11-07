import json
import pygame
import os.path


def check_validation(func):
    """ decorates a function to validate whether the value is bigger than 0 and not none"""

    def decorated_function(self, value):
        if value is None or value < 0:
            print(f"Cannot assign 0 to {func.__name__}")
        else:
            return func(value)

    return decorated_function


class Weapon:
    counter = 0

    def __init__(self, name: str, image_path: str = "", image=None, size_factor=1, ammo: int = 0, current_ammo: int = 0,
                 sound_effect=None):
        self.__name = name
        self.__image_path = image_path
        if image is None and os.path.exists(image_path):
            self.__image = pygame.image.load(image_path)
        self.__size_factor = size_factor
        self.__ammo = ammo
        self.__current_ammo = current_ammo
        self.___sound_effect = sound_effect
        Weapon.counter += 1

    # Gets
    def get_name(self):
        return self.__name

    def get_image_path(self):
        return self.__image_path

    def get_size_factor(self):
        return self.__size_factor

    def get_image(self):
        return self.__image

    def get_ammo(self):
        return self.__ammo

    def get_current_ammo(self):
        return self.__current_ammo

    def get_sound_effect(self):
        return self.___sound_effect

    # Sets
    def set_name(self, name: str):
        self.__name = name

    def set_image_path(self, image_path: str):
        self.__image_path = image_path

    def set_size_factor(self, size_factor):
        self.__size_factor = size_factor

    def set_ammo(self, ammo: int):
        self.__ammo = ammo

    def set_current_ammo(self, current_ammo):
        if current_ammo >= 0:
            self.__current_ammo = current_ammo
        else:
            print("Cannot assign a negative ammo!")

    def decrease_ammo(self, value: int):
        current_ammo = self.__current_ammo - value
        self.set_current_ammo(current_ammo)

    def set_sound_effect(self, sound_effect):
        self.___sound_effect = sound_effect

    def to_json(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.to_json()

    def __del__(self):
        Weapon.counter += 1
        print("Deleting")
        del self
