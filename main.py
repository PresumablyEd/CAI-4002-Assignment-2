# Main application for Tic Tac Toe game with AI

from game import Board
from ai import AIPlayer

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = 'X'
        self.game_mode = None
        self.ai_players = {}
        self.game_over = False
        
    def set_game_mode(self, mode):
        """Set the game mode (human_vs_human, human_vs_ai, ai_vs_ai)"""
        self.game_mode = mode
        
    def start_new_game(self):
        """Start a new game with reset board and state"""
        self.board.reset()
        self.current_player = 'X'
        self.game_over = False
        print("New game started!")
        
    def display_welcome(self):
        """Display welcome message and game modes"""
        print("=" * 50)
        print("           TIC TAC TOE GAME")
        print("=" * 50)
        print("\nSelect Game Mode:")
        print("1. Human vs Human")
        print("2. Human vs AI") 
        print("3. AI vs AI (Auto-play)")
        
    def get_human_move(self):
        """Get move from human player"""
        while True:
            try:
                move = input(f"Player {self.current_player}, enter your move (row,col) e.g. 1,2: ")
                row, col = map(int, move.split(','))
                if self.board.is_valid_move(row, col):
                    return row, col
                else:
                    print("Invalid move! Cell is occupied or out of bounds.")
            except (ValueError, IndexError):
                print("Invalid input! Please enter as 'row,col' e.g. 1,2")
                
    def display_game_state(self):
        """Display current game state"""
        print("\nCurrent Board:")
        self.board.display()
        
        winner = self.board.check_winner()
        if winner:
            if winner == 'Draw':
                print("Game ended in a draw!")
            else:
                print(f"Player {winner} wins!")
            self.game_over = True
        elif self.board.is_board_full():
            print("Game ended in a draw!")
            self.game_over = True
        else:
            print(f"\nCurrent turn: Player {self.current_player}")
            
    def switch_player(self):
        """Switch player from X to O or vice versa"""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        
    def play_human_vs_human(self):
        """Play Human vs Human mode"""
        print("\nHuman vs Human Mode")
        print("Player X goes first.")
        
        while not self.game_over:
            self.display_game_state()
            
            # Get move
            row, col = self.get_human_move()
            
            # Make the move
            self.board.make_move(row, col, self.current_player)
            
            # Check for game end and switch player
            self.switch_player()
            
        self.display_game_state()
        
    def play_human_vs_ai(self):
        """Play Human vs AI mode"""
        print("\nHuman vs AI Mode")
        print("Choose your options:")
        
        # Choose which algorithm to use for AI
        print("AI Algorithm Options:")
        print("1. Minimax")
        print("2. Alpha-Beta Pruning")
        
        while True:
            try:
                choice = int(input("Select AI algorithm (1 or 2): "))
                if choice == 1:
                    ai_algorithm = 'minimax'
                    break
                elif choice == 2:
                    ai_algorithm = 'alpha_beta'
                    break
                else:
                    print("Please select 1 or 2")
            except ValueError:
                print("Invalid input!")
                
        # Choose turn order
        while True:
            try:
                turn_choice = int(input("Choose turn (1 for Human first, 2 for AI first): "))
                if turn_choice == 1:
                    human_first = True
                    break
                elif turn_choice == 2:
                    human_first = False
                    break
                else:
                    print("Please select 1 or 2")
            except ValueError:
                print("Invalid input!")
                
        # Set up AI player
        ai_symbol = 'O' if human_first else 'X'
        self.ai_players['ai'] = AIPlayer(algorithm=ai_algorithm, player_symbol=ai_symbol)
        
        print(f"\nYou are Player {'X' if not human_first else 'O'}")
        print(f"AI uses {ai_algorithm} algorithm")
        
        # Set starting player
        self.current_player = 'X' if human_first else 'O'
        
        while not self.game_over:
            self.display_game_state()
            
            if self.current_player == ('X' if human_first else 'O'):
                # Human's turn
                row, col = self.get_human_move()
                self.board.make_move(row, col, self.current_player)
            else:
                # AI's turn
                print("\nAI is thinking...")
                ai_move = self.ai_players['ai'].get_move(self.board)
                if ai_move:
                    row, col = ai_move
                    self.board.make_move(row, col, self.current_player)
                    
                    # Display performance metrics
                    perf_metrics = self.ai_players['ai'].get_performance()
                    print(f"AI Decision Time: {perf_metrics['decision_time']} ms")
                    print(f"Nodes explored: {perf_metrics['nodes_explored']}")
                    if ai_algorithm == 'alpha_beta':
                        print(f"Pruning efficiency: {perf_metrics['pruning_efficiency']}%")
                
            # Switch player
            self.switch_player()
            
        self.display_game_state()
        
    def play_ai_vs_ai(self):
        """Play AI vs AI mode with auto-play"""
        print("\nAI vs AI Mode")
        
        # Choose algorithms for both AIs
        print("AI 1 Algorithm Options:")
        print("1. Minimax")
        print("2. Alpha-Beta Pruning")
        
        while True:
            try:
                choice = int(input("Select AI 1 algorithm (1 or 2): "))
                if choice == 1:
                    ai1_algorithm = 'minimax'
                    break
                elif choice == 2:
                    ai1_algorithm = 'alpha_beta'
                    break
                else:
                    print("Please select 1 or 2")
            except ValueError:
                print("Invalid input!")
                
        while True:
            try:
                choice = int(input("Select AI 2 algorithm (1 or 2): "))
                if choice == 1:
                    ai2_algorithm = 'minimax'
                    break
                elif choice == 2:
                    ai2_algorithm = 'alpha_beta'
                    break
                else:
                    print("Please select 1 or 2")
            except ValueError:
                print("Invalid input!")
                
        # Set up AI players 
        self.ai_players['ai1'] = AIPlayer(algorithm=ai1_algorithm, player_symbol='X')
        self.ai_players['ai2'] = AIPlayer(algorithm=ai2_algorithm, player_symbol='O')
        
        print(f"\nAI 1 (X) uses {ai1_algorithm}")
        print(f"AI 2 (O) uses {ai2_algorithm}")
        
        # Play game with auto-play
        step_count = 0
        
        while not self.game_over:
            self.display_game_state()
            
            if self.current_player == 'X':
                ai_player = self.ai_players['ai1']
                print("\nAI 1 is thinking...")
            else:
                ai_player = self.ai_players['ai2'] 
                print("\nAI 2 is thinking...")
                
            # Get AI move
            ai_move = ai_player.get_move(self.board)
            if ai_move:
                row, col = ai_move
                self.board.make_move(row, col, self.current_player)
                
                # Display performance metrics for this AI
                perf_metrics = ai_player.get_performance()
                print(f"Decision Time: {perf_metrics['decision_time']} ms")
                print(f"Nodes explored: {perf_metrics['nodes_explored']}")
                if ai_player.algorithm == 'alpha_beta':
                    print(f"Pruning efficiency: {perf_metrics['pruning_efficiency']}%")
                    
            # Pause for better visualization
            input("\nPress Enter to continue...")
            
            step_count += 1
            
            # Switch player
            self.switch_player()
            
        self.display_game_state()
        
    def run(self):
        """Run the main game loop"""
        while True:
            self.display_welcome()
            
            try:
                choice = int(input("\nSelect mode (1-3): "))
                
                if choice == 1:
                    self.set_game_mode('human_vs_human')
                    self.start_new_game()
                    self.play_human_vs_human()
                    
                elif choice == 2:
                    self.set_game_mode('human_vs_ai')
                    self.start_new_game()
                    self.play_human_vs_ai()
                    
                elif choice == 3:
                    self.set_game_mode('ai_vs_ai')
                    self.start_new_game()
                    self.play_ai_vs_ai()
                    
                else:
                    print("Invalid selection. Please choose 1, 2, or 3.")
                    continue
                    
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue
                
            # Ask if player wants to play again
            while True:
                play_again = input("\nWould you like to play another game? (y/n): ").lower()
                if play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    print("Thanks for playing!")
                    return
                else:
                    print("Please enter 'y' or 'n'")

if __name__ == "__main__":
    game = Game()
    game.run()
