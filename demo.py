from game import Checkers, QCheckers
from board import QBoard

def huge_measurement():
    checkers = QBoard(7,1)
    checkers.quantum_split(2,0,1)
    checkers.move(0,6,1,-1,-1)
    checkers.quantum_split(4,0,1)
    checkers.move(1,5,1,-1,-1)
    checkers.move(5,1,1,1,1)
    checkers.move(2,4,-1,-1,-1)
    checkers.move(1,1,1,1,1)

    match = QCheckers(7,1)
    match.environment = checkers
    match.player_turn = -1
    return match