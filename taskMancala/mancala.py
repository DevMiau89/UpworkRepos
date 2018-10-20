"""
A game state is represented by a tuple.  The leading elements of
the tuple are the number of stones in each position, from position 0
to the final position. The last element of the tuple is the current
player, either 0 or 1.
"""

class MancalaGame:

    def __init__(self, size=6, count=4):
        self.size = size
        self.count = count

    def initial(self):
        """
        Return the initial game state.
        """
        return ((self.count,)*self.size + (0,))*2 + (0,)

    def player(self, state):
        """
        Return the current player in the given game state.
        """
        print('to jest state', state[-1])
        return state[-1]
    
    # def actions(self, state):
    #     """
    #     Return a list of all actions available in the current game state.
    #     Each action is the position number of a non-empty small position
    #     on the current player's half of the board.
    #     """
    #     ## Finish me! ##
    #     raise(Exception("Not implemented yet."))
    
    # def result(self, state, action):
    #     """
    #     Return the new game state that results from playing the given
    #     action in the given state.  Be sure to account for the special
    #     cases where a player's last stone lands in one of their own small
    #     positions, and when a player's last stone lands in their own mancala.
    #     """
    #     ## Finish me! ##
    #     raise(Exception("Not implemented yet."))

    def is_over(self, state):
        """
        Return True if the game is over in the given state, False otherwise.
        The game is over if either player has no stones left in their small positions.
        """
        ## Finish me! ##
        over = True
        for elem in state:
            if elem != 0:
                over = False
        if over:
            return True

        over = True
        for elem in state:
            if elem != 0:
                over = False
        return over


    def score(self, state):
        """
        Return the score in the current state, from player 0's perspective.
        If the game is over and one player still has stones on their side,
        those stones are added to that player's score.
        """
        ## Finish me! ##

        if self.is_over(state) and self.player(state):



        return score


    def string(self, state):
        """
        Display current state as a game board.  The current player's mancala
        is marked with *.
        """
        z = self.size
        s = " ".join(["%2d"%m for m in state[-2:z:-1]] + [" *" if state[-1]==0 else "  "])
        s += "\n"
        s += " ".join(["  " if state[-1]==0 else " *"] + ["%2d"%m for m in state[:(z+1)]])
        return s

if __name__ == "__main__":

    """
    Scratch pad for informal tests
    """

    mg = MancalaGame(size=3, count=2)

    s = mg.initial()
    mg.player(s)
    # a = mg.actions(s)
    print(mg.string(s))
    # print(s)
    # print(a)
    print("Is over: %s"%mg.is_over(s))
    # print("Score = %d"%mg.score(s))
    # print("")
    #
    # s = mg.result(s, 2)
    # a = mg.actions(s)
    # print(mg.string(s))
    # print(s)
    # print(a)
    # print("Is over: %s"%mg.is_over(s))
    # print("Score = %d"%mg.score(s))
    # print("")

