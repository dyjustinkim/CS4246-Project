import numpy as np

# Parameters can be changed
ROWS       = 6
COLUMNS    = 7
IN_A_ROW = 4

class Connect4Board:
    def __init__(self,  board=None, rows=ROWS, columns=COLUMNS):
        self.rows = rows
        self.columns = columns
        self.current_column, self.current_row = 0, 0 

        if board is not None:
            # If a board state is provided, directly use it to create the new instance
            self.board = np.copy(board)
        else:
            # If no board state is provided, initialize a new board with all positions empty
            self.board = np.full((rows, columns), '_', dtype=str)

    def display(self):
        print(self.board)
        return self.board

    def drop_piece(self, column, piece):
        '''
        Drops a piece into the lowest open spot in a column
        '''

        self.current_column = column
        self.current_row = self.rows - 1 # Keeps track of position of the most recently played piece
        for row in reversed(self.board):
            if row[column] == '_':
                row[column] = piece
                return
            self.current_row-=1
        

    def copy_drop_return(self, column, piece): # copies a board, then drops a piece, then returns the copied board
        copied = self.copy()
        copied.drop_piece(column, piece)
        return copied

    def check_move(self, column):
        '''
        Checks if there are any empty spaces/
        available moves left in a column
        '''
        if self.board[0][column] == '_':
            return True
        return False
    
    def is_full(self):
        ret = True
        for c in range(self.columns):
            if self.board[0][c] == '_':
                ret = False
                break
        return ret
    
    def get_valid_moves(self):
        valid_moves = []
        for c in range(self.columns):
            if self.check_move(c):
                valid_moves.append(c)
        return valid_moves

    def reward_and_done(self):
        """Provides reward and 'done' status after a move."""
        reward = 0

        done = self.check_win('x') or self.check_win('o') or self.is_full()

        if self.check_win('x', in_a_row = 2):  # Agent is 'x'
            reward += 500
            
        if self.check_win('o', in_a_row = 2):
            reward += -1000
        
        if self.check_win('x', in_a_row = 3):  # Agent is 'x'
            reward += 500000
            
        if self.check_win('o', in_a_row = 3):
            reward += -1000000

        if self.check_win('x'):  # Agent is 'x'
            #print('win')
            return 1e9, done  # Large positive reward for winning
            
        elif self.check_win('o'):
            #print('lose')
            return -1e9, done  # Large negative reward for losing
        
        elif self.is_full():
            return 0, done  # Neutral (or slightly negative) reward for a draw
        else:
            return reward, done  # Small positive reward to encourage continuing the game

    def copy(self):
        copy = Connect4Board(board=self.board, rows=self.rows, columns=self.columns)
        return copy

    def check_win(self, piece, in_a_row = IN_A_ROW):
        '''
        Checks if there is a winning combination of 
        pieces in a row, based around the most
        recently dropped piece
        '''

        for num in range(in_a_row):
            match num:
                # Checks for a horiz3ontal combination
                case 0:
                    array = self.board[self.current_row, :]

                # Checks vertically
                case 1:
                    array = self.board[:, self.current_column]

                # Checks diagonally from top left \
                case 2:
                    ofs = self.current_column - self.current_row
                    array = np.diagonal(self.board, offset=ofs)

                # Checks diagonally from top right /
                case 3:
                    ofs = (self.columns - 1 - self.current_column) - self.current_row
                    array = np.diagonal(np.flip(self.board, axis=1), offset=ofs)
            
            '''
            Counts if there is an interrupted streak
            of the indicated pieces in each alignment
            '''
            
            streak = 0
            for x in range(len(array)):
                if array[x] == piece:
                    streak+=1
                else:
                    streak=0
                if streak==in_a_row:
                    return True
        return False



