# SudokuSolver

This python project solves a given sudoku puzzle. The reader takes an image of a puzzle and translates it into a two dimensional array. 
The solver then takes the array, formats it into a the matrix and solves the matrix with linear algebra.

I did find a paper on the matter which was able to solve a 4x4 matrix but was unable to solve it with a 9x9 matrix
However when they simplified, their final matrix was only 27 rows. 

I don't know too much linear algebra but what I think may make the difference is that besides the relationship within a square, row and column,
you can also model any n number of squares where the sum of those squares is n * 45. Is this redundant becuase an square has to sum to 45? Maybe idk. 
However becuase I can do this I create a significantly more relationships between eac hof the 81 varaibles. 

The program is hardcoded to 9x9 puzzles. 
