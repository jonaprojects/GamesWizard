import bisect


class User:
    def __init__(self, user_name, email, password, cash=0, has_premium=False, guns=None, grenades=0, extra_hearts=0):
        self.__user_name = user_name
        self.__email = email
        self.__password = password
        self.__cash = cash
        self.__has_premium = has_premium
        self.__guns = [0] if guns is None else guns
        self.__max_ammo = [40, 60, 35]
        self.__grenades = grenades
        self.__extra_hearts = extra_hearts

    # GETTERS METHODS
    def get_user_name(self):
        return self.__user_name

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_cash(self):
        return self.__cash

    def get_guns(self):
        return self.__guns

    def get_max_ammo(self):
        return self.__max_ammo

    def has_premium(self):
        return self.__has_premium

    # SETTERS METHODS

    def set_user_name(self, user_name):
        self.__user_name = user_name

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def add_gun(self, gun_index):
        bisect.insort(self.__guns, gun_index)  # add sorted

    def set_cash(self, cash):
        self.__cash = cash

    def set_has_premium(self, has_premium):
        self.__has_premium = has_premium

    # OTHER METHODS

    def __str__(self):
        pass

    def __repr__(self):
        pass
