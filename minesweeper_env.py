import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog


# Minesweeper button extending ttk button
class MinesweeperButton(ttk.Button):
    def __init__(self, ):
        self.x = ttk.Button()


class MinesweeperEnv:
    def __init__(self, master=None):
        # main ui
        self.top_level = ttk.Frame(master)
        self.header_label = ttk.Label(self.top_level)
        self.header_label.configure(font='{Arial} 16 {bold}', text='Minesweeper')

        # minesweeper grid ui
        self.grid_frame = ttk.Frame(self.top_level)

        for x in range(0, 10):
            for y in range(0, 10):
                pass

        # main widget
        self.mainwindow = self.top_level

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Minesweeper')
    root.geometry('1024x576')
    app = MinesweeperEnv(root)
    app.run()
