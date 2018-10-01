from board import Board, QBoard, Move

class Checkers:
    def __init__(self,size=10,population=3):
        self.environment = Board(size,population)
        self.player_turn = 1
    
    def tstart(self,debug=False):
        
        while not self.environment.finished:
            self.ask_for_next_move(debug)
        
        print('=============')
        if self.player_turn == 1:
            print('Player 1 has won!')
        else:
            print('Player 2 has won!')

    def ask_for_next_move(self,debug):

        print(self.environment)
        if debug == True:
            print(self.environment.capture_options)

        # Interpret the user's input.
        question = input("What to do next? ").split(' ')
        try:
            int(question)
        except:
            print("Sorry, but that isn't a valid input!")
            return
        answer = self.environment.move(int(question[0]),int(question[1]),int(question[2]),int(question[3]), self.player_turn)

        if debug == True:
            print(answer)

        # Switch turns if move was accepted.        
        if answer == Move.success_opponents_turn and self.environment.finished == False:
            self.player_turn *= -1


class QCheckers:
    def __init__(self,size=10,population=3):
        self.environment = QBoard(size,population)
        self.player_turn = 1
    
    def tstart(self,debug=False):
        
        while not self.environment.finished:
            self.ask_for_next_move(debug)
        
        print('=============')

        if self.player_turn == 1:
            print('Player 1 has won!')
        else:
            print('Player 2 has won!')
    
    def ask_for_next_move(self,debug):

        print(self.environment)
        if debug == True:
            print(self.environment.capture_options)

        # Ask for the user's input
        question = input("What to do next? ").split(' ')
        if question[0] == 'Q':
            answer = self.environment.quantum_split(int(question[1]),int(question[2]),self.player_turn)
        else:
            answer = self.environment.move(int(question[0]),int(question[1]),int(question[2]),int(question[3]), self.player_turn)

        if debug == True:
            print(answer)
        
        # Switch teams if the move is accepted.
        if Move.success_opponents_turn in answer and self.environment.finished == False:
            self.player_turn *= -1
