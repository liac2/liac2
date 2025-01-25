import unittest
from tictactoe import winner

X = "X"
O = "O"
EMPTY = None

class Tests(unittest.TestCase):

    def test1(self):
        test = [
            [EMPTY, EMPTY, X],
            [EMPTY, EMPTY, X],
            [EMPTY, EMPTY, X],
        ]
        self.assertEqual(winner(test), X)

    def test2(self):
        test = [
            [EMPTY, O, EMPTY],
            [EMPTY, O, EMPTY],
            [EMPTY, O, EMPTY],
        ]
        self.assertEqual(winner(test), O)


    def test3(self):
        test = [
            [X, EMPTY, EMPTY],
            [EMPTY, X, EMPTY],
            [EMPTY, EMPTY, X],
        ]
        self.assertEqual(winner(test), X)

    def test4(self):
        test = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ]
        self.assertEqual(winner(test), EMPTY)

    def test5(self):
        test = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ]
        self.assertEqual(winner(test), EMPTY)


    def test6(self):
        test = [
            [EMPTY, X, EMPTY],
            [EMPTY, X, EMPTY],
            [EMPTY, X, EMPTY],
        ]
        self.assertEqual(winner(test), X)


    def test7(self):
        test = [
            [EMPTY, EMPTY, X],
            [EMPTY, X, EMPTY],
            [X, EMPTY, EMPTY],
        ]
        self.assertEqual(winner(test), X)


    def test8(self):
        test = [
            [EMPTY, EMPTY, X],
            [EMPTY, X, EMPTY],
            [X, EMPTY, EMPTY],
        ]
        self.assertEqual(minimax(test), X)



if __name__ == "__main__":
    unittest.main()