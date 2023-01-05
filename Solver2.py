import numpy as np

PUZZLE = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 3, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0] 
]

class Puzz():
    def __init__(self, puzzle):
        self.rows = puzzle
        self.cols = self.find_col()
        self.sqrs = self.find_sqr()
    
    def __str__(self):
        return str(self.rows)
    
    def find_col(self):
        cols = []
        col = []
        for i in range(9):
            for j in range(9):
                col.append(self.rows[j][i])
            cols.append(col)
            col = []
        return cols

    def find_sqr(self):

        Arr = []
        sqr = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        sqr.append(self.rows[3*i + k][3*j + l])
                Arr.append(sqr)
                sqr = []
        return Arr

class Solution():
    def __init__(self, puzzle):
        self.puzz = puzzle
        self.MatrixA = []
        self.MatrixB = []
        self.constraints = []
        self.fillB()
        self.fillA()
    
    def fillB(self):
        for i in self.puzz.rows:
            self.MatrixB.append(45 - sum(i))
        for j in self.puzz.cols:
            self.MatrixB.append(45 - sum(j))
        for k in self.puzz.sqrs:
            self.MatrixB.append(45 - sum(k))
        for i in self.MatrixB:
            if i == 0:
                self.MatrixB.remove(i)
    
    def A_row(self):
        R = []
        for i in range(len(self.puzz.rows)):
            row = []
            for x in range(len(self.puzz.rows)):
                for y in range(len(self.puzz.rows[0])):
                    if (i == x):
                        if (self.puzz.rows[x][y]) == 0:
                            row.append(1)
                    else:
                        if (self.puzz.rows[x][y]) == 0:
                            row.append(0)
            R.append(row)
        return R
    
    def A_col(self):
        C = []
        for i in range(len(self.puzz.rows[0])):
            col = []
            for x in range(len(self.puzz.rows)):
                for y in range(len(self.puzz.rows[0])):
                    if (i == y):
                        if (self.puzz.rows[x][y]) == 0:
                            col.append(1)
                    else:
                        if (self.puzz.rows[x][y]) == 0:
                            col.append(0)
            C.append(col)
        return C
    
    def A_sqr(self):
        #hard coded for a 9x9 puzzle sorry
        S = []
        for i in range(3):
            for j in range(3):
                sqr = []
                for x in range(len(self.puzz.rows)):
                    for y in range(len(self.puzz.rows[0])):
                        if (i == x//3 and j == y//3):
                            if (self.puzz.rows[x][y]) == 0:
                                sqr.append(1)
                        else:
                            if (self.puzz.rows[x][y]) == 0:
                                sqr.append(0)
                S.append(sqr)
        return S
    
    def fillA(self):
        for r in self.A_row():
            self.MatrixA.append(r)
        for c in self.A_col():
            self.MatrixA.append(c)
        for s in self.A_sqr():
            self.MatrixA.append(s)
        for i in self.MatrixA:
            if sum(i) == 0:
                self.MatrixA.remove(i)

    def setConstraints(self):
        Rc = []
        temp = range(1, 10)

print(list(range(1, 10)))