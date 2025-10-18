import streamlit as st
import time
from typing import Dict, Optional
import ttt_backend as backend

st.set_page_config(page_title="Tic-Tac-Toe — Minimax vs Alpha-Beta", page_icon="🎮", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #f6f8fc;
        }

        /* Sidebar background and text color */
        [data-testid="stSidebar"] {
            background-color: #e3f2fd !important;
            color: #0d47a1 !important;
        }
        [data-testid="stSidebar"] * {
            color: #0d47a1 !important;
        }

        /* Make sidebar inputs readable */
        [data-testid="stSidebar"] .stSelectbox > div > div {
            background: #ffffff !important;
            border: 1px solid #90caf9 !important;
            border-radius: 10px !important;
            color: #0d47a1 !important;
        }

        [data-testid="stSidebar"] div[role="listbox"] {
            background: #ffffff !important;
            border: 1px solid #bbdefb !important;
            border-radius: 10px !important;
            color: #0d47a1 !important;
        }

        [data-testid="stSidebar"] div[role="option"]:hover,
        [data-testid="stSidebar"] div[role="option"][aria-selected="true"] {
            background: #e3f2fd !important;
            color: #0d47a1 !important;
        }

        [data-testid="stSidebar"] .stSlider label,
        [data-testid="stSidebar"] .stSlider span {
            color: #0d47a1 !important;
        }

        [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div {
            background: #dbeafe !important;
        }

        [data-testid="stSidebar"] .stSlider [role="slider"] {
            background: #ef5350 !important;
            box-shadow: 0 0 0 2px #ffcdd2 inset !important;
        }

        /* Base button style */
        .stButton>button {
            height: 80px !important;
            font-size: 28px !important;
            border-radius: 12px !important;
            border: 2px solid #e0e0e0 !important;
            background-color: #ffffff !important;
            color: #1a1a1a !important;
            transition: all 0.2s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #e3f2fd !important;
            border-color: #64b5f6 !important;
        }

        /* Winning highlight (type="primary") */
        .stButton>button[kind="primary"] {
            background-color: #ffeb3b !important;  /* gold */
            border-color: #fbc02d !important;
            color: #000000 !important;
            box-shadow: 0 0 6px rgba(255, 193, 7, 0.6);
        }

        .x-cell>button {
            color: #1976d2 !important;
            font-weight: bold !important;
        }
        .o-cell>button {
            color: #d32f2f !important;
            font-weight: bold !important;
        }

        .restart-btn>button {
            background-color: #42a5f5 !important;
            color: white !important;
            border: none !important;
            font-weight: bold !important;
            height: 50px !important;
            border-radius: 10px !important;
        }
        .restart-btn>button:hover {
            background-color: #1e88e5 !important;
        }
    </style>
""", unsafe_allow_html=True)


# - Helpers for session state 
def init_state():
    if "mode" not in st.session_state:
        st.session_state.mode = "Human vs AI"  # default
    if "algo_p1" not in st.session_state:
        st.session_state.algo_p1 = "Minimax"
    if "algo_p2" not in st.session_state:
        st.session_state.algo_p2 = "Alpha-Beta"
    if "human_plays" not in st.session_state:
        st.session_state.human_plays = "X"
    if "board" not in st.session_state:
        st.session_state.board = backend.new_board()
    if "current" not in st.session_state:
        st.session_state.current = "X"
    if "history" not in st.session_state:
        st.session_state.history = []  # list of dicts with move + metrics
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "autoplay" not in st.session_state:
        st.session_state.autoplay = False
    if "speed" not in st.session_state:
        st.session_state.speed = 0.4  # seconds

def soft_reset():
    st.session_state.board = backend.new_board()
    st.session_state.current = "X"
    st.session_state.history = []
    st.session_state.game_over = False
    st.session_state.autoplay = False

init_state()

# - Sidebar controls
with st.sidebar:
    st.markdown("## ⚙️ Controls")
    st.session_state.mode = st.selectbox(
        "Game mode",
        ["Human vs Human", "Human vs AI", "AI vs AI"],
        index=["Human vs Human","Human vs AI","AI vs AI"].index(st.session_state.mode)
    )
    st.session_state.algo_p1 = st.selectbox("Algorithm for X", ["Minimax", "Alpha-Beta"], index=0)
    st.session_state.algo_p2 = st.selectbox("Algorithm for O", ["Minimax", "Alpha-Beta"], index=1)
    st.session_state.human_plays = st.selectbox("Human plays as", ["X", "O"], index=0)
    st.session_state.speed = st.slider("AI auto-play speed (sec/move)", 0.1, 2.0, st.session_state.speed, 0.1)


st.markdown("""
<div style="text-align: center;">
    <h1 style="margin-bottom: 0;">❌Tic-Tac-Toe⭕</h1>
    <h3 style="margin-top: 5px; color: #0d47a1;">Minimax vs Alpha-Beta</h3>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1.6])
with c1:
    st.markdown(f"**Mode:** {st.session_state.mode}")
with c2:
    st.markdown(f"**Turn:** {'—' if st.session_state.game_over else st.session_state.current}")
with c3:
    st.markdown(
        f"""<div style="text-align:right;">
            <strong>Algorithms —</strong>
            <span style="white-space:nowrap">X: {st.session_state.algo_p1}</span>
            |
            <span style="white-space:nowrap">O: {st.session_state.algo_p2}</span>
        </div>""",
        unsafe_allow_html=True
    )

# - Core helpers
def algo_for(player: str) -> str:
    return st.session_state.algo_p1 if player == "X" else st.session_state.algo_p2

def is_human_turn() -> bool:
    mode = st.session_state.mode
    curr = st.session_state.current
    if mode == "Human vs Human":
        return True
    if mode == "Human vs AI":
        return st.session_state.human_plays == curr
    return False  # AI vs AI

def apply_ai_if_needed():
    if st.session_state.game_over:
        return
    while (not is_human_turn()) and (not st.session_state.game_over):
        player = st.session_state.current
        algo = algo_for(player)
        start = time.perf_counter()
        move, metrics = backend.get_ai_move(st.session_state.board, player, algo)
        elapsed = (time.perf_counter() - start) * 1000.0  # ms
        metrics = metrics or {}
        metrics.setdefault("decision_time_ms", round(elapsed, 3))
        make_move(move, player, algo, metrics)
        if st.session_state.mode == "AI vs AI":
            time.sleep(st.session_state.speed)
        else:
            break

def make_move(idx: int, player: str, algo_used: Optional[str]=None, metrics: Optional[Dict]=None):
    if st.session_state.board[idx] != " " or st.session_state.game_over:
        return
    st.session_state.board = backend.place(st.session_state.board, idx, player)
    result = backend.check_result(st.session_state.board)
    st.session_state.history.append({
        "move_index": idx,
        "player": player,
        "algo": algo_used if algo_used else "Human",
        "decision_time_ms": (metrics or {}).get("decision_time_ms"),
        "nodes": (metrics or {}).get("nodes"),
        "pruned": (metrics or {}).get("pruned"),
        "prune_pct": (metrics or {}).get("prune_pct"),
    })
    if result["status"] != "ongoing":
        st.session_state.game_over = True
    else:
        st.session_state.current = "O" if player == "X" else "X"

# - Board UI (highlight winning cells)
def render_cell(i: int, winning_cells=None):
    mark = st.session_state.board[i]
    disabled = (mark != " ") or st.session_state.game_over or (not is_human_turn())
    highlight = bool(winning_cells) and (i in winning_cells)

    btn = st.button(
        mark if mark != " " else " ",
        key=f"cell_{i}",
        use_container_width=True,
        disabled=disabled,
        type="primary" if highlight else "secondary",
    )
    if btn and is_human_turn():
        make_move(i, st.session_state.current)
        st.experimental_rerun()

# determine winning cells
_result_for_highlight = backend.check_result(st.session_state.board)
_winning_cells = set(_result_for_highlight["line"]) if _result_for_highlight["status"] == "win" else None

board_cols = st.columns(3, gap="small")
for r in range(3):
    with board_cols[0]:
        render_cell(3*r + 0, _winning_cells)
    with board_cols[1]:
        render_cell(3*r + 1, _winning_cells)
    with board_cols[2]:
        render_cell(3*r + 2, _winning_cells)

# Restart button
center = st.columns([1, 1, 1])
with center[1]:
    with st.container():
        st.markdown('<div class="restart-btn">', unsafe_allow_html=True)
        if st.button("🔄 Restart", use_container_width=True, key="restart"):
            soft_reset()
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Draw status
result = backend.check_result(st.session_state.board)
status = result["status"]
if status == "win":
    st.success(f"✅ {result['winner']} wins!")
elif status == "draw":
    st.info("🤝 It's a draw.")

# Performance table
if st.session_state.history:
    import pandas as pd
    df = pd.DataFrame(st.session_state.history)
    st.subheader("📊 Performance per move")
    st.dataframe(df, use_container_width=True)

# Autoplay (AI vs AI)
if st.session_state.mode == "AI vs AI" and not st.session_state.game_over:
    c4, c5 = st.columns(2)
    with c4:
        if st.button("▶️ Start Auto-Play") and not st.session_state.autoplay:
            st.session_state.autoplay = True
    with c5:
        if st.button("⏹ Stop Auto-Play") and st.session_state.autoplay:
            st.session_state.autoplay = False

    if st.session_state.autoplay:
        apply_ai_if_needed()
        st.experimental_rerun()

# Auto-move for AI
if (st.session_state.mode == "Human vs AI") and (not st.session_state.game_over):
    apply_ai_if_needed()
