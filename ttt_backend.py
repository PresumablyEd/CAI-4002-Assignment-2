"""
Backend template.

To do: implement Minimax and Alpha-Beta.
Keep these public function names/signatures the same so the UI doesn't need changes.
"""

from typing import List, Tuple, Dict, Optional

Board = List[str]  # 9-length list with 'X', 'O', or ' '

WIN_LINES = [
    (0,1,2), (3,4,5), (6,7,8),   # rows
    (0,3,6), (1,4,7), (2,5,8),   # cols
    (0,4,8), (2,4,6)             # diagonals
]

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

def get_ai_move(board: Board, player: str, algo: str) -> Tuple[int, Dict]:
    """
    TEMPORARY placeholder to let the UI run without the real algorithms.

    Returns:
      (move_index, metrics)
    where metrics is a dict the UI can display. Your teammate will later fill
    nodes/pruning stats from their actual search.
    """
    # - placeholder: pick the first available cell 
    moves = available_moves(board)
    move_index = moves[0] if moves else 0

    # Minimal metrics structure the UI expects.
    metrics = {
        "nodes": None,         # to be filled by real Minimax/Alpha-Beta
        "pruned": None,        # Alpha-Beta only (later)
        "prune_pct": None,     # Alpha-Beta only (later)
        # UI auto-fills 'decision_time_ms'
    }
    return move_index, metrics

# ---------- TODO  ----------
# They should implement these and wire them inside get_ai_move().
#
# def minimax(board: Board, player: str, ai: str, opp: str) -> Tuple[int, int]:
#     """Return (best_move, nodes_explored)."""
#     ...
#
# def alphabeta(board: Board, player: str, ai: str, opp: str) -> Tuple[int, int, int]:
#     """Return (best_move, nodes_explored, pruned_count)."""
#     ...
#
# def get_ai_move(board: Board, player: str, algo: str) -> Tuple[int, Dict]:
#     ai, opp = player, ("O" if player == "X" else "X")
#     if algo == "Alpha-Beta":
#         move, nodes, pruned = alphabeta(board, player, ai, opp)
#         total = (nodes or 0) + (pruned or 0)
#         prune_pct = (pruned / total * 100.0) if total else None
#         return move, {"nodes": nodes, "pruned": pruned, "prune_pct": prune_pct}
#     else:
#         move, nodes = minimax(board, player, ai, opp)
#         return move, {"nodes": nodes, "pruned": None, "prune_pct": None}
