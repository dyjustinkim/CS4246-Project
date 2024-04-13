from connect4 import Connect4Board, COLUMNS

import random
import math

ITERMAX = 2000

class Node:
    def __init__(self, board, parent=None, move=None, player='x'):
        self.board = board
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_cols = []
        for col in range(COLUMNS):
            if board.check_move(col):
                self.untried_cols.append(col)
        self.player = player
        self.next_player = 'o' if player == 'x' else 'x'

    def uct_select_child(self):
        # UCT formula
        log_parent_visits = math.log(self.visits)
        C = math.sqrt(2)
        return max(self.children, key=lambda child: child.wins / child.visits + C * math.sqrt(log_parent_visits / child.visits))

    def add_child(self, new_col, state):
        new_node = Node(board = state, parent=self, move=new_col, player=self.next_player)
        self.untried_cols.remove(new_col)
        self.children.append(new_node)
        return new_node

    def update(self, winner):
        self.visits += 1
        if self.player == winner:
            self.wins += 1



def uct(root_board, itermax, player):
    rootnode = Node(board=root_board, player=player)

    for _ in range(itermax):
        node = rootnode
        curr_board_state = root_board.copy()
        current_player = player

        # Selection
        while node.untried_cols == [] and node.children != []:
            # DFS into the deepest leaf node
            # The loop continues until it finds a node that either can be expanded (i.e., has untried moves) or is a terminal node with no children.
            node = node.uct_select_child()
            curr_board_state.drop_piece(node.move, node.player)

        # Expansion
        if node.untried_cols:
            new_col = random.choice(node.untried_cols)
            curr_board_state.drop_piece(new_col, node.next_player)
            node = node.add_child(new_col, curr_board_state)

        # Simulation
        current_player = node.next_player
        while not curr_board_state.is_full():
            possible_moves = []
            for col in range(COLUMNS):
                if curr_board_state.check_move(col):
                    possible_moves.append(col)
            if not possible_moves or curr_board_state.check_win('x') or curr_board_state.check_win('o'):
                break
            new_col = random.choice(possible_moves)
            curr_board_state.drop_piece(new_col, current_player)
            current_player = 'o' if current_player == 'x' else 'x'

        # Backpropagation
        while node is not None: 
            winner = None
            if curr_board_state.check_win('x'):
                winner = 'x'
            elif curr_board_state.check_win('o'):
                winner = 'o'
            node.update(winner)
            node = node.parent

    # Return the move that was most visited
    return sorted(rootnode.children, key=lambda c: c.visits)[-1].move

def two_mcts_agents_play_game():
    board = Connect4Board()
    current_player = 'x'
    
    while True:
        print(f"Player {current_player}'s turn")

        best_move = uct(root_board = board, itermax = ITERMAX, player = current_player)
        
        board.drop_piece(best_move, current_player)
        
        board.display()
        if board.check_win(current_player):
            print(f"Player {current_player} wins!")
            break
        
        if board.is_full():
            print("The game is a draw!")
            break
        
        current_player = 'o' if current_player == 'x' else 'x'

def human_mcts_play_game():
    board = Connect4Board()
    current_player = 'x'
    board.display()
    while True:
        print(f"Player {current_player}'s turn")
        if (current_player == 'x'):
            move = input("Human move: ")
            if move == 'exit':
                return
            try:
                move = int(move)
                if board.check_move(move):
                    board.drop_piece(move, current_player)
                else: 
                    print("Cannot insert piece there! Try again. ")
            except ValueError:
                print("Enter valid column number!")
        else:
            best_move = uct(root_board = board, itermax = ITERMAX, player = current_player)
            board.drop_piece(best_move, current_player)
        
        board.display()
        if board.check_win(current_player):
            print(f"Player {current_player} wins!")
            break
        
        if board.is_full():
            print("The game is a draw!")
            break
        
        current_player = 'o' if current_player == 'x' else 'x'

def random_move(board):
    loop = True
    while loop:
        move = random.randint(0, (board.columns - 1))
        if board.check_move(move) == True:
           return move

def mcts_vs_random(first):
    board = Connect4Board()
    current_player = 'x'
    curr_algo = first
    while True:
        if curr_algo == 'mcts':
            move = uct(root_board = board, itermax = ITERMAX, player = current_player)
        else:
            move = random_move(board)
        board.drop_piece(move, current_player)
        
        if board.check_win(current_player) == True:
            board.display()
            return(curr_algo)
        
        if board.is_full() == True:
            board.display()
            return
        
        current_player = 'o' if current_player == 'x' else 'x'
        curr_algo = 'rand' if curr_algo == 'mcts' else 'mcts'

def test_winrates_random(games): #test mcts winrates in specified matches between minimax and mcts
    mcts_wins = 0
    algo = "mcts"
    for g in range(games):
        print("first turn algo: " + algo)
        winner = mcts_vs_random(algo)
        if winner == 'rand':
            print("rand win")
        elif winner == 'mcts':
            mcts_wins += 1
            print('mcts win')
        else: 
            print('draw')
        algo = "rand" if algo == "mcts" else "mcts"
    print("mcts winrate: " + str(float(mcts_wins)/games))

# human_mcts_play_game()

# Tune MCTS with different values of ITERMAX and C (in uct.select_child)
# Decide the best parameters of ITERMAX and C

#test_winrates_random(5)