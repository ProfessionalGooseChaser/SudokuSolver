#Sodoku Solver

#sources
#   https://www.geeksforgeeks.org/how-to-extract-text-from-images-with-python/
#   

from PIL import Image
from pytesseract import pytesseract
import numpy as np
import time

pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
src1 = r"ExamplePuzzle1.png"


nums = ['1\n', '2\n', '3\n', '4\n', '5\n', '6\n', '7\n', '8\n', '9\n']

def dimensions(src):
    img = Image.open(src)
    SqrLength = img.width/9
    SqrHeight = img.height/9
    return SqrLength, SqrHeight

def find_imgs(src):
    imgs = []
    img = Image.open(src)
    for i in range(9):      #y
        for j in range(9):  #x
            temp = img.crop((j*SqrLength + 8, i*SqrHeight + 8, (j+1)*SqrLength - 8, (i+1)*SqrHeight - 8))
            imgs.append(temp.resize((900, 900))) #scaling up the image so it's easier to read
    return imgs


def create_puzzle(imgs):
    Arr = []
    row = []
    for i, img in enumerate(imgs):
        txt = pytesseract.image_to_string(img, lang="eng", config="--psm 10")
        #psm10 assumes single char
        #if i in problems:
            #img.show()
        row.append(txt)
        if(len(row) >= 9):
            Arr.append(row)
            row = []
    return Arr

def cleanUp(trix):
    for x in range(len(trix)):
        for y in range(len(trix[x])):
            j = trix[x][y]
            j = j[0]
            match j:
                case '/':
                    j = 7
                case 'O':
                    j = 8
                case 'i':
                    j = 1
                case '°':
                    j = 8
                case 'A':
                    j = 4
                case '>':
                    j = 5
                case '_':
                    j = 0
            j = int(j)
            trix[x][y] = j
    return trix

src2 = r"431.webp"

SqrLength, SqrHeight = dimensions(src1)

start = time.time()
trix1 = create_puzzle(find_imgs(src1))

print(np.matrix(cleanUp(trix1)))
print(time.time() - start)
