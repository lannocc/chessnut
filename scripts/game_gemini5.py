import pygame
import sys

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

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.selected_piece = None
        self.possible_moves = []
        pygame.font.init()

    def handle_input(self, event):
        """Handles user input events (mouse clicks)."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_row = event.pos[1] // SQUARE_SIZE
            mouse_col = event.pos[0] // SQUARE_SIZE

            if self.selected_piece:
                # Try to move the selected piece
                if self.board.is_valid_move(self.selected_piece.row, self.selected_piece.col, mouse_row, mouse_col):
                    if self.board.move_piece(self.selected_piece.row, self.selected_piece.col, mouse_row, mouse_col):
                        self.selected_piece = None
                        self.possible_moves = [] # Clear Possible Moves after Piece Selection
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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()
    pygame.font.init() #Initialize Font
    game = Game(screen)
    game_over = False # Game Over Bool
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_input(event)

        if not game_over:
            game_over = game.update() # Only update the game if it's not over

        game.draw()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

