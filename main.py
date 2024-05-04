import pygame
import playing

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
PADDING = 5
CHIP_SIZE = WIDTH // COLS - 2 * PADDING
BORDER_WIDTH = 4
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 236, 161)
INF = 100000000
# Tokens
RED_CHIP = pygame.image.load("images/red_chip.png")
BLACK_CHIP = pygame.image.load("images/black_chip.png")
BLACK_CHIP2 = pygame.image.load("images/black_chip2.png")
RED_CHIP2 = pygame.image.load("images/red_chip2.png")

RED_CHIP = pygame.transform.scale(RED_CHIP, (SQUARE_SIZE - 2 * PADDING, SQUARE_SIZE - 2 * PADDING))
RED_CHIP2 = pygame.transform.scale(RED_CHIP2, (SQUARE_SIZE - 2 * PADDING, SQUARE_SIZE - 2 * PADDING))
BLACK_CHIP = pygame.transform.scale(BLACK_CHIP, (SQUARE_SIZE - 2 * PADDING, SQUARE_SIZE - 2 * PADDING))
BLACK_CHIP2 = pygame.transform.scale(BLACK_CHIP2, (SQUARE_SIZE - 2 * PADDING, SQUARE_SIZE - 2 * PADDING))

# Create the display surface
turn_played = False
moves = []
opcija = '1'
ima_jedenja = False
# Checkers board representation, 1=red, 2=black

board = [
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0]
]
next_move = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]


# Main function to draw the board
def draw_board():
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 1:
                pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == 1:
                screen.blit(RED_CHIP, (c * SQUARE_SIZE + PADDING, r * SQUARE_SIZE + PADDING))
            if board[r][c] == 2:
                screen.blit(BLACK_CHIP, (c * SQUARE_SIZE + PADDING, r * SQUARE_SIZE + PADDING))
            if board[r][c] == 3:
                screen.blit(RED_CHIP2, (c * SQUARE_SIZE + PADDING, r * SQUARE_SIZE + PADDING))
            if board[r][c] == 4:
                screen.blit(BLACK_CHIP2, (c * SQUARE_SIZE + PADDING, r * SQUARE_SIZE + PADDING))

            if next_move[r][c] == 1:
                pygame.draw.rect(screen, RED, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                                 BORDER_WIDTH)
            if next_move[r][c] == 2:
                pygame.draw.rect(screen, YELLOW, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                                 BORDER_WIDTH)
            if next_move[r][c] == 3:
                pygame.draw.rect(screen, YELLOW, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                                 BORDER_WIDTH//2)


def highlight(r, c):    # ovo zapravo napravi moves za trenutno kliknuto polje
    global moves, ima_jedenja
    if board[r][c] != 0 and board[r][c] != 1 and board[r][c] != 3:
        next_move[r][c] = 2
        moves = []
        playing.find_moves(board, r, c, 2, [], True, moves)
        #print("Za trenutno kliknuto polje dostupni potezi su:")
        for move in moves:
            if ima_jedenja and (abs(move[0][0] - r) + abs(move[0][1] - c)) == 4 and opcija == '1':
                next_move[move[-1][0]][move[-1][1]] = 1
                next_move[r][c] = 3
                #print(move)
            if opcija == '2':
                next_move[move[-1][0]][move[-1][1]] = 1
            if opcija == '1' and not ima_jedenja:
                next_move[move[-1][0]][move[-1][1]] = 1
                #print(move)
        #playing.print_board(next_move)


def make_turn(r, c):  # kliknuto je na R, C
    global turn_played, moves, ima_jedenja
    if next_move[r][c] != 1:
        return False

    ima_jedenja = False
    x = ru = cu = 1
    #print("Igram potez")
    for i in range(8):
        for j in range(8):
            if next_move[i][j] == 2 or next_move[i][j] == 3:
                x = board[i][j]
                ru = i
                cu = j
                break
    #print("Pocinjem sa polja: ", ru, " ", cu)
    for move in moves:
        if move[-1][0] == r and move[-1][1] == c:
            board[ru][cu] = 0
            for elem in move:
                board[ru + (elem[0] - ru) // 2][cu + (elem[1] - cu) // 2] = 0
                ru = elem[0]
                cu = elem[1]

            board[r][c] = x

            if r == 0:
                board[r][c] = 4

            turn_played = True
            return True


def handle_click(pos):
    global next_move
    r = pos[1] // SQUARE_SIZE
    c = pos[0] // SQUARE_SIZE
    print("Clicked on:", r, c)
    #playing.print_board(next_move)

    if make_turn(r, c):
        for i in range(8):
            for j in range(8):
                next_move[i][j] = 0
    else:
        for i in range(8):
            for j in range(8):
                if next_move[i][j] != 3:
                    next_move[i][j] = 0
        highlight(r, c)


def find_all_moves():
    if opcija == '2':
        return
    global ima_jedenja
    for r in range(8):
        for c in range(8):
            if board[r][c] == 2 or board[r][c] == 4:
                moves = []
                playing.find_moves(board, r, c, 2, [], True, moves)
                for move in moves:
                    if abs(move[0][0] - r) + abs(move[0][1] - c) == 4:
                        ima_jedenja = True
                        next_move[r][c] = 3
                        break


def main():         # Main game loop
    global board, turn_played
    board = [
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 2, 0, 2, 0, 2, 0]
    ]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                handle_click(pos)

        draw_board()
        pygame.display.update()

        if turn_played:
            playing.minimax(board, 7, 7, True, 1, -INF, INF, opcija)
            turn_played = False
            find_all_moves()


if __name__ == "__main__":
    '''while True:
        opcija = input("Da li su potezi jedenja obavezni? 1 da, 2 ne: ")
        if opcija == '1' or opcija == '2':
            break'''
    opcija = '2'
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Checkers")
    main()
'''
    board = [
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 2, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 1],
        [0, 0, 2, 0, 2, 0, 1, 0],
        [0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 2, 0, 2, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 3, 0, 0, 0, 0, 0]
    ]
    board1 = [
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 2, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 1],
        [0, 0, 2, 0, 2, 0, 0, 0],
        [0, 0, 0, 2, 0, 1, 0, 0],
        [0, 0, 2, 0, 2, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 3, 0, 0, 0, 0, 0]
    ]
    board2 = [
        [0, 1, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 1],
        [0, 0, 2, 0, 0, 0, 1, 0],
        [0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 2, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [2, 0, 3, 0, 0, 0, 0, 0]
    ]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                playing.minimax(board, 5, 5, True, 1, -INF, INF)

        draw_board()
        pygame.display.update()'''
