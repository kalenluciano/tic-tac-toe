import math
import time
from player import HumanPlayer, RandomComputerPlayer, SuperComputerPlayer


class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)] # use a single list to rep 3x3 board
        self.current_winner = None # keep track of winner

    def print_board(self):
        # get the rows
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2 etc (tells us what number corresponds to what box)
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print("| " + " | ".join(row) + " |")

    def make_move(self, square, letter):
        if self.board[square] == " ":
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # check rows
        row_ind = math.floor(square / 3)
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([s == letter for s in row]):
            return True
        # check columns
        col_ind = square % 3
        column = [self.board[col_ind+(i*3)] for i in range(3)]
        if all([s == letter for s in column]):
            return True
        # check diagnols
        if square % 2 == 0:
            diagnol1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == letter for s in diagnol1]):
                return True
            diagnol2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagnol2]):
                return True
        return False

    def available_moves(self):
        available_moves = []
        for i in range(len(self.board)):
            if self.board[i] == " ":
                available_moves.append(i)
        return available_moves

    def empty_squares(self):
        return " " in self.board

    def num_empty_squares(self):
        return self.board.count(" ")


def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = "X"

    while game.empty_squares():
        if letter == "O":
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):

            if print_game:
                print(letter + f" makes a move to square {square}")
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(letter + " is the winner!")
                return letter

            letter = "O" if letter == "X" else "X" # switches players

        time.sleep(1)

    if print_game:
        print("It's a tie!")


def start_game():
    mode_choice = ""
    mode = ["Easy", "Hard"]
    valid_mode = False
    user_letter_choice = ""
    letter_options = ["X", "O"]
    valid_letter = False

    while not valid_mode:
        mode_choice = input("Choose a level: Easy or Hard?\n")
        try:
            if mode_choice not in mode:
                raise ValueError
            valid_mode = True
        except ValueError:
            print("Invalid choice. Try again.")

    while not valid_letter:
        user_letter_choice = input("Pick X or O: ")
        try:
            if user_letter_choice not in letter_options:
                raise ValueError
            valid_letter = True
        except ValueError:
            print("Invalid choice. Try again.")

    if user_letter_choice == "O" and mode_choice == "Easy":
        x_player = RandomComputerPlayer("X")
        o_player = HumanPlayer("O")
    elif user_letter_choice == "X" and mode_choice == "Easy":
        x_player = HumanPlayer("X")
        o_player = RandomComputerPlayer("O")
    elif user_letter_choice == "O" and mode_choice == "Hard":
        x_player = SuperComputerPlayer("X")
        x_player.set_opponent_side(user_letter_choice)
        o_player = HumanPlayer("O")
    else:
        x_player = HumanPlayer("X")
        o_player = SuperComputerPlayer("O")
        o_player.set_opponent_side(user_letter_choice)

    return x_player, o_player

if __name__ == "__main__":
    x_player, o_player = start_game()
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)