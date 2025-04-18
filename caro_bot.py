import asyncio
import platform
import pygame
import os #quản lý hệ thống
import sys #quản lý hệ thống 
import numpy as np
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Cấu hình giao diện
size_of_board = 750
grid_size = 15
cell_size = size_of_board // grid_size
symbol_size = cell_size // 3
symbol_thickness = 8
symbol_X_color = (238, 64, 53)  # #EE4035
symbol_O_color = (4, 146, 207)  # #0492CF
symbol_green_color = (124, 252, 0)  # #7CFC00
line_color = (0, 173, 181)
bg_color = (240, 248, 255)
hover_color = (200, 220, 255)
header_height = 80
FPS = 60
AI_MOVE_DELAY = 1  # Độ trễ cho nước đi của máy (giây)
WIN_DISPLAY_DELAY = 1  # Độ trễ hiển thị đường thắng (giây)

class TicTacToeAI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((size_of_board, size_of_board + header_height))
        pygame.display.set_caption('🎮 Game Cờ Caro Chơi với Máy')
        self.clock = pygame.time.Clock()
        self.running = True
        self.player_X_turns = True
        self.board_status = np.zeros((grid_size, grid_size))
        self.reset_board = False
        self.X_score = 0
        self.O_score = 0
        self.X_wins = False
        self.O_wins = False
        self.tie = False
        self.winning_cells = []
        self.score_updated = False
        self.showing_win = False  # Cờ để theo dõi trạng thái hiển thị đường thắng
        self.font = pygame.font.SysFont("Tahoma", 35, bold=True)
        self.small_font = pygame.font.SysFont("Tahoma", 25)
        self.font_bold = pygame.font.SysFont("Tahoma", 25, bold=True)
        self.font_icon = pygame.font.SysFont("Segoe UI Emoji", 35)

    def draw_header(self):
        pygame.draw.rect(self.screen, (0, 173, 181), (0, 0, size_of_board, header_height))
        text = f"Lượt: {'Người chơi (X)' if self.player_X_turns else 'Máy (O)'}"
        render = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(render, (20, header_height // 2 - render.get_height() // 2))

    def draw_grid(self, mouse_pos):
        for row in range(grid_size):
            for col in range(grid_size):
                x = col * cell_size
                y = row * cell_size + header_height
                rect = pygame.Rect(x, y, cell_size, cell_size)
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, hover_color, rect)
                pygame.draw.rect(self.screen, line_color, rect, 1)

    def draw_X(self, pos):
        x, y = self.convert_logical_to_grid_position(pos)
        offset = symbol_size
        pygame.draw.line(self.screen, symbol_X_color, (x - offset, y - offset), (x + offset, y + offset), symbol_thickness)
        pygame.draw.line(self.screen, symbol_X_color, (x - offset, y + offset), (x + offset, y - offset), symbol_thickness)

    def draw_O(self, pos):
        x, y = self.convert_logical_to_grid_position(pos)
        pygame.draw.circle(self.screen, symbol_O_color, (int(x), int(y)), symbol_size, symbol_thickness)

    def convert_logical_to_grid_position(self, pos):
        return (cell_size * pos[1] + cell_size // 2, cell_size * pos[0] + cell_size // 2 + header_height)

    def convert_grid_to_logical_position(self, pos):
        return (int((pos[1] - header_height) // cell_size), int(pos[0] // cell_size))

    def is_grid_occupied(self, pos):
        return self.board_status[int(pos[0])][int(pos[1])] != 0

    def is_winner(self, player):
        p = -1 if player == 'X' else 1
        for i in range(grid_size):
            for j in range(grid_size - 4):
                if all(self.board_status[i][j + k] == p for k in range(5)):
                    return [(i, j + k) for k in range(5)]
                if all(self.board_status[j + k][i] == p for k in range(5)):
                    return [(j + k, i) for k in range(5)]
        for i in range(grid_size - 4):
            for j in range(grid_size - 4):
                if all(self.board_status[i + k][j + k] == p for k in range(5)):
                    return [(i + k, j + k) for k in range(5)]
                if all(self.board_status[i + k][j + 4 - k] == p for k in range(5)):
                    return [(i + k, j + 4 - k) for k in range(5)]
        return None

    def highlight_winning_cells(self):
        for cell in self.winning_cells:
            x, y = self.convert_logical_to_grid_position(cell)
            radius = symbol_size / 2
            pygame.draw.circle(self.screen, symbol_green_color, (int(x), int(y)), int(radius))

    def is_tie(self):
        return not np.any(self.board_status == 0)

    def is_gameover(self):
        win_X = self.is_winner('X')
        if win_X:
            self.X_wins = True
            self.winning_cells = win_X
            return True
        win_O = self.is_winner('O')
        if win_O:
            self.O_wins = True
            self.winning_cells = win_O
            return True
        if self.is_tie():
            self.tie = True
            return True
        return False

    def show_result(self):
        if not self.score_updated:
            if self.X_wins:
                self.X_score += 1
            elif self.O_wins:
                self.O_score += 1
            self.score_updated = True

        # Define result text and color based on win conditions
        if self.X_wins:
            text = 'Người chơi (X) thắng!'
            color = symbol_X_color
            emoji = "🎉"
        elif self.O_wins:
            text = 'Máy (O) thắng!'
            color = symbol_O_color
            emoji = "🎉"
        else:
            text = 'Hòa!'
            color = (255, 223, 0)
            emoji = "🤝"

        # Create overlay for result display
        overlay = pygame.Surface((size_of_board, size_of_board + header_height))
        overlay.set_alpha(240)
        overlay.fill(bg_color)
        self.screen.blit(overlay, (0, 0))

        # Create emoji and result text
        emoji_text = self.font_icon.render(emoji, True, color)
        result_text = self.font.render(text, True, color)

        # Draw emoji and result text separately, with padding between them
        self.screen.blit(emoji_text, (size_of_board // 2 - emoji_text.get_width() // 2 - result_text.get_width() // 2 - 20, size_of_board // 2 - 80))
        self.screen.blit(result_text, (size_of_board // 2 - result_text.get_width() // 2, size_of_board // 2 - 80))

        # Score display
        score_header_text = self.font_bold.render("Điểm số:", True, (0, 0, 0))
        self.screen.blit(score_header_text, (size_of_board // 2 - score_header_text.get_width() // 2,
                                            size_of_board // 2 + 10))

        score_margin = 10  # Add a little margin between score texts
        score_text_X = self.small_font.render(f"Người chơi (X): {self.X_score}", True, symbol_X_color)
        self.screen.blit(score_text_X, (size_of_board // 2 - score_text_X.get_width() // 2,
                                    size_of_board // 2 + 40 + score_margin))

        score_text_O = self.small_font.render(f"Máy (O): {self.O_score}", True, symbol_O_color)
        self.screen.blit(score_text_O, (size_of_board // 2 - score_text_O.get_width() // 2,
                                    size_of_board // 2 + 70 + score_margin))

        # Button dimensions
        button_width = 140
        button_height = 50
        button_spacing = 40
        total_width = button_width * 2 + button_spacing
        start_x = size_of_board // 2 - total_width // 2
        y_position = size_of_board // 2 + 150

        # Play again and quit button positions
        self.play_again_rect = pygame.Rect(start_x, y_position, button_width, button_height)
        self.quit_rect = pygame.Rect(start_x + button_width + button_spacing, y_position, button_width, button_height)

        mouse_pos = pygame.mouse.get_pos()
        cursor_changed = False

        # -------- Play Again Button --------
        if self.play_again_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            cursor_changed = True
            pygame.draw.rect(self.screen, (220, 255, 220), self.play_again_rect)  # Hover effect: light green
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.play_again_rect)  # Normal white background

        pygame.draw.rect(self.screen, (0, 128, 0), self.play_again_rect, 2)  # Green border
        play_text = self.small_font.render("Chơi lại", True, (0, 128, 0))
        self.screen.blit(play_text, (
            self.play_again_rect.centerx - play_text.get_width() // 2,
            self.play_again_rect.centery - play_text.get_height() // 2)
        )

        # -------- Quit Button --------
        if self.quit_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            cursor_changed = True
            pygame.draw.rect(self.screen, (255, 220, 220), self.quit_rect)  # Hover effect: light red
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.quit_rect)  # Normal white background

        pygame.draw.rect(self.screen, (255, 0, 0), self.quit_rect, 2)  # Red border
        quit_text = self.small_font.render("Thoát", True, (255, 0, 0))
        self.screen.blit(quit_text, (
            self.quit_rect.centerx - quit_text.get_width() // 2,
            self.quit_rect.centery - quit_text.get_height() // 2)
        )

        if not cursor_changed:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def restart_game(self, pos):
        if self.play_again_rect.collidepoint(pos):
            logging.info("Restarting game")
            self.screen.fill(bg_color)
            self.board_status = np.zeros((grid_size, grid_size))
            self.player_X_turns = True
            self.reset_board = False
            self.X_wins = False
            self.O_wins = False
            self.tie = False
            self.winning_cells = []
            self.score_updated = False
            self.showing_win = False
        elif self.quit_rect.collidepoint(pos):
            logging.info("Exiting game")
            self.running = False
            os.execl(sys.executable, sys.executable, 'caro_game.py')

    def click(self, pos):
        logical_pos = self.convert_grid_to_logical_position(pos)
        if 0 <= logical_pos[0] < grid_size and 0 <= logical_pos[1] < grid_size and pos[1] > header_height:
            if not self.reset_board and self.player_X_turns and not self.is_grid_occupied(logical_pos):
                self.draw_X(logical_pos)
                self.board_status[logical_pos[0]][logical_pos[1]] = -1
                self.player_X_turns = False
                if self.is_gameover():
                    self.showing_win = True
                else:
                    asyncio.ensure_future(self.make_ai_move())

    async def make_ai_move(self):
        await asyncio.sleep(AI_MOVE_DELAY)
        ai = HeuristicAI(self.board_status, grid_size)
        move = ai.find_best_move()
        if move:
            self.draw_O(move)
            self.board_status[move[0]][move[1]] = 1
            if self.is_gameover():
                self.showing_win = True
            else:
                self.player_X_turns = True
        else:
            logging.warning("AI could not find a valid move")

    async def main(self):
        self.screen.fill(bg_color)
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(bg_color)

            if self.showing_win:
                # Hiển thị đường thắng
                self.draw_header()
                self.draw_grid(mouse_pos)
                for row in range(grid_size):
                    for col in range(grid_size):
                        if self.board_status[row][col] == -1:
                            self.draw_X((row, col))
                        elif self.board_status[row][col] == 1:
                            self.draw_O((row, col))
                if self.winning_cells:
                    self.highlight_winning_cells()
                pygame.display.flip()
                await asyncio.sleep(WIN_DISPLAY_DELAY)  # Chờ để hiển thị đường thắng
                self.showing_win = False
                self.reset_board = True

            elif not self.reset_board:
                self.draw_header()
                self.draw_grid(mouse_pos)
                for row in range(grid_size):
                    for col in range(grid_size):
                        if self.board_status[row][col] == -1:
                            self.draw_X((row, col))
                        elif self.board_status[row][col] == 1:
                            self.draw_O((row, col))
            else:
                self.show_result()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logging.info("Quitting game")
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.reset_board:
                        self.restart_game(event.pos)
                    else:
                        self.click(event.pos)

            self.clock.tick(FPS)
            pygame.display.flip()
            await asyncio.sleep(1.0 / FPS)

class HeuristicAI:
    def __init__(self, board_status, grid_size):
        self.board_status = board_status
        self.grid_size = grid_size
        self.score_table = {
            (2, 'open'): 100,
            (2, 'half'): 10,
            (3, 'open'): 1000,
            (3, 'half'): 100,
            (4, 'open'): 10000,
            (4, 'half'): 1000,
            (5, 'open'): 1000000
        }

    def evaluate_direction(self, x, y, dx, dy, player):
        count = 1
        open_ends = 0
        i = 1
        while True:
            nx, ny = x + dx * i, y + dy * i
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                val = self.board_status[nx][ny]
                if val == player:
                    count += 1
                elif val == 0:
                    open_ends += 1
                    break
                else:
                    break
            else:
                break
            i += 1
        i = 1
        while True:
            nx, ny = x - dx * i, y - dy * i
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                val = self.board_status[nx][ny]
                if val == player:
                    count += 1
                elif val == 0:
                    open_ends += 1
                    break
                else:
                    break
            else:
                break
            i += 1
        if count >= 5:
            return self.score_table.get((5, 'open'), 0)
        if open_ends == 2:
            status = 'open'
        elif open_ends == 1:
            status = 'half'
        else:
            return 0
        return self.score_table.get((count, status), 0)

    def evaluate_move(self, x, y, player):
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            score += self.evaluate_direction(x, y, dx, dy, player)
        return score

    def find_best_move(self):
        empty_cells = list(zip(*np.where(self.board_status == 0)))
        if not empty_cells:
            logging.warning("No empty cells available")
            return None
        best_score = -1
        best_move = None
        for x, y in empty_cells:
            attack_score = self.evaluate_move(x, y, 1)
            defend_score = self.evaluate_move(x, y, -1)
            score = attack_score + 0.8 * defend_score
            center = self.grid_size / 2
            dist = abs(x - center) + abs(y - center)
            score += (15 - dist)
            if score > best_score:
                best_score = score
                best_move = (x, y)
        if best_move is None:
            center = self.grid_size // 2
            if self.board_status[center][center] == 0:
                best_move = (center, center)
            else:
                best_move = empty_cells[0]
        return best_move

if platform.system() == "Emscripten":
    async def main():
        game = TicTacToeAI()
        await game.main()
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        try:
            game = TicTacToeAI()
            asyncio.run(game.main())
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            pygame.quit()
            sys.exit(1)