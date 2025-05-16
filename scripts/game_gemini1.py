import pygame
from sys import exit

class ChessPiece:
    def __init__(self, color, piece_type):
        self.color = color
        self.type = piece_type

    def __repr__(self):  # Add for debugging
        return f"{self.color} {self.type}"

    def get_type(self):
        return self.type

class ChessGame:
    def __init__(self, board_size=8, square_size=80):  # Slightly smaller squares
        pygame.init()
        self.board_size = board_size
        self.sq_size = square_size
        self.screen_width = board_size * square_size
        self.screen_height = board_size * square_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Chess Game")
        self.board = [[None for _ in range(board_size)] for __ in range(board_size)] # Changed to None
        self.selected_piece = None
        self.selected_piece_pos = None # Keep track of selected piece position
        self.current_player = 'white'
        self.game_mode = '2player'
        self.possible_moves = {} # store possible moves (row,col)
        self.setup_board()

    def setup_board(self):
        # Pawns
        for i in range(self.board_size):
            self.board[1][i] = Pawn('black')
            self.board[self.board_size - 2][i] = Pawn('white')

        # Rooks
        self.board[0][0] = Rook('black')
        self.board[0][7] = Rook('black')
        self.board[self.board_size - 1][0] = Rook('white')
        self.board[self.board_size - 1][7] = Rook('white')

        # Knights
        self.board[0][1] = Knight('black')
        self.board[0][6] = Knight('black')
        self.board[self.board_size - 1][1] = Knight('white')
        self.board[self.board_size - 1][6] = Knight('white')

        # Bishops
        self.board[0][2] = Bishop('black')
        self.board[0][5] = Bishop('black')
        self.board[self.board_size - 1][2] = Bishop('white')
        self.board[self.board_size - 1][5] = Bishop('white')

        # Queens
        self.board[0][3] = Queen('black')
        self.board[self.board_size - 1][3] = Queen('white')

        # Kings (Not implemented, add kings)
        #self.board[0][4] = King('black')  # Example (replace with King class)
        #self.board[self.board_size - 1][4] = King('white') # Example


    def draw_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = 'white' if (row + col) % 2 == 0 else 'gray'  # Use gray
                rect = pygame.Rect(col * self.sq_size, row * self.sq_size, self.sq_size, self.sq_size)
                pygame.draw.rect(self.screen, color, rect)

                # Highlight possible moves
                if self.selected_piece and (row, col) in self.possible_moves:
                    pygame.draw.rect(self.screen, 'green', rect, 3) # Green border

                piece = self.board[row][col]
                if piece:
                    piece_color = (0,0,0) if piece.color == 'black' else (255,0,0) # Black or red
                    text_surface = pygame.font.SysFont(None, 30).render(piece.type[:1], True, piece_color)
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.screen.blit(text_surface, text_rect)

    def get_possible_moves(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return []

        if piece.type == 'Knight':
            return Knight.get_valid_moves(piece, row, col, self.board, self.board_size)
        elif piece.type == 'Bishop':
            return Bishop.get_valid_moves(piece, row, col, self.board, self.board_size)
        elif piece.type == 'Rook':
            return Rook.get_valid_moves(piece, row, col, self.board, self.board_size)
        elif piece.type == 'Queen':
            return Queen.get_valid_moves(piece, row, col, self.board, self.board_size)
        elif piece.type == 'Pawn':
            return Pawn.get_valid_moves(piece, row, col, self.board, self.board_size)
        else:
            return []

    def is_valid_move(self, from_row, from_col, to_row, to_col):
        possible_moves = self.get_possible_moves(from_row, from_col)
        return (to_row, to_col) in possible_moves

    def make_move(self, from_row, from_col, to_row, to_col):
        piece = self.board[from_row][from_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None # Clear the original position
        self.toggle_player_turn()
        self.selected_piece = None
        self.selected_piece_pos = None
        self.possible_moves = {}  # Clear possible moves

    def handle_click(self, pos):
        col = pos[0] // self.sq_size
        row = pos[1] // self.sq_size

        clicked_piece = self.board[row][col]

        if self.selected_piece:
            # A piece is already selected, try to move it

            if self.is_valid_move(self.selected_piece_pos[0], self.selected_piece_pos[1], row, col):
                self.make_move(self.selected_piece_pos[0], self.selected_piece_pos[1], row, col)
                return # End turn and reset selections

            else:
                # Invalid move, deselect the piece
                self.selected_piece = None
                self.selected_piece_pos = None
                self.possible_moves = {}
                if clicked_piece and clicked_piece.color == self.current_player:
                    #Select the new piece if it's the right color
                    self.select_piece(row, col)
        elif clicked_piece and clicked_piece.color == self.current_player:
            # No piece selected, select one if it belongs to the current player
            self.select_piece(row, col)

    def select_piece(self, row, col):
        self.selected_piece = self.board[row][col]
        self.selected_piece_pos = (row, col)
        self.possible_moves = self.get_possible_moves(row, col)

    def get_square_color(self, row, col):
        return 'black' if (row + col) % 2 else 'white'

    def toggle_player_turn(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'


class Knight(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'Knight')

    @staticmethod
    def get_valid_moves(piece, row, col, board, board_size):  # Staticmethod
        valid = []
        moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < board_size and 0 <= new_col < board_size:
                target_piece = board[new_row][new_col]
                if target_piece is None or target_piece.color != piece.color:  # Changed logic
                    valid.append((new_row, new_col))
        return valid

class Bishop(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'Bishop')

    @staticmethod
    def get_valid_moves(piece, row, col, board, board_size):
        valid = []
        # Diagonals
        for i in range(1, board_size):
            # Up-Right
            if row - i >= 0 and col + i < board_size:
                target = board[row - i][col + i]
                if target is None:
                    valid.append((row - i, col + i))
                elif target.color != piece.color:
                    valid.append((row - i, col + i))
                    break  # Can't move past opponent piece
                else:
                    break  # Blocked by own piece
            else:
                break

            # Up-Left
            if row - i >= 0 and col - i >= 0:
                target = board[row - i][col - i]
                if target is None:
                    valid.append((row - i, col - i))
                elif target.color != piece.color:
                    valid.append((row - i, col - i))
                    break
                else:
                    break
            else:
                break

            # Down-Right
            if row + i < board_size and col + i < board_size:
                target = board[row + i][col + i]
                if target is None:
                    valid.append((row + i, col + i))
                elif target.color != piece.color:
                    valid.append((row + i, col + i))
                    break
                else:
                    break
            else:
                break

            # Down-Left
            if row + i < board_size and col - i >= 0:
                target = board[row + i][col - i]
                if target is None:
                    valid.append((row + i, col - i))
                elif target.color != piece.color:
                    valid.append((row + i, col - i))
                    break
                else:
                    break
            else:
                break

        return valid

class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'Queen')

    @staticmethod
    def get_valid_moves(piece, row, col, board, board_size):
        # Queen moves like a Bishop and a Rook
        bishop_moves = Bishop.get_valid_moves(piece, row, col, board, board_size)
        rook_moves = Rook.get_valid_moves(piece, row, col, board, board_size)
        return bishop_moves + rook_moves

class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'Rook')

    @staticmethod
    def get_valid_moves(piece, row, col, board, board_size):
        valid = []
        # Horizontal and Vertical
        for i in range(1, board_size):
            # Up
            if row - i >= 0:
                target = board[row - i][col]
                if target is None:
                    valid.append((row - i, col))
                elif target.color != piece.color:
                    valid.append((row - i, col))
                    break  # Can't move past opponent piece
                else:
                    break  # Blocked by own piece
            else:
                break
            # Down
            if row + i < board_size:
                target = board[row + i][col]
                if target is None:
                    valid.append((row + i, col))
                elif target.color != piece.color:
                    valid.append((row + i, col))
                    break
                else:
                    break
            else:
                break
            # Left
            if col - i >= 0:
                target = board[row][col - i]
                if target is None:
                    valid.append((row, col - i))
                elif target.color != piece.color:
                    valid.append((row, col - i))
                    break
                else:
                    break
            else:
                break
            # Right
            if col + i < board_size:
                target = board[row][col + i]
                if target is None:
                    valid.append((row, col + i))
                elif target.color != piece.color:
                    valid.append((row, col + i))
                    break
                else:
                    break
            else:
                break

        return valid

class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'Pawn')
        self.has_moved = False  # Track if the pawn has moved

    @staticmethod
    def get_valid_moves(piece, row, col, board, board_size):
        valid = []
        direction = 1 if piece.color == 'white' else -1
        start_row = board_size - 2 if piece.color == 'white' else 1

        # Move forward one square
        new_row = row + direction
        if 0 <= new_row < board_size and board[new_row][col] is None:
            valid.append((new_row, col))

            # Move forward two squares (if hasn't moved yet)
            if row == start_row:
                new_row += direction
                if 0 <= new_row < board_size and board[new_row][col] is None:
                    valid.append((new_row, col))

        # Capture diagonally
        for dc in (-1, 1):
            new_row = row + direction
            new_col = col + dc
            if 0 <= new_row < board_size and 0 <= new_col < board_size:
                target = board[new_row][new_col]
                if target is not None and target.color != piece.color:
                    valid.append((new_row, new_col))

        return valid



# Initialize the game
game = ChessGame()
game_mode = game.game_mode

def main():
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.handle_click(pos)

        # Drawing
        game.screen.fill((0, 0, 0))  # Clear the screen
        game.draw_board()
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    exit()

if __name__ == "__main__":
    main()

