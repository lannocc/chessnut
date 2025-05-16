import pygame
import sys
import random
import argparse

# --- Constants ---
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
FPS = 60

# --- Colors ---
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT = (124, 252, 0)  # Light Green
POSSIBLE_MOVE = (173, 216, 230)  # Light Blue
PIECE_COLORS = {
    'white': (255, 255, 255),  # Pure white for pieces
    'black': (0, 0, 0)       # Pure black for pieces
}
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)

# --- Piece Definitions ---
PIECES = {
    'wp': 'wp', #Placeholder to reference in image loading.
    'wr': 'wr',
    'wn': 'wn',
    'wb': 'wb',
    'wq': 'wq',
    'wk': 'wk',
    'bp': 'bp',
    'br': 'br',
    'bn': 'bn',
    'bb': 'bb',
    'bq': 'bq',
    'bk': 'bk'
}


class Piece:
    def __init__(self, color, piece_type, row, col):
        self.color = color
        self.piece_type = piece_type
        self.row = row
        self.col = col
        self.image = self.create_piece_image()  # Create image
        self.rect = self.image.get_rect() #Creates a rect for piece.
        self.update_rect() #Updates Rect
        self.moved = False # Bool that indicates if the Piece has been moved before.

    def __repr__(self):
        return f"{self.color[0].upper()}{self.piece_type[0].upper()} ({self.row}, {self.col})"

    def update_rect(self):
        self.rect.topleft = (self.col * SQUARE_SIZE, self.row * SQUARE_SIZE)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.update_rect()
        self.moved = True

    def get_valid_moves(self, board):
        """Returns a list of valid move coordinates (row, col) for this piece,
        considering the board state."""
        moves = []
        if self.piece_type == 'pawn':
            moves = self.get_pawn_moves(board)
        elif self.piece_type == 'rook':
            moves = self.get_rook_moves(board)
        elif self.piece_type == 'knight':
            moves = self.get_knight_moves(board)
        elif self.piece_type == 'bishop':
            moves = self.get_bishop_moves(board)
        elif self.piece_type == 'queen':
            moves = self.get_queen_moves(board)
        elif self.piece_type == 'king':
            moves = self.get_king_moves(board)
        return moves
    def create_piece_image(self):
        """Generates a simple graphical representation of the piece."""
        image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)  # Transparent background
        color = PIECE_COLORS[self.color]
        pygame.draw.circle(image, color, (SQUARE_SIZE // 2, SQUARE_SIZE // 2), SQUARE_SIZE // 3)  # Circle
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.piece_type[0].upper(), True, (255-color[0], 255-color[1], 255-color[2]))  # Opposite color for text
        text_rect = text_surface.get_rect(center=(SQUARE_SIZE // 2, SQUARE_SIZE // 2))
        image.blit(text_surface, text_rect)
        return image


    def get_pawn_moves(self, board):
        moves = []
        direction = -1 if self.color == 'white' else 1 # Reversed Directions
        start_row = 6 if self.color == 'white' else 1

        # Move one square forward
        new_row = self.row + direction
        if 0 <= new_row < ROWS and board[new_row][self.col] is None:
            moves.append((new_row, self.col))

            # Move two squares forward from starting position
            if self.row == start_row and not self.moved and 0 <= new_row < ROWS and board[new_row][self.col] is None and 0 <= new_row + direction < ROWS and board[new_row + direction][self.col] is None:
                moves.append((new_row + direction, self.col))

        # Capture diagonally
        new_row = self.row + direction
        for col_offset in [-1, 1]:
            new_col = self.col + col_offset
            if 0 <= new_col < COLS and 0 <= new_row < ROWS: #Added row check.
                piece = board[new_row][new_col]
                if piece is not None and piece.color != self.color:
                    moves.append((new_row, new_col))

        return moves

    def get_rook_moves(self, board):
        moves = []
        # Directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            for i in range(1, ROWS):
                new_row, new_col = self.row + dr * i, self.col + dc * i
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    piece = board[new_row][new_col]
                    if piece is None:
                        moves.append((new_row, new_col))
                    elif piece.color != self.color:
                        moves.append((new_row, new_col))
                        break  # Stop after capturing
                    else:
                        break  # Blocked by own piece
                else:
                    break  # Out of bounds
        return moves

    def get_knight_moves(self, board):
        moves = []
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for dr, dc in knight_moves:
            new_row, new_col = self.row + dr, self.col + dc
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                piece = board[new_row][new_col]
                if piece is None or piece.color != self.color:
                    moves.append((new_row, new_col))
        return moves

    def get_bishop_moves(self, board):
        moves = []
        # Directions: up-left, up-right, down-left, down-right
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            for i in range(1, ROWS):
                new_row, new_col = self.row + dr * i, self.col + dc * i
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    piece = board[new_row][new_col]
                    if piece is None:
                        moves.append((new_row, new_col))
                    elif piece.color != self.color:
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return moves

    def get_queen_moves(self, board):
        # Queen moves are a combination of rook and bishop moves
        return self.get_rook_moves(board) + self.get_bishop_moves(board)

    def get_king_moves(self, board):
        moves = []
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dr, dc in king_moves:
            new_row, new_col = self.row + dr, self.col + dc
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                piece = board[new_row][new_col]
                if piece is None or piece.color != self.color:
                    moves.append((new_row, new_col))
        return moves


class Board:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)] # Represents the board
        self.setup_board()
        self.white_to_move = True

    def setup_board(self):
        # White pieces
        self.board[7][0] = Piece('white', 'rook', 7, 0)
        self.board[7][1] = Piece('white', 'knight', 7, 1)
        self.board[7][2] = Piece('white', 'bishop', 7, 2)
        self.board[7][3] = Piece('white', 'queen', 7, 3)
        self.board[7][4] = Piece('white', 'king', 7, 4)
        self.board[7][5] = Piece('white', 'bishop', 7, 5)
        self.board[7][6] = Piece('white', 'knight', 7, 6)
        self.board[7][7] = Piece('white', 'rook', 7, 7)
        for i in range(COLS):
            self.board[6][i] = Piece('white', 'pawn', 6, i)

        # Black pieces
        self.board[0][0] = Piece('black', 'rook', 0, 0)
        self.board[0][1] = Piece('black', 'knight', 0, 1)
        self.board[0][2] = Piece('black', 'bishop', 0, 2)
        self.board[0][3] = Piece('black', 'queen', 0, 3)
        self.board[0][4] = Piece('black', 'king', 0, 4)
        self.board[0][5] = Piece('black', 'bishop', 0, 5)
        self.board[0][6] = Piece('black', 'knight', 0, 6)
        self.board[0][7] = Piece('black', 'rook', 0, 7)
        for i in range(COLS):
            self.board[1][i] = Piece('black', 'pawn', 1, i)

    def draw(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                piece = self.board[row][col]
                if piece:
                    screen.blit(piece.image, piece.rect)

    def move_piece(self, start_row, start_col, end_row, end_col):
        """Moves a piece from start_row, start_col to end_row, end_col."""

        piece = self.board[start_row][start_col]
        if piece:
            # Update the board
            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = None  # Clear the old position

            # Update the piece's position
            piece.move(end_row, end_col)

            # Switch turns
            self.white_to_move = not self.white_to_move
            return True
        return False

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Checks if a move is valid based on the piece's movement rules and board state."""
        piece = self.board[start_row][start_col]
        if not piece:
            return False

        # Check turn
        if (piece.color == 'white' and not self.white_to_move) or \
           (piece.color == 'black' and self.white_to_move):
            return False

        # Check if the destination is within the valid moves for the piece
        valid_moves = piece.get_valid_moves(self.board)
        if (end_row, end_col) not in valid_moves:
            return False

        return True

    def get_piece(self, row, col):
        """Returns the piece at the specified row and column, or None if the square is empty."""
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        return None

    def check_win_condition(self):
        """Checks if any win conditions are met and returns the winning color or None"""
        white_king_alive = False
        black_king_alive = False
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    if piece.color == 'white' and piece.piece_type == 'king':
                        white_king_alive = True
                    if piece.color == 'black' and piece.piece_type == 'king':
                        black_king_alive = True

        if not white_king_alive:
            return 'black'
        if not black_king_alive:
            return 'white'
        return None # None if no win condition

    def is_game_over(self):
        """Returns True if the game is over (checkmate or stalemate), False otherwise."""
        return self.check_win_condition() is not None

    def get_all_pieces(self, color):
        """Returns a list of all pieces of a given color on the board."""
        pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    pieces.append(piece)
        return pieces

class AIPlayer:
    def __init__(self, color):
        self.color = color

    def get_best_move(self, board):
        """Returns the best move for the AI player based on a simple evaluation."""
        possible_moves = self.get_all_possible_moves(board)
        if not possible_moves:
            return None

        # Simple evaluation: choose a random valid move
        return random.choice(possible_moves)

    def get_all_possible_moves(self, board):
        """Returns a list of all possible moves for the AI player."""
        pieces = board.get_all_pieces(self.color)
        possible_moves = []
        for piece in pieces:
            valid_moves = piece.get_valid_moves(board.board)
            for move in valid_moves:
                possible_moves.append((piece.row, piece.col, move[0], move[1])) # start_row, start_col, end_row, end_col
        return possible_moves


class Game:
    def __init__(self, screen, num_players):
        self.screen = screen
        self.board = Board()
        self.selected_piece = None
        self.possible_moves = []
        pygame.font.init()
        self.num_players = num_players
        self.ai_player_white = AIPlayer('white') if num_players == 0 else None
        self.ai_player_black = AIPlayer('black') if num_players in [0, 1] else None  # AI plays as black or both
        self.game_over = False


    def handle_input(self, event):
        """Handles user input events (mouse clicks)."""
        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over and self.num_players > 0:
            mouse_row = event.pos[1] // SQUARE_SIZE
            mouse_col = event.pos[0] // SQUARE_SIZE

            if self.selected_piece:
                # Try to move the selected piece
                if self.board.is_valid_move(self.selected_piece.row, self.selected_piece.col, mouse_row, mouse_col):
                    if self.board.move_piece(self.selected_piece.row, self.selected_piece.col, mouse_row, mouse_col):
                        self.selected_piece = None
                        self.possible_moves = [] # Clear Possible Moves after Piece Selection
                        if self.num_players == 1 and not self.board.white_to_move and not self.game_over:
                            self.ai_move() # Trigger AI Move if required.
                else:
                    # Deselect the piece if the click is not a valid move
                    self.selected_piece = None
                    self.possible_moves = [] # Clear Possible Moves after Piece Selection
                    # Optionally, try selecting a new piece at the clicked square
                    piece = self.board.get_piece(mouse_row, mouse_col)
                    if piece and ((piece.color == 'white' and self.board.white_to_move) or (piece.color == 'black' and not self.board.white_to_move)):
                        self.selected_piece = piece
                        self.possible_moves = piece.get_valid_moves(self.board.board)
            else:
                # Select a piece
                piece = self.board.get_piece(mouse_row, mouse_col)
                if piece and ((piece.color == 'white' and self.board.white_to_move) or (piece.color == 'black' and not self.board.white_to_move)):
                    self.selected_piece = piece
                    self.possible_moves = piece.get_valid_moves(self.board.board)

    def update(self):
        """Updates the game state."""
        # Check for game over (win condition)
        winner = self.board.check_win_condition()
        if winner:
            print(f"{winner.capitalize()} wins!")
            self.game_over = True
            return True  # Game is over
        return False # Game is not over

    def draw(self):
        """Draws the game board and pieces to the screen."""
        self.board.draw(self.screen)

        # Highlight possible moves for the selected piece
        if self.selected_piece:
            for row, col in self.possible_moves:
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                s.set_alpha(128)  # Transparency value (0-255)
                s.fill(POSSIBLE_MOVE)
                self.screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            pygame.draw.rect(self.screen, HIGHLIGHT, self.selected_piece.rect, 3)  # Highlight Thickness of 3 Pixels.
        if self.game_over:
            self.draw_game_over()

    def ai_move(self):
        """Executes a move for the AI player."""
        if not self.game_over:
            if self.num_players == 0: # 0 Player, both AIs play
                if self.board.white_to_move:
                    ai_player = self.ai_player_white
                else:
                    ai_player = self.ai_player_black
            elif self.num_players == 1:  # 1 Player, Black AI plays
                ai_player = self.ai_player_black
            else:
                return  # No AI in 2-player mode

            if ai_player:
                move = ai_player.get_best_move(self.board)
                if move:
                    start_row, start_col, end_row, end_col = move
                    if self.board.move_piece(start_row, start_col, end_row, end_col):
                        print(f"AI ({ai_player.color}) made a move.")
                        self.update() #Check For Game Over.
                else:
                    print("AI has no possible moves.")
                    self.game_over = True # end the game because ai can't move

    def draw_game_over(self):
        """Draws the game over screen."""
        winner = self.board.check_win_condition()
        font = pygame.font.Font(None, 60)
        text = font.render(f"{winner.capitalize()} wins!", True, TEXT_COLOR)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.Font(None, 36)
        self.text_surface = self.font.render(text, True, TEXT_COLOR)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        """Draws the button on the screen."""
        current_color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        """Handles mouse click events for the button."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()

class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 72)
        self.title_text = self.font.render("Chess Game", True, TEXT_COLOR)
        self.title_rect = self.title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))

        button_width, button_height = 200, 50
        button_x = WIDTH // 2 - button_width // 2
        self.zero_player_button = Button(button_x, HEIGHT // 2 - 100, button_width, button_height,
                                        "0 Player", BUTTON_COLOR, BUTTON_HOVER_COLOR, self.start_zero_player)
        self.one_player_button = Button(button_x, HEIGHT // 2, button_width, button_height,
                                        "1 Player", BUTTON_COLOR, BUTTON_HOVER_COLOR, self.start_one_player)
        self.two_player_button = Button(button_x, HEIGHT // 2 + 100, button_width, button_height,
                                        "2 Players", BUTTON_COLOR, BUTTON_HOVER_COLOR, self.start_two_player)
        self.exit_button = Button(button_x, HEIGHT // 2 + 200, button_width, button_height,
                                 "Exit", BUTTON_COLOR, BUTTON_HOVER_COLOR, self.exit_game)

        self.start_game = False  # Flag to indicate game start
        self.num_players = 0  # Number of players selected

    def draw(self):
        """Draws the title screen."""
        self.screen.fill(WHITE)
        self.screen.blit(self.title_text, self.title_rect)
        self.zero_player_button.draw(self.screen)
        self.one_player_button.draw(self.screen)
        self.two_player_button.draw(self.screen)
        self.exit_button.draw(self.screen)

    def handle_input(self, event):
        """Handles user input events for the title screen."""
        self.zero_player_button.handle_event(event)
        self.one_player_button.handle_event(event)
        self.two_player_button.handle_event(event)
        self.exit_button.handle_event(event)

    def start_zero_player(self):
        """Starts a zero-player game."""
        self.start_game = True
        self.num_players = 0

    def start_one_player(self):
        """Starts a one-player game."""
        self.start_game = True
        self.num_players = 1

    def start_two_player(self):
        """Starts a two-player game."""
        self.start_game = True
        self.num_players = 2

    def exit_game(self):
        """Exits the game."""
        pygame.quit()
        sys.exit()



def main():
    parser = argparse.ArgumentParser(description="Chess Game with AI")
    parser.add_argument("--zero-player", action="store_true", help="Run the game in 0-player mode (AI vs AI)")
    args = parser.parse_args()


    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()
    pygame.font.init() #Initialize Font

    if args.zero_player:
        game = Game(screen, 0)  # Initialize game directly in 0-player mode
        in_title_screen = False
    else:
        # Title Screen Setup
        title_screen = TitleScreen(screen)
        in_title_screen = True
        game = None  # Initialize game to None



    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if in_title_screen:
                title_screen.handle_input(event)
                if title_screen.start_game:
                    game = Game(screen, title_screen.num_players)
                    in_title_screen = False
            elif game:
                game.handle_input(event)

        if in_title_screen:
            title_screen.draw()
        elif game:
            if not game.game_over:
                if game.num_players == 0: # 0 player Mode
                    game.ai_move()
                else:
                    game.update()


            game.draw()


        pygame.display.flip()

        if args.zero_player and game and game.game_over:  # Automatically exit 0-player mode after game over
            running = False


    pygame.quit()
    if args.zero_player:
         winner = game.board.check_win_condition()
         if winner == 'white':
             sys.exit(1)
         elif winner == 'black':
             sys.exit(2)
    sys.exit()

if __name__ == "__main__":
    main()

