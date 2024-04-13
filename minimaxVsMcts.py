from connect4 import Connect4Board
import mcts
import minimax
import math

ITERMAX = 1000
CONST_C = math.sqrt(2)

controls_central = 0

def minimax_vs_mcts(first):
    board = Connect4Board()
    current_player = 'x'
    curr_algo = first
    isFirstMove = True
    global controls_central
    while True:
        if curr_algo == 'mcts':
            move = mcts.uct(root_board = board, itermax = ITERMAX, player = current_player, const_c = CONST_C)
        else:
            move = minimax.minimax(current_player, board)
        board.drop_piece(move, current_player)
        if isFirstMove:
            if move == 3:
                controls_central += 1
            isFirstMove = False
        
        if board.check_win(current_player) == True:
            board.display()
            return(curr_algo)
        
        if board.is_full() == True:
            board.display()
            return
        
        current_player = 'o' if current_player == 'x' else 'x'
        curr_algo = 'mm' if curr_algo == 'mcts' else 'mcts'

def test_winrates(games, first_algo): #test mcts winrates in specified matches between minimax and mcts
    mcts_wins = 0
    mm_wins = 0
    algo = first_algo
    for g in range(games):
        print("first turn algo: " + algo)
        winner = minimax_vs_mcts(algo)
        if winner == 'mm':
            mm_wins += 1
            print("mm win")
        elif winner == 'mcts':
            mcts_wins += 1
            print('mcts win')
        else: 
            print('draw')
        algo = first_algo
    print("mcts winrate: " + str(float(mcts_wins)/games))
    print("mcts wins: " + str(mcts_wins))
    print("mm wins: " + str(mm_wins))
    print("controls central: " + str(controls_central))

test_winrates(50, 'mm')