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

class Puzzle():
    def __init__(self, arr):
        self.puzz = arr
        self.givens = 0
        self.solvable = False
        self.rows = []
        self.cols = []
        self.sqrs = []
        self.find_row()
        self.find_col()
        self.find_sqr()
        self.IsSolvable()

    def IsSolvable(self):
        self.find_givens()
        if 81 - self.givens > 27:
            self.solvable = False
        else:
            self.solvable = True

    def find_givens(self):
        temp = 0
        for i in self.puzz:
            for j in i:
                if j != 0:
                    temp +=1
        self.givens = temp
    
    def find_col(self):
        cols = []
        col = []
        for i in range(9):
            for j in range(9):
                col.append(self.puzz[j][i])
            cols.append(col)
            col = []
        self.cols = cols
    
    def find_row(self):
        Arr = []
        row = []
        for i in self.puzz:
            row = i
            Arr.append(row)
        self.rows = Arr

    def find_sqr(self):
        Arr = []
        sqr = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        sqr.append(self.puzz[3*i + k][3*j + l])
                Arr.append(sqr)
                sqr = []
        self.sqrs = Arr
        

class Matrix():
    def __init__(self, puzz):
        self.puzz = puzz
        self.trixA = []
        self.trixC = []

    def GivensPerRow(self):
        givens = []
        for i in self.puzz.rows:
            temp = 0
            for j in i:
                if j != 0:
                    temp += 1
            givens.append(temp)
        return givens

    def fillTrixC(self):
        Matrix = []

        for i in self.puzz.rows:
            Matrix.append(i)
        for j in self.puzz.cols:
            Matrix.append(j)
        for k in self.puzz.sqrs:
            Matrix.append(k)
        for l in Matrix:
            sol = 45
            for m in l:
                sol = sol - m
            self.trixC.append(sol)

    #def fillTrixA(self):
    def MatrixARows(self):
        NewRows = []
        givens = self.GivensPerRow()

        for k in range(len(self.puzz.rows)):
            rowK = []
            if k > 0:
                for z in range(9 - givens[k-1]):
                    rowK.append(0)
            for j in range(len(self.puzz.rows[k])):
                if self.puzz.puzz[k][j] == 0:
                    rowK.append(1)
            if k < 9:
                for z in range(81 - self.puzz.givens - len(rowK)):
                    rowK.append(0)
            NewRows.append(rowK)
        return NewRows
    
    def GivensBetIndex(self, tpl1, tpl2):
        givens = 0
        for i in range(tpl2[0] - tpl1[0]):
            for j in range(tpl2[1] - tpl1[1]):
                if self.puzz[tpl1[0] + i][tpl1[1] + j] != 0:
                    givens += 1
                if (i,j) == tpl2:
                    return givens
    
    def MatrixACols(self):
        prev = (0,0)
        cols = []
        for i in range(len(self.puzz.rows)):
            rowJ = []
            for j in range(len(self.puzz.rows[i])):
                Zgiven = 0
                if i > 0 or j > 0:
                    Zgiven = self.GivensBetIndex(prev, (j, i))
                    prev = (j, i)
                for z in range(Zgiven):
                    rowJ.append(0)
                if self.puzz.arr[j][i] != 0:
                    rowJ.append(1)
                if i >= len(self.puzz.rows) and j >= len(self.puzz.rows[i]):
                    Zgiven = self.GivensBetIndex(prev, (len(self.puzz.rows), len(self.puzz.rows[i])))
                    for z1 in range(Zgiven):
                        rowJ.append(0)
            cols.append(rowJ)

        return cols
                


            

    

Trixie = Matrix(puzz=Puzzle(PUZZLE))
    
print(Trixie.puzz.givens)
for i in Trixie.MatrixARows():
    print(len(i))


    



def find_Matrix_Rows(puzz):
    rows = []
    r = []
    for i in range(len(puzz)):
        Zfront = 9 * i
        Zback = (8 - i) * 9
        for Zf in range(Zfront):
            r.append(0)
        for j in puzz[i]:
            if puzz[i][j] == 0:
                r.append(1)
            else:
                continue
        for Zb in range(Zback):
            r.append(0)
        rows.append(r)
        r = []
    return rows

def find_Matrix_Cols(puzz):
    cols = []
    c = []
    for i in range(len(puzz)):
        Zfront = i
        Zback = 8 - i
        for j in range(len(puzz[i])):
            for Zf in range(Zfront):
                c.append(0)
            if puzz[i][j] == 0:
                c.append(1)
            else:
                continue
            for Zb in range(Zback):
                c.append(0)
        cols.append(c)
        c = []
    return cols

def find_Matrix_Sqrs(puzz):
    sqrs = []
    s = []
    for i in range(3):
        Zfront = 3 * i
        Zback = 6 - Zfront
        for j in range(3):
            Zabove = 3 * j
            Zdown = 6 - Zabove
            for Za in range(9 * Zabove):
                s.append(0)
            for k in range(3):
                for Zf in range(Zfront):
                    s.append(0)
                for l in range(3):
                    if puzz[3*i + k][3*j + l] == 0:
                        s.append(1)
                    else:
                        continue #Don't append values when we have that value
                for Zb in range(Zback):
                    s.append(0)
            for Zd in range(9 * Zdown):
                s.append(0)
            sqrs.append(s)
            s = []
    return sqrs

def New_Matrix(trix, puzz):
    for i in find_Matrix_Rows(puzz):
        trix.append(i)
        print(len(i))
    for j in find_Matrix_Cols(puzz):
        trix.append(j)
        print(len(j))
    for k in find_Matrix_Sqrs(puzz):
        trix.append(k)
        print(len(k))




#Okie dokie so here's where we're at
#I have 27 equations that describe the puzzle
#   Those 27 descirbe the relationships between the 3x3 grid, the row and the columns
#   Furthermore: we know that there must be 9 of each number
#   Each number is an integer

