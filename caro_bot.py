from tkinter import *
import numpy as np
import random

# Các tham số và cấu hình giống như trên
size_of_board = 750
grid_size = 15
symbol_size = (size_of_board / grid_size - size_of_board / 8) / 2
symbol_thickness = 10
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
symbol_green_color = '#7BC043'

class TicTacToeAI:
    def __init__(self):
        self.window = Tk()
        self.window.title('Cờ Caro Chơi với Bot')
        self.window.resizable(False, False)
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.winning_cells = []

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(grid_size, grid_size))

        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        if not self.player_X_turns:
            self.make_ai_move()

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(1, grid_size):
            self.canvas.create_line(i * size_of_board / grid_size, 0, i * size_of_board / grid_size, size_of_board)
            self.canvas.create_line(0, i * size_of_board / grid_size, size_of_board, i * size_of_board / grid_size)

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        grid_position = self.convert_logical_to_grid_position(logical_position)
        radius = symbol_size
        self.canvas.create_oval(
            grid_position[0] - radius, grid_position[1] - radius,
            grid_position[0] + radius, grid_position[1] + radius,
            width=symbol_thickness, outline=symbol_O_color
        )

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        offset = symbol_size
        self.canvas.create_line(
            grid_position[0] - offset, grid_position[1] - offset,
            grid_position[0] + offset, grid_position[1] + offset,
            width=symbol_thickness, fill=symbol_X_color
        )
        self.canvas.create_line(
            grid_position[0] - offset, grid_position[1] + offset,
            grid_position[0] + offset, grid_position[1] - offset,
            width=symbol_thickness, fill=symbol_X_color
        )

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / grid_size) * logical_position + size_of_board / (2 * grid_size)

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / grid_size), dtype=int)

    def is_grid_occupied(self, logical_position):
        return self.board_status[logical_position[0]][logical_position[1]] != 0

    def is_winner(self, player):
        player_val = -1 if player == 'X' else 1
        for i in range(grid_size):
            for j in range(grid_size - 4):
                if all(self.board_status[i][j + k] == player_val for k in range(5)):
                    return [(i, j + k) for k in range(5)]
            for j in range(grid_size - 4):
                if all(self.board_status[j + k][i] == player_val for k in range(5)):
                    return [(j + k, i) for k in range(5)]
        for i in range(grid_size - 4):
            for j in range(grid_size - 4):
                if all(self.board_status[i + k][j + k] == player_val for k in range(5)):
                    return [(i + k, j + k) for k in range(5)]
                if all(self.board_status[i + k][j + 4 - k] == player_val for k in range(5)):
                    return [(i + k, j + 4 - k) for k in range(5)]
        return None


    def is_tie(self):
        r, c = np.where(self.board_status == 0)
        return len(r) == 0

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


    def display_gameover(self):
        self.highlight_winning_cells()
        self.window.after(1000, self.show_result)

    def show_result(self):
        if self.X_wins:
            text = 'Thắng: Người chơi (X)'
            color = symbol_X_color
        elif self.O_wins:
            text = 'Thắng: Máy (O)'
            color = symbol_O_color
        else:
            text = 'Hoà'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 30 bold", fill=color, text=text)
        self.reset_board = True

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_X_turns = not self.player_X_turns
                    if not self.is_gameover():
                        self.make_ai_move()

            if self.is_gameover():
                self.display_gameover()
        else:
            self.canvas.delete("all")
            self.reset_board = False
            self.board_status = np.zeros(shape=(grid_size, grid_size))
            self.player_X_turns = True
            self.initialize_board()

    def highlight_winning_cells(self):
        for cell in self.winning_cells:
            grid_pos = self.convert_logical_to_grid_position(cell)
            radius = symbol_size / 2
            self.canvas.create_oval(
                grid_pos[0] - radius, grid_pos[1] - radius,
                grid_pos[0] + radius, grid_pos[1] + radius,
                fill=symbol_green_color, outline=""
            )


    def make_ai_move(self):
        ai = HeuristicAI(self.board_status, grid_size)
        move = ai.find_best_move()
        if move:
            self.draw_O(move)
            self.board_status[move[0]][move[1]] = 1
            if self.is_gameover():
                self.display_gameover()
            else:
                self.player_X_turns = True


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
        max_len = 0
        count = 1  # vị trí (x, y)
        open_ends = 0

        # Forward
        i = 1
        while True:
            nx, ny = x + dx*i, y + dy*i
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

        # Backward
        i = 1
        while True:
            nx, ny = x - dx*i, y - dy*i
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
            return self.score_table.get((5, 'open'))

        if open_ends == 2:
            status = 'open'
        elif open_ends == 1:
            status = 'half'
        else:
            return 0

        return self.score_table.get((count, status), 0)

    def evaluate_move(self, x, y, player):
        score = 0
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        for dx, dy in directions:
            score += self.evaluate_direction(x, y, dx, dy, player)
        return score

    def find_best_move(self):
        empty_cells = list(zip(*np.where(self.board_status == 0)))
        best_score = -1
        best_move = None
        for x, y in empty_cells:
            # bỏ qua ô quá xa (tối ưu hóa)
            if not self.has_neighbor(x, y): continue

            attack_score = self.evaluate_move(x, y, 1)
            defend_score = self.evaluate_move(x, y, -1)
            score = attack_score + 0.8 * defend_score

            # thêm bonus gần trung tâm
            center = self.grid_size / 2
            dist = abs(x - center) + abs(y - center)
            score += (15 - dist)

            if score > best_score:
                best_score = score
                best_move = (x, y)
        return best_move

    def has_neighbor(self, x, y, distance=2):
        for dx in range(-distance, distance+1):
            for dy in range(-distance, distance+1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    if self.board_status[nx][ny] != 0:
                        return True
        return False


if __name__ == '__main__':
    game = TicTacToeAI()
    game.mainloop()
