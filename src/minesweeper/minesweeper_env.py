import tkinter as tk
import tkinter.ttk as ttk

import numpy as np
import random

ADJACENT_TILES = [[-1, -1], [0, -1], [-1, 0], [1, -1], [-1, 1], [0, 1], [1, 0], [1, 1]]

BUTTON_CLICK = "<ButtonRelease-1>"
BUTTON_FLAG = "<ButtonRelease-3>"


# Minesweeper button extending tk button
class MineButton(tk.Button):
    def __init__(self, parent, x, y, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.num = 0
        self.x = x
        self.y = y

        self.isFlagged = False
        self.isMarked = False
        self.isRevealed = False

    def showNumber(self):
        text = ""
        if self.num == -1:
            text = "*"
        elif 0 < self.num <= 8:
            text = f"{self.num}"
        self.configure(text=text)

    def isMine(self):
        return self.num == -1

    def revealTile(self):
        self.configure(background='#ffffff')
        self.showNumber()
        self.isRevealed = True


class MinesweeperEnv:
    def __init__(self, master=None):
        # game
        self.MINES = 40
        self.LENGTH = 16
        self.HEIGHT = 16

        self.revealed = 0

        self.tiles = [[MineButton for _ in range(self.LENGTH)] for _ in range(self.HEIGHT)]

        self.TILE_COORDINATES = [[x, y] for x in range(self.LENGTH) for y in range(self.HEIGHT)]

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

        # initialize mines as MineButton
        for x in range(0, self.LENGTH):
            for y in range(0, self.HEIGHT):
                b = MineButton(self.gridFrame, x, y)
                b.configure(default='normal', font='{Arial} 9 {bold}', text='', width=5, height=2, compound='center',
                            padx=0, pady=0)
                b.grid(row=x, column=y)

                b.bind(BUTTON_CLICK, self.leftClickWrapper(x, y))
                b.bind(BUTTON_FLAG, self.rightClickWrapper(x, y))

                self.tiles[x][y] = b

    def leftClickWrapper(self, x, y):
        return lambda Button: self.leftClicked(self.tiles[x][y])

    def leftClicked(self, mb: MineButton):
        if not mb.isFlagged:
            if not mb.isRevealed and not mb.isMine():
                mb.revealTile()

                # chord surrounding tiles
                for dx, dy in ADJACENT_TILES:
                    if 0 <= mb.x + dx < self.LENGTH and 0 <= mb.y + dy < self.HEIGHT:
                        if mb.num == 0:
                            self.leftClicked(self.tiles[mb.x + dx][mb.y + dy])

                self.revealed += 1
                if self.won():
                    # win
                    self.gameEnd(True)
            elif mb.isMine():
                if self.revealed == 0:
                    # first click safety
                    pass
                else:
                    mb.revealTile()
                    # lose
                    self.gameEnd(False)

    def rightClickWrapper(self, x, y):
        return lambda Button: self.rightClicked(self.tiles[x][y])

    def rightClicked(self, mb: MineButton):
        print(f"({mb.x}, {mb.y}) right clicked")

    def won(self):
        return self.revealed == self.LENGTH * self.HEIGHT - self.MINES

    def gameEnd(self, won: bool):
        # game end condition
        pass

    def placeMines(self):
        randList = [divmod(i, self.HEIGHT) for i in random.sample(range(self.LENGTH * self.HEIGHT), self.MINES)]

        for x, y in randList:
            mb = self.tiles[x][y]
            mb.num = -1
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
            for dx, dy in ADJACENT_TILES:
                if 0 <= x + dx < self.LENGTH and 0 <= y + dy < self.HEIGHT:
                    if self.tiles[x + dx][y + dy].isMine():
                        count += 1

            if count != 0:
                mb.num = count

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
        for dx, dy in ADJACENT_TILES:
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
