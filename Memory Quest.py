import tkinter as tk
import random
from functools import partial
import time

# تخزين أفضل النتائج
high_scores = {
    4: {"time": None, "attempts": None},
    6: {"time": None, "attempts": None},
    8: {"time": None, "attempts": None}
}

class MemoryGame:
    def __init__(self, root, size):
        self.root = root
        self.size = size
        self.root.title(f"🎯 لعبة اختبار الذاكرة {size}x{size}")

        emojis = ["🍎", "🍌", "🍇", "🍒", "🍉", "🍋", "🥝", "🍍",
                  "🐶", "🐱", "🐰", "🐼", "🦁", "🐸", "🐵", "🐤",
                  "❤️", "💙", "💚", "💜", "🧡", "💛", "🤍", "🖤"]

        total_pairs = (size * size) // 2
        symbols = emojis[:total_pairs] * 2
        random.shuffle(symbols)
        self.symbols = symbols

        self.buttons = []
        self.revealed = [False] * len(symbols)
        self.first_choice = None
        self.attempts = 0
        self.matched = 0

        self.start_time = None
        self.timer_running = False

        for i in range(size * size):
            btn = tk.Button(root, text="❓", width=4, height=2, font=("Arial", 18),
                            command=partial(self.reveal_card, i))
            btn.grid(row=i // size, column=i % size, padx=3, pady=3)
            self.buttons.append(btn)

        self.label = tk.Label(root, text="المحاولات: 0 | الوقت: 0 ث", font=("Arial", 14))
        self.label.grid(row=size + 1, column=0, columnspan=size, pady=10)

        self.update_timer()

    def reveal_card(self, index):
        if self.revealed[index]:
            return

        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True

        self.buttons[index].config(text=self.symbols[index])
        self.buttons[index].update()

        if self.first_choice is None:
            self.first_choice = index
        else:
            self.attempts += 1
            if self.symbols[self.first_choice] == self.symbols[index]:
                self.revealed[self.first_choice] = True
                self.revealed[index] = True
                self.matched += 1
                self.first_choice = None

                if self.matched == len(self.symbols) // 2:
                    self.timer_running = False
                    elapsed = int(time.time() - self.start_time)
                    msg = f"🎉 مبروك! أنهيت المستوى {self.size}x{self.size} " \
                          f"في {self.attempts} محاولة و {elapsed} ثانية.\n"

                    best = high_scores[self.size]
                    if best["time"] is None or elapsed < best["time"]:
                        best["time"] = elapsed
                        best["attempts"] = self.attempts
                        msg += "🏆 رقم قياسي جديد! أحسنت 👏"
                    else:
                        msg += f"⏱️ أفضل وقت سابق: {best['time']} ثانية و {best['attempts']} محاولة"

                    self.label.config(text=msg)
            else:
                self.root.after(800, self.hide_cards, self.first_choice, index)
                self.first_choice = None

        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.label.config(text=f"المحاولات: {self.attempts} | الوقت: {elapsed} ث")

    def hide_cards(self, first, second):
        self.buttons[first].config(text="❓")
        self.buttons[second].config(text="❓")

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.label.config(text=f"المحاولات: {self.attempts} | الوقت: {elapsed} ث")
        self.root.after(1000, self.update_timer)


def start_game(size):
    game_window = tk.Toplevel(root)
    MemoryGame(game_window, size)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("🎮 اختيار مستوى اللعبة")
    root.geometry("300x220")

    tk.Label(root, text="اختر مستوى الصعوبة:", font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="سهل (4x4)", font=("Arial", 12),
              command=lambda: start_game(4)).pack(pady=5)
    tk.Button(root, text="متوسط (6x6)", font=("Arial", 12),
              command=lambda: start_game(6)).pack(pady=5)
    tk.Button(root, text="صعب (8x8)", font=("Arial", 12),
              command=lambda: start_game(8)).pack(pady=5)

    root.mainloop()







