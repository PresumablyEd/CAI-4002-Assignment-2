# Tic Tac Toe Game with AI

A complete Tic Tac Toe implementation featuring two AI algorithms: Minimax and Alpha-Beta Pruning. The application supports three game modes:
1. Human vs Human
2. Human vs AI 
3. AI vs AI (Auto-play)

## Features

- **Game Modes**:
  - Human vs Human: Two players take turns on the same device
  - Human vs AI: Player competes against AI with algorithm selection
  - AI vs AI: Automated play with step-by-step visualization

- **AI Algorithms**:
  - Minimax Algorithm with standard evaluation function
  - Alpha-Beta Pruning optimization for improved performance
  
- **Performance Tracking**:
  - Decision time measurement (milliseconds)
  - Nodes explored counting
  - Pruning efficiency percentage for Alpha-Beta

- **Web Interface**:
  - Interactive Streamlit-based web application
  - Real-time game board with visual feedback
  - Performance metrics table
  - Algorithm selection controls

## Implementation Details

The game follows standard Tic Tac Toe rules where players take turns marking empty cells with their symbol ('X' or 'O'). The first player to align three symbols in a row wins. If the board fills without a winner, the game ends in a draw.

### Game State Management
- Board representation as 1D list (9 cells)
- Turn tracking between players  
- Win/draw condition detection
- Move validation

### AI Implementation
Both algorithms use an evaluation function:
- Winning state: +10 (AI wins), -10 (opponent wins)
- Draw state: 0

### Performance Metrics
- **Decision Time**: Time taken for AI to make a move (milliseconds)
- **Nodes Explored**: Total number of game tree nodes evaluated
- **Pruning Efficiency**: Percentage of nodes pruned by Alpha-Beta algorithm

## Requirements
- Python 3.x
- Streamlit
- Pandas

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Web Application (Recommended)
```bash
streamlit run streamlit_app.py
```
The application will open in your browser at `http://localhost:8501`

### Console Application
```bash
python main.py
```

## Project Structure
```
.
├── README.md
├── requirements.txt      # Python dependencies
├── streamlit_app.py      # Web application interface
├── ttt_backend.py        # Backend logic with AI algorithms
├── main.py              # Console application entry point  
├── game.py              # Core game logic and board management
├── ai.py                # Original AI algorithms (Minimax and Alpha-Beta)
└── utils.py             # Utility functions for performance tracking
```

## Usage

### Web Application
1. Run `streamlit run streamlit_app.py`
2. Select game mode from the sidebar
3. Choose AI algorithms for each player
4. Click on the board to make moves (Human vs Human/Human vs AI)
5. Use auto-play controls for AI vs AI mode

### Console Application
1. Run `python main.py`
2. Follow the on-screen prompts to select game mode
3. Enter moves as row,column coordinates (e.g., "1,2")

## Algorithm Comparison

| Algorithm | Nodes Explored | Pruning | Performance |
|-----------|----------------|---------|-------------|
| Minimax | All possible nodes | None | Baseline |
| Alpha-Beta | Reduced nodes | Yes | Faster |

The Alpha-Beta algorithm typically explores 30-50% fewer nodes than Minimax while producing identical results.
