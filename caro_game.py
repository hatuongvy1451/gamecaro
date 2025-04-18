import pygame
import sys
import subprocess

# Khởi tạo pygame
pygame.init()

# Màu sắc
WHITE = (255, 255, 255)
BG_COLOR = (242, 242, 242)
BTN_COLOR = (0, 173, 181)
BTN_HOVER = (0, 163, 163)
TEXT_COLOR = (255, 255, 255)
TEXT_COLOR_1 = (0, 0, 0)

# Kích thước màn hình
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎮 GAME CỜ CARO - NHÓM 11 🎮")

# Font
font_title_icon = pygame.font.SysFont("Segoe UI Emoji", 38)
font_title_text = pygame.font.SysFont("Tahoma", 28, bold=True)
font_text = pygame.font.SysFont("Tahoma", 22, bold=True)
font_text_1 = pygame.font.SysFont("Tahoma", 20)
font_footer = pygame.font.SysFont("Tahoma", 16)
font_icon = pygame.font.SysFont("Segoe UI Emoji", 32)

class Button:
    def __init__(self, x, y, icon, text, action=None, width=300, height=60):
        self.x = x
        self.y = y
        self.icon = icon
        self.text = text
        self.action = action
        self.width = width
        self.height = height
        self.is_hovered = False  # Để lưu trạng thái của nút

    def draw(self, surface, mouse_pos):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        is_hovered = rect.collidepoint(mouse_pos)
        if is_hovered != self.is_hovered:  # Kiểm tra xem trạng thái hover có thay đổi không
            self.is_hovered = is_hovered
            # Thay đổi con trỏ chuột chỉ khi trạng thái hover thay đổi
            if self.is_hovered:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Đặt con trỏ thành hình bàn tay
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Đặt lại con trỏ mặc định

        # Vẽ nút
        color = BTN_HOVER if self.is_hovered else BTN_COLOR
        pygame.draw.rect(surface, color, rect, border_radius=12)

        # Vẽ icon
        icon_render = font_icon.render(self.icon, True, TEXT_COLOR)
        surface.blit(icon_render, (self.x + 20, self.y + 15))

        # Vẽ text
        text_render = font_text.render(self.text, True, TEXT_COLOR)
        surface.blit(text_render, (self.x + 70, self.y + 18))

        return rect

    def handle_event(self, event, mouse_pos):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            if self.action:
                self.action()

# Hành động
def play_with_computer():
    subprocess.Popen(["python", "caro_bot.py"])
    pygame.quit()
    sys.exit()

def play_with_friend():
    subprocess.Popen(["python", "caro_2players.py"])
    pygame.quit()
    sys.exit()

def show_guide():
    guide_running = True
    while guide_running:
        screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        # Vẽ tiêu đề
        title_icon_left = font_title_icon.render("📘", True, BTN_COLOR)
        title_text = font_title_text.render("Hướng dẫn chơi", True, BTN_COLOR)

        total_width = title_icon_left.get_width() + title_text.get_width()
        x_start = WIDTH // 2 - total_width // 2
        screen.blit(title_icon_left, (x_start, 50))
        screen.blit(title_text, (x_start + title_icon_left.get_width(), 50))

        # Tách icon và text trong instructions
        instructions = [
            ("📍", "Người chơi lần lượt đánh X hoặc O vào ô trống."),
            ("🎯", "Người nào có 5 ký hiệu liền kề nhau (theo hàng ngang,"),
            ("", "hàng dọc hoặc chéo) là người chiến thắng."),
            ("🤖", "Chế độ 'Chơi với máy' sử dụng thuật toán cơ bản."),
            ("👬", "Chế độ 'Chơi với bạn' dành cho 2 người chơi cùng máy."),
            ("💡", "Chúc bạn chơi game vui vẻ!")
        ]
        
        y_offset = 130  
        margin_left = 95  
        for icon, text in instructions:
            icon_render = font_icon.render(icon, True, TEXT_COLOR_1)
            text_render = font_text_1.render(text, True, TEXT_COLOR_1)
            
            screen.blit(icon_render, (margin_left, y_offset))
            screen.blit(text_render, (margin_left + icon_render.get_width() + 10, y_offset))
            y_offset += 40

        # Nút "Đã hiểu"
        button_width = 200
        button_x = (WIDTH - button_width) // 2
        understand_button = Button(button_x, HEIGHT - 100, "👍", "Đã hiểu", show_main_menu, width=200)
        understand_button.draw(screen, mouse_pos)

        # Sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                guide_running = False

            understand_button.handle_event(event, mouse_pos)

        pygame.display.flip()

def show_main_menu():
    running = True  # Set the main loop to be active
    while running:
        screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        # Vẽ tiêu đề: icon - text - icon
        title_icon_left = font_title_icon.render("✨🎮", True, BTN_COLOR)
        title_text = font_title_text.render(" GAME CỜ CARO ", True, BTN_COLOR)
        title_icon_right = font_title_icon.render("🎮✨", True, BTN_COLOR)

        total_width = title_icon_left.get_width() + title_text.get_width() + title_icon_right.get_width()
        x_start = WIDTH // 2 - total_width // 2
        screen.blit(title_icon_left, (x_start, 50))
        screen.blit(title_text, (x_start + title_icon_left.get_width(), 50))
        screen.blit(title_icon_right, (x_start + title_icon_left.get_width() + title_text.get_width(), 50))

        # Vẽ các nút trong menu
        for btn in buttons:
            btn.draw(screen, mouse_pos)

        # Footer (canh lề ở dưới)
        version = font_footer.render("Phiên bản nhóm 11 - 2025", True, (51, 51, 51))
        screen.blit(version, (WIDTH // 2 - version.get_width() // 2, HEIGHT - 30))

        # Sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for btn in buttons:
                btn.handle_event(event, mouse_pos)

        pygame.display.flip()

def exit_game():
    pygame.quit()
    sys.exit()

# Tạo nút
buttons = [
    Button(WIDTH // 2 - 150, 150, "🤖", "Chơi với máy", play_with_computer),
    Button(WIDTH // 2 - 150, 230, "👬", "Chơi với bạn", play_with_friend),
    Button(WIDTH // 2 - 150, 310, "📘", "Hướng dẫn chơi", show_guide),
    Button(WIDTH // 2 - 150, 390, "❌", "Thoát", exit_game)
]

show_main_menu()
