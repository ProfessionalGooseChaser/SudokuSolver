#CV2 way

import cv2
from pytesseract import pytesseract

def StackOverflow():
    img = cv2.imread("ExamplePuzzle1.png")
    (h, w) = img.shape[:2]
    img = cv2.resize(img, (w*3, h*3))
    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thr = cv2.threshold(gry, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    txt = pytesseract.image_to_string(thr)
    print(txt)

def ChatGPT(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Otsu's thresholding
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply morphological transformations to clean up the image
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # Use pytesseract to extract the text from the image
    text = pytesseract.image_to_string(thresh, lang="eng", config="--psm 10")

    # Split the text into lines and remove empty lines
    lines = [line for line in text.split("\n") if line.strip()]

    # Create a 2-dimensional list of numbers from the lines of text
    sudoku = []
    for line in lines:
        row = []
        for number in line:
            if number.isdigit():
                row.append(int(number))
            else:
                row.append(0)
        sudoku.append(row)

    return sudoku

print(ChatGPT("ExamplePuzzle1.png"))

def oldTRIXsqrs():
    for i in range(3):
            for j in range(3):
                sqr = []
                for k in range(3):
                    for l in range(3):
                        for m in range(3):
                            for n in range(3):
                                if(i, j) == (k, l):
                                    if self.puzz.puzz[3*k + m][3*l + n] == 0:
                                        sqr.append(1)
                                else:
                                    if self.puzz.puzz[3*k + m][3*l + n] == 0:
                                        sqr.append(0)
                sqrs.append(sqr)
                sqr = []

    
def improve_solution(solution):
    # Implement your algorithm to improve the solution here
    return improved_solution

def iterative_improvement(initial_solution):
    solution_set = {}
    current_solution = initial_solution
    while True:
        improved_solution = improve_solution(current_solution)
        if improved_solution in solution_set:
            # This solution has already been seen, so skip it
            continue
        else:
            solution_set[improved_solution] = current_state
            if improved_solution is better than current_solution:
                current_solution = improved_solution
            else:
                # We have reached a local optimum, so we need to backtrack
                while improved_solution is not better than current_solution:
                    current_solution = previous_solution
                    current_state = solution_set[current_solution]
                    improved_solution = improve_solution(current_solution)
                    if improved_solution in solution_set:
                        # This solution has already been seen, so skip it
                        continue
                # We have found a better solution, so we can continue the search
                current_solution = improved_solution
    return current_solution
