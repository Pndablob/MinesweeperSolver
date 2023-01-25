import tkinter as tk
import tkinter.ttk as ttk

import random
import json
import time

# file constants
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
        elif 1 <= self.num <= 8:
            # hex rgb colors for numbers
            buttonColors = ["#2904cf", "#077023", "#db1507", "#180b8c", "#801a16", "#11a697", "#000000", "#7f828a"]
            self.configure(fg=buttonColors[self.num-1])

            text = f"{self.num}"
        self.configure(text=text)

        self.isRevealed = True

    def flagTile(self):
        if not self.isRevealed and not self.isFlagged:
            self.isFlagged = True
            self.configure(fg='#ff0000', text="Flag")
        elif self.isFlagged:
            self.isFlagged = False
            self.configure(fg="#000000", text="")

    def isMine(self):
        return self.num == -1


class MinesweeperEnv:
    def __init__(self, epochs, master=None):
        # class constants
        self.MINES = 40
        self.LENGTH = 16
        self.HEIGHT = 16
        self.TILE_COORDINATES = [[x, y] for x in range(self.LENGTH) for y in range(self.HEIGHT)]

        # game variables
        self.tiles = [[MineButton for _ in range(self.LENGTH)] for _ in range(self.HEIGHT)]
        self.gameStarted = False
        self.revealed = 0
        self.tbv = 0
        self.time = 0

        # stat tracking variables
        self.epochs = epochs
        self.epochCounter = 0
        self.leftClicks = 0
        self.rightClicks = 0
        self.gameStats = []

        # main ui
        self.master = master
        self.topLevel = ttk.Frame(self.master)
        self.topLevel.pack(anchor='nw')

        # minesweeper grid ui
        self.gridFrame = ttk.Frame(self.topLevel)
        self.gridFrame.pack(side='left')

        # stats ui
        self.statsFrame = tk.LabelFrame(self.topLevel, font='{Ariel} 14 {bold}', text='Statistics')
        self.statsFrame.pack(side='right', expand=True, fill='both', padx=20)

        self.timeLabel = ttk.Label(self.statsFrame, font="{Comic Sans} 10 {bold}", text='Time:', anchor='w', justify='left')
        self.timeLabel.grid(row=0, column=0, sticky='W')
        self.TBVLabel = ttk.Label(self.statsFrame, font="{Comic Sans} 10 {bold}", text='3BV:', anchor='w', justify='left')
        self.TBVLabel.grid(row=1, column=0, sticky='W')
        self.TBVPerSecLabel = ttk.Label(self.statsFrame, font="{Comic Sans} 10 {bold}", text='3BV/sec:', anchor='w', justify='left')
        self.TBVPerSecLabel.grid(row=2, column=0, sticky='W')
        self.efficiencyLabel = ttk.Label(self.statsFrame, font="{Comic Sans} 10 {bold}", text='Efficiency:', anchor='w', justify='left')
        self.efficiencyLabel.grid(row=3, column=0, sticky='W')

        self.initBoard()

    # initialize tiles as MineButton instances
    def initBoard(self):
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

    def rightClickWrapper(self, x, y):
        return lambda Button: self.rightClicked(self.tiles[x][y])

    def leftClicked(self, mb: MineButton):
        self.leftClicks += 1

        # start timer on first click
        if not self.gameStarted:
            self.gameStarted = True
            self.time = time.time()

        if not mb.isFlagged:
            if not mb.isRevealed and not mb.isMine():
                mb.configure(background='#ffffff')
                mb.showNumber()

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
                # first click safety
                if self.revealed == 0:
                    # TODO: first click safety
                    pass
                else:
                    mb.configure(background='#ff0000')
                    mb.showNumber()
                    # lose
                    self.gameEnd(False)

        # TODO: fix error in chording
        # chording
        elif mb.isRevealed:
            print("attempted chording")
            # count adjacent flags
            c = 0
            for dx, dy in ADJACENT_TILES:
                if 0 <= mb.x + dx < self.LENGTH and 0 <= mb.y + dy < self.HEIGHT:
                    if self.tiles[mb.x + dx][mb.y + dy].isFlagged:
                        c += 1
            if mb.num == c:
                # reveal surrounding tiles
                for dx, dy in ADJACENT_TILES:
                    if 0 <= mb.x + dx < self.LENGTH and 0 <= mb.y + dy < self.HEIGHT:
                        self.leftClicked(self.tiles[mb.x + dx][mb.y + dy])

    def rightClicked(self, mb: MineButton):
        self.rightClicks += 1

        if not self.gameStarted:
            self.gameStarted = True
            self.time = time.time()

        mb.flagTile()

    def placeMines(self):
        randList = [divmod(i, self.HEIGHT) for i in random.sample(range(self.LENGTH * self.HEIGHT), self.MINES)]

        for x, y in randList:
            mb = self.tiles[x][y]
            mb.num = -1
            mb.isMarked = True

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

    def calcTBV(self):
        """
        Calculates the minimum number of clicks to solve the board (3BV)

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

            if mb.isMarked:
                continue
            elif mb.isMine():
                mb.isMarked = True
                continue
            elif mb.num == 0:
                mb.isMarked = True
                tbv += 1
                self.floodMark(x, y)

        for x, y in self.TILE_COORDINATES:
            mb = self.tiles[x][y]
            if not mb.isMarked:
                tbv += 1

        return tbv

    def floodMark(self, x, y):
        for dx, dy in ADJACENT_TILES:
            # prevent out of bounds
            if 0 <= (x + dx) < self.LENGTH and 0 <= (y + dy) < self.HEIGHT:
                mb = self.tiles[x + dx][y + dy]

                if mb.isMarked:
                    continue

                mb.isMarked = True
                if mb.num == 0:
                    self.floodMark(x + dx, y + dy)

    def setup(self):
        self.placeMines()
        self.setNumbers()

        self.tbv = self.calcTBV()

        self.TBVLabel.configure(text=f"3BV: {str(self.tbv)}")

    def resetEnv(self):
        self.initBoard()

        self.gameStarted = False
        self.time = 0
        self.revealed = 0
        self.leftClicks = 0
        self.rightClicks = 0

        self.setup()

    def won(self):
        return self.revealed == self.LENGTH * self.HEIGHT - self.MINES

    def gameEnd(self, won: bool):
        # dump stats into json after training for n epochs
        if self.epochCounter == self.epochs:
            with open("statistics.json", 'r+') as f:
                data = json.load(f)
                for value in self.gameStats:
                    data["statistics"].append(value)
                f.seek(0)

                json.dump(data, f, indent=4)

            self.master.destroy()

        # compile stats for this board
        # 3bv
        # TODO: calculate 3bv of revealed tiles
        # time
        self.time = round((time.time() - self.time), 3)
        # 3bv/s
        # TODO: division by zero error
        tbvPerSec = round(self.tbv / self.time, 4)
        # TODO: efficiency --> clicks used / 3bv (revealed or complete)

        # game stats as dict
        currentGameStats = {"won": won, "time": self.time, "3bv": self.tbv, "3bv/s": tbvPerSec, "clicks": {"left": self.leftClicks, "right": self.rightClicks}}

        self.gameStats.append(currentGameStats)

        self.resetEnv()

        self.epochCounter += 1

    def run(self):
        self.setup()


if __name__ == '__main__':
    print(time.time())
    root = tk.Tk()
    root.title('Minesweeper')
    root.geometry('850x625')
    root.resizable(False, False)
    app = MinesweeperEnv(5, root)
    app.run()
    root.mainloop()
