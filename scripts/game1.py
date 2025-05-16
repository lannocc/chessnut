class ChessPiece:
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol

    def get_valid_moves(self, row, col, board):
        """
        Returns a list of all valid moves from (row, col) on the given board.
        Implements move validation based on piece type.
        """
        pass  # To be implemented by subclasses


class Pawn(ChessPiece):
    def __init__(self, color, symbol="♙"):
        super().__init__(color, symbol)
    
    def get_valid_moves(self, row, col, board):
        if self.color == "white":
            # White pawn moves forward diagonally
            new_row = row + 1
            possible_moves = []
            for direction in [(2, -1), (2, 1)]:
                move_row, move_col = new_row + direction[0], col + direction[1]
                if self._is_within_board(move_row, move_col) and board[move_row][move_col] == "♟" * (-self.color != 
"white"):
                    possible_moves.append((move_row, move_col))
            # White pawn can move two squares forward on initial position
            if 0 <= row - 2 < len(board):
                move_row = row - 2
                move_col = col
                if self._is_within_board(move_row, move_col) and board[move_row][move_col] == "♟" * (-self.color != 
"white"):
                    possible_moves.append((move_row, move_col))
            # Black pawn moves backward diagonally
            new_row = row - 1
            possible_moves = []
            for direction in [(2, -1), (2, 1)]:
                move_row, move_col = new_row + direction[0], col + direction[1]
                if self._is_within_board(move_row, move_col) and board[move_row][move_col] == "♟" * (-self.color != 
"black"):
                    possible_moves.append((move_row, move_col))
            # Black pawn can move two squares backward on initial position
            if 0 <= row + 2 < len(board):
                move_row = row + 2
                move_col = col
                if self._is_within_board(move_row, move_col) and board[move_row][move_col] == "♟" * (-self.color != 
"black"):
                    possible_moves.append((move_row, move_col))
            return possible_moves
        else:
            # Black pawn moves forward diagonally (which is upward in the list)
            new_row = row - 1
            possible_moves = []
            for direction in [(2, -1), (2, 1)]:
                move_row, move_col = new_row + direction[0], col + direction[1]
                if self._is_within_board(move_row, move_col) and board[move_row][move_col] == "♟" * (-self.color != 
"black"):
                    possible_moves.append((move_row, move_col))
            # Black pawn can move two squares backward on initial position
            if 0 <= row + 2 < len(board):
                move_row = row - 2
                move_col = col
                if self._is_within_board(move_row, move_col) and board[move_row][move_col] == "♟" * (-self.color != 
"black"):
                    possible_moves.append((move_row, move_col))
            # White pawn moves backward diagonally (which is downward in the list)
            new_row = row + 1
            possible_moves = []
            for direction in [(2, -1), (2, 1)]:
                move_row, move_col = new_row + direction[0], col + direction[1]
                if self._is_within_board(move_row, move_col) and board[move_row][move_col] == "♟" * (-self.color != 
"white"):
                    possible_moves.append((move_row, move_col))
            # White pawn can move two squares forward on initial position
            if 0 <= row - 2 < len(board):
                move_row = row - 2
                move_col = col
                if self._is_within_board(move_row, move_col) and board[move_row][move_col] == "♟" * (-self.color != 
"white"):
                    possible_moves.append((move_row, move_col))
            return possible_moves

    def _is_within_board(self, row, col):
        """Check if the given row and column are within the chessboard."""
        return 0 <= row < len(self.board) and 0 <= col < len(self.board[0])

class Bishop(ChessPiece):
    def __init__(self, color, symbol="♗"):
        super().__init__(color, symbol)
    
    def get_valid_moves(self, row, col, board):
        """
        Returns a list of all valid diagonal moves from (row, col) on the given board.
        Bishops move diagonally any number of squares until blocked.
        """
        possible_moves = []
        # Check four diagonal directions
        for direction in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            step = 1
            while True:
                new_row = row + direction[0] * step
                new_col = col + direction[1] * step
                if self._is_within_board(new_row, new_col) and board[new_row][new_col] != "♟" * (-self.color != 
board[new_row][new_col].color):
                    possible_moves.append((new_row, new_col))
                else:
                    break
                step += 1
        return possible_moves

class Knight(ChessPiece):
    def __init__(self, color, symbol="♘"):
        super().__init__(color, symbol)
    
    def get_valid_moves(self, row, col, board):
        """
        Returns a list of all valid knight moves from (row, col) on the given board.
        Knights move in an L-shape: two squares in one direction and then one square perpendicular.
        """
        possible_moves = []
        # Knight has 8 possible moves
        deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
        for delta in deltas:
            new_row = row + delta[0]
            new_col = col + delta[1]
            if self._is_within_board(new_row, new_col):
                possible_moves.append((new_row, new_col))
        return possible_moves

class Rook(ChessPiece):
    def __init__(self, color, symbol="♖"):
        super().__init__(color, symbol)
    
    def get_valid_moves(self, row, col, board):
        """
        Returns a list of all valid rook moves from (row, col) on the given board.
        Rooks move in straight lines any number of squares until blocked.
        """
        possible_moves = []
        # Check four directions
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            step = 1
            while True:
                new_row = row + direction[0] * step
                new_col = col + direction[1] * step
                if self._is_within_board(new_row, new_col) and board[new_row][new_col] != "♟" * (-self.color != 
board[new_row][new_col].color):
                    possible_moves.append((new_row, new_col))
                else:
                    break
                step += 1
        return possible_moves

class Queen(ChessPiece):
    def __init__(self, color, symbol="♕"):
        super().__init__(color, symbol)
    
    def get_valid_moves(self, row, col, board):
        """
        Returns a list of all valid queen moves from (row, col) on the given board.
        Queens move like rooks and bishops combined, any number of squares in straight or diagonal lines until blocked.
        """
        possible_moves = []
        # Combine Rook and Bishop moves
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Rook directions
            step = 1
            while True:
                new_row = row + direction[0] * step
                new_col = col + direction[1] * step
                if self._is_within_board(new_row, new_col) and board[new_row][new_col] != "♟" * (-self.color != 
board[new_row][new_col].color):
                    possible_moves.append((new_row, new_col))
                else:
                    break
                step += 1

        for direction in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Bishop directions
            step = 1
            while True:
                new_row = row + direction[0] * step
                new_col = col + direction[1] * step
                if self._is_within_board(new_row, new_col) and board[new_row][new_col] != "♟" * (-self.color != 
board[new_row][new_col].color):
                    possible_moves.append((new_row, new_col))
                else:
                    break
                step += 1
        return possible_moves

class King(ChessPiece):
    def __init__(self, color, symbol="♔"):
        super().__init__(color, symbol)
    
    def get_valid_moves(self, row, col, board):
        """
        Returns a list of all valid king moves from (row, col) on the given board.
        Kings move one square in any direction horizontally, vertically, or diagonally.
        """
        possible_moves = []
        deltas = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0), (1, 1)]
        for delta in deltas:
            new_row = row + delta[0]
            new_col = col + delta[1]
            if self._is_within_board(new_row, new_col) and board[new_row][new_col] != "♟" * (-self.color != 
board[new_row][new_col].color):
                possible_moves.append((new_row, new_col))
        return possible_moves

class CompositePiece(ChessPiece):
    def __init__(self, color, symbol="♟"):
        super().__init__(color, symbol)
    
    def get_valid_moves(self, row, col, board):
        """
        Returns a list of all valid moves from (row, col) on the given board.
        The CompositePiece combines multiple types of pieces as per the game rules provided in the problem statement.
        For this problem:
            - The first part is always a Bishop
            - The second part can be any piece
        So, for example: Bishop + Rook would result in moves from both Bishops and Rooks being available on the board.
        """
        # Combine all possible moves of each part
        moves = set()

        # Add moves from the first part (Bishop)
        bishop_moves = self.get_part(0).get_valid_moves(row, col, board)
        for move in bishop_moves:
            if not any(board[new_row][new_col] == "♟" * (-self.color != board[new_row][new_col].color) for new_row, new_col 
in moves):
                # Check if the square is blocked by own pieces
                pass  # Already handled within get_valid_moves of each part

        # Add moves from the second part (any piece)
        other_moves = self.get_part(1).get_valid_moves(row, col, board)
        for move in other_moves:
            if not any(board[new_row][new_col] == "♟" * (-self.color != board[new_row][new_col].color) for new_row, new_col 
in moves):
                # Check if the square is blocked by own pieces
                pass  # Already handled within get_valid_moves of each part

        # Combine all unique moves from both parts and ensure no duplicates
        return list(moves)

def main():
    import sys
    board = []
    q = int(sys.stdin.readline())
    for _ in range(q):
        line = sys.stdin.readline().strip()
        if not line:
            continue  # Skip empty lines
        parts = line.split()
        color = parts[0]
        row_str = parts[1]
        col_str = parts[2]
        piece_type = parts[3]
        symbol = parts[4] if len(parts) >5 else ''
        # Validate the input (simplify for this problem)
        board_row = int(row_str) - 1
        board_col = int(col_str) - 1
        current_color = 'white' if color == 'black' else 'black'
        piece = None

        if len(parts) >4:
            # Check if it's a composite piece (Bishop + other)
            if parts[2] == "♟":
                # It's a Bishop part, so first part is Bishop
                other_part = parts[3]
                if other_part in ['♜', '♞', '♝', '♛', '♚']:
                    pass  # Other part must be another piece type

        # Create the appropriate piece based on type and symbol
        if piece_type == '♟':
            # It's a Bishop + something else
            piece = CompositePiece(color, symbol)
        elif piece_type in ['♜', '♞', '♝', '♛', '♚']:
            piece = ChessPiece(color, symbol)
        else:
            # Unknown piece type (simplify for this problem)
            piece = None

        if not piece or piece is None:
            print("Invalid piece type")
            continue

        # Get all valid moves
        valid_moves = piece.get_valid_moves(board_row, board_col, board)

        # Print the number of valid moves and each move in order from top-left to bottom-right
        print(len(valid_moves))
        for r, c in sorted(valid_moves):
            print(r+1, c+1)

if __name__ == "__main__":
    main()

