import math
import random


class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter

    # we want all players to get their next move given a game
    def get_move(self, game):
        pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + "'s turn. Input move (0-8): ")
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val

class SuperComputerPlayer(Player):
    opponent_letter = ""

    def __init__(self, letter):
        super().__init__(letter)

    def set_opponent_side(self, player_side):
        self.opponent_letter = player_side

    def get_move(self, game):
        corners = [i for i in range(0, 9, 2) if i % 2 == 0 and i != 4]
        edges = [i for i in range(1, 8, 2)]
        edges_taken = [game.board[i] for i in edges]
        edges_taken_counter = 0
        # If computer goes first:
        # First move is to put a letter in a corner
        if game.num_empty_squares() == 9:
            square = random.choice(corners)
            return square
        # Second move depends on opponent's move
        elif game.num_empty_squares() == 7:
            # If opponent places letter in the center, place letter in the corner across from computer's first letter
            if game.board[4] != " ":
                if game.board[0] != " ":
                    square = 8
                    return square
                elif game.board[2] != " ":
                    square = 6
                    return square
                elif game.board[6] != " ":
                    square = 2
                    return square
                elif game.board[8] != " ":
                    square = 0
                    return square
            # If opponent places letter at an edge, place letter in a corner with a space between first letter
            # First, figure out if any edges are taken
            for i in edges:
                if game.board[i] == " ":
                    edges_taken[edges_taken_counter] = False
                else:
                    edges_taken[edges_taken_counter] = True
                edges_taken_counter += 1
            # If any are taken, take action on which spot to put the letter
            if any(edges_taken):
                if self.letter in game.board[0]:
                    if game.board[1] != " ":
                        square = 6
                        return square
                    elif game.board[3] != " ":
                        square = 2
                        return square
                elif self.letter in game.board[2]:
                    if game.board[1] != " ":
                        square = 8
                        return square
                    elif game.board[5] != " ":
                        square = 0
                        return square
                elif self.letter in game.board[6]:
                    if game.board[3] != " ":
                        square = 8
                        return square
                    elif game.board[7] != " ":
                        square = 0
                        return square
                elif self.letter in game.board[8]:
                    if game.board[7] != " ":
                        square = 2
                        return square
                    elif game.board[5] != " ":
                        square = 6
                        return square
            # If opponent places letter at a corner, place in any available corner
            else:
                for i in corners:
                    if game.board[i] == " ":
                        square = i
                        return square
        # Third and fourth move depends on opponent's move
        elif game.num_empty_squares() == 5 or game.num_empty_squares() == 3:
            for i in game.available_moves():
                game.board[i] = self.letter
                if game.winner(i, self.letter):
                    game.board[i] = " "
                    square = i
                    return square
                else:
                    game.board[i] = " "
            for i in game.available_moves():
                game.board[i] = self.opponent_letter
                if game.winner(i, self.opponent_letter):
                    game.board[i] = " "
                    square = i
                    return square
                else:
                    game.board[i] = " "
            for i in corners:
                if game.board[i] == " ":
                    square = i
                    return square
        # Fifth move is whatever spot is available
        elif game.num_empty_squares() == 1:
            square = random.choice(game.available_moves())
            return square

        # If computer goes second:
        # First move
        if game.num_empty_squares() == 8:
            # And human placed in center, place letter in a corner
            if game.board[4] != " ":
                square = random.choice([0, 2, 6, 8])
                return square
            # And human placed in corner or edge, place letter in center
            else:
                square = 4
                return square
        # Second move
        elif game.num_empty_squares() == 6:
            # Block any potential wins for opponent
            for i in game.available_moves():
                game.board[i] = self.opponent_letter
                if game.winner(i, self.opponent_letter):
                    game.board[i] = " "
                    square = i
                    return square
                else:
                    game.board[i] = " "
            # If first move was in the center:
            if game.board[4] == self.letter:
                # And opponent is only on the edges:
                for i in edges:
                    if game.board[i] == self.opponent_letter:
                        edges_taken[edges_taken_counter] = True
                    else:
                        edges_taken[edges_taken_counter] = False
                    edges_taken_counter += 1
                if edges_taken.count(True) == 2:
                    square = random.choice(corners)
                    return square
                else:
                    square_options = edges
                    for i in square_options:
                        if game.board[i] != " ":
                            square_options.remove(i)
                    square = random.choice(square_options)
                    return square
        # Third and fourth move
        else:
            for i in game.available_moves():
                game.board[i] = self.letter
                if game.winner(i, self.letter):
                    game.board[i] = " "
                    square = i
                    return square
                else:
                    game.board[i] = " "
            for i in game.available_moves():
                game.board[i] = self.opponent_letter
                if game.winner(i, self.opponent_letter):
                    game.board[i] = " "
                    square = i
                    return square
                else:
                    game.board[i] = " "
            square = random.choice(game.available_moves())
            return square