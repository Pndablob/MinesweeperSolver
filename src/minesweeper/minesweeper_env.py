import tkinter as tk
import tkinter.ttk as ttk

import numpy as np
import random


# Minesweeper button extending tk button
class MineButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.isFlagged = False
        self.isRevealed = False
        self.isMarked = False
        self.num = 0

    def showNumber(self):
        self.configure(text=f'{self.num}')

    def isMine(self):
        return self.num == -1


class MinesweeperEnv:
    def __init__(self, master=None):
        # game
        self.MINES = 40
        self.LENGTH = 16
        self.HEIGHT = 16

        self.tiles = [[MineButton for _ in range(self.LENGTH)] for _ in range(self.HEIGHT)]

        self.TILE_COORDINATES = [[x, y] for x in range(self.LENGTH) for y in range(self.HEIGHT)]

        self.ADJACENT_TILES = [[-1, -1], [0, -1], [-1, 0], [1, -1], [-1, 1], [0, 1], [1, 0], [1, 1]]

        # main ui
        self.topLevel = ttk.Frame(master)
        self.topLevel.pack(anchor='nw')

        # minesweeper grid ui
        self.gridFrame = ttk.Frame(self.topLevel)
        self.gridFrame.pack(side='left')

        # stats ui
        self.statsFrame = tk.LabelFrame(self.topLevel, font='{Ariel} 12 {bold}', text='Statistics')
        self.statsFrame.pack(side='right', expand=True, fill='both', padx=20)

        self.TBVLabel = ttk.Label(self.statsFrame, text='3BV:', anchor='w', justify='left')
        self.TBVLabel.grid(row=0, column=0)
        self.TBVPerSecLabel = ttk.Label(self.statsFrame, text='3BV/sec:', anchor='w', justify='left')
        self.TBVPerSecLabel.grid(row=1, column=0)
        self.efficiencyLabel = ttk.Label(self.statsFrame, text='Efficiency:', anchor='w', justify='left')
        self.efficiencyLabel.grid(row=2, column=0)

        for x in range(0, self.LENGTH):
            for y in range(0, self.HEIGHT):
                b = MineButton(self.gridFrame)
                b.configure(default='normal', font='{Arial} 9 {bold}', text='', width=5, height=2, compound='center', padx=0, pady=0)
                b.grid(row=x, column=y)

                b.bind('<ButtonRelease-1>', self.leftClicked(x, y))

                self.tiles[x][y] = b

    def leftClickHandler(self, event):
        x = round(event.x / 42.9375)
        y = round(event.y / 38.8125)

        print(f"button clicked at {x}, {y}")

        self.leftClicked(x, y)

        # button width: 42.9375 pixels
        # button height: 38.8125 pixels

    def leftClicked(self, x, y):
        # print(f"button at ({x}, {y}) was clicked")

        # mb = self.tiles[x][y]
        # print(mb)
        """if (not mb.isClicked or not mb.isFlagged) and not mb.isMine:
            mb.configure(background='#ffffff')
            mb.showNumber()
            mb.isClicked = True
        """

    def placeMines(self):
        randList = [divmod(i, self.HEIGHT) for i in random.sample(range(self.LENGTH * self.HEIGHT), self.MINES)]

        for x, y in randList:
            mb = self.tiles[x][y]
            mb.num = -1
            mb.configure(text='*')
            mb.isMarked = True
            print(f"set {x} {y} to mine")

    def setNumbers(self):
        for x, y in self.TILE_COORDINATES:
            mb = self.tiles[x][y]
            if mb.isMine():
                # Skip cells that already contain a mine
                continue

            # Count the number of mines in the adjacent cells
            count = 0
            for dx, dy in self.ADJACENT_TILES:
                if dx == 0 and dy == 0:
                    # Skip the current cell
                    continue
                if 0 <= x + dx < self.LENGTH and 0 <= y + dy < self.HEIGHT:
                    if self.tiles[x + dx][y + dy].isMine():
                        count += 1

            if count != 0:
                mb.num = count
                mb.showNumber()

        """
    def showMines(self):
        for x in range(self.LENGTH):
            for y in range(self.HEIGHT):
                if self.tiles[x][y].isMine():
                    self.tiles[x][y].configure(text="*")
                    """

    # calculate 3BV of the current minesweeper board
    def calcTBV(self):
        """
        Count3BV:
            For each empty ("0") cell C:
                If C has already been marked, continue.
                Mark C. Add 1 to your 3BV count.
                Call FloodFillMark(C).
            For each non-marked, non-mine cell:
                Add 1 to your 3BV count.
    
        FloodFillMark(C):
            For every non-marked neighbor N of C (diagonal and orthogonal):
                Mark N.
                If N is an empty cell, call FloodFillMark(N).
        """

        tbv = 0

        for x, y in self.TILE_COORDINATES:
            mb = self.tiles[x][y]
            # if already marked, continue
            if mb.isMarked:
                continue
            # if mine, mark and continue
            elif mb.isMine():
                mb.isMarked = True
                continue
            # if an empty cell, mark, count for 3BV, and floodflill
            elif mb.num == 0:
                mb.isMarked = True
                tbv += 1
                self.floodMark(x, y)

        for x, y in self.TILE_COORDINATES:
            mb = self.tiles[x][y]
            # for each non-marked, non-mine cell add 1 to 3BV
            if not mb.isMarked:
                tbv += 1

        return tbv

    def floodMark(self, x, y):
        # check adjacent tiles
        for dx, dy in self.ADJACENT_TILES:
            # prevent out of bounds
            if 0 <= (x + dx) < self.LENGTH and 0 <= (y + dy) < self.HEIGHT:
                mb = self.tiles[x + dx][y + dy]

                if mb.isMarked:
                    continue

                mb.isMarked = True
                # if adjacent empty tile, recurse
                if mb.num == 0:
                    self.floodMark(x + dx, y + dy)

    def setup(self):
        self.placeMines()
        self.setNumbers()

        self.TBVLabel.configure(text=f"3BV: {str(self.calcTBV())}")

    def run(self):
        self.setup()

        for r in self.tiles:
            print(np.matrix([mb.num for mb in r]))

        print([[mb.num for mb in self.tiles[y]] for y in range(len(self.tiles))])


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Minesweeper')
    root.geometry('850x625')
    root.resizable(False, False)
    app = MinesweeperEnv(root)
    app.run()
    root.mainloop()
