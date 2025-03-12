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
MARGIN = 150  # Left and Right space for lost pieces display

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Piece images setup (replace these paths with the actual image files)
piece_images = {}

def load_images():
    piece_names = ["white_pawn", "black_pawn", "white_rook", "black_rook", "white_knight", "black_knight", "white_bishop", "black_bishop", "white_queen", "black_queen", "white_king", "black_king"]
    for piece in piece_names:
        piece_images[piece] = pygame.image.load(os.path.join(SCRIPT_DIR, 'img', f'{piece}.png'))
        print(f"Loading image: {os.path.join(SCRIPT_DIR, 'img', f'{piece}.png')}")  # Debugging line
        piece_images[piece] = pygame.transform.scale(piece_images[piece], (SQUARE_SIZE, SQUARE_SIZE))

# Chess pieces setup (with correct placement and board size adjustments)
initial_setup = [
    first_row := ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook'],
    ['Pawn'] * 8,
    *([[None] * 8] * 4),  # 4 rows of empty spaces
    ['Pawn'] * 8,
    first_row
]

# Lost pieces setup (arrays to store lost pieces)
white_lost_pieces = []
black_lost_pieces = []

# Create the chess board
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE + MARGIN, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Draw boundary lines
    line_color = BLACK
    pygame.draw.line(screen, line_color, (MARGIN, 0), (MARGIN, HEIGHT), 2)  
    pygame.draw.line(screen, line_color, (WIDTH - MARGIN, 0), (WIDTH - MARGIN, HEIGHT), 2)  

# Draw chess pieces
def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = initial_setup[row][col]
            if piece:
                piece_color = "white" if row < 2 else "black"
                piece_name = f"{piece_color}_{piece.lower()}"

                # Center piece image on the square
                piece_image = piece_images.get(piece_name)
                if piece_image:
                    screen.blit(piece_image, (col * SQUARE_SIZE + MARGIN, row * SQUARE_SIZE))

# Draw lost pieces on the sides
def draw_lost_pieces():
    # Draw white lost pieces on the left
    y_offset = 20
    for piece in white_lost_pieces:
        piece_image = piece_images.get(piece)
        if piece_image:
            screen.blit(piece_image, (20, y_offset))
            y_offset += 60  # Space out the lost pieces

    # Draw black lost pieces on the right
    y_offset = 20
    for piece in black_lost_pieces:
        piece_image = piece_images.get(piece)
        if piece_image:
            screen.blit(piece_image, (WIDTH - 80, y_offset))
            y_offset += 60  # Space out the lost pieces

# Main game loop
def main():
    load_images()
    
    running = True
    while running:
        screen.fill((255, 255, 255))  # Fill the background with white
        draw_board()
        draw_pieces()
        draw_lost_pieces()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()  # Update the display

    pygame.quit()

if __name__ == "__main__":
    main()
