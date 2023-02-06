from random import randint, seed
from Solver2 import Puzz, Solution
import numpy as np
from functools import reduce
from time import time

seed() #generating a random seed from sys time

BASE = ((0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0))

#creating the base puzzle to build off of, every puzzle starts from here. 

def AddNum(puzzle):
    based = list(puzzle.puzz.rows)
    while True:
        r = randint(0, 8)
        c = randint(0, 8)
        if based[r][c] == 0:                
            intersects = reduce(np.intersect1d, (puzzle.constraints[0][r], puzzle.constraints[1][c], puzzle.constraints[2][(3 * (r//3)) + (c//3)]))
            based[r] = list(based[r])
            based[r][c] = intersects[randint(0, len(intersects)-1)]
            based[r] = tuple(based[r])
            return Solution(Puzz(tuple(based)))


def CreatePuzzle():
    global BASE
    toBeGenerated = randint(7, 31)
    puzz = Solution(Puzz(BASE))
    for i in range(toBeGenerated):
        puzz = AddNum(puzz)
    return puzz
start = time()
genedPuzz = CreatePuzzle()
print(np.matrix(genedPuzz.puzz.rows))
print(time() - start)
