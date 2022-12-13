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
    
    def WhichSqr(self, x, y):
        return (x//3)+(y//3)

class Matrix():
    def __init__(self, puzz):
        self.puzz = puzz
        self.trixA = []
        self.trixB = []
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
            NewRows.append(rowK)
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
            cols.append(col)
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
                sqrs.append(sqr)

        return sqrs

    def IsSolvable(self):
        relationships = 0
        vars = len(self.trixA[0])
        for i in self.TrixB:
            if i != 0:
                relationships += 1
        return True if vars == relationships else False

    def Solve(self):
        A = np.array(self.trixA)
        B = np.array(self.trixB)
        return np.linalg.solve(A, B)

class Guesser():
    def __init__(self, matrix, puzzle):
        self.puzz = puzzle
        self.trix = matrix
        self.RowConstraints = {}
        self.ColConstraints = {}
        self.SqrConstraints = {}
        self.MUST = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.SetRowConstraints()
        self.SetColConstraints()
        self.SetSqrConstraints()
    
    def SetRowConstraints(self):
        count = 0
        for i in self.puzz.rows:
            temp = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for j in i:
                if j in temp:
                    temp.remove(j)
            self.RowConstraints.update({count: temp})
            count +=1
            del temp

    def SetColConstraints(self):
        count = 0
        for i in self.puzz.cols:
            temp = self.MUST
            for j in i:
                if j in temp:
                    temp.remove(j)
            self.ColConstraints.update({count: temp})
            count +=1
            del temp
    
    def SetSqrConstraints(self):
        count = 0
        for i in self.puzz.rows:
            temp = self.MUST
            for j in i:
                if j in temp:
                    temp.remove(j)
            self.RowConstraints.update({count: temp})
            count +=1
            del temp

        

# i want to pass it something better than coords, maybe an index and coords? And pass it coords more effectively?
def guess(solution, I, J):
        puzzle = solution.puzz.arr
        for i in range(len(puzzle)):
            if(i ==0):
                i += I
            for j in range(len(puzzle[i])):
                if (j ==0):
                    j += J
                if puzzle[i][j]==0:
                    intersect = list(np.intersect1d((solution.RowConstraints[i], solution.ColConstraints[j], solution.SqrConstratins[3*(i//3) + j//3])))
                    for k in intersect:
                        puzzle[i][j] = k
                        NewPuzz = Puzzle(puzzle)
                        NewTrix = Matrix(NewPuzz)
                        return Guesser(NewTrix, NewPuzz)
        return 0

def iterative_improvement(initial):  #These two functions were described by Chat GPT. I will upload a picture of what I am referencing
    solution_set = {}
    curr = initial
    while True:
        improved = guess(curr, 0, 0)
        if improved in solution_set:
            continue
        else:
            solution_set[improved] = curr
            if improved.trix.solvable:
                IFFY = False
                for i in improved.trix.Solve():
                    if i not in NUM:
                       IFFY = True
                    else: 
                        return improved
            elif improved != 0 and len(improved.trix.trixA[0]) < len(curr.trix.trixA[0]): #better solution
                curr = improved
            else:
                #backtracking
                while len(improved.trix.trixA[0]) == len(curr.trix.trixA[0]):
                    curr = solution_set[curr]
                    i, j = 0
                    improved = guess(curr, i, j)
                    i, j += 1
                    if improved in solution_set:
                        continue
            if IFFY:
                while len(improved.trix.trixA[0]) == len(curr.trix.trixA[0]):
                    curr = solution_set[curr]
                    i, j = 0
                    improved = guess(curr, i, j)
                    i, j += 1
                    if improved in solution_set:
                        continue
            curr = improved
    



#Testing!!
Trixie = Matrix(puzz=Puzzle(PUZZLE))
    
GuessNot = Guesser(Trixie, Trixie.puzz)

GuessNot.SetRowConstraints()
print(GuessNot.RowConstraints)



#Okie dokie so here's where we're at
#I have 27 equations that describe the puzzle
#   Those 27 descirbe the relationships between the 3x3 grid, the row and the columns
#   Furthermore: we know that there must be 9 of each number
#   Each number is an integer

