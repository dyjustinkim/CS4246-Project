import numpy as np

# Parameters can be changed
ROWS       = 6
COLUMNS    = 7
IN_A_ROW = 4

class Connect4Board:
    def __init__(self,  board=None, rows=ROWS, columns=COLUMNS):
        self.rows = rows
        self.columns = columns
        if board is not None:
            # If a board state is provided, directly use it to create the new instance
            self.board = np.copy(board)
        else:
            # If no board state is provided, initialize a new board with all positions empty
            self.board = np.full((rows, columns), '_', dtype=str)

    def display(self):
        print(self.board)

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
    
    def copy(self):
        return Connect4Board(board=self.board, rows=self.rows, columns=self.columns)

    def check_win(self, piece):
        '''
        Checks if there is a winning combination of 
        pieces in a row, based around the most
        recently dropped piece
        '''

        for num in range(4):
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
                if streak==IN_A_ROW:
                    return True
        return False
        

        


