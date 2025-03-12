import pygame
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 1100
HEIGHT = 800
SQUARE_SIZE = 100
MARGIN = 150  # Space for lost pieces
LOST_PIECE_SIZE = 100  # Captured piece size
LOST_PIECE_SPACING = 47  # Space per piece, ensuring 15 fit vertically

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Load piece images
piece_images = {}

def load_images():
    pieces = ["pawn", "rook", "knight", "bishop", "queen", "king"]
    colors = ["white", "black"]
    for color in colors:
        for piece in pieces:
            piece_images[f"{color}_{piece}"] = pygame.transform.scale(
                pygame.image.load(os.path.join(SCRIPT_DIR, 'img', f'{color}_{piece}.png')),
                (SQUARE_SIZE, SQUARE_SIZE)
            )
                       
# Pawn class
class Pawn:
    def __init__(self, color, piece_type):
        self.color = color
        self.image = piece_images[f"{color}_{piece_type}"]
    def valid_move(self, start_row, start_col, end_row, end_col, board):
        direction = -1 if self.color == 'white' else 1
        if start_col == end_col:
            if (end_row - start_row) == direction and board[end_row][end_col] is None:
                return True
            elif (end_row - start_row) == 2 * direction and start_row in (1, 6) and board[end_row][end_col] is None:
                return True
        elif abs(start_col - end_col) == 1 and (end_row - start_row) == direction:
            if board[end_row][end_col] and board[end_row][end_col].color != self.color:
                return True
        return False
    
class Rook:
    def __init__(self, color, piece_type):
        self.color = color
        self.image = piece_images[f"{color}_{piece_type}"]
        
class Knight:
    def __init__(self, color, piece_type):
        self.color = color
        self.image = piece_images[f"{color}_{piece_type}"]

class Bishop:
    def __init__(self, color, piece_type):
        self.color = color
        self.image = piece_images[f"{color}_{piece_type}"]

class Queen:
    def __init__(self, color, piece_type):
        self.color = color
        self.image = piece_images[f"{color}_{piece_type}"]

class King:
    def __init__(self, color, piece_type):
        self.color = color
        self.image = piece_images[f"{color}_{piece_type}"]

# Initialize board
def setup_board():
    global board  # Ensure we modify the global board variable
    board = [[None for _ in range(8)] for _ in range(8)]
    
    # Place pawns
    for col in range(8):
        board[1][col] = Pawn("black", "pawn")
        board[6][col] = Pawn("white", "pawn")

    # Place rooks
    board[0][0] = board[0][7] = Rook("black", "rook")
    board[7][0] = board[7][7] = Rook("white", "rook")

    # Place knights
    board[0][1] = board[0][6] = Knight("black", "knight")
    board[7][1] = board[7][6] = Knight("white", "knight")

    # Place bishops
    board[0][2] = board[0][5] = Bishop("black", "bishop")
    board[7][2] = board[7][5] = Bishop("white", "bishop")

    # Place queens
    board[0][3] = Queen("black", "queen")
    board[7][3] = Queen("white", "queen")

    # Place kings
    board[0][4] = King("black", "king")
    board[7][4] = King("white", "king")
    
load_images()
setup_board()

# Lists for lost pieces
white_lost_pieces = []
black_lost_pieces = []

# Draw the board with margins
def draw_board():
    board_x_offset = MARGIN  # Offset to center board properly
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE + MARGIN, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
    line_color = BLACK
    pygame.draw.line(screen, line_color, (MARGIN, 0), (MARGIN, HEIGHT), 2)  
    pygame.draw.line(screen, line_color, (WIDTH - MARGIN, 0), (WIDTH - MARGIN, HEIGHT), 2)  

def draw_pieces():
    board_x_offset = MARGIN
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                screen.blit(piece.image, (col * SQUARE_SIZE + MARGIN, row * SQUARE_SIZE))

# Draw lost pieces with proper spacing
def draw_lost_pieces():

    # White lost pieces (left side)
    for i, piece in enumerate(white_lost_pieces):
        screen.blit(pygame.transform.scale(piece.image, (LOST_PIECE_SIZE, LOST_PIECE_SIZE)), 
                    (25, i * LOST_PIECE_SPACING))

    # Black lost pieces (right side)
    for i, piece in enumerate(black_lost_pieces):
        screen.blit(pygame.transform.scale(piece.image, (LOST_PIECE_SIZE, LOST_PIECE_SIZE)), 
                    (WIDTH - 125, i * LOST_PIECE_SPACING))

# Handle moves and capturing
def handle_move(start_row, start_col, end_row, end_col):
    piece = board[start_row][start_col]
    if piece and piece.valid_move(start_row, start_col, end_row, end_col, board):
        captured_piece = board[end_row][end_col]
        if captured_piece:
            if captured_piece.color == "white":
                white_lost_pieces.append(captured_piece)
            else:
                black_lost_pieces.append(captured_piece)

        board[end_row][end_col] = piece
        board[start_row][start_col] = None
        print(f"{piece.color.capitalize()} Pawn moved from ({start_row}, {start_col}) to ({end_row}, {end_col})")
        return True
    return False

# Main game loop
def main():
    load_images()
    selected_piece = None
    running = True

    while running:
        screen.fill((255, 255, 255))
        draw_board()
        draw_pieces()
        draw_lost_pieces()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                col = (mouse_x - MARGIN) // SQUARE_SIZE
                row = mouse_y // SQUARE_SIZE

                if 0 <= row < 8 and 0 <= col < 8:
                    if selected_piece is None:
                        if board[row][col]:
                            selected_piece = (row, col)
                    else:
                        if handle_move(selected_piece[0], selected_piece[1], row, col):
                            selected_piece = None
                        else:
                            selected_piece = None

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
