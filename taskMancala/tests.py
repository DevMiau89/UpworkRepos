import unittest as ut
from mancala import *
from minimax import *
from test_trees import trees

class TestGame:
    def __init__(self, tree):
        # tree[i]: ith state
        # state = (player, score, child state indices ...)
        # action is just the child state index
        self.tree = tree

    def initial(self):
        return self.tree[0]

    def player(self, state):
        return state[0]
    
    def actions(self, state):
        return state[2:]

    def result(self, state, action):
        return self.tree[action]

    def is_over(self, state):
        return len(state) == 2

    def score(self, state):
        return state[1]

    def string(self, state):
        return str(state)

class MinimaxTestCase(ut.TestCase):
    def do_test(self, tree, expected_score):
        game = TestGame(tree)
        u, _, node_count = minimax(game, game.initial())
        self.assertTrue(u == expected_score)
    def test_0(self):
        self.do_test(trees[0], 10)
    def test_1(self):
        self.do_test(trees[1], 5)
    def test_2(self):
        self.do_test(trees[2], -2)
    def test_3(self):
        self.do_test(trees[3], 1)

class MinimaxABTestCase(ut.TestCase):
    def do_test(self, tree, expected_node_count):
        game = TestGame(tree)
        u, _, _ = minimax(game, game.initial())
        u_ab, _, actual_node_count = minimax_ab(game, game.initial())
        self.assertTrue(u == u_ab)
        self.assertTrue(actual_node_count == expected_node_count)
    def test_0(self):
        self.do_test(trees[0], 1)
    def test_1(self):
        self.do_test(trees[1], 3)
    def test_2(self):
        self.do_test(trees[2], 7)
    def test_3(self):
        self.do_test(trees[3], 12)

class MancalaGameTestCase(ut.TestCase):
    def setUp(self):
        self.mg = MancalaGame()
    def test_initial(self):
        actual = self.mg.initial()
        expected = (4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0)
        self.assertTrue(actual == expected)
    def test_actions(self):
        states = [
            (4, 4, 0, 4, 4, 4, 0, 4, 0, 4, 4, 0, 4, 0, 0),
            (4, 3, 4, 0, 0, 4, 0, 4, 1, 1, 0, 4, 4, 0, 0),
            (2, 4, 3, 0, 4, 4, 0, 4, 1, 3, 4, 5, 4, 0, 1),
            (4, 3, 0, 4, 5, 6, 0, 0, 0, 0, 0, 0, 0, 3, 1),
        ]
        actions = [
            [0, 1, 3, 4, 5],
            [0, 1, 2, 5],
            [7, 8, 9, 10, 11, 12],
            [],
        ]
        for s, a in zip(states, actions):
            self.assertTrue(self.mg.actions(s) == a)
    def test_result(self):
        states = [
            (4, 4, 0, 4, 4, 4, 0, 4, 0, 4, 4, 0, 4, 0, 0), # 0, 3
            (4, 4, 0, 0, 5, 5, 1, 5, 0, 4, 4, 0, 4, 0, 1), # 1, 9
            (4, 4, 0, 0, 5, 5, 1, 5, 0, 0, 5, 1, 5, 1, 1), # 2, 12
            (5, 5, 1, 1, 5, 5, 1, 5, 0, 0, 5, 1, 0, 2, 0), # 3, 4
            (5, 5, 1, 1, 0, 6, 2, 6, 1, 1, 5, 1, 0, 2, 1), # 4, 11
            (0, 5, 1, 1, 0, 6, 2, 6, 1, 1, 5, 0, 0, 8, 0), # 5, 1
            (0, 0, 2, 2, 1, 7, 3, 6, 1, 1, 5, 0, 0, 8, 0), # 6, 3
            (0, 0, 2, 0, 2, 8, 3, 6, 1, 1, 5, 0, 0, 8, 1), # 7, 8
            (0, 0, 2, 0, 2, 8, 3, 6, 0, 2, 5, 0, 0, 8, 0), # 8, 5
            (0, 0, 2, 0, 2, 0, 6, 7, 1, 3, 6, 1, 0, 8, 1), # 9, 7
            (1, 0, 2, 0, 2, 0, 6, 0, 2, 4, 7, 2, 1, 9, 0), # 10
        ]
        actions = [3, 9, 12, 4, 11, 1, 3, 8, 5, 7]
        for k in range(len(actions)):
            s_new = self.mg.result(states[k], actions[k])
            self.assertTrue(s_new == states[k+1])

    def test_is_over(self):
        self.assertFalse(self.mg.is_over((4, 4, 0, 4, 4, 4, 0, 4, 0, 4, 4, 0, 4, 0, 0)))
        self.assertTrue(self.mg.is_over((4, 4, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 10, 0)))
        self.assertTrue(self.mg.is_over((4, 4, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 10, 1)))

    def test_score(self):
        self.assertTrue(self.mg.score((4, 4, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 10, 0)) == 10)
        self.assertTrue(self.mg.score((1, 0, 2, 0, 2, 0, 6, 0, 2, 4, 7, 2, 1, 9, 0)) == -3)

if __name__ == "__main__":
    test_suite = ut.TestLoader().loadTestsFromTestCase(MancalaGameTestCase)
    ut.TextTestRunner(verbosity=2).run(test_suite)

    test_suite = ut.TestLoader().loadTestsFromTestCase(MinimaxTestCase)
    ut.TextTestRunner(verbosity=2).run(test_suite)

    test_suite = ut.TestLoader().loadTestsFromTestCase(MinimaxABTestCase)
    ut.TextTestRunner(verbosity=2).run(test_suite)

