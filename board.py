from enum import Enum
import random
import copy

class Move(Enum):
    success_opponents_turn = 1
    success_same_turn = 2
    finish = 3
    
    no_piece_found = 4
    no_victim_found = 5
    path_blocked = 6
    out_of_bounds = 7
    invalid_destination = 8

    capture_ignored = 9
    friendly_piece = 10

    quantum_not_ready = 11

class Board:
    def __init__(self,size, population):
        """Create a new board to play a game on checkers on!  
        Keyword arguments:  
        size -> the size of the board  
        population -> the amount of rows each player has populated with pieces"""

        if size < 2 * population:
            raise ValueError("Game board not big enough to fit population for both players.")

        self.board = [[0 for row in range(size)] for column in range(size)]
        self.capture_options = []
        self.finished = False
    
        for row in range(size):
            # Only populate the given row amount for each player.
            if row < population or row > size - population - 1:
                for column in range(size):
                    if (row+column) % 2 == 0:
                        self.board[row][column] = 1
                        if row > size - population - 1:
                            self.board[row][column] = -1
    
    def __repr__(self):
        """Display the board to the terminal, if wished."""
        answer = '\n'
        for i in range(len(self)):
            for j in range(len(self)):
                if (i+j)%2 == 0:
                    answer += '{}'.format(self.board[i][j])
                else:
                    answer += '-'
                answer += '\t'
            answer += '\n'
        return answer

    def __len__(self):
        """Return the size of the board. One dimension is provided, not all squares comined."""
        return len(self.board)

    def move(self,x_pos,y_pos,x_dir,y_dir,user):
        """Move a certain piece, if possible.  
        The function returns an that explains whether the move has been made, and why so/not."""

        if self.finished == True:
            return Move.finish

        size = len(self)
        if not self.__on_the_board(x_pos+x_dir, y_pos+y_dir):
            return Move.out_of_bounds

        moving_piece = self.board[y_pos][x_pos]

        if moving_piece == 0 or user * moving_piece < 0:
            return Move.no_piece_found

        if not self.__valid_direction(x_dir,y_dir):
            return Move.invalid_destination

        if self.board[y_pos+y_dir][x_pos+x_dir] != 0:
            return Move.path_blocked
        
        # List of moves the user can make if captures are possible.
        user_capture_options = [forced_move for forced_move in self.capture_options if forced_move.user == moving_piece]

        if user_capture_options != []:
            if not self.__is_capture_move(moving_piece,x_pos,y_pos,x_dir,y_dir):
                return Move.capture_ignored
        
        if abs(x_dir) == 1:
            return self.__move_single_tile(moving_piece,x_pos,y_pos,x_dir,y_dir,user)

        if abs(x_dir) == 2:
            return self.__move_double_tile(moving_piece,x_pos,y_pos,x_dir,y_dir,user)

        # This code should not be reached, as abs(x_dir) is forced to be either 1 or 2 before looking at the if-clauses.
        # However, may this filter ever need to be altered, here's a handy error to let you know that you did something wrong.
        raise NotImplementedError("This code should not be reached!")

    def quantum_move(self,x_pos,y_pos,user):
        """This function tests if it is possible to make a quantum move for this function."""
        test_board_left = copy.deepcopy(self)
        test_board_right = copy.deepcopy(self)

        if not self.__on_the_board(x_pos,y_pos):
            return False

        if test_board_left.move(x_pos,y_pos,-1,user,user) == Move.success_opponents_turn:
            return test_board_right.move(x_pos,y_pos,1,user,user) == Move.success_opponents_turn
        return False

    def __move_single_tile(self,moving_piece,x_pos,y_pos,x_dir,y_dir,user):
        # * The piece makes a normal move.
        size = len(self)

        if self.__walks_backwards(moving_piece, y_dir):
            return Move.invalid_destination
        
        # * If everything else goes right, finally make the move to the location.
        self.board[y_pos+y_dir][x_pos+x_dir] = moving_piece
        self.board[y_pos][x_pos] = 0

        # * Refresh all CaptureOptions and add new potential ones.
        self.capture_options = [forced_move for forced_move in self.capture_options if forced_move.still_valid(self.board)]

        # Look for kills that appear now the user has left the space empty.
        for killer_coords in [(2,2),(2,-2),(-2,2),(-2,-2)]:
            x_killer = x_pos - killer_coords[0]
            y_killer = y_pos - killer_coords[1]
            x_direct = killer_coords[0]
            y_direct = killer_coords[1]

            if x_killer in range(size) and y_killer in range(size):
                order = CaptureOption(self.board[y_killer][x_killer],x_killer,y_killer,x_direct,y_direct)

                if order.still_valid(self.board) and order not in self.capture_options:
                    self.capture_options.append(order)

        # Look for kills that appear because the user stepped on the new tile.
        for killer_coords in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            x_killer = x_pos + x_dir - killer_coords[0]
            y_killer = y_pos + y_dir - killer_coords[1]
            x_direct = 2*killer_coords[0]
            y_direct = 2*killer_coords[1]

            if x_killer in range(size) and y_killer in range(size):
                order = CaptureOption(self.board[y_killer][x_killer],x_killer,y_killer,x_direct,y_direct)

                if order.still_valid(self.board) and order not in self.capture_options:
                    self.capture_options.append(order)

        # Last, look if the user could kill someone next turn.
        # When taking a small step, this isn't important, but taking this action separately is crucial
        # when capturing players. 
        for killer_coords in [(2,2),(2,-2),(-2,2),(-2,-2)]:
            x_killer = x_pos + x_dir
            y_killer = y_pos + y_dir
            x_direct = killer_coords[0]
            y_direct = killer_coords[1]

            order = CaptureOption(self.board[y_killer][x_killer],x_killer,y_killer,x_direct,y_direct)

            if order.still_valid(self.board) and order not in self.capture_options:
                self.capture_options.append(order)

        if self.__reached_end():
            self.finished = True
            self.winner = user
            return Move.finish

        return Move.success_opponents_turn

    def __move_double_tile(self,moving_piece,x_pos,y_pos,x_dir,y_dir,user):
        # * The piece attempts to capture another piece.
        size = len(self)

        if self.board[y_pos+(y_dir//2)][x_pos+(x_dir//2)] == 0:
            return Move.no_victim_found
        
        try:
            self.capture_options.remove(CaptureOption(moving_piece,x_pos,y_pos,x_dir,y_dir))
        except ValueError:
            # This move should've been present as a CaptureOption.
            # However, if it wasn't, it doesn't need to stop the whole program,
            # a warning should suffice.
            print("WARNING: Failed attempt to remove a CaptureOption that wasn\'t present.")

        self.board[y_pos][x_pos] = 0
        self.board[y_pos+(y_dir//2)][x_pos+(x_dir//2)] = 0
        self.board[y_pos+y_dir][x_pos+x_dir] = moving_piece

        # * Refresh all CaptureOptions and add new potential ones.
        self.capture_options = [forced_move for forced_move in self.capture_options if forced_move.still_valid(self.board)]

        # Look for kills that appear now the user has left their own space empty.
        for killer_coords in [(2,2),(2,-2),(-2,2),(-2,-2)]:
            x_killer = x_pos - killer_coords[0]
            y_killer = y_pos - killer_coords[1]
            x_direct = killer_coords[0]
            y_direct = killer_coords[1]

            if x_killer in range(size) and y_killer in range(size):
                order = CaptureOption(self.board[y_killer][x_killer],x_killer,y_killer,x_direct,y_direct)

                if order.still_valid(self.board) and order not in self.capture_options:
                    self.capture_options.append(order)

        # Look for kills that appear now the user has left the victim's space empty.
        for killer_coords in [(2,2),(2,-2),(-2,2),(-2,-2)]:
            x_killer = x_pos + (x_dir//2) - killer_coords[0]
            y_killer = y_pos + (y_dir//2) - killer_coords[1]
            x_direct = killer_coords[0]
            y_direct = killer_coords[1]

            if x_killer in range(size) and y_killer in range(size):
                order = CaptureOption(self.board[y_killer][x_killer],x_killer,y_killer,x_direct,y_direct)

                if order.still_valid(self.board) and order not in self.capture_options:
                    self.capture_options.append(order)

        # Look for kills that appear because the user stepped on the new tile.
        for killer_coords in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            x_killer = x_pos + x_dir - killer_coords[0]
            y_killer = y_pos + y_dir - killer_coords[1]
            x_direct = 2*killer_coords[0]
            y_direct = 2*killer_coords[1]

            if x_killer in range(size) and y_killer in range(size):
                order = CaptureOption(self.board[y_killer][x_killer],x_killer,y_killer,x_direct,y_direct)

                if order.still_valid(self.board) and order not in self.capture_options:
                    self.capture_options.append(order)

        # Last, look if the user could kill someone next turn.
        # When taking a small step, this isn't important, but taking this action separately is crucial
        # when capturing players.
        another_capture_found = False
        for killer_coords in [(2,2),(2,-2),(-2,2),(-2,-2)]:
            x_killer = x_pos + x_dir
            y_killer = y_pos + y_dir
            x_direct = killer_coords[0]
            y_direct = killer_coords[1]

            order = CaptureOption(self.board[y_killer][x_killer],x_killer,y_killer,x_direct,y_direct)

            if order.still_valid(self.board) and order not in self.capture_options:
                self.capture_options.append(order)
                another_capture_found = True

        if self.__victory_found():
            self.finished = True
            self.winner = user
            return Move.finish

        if another_capture_found:
            return Move.success_same_turn
        return Move.success_opponents_turn

    def __victory_found(self):
        if 1 in self.board[-1] or -1 in self.board[0]:
            return True
        
        player1_found = False
        player2_found = False
        
        for row in self.board:
            if 1 in row:
                player1_found = True
                if player2_found:
                    return False
            if -1 in row:
                player2_found = True
                if player1_found:
                    return False
        
        return True

    def __reached_end(self):
        return 1 in self.board[-1] or -1 in self.board[0]

    def __on_the_board(self,x,y):
        if x in range(len(self)) and y in range(len(self)):
            return True
        return False

    def __valid_direction(self,x_direction,y_direction):
        if abs(x_direction) != abs(y_direction):
            return False
        if abs(x_direction) == 0:
            return False
        if abs(x_direction) > 2:
            return False
        return True
    
    def __is_capture_move(self,user,x_pos,y_pos,x_dir,y_dir):
        return CaptureOption(user,x_pos,y_pos,x_dir,y_dir) in self.capture_options

    def __walks_backwards(self,user,direction):
        return user * direction < 0

class CaptureOption:
    def __init__(self,user,x_pos,y_pos,x_dir,y_dir):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.user = user
    
    def __eq__(self,other):
        if self.user == other.user:
            return self.x_pos == other.x_pos and self.y_pos == other.y_pos and self.x_dir == other.x_dir and self.y_dir == other.y_dir
        return False

    def __repr__(self):
        return "<({},{}) -> ({},{})>".format(self.x_pos,self.y_pos,self.x_pos+self.x_dir,self.y_pos+self.y_dir)

    def still_valid(self,board) -> bool:
        """"Make sure a capture force is still valid.  
        If the kill is still valid, it returns True. Otherwise, it returns False."""

        # Return False if any of the pieces are outside the board.
        if self.y_pos not in range(len(board)) or self.x_pos not in range(len(board)):
            return False
        if self.y_pos + self.y_dir not in range(len(board)) or self.x_pos + self.x_dir not in range(len(board)):
            return False
        # Return False if the spot behind the victim_piece is no longer empty.
        if board[self.y_pos+self.y_dir][self.x_pos+self.x_dir] != 0:
            return False

        killer_piece = board[self.y_pos][self.x_pos]
        victim_piece = board[self.y_pos+(self.y_dir//2)][self.x_pos+(self.x_dir//2)]

        # Return False if the pieces are the same type or if either piece has disappeared from the spot.
        if killer_piece == victim_piece or 0 in [killer_piece,victim_piece]:
            return False
        return True

class QBoard:
    def __init__(self,size=10,population=3):
        self.board_list = [Board(size,population)]
        self.quantum_board = self.update_quantum_board()
        self.capture_options = []
        self.finished = False
    
    def __repr__(self):
        """Display the board to the terminal, if wished."""
        answer = '\n'
        for i in range(len(self)):
            for j in range(len(self)):
                if (i+j)%2 == 0:
                    answer += '{}'.format(self.quantum_board[i][j])
                else:
                    answer += '-'
                answer += '\t'
            answer += '\n'
        return answer

    def __len__(self):
        return len(self.board_list[0])

    def quantum_split(self,x_pos,y_pos,user):
        if self.finished == True:
            return [Move.finish for i in range(len(self.board_list))]
        if self.capture_options != []:
            return [Move.capture_ignored for i in range(len(self.board_list))]

        quantum_ready = False

        for board in self.board_list:
            if board.quantum_move(x_pos,y_pos,user):
                quantum_ready = True
                break

        if quantum_ready:
            left_move = copy.deepcopy(self.board_list)
            right_move = copy.deepcopy(self.board_list)
            evaluation_table = []

            for board in left_move:
                response = board.move(x_pos,y_pos,-1,user,user)
                evaluation_table.append(response)
            
            for board in right_move:
                response = board.move(x_pos,y_pos,1,user,user)
                evaluation_table.append(response)
            
            if Move.success_opponents_turn in evaluation_table:
                self.board_list = left_move
                self.board_list.extend(right_move)
                
                self.remove_potential_collision(x_pos-1,y_pos+user)
                self.remove_potential_collision(x_pos+1,y_pos+user)
                self.update_quantum_board()

                return [Move.success_opponents_turn]
    
            self.update_quantum_board()
            return evaluation_table

        return [Move.quantum_not_ready]

    def move(self,x_pos,y_pos,x_dir,y_dir,user):
        if x_pos + x_dir not in range(len(self)) or y_pos + y_dir not in range(len(self)):
            return [Move.out_of_bounds for i in range(len(self.board_list))]
        if not self.__is_capture_move(user,x_pos,y_pos,x_dir,y_dir) and self.capture_options != []:
            return [Move.capture_ignored for i in range(len(self.board_list))]

        response = [board.move(x_pos,y_pos,x_dir,y_dir,user) for board in self.board_list]

        self.remove_potential_collision(x_pos+x_dir,y_pos+y_dir)
        self.update_quantum_board()

        return response
    
    def update_quantum_board(self):
        size = len(self.board_list[0])
        quantum_table = [[0 for row in range(size)] for column in range(size)]
        
        for board_instance in self.board_list:
            for row in range(size):
                for column in range(size):
                    quantum_value = quantum_table[row][column]
                    extra_value = board_instance.board[row][column]

                    # Remove any potential collisions. This should not happen.
                    if quantum_value * extra_value < 0:
                        raise ValueError("Caught unnoticed piece collision!")
                    
                    quantum_table[row][column] += 100*extra_value
        
        self.quantum_board = quantum_table
        for row in range(size):
            for column in range(size):
                self.quantum_board[row][column] = self.quantum_board[row][column] // len(self.board_list)
        
        self.__update_finished_condition()
        self.__load_capture_options()
        return self.quantum_board

    def remove_potential_collision(self,x_pos,y_pos):
        player1_found = False
        player2_found = False

        if x_pos not in range(len(self)) or y_pos not in range(len(self)):
            return

        for board in self.board_list:
            if board.board[y_pos][x_pos] == 1:
                if player2_found:
                    self.__remove_collision(x_pos,y_pos)
                    return
                player1_found = True

            if board.board[y_pos][x_pos] == -1:
                if player1_found:
                    self.__remove_collision(x_pos,y_pos)
                    return
                player2_found = True

    def __remove_collision(self,x_pos,y_pos):
        """Make a measurement on a given tile."""
        random_board = random.choice(self.board_list).board
        collision_measurement = random_board[y_pos][x_pos]
        
        self.board_list = [board for board in self.board_list if board.board[y_pos][x_pos] == collision_measurement]

    def __update_finished_condition(self):
        for board in self.board_list:
            if board.finished == False:
                self.finished = False
                return
        self.finished = True
        
    def __load_capture_options(self):
        self.capture_options = []
        for board_instance in self.board_list:
            for option in board_instance.capture_options:
                if option not in self.capture_options:
                    self.capture_options.append(option)

    def __is_capture_move(self,user,x_pos,y_pos,x_dir,y_dir):
        return CaptureOption(user,x_pos,y_pos,x_dir,y_dir) in self.capture_options                
