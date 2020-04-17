import tkinter as tk
from tkinter import font as tkFont

class Cell():
    def __init__(self, row, col, id, board):
        self.row = row
        self.col = col
        self.id = id
        self.value = 0
        self.board = board
        self.colours = ["white", "black"]

    def flip(self):
        self.value = (self.value+1)%2
        self.board.itemconfig(self.id, fill=self.colours[self.value])

    def setValue(self, value):
        self.value = value
        self.board.itemconfig(self.id, fill=self.colours[self.value])

    def countNeighbours(self, cells):
        neighbourcount = 0
        for xdiff in range (-1,2):
            for ydiff in range(-1,2):
                neighbourx = self.col + xdiff
                neighboury = self.row + ydiff
                if neighbourx < 0 or neighbourx > len(cells)-1 or neighboury < 0 or neighboury > len(cells)-1 or(xdiff == 0 and ydiff == 0):
                    continue
                neighbourcount += cells[neighboury][neighbourx].value
        return neighbourcount


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.cellSize = 40
        self.geometry("900x980+50+50")
        self.titlefont = tkFont.Font(family="Arial", size=20, slant="italic")
        self.buttonfont = tkFont.Font(family="consolas", size=20)
        l1 = tk.Label(self, text="Conway's Game of Life", font=self.titlefont)
        l1.grid(row=0,column=1)
        self.board = tk.Canvas(self, width=900,height = 900, bg="white")
        self.board.grid(row=1, column=0, columnspan=3)
        self.sizeSlider = tk.Scale(self, from_=20, to=40, tickinterval = 10, resolution=10,  orient= tk.HORIZONTAL)
        self.sizeSlider.set(self.cellSize)
        self.sizeSlider.grid(row=0, column=2)
        self.sizeSlider.bind("<ButtonRelease-1>", self.scaled)
        self.drawgrid()
        self.board.bind("<Button-1>", self.clicked)
        self.board.bind("<B1-Motion>", self.dragged)
        self.dragColour = None
        self.goButton = tk.Button(self, text="Go!", width=10, font = self.buttonfont, command=self.stopgo, bg="green")
        self.goButton.grid(row=0, column=0)
        self.running = False
        self.mainloop()

    def drawgrid(self):
        self.board.delete("all")
        self.cells= [ [None for x in range(900//self.cellSize)] for y in range(900//self.cellSize)]
        self.cellId = {}
        for row in range(0,900//self.cellSize):
            for col in range(0,900//self.cellSize):
                x = col * self.cellSize
                y = row * self.cellSize
                thisCell = Cell(row, col, self.board.create_rectangle(x,y,x+self.cellSize-1, y+ self.cellSize-1), self.board)
                self.cells[row][col] = thisCell
                self.cellId[thisCell.id] = thisCell
                

    def clicked(self, e):
        thisId = self.board.find_closest(e.x, e.y)[0]
        thisCell = self.cellId[thisId]
        self.dragColour = (thisCell.value+1)%2 # the opposite colour
        thisCell.flip()

    def stopgo(self):
        self.running = not self.running
        if self.running:
            self.goButton.config(bg="red", text="Stop!")
            self.simulate()
        else:
            self.goButton.config(bg="green", text="Go!")
        
            

    def dragged(self, e):
        thisId = self.board.find_closest(e.x, e.y)[0]
        thisCell = self.cellId[thisId]
        thisCell.setValue(self.dragColour)


    def scaled(self,e):
        selectedScale = self.sizeSlider.get()
        if selectedScale != self.cellSize:
            self.cellSize = selectedScale
            self.drawgrid()


    def simulate(self):
        # Make a new 2D array to represent the new grid
        newgrid = [ [0 for x in range(900//self.cellSize)] for y in range(900//self.cellSize)]
        # Loop through the 2D array of existing cells (self.cells)...
        for row in range(0,900//self.cellSize):
            for col in range(0,900//self.cellSize):
                newgrid[row][col] = self.cells[row][col].value
        #      count how many neighbours there are
                neighbours = self.cells[row][col].countNeighbours(self.cells)
        #      Set the new grid value appropriately
                if self.cells[row][col].value == 0:
                    if neighbours == 3:
                        newgrid[row][col] = 1
                else:
                    if neighbours < 2 or neighbours > 3:
                        newgrid[row][col] = 0
        # Update all the cells in self.cells with the newgrid values
        for row in range(0,900//self.cellSize):
            for col in range(0,900//self.cellSize):
                self.cells[row][col].setValue(newgrid[row][col])
        if self.running:
            self.after(500, self.simulate)

main = App()
