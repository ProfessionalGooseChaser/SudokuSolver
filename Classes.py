import numpy as np

#making a separate file for classes. 
#Puzzle Class
class Puzz():
    def __init__(self, puzzle):
        #organizes the puzzle into rows, cols and squares
        self.rows = puzzle
        self.cols = self.find_col()
        self.sqrs = self.find_sqr()
    
    def __str__(self):
        return str(self.rows)
    
    #finds the columns of the puzzle array
    def find_col(self):
        cols = []
        col = []
        for i in range(9):
            for j in range(9):
                col.append(self.rows[j][i])
            cols.append(col)
            col = []
        return cols

    #finds the 3x3 squares in the array
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

#This big class is how I'm organizing all the stuff
class Solution():
    def __init__(self, puzzle):
        #puzzle Object
        self.puzz = puzzle
        #matrix A and B, used for solving
        self.MatrixA = []
        self.MatrixB = []
        #what numbers I need for any given row/col/sqr
        self.constraints = []
        #fills the matrixes on initialization
        self.fillB()
        self.fillA()
        #Find what I need for each clue
        self.setConstraints()
    
    def fillB(self):
        #The sum of 1-9 is 45. So the remain variables must be 45 - sum(i)
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
        #Organizes puzzle rows into the form factor of the Matrix
        for i in range(len(self.puzz.rows)):
            row = []
            for x in range(len(self.puzz.rows)):
                for y in range(len(self.puzz.rows[x])):
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
        #organizes the puzzle columns into the matrix form factor
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
        #organizes the sqrs into the matrix form factor
        for i in range(3):
            for j in range(3):
                sqr = []
                for x in range(len(self.puzz.rows)):
                    for y in range(len(self.puzz.rows[x])):
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
                self.MatrixA.remove(i) #This is doing something it shouldn't. I think
        
    def setConstraints(self):

        #Can I use quicksort(i) - set(range(1, 10)) to get rid of the for loop?

        #Row Constraints
        Rc = []
        #what does each row need?
        for i in self.puzz.rows:
            temp = list(range(1, 10))
            for j in i:
                if j in temp:
                    temp.remove(j)
            Rc.append(temp)
        self.constraints.append(Rc)

        #Column Constraints
        Cc = []
        #What does each row need?
        for i in self.puzz.cols:
            temp = list(range(1, 10))
            for j in i:
                if j in temp:
                    temp.remove(j)
            Cc.append(temp)
        self.constraints.append(Cc)

        #Square Constraints
        Sc = []
        #what does each square need
        for i in self.puzz.sqrs:
            temp = list(range(1, 10))
            for j in i:
                if j in temp:
                    temp.remove(j)
            Sc.append(temp)
        self.constraints.append(Sc)

    def Solvable(self):
        #print(np.matrix(self.MatrixA))
        if len(self.MatrixA[0]) != len(self.MatrixB):
            #Checks to see if the matrixes have matching sizes
            return False
        elif np.linalg.det(np.array(self.MatrixA)) == 0:
            #is the determinant non-zero?
            return False
        else:
            #looks like we're good
            return True

    def Solve(self):
        #just solving the matrix
        #this way I don't have to guess the last 24ish vairables
        A = np.array(self.MatrixA)
        B = np.array(self.MatrixB)
        return np.linalg.solve(A, B)

class branch():
    #created a quick tree-like data structure. 
    def __init__(self, parent, sol):
        self.parent = parent
        self.data = sol
        self.children = []