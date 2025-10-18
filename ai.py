# AI algorithms for Tic Tac Toe: Minimax and Alpha-Beta Pruning

import time
from utils import PerformanceTracker

class AIPlayer:
    def __init__(self, algorithm='minimax', player_symbol='O'):
        self.algorithm = algorithm
        self.player_symbol = player_symbol
        if player_symbol == 'X':
            self.opponent_symbol = 'O'
        else:
            self.opponent_symbol = 'X'
        self.performance_tracker = PerformanceTracker()
    
    def get_move(self, board):
        """Get the best move for the AI using the selected algorithm"""
        # Reset performance tracking
        self.performance_tracker.reset()
        
        start_time = time.time() 
        
        if self.algorithm == 'minimax':
            score, move = self.minimax(board, True)
        elif self.algorithm == 'alpha_beta':
            score, move = self.alpha_beta(board, float('-inf'), float('inf'), True)
        else:
            raise ValueError("Invalid algorithm. Choose 'minimax' or 'alpha_beta'")
        
        end_time = time.time()
        decision_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Update performance metrics
        self.performance_tracker.update_performance(decision_time, 
                                                   self.performance_tracker.nodes_explored)
        
        return move
    
    def minimax(self, board, is_maximizing):
        """Standard Minimax algorithm implementation"""
        winner = board.check_winner()
        
        # Base cases
        if winner == self.player_symbol:
            return 10, None
        elif winner == self.opponent_symbol:
            return -10, None
        elif winner == 'Draw':
            return 0, None
            
        self.performance_tracker.increment_nodes_explored()  # Count nodes explored
        
        if is_maximizing:
            best_score = float('-inf')
            best_move = None
            for row, col in board.get_empty_cells():
                board.make_move(row, col, self.player_symbol)
                score, _ = self.minimax(board, False)
                board.undo_move(row, col)
                
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for row, col in board.get_empty_cells():
                board.make_move(row, col, self.opponent_symbol)
                score, _ = self.minimax(board, True)
                board.undo_move(row, col)
                
                if score < best_score:
                    best_score = score
                    best_move = (row, col)
            return best_score, best_move
    
    def alpha_beta(self, board, alpha, beta, is_maximizing):
        """Alpha-Beta Pruning optimization of Minimax"""
        winner = board.check_winner()
        
        # Base cases
        if winner == self.player_symbol:
            return 10, None
        elif winner == self.opponent_symbol:
            return -10, None
        elif winner == 'Draw':
            return 0, None
            
        self.performance_tracker.increment_nodes_explored()  # Count nodes explored
        
        if is_maximizing:
            best_score = float('-inf')
            best_move = None
            for row, col in board.get_empty_cells():
                board.make_move(row, col, self.player_symbol)
                score, _ = self.alpha_beta(board, alpha, beta, False)
                board.undo_move(row, col)
                
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
                
                # Alpha-Beta pruning
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    self.performance_tracker.increment_pruned_nodes()
                    break  # Prune the remaining branches
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for row, col in board.get_empty_cells():
                board.make_move(row, col, self.opponent_symbol)
                score, _ = self.alpha_beta(board, alpha, beta, True)
                board.undo_move(row, col)
                
                if score < best_score:
                    best_score = score
                    best_move = (row, col)
                    
                # Alpha-Beta pruning
                beta = min(beta, best_score)
                if beta <= alpha:
                    self.performance_tracker.increment_pruned_nodes()
                    break  # Prune the remaining branches
            return best_score, best_move

    def get_performance(self):
        """Get current performance metrics"""
        return self.performance_tracker.get_metrics()
