import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 640  # Increased the width
GRID_SIZE = 640  # Size of the grid
ROWS, COLS = 20, 20
CELL_SIZE = GRID_SIZE // COLS
BUTTON_WIDTH, BUTTON_HEIGHT = 80, 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (64, 64, 64)  # Color for the empty space
RED = (255, 0, 0)  # Color for the save button
DARK_RED = (128, 0, 0)  # Color for the save button when clicked


# Load the map from the CSV file, or create a new one if the file doesn't exist
try:
    map = np.loadtxt("map.csv", dtype=int)
except OSError:
    map = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

# Create the window
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Load the font
font = pygame.font.Font('return-to-castle-font/ReturnToCastle-MZnx.ttf', 44)

def draw_grid():
    for i in range(ROWS):
        for j in range(COLS):
            color = BLACK if map[i][j] == 1 else DARK_GRAY
            pygame.draw.rect(win, color, (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw gridlines
    for i in range(ROWS + 1):
        pygame.draw.line(win, WHITE, (0, i * CELL_SIZE), (GRID_SIZE, i * CELL_SIZE))
    for j in range(COLS + 1):
        pygame.draw.line(win, WHITE, (j * CELL_SIZE, 0), (j * CELL_SIZE, HEIGHT))

def draw_button(is_clicked):
    color = DARK_RED if is_clicked else RED
    pygame.draw.rect(win, color, (GRID_SIZE + (WIDTH - GRID_SIZE - BUTTON_WIDTH) // 2, HEIGHT - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT))
    text_surface = font.render('SAVE', True, WHITE)
    win.blit(text_surface, (GRID_SIZE + (WIDTH - GRID_SIZE - BUTTON_WIDTH) // 2, HEIGHT - BUTTON_HEIGHT))

def get_cell_pos(mouse_pos):
    x, y = mouse_pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col

def is_button_clicked(pos):
    x, y = pos
    return GRID_SIZE <= x <= WIDTH and HEIGHT - BUTTON_HEIGHT <= y <= HEIGHT

run = True
button_clicked = False
while run:
    draw_grid()
    draw_button(button_clicked)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_button_clicked(pygame.mouse.get_pos()):
                button_clicked = True
            else:
                row, col = get_cell_pos(pygame.mouse.get_pos())
                if row < ROWS and col < COLS:  # Ensure the click is within the grid
                    map[row][col] = 1 - map[row][col]  # Toggle between 1 and 0
        if event.type == pygame.MOUSEBUTTONUP:
            if button_clicked:
                np.savetxt("map.csv", map, fmt="%d")
                print("Map saved!")
                button_clicked = False

    pygame.display.update()

pygame.quit()