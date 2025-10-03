import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("TIC TAC TOE ULTIMATE")
icon_image = pygame.image.load("imgs/images.png") 

pygame.display.set_icon(icon_image)

rect_width, rect_height = 350, 350
window = pygame.Rect(0, 0, rect_width, rect_height)
window_border = pygame.Rect(0, 0, rect_width + 10, rect_height + 10)

overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
overlay_color = pygame.Color(130, 130, 130, 120)
window.center = screen.get_rect().center
window_border.center = screen.get_rect().center
running = True

light_blue = (195, 216, 247)
dark_blue = (130, 150, 179)


stripe_width = 100 
scroll_speed = 2
offset = 0

board = [['', '', ''],
         ['', '', ''],
         ['', '', '']]
current_player = 'X'
game_over = False
cell_padding = 10

def draw_tictactoe_board(screen, window, board, cell_padding):
    grid_color = (255, 255, 255)
    line_thickness = 5
    
    board_width = window.width - 2 * cell_padding
    board_height = window.height - 2 * cell_padding
    cell_size = min(board_width, board_height) / 3
  
    board_x = window.x + cell_padding
    board_y = window.y + cell_padding

    pygame.draw.line(screen, grid_color, 
                     (board_x + cell_size, board_y), 
                     (board_x + cell_size, board_y + board_height), 
                     line_thickness)
    pygame.draw.line(screen, grid_color, 
                     (board_x + 2 * cell_size, board_y), 
                     (board_x + 2 * cell_size, board_y + board_height), 
                     line_thickness)

    pygame.draw.line(screen, grid_color, 
                     (board_x, board_y + cell_size), 
                     (board_x + board_width, board_y + cell_size), 
                     line_thickness)
    pygame.draw.line(screen, grid_color, 
                     (board_x, board_y + 2 * cell_size), 
                     (board_x + board_width, board_y + 2 * cell_size), 
                     line_thickness)
    
    return board_x, board_y, cell_size

def draw_marks(screen, board, board_x, board_y, cell_size):
    
    mark_color = ((47, 65, 89))
    mark_thickness = 10
    
    for row in range(3):
        for col in range(3):
            center_x = board_x + col * cell_size + cell_size / 2
            center_y = board_y + row * cell_size + cell_size / 2
            mark = board[row][col]
            
            if mark == 'X':

                size = cell_size * 0.4 
                pygame.draw.line(screen, mark_color, 
                                 (center_x - size, center_y - size), 
                                 (center_x + size, center_y + size), 
                                 mark_thickness)
                pygame.draw.line(screen, mark_color, 
                                 (center_x + size, center_y - size), 
                                 (center_x - size, center_y + size), 
                                 mark_thickness)
            elif mark == 'O':

                radius = int(cell_size * 0.4)
                pygame.draw.circle(screen, mark_color, (int(center_x), int(center_y)), 
                                   radius, mark_thickness)

def check_win(board, player):


    for row in range(3):
        if all(board[row][col] == player for col in range(3)):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)): # Top-left to bottom-right
        return True
    if all(board[i][2 - i] == player for i in range(3)): # Top-right to bottom-left
        return True
        
    return False

def check_draw(board):

    return all(board[row][col] != '' for row in range(3) for col in range(3)) and not (check_win(board, 'X') or check_win(board, 'O'))

def reset_game():

    global board, current_player, game_over
    board = [['', '', ''], ['', '', ''], ['', '', '']]
    current_player = 'X'
    game_over = False

while running:

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            if not game_over:
                mouse_pos = event.pos
                

                if window.collidepoint(mouse_pos):

                    board_width = window.width - 2 * cell_padding
                    board_height = window.height - 2 * cell_padding
                    cell_size = min(board_width, board_height) / 3
                    board_x = window.x + cell_padding
                    board_y = window.y + cell_padding
                    

                    if board_x <= mouse_pos[0] < board_x + 3 * cell_size and \
                       board_y <= mouse_pos[1] < board_y + 3 * cell_size:
                        

                        col = int((mouse_pos[0] - board_x) // cell_size)
                        row = int((mouse_pos[1] - board_y) // cell_size)
                        

                        if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == '':
                            board[row][col] = current_player
                            

                            if check_win(board, current_player):
                                print(f"Player {current_player} wins!")
                                game_over = True
                            elif check_draw(board):
                                print("It's a draw!")
                                game_over = True
                            else:
  
                                current_player = 'O' if current_player == 'X' else 'X'
                                
            else: 
                reset_game()
        if event.type == pygame.QUIT:
            running = False
    
        
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            window.center = screen.get_rect().center
            window_border.center = screen.get_rect().center
            overlay = pygame.Surface((event.w, event.h), pygame.SRCALPHA)

    screen_width, screen_height = screen.get_size()

    offset = (offset + scroll_speed) % (stripe_width * 2)

    for x in range(-offset, screen_width, stripe_width * 2):
        pygame.draw.rect(screen, dark_blue, (x, 0, stripe_width, screen_height))
        pygame.draw.rect(screen, light_blue, (x + stripe_width, 0, stripe_width, screen_height))


    overlay.fill(overlay_color)
    screen.blit(overlay, (0, 0))

    pygame.draw.rect(screen, (255, 255, 255), window_border)
    pygame.draw.rect(screen, (117, 144, 186), window)

    board_x, board_y, cell_size = draw_tictactoe_board(screen, window, board, cell_padding)
   
    draw_marks(screen, board, board_x, board_y, cell_size)

    if game_over:
        font = pygame.font.Font(None, 74) 
        
        status_text = ""
        if check_win(board, 'X'):
            status_text = "X Wins! (Click to Restart)"
        elif check_win(board, 'O'):
            status_text = "O Wins! (Click to Restart)"
        elif check_draw(board):
            status_text = "Draw! (Click to Restart)"

        text_surface = font.render(status_text, True, (45, 62, 84))
        text_rect = text_surface.get_rect(center=(window.centerx, window.bottom + 50))
        screen.blit(text_surface, text_rect)
    else:
   
        font = pygame.font.Font(None, 48)
        status_text = f"Player: {current_player}"
        text_surface = font.render(status_text, True, (237, 245, 255))
        text_rect = text_surface.get_rect(center=(window.centerx, window.y - 30))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

    dt = clock.tick(60)

pygame.quit()
