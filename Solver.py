import numpy as np

puzzle = [
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
#003020600
#900305001
#001806400
#008102900
#700000008
#006708200
#002609500
#800203009
#005010300

def find_col(puz):
    Arr = []
    col = []
    for i in range(9):
        for j in range(9):
            col.append(puz[j][i])
        Arr.append(col)
        col = []
    return Arr

def find_row(puz):
    Arr = []
    row = []
    for i in puz:
        row = i
        Arr.append(row)
    return Arr

def find_sqr(puz):
    Arr = []
    sqr = []
    temp = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    sqr.append(puz[3*i + k][3*j + l])
        Arr.append(sqr)
        sqr = []
    for i in Arr:
        sqr = i[0:9]
        temp.append(sqr)
        sqr = i[9:18]
        temp.append(sqr)
        sqr = i[18:len(i)]
        temp.append(sqr)
    return temp

sols = []
def fill_sols(puzz):
    Matrix = []
    for i in find_row(puzz):
        Matrix.append(i)
    for j in find_col(puzz):
        Matrix.append(j)
    for k in find_sqr(puzz):
        Matrix.append(k)
    for l in Matrix:
        sol = 45
        for m in l:
            sol = sol - m
        sols.append(sol)
    

def PuzzToList(puz):
    arr = []
    for i in puz:
        for j in i:
            arr.append(j)
    return arr

def find_Matrix_Rows(puzz):
    rows = []
    r = []
    for i in range(len(puzz)):
        Zfront = 9 * i
        Zback = (8 - i) * 9
        for Zf in range(Zfront):
            r.append(0)
        for j in puzz[i]:
            if j == 0:
                r.append(1)
            else:
                r.append(0)
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
            c.append(1)
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
                        s.append(0)
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

fill_sols(puzzle)

MatrixA = []
New_Matrix(MatrixA, puzzle)
print(len(MatrixA))

#Okie dokie so here's where we're at
#I have 27 equations that describe the puzzle
#   Those 27 descirbe the relationships between the 3x3 grid, the row and the columns
#However
#   We also can deduce the relationship between any n (<9) number of grids
#   any 2 grids add up to 90
#   any 3 grids add up to 145
#   any n number of 3x3 girds adds up to n * 45
#
#           n!
#   C = ----------
#       (n-r)! *r!
#
#   N = 9 grids,
#   R = 2, 3, 4, 5, 6, 7, 8
#   Obviously I have the 1s covered
#   9, the total sudoku puzzle = 405
#   
#   For when R=
#   2 -> 8*9/2
#   3 -> 7*8*9/2*3
#   4 -> 6*7*8*9/2*3*4
#   5 -> 6*7*8*9/2*3*4
#   6 -> 7*8*9/2*3*4
#   7 -> 8*9/2
#   8 -> 9