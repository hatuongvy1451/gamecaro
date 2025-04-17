from tkinter import *
import numpy as np
import subprocess
import sys

# Cấu hình giao diện
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

        # Căn giữa cửa sổ
        window_width = size_of_board + 40
        window_height = size_of_board + 100
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        position_top = (screen_height // 2) - (window_height // 2)
        position_left = (screen_width // 2) - (window_width // 2)
        self.window.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

        # Khung chứa canvas
        self.frame = Frame(self.window, width=window_width, height=window_height, bg="#f0f8ff",
                           bd=5, relief="solid", highlightbackground="#003366", highlightthickness=5)
        self.frame.pack_propagate(False)
        self.frame.pack(pady=20)

        self.canvas = Canvas(self.frame, width=size_of_board, height=size_of_board, bg='#e6f7ff', bd=0)
        self.canvas.pack(pady=10)

        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros((grid_size, grid_size))
        self.reset_board = False
        self.X_score = 0
        self.O_score = 0
        self.X_wins = False
        self.O_wins = False
        self.tie = False
        self.winning_cells = []
        self.window.bind("<Motion>", self.on_hover_buttons)
        self.hover_state = None


    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(1, grid_size):
            self.canvas.create_line(i * size_of_board / grid_size, 0, i * size_of_board / grid_size, size_of_board, fill="#4c8d99")
            self.canvas.create_line(0, i * size_of_board / grid_size, size_of_board, i * size_of_board / grid_size, fill="#4c8d99")

    def draw_X(self, pos):
        x, y = self.convert_logical_to_grid_position(pos)
        offset = symbol_size
        self.canvas.create_line(x - offset, y - offset, x + offset, y + offset, width=symbol_thickness, fill=symbol_X_color)
        self.canvas.create_line(x - offset, y + offset, x + offset, y - offset, width=symbol_thickness, fill=symbol_X_color)

    def draw_O(self, pos):
        x, y = self.convert_logical_to_grid_position(pos)
        radius = symbol_size
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, width=symbol_thickness, outline=symbol_O_color)

    def convert_logical_to_grid_position(self, pos):
        return (size_of_board / grid_size) * np.array(pos) + size_of_board / (2 * grid_size)

    def convert_grid_to_logical_position(self, pos):
        return np.array(pos) // (size_of_board / grid_size)

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
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=symbol_green_color, outline="")

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

    def display_gameover(self):
        if self.winning_cells:
            self.highlight_winning_cells()
            self.window.after(1000, self.show_result)
        else:
            self.show_result()

    def show_result(self):
        if self.X_wins:
            text = 'Thắng: Người chơi (X)'
            color = symbol_X_color
            self.X_score += 1
        elif self.O_wins:
            text = 'Thắng: Máy (O)'
            color = symbol_O_color
            self.O_score += 1
        else:
            text = 'Hoà'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 4, font="Arial 30 bold", fill=color, text=text)

        # Hiển thị điểm số
        score_text = f"Điểm số\nX: {self.X_score}\nO: {self.O_score}"
        self.canvas.create_text(size_of_board / 2, size_of_board / 2, font="Arial 20 bold", fill="black", text=score_text)

        # Tọa độ nút
        btn_width = 150
        btn_height = 50

        # Vẽ nút "Chơi lại"
        x1 = size_of_board / 2 - btn_width / 2
        y1 = size_of_board / 1.5 - btn_height / 2
        x2 = x1 + btn_width
        y2 = y1 + btn_height
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="green", width=3, tags="reset_box")
        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="Chơi lại", fill="green",
                                font="Arial 20 bold", tags="reset")

        # Vẽ nút "Thoát"
        x1 = size_of_board / 2 - btn_width / 2
        y1 = size_of_board / 1.3 - btn_height / 2
        x2 = x1 + btn_width
        y2 = y1 + btn_height
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="red", width=3, tags="exit_box")
        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="Thoát", fill="red",
                                font="Arial 20 bold", tags="exit")

        self.window.bind("<Button-1>", self.restart_game)
        self.reset_board = True

    def on_hover_buttons(self, event):
        if not self.reset_board:
            return

        x, y = event.x, event.y
        btn_width = 150
        btn_height = 50

        # Vị trí nút
        rx1 = size_of_board / 2 - btn_width / 2
        ry1 = size_of_board / 1.5 - btn_height / 2
        rx2 = rx1 + btn_width
        ry2 = ry1 + btn_height

        ex1 = size_of_board / 2 - btn_width / 2
        ey1 = size_of_board / 1.3 - btn_height / 2
        ex2 = ex1 + btn_width
        ey2 = ey1 + btn_height

        # Kiểm tra nếu chuột đang hover vào đâu
        if rx1 < x < rx2 and ry1 < y < ry2:
            if self.hover_state != 'reset':
                self.canvas.itemconfig("reset_box", fill="#ccffcc")  # nền xanh nhạt
                self.canvas.itemconfig("exit_box", fill="white")     # khôi phục nút kia
                self.hover_state = 'reset'
        elif ex1 < x < ex2 and ey1 < y < ey2:
            if self.hover_state != 'exit':
                self.canvas.itemconfig("exit_box", fill="#ffcccc")   # nền đỏ nhạt
                self.canvas.itemconfig("reset_box", fill="white")    # khôi phục nút kia
                self.hover_state = 'exit'
        else:
            if self.hover_state is not None:
                self.canvas.itemconfig("reset_box", fill="white")
                self.canvas.itemconfig("exit_box", fill="white")
                self.hover_state = None


    def restart_game(self, event):
        x, y = event.x, event.y

        # Nút "Chơi lại"
        btn_width = 150
        btn_height = 50
        rx1 = size_of_board / 2 - btn_width / 2
        ry1 = size_of_board / 1.5 - btn_height / 2
        rx2 = rx1 + btn_width
        ry2 = ry1 + btn_height

        # Nút "Thoát"
        ex1 = size_of_board / 2 - btn_width / 2
        ey1 = size_of_board / 1.3 - btn_height / 2
        ex2 = ex1 + btn_width
        ey2 = ey1 + btn_height

        if rx1 < x < rx2 and ry1 < y < ry2:
            self.canvas.delete("all")
            self.initialize_board()
            self.board_status = np.zeros((grid_size, grid_size))
            self.player_X_turns = True
            self.reset_board = False
            self.X_wins = False
            self.O_wins = False
            self.tie = False
            self.winning_cells = []
            self.window.bind("<Button-1>", self.click)

        elif ex1 < x < ex2 and ey1 < y < ey2:
            self.window.destroy()
            subprocess.Popen([sys.executable, "caro_game.py"], shell=True)



    def click(self, event):
        grid_pos = [event.x, event.y]
        logical_pos = self.convert_grid_to_logical_position(grid_pos).astype(int)

        if not self.reset_board:
            if self.player_X_turns and not self.is_grid_occupied(logical_pos):
                self.draw_X(logical_pos)
                self.board_status[logical_pos[0]][logical_pos[1]] = -1
                self.player_X_turns = False
                if not self.is_gameover():
                    self.make_ai_move()
            if self.is_gameover() and not self.reset_board:
                self.reset_board = True  # Ngăn gọi lại lần nữa
                self.display_gameover()


    def make_ai_move(self):
        ai = HeuristicAI(self.board_status, grid_size)
        move = ai.find_best_move()
        if move:
            self.draw_O(move)
            self.board_status[move[0]][move[1]] = 1
            if self.is_gameover() and not self.reset_board:
                self.reset_board = True
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