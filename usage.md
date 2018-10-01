# Playing QCheckers

This guide will help you to understand how the functions and classes in this module work. The module is built to support Quantum Checkers, though the regular game of Checkers is supported under both the `Checkers` and the `QCheckers` class.

## **Introduction**
The usage is very simple. All you need to do, is to import the `Checkers` or `QCheckers` class from `game` and start the function.

    from game import Checkers
    
    game = Checkers()
    game.tstart()

The upper code is for playing a regular game of checkers, whereas the lower one is for playing a game of Quantum Checkers.

    from game import QCheckers

    game = QCheckers()
    game.tstart()

## **Jump**
[Checkers class](#Checkers)  
[QCheckers class](#QCheckers)  
[Other classes](#other)  
|---> [Board](#Board)  
|---> [QBoard](#QBoard)  
|---> [CaptureOption](#CaptureOption)  

# <a head="#Checkers"></a>Checkers(*size=10*, *population=3*)
The `Checkers` object stores and takes care of the rules of a game of checkers. The Checkers object stores only a few variables.

When creating an instance, the class has two parameters, **size** and **population**. The **size** parameter indicates the size of the board, while **population** indicates how many layers are filled with pieces for each player.

    game = Checkers(size=3,population=1)

    # Returns True
    game.environment.board == [[1,0,1],[0,0,0],[-1,0,-1]]

### ***Object*.environment**

This value contains a [Board](#Board) class that is manipulated to play a game.

### ***Object*.player_turn**

Integer that stores whose turn it is. The value is either 1 or -1, standing for player 1 or 2 respectively.

### ***Object*.tstart(*debug=False*)**

Start a game in the terminal. This allows the player to test the object in the terminal or to play a simple game.
The input isn't sanitized, so blind usage by a client is not to be trusted;

    x_position y_position x_direction y_direction # Move a piece

    => 0 0 1 1
    => 1 1 -1 1
    => 0 2 1 1
    => 1 3 1 1

A checkers board will be printed to the terminal.


# <a head="#QCheckers"></a>QCheckers(*size=10*, *population=3*)
The `QCheckers` object allows the user to play a game of Quantum Checkers. In theory, a regular game of checkers can be played on the QCheckers object, though it is recommended to use the regular Checkers class for that.

### ***Object*.environment**

This value contains a [QBoard](#QBoard) class, which is used to play a quantum game.

### ***Object*.player_turn**

Integer that stores whose turn it is. The value is either 1 or -1, standing for player 1 or 2 respectively.

### ***Object*.tstart(*debug=False*)**

Start a game in the terminal. This allows the player to test the object in the terminal or to play a simple game.
The input isn't sanitized, so blind usage by a client is not to be trusted;

    x_position y_position x_direction y_direction   # Move a piece
    Q x_position y_position                         # Make a quantum move

    => 0 0 1 1
    => Q 1 1
    => 0 2 1 1
    => 1 3 1 1
    => 2 2 1 1

A checkers board will be printed to the terminal.

# <a head="#other"></a>Internal objects

## <a head="#Board"></a>**Board(*size=10*, *population=3*)**
The `Board` object has a few values stored that can be accessed.

    game = Board()
    game = (size=3,population=1)

### ***Object*.board**

This variable stores the current game state in a grid. This is a list of lists.

### ***Object*.capture_options**

The given variable stores a list of **[CaptureOption](#CaptureOption)** objects. If the list is not empty, the user must make any of these options as their next move.

### ***Object*.move(*x_pos*, *y_pos*, *x_dir*, *y_dir*, *user*)**

This function moves a given piece for a given user. This function is sanitized, so incorrect values are allowed to be inserted.

    game = Board(size=3,population=1)
    game.move(0,0,1,1,1)                # => Move.succes_opponents_turn
    game.move(3,5,100,23,-1)            # => Move.out_of_bounds

### ***Object*.quantum_move(*x_pos*, *y_pos*, *user*)**

Function that returns **True** or **False** based on whether a piece is ready to make a quantum move.

### **Other (private) functions**
There are a few more functions that the class has, but these are internal commands that are only to be used on the inside of the class.
If it is needed to use these functions, however, then they are explained in the code. The functions are the following;

    Object.__move_single_tile(self,moving_piece,x_pos,y_pos,x_dir,y_dir,user)
    Object.__move_double_tile(self,moving_piece,x_pos,y_pos,x_dir,y_dir,user)
    Object.__victory_found()
    Object.__reached_end()
    Object.__on_the_board(x,y)
    Object.__valid_direction(x_direction,y_direction)
    Object.__is_capture_move(user,x_pos,y_pos,x_dir,y_dir)
    Object.__walks_backwards(user,direction)

## <a head="#QBoard"></a> **QBoard(*size=10*, *population=3*)**
The Quantum Checkers Board class has a few other variables to manage multiple co-existing checker games, but the input is the same. The **size** determines the board's size, while **population** indicates how many layers are filled with players.

### ***Object*.board_list**

This is a list of [Board](#Board) objects. All of these objects are possible playouts of the quantum checkers game.

### ***Object*.quantum_board**

This is a representation of the current quantum states the board is in. The board displays checker pieces, though the values are now between -100 and 100, representing their values.

### ***Object*.capture_options**

The given variable stores a list of **[CaptureOption](#CaptureOption)** objects. If the list is not empty, the user must make any of these options as their next move.

### ***Object*.finished**

This function stores whether the game has ended. It is a boolean.

### ***Object*.quantum_split(*x_pos*, *y_pos*, *user*)**

This function allows the player(, whose turn it is,) to make a quantum move, effectively causing the piece into a superposition on the next two tiles.

### ***Object*.move(*x_pos*, *y_pos*, *x_dir*, *y_dir*, *user*)**

Make a move. This is a standard move, though it is made sure that the move is made on all fields.

### ***Object*.remove_potential_collision(*x_pos*, *y_pos*)**

This function makes sure there are no collisions on the board. This should happen in any function built, as accepting pieces of both teams on one tile is against the rules. The function `*Object*.__remove_collision(x_pos,y_pos)`, but it is recommended to use this function; removing collisions can be a time-consuming task in more complicated scenarios, leaving it way more efficient to make sure first that whether there **is** a collision or not.

### ***Object*.update_quantum_board()**

Function that updates `Object.quantum_board`. This function is to be used when the quantum board is altered manually. If the object's functions are used, this function should triggered manually and can be ignored.

### **Other (private) functions**
There are a few more functions that the class has, but these are internal commands that are only to be used on the inside of the class.
If it is needed to use these functions, however, then they are explained in the code. The functions are the following;

    Object.__remove_collision(x_pos,y_pos)
    Object.__update_finished_condition()
    Object.__load_capture_options()
    Object.__is_capture_move(user,x_pos,y_pos,x_dir,y_dir)


## <a head="#CaptureOption"></a> **CaptureOption**
This object is mainly used on the background, but is still taken along in the documentation.

To begin, the object stores coordinates plus directions.

    Object.x_pos
    Object.y_pos
    Object.x_dir
    Object.y_dir
    Object.user

### ***Object*.still_valid(board)**

This function returns **True** or **False**. It indicates whether a given move is valid on a provided board.