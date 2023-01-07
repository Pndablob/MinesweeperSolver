import tkinter as tk
import tkinter.ttk as ttk

import random
import math


# Minesweeper button extending tk button
class MineButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.isMine = False
        self.isFlagged = False
        self.isClicked = False
        self.num = 0

    def showNumber(self):
        self.configure(text=f'{self.num}')

    def leftClickHandler(self, e):
        pass
        #return [math.floor(e.x / )]


class MinesweeperEnv:
    def __init__(self, master=None):
        # game
        self.MINES = 40
        self.LENGTH = 16
        self.HEIGHT = 16

        self.mineGrid = [[MineButton for i in range(self.LENGTH)] for j in range(self.HEIGHT)]

        # minesweeper grid ui
        self.topLevel = ttk.Frame(master)
        self.topLevel.pack(side='top')

        self.gridFrame = ttk.Frame(self.topLevel)
        self.gridFrame.grid(row=0, column=0)

        # stats ui
        self.statsFrame = ttk.Frame(self.topLevel)
        self.statsFrame.grid(row=0, column=1)

        for x in range(0, self.LENGTH):
            for y in range(0, self.HEIGHT):
                b = MineButton(self.gridFrame, default='normal', text='', width=5, height=2, compound='c', padx=0, pady=0)
                b.grid(row=x, column=y)

                b.bind('<ButtonRelease-1>', b.leftClickHandler)

                self.mineGrid[x][y] = b

    def leftClicked(self, x, y):
        print(f"button at ({x}, {y}) was clicked")

        mb = self.mineGrid[x][x]
        if (not mb.isClicked or not mb.isFlagged) and not mb.isMine:
            mb.configure(background='#ffffff')
            mb.showNumber()
            mb.isClicked = True

    def setup(self):
        self.placeMines()
        self.setNumbers()

    def placeMines(self):
        randList = [divmod(i, self.HEIGHT) for i in random.sample(range(self.LENGTH * self.HEIGHT), self.MINES)]

        for x, y in randList:
            self.mineGrid[x][y].isMine = True
            print(f"set {x} {y} to mine")

    def setNumbers(self):
        for x in range(self.LENGTH):
            for y in range(self.HEIGHT):
                mine = self.mineGrid[x][y]
                count = 0

                if not mine.isMine:
                    for i in range(-1, 1):
                        for j in range(-1, 1):
                            # when in bounds
                            try:
                                if self.mineGrid[x+i][y+j].isMine:
                                    count += 1
                            except:
                                # edges
                                pass
                    if count != 0:
                        mine.configure(text=f'{count}')
                else:
                    mine.configure(text='Mine')

    def run(self):
        self.setup()
        ## print([[MineButton[x][y].num for x in range(self.LENGTH)] for y in range(self.HEIGHT)])


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Minesweeper')
    root.geometry('1200x800')
    app = MinesweeperEnv(root)
    app.run()
    root.mainloop()
