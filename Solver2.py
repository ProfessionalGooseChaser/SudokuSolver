from functools import reduce
import numpy as np              #for the matrix math
import time
from Classes import Puzz, Solution, branch
#---------------
#Testing Puzzle
PUZZLE =(
    (0, 0, 3, 0, 2, 0, 6, 0, 0),
    (9, 0, 0, 3, 0, 5, 0, 0, 1),
    (0, 0, 1, 8, 0, 6, 4, 0, 0),
    (0, 0, 8, 1, 0, 2, 9, 0, 0),
    (7, 0, 0, 0, 0, 0, 0, 0, 8),
    (0, 0, 6, 7, 0, 8, 2, 0, 0),
    (0, 0, 2, 6, 0, 9, 5, 0, 0),
    (8, 0, 0, 2, 0, 3, 0, 0, 9),
    (0, 0, 5, 0, 1, 0, 3, 0, 0) 
)

PUZZLE2 = (
    (5, 3, 0, 0, 7, 0, 0, 0, 0),
    (6, 0, 0, 1, 9, 5, 0, 0, 0),
    (0, 9, 8, 0, 0, 0, 0, 6, 0),
    (8, 0, 0, 0, 6, 0, 0, 0, 3),
    (4, 0, 0, 8, 0, 3, 0, 0, 1),
    (7, 0, 0, 0, 2, 0, 0, 0, 6),
    (0, 6, 0, 0, 0, 0, 2, 8, 0),
    (0, 0, 0, 4, 1, 9, 0, 0, 5),
    (0, 0, 0, 0, 8, 0, 0, 7, 9)
)


def guess2(given):
    #This is no longer fucked up but I want to sort intersects by length
    puzpuz = given.data.puzz.rows
    possibilities = []
    branches = []
    for x in range(len(puzpuz)):
        for y in range(len(puzpuz[0])):
            if puzpuz[x][y] == 0:
                intersects = reduce(np.intersect1d, (given.data.constraints[0][x], given.data.constraints[1][y], given.data.constraints[2][(3 * (x//3)) + (y//3)]))
                temp = [(x,y)]
                temp.extend(list(intersects))
                possibilities.append(temp)
    possibilities.sort(key = len)
    for p in possibilities:
        x, y = p[0]
        tmpPuz = list(puzpuz)
        for pp in range(len(p) - 1):
            tmpPuz[x] = list(tmpPuz[x])
            tmpPuz[x][y] = p[pp+1]
            temp = branch(given, Solution(Puzz(tmpPuz)))
            branches.append(temp)
            tmpPuz[x] = tuple(tmpPuz[x])
    return branches

solved = False

def iter_improv(initial):
    global solved
    #systematically takes guesses
    while True:
        if solved:
            break
        possibilities = guess2(initial)
        if initial in solset:
            break
        else:
            solset.add(initial)
        if possibilities == []:
            file = open("solution.txt", 'w')
            for line in initial.data.puzz.rows:
                file.write((str(line)))
                file.write("\n")
            print(time.time()-start)
            solved = True
            #quit()
        else:
            for p in possibilities:
                if p.data.Solvable():
                    print(p.data.Solve())
                iter_improv(p)
                if solved:
                    break
        if initial.parent == None:
            break
        return 0
    

solset = set()


#Testing
#--------------
tester = branch(None, Solution(Puzz(PUZZLE2))) #same as the original

print('-------------------------------')

#for i in pp2:
    #print(np.matrix(i.data.puzz.rows))

start = time.time()
SOLUTION = []
iter_improv(tester)

print(time.time() - start)
print('-------------------------------')
