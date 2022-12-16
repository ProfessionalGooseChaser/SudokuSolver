import numpy as np
from functools import reduce
from random import randint

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

NUM = [1, 2, 3, 4, 5, 6, 7, 8, 9]

class Puzzle():
    def __init__(self, arr):
        self.puzz = arr
        self.rows = []
        self.cols = []
        self.sqrs = []
        self.find_row()
        self.find_col()
        self.find_sqr()
        self.givens = self.find_givens()

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

    def find_givens(self):
        temp = 0
        for i in self.puzz:
            for j in i:
                if j != 0:
                    temp +=1
        return temp
    
    def WhichSqr(self, x, y):
        return (x//3)+(y//3)

class Matrix():
    def __init__(self, puzz):
        self.puzz = puzz
        self.trixA = []
        self.trixB = []
        self.fillTrixA()
        self.fillTrixB()
        self.solvable = self.IsSolvable()

    def GivensPerRow(self):
        givens = []
        for i in self.puzz.rows:
            temp = 0
            for j in i:
                if j != 0:
                    temp += 1
            givens.append(temp)
        return givens

    def fillTrixB(self):
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
            if sol == 0:
                continue
            else:
                self.trixB.append(sol)

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
            if sum(rowK) > 0:
                NewRows.append(rowK)
            else:
                continue
        return NewRows
    
    def MatrixACols(self):
        prev = (0,0)
        cols = []
        for i in range(len(self.puzz.cols)):
            col = []
            for j in range(len(self.puzz.puzz)):
                for k in range(len(self.puzz.puzz[j])):
                    if k == i:
                        if self.puzz.puzz[j][k] == 0:
                            col.append(1)
                        else:
                            continue
                    else:
                        if self.puzz.puzz[j][k] == 0:
                            col.append(0)
            if sum(col) > 0:
                cols.append(col)
            else:
                continue
        return cols
                
    def MatrixASqrs(self):
        #do i need 6 or eight loops here?
        #I should only need 6
        #The first two select which of the 9 squares i need, the other four do the normal function
        sqrs = []
        for i in range(3):
            for j in range(3):
                sqr = []
                for k in range(len(self.puzz.puzz)):
                    for l in range(len(self.puzz.puzz[k])):
                        if (k//3 == i and l//3 == j):
                            if self.puzz.puzz[k][l] == 0:
                                sqr.append(1)
                        else:
                            if self.puzz.puzz[k][l] == 0:
                                sqr.append(0)
                if sum(sqr) > 0:
                    sqrs.append(sqr)
                else:
                    continue

        return sqrs

    def fillTrixA(self):
        for i in self.MatrixARows():
            self.trixA.append(i)
        for j in self.MatrixACols():
            self.trixA.append(j)
        for k in self.MatrixASqrs():
            self.trixA.append(k)

    def IsSolvable(self):
        relationships = 0
        vars = len(self.trixA[0])
        for i in self.trixB:
            if i != 0:
                relationships += 1
        return True if vars == relationships else False

    def CheckSingularity(self):
        A = np.array(self.trixA)
        return True if np.linalg.det(A) == 0 else False

    def Solve(self):
        A = np.array(self.trixA)
        B = np.array(self.trixB)
        for i in A:
            print(i)
            print('\n')
        return np.linalg.solve(A, B)

class Guesser():
    def __init__(self, matrix, puzzle):
        self.puzz = puzzle
        self.trix = matrix
        self.RowConstraints = []
        self.ColConstraints = []
        self.SqrConstraints = []
        self.MUST = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.SetRowConstraints()
        self.SetColConstraints()
        self.SetSqrConstraints()
    
    def SetRowConstraints(self):
        for i in self.puzz.rows:
            temp = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for j in i:
                if j in temp:
                    temp.remove(j)
            self.RowConstraints.append(temp)
            del temp

    def SetColConstraints(self):
        for i in self.puzz.cols:
            temp = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for j in i:
                if j in temp:
                    temp.remove(j)
            self.ColConstraints.append(temp)
            del temp
    
    def SetSqrConstraints(self):
        ##This is just the row constraints, need to fix. 
        for i in self.puzz.sqrs:
            temp = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for j in i:
                if j in temp:
                    temp.remove(j)
            self.SqrConstraints.append(temp)
            del temp

        

# i want to pass it something better than coords, maybe an index and coords? And pass it coords more effectively?
def guess(solution, I, J, K):
    puzzle = solution.puzz.puzz
    for i in range(len(puzzle) - I):
        for j in range(len(puzzle[i]) - J):    
            if puzzle[i][j]==0:
                intersect = reduce(np.intersect1d, (solution.RowConstraints[i], solution.ColConstraints[j], solution.SqrConstraints[3*(i//3) + j//3]))
                for k in intersect:
                    if K > len(intersect):
                        K = len(intersect)
                    puzzle[i][j] = intersect[K]
                    NewPuzz = Puzzle(puzzle)
                    NewTrix = Matrix(NewPuzz)
                    return Guesser(NewTrix, NewPuzz)
    return solution

def RandomGuess(solution):
    puzzle = solution.puzz.puzz
    while True:
        x = randint(0, len(puzzle))
        y = randint(0, len(puzzle[x]))
        if puzzle[x][y] == 0:
            intersect = reduce(np.intersect1d, (solution.RowConstraints[x], solution.ColConstraints[y], solution.SqrConstraints[3*(x//3) + y//3]))
            if intersect: #truthy values
                k = randint(0, len(intersect) - 1)
                puzzle[x][y] = intersect[k]
                NewPuzz = Puzzle(puzzle)
                NewTrix = Matrix(NewPuzz)
                return Guesser(NewTrix, NewPuzz)
            else:
                print(intersect)


def iterative_improvement(initial):  #These two functions were described by Chat GPT. I will upload a picture of what I am referencing
    solution_set = {}
    curr = initial
    count = 0
    IFFY = False
    while True:
        count += 1
        print(count)
        improved = RandomGuess(curr)
        if improved in solution_set:
            continue
        else:
            count += 1
            solution_set[improved] = curr
            if improved.trix.solvable:
                if improved.trix.CheckSingularity:
                    IFFY = True
                else:
                    print(improved.puzz.puzz)
                    return improved
            elif len(improved.trix.trixA[0]) != 0 and len(improved.trix.trixA[0]) < len(curr.trix.trixA[0]): #better solution
                curr = improved
            else:
                #backtracking
                #i = 1
                #j = 1
                #k = 1
                while len(improved.trix.trixA[0]) == len(curr.trix.trixA[0]):
                    curr = solution_set[curr]
                    
                    improved = RandomGuess(curr)
                    #if(i < 9):
                        #i += 1
                    #else:
                        #i = 0
                        #j+= 1
                    #if i > 9 and j > 9:
                        #i = 0
                        #j = 0
                        #k += 1
                    if improved in solution_set:
                        continue
            if IFFY:
                #l = 0
                #m = 0
                #n = 0
                while len(improved.trix.trixA[0]) == len(curr.trix.trixA[0]):
                    curr = solution_set[curr]
                    
                    improved = RandomGuess(curr)
                    #if(l < 9):
                        #l += 1
                    #else:
                        #l = 0
                        #m += 1
                    #if l > 9 and m > 9:
                        #l = 0
                        #m = 0
                        #n += 1
                    if improved in solution_set:
                        continue
            IFFY = False
            curr = improved
    



#Testing!!
Trixie = Matrix(puzz=Puzzle(PUZZLE))
    
GuessNot = Guesser(Trixie, Trixie.puzz)

iterative_improvement(GuessNot)



#Okie dokie so here's where we're at
#I have 27 equations that describe the puzzle
#   Those 27 descirbe the relationships between the 3x3 grid, the row and the columns
#   Furthermore: we know that there must be 9 of each number
#   Each number is an integer

