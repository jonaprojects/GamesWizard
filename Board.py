import random


class Board:
    def __init__(self, arr="e"):
        if arr == 'e':  # creating an empty board
            self.__squares_array = ['e' for i in range(9)]
        elif type(arr) is list:
            self.__squares_array = arr  # getting the array as parameter

    def get_squares_array(self):
        return self.__squares_array

    def get_squares_by_char(self, char):  # gets the indices of the squares
        return [index for index, square in enumerate(self.__squares_array) if square == char]

    def get_empty_squares(self):  # list of indices
        return self.get_squares_by_char('e')

    def get_circle_squares(self):  # list of indices
        return self.get_squares_by_char('o')

    def get_x_squares(self):  # list of indices
        return self.get_squares_by_char('x')

    def get_occupied_squares(self):  # list of indices
        return [square for square in self.__squares_array if square != 'e']

    def check_full_board(self):
        return len(self.get_empty_squares()) == 0  # ( NO MORE EMPTY SQUARES )

    def fill_empty_square(self, index, char):
        if char == 'o' or char == 'x' and 0 <= index < len(self.__squares_array):  # if the parameters are valid ..
            self.__squares_array[index] = char

    def is_empty_square(self, index):
        return self.__squares_array[index] == "e"

    def get_line(self, line_index):
        if line_index == 0:
            return self.__squares_array[:3]
        elif line_index == 1:
            return self.__squares_array[3:6]
        elif line_index == 2:
            return self.__squares_array[6:9]
        else:  # invalid column index has been entered !
            return -1

    def get_column(self, column_index):
        """getting the column by column number """
        if column_index == 0:  # retrieving the first column, [ 0,3,6]
            return [self.__squares_array[0]] + [self.__squares_array[3]] + [self.__squares_array[6]]
        elif column_index == 1:
            return [self.__squares_array[1]] + [self.__squares_array[4]] + [self.__squares_array[7]]
        elif column_index == 2:
            return [self.__squares_array[2]] + [self.__squares_array[5]] + [self.__squares_array[8]]
        else:  # invalid column index has been entered !
            return -1

    def get_diagonals(self):
        """ getting the two diagonals """
        primary_diagonal = [self.__squares_array[0]] + [self.__squares_array[4]] + [self.__squares_array[8]]
        secondary_diagonal = [self.__squares_array[2]] + [self.__squares_array[4]] + [self.__squares_array[6]]
        return primary_diagonal, secondary_diagonal

    def check_winning(self):
        # FIRST - CHECKING THE LINES
        if self.__squares_array[0] == self.__squares_array[1] == self.__squares_array[2]:  # FIRST LINE
            return self.__squares_array[0]
        if self.__squares_array[3] == self.__squares_array[4] == self.__squares_array[5]:  # SECOND LINE
            return self.__squares_array[3]
        if self.__squares_array[6] == self.__squares_array[7] == self.__squares_array[8]:  # THIRD LINE
            return self.__squares_array[6]
        # SECOND - CHECKING THE COLUMNS
        if self.__squares_array[0] == self.__squares_array[3] == self.__squares_array[6]:  # FIRST COLUMN
            return self.__squares_array[0]
        if self.__squares_array[1] == self.__squares_array[4] == self.__squares_array[7]:  # SECOND COLUMN
            return self.__squares_array[1]
        if self.__squares_array[2] == self.__squares_array[5] == self.__squares_array[8]:  # THIRD COLUMN
            return self.__squares_array[2]
        # THIRD - CHECKING THE DIAGONALS
        if self.__squares_array[0] == self.__squares_array[4] == self.__squares_array[8]:  # PRIMARY DIAGONAL
            return self.__squares_array[0]
        if self.__squares_array[2] == self.__squares_array[4] == self.__squares_array[6]:  # SECONDARY DIAGONAL
            return self.__squares_array[2]
        return 'e'

    def find_winning_moves(self, turn):
        """find the winning moves, by finding the urgent moves the opponent has to react ..."""
        turn = 'x'
        winning_moves = self.find_blocking_moves(turn)
        print(f"the winning moves are {winning_moves}")
        return winning_moves

    def find_blocking_moves(self, turn):
        """find moves that are necessary in order to not lose """
        opponent = 'o' if turn == 'x' else 'x'
        # FIRST, CHECKING IF THE THE OPPONENT CAN WIN VIA LINES
        recommended_indices = []
        for i in range(3):
            data = "".join(self.get_line(i))
            if data.count(opponent) == 2:  # if there are two enemy shapes in a line, put the shape on the free square.
                if data.find('e') != -1:
                    recommended_indices.append(3 * i + data.find('e'))
        for i in range(3):
            data = "".join(self.get_column(i))
            if data.count(opponent) == 2:
                if data.find('e') != -1:
                    recommended_indices.append(3 * data.find('e') + i)
        primary_diagonal, secondary_diagonal = self.get_diagonals()
        data = "".join(primary_diagonal)
        if data.count(opponent) == 2:
            if data.find('e') != -1:
                recommended_indices.append(4 * data.find('e'))
        data = "".join(secondary_diagonal)
        if data.count(opponent) == 2:
            if data.find("e") != -1:
                recommended_indices.append(2 * data.find('e') + 2)
        return recommended_indices

    def random_move(self, empty_squares):
        return empty_squares[random.randrange(len(empty_squares))]

    def find_strategic_move(self, empty_squares):
        pass

    def basic_find_move(self, turn, mode=0):  # the turn can be either 'x' or 'o'
        if self.check_winning() == 'e' and not self.check_full_board():  # the board can't be full, or finished by win.
            empty_squares = self.get_empty_squares()
            blocking_moves = self.find_blocking_moves(turn)
            winning_moves = self.find_winning_moves(turn)
            print(winning_moves)
            if len(winning_moves) == 0:
                if len(blocking_moves) == 0:  # therefore everything is ok, and no urgent response is required
                    return self.random_move(empty_squares) if mode == 0 else self.find_strategic_move(empty_squares)
                elif len(blocking_moves) == 1:  # dealing with one issue, possible to defend !
                    return blocking_moves[0]
                else:
                    return "resign"  # if the opponent threatens on two fronts to get victory, the computer will resign !
            elif len(winning_moves) > 0:
                return winning_moves[0]

    def medium_find_move(self, turn):
        if turn == 'o':
            if len(self.get_empty_squares()) == 8:  # meaning this is the first move
                x_squares = self.get_x_squares()
                if 0 in x_squares or 2 in x_squares or 6 in x_squares or 8 in x_squares:
                    return 4
        return self.basic_find_move(turn=turn,
                                    mode=0)

    def run_in_console(self):
        win = self.check_winning()
        while win == 'e' and not self.check_full_board():
            player_move = int(input("Your Move:").strip())
            while not 0 <= player_move < 9 or not self.is_empty_square(player_move):
                player_move = int(input("Your Move:").strip())
            self.fill_empty_square(player_move, 'x')
            print(self)
            computer_move = self.basic_find_move('o')
            if str(computer_move) == 'resign':
                print("the computer resigned the game !")
                win = 'x'
                break
            else:
                self.fill_empty_square(computer_move, 'o')
                print(self)
            win = self.check_winning()
        if win == 'o':
            print("The computer won ..")
        elif win == 'x':
            print("You Won the game !")
        elif win == 'e':
            print("Tie !")
        else:
            print("An error has occured ..")

    def __str__(self):
        accumulator = ""
        for i in range(len(self.__squares_array)):
            value = "*" if self.__squares_array[i] == 'e' else self.__squares_array[i]
            accumulator += f"{value}"
            accumulator += "\n" if (i + 1) % 3 == 0 else " | "
        return accumulator


def main():
    new_board = Board()
    new_board.run_in_console()


if __name__ == '__main__':
    main()
