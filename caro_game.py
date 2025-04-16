from tkinter import *
import os

def play_with_computer():
    os.system("python caro_bot.py")

def play_with_friend():
    os.system("python caro_2players.py")

def show_guide():
    guide = Toplevel(window)
    guide.title("📘 Hướng dẫn chơi Game Cờ Caro")
    guide.configure(bg="#f2f2f2")
    guide.geometry("500x350")
    
    Label(guide, text="📌 Hướng dẫn chơi", font=("Consolas", 20, "bold"),
          fg="#00ADB5", bg="#f2f2f2").pack(pady=15)
    
    Frame(guide, height=2, bg="#00ADB5").pack(fill=X, padx=50, pady=5)

    instructions = (
        "📍 Người chơi lần lượt đánh X hoặc O vào ô trống.\n\n"
        "🎯 Người nào có 5 ký hiệu liền kề nhau (theo hàng ngang,\n"
        "   hàng dọc hoặc chéo) là người chiến thắng.\n\n"
        "🤖 Chế độ 'Chơi với máy' sử dụng thuật toán cơ bản.\n\n"
        "👬 Chế độ 'Chơi với bạn' dành cho 2 người chơi cùng máy.\n\n"
        "💡 Chúc bạn chơi game vui vẻ!"
    )

    Label(guide, text=instructions, font=("Arial", 13),
          fg="#333333", bg="#f2f2f2", justify=LEFT).pack(padx=30, pady=10)

    # Increase button size and adjust color
    Button(guide, text="Đã hiểu 👍", command=guide.destroy,
           font=("Consolas", 14, "bold"), bg="#00A3A3", fg="white",
           width=20, height=2, bd=3, relief="ridge", activebackground="#00ADB5", activeforeground="white", cursor="hand2").pack(pady=15)

def exit_game():
    window.destroy()

# Cửa sổ chính
window = Tk()
window.title("🎮 GAME CỜ CARO - NHÓM 11 🎮")
window.configure(bg="#f2f2f2")

# Gán icon (nếu có file)
try:
    window.iconbitmap("caro_icon.ico")
except:
    pass  # không có icon cũng không sao

# Căn giữa cửa sổ lớn hơn
window_width = 700
window_height = 500
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Tiêu đề
label_title = Label(window, text="✨🎮 GAME CỜ CARO 🎮✨", font=("Consolas", 28, "bold"),
                    fg="#00ADB5", bg="#f2f2f2")
label_title.pack(pady=30)

# Frame chứa nút
frame_buttons = Frame(window, bg="#f2f2f2")
frame_buttons.pack(pady=20)

# Style nút lớn hơn
button_style = {
    "font": ("Consolas", 16, "bold"),
    "width": 25,
    "height": 2,
    "bg": "#00ADB5",
    "fg": "#f2f2f2",
    "activebackground": "#00A3A3",
    "activeforeground": "#ffffff",
    "bd": 3,
    "relief": "ridge",
    "cursor": "hand2"
}

# Các nút
btn_computer = Button(frame_buttons, text="🤖 Chơi với máy", command=play_with_computer, **button_style)
btn_computer.pack(pady=12)

btn_friend = Button(frame_buttons, text="👬 Chơi với bạn", command=play_with_friend, **button_style)
btn_friend.pack(pady=12)

btn_guide = Button(frame_buttons, text="📘 Hướng dẫn chơi", command=show_guide, **button_style)
btn_guide.pack(pady=12)

btn_exit = Button(frame_buttons, text="❌ Thoát", command=exit_game, **button_style)
btn_exit.pack(pady=12)

# Phiên bản
label_version = Label(window, text="Phiên bản nhóm 11 - 2025", font=("Arial", 12, "italic"),
                      fg="#333333", bg="#f2f2f2")
label_version.pack(pady=10)

window.mainloop()
