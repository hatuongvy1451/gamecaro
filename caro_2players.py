import pygame
import sys
import subprocess
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Constants
size_of_board = 750  # Kích thước bàn cờ
grid_size = 15  # Số ô cờ
cell_size = size_of_board // grid_size  # Kích thước mỗi ô cờ
symbol_size = cell_size // 3  # Kích thước biểu tượng X, O
symbol_thickness = 8  # Độ dày đường kẻ biểu tượng
symbol_X_color = (238, 64, 53)  # Màu của X
symbol_O_color = (4, 146, 207)  # Màu của O
symbol_green_color = '#7BC043'  # Màu xanh cho chiến thắng
line_color = (0, 173, 181)  # Màu của các đường kẻ lưới
bg_color = (240, 248, 255)  # Màu nền
hover_color = (200, 220, 255)  # Màu nền khi di chuột qua
header_height = 80  # Chiều cao của phần tiêu đề
is_sound_on = sys.argv[1] == "True"

pygame.init()
pygame.mixer.init()

if not is_sound_on:
    pygame.mixer.pause()  
else:
    pygame.mixer.unpause()

# Tải âm thanh thắng
if is_sound_on:
    win_sound = pygame.mixer.Sound("sounds/win.wav")
    win_sound_played = False

    click_sound = pygame.mixer.Sound("sounds/click.wav")
else:
    pygame.mixer.pause() 

screen = pygame.display.set_mode((size_of_board, size_of_board + header_height))
pygame.display.set_caption('🎮 Game Cờ Caro 2 Người')
font = pygame.font.SysFont("Tahoma", 35, bold=True)
small_font = pygame.font.SysFont("Tahoma", 25)
font_bold = pygame.font.SysFont("Tahoma", 25, bold=True)
font_icon = pygame.font.SysFont("Segoe UI Emoji", 35)

# Vẽ tiêu đề của game
def draw_header(player_X_turn):
    pygame.draw.rect(screen, (0, 173, 181), (0, 0, size_of_board, header_height))
    text = f"Lượt: {'Người chơi 1 (X)' if player_X_turn else 'Người chơi 2 (O)'}"
    render = font.render(text, True, (255, 255, 255))
    screen.blit(render, (20, header_height // 2 - render.get_height() // 2))

# Vẽ lưới bàn cờ
def draw_grid(mouse_pos):
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * cell_size
            y = row * cell_size + header_height
            rect = pygame.Rect(x, y, cell_size, cell_size)
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, hover_color, rect)
            pygame.draw.rect(screen, line_color, rect, 1)

# Vẽ biểu tượng O
def draw_O(row, col):
    center = (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2 + header_height)
    pygame.draw.circle(screen, symbol_O_color, center, symbol_size, symbol_thickness)

# Vẽ biểu tượng X
def draw_X(row, col):
    x = col * cell_size + cell_size // 2
    y = row * cell_size + cell_size // 2 + header_height
    offset = symbol_size
    pygame.draw.line(screen, symbol_X_color, (x - offset, y - offset), (x + offset, y + offset), symbol_thickness)
    pygame.draw.line(screen, symbol_X_color, (x - offset, y + offset), (x + offset, y - offset), symbol_thickness)

# Kiểm tra xem người chơi có thắng không
def is_winner(board, player):
    for i in range(grid_size):
        for j in range(grid_size):
            if j <= grid_size - 5 and all(board[i][j + k] == player for k in range(5)):
                return [(i, j + k) for k in range(5)]  # Đường ngang
            if i <= grid_size - 5 and all(board[i + k][j] == player for k in range(5)):
                return [(i + k, j) for k in range(5)]  # Đường dọc
            if i <= grid_size - 5 and j <= grid_size - 5 and all(board[i + k][j + k] == player for k in range(5)):
                return [(i + k, j + k) for k in range(5)]  # Đường chéo trái phải
            if i <= grid_size - 5 and j >= 4 and all(board[i + k][j - k] == player for k in range(5)):
                return [(i + k, j - k) for k in range(5)]  # Đường chéo phải trái
    return None

# Hàm vẽ đường thắng
def draw_win_line(winning_positions):
    for pos in winning_positions:
        row, col = pos
        x = col * cell_size
        y = row * cell_size + header_height
        rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, symbol_green_color, rect)
    pygame.display.update() 
    pygame.time.wait(1200)  

# Kiểm tra nếu có hòa
def is_tie(board):
    return not np.any(board == 0)

# Hiển thị kết quả sau khi chơi
def display_result(text, score_X, score_O):
    overlay = pygame.Surface((size_of_board, size_of_board + header_height))
    overlay.set_alpha(240)
    overlay.fill(bg_color)
    screen.blit(overlay, (0, 0))

    if "X" in text:
        result_color = symbol_X_color
    elif "O" in text:
        result_color = symbol_O_color
    else:
        result_color = (255, 223, 0)

    emoji = "🎉" if "thắng!" in text else "🤝"
    emoji_text = font_icon.render(emoji, True, result_color)
    result_text = font.render(text[2:], True, result_color)

    screen.blit(emoji_text, (size_of_board // 2 - emoji_text.get_width() // 2 - result_text.get_width() // 2 - 20, size_of_board // 2 - 80))
    screen.blit(result_text, (size_of_board // 2 - result_text.get_width() // 2, size_of_board // 2 - 80))

    score_header_text = font_bold.render("Điểm số:", True, (0, 0, 0))
    screen.blit(score_header_text, (size_of_board // 2 - score_header_text.get_width() // 2, size_of_board // 2 + 10))

    score_margin = 10
    score_text_X = small_font.render(f"Người chơi 1 (X): {score_X}", True, symbol_X_color)
    screen.blit(score_text_X, (size_of_board // 2 - score_text_X.get_width() // 2, size_of_board // 2 + 40 + score_margin))

    score_text_O = small_font.render(f"Người chơi 2 (O): {score_O}", True, symbol_O_color)
    screen.blit(score_text_O, (size_of_board // 2 - score_text_O.get_width() // 2, size_of_board // 2 + 70 + score_margin))

    button_width = 140
    button_height = 50
    button_spacing = 40
    total_width = button_width * 2 + button_spacing
    start_x = size_of_board // 2 - total_width // 2
    y_position = size_of_board // 2 + 150

    play_again_rect = pygame.Rect(start_x, y_position, button_width, button_height)
    quit_rect = pygame.Rect(start_x + button_width + button_spacing, y_position, button_width, button_height)

    mouse_pos = pygame.mouse.get_pos()

    if play_again_rect.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        pygame.draw.rect(screen, (220, 255, 220), play_again_rect)
    else:
        pygame.draw.rect(screen, (255, 255, 255), play_again_rect)
    pygame.draw.rect(screen, (0, 128, 0), play_again_rect, 2)
    play_text = small_font.render("Chơi lại", True, (0, 128, 0))
    screen.blit(play_text, (play_again_rect.centerx - play_text.get_width() // 2, play_again_rect.centery - play_text.get_height() // 2))

    if quit_rect.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        pygame.draw.rect(screen, (255, 220, 220), quit_rect)
    else:
        pygame.draw.rect(screen, (255, 255, 255), quit_rect)
    pygame.draw.rect(screen, (255, 0, 0), quit_rect, 2)
    quit_text = small_font.render("Thoát", True, (255, 0, 0))
    screen.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2, quit_rect.centery - quit_text.get_height() // 2))

    pygame.display.update()
    return play_again_rect, quit_rect

# Hàm chính của trò chơi
def main():
    board = np.zeros((grid_size, grid_size))  # Khởi tạo bàn cờ
    player_X_turn = True  # Người chơi 1 (X) bắt đầu
    running = True  # Trạng thái chạy của game
    game_over = False  # Trạng thái kết thúc game
    winner = None  # Biến lưu trữ người chiến thắng (None: không có ai thắng, True: Người chơi X thắng, False: Người chơi O thắng)
    score_X = 0  # Điểm của người chơi 1
    score_O = 0  # Điểm của người chơi 2
    play_btn = quit_btn = None  # Nút chơi lại và thoát
    root = tk.Tk()
    root.withdraw()  # Giấu cửa sổ tkinter

    global win_sound_played

    while running:
        mouse_pos = pygame.mouse.get_pos()  # Vị trí chuột
        screen.fill(bg_color)  # Tô nền của màn hình

        if not game_over:  # Nếu game chưa kết thúc
            draw_header(player_X_turn)  # Vẽ tiêu đề
            draw_grid(mouse_pos)  # Vẽ lưới
            for row in range(grid_size):
                for col in range(grid_size):
                    if board[row][col] == -1:
                        draw_X(row, col)  # Vẽ X
                    elif board[row][col] == 1:
                        draw_O(row, col)  # Vẽ O
        else:  # Nếu game kết thúc
            if winner is None:
                result_text = "🤝 Hòa!"
            elif winner:  # Người chơi X thắng
                result_text = "🎉 Người chơi 1 (X) thắng!"
            else:  # Người chơi O thắng
                result_text = "🎉 Người chơi 2 (O) thắng!"
                
            if winner is not None and is_sound_on and not win_sound_played:
                win_sound.play()
                win_sound_played = True

            play_btn, quit_btn = display_result(result_text, score_X, score_O)

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if messagebox.askokcancel("Xác nhận thoát", "Bạn có chắc chắn muốn thoát khỏi trò chơi không?"):
                    if is_sound_on:
                        click_sound.play() 
                        pygame.time.wait(300)
                    running = False
                else:
                    if is_sound_on:
                        click_sound.play()  
                        pygame.time.wait(300)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    x, y = event.pos
                    if y > header_height:
                        col = x // cell_size
                        row = (y - header_height) // cell_size
                        if board[row][col] == 0:
                            board[row][col] = -1 if player_X_turn else 1
                            if is_sound_on:
                                click_sound.play()
                            winner_positions = is_winner(board, board[row][col])
                            if winner_positions:
                                winner = player_X_turn  # Lưu người thắng
                                if player_X_turn:
                                    score_X += 1
                                else:
                                    score_O += 1
                                game_over = True
                                draw_win_line(winner_positions)
                            elif is_tie(board):
                                game_over = True
                                winner = None  # Hòa không có người thắng
                            else:
                                player_X_turn = not player_X_turn
                else:
                    if play_btn and play_btn.collidepoint(event.pos):
                        board = np.zeros((grid_size, grid_size))
                        game_over = False
                        player_X_turn = True
                        winner = None  # Reset người thắng
                        if is_sound_on:
                            win_sound_played = False
                            click_sound.play()
                            pygame.time.wait(200)
                    elif quit_btn and quit_btn.collidepoint(event.pos):
                        if is_sound_on:
                            click_sound.play()
                            pygame.time.wait(200)
                        subprocess.Popen(["python", "caro_game.py", str(is_sound_on)])
                        running = False

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()