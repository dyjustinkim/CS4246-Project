from connect4 import Connect4Board, IN_A_ROW
import numpy as np
import random

TERMINAL = 4

def minimax(first_player, board, maxturn=True, target=0, curr_player=None):
    next_turn = False if maxturn == True else False
    curr_player = first_player if target==0 else curr_player
    next_player = 'x' if curr_player == 'o' else 'o'

    if target == TERMINAL: # returns the scoring of the board after the specified depth of recursion is reached
        this_turn = False if maxturn == True else True
        return eval_board(first_player, board, this_turn)
    
    moves = {} # recursion through calling minimax to evaluate possible moves
    for col in range(board.columns):
        if board.check_move(col):
            b1 = board.copy_drop_return(col, curr_player)
            moves[col] = minimax(first_player, b1, next_turn, target+1, next_player)
    
    keys = list(moves.keys()) # finds the minimum or maximum score that can be attained from the moves
    if len(keys) == 0:
        return -100000 if maxturn==True else 100000
    index = keys[0]
    val = moves[index]
    for i in range(len(keys)):

        if maxturn:
            if moves[keys[i]]>val:
                index = keys[i]
                val = moves[index]
            if moves[keys[i]]==val:
                chance = random.randint(0, 1)
                if chance == 0:
                    index = keys[i]

        else:
            if moves[keys[i]]<val:
                index = keys[i]
                val = moves[index]
            if moves[keys[i]]==val:
                chance = random.randint(0, 1)
                if chance == 0:
                    index = keys[i]

    return moves[index] if target>0 else index

def streak_score(streak): # score function from placing pieces in a row
    match streak:
        case 0:
            return 0 
        case 1:
            return 0
        case 2:
            return 100
        case 3: 
            return 2000
        case 4:
            return 1000000
        case _:
            return 1000000

def eval_board(piece, board, maxturn, test=False):

    score = 0
    (my_coeff, other_coeff) = (1, 2) if maxturn == True else (2, 1) #gives higher priority to blocking enemy's 3-in-a-rows

    for arrangement in range(4):
        arrays = []

        match arrangement:
            case 0: #evaluates the rows
                for row in range(board.rows):
                    arrays.append(board.board[row, :])
                
            case 1: #evaluates the columns
                for column in range(board.columns):
                    arrays.append(board.board[:, column])
                
            case 2: #evaluates diagonal from top left \
                for diag in range(board.rows + board.columns - IN_A_ROW * 2 + 1):
                    ofs = -board.rows + IN_A_ROW + diag
                    arrays.append(np.diagonal(board.board, offset=ofs))
                
            case 3: #evaluates diagonal from top right /
                flip = np.flip(board.board, axis=1)
                for diag in range(board.rows + board.columns - IN_A_ROW * 2 + 1):
                    ofs = -board.rows + IN_A_ROW + diag
                    arrays.append(np.diagonal(flip, offset=ofs))
    
        for array in arrays: # calculates score based on amount of pieces in a slice, how many pieces are consecutive
            temp_score = 0 # as well as how many potential ways there are to connect 4 in a row from pieces
            my_pieces, my_potentials, my_streak = 0, 0, 0
            other_pieces, other_potentials, other_streak = 0, 0, 0

            for index in range(len(array)):
                curr = array[index]

                if curr == piece:           
                    my_pieces +=1 
                    my_potentials += 1
                    my_streak += 1
                    if other_pieces>0 and other_potentials>=IN_A_ROW:
                        temp_score -= other_coeff*(5*other_pieces + streak_score(other_streak)*2**(other_potentials-IN_A_ROW))
                    
                    other_pieces, other_potentials, other_streak = 0, 0, 0
                    
                elif curr != '_': # if the space is occupied by the other player's piece
                    other_pieces +=1 
                    other_potentials += 1
                    other_streak += 1
                    if my_pieces>0 and my_potentials>=IN_A_ROW:
                        temp_score += my_coeff*(5*my_pieces + streak_score(my_streak)*2**(my_potentials-IN_A_ROW))
                    
                    my_pieces, my_potentials, my_streak = 0, 0, 0
                    

                else: # if the space is blank
                    my_potentials+=1
                    other_potentials+=1


                if (index == len(array) - 1):
                    if(test == True):
                        print(my_pieces, my_potentials, my_streak, other_pieces, other_potentials, other_streak)
                    if my_pieces>0 and my_potentials>=IN_A_ROW:
                        temp_score += my_coeff*(5*my_pieces + streak_score(my_streak)*2**(my_potentials-IN_A_ROW))
                
                    elif other_pieces>0 and other_potentials>=IN_A_ROW:
                        temp_score -= other_coeff*(5*other_pieces + streak_score(other_streak)*2**(other_potentials-IN_A_ROW))
                        
                                                
            score += temp_score
            
            if test==True:
                print(array, temp_score)

    return score


def human_minimax_play_game(human_first=True):
    turn = 0
    b1 = Connect4Board()
    b1.display()
    turn = human_first
    while True:
        if turn == True:
            piece = 'x'
            player = "Human"
            while True:
                move = input("Human player move: ")
                if move == 'exit':
                    return
                try:
                    move = int(move)
                    if b1.check_move(move):
                        b1.drop_piece(move, piece)
                        break
                    else: 
                        print("Cannot insert piece there! Try again. ")
                except ValueError:
                    print("Enter valid column number!")
        else:
            piece = 'o'
            player = "AI"
            move = minimax('o', b1)
            print("AI player move: " + str(move))
            b1.drop_piece(move, piece)
    
        b1.display()
        if b1.check_win(piece):
            print("Player " + player + " wins!")
            return
        turn = False if turn == True else True
    
# human_minimax_play_game(True)