from board import Board, CaptureOption, QBoard, Move

import unittest

class Test_Board(unittest.TestCase):
    def test_simple_game(self):

        # Create a board and compare the result.
        checkers = Board(3,1)
        self.assertEqual(checkers.board, [[1,0,1],[0,0,0],[-1,0,-1]])
        self.assertEqual(checkers.move(0,0,1,1,1), Move.success_opponents_turn)
        self.assertEqual(checkers.move(2,2,-2,-2,-1), Move.finish)
        self.assertEqual(checkers.board, [[-1,0,1],[0,0,0],[-1,0,0]])

    def test_capture_options(self):
        checkers = Board(5,1)
        self.assertEqual(checkers.move(0,0,1,1,1), Move.success_opponents_turn)
        self.assertEqual(checkers.capture_options, [])
        self.assertEqual(checkers.move(1,1,1,1,1), Move.success_opponents_turn)
        self.assertEqual(checkers.capture_options, [])
        self.assertEqual(checkers.move(2,2,2,2,1), Move.path_blocked)
        self.assertEqual(checkers.move(2,2,1,1,1), Move.success_opponents_turn)
        self.assertEqual(checkers.capture_options, [CaptureOption(-1,4,4,-2,-2),CaptureOption(-1,2,4,2,-2)])

    def test_full_game(self):
        checkers = Board(7,1)
        self.assertEqual(checkers.move(0,0,1,1,1), Move.success_opponents_turn)
        self.assertEqual(checkers.move(0,0,1,1,1), Move.no_piece_found)
        self.assertEqual(checkers.move(0,6,1,-1,-1), Move.success_opponents_turn)
        self.assertEqual(checkers.move(6,0,-1,1,1), Move.success_opponents_turn)
        self.assertEqual(checkers.move(2,6,1,-1,-1), Move.success_opponents_turn)
        self.assertEqual(checkers.move(5,1,1,1,1), Move.success_opponents_turn)
        self.assertEqual(checkers.move(4,6,1,-1,-1), Move.success_opponents_turn)
        self.assertEqual(checkers.move(1,1,-1,1,1), Move.success_opponents_turn)
        self.assertEqual(checkers.move(1,5,1,-1,-1), Move.success_opponents_turn)
        self.assertEqual(checkers.move(6,2,-1,1,1), Move.success_opponents_turn)
        self.assertEqual(checkers.move(2,4,-1,-1,-1), Move.success_opponents_turn)
        self.assertEqual(checkers.move(0,2,2,2,1), Move.success_same_turn)
        self.assertEqual(checkers.finished,False)
        self.assertEqual(checkers.move(2,4,2,2,1), Move.finish)
        self.assertEqual(checkers.finished,True)

    def test_entanglement(self):
        checkers = QBoard(7,1)
        checkers.quantum_split(2,0,1)
        checkers.move(0,6,1,-1,-1)
        checkers.quantum_split(4,0,1)
        checkers.move(1,5,1,-1,-1)
        checkers.move(5,1,1,1,1)
        checkers.move(2,4,-1,-1,-1)
        checkers.move(1,1,1,1,1)
        self.assertEqual(checkers.quantum_board,[[100,0,0,0,25,0,100],[0,0,0,75,0,0,0],[0,0,50,0,0,0,50],[0,-100,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,-100,0,-100,0,-100]])

    def test_full_normal_game_on_quantum_board(self):

        checkers = QBoard(7,1)
        self.assertEqual(checkers.move(0,0,1,1,1), [Move.success_opponents_turn])
        self.assertEqual(checkers.move(1,1,1,1,-1), [Move.no_piece_found])
        self.assertEqual(checkers.move(0,6,1,-1,-1), [Move.success_opponents_turn])
        self.assertEqual(checkers.move(6,0,-1,1,1), [Move.success_opponents_turn])
        self.assertEqual(checkers.move(2,6,1,-1,-1), [Move.success_opponents_turn])
        self.assertEqual(checkers.move(5,1,1,1,1), [Move.success_opponents_turn])
        self.assertEqual(checkers.move(4,6,1,-1,-1), [Move.success_opponents_turn])
        self.assertEqual(checkers.move(1,1,-1,1,1), [Move.success_opponents_turn])
        self.assertEqual(checkers.move(1,5,1,-1,-1), [Move.success_opponents_turn])
        self.assertEqual(checkers.move(6,2,-1,1,1), [Move.success_opponents_turn])
        self.assertEqual(checkers.move(2,4,-1,-1,-1), [Move.success_opponents_turn])
        self.assertEqual(checkers.move(0,2,2,2,1), [Move.success_same_turn])
        self.assertEqual(checkers.finished,False)
        self.assertEqual(checkers.move(2,4,2,2,1), [Move.finish])
        self.assertEqual(checkers.finished,True)

    def test_board_init(self):
        checkers = Board(3,1)
        self.assertEqual(checkers.board, [[1,0,1],[0,0,0],[-1,0,-1]])
    
    def test_bad_board(self):
        with self.assertRaises(ValueError):
            Board(4,3)

    def test_quantum_split(self):
        checkers = QBoard(5,1)
        self.assertEqual(checkers.quantum_split(2,0,1),[Move.success_opponents_turn])
        self.assertEqual(checkers.quantum_board,[[100,0,0,0,100],[0,50,0,50,0],[0,0,0,0,0],[0,0,0,0,0],[-100,0,-100,0,-100]])


if __name__ == '__main__':
    unittest.main()
