import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog


# Minesweeper button extending tk button
class MineButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.isMine = False
        self.num = 0

    def clicked(self):
        pass


class MinesweeperEnv:
    def __init__(self, master=None):
        # resources ui
        self.top_level = ttk.Frame(master)
        self.top_level.pack(side='top')
        self.top_level.configure(width=1024, height=576)
        self.scoreboard_frame = ttk.Frame(self.top_level)
        self.scoreboard_frame.grid(row=0, column=0)

        # scoreboard ui
        self.mine_label = ttk.Label(self.scoreboard_frame)
        flag_image = tk.PhotoImage(file="src/resources/flag.gif")
        self.mine_label.configure(font='{Arial} 12 {bold}', text='0', justify='left', image=flag_image)
        self.mine_label.pack(side='left', padx=50)
        self.time_label = ttk.Label(self.scoreboard_frame)
        self.time_label.configure(font='{Arial} 12 {bold}', text='0', justify='right')
        self.time_label.pack(side='right', padx=50)

        # minesweeper grid ui
        self.grid_frame = ttk.Frame(self.top_level)
        self.grid_frame.grid(row=1, column=0)

        for x in range(0, 16):
            for y in range(0, 16):
                b = ttk.Button(self.grid_frame)
                b.configure(default='normal', text=f'{x}{y}', width=5)
                b.grid(row=x, column=y)

        # resources widget
        self.mainwindow = self.top_level

    def setup(self):
        pass

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Minesweeper')
    root.geometry('1024x576')
    app = MinesweeperEnv(root)
    root.mainloop()
