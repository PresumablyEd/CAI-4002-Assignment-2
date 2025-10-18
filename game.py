# Game logic for Tic Tac Toe implementation

class Board:
    def __init__(self):
        # Initialize empty 3x3 board
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.size = 3
        
    def display(self):
        """Display the current board state"""
        print("\n   0   1   2")
        for i in range(self.size):
            print(f"{i}  {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]}")
            if i < self.size - 1:
                print("  -----------")
    
    def is_valid_move(self, row, col):
        """Check if a move is valid (within bounds and cell is empty)"""
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == ' '
    
    def make_move(self, row, col, player):
        """Make a move on the board if it's valid"""
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False
    
    def undo_move(self, row, col):
        """Undo a move by clearing the cell"""
        if 0 <= row < self.size and 0 <= col < self.size:
            self.board[row][col] = ' '
    
    def check_winner(self):
        """Check if there's a winner or if it's a draw
        Returns: 'X' if X wins, 'O' if O wins, 'Draw' if no winner, None if game continues
        """
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        
        # Check for draw (board full)
        is_board_full = all(self.board[i][j] != ' ' for i in range(3) for j in range(3))
        if is_board_full:
            return 'Draw'
            
        return None  # Game continues
    
    def get_empty_cells(self):
        """Get list of empty cells as (row, col) tuples"""
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    empty_cells.append((i, j))
        return empty_cells
    
    def is_board_full(self):
        """Check if the board is full"""
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3))
    
    def reset(self):
        """Reset the board to initial state"""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
