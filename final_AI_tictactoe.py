import pygame
from pygame.locals import *

pygame.init()

screen_height = 300
screen_width = 300
screen = pygame.display.set_mode((screen_height, screen_width))
pygame.display.set_caption("TicTacToe")

line_width = 6 
table = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
clicked = False
player = 1
winner = 0
game_over = 0
pa_rect = Rect(screen_width // 2 - 100, screen_height // 2 + 65, 180, 50)
font = pygame.font.SysFont(None, 40)
 
def draw_grid():
    screen.fill((0, 0, 0))
    for i in range(3):
        pygame.draw.line(screen, (255, 255, 255), (0, i * (screen_width/3)), (screen_width, i * (screen_width/3)))
        pygame.draw.line(screen, (255, 255, 255),  (i * (screen_height/3), 0), (i * (screen_height/3), screen_height))

def draw_symbols():
    x_pos = 0
    for x in table:
        y_pos = 0
        for y in x:
            if y == 1:
                pygame.draw.line(screen, (255, 255, 255), (x_pos * 100 + 15, y_pos * 100 + 15), (x_pos * 100 + 85, y_pos * 100 + 85), line_width)
                pygame.draw.line(screen, (255, 255, 255), (x_pos * 100 + 15, y_pos * 100 + 85), (x_pos * 100 + 85, y_pos * 100 + 15), line_width)
            elif y == -1:
                pygame.draw.circle(screen, (255, 255, 255), (x_pos * 100 + 50, y_pos * 100 + 50), 30, line_width)
            y_pos += 1
        x_pos += 1

def check_winner():
    global winner
    global game_over

    for i in range(3):
        if sum(table[i]) == 3 or table[0][i] + table[1][i] + table[2][i] == 3:
            winner = 1
            game_over = 1
        elif sum(table[i]) == -3 or table[0][i] + table[1][i] + table[2][i] == -3:
            winner = 2
            game_over = 1

    if table[0][0] + table[1][1] + table[2][2] == 3 or table[2][0] + table[1][1] + table[0][2] == 3:
        winner = 1
        game_over = 1
    elif table[0][0] + table[1][1] + table[2][2] == -3 or table[2][0] + table[1][1] + table[0][2] == -3:
        winner = 2
        game_over = 1

    if game_over == 0 and all(all(cell != 0 for cell in row) for row in table):
        game_over = 1
        winner = 0 

def draw_winner():
    if winner == 0:
        win_txt = "It's a Tie!"
    else:
        win_txt = "Player " + str(winner) + " wins!"
    win_img = font.render(win_txt, True, (0, 0, 255))
    pygame.draw.rect(screen, (0, 255, 0), (screen_width // 2 - 120, screen_height // 2 - 30, 240, 50))
    screen.blit(win_img, (screen_width // 2 - 100, screen_height // 2 - 20 ))

    pa_txt = "Play Again"
    pa_img = font.render(pa_txt, True, (0, 0 ,255))
    pygame.draw.rect(screen, (0, 255, 0), pa_rect)
    screen.blit(pa_img, (screen_width // 2 - 75, screen_height // 2 + 75 ))

def clear_grid():
    global table
    table = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

def get_available_moves(board):
    moves = []
    for col in range(3):
        for row in range(3):
            if board[col][row] == 0:
                moves.append((col, row))
    return moves

def evaluate(board):
    for i in range(3):
        if sum(board[i]) == 3 or board[0][i] + board[1][i] + board[2][i] == 3:
            return 1
        elif sum(board[i]) == -3 or board[0][i] + board[1][i] + board[2][i] == -3:
            return -1

    if board[0][0] + board[1][1] + board[2][2] == 3 or board[2][0] + board[1][1] + board[0][2] == 3:
        return 1
    elif board[0][0] + board[1][1] + board[2][2] == -3 or board[2][0] + board[1][1] + board[0][2] == -3:
        return -1

    return 0

def minimax(board, depth, isMaximizing):
    result = evaluate(board)
    if result == 1:
        return 100 - depth
    elif result == -1:
        return -100 + depth
    elif not get_available_moves(board):
        return 0

    if isMaximizing:
        best_score = float("-inf")
        for move in get_available_moves(board):
            col, row = move
            board[col][row] = 1
            score = minimax(board, depth + 1, False)
            board[col][row] = 0
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for move in get_available_moves(board):
            col, row = move
            board[col][row] = -1
            score = minimax(board, depth + 1, True)
            board[col][row] = 0
            best_score = min(best_score, score)
        return best_score

def make_ai_move(): 
    global table
    best_score = float("-inf")
    best_move = None
    for move in get_available_moves(table):
        col, row = move
        table[col][row] = 1
        score = minimax(table, 0, False)
        table[col][row] = 0
        if score > best_score:
            best_score = score
            best_move = move
    if best_move:
        col, row = best_move
        table[col][row] = 1
        
def handle_events():
    global game_over
    global player
    global clicked
    global event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if game_over == 0 and player == -1:    
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                pos = pygame.mouse.get_pos()
                x_coord = pos[0]
                y_coord = pos[1]
                if table[x_coord // 100][y_coord // 100] == 0:
                    table[x_coord // 100][y_coord // 100] = player
                    player *= -1
                    check_winner()
        elif game_over == 0 and player == 1:
            make_ai_move()
            check_winner()
            player *= -1
    if game_over == 1:
        draw_winner()     
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            pos = pygame.mouse.get_pos()
            if pa_rect.collidepoint(pos):
                clear_grid()
                player = 1
                winner = 0
                game_over = 0
                clicked = False

def main():
    global clicked
    global player
    while True:
        draw_grid() 
        draw_symbols()
        handle_events()  
        pygame.display.update()

if __name__ == "__main__":
    main()