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

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(grid_size, grid_size))

        self.reset_board = False
        self.gameover = False
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
        player = -1 if player == 'X' else 1
        for i in range(grid_size):
            for j in range(grid_size - 4):
                if all(self.board_status[i][j + k] == player for k in range(5)):
                    return True
            for j in range(grid_size - 4):
                if all(self.board_status[j + k][i] == player for k in range(5)):
                    return True
        for i in range(grid_size - 4):
            for j in range(grid_size - 4):
                if all(self.board_status[i + k][j + k] == player for k in range(5)):
                    return True
                if all(self.board_status[i + k][j + 4 - k] == player for k in range(5)):
                    return True
        return False

    def is_tie(self):
        r, c = np.where(self.board_status == 0)
        return len(r) == 0

    def is_gameover(self):
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')
        if not self.O_wins:
            self.tie = self.is_tie()
        return self.X_wins or self.O_wins or self.tie

    def display_gameover(self):
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

    def make_ai_move(self):
        # Tìm một ô trống ngẫu nhiên cho máy
        empty_cells = list(zip(*np.where(self.board_status == 0)))
        move = random.choice(empty_cells)
        self.draw_O(move)
        self.board_status[move[0]][move[1]] = 1
        if self.is_gameover():
            self.display_gameover()

if __name__ == '__main__':
    game = TicTacToeAI()
    game.mainloop()
