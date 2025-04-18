import pygame
import os
import sys
import numpy as np

# Constants
size_of_board = 750
grid_size = 15
cell_size = size_of_board // grid_size
symbol_size = cell_size // 3
symbol_thickness = 8
symbol_X_color = (238, 64, 53)  # '#EE4035'
symbol_O_color = (4, 146, 207) # '#0492CF'
symbol_green_color = '#7BC043'
line_color = (0, 173, 181)
bg_color = (240, 248, 255)
hover_color = (200, 220, 255)
header_height = 80

pygame.init()
screen = pygame.display.set_mode((size_of_board, size_of_board + header_height))
pygame.display.set_caption('🎮 Game Cờ Caro 2 Người')
font = pygame.font.SysFont("Tahoma", 35, bold=True)
small_font = pygame.font.SysFont("Tahoma", 25)
font_bold = pygame.font.SysFont("Tahoma", 25, bold=True)
font_icon = pygame.font.SysFont("Segoe UI Emoji", 35)

def draw_header(player_X_turn):
    pygame.draw.rect(screen, (0, 173, 181), (0, 0, size_of_board, header_height))
    text = f"Lượt: {'Người chơi 1 (X)' if player_X_turn else 'Người chơi 2 (O)'}"
    render = font.render(text, True, (255, 255, 255))
    screen.blit(render, (20, header_height // 2 - render.get_height() // 2))

def draw_grid(mouse_pos):
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * cell_size
            y = row * cell_size + header_height
            rect = pygame.Rect(x, y, cell_size, cell_size)
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, hover_color, rect)
            pygame.draw.rect(screen, line_color, rect, 1)

def draw_O(row, col):
    center = (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2 + header_height)
    pygame.draw.circle(screen, symbol_O_color, center, symbol_size, symbol_thickness)

def draw_X(row, col):
    x = col * cell_size + cell_size // 2
    y = row * cell_size + cell_size // 2 + header_height
    offset = symbol_size
    pygame.draw.line(screen, symbol_X_color, (x - offset, y - offset), (x + offset, y + offset), symbol_thickness)
    pygame.draw.line(screen, symbol_X_color, (x - offset, y + offset), (x + offset, y - offset), symbol_thickness)

def is_winner(board, player):
    for i in range(grid_size):
        for j in range(grid_size):
            # Check horizontal
            if j <= grid_size - 5 and all(board[i][j + k] == player for k in range(5)):
                return True
            # Check vertical
            if i <= grid_size - 5 and all(board[i + k][j] == player for k in range(5)):
                return True
            # Check main diagonal
            if i <= grid_size - 5 and j <= grid_size - 5 and all(board[i + k][j + k] == player for k in range(5)):
                return True
            # Check anti diagonal
            if i <= grid_size - 5 and j >= 4 and all(board[i + k][j - k] == player for k in range(5)):
                return True
    return False

def is_tie(board):
    return not np.any(board == 0)

def display_result(text, score_X, score_O):
    overlay = pygame.Surface((size_of_board, size_of_board + header_height))
    overlay.set_alpha(240)
    overlay.fill((240, 248, 255))
    screen.blit(overlay, (0, 0))

    # Màu kết quả
    if "X" in text:
        result_color = (238, 64, 53)
    elif "O" in text:
        result_color = (4, 146, 207)
    else:
        result_color = (255, 223, 0)

    # Create the emoji part
    emoji = "🎉" if "thắng!" in text else "🤝"
    emoji_text = font_icon.render(emoji, True, result_color)

    # Render the rest of the result text (after the emoji)
    result_text = font.render(text[2:], True, result_color)  # Skip the emoji

    # Draw the emoji and result text separately
    screen.blit(emoji_text, (size_of_board // 2 - emoji_text.get_width() // 2 - result_text.get_width() // 2 - 20, size_of_board // 2 - 80))
    screen.blit(result_text, (size_of_board // 2 - result_text.get_width() // 2, size_of_board // 2 - 80))

    # Điểm số
    score_header_text = font_bold.render("Điểm số:", True, (0, 0, 0))
    screen.blit(score_header_text, (size_of_board // 2 - score_header_text.get_width() // 2,
                                    size_of_board // 2 + 10))

    # Adjusted y position for a little margin between "Điểm số" and player scores
    score_margin = 10  # Add a little margin
    score_text_X = small_font.render(f"Người chơi 1 (X): {score_X}", True, symbol_X_color)
    screen.blit(score_text_X, (size_of_board // 2 - score_text_X.get_width() // 2,
                               size_of_board // 2 + 40 + score_margin))

    score_text_O = small_font.render(f"Người chơi 2 (O): {score_O}", True, symbol_O_color)
    screen.blit(score_text_O, (size_of_board // 2 - score_text_O.get_width() // 2,
                               size_of_board // 2 + 70 + score_margin))

    # Nút
    button_width = 140
    button_height = 50
    button_spacing = 40
    total_width = button_width * 2 + button_spacing
    start_x = size_of_board // 2 - total_width // 2
    y_position = size_of_board // 2 + 150

    play_again_rect = pygame.Rect(start_x, y_position, button_width, button_height)
    quit_rect = pygame.Rect(start_x + button_width + button_spacing, y_position, button_width, button_height)

    mouse_pos = pygame.mouse.get_pos()

    cursor_changed = False

    # -------- Nút Chơi lại --------
    if play_again_rect.collidepoint(mouse_pos):
        if not cursor_changed:  # Chỉ thay đổi con trỏ khi cần
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            cursor_changed = True
        pygame.draw.rect(screen, (220, 255, 220), play_again_rect)  # Hover nền xanh nhạt
    else:
        pygame.draw.rect(screen, (255, 255, 255), play_again_rect)  # Nền trắng

    pygame.draw.rect(screen, (0, 128, 0), play_again_rect, 2)  # Viền xanh lá
    play_text = small_font.render("Chơi lại", True, (0, 128, 0))
    screen.blit(play_text, (
        play_again_rect.centerx - play_text.get_width() // 2,
        play_again_rect.centery - play_text.get_height() // 2)
    )

    # -------- Nút Thoát --------
    if quit_rect.collidepoint(mouse_pos):
        if not cursor_changed:  # Chỉ thay đổi con trỏ khi cần
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            cursor_changed = True
        pygame.draw.rect(screen, (255, 220, 220), quit_rect)  # Hover nền đỏ nhạt
    else:
        pygame.draw.rect(screen, (255, 255, 255), quit_rect)  # Nền trắng

    pygame.draw.rect(screen, (255, 0, 0), quit_rect, 2)  # Viền đỏ
    quit_text = small_font.render("Thoát", True, (255, 0, 0))
    screen.blit(quit_text, (
        quit_rect.centerx - quit_text.get_width() // 2,
        quit_rect.centery - quit_text.get_height() // 2)
    )

    pygame.display.update()
    return play_again_rect, quit_rect

def main():
    board = np.zeros((grid_size, grid_size))
    player_X_turn = True
    running = True
    game_over = False
    score_X = 0
    score_O = 0
    play_btn = quit_btn = None

    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(bg_color)

        if not game_over:
            draw_header(player_X_turn)  # Draw the header only if the game is not over
            draw_grid(mouse_pos)

            for row in range(grid_size):
                for col in range(grid_size):
                    if board[row][col] == -1:
                        draw_X(row, col)
                    elif board[row][col] == 1:
                        draw_O(row, col)
        else:
            # When the game is over, skip drawing the header
            play_btn, quit_btn = display_result(f"🎉 Người chơi {'1 (X)' if score_X > score_O else '2 (O)'} thắng!" if score_X > score_O else "🤝 Hòa!", score_X, score_O)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    x, y = event.pos
                    if y > header_height:
                        col = x // cell_size
                        row = (y - header_height) // cell_size
                        if board[row][col] == 0:
                            board[row][col] = -1 if player_X_turn else 1
                            if is_winner(board, board[row][col]):
                                if player_X_turn:
                                    score_X += 1
                                    result_text = "🎉 Người chơi 1 (X) thắng!"
                                else:
                                    score_O += 1
                                    result_text = "🎉 Người chơi 2 (O) thắng!"
                                play_btn, quit_btn = display_result(result_text, score_X, score_O)
                                game_over = True
                            elif is_tie(board):
                                play_btn, quit_btn = display_result("🤝 Hòa!", score_X, score_O)
                                game_over = True
                            player_X_turn = not player_X_turn
                else:
                    if play_btn and play_btn.collidepoint(event.pos):
                        board = np.zeros((grid_size, grid_size))
                        game_over = False
                        player_X_turn = True
                    elif quit_btn and quit_btn.collidepoint(event.pos):
                        pygame.quit()  # Close pygame
                        os.execl(sys.executable, sys.executable, 'caro_game.py')  # Restart the game

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
