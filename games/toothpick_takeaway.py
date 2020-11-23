from random import randrange

class Game:
    def __init__(self):
        """
        Initializes a Game instance
        """
        self.toothpicks = 10
        self.winner = None
        self.in_progress = False

    def play(self, toothpicks):
        """
        Plays the game

        Parameters:
            toothpicks : int
                Number of toothpicks to start with
        """
        self.toothpicks = toothpicks
        self.in_progress = True
        self.winner = None

    def get_state(self, player, taken):
        """
        Gets the current state of the board

        Parameters:
            player : str
                The player who just move
            taken : int
                Number of toothpicks just taken

        Return:
            A message of the current game state
        """
        msg = "{} took {} toothpicks\nToothpicks Left: {}".format(player, taken, self.toothpicks)

        if self.winner is not None:
            msg = "Game over! {} wins!".format(self.winner)
            self.in_progress = False

        return msg

    def move(self, player, to_take):
        """
        Applies a given move to the board

        Parameters:
            player : int
                Player who moved
            to_take : int
                Number of toothpicks to take

        Return:
            True if the move was valid, else false
        """
        if to_take == 1 or to_take == 2:
            if self.toothpicks - to_take == 0:
                self.toothpicks -= to_take
                self.winner = player
                return True
            elif self.toothpicks - to_take > 0:
                self.toothpicks -= to_take
                return True
        return False

    def cpu_move(self):
        """
        Generates a random move of 1 or 2

        Return:
            A random number between 1 and 2
        """
        return randrange(1, 3)

