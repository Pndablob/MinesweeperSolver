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
        self.MINES = 5
        self.LENGTH = 4
        self.HEIGHT = 4

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
        """# Convert the board to a NumPy array for easier manipulation
        board = np.array([[mb.num for mb in self.tiles[y]] for y in range(len(self.tiles))])
        rows, cols = board.shape
        # Initialize the 3BV counter to zero
        tbv = 0
        # Loop through all the cells in the board
        for row in range(rows):
            for col in range(cols):
                # If the cell is a mine, skip it
                if self.tiles[row][col].isMine():
                    continue
                # If the cell has no mines in its neighborhood, click it and add 1 to the 3BV counter
                if board[row - 1:row + 2, col - 1:col + 2].sum() == 0:
                    tbv += 1"""

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

        # error in function
        for x, y in self.TILE_COORDINATES:
            mb = self.tiles[x][y]
            if mb.isMine():
                mb.isMarked = True
                print(f"mine marked ({x}, {y})")

            if mb.num == 0:
                if mb.isMarked:
                    continue
                else:
                    mb.isMarked = True
                    print(f"marked ({x}, {y})")
                    tbv += 1
                    print(f"({x}, {y}) flooded, counted for 3bv")
                    self.floodMark(x, y)

        for x, y in self.TILE_COORDINATES:
            mb = self.tiles[x][y]
            if not mb.isMarked and not mb.isMine():
                print(f"({x}, {y}) not mine, not marked counted for 3bv")
                tbv += 1

        """for x, y in self.TILE_COORDINATES:
            c = 0
            if self.tiles[x][y].num == 0:
                continue
            for dx, dy in self.ADJACENT_TILES:
                if 0 <= (x + dx) < self.LENGTH and 0 <= (y + dy) < self.HEIGHT:
                    mb = self.tiles[x+dx][y+dy]
                    if mb.num == 0:
                        c += 1"""

        return tbv

    def floodMark(self, x, y):
        for dx, dy in self.ADJACENT_TILES:
            if 0 <= (x + dx) < self.LENGTH and 0 <= (y + dy) < self.HEIGHT:
                mb = self.tiles[x + dx][y + dy]

                if mb.isMarked:
                    continue
                elif mb.num == 0:
                    print(f"({x}, {y}) --> ({x + dx}, {y + dy})")
                    if mb.num == 0:
                        self.floodMark(x + dx, y + dy)

    def setup(self):
        self.placeMines()
        self.TBVLabel.configure(text=f"3BV: {str(self.calcTBV())}")
        self.setNumbers()

        # self.showMines()

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
