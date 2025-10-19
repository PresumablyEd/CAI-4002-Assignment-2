"""
Backend implementation with Minimax and Alpha-Beta algorithms integrated from original AI implementation.
"""

from typing import List, Tuple, Dict, Optional

Board = List[str]  # 9-length list with 'X', 'O', or ' '

WIN_LINES = [
    (0,1,2), (3,4,5), (6,7,8),   # rows
    (0,3,6), (1,4,7), (2,5,8),   # cols
    (0,4,8), (2,4,6)             # diagonals
]

# Performance tracking variables
_nodes_explored = 0
_pruned_nodes = 0

# - Public API (used by the UI) 
def new_board() -> Board:
    """Return an empty 3x3 board as a 9-length list of spaces."""
    return [" "] * 9

def place(board: Board, idx: int, player: str) -> Board:
    """Place player's mark at idx and return the NEW board (do not mutate input)."""
    b = board.copy()
    b[idx] = player
    return b

def available_moves(board: Board):
    """Return list of empty cell indices."""
    return [i for i, v in enumerate(board) if v == " "]

def check_result(board: Board) -> Dict:
    """Return {'status': 'ongoing'|'draw'|'win', ...}."""
    for a,b,c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return {"status": "win", "winner": board[a], "line": (a,b,c)}
    if all(v != " " for v in board):
        return {"status": "draw"}
    return {"status": "ongoing"}

def check_winner_1d(board: Board) -> Optional[str]:
    """Check winner for 1D board format. Returns 'X', 'O', 'Draw', or None."""
    result = check_result(board)
    if result["status"] == "win":
        return result["winner"]
    elif result["status"] == "draw":
        return "Draw"
    return None

def minimax(board: Board, is_maximizing: bool, ai_player: str, human_player: str) -> Tuple[int, Optional[int]]:
    """
    Standard Minimax algorithm implementation for 1D board.
    Returns (score, best_move).
    """
    global _nodes_explored
    _nodes_explored += 1
    
    winner = check_winner_1d(board)
    
    # Base cases
    if winner == ai_player:
        return 10, None
    elif winner == human_player:
        return -10, None
    elif winner == 'Draw':
        return 0, None
    
    moves = available_moves(board)
    
    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for move in moves:
            board[move] = ai_player
            score, _ = minimax(board, False, ai_player, human_player)
            board[move] = " "
            
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for move in moves:
            board[move] = human_player
            score, _ = minimax(board, True, ai_player, human_player)
            board[move] = " "
            
            if score < best_score:
                best_score = score
                best_move = move
        return best_score, best_move

def alphabeta(board: Board, alpha: float, beta: float, is_maximizing: bool, ai_player: str, human_player: str) -> Tuple[int, Optional[int]]:
    """
    Alpha-Beta Pruning optimization of Minimax for 1D board.
    Returns (score, best_move).
    """
    global _nodes_explored, _pruned_nodes
    _nodes_explored += 1
    
    winner = check_winner_1d(board)
    
    # Base cases
    if winner == ai_player:
        return 10, None
    elif winner == human_player:
        return -10, None
    elif winner == 'Draw':
        return 0, None
    
    moves = available_moves(board)
    
    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for move in moves:
            board[move] = ai_player
            score, _ = alphabeta(board, alpha, beta, False, ai_player, human_player)
            board[move] = " "
            
            if score > best_score:
                best_score = score
                best_move = move
            
            # Alpha-Beta pruning
            alpha = max(alpha, best_score)
            if beta <= alpha:
                _pruned_nodes += 1
                break  # Prune the remaining branches
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for move in moves:
            board[move] = human_player
            score, _ = alphabeta(board, alpha, beta, True, ai_player, human_player)
            board[move] = " "
            
            if score < best_score:
                best_score = score
                best_move = move
                
            # Alpha-Beta pruning
            beta = min(beta, best_score)
            if beta <= alpha:
                _pruned_nodes += 1
                break  # Prune the remaining branches
        return best_score, best_move

def get_ai_move(board: Board, player: str, algo: str) -> Tuple[int, Dict]:
    """
    Get the best move for AI using the selected algorithm.
    Returns (move_index, metrics).
    """
    global _nodes_explored, _pruned_nodes
    
    # Reset performance tracking
    _nodes_explored = 0
    _pruned_nodes = 0
    
    # Determine players
    ai_player = player
    human_player = "O" if player == "X" else "X"
    
    # Check if board is full or game is over
    if check_winner_1d(board) is not None:
        return 0, {"nodes": 0, "pruned": 0, "prune_pct": 0.0}
    
    moves = available_moves(board)
    if not moves:
        return 0, {"nodes": 0, "pruned": 0, "prune_pct": 0.0}
    
    # Get best move using selected algorithm
    if algo == "Alpha-Beta":
        score, move = alphabeta(board, float('-inf'), float('inf'), True, ai_player, human_player)
        total_nodes = _nodes_explored
        pruned_count = _pruned_nodes
        prune_pct = (pruned_count / total_nodes * 100.0) if total_nodes > 0 else 0.0
        metrics = {
            "nodes": total_nodes,
            "pruned": pruned_count,
            "prune_pct": round(prune_pct, 2)
        }
    else:  # Minimax
        score, move = minimax(board, True, ai_player, human_player)
        metrics = {
            "nodes": _nodes_explored,
            "pruned": None,
            "prune_pct": None
        }
    
    # Fallback to first available move if no move found
    if move is None:
        move = moves[0]
    
    return move, metrics
