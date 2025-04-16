from tkinter import *
import numpy as np
import subprocess
import sys

# Constants for the game
size_of_board = 750
grid_size = 15
symbol_size = (size_of_board / grid_size - size_of_board / 8) / 2
symbol_thickness = 10
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
symbol_green_color = '#7BC043'

class TicTacToe:
    def __init__(self):
        self.window = Tk()
        self.window.title('Game Cờ Caro 2 Người')
        self.window.resizable(False, False)
        
        # Center the window on the screen
        window_width = size_of_board + 40  
        window_height = size_of_board + 100  
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        position_top = (screen_height // 2) - (window_height // 2)
        position_left = (screen_width // 2) - (window_width // 2)
        self.window.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')
        
        # Frame around the game board with a nicer background color and rounded corners
        self.frame = Frame(self.window, width=window_width, height=window_height, bg="#f0f8ff", bd=5, relief="solid", highlightbackground="#003366", highlightthickness=5)
        self.frame.pack_propagate(False)  # Prevent the frame from resizing to fit its content
        self.frame.pack(pady=20)

        self.canvas = Canvas(self.frame, width=size_of_board, height=size_of_board, bg='#e6f7ff', bd=0)
        self.canvas.pack(pady=10)

        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(grid_size, grid_size))

        self.reset_board = False
        self.gameover = False
        self.X_wins = False
        self.O_wins = False
        self.X_score = 0
        self.O_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(1, grid_size):
            self.canvas.create_line(i * size_of_board / grid_size, 0, i * size_of_board / grid_size, size_of_board, fill="#4c8d99")  
            self.canvas.create_line(0, i * size_of_board / grid_size, size_of_board, i * size_of_board / grid_size, fill="#4c8d99")  

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
            text = 'Thắng: Người chơi 1 (X)'
            color = symbol_X_color
            self.X_score += 1
        elif self.O_wins:
            text = 'Thắng: Người chơi 2 (O)'
            color = symbol_O_color
            self.O_score += 1
        else:
            text = 'Hoà'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 4, font="Arial 30 bold", fill=color, text=text)
        
        # Display score with stylish text
        score_text = f"Điểm số - X: {self.X_score} | O: {self.O_score}"
        self.canvas.create_text(size_of_board / 2, size_of_board / 2, font="Arial 20 bold", fill="black", text=score_text)
        
        # Buttons with better positioning and styling
        self.canvas.create_text(size_of_board / 2, size_of_board / 1.5, font="Arial 20 bold", fill="green", text="Chơi lại", tags="reset", activefill="limegreen")
        self.canvas.create_text(size_of_board / 2, size_of_board / 1.3, font="Arial 20 bold", fill="red", text="Thoát", tags="exit", activefill="darkred")

        self.window.bind("<Button-1>", self.restart_game)
        self.reset_board = True

    def restart_game(self, event):
        if self.reset_board:
            # Check the position of the "Chơi lại" button
            if size_of_board / 2 - 50 < event.x < size_of_board / 2 + 50 and size_of_board / 1.5 - 20 < event.y < size_of_board / 1.5 + 20:
                self.reset_board = False
                self.window.bind('<Button-1>', self.click)
                self.canvas.delete("all")
                self.board_status = np.zeros(shape=(grid_size, grid_size))  # Reset the board
                self.initialize_board()  
                self.player_X_turns = True 
            # Check the position of the "Thoát" button
            elif size_of_board / 2 - 50 < event.x < size_of_board / 2 + 50 and size_of_board / 1.3 - 20 < event.y < size_of_board / 1.3 + 20:
                self.window.destroy()
                subprocess.Popen([sys.executable, "caro_game.py"], shell=True)

    def click(self, event):
        if not self.reset_board:
            grid_position = [event.x, event.y]
            logical_position = self.convert_grid_to_logical_position(grid_position)

            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_X_turns = not self.player_X_turns
            else:
                if not self.is_grid_occupied(logical_position):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = not self.player_X_turns

            if self.is_gameover():
                self.display_gameover()

if __name__ == '__main__':
    game = TicTacToe()
    game.mainloop()
