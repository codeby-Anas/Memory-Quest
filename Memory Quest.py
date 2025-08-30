import tkinter as tk
import random
import time
import platform

if platform.system() == "Windows":
    import winsound

def play_sound(success=True):
    if platform.system() == "Windows":
        if success:
            winsound.MessageBeep(winsound.MB_OK)
        else:
            winsound.MessageBeep(winsound.MB_ICONHAND)

EMOJI_COLORS = [
    "#ff9999", "#99ccff", "#99ff99", "#ffff99", "#ffcc99", "#c299ff",
    "#ffc0cb", "#add8e6", "#f0e68c", "#e6e6fa", "#ffb6c1", "#b0e0e6",
    "#98fb98", "#dda0dd", "#f5deb3", "#d8bfd8", "#ffe4e1", "#e0ffff",
    "#fafad2", "#c1ffc1", "#f08080", "#87cefa", "#ffd700", "#7fffd4"
]

class MemoryCanvasGame:
    def __init__(self, root, size=4):
        self.root = root
        self.size = size
        self.cell_size = 100
        self.padding = 10

        canvas_width = size * (self.cell_size + self.padding)
        canvas_height = size * (self.cell_size + self.padding)
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="#f0f0f0")
        self.canvas.pack()

        emojis = ["🍎", "🍌", "🍇", "🍒", "🍉", "🍋", "🥝", "🍍",
                  "🐶", "🐱", "🐰", "🐼", "🦁", "🐸", "🐵", "🐤",
                  "❤️", "💙", "💚", "💜", "🧡", "💛", "🤍", "🖤"]

        total_pairs = (size * size) // 2
        self.symbols = emojis[:total_pairs] * 2
        random.shuffle(self.symbols)

        self.symbol_colors = {}
        for i, symbol in enumerate(set(self.symbols)):
            self.symbol_colors[symbol] = EMOJI_COLORS[i % len(EMOJI_COLORS)]

        self.rect_items = []
        self.text_items = []
        self.revealed = [False] * len(self.symbols)
        self.first_card = None
        self.attempts = 0
        self.matches = 0
        self.timer_running = False
        self.start_time = None

        self.draw_board()

        self.status_label = tk.Label(root, text="المحاولات: 0 | الوقت: 0 ث", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.restart_button = tk.Button(root, text="🔄 إعادة اللعبة", font=("Arial", 12), command=self.restart_game)
        self.restart_button.pack(pady=5)

        self.update_timer()

    def draw_board(self):
        self.canvas.delete("all")
        self.rect_items.clear()
        self.text_items.clear()
        self.revealed = [False] * len(self.symbols)
        self.first_card = None
        self.attempts = 0
        self.matches = 0
        self.timer_running = False
        self.start_time = None

        for i in range(self.size * self.size):
            row = i // self.size
            col = i % self.size
            x1 = col * (self.cell_size + self.padding)
            y1 = row * (self.cell_size + self.padding)
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size

            rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#cccccc", outline="#888", width=2)
            text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                           text="❓", font=("Arial", 32))
            self.rect_items.append(rect)
            self.text_items.append(text)

            self.canvas.tag_bind(rect, "<Button-1>", lambda e, idx=i: self.reveal_card(idx))
            self.canvas.tag_bind(text, "<Button-1>", lambda e, idx=i: self.reveal_card(idx))

    def reveal_card(self, index):
        if self.revealed[index]:
            return

        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True

        symbol = self.symbols[index]
        color = self.symbol_colors[symbol]

        self.animate_zoom(index)

        self.canvas.itemconfig(self.rect_items[index], fill=color)
        self.canvas.itemconfig(self.text_items[index], text=symbol)

        if self.first_card is None:
            self.first_card = index
        else:
            self.attempts += 1
            second_card = index
            if self.symbols[self.first_card] == self.symbols[second_card]:
                play_sound(True)
                self.revealed[self.first_card] = True
                self.revealed[second_card] = True
                self.first_card = None
                self.matches += 1
                self.status_label.config(text="أحسنت يا بطل! 🏆")
                self.root.after(1000, self.update_status)  # بعد ثانية نرجع نحدث الحالة العادية
                if self.matches == len(self.symbols) // 2:
                    elapsed = int(time.time() - self.start_time)
                    self.status_label.config(
                        text=f"🎉 مبروك! أنهيت المستوى {self.size}x{self.size} | المحاولات: {self.attempts} | الوقت: {elapsed} ث")
            else:
                play_sound(False)
                self.root.after(800, self.hide_cards, self.first_card, second_card)
                self.first_card = None

        # تحديث الحالة العادية فقط إذا مش في فترة عرض رسالة أحسنت
        if not self.status_label.cget("text").startswith("أحسنت"):
            self.update_status()

    def update_status(self):
        elapsed = int(time.time() - self.start_time) if self.timer_running else 0
        self.status_label.config(text=f"المحاولات: {self.attempts} | الوقت: {elapsed} ث")

    def hide_cards(self, i1, i2):
        self.canvas.itemconfig(self.rect_items[i1], fill="#cccccc")
        self.canvas.itemconfig(self.text_items[i1], text="❓")
        self.canvas.itemconfig(self.rect_items[i2], fill="#cccccc")
        self.canvas.itemconfig(self.text_items[i2], text="❓")

    def update_timer(self):
        if self.timer_running and self.matches < len(self.symbols) // 2:
            elapsed = int(time.time() - self.start_time)
            # تحديث فقط إذا مش في فترة عرض رسالة أحسنت
            if not self.status_label.cget("text").startswith("أحسنت"):
                self.status_label.config(text=f"المحاولات: {self.attempts} | الوقت: {elapsed} ث")
        self.root.after(1000, self.update_timer)

    def restart_game(self):
        self.symbols = self.symbols[:]
        random.shuffle(self.symbols)
        self.draw_board()
        self.status_label.config(text="المحاولات: 0 | الوقت: 0 ث")

    def animate_zoom(self, index):
        def zoom(step=0):
            if step > 5:
                self.canvas.itemconfig(self.text_items[index], font=("Arial", 32))
                return
            size = 32 + step * 4
            self.canvas.itemconfig(self.text_items[index], font=("Arial", size))
            self.root.after(30, zoom, step + 1)
        zoom()

def start_game(size):
    game_window = tk.Toplevel(root)
    game_window.title(f"🎯 لعبة الذاكرة - مستوى {size}x{size}")
    MemoryCanvasGame(game_window, size)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("🎮 اختيار مستوى اللعبة")
    root.geometry("320x300")

    tk.Label(root, text="اختر مستوى الصعوبة:", font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="سهل (4x4)", font=("Arial", 12), command=lambda: start_game(4)).pack(pady=5)
    tk.Button(root, text="متوسط (6x6)", font=("Arial", 12), command=lambda: start_game(6)).pack(pady=5)
    tk.Button(root, text="صعب (8x8)", font=("Arial", 12), command=lambda: start_game(8)).pack(pady=5)

    root.mainloop()









