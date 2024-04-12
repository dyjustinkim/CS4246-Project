import random, pickle
import numpy as np
from connect4 import Connect4Board 
from mcts import uct
from mcts import ITERMAX

COLUMNS = 7 # Assumes standard Connect 4

class QLearningAgent:
    def __init__(self, alpha=0.2, gamma=0.9, epsilon=0.7):
        self.Q = {}  # Q-table
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration probability

    def get_state_repr(self, board):
        return board.display().tostring() # keys of Q table is the board converted to string

    def choose_action(self, board):
        state = self.get_state_repr(board)
        if state not in self.Q:
            self.Q[state] = [0] * COLUMNS  # Initialize Q-values

        if random.random() < self.epsilon: 
            # Exploration: instead of playing a random move, play a move suggested by mcts
            best_move = uct(root_board = board, itermax = ITERMAX, player = 'x')
            return best_move

            #return random.choice(board.get_valid_moves()) 
        else:
            # Exploitation: play a move suggested by the Q function
            actions_rank = np.argsort(self.Q[state])
            for action in actions_rank:
                if action in board.get_valid_moves():
                    return action
             
    def update(self, prev_state, action, reward, next_state, player):
        prev_q_value = self.Q.get(prev_state, [0] * COLUMNS)[action]  # Get existing Q-value or initialize

        max_next_q = max(self.Q.get(next_state, [0] * COLUMNS))
        new_q_value = prev_q_value + self.alpha * (reward + self.gamma * max_next_q - prev_q_value)
        self.Q.setdefault(prev_state, [0] * COLUMNS)[action] = new_q_value  # Update Q-value in the agent's Q-table


def play_training_game_with_mcts(agent, n_games):
    wins = 0
    for _ in range(n_games):
        current_player = 'x'
        board = Connect4Board()

        while True:
            if current_player == 'x': # RL agent's turn
                prev_state = agent.get_state_repr(board)
                action = agent.choose_action(board)
                board.drop_piece(action, current_player)
                _, done = board.reward_and_done()

            else:
                best_move = uct(root_board = board, itermax = ITERMAX, player = current_player)
                board.drop_piece(best_move, current_player)
                reward, done = board.reward_and_done()

                next_state = agent.get_state_repr(board)

                # Update the corresponding agent
                agent.update(prev_state, action, reward, next_state, current_player)

            if done:
                if current_player == 'x':
                    wins += 1
                print(wins/(_+1))
                break  

            current_player = 'o' if current_player == 'x' else 'x'


# loading & saving agent every 1000 games
with open('saved_agent_mcts.pkl', 'rb') as f:
    agent = pickle.load(f)

play_training_game_with_mcts(agent, 1000)
print(agent.Q) 

with open('saved_agent_mcts.pkl', 'wb') as f:
    pickle.dump(agent, f)

