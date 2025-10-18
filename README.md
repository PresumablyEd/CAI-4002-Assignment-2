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

## Implementation Details

The game follows standard Tic Tac Toe rules where players take turns marking empty cells with their symbol ('X' or 'O'). The first player to align three symbols in a row wins. If the board fills without a winner, the game ends in a draw.

### Game State Management
- Board representation as 3x3 grid
- Turn tracking between players  
- Win/draw condition detection
- Move validation

### AI Implementation
Both algorithms use an evaluation function:
- Winning state: +10 (AI wins), -10 (opponent wins)
- Draw state: 0

## Requirements
- Python 3.x

## Running the Application
```
python main.py
```

## Project Structure
```
.
├── README.md
├── main.py              # Main application entry point  
├── game.py              # Core game logic and board management
├── ai.py                # AI algorithms (Minimax and Alpha-Beta)
└── utils.py             # Utility functions for performance tracking
