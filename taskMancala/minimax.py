from itertools import count
from mancala import *

def minimax(game, state, max_depth=None):
    """
    Run minimax search from the current game state up to a maximum search depth.
    Return the best utility found for the current player, the best next action,
    and the number of nodes encountered during the search.
    """
    
    ## Finish me! ##
    # Update the following code to return the correct node count
    # and the correct utility.

    if game.is_over(state) or max_depth == 0: return game.score(state), None, 1

    actions = game.actions(state)
    utilities = []
    node_count = 0
    for action in actions:
    
        new_state = game.result(state, action)
        u, _, nc = minimax(game, new_state, None if max_depth is None else max_depth - 1)
        utilities.append(u)
        # update node count here
    
    u = utilities[0] # change this to update utility correctly
    return u, actions[utilities.index(u)], node_count + 1

def minimax_ab(game, state, alpha=None, beta=None, max_depth=None):
    """
    Run minimax search with alpha-beta pruning.
    """

    ## Finish me! [grad] ##
    # Update the following code to return the correct node count
    # and the correct utility.

    if game.is_over(state) or max_depth == 0: return game.score(state), None, 1

    actions = game.actions(state)
    utilities = []
    node_count = 0
    for action in actions:
    
        new_state = game.result(state, action)
        u, _, nc = minimax_ab(
            game, new_state, alpha, beta,
            None if max_depth is None else max_depth - 1)
        utilities.append(u)
        # Update node count here
        
        if game.player(state) == 0:
            if beta is not None and u > beta: break
            ## Finish me! [grad] ##
            # If the current child utility for player 0 is higher than the best
            # found so far, update alpha. Alpha is the best utility player 0 has
            # been able to achieve at any of player 0's choice points so far.
            alpha = None # change this to correctly update alpha
        else:
            if alpha is not None and u < alpha: break
            ## Finish me! [grad] ##
            # If the current child utility for player 0 is lower than the worst
            # found so far, update beta. Beta is the worst utility player 0 has
            # encountered at any of player 1's choice points so far.
            beta = None # change this to correctly update alpha
    
    u = utilities[0] # change this to update utility correctly
    return u, actions[utilities.index(u)], node_count + 1

def play(game, alg, moves=None, verbose=False):

    state = game.initial()
    if verbose: print(game.string(state))

    player = game.player(state)
    turn = 0
    full_node_count = 0
    for move in count():

        if game.is_over(state): break
        if move == moves: break
    
        if player != game.player(state): turn += 1
        player = game.player(state)
        score = game.score(state)
        utility, action, node_count = alg(game, state)
        if move == 0: full_node_count = node_count

        if verbose: print("Move %d, turn %d: Player %d's move = %d, utility = %d, score = %d"%(
            move, turn, player, action, utility, score))
        if verbose: print("")

        state = game.result(state, action)
        if verbose: print(game.string(state))

    if verbose: print("Final score: %d, node count = %d" % (game.score(state), full_node_count))
    return game.score(state)

def play_minimax(game, max_depth=None, moves=None, verbose=False):
    alg = lambda game, state: minimax(game, state, max_depth=max_depth)
    final_score = play(game, alg, moves=moves, verbose=verbose)
    return final_score

if __name__ == "__main__":

    """
    Scratch pad for informal tests
    """

    max_depth = 5
    moves = 100
    verbose=True
    mg = MancalaGame(size=5, count=2)

    fs = play_minimax(mg, max_depth=max_depth, moves=moves, verbose=verbose)

    # alg = lambda game, state: minimax_ab(game, state, max_depth=max_depth)
    # fs_ab = play(mg, alg, moves=moves, verbose=verbose)

    print("minimax: %f" % fs)
    # print("ab: %f" % fs_ab)

