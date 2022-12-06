#Sodoku Solver

#sources
#   https://www.geeksforgeeks.org/how-to-extract-text-from-images-with-python/
#   

from PIL import Image
from pytesseract import pytesseract

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
            imgs.append(temp.resize((700, 700))) #scaling up the image so it's easier to read
    return imgs


def create_puzzle(imgs):
    Arr = []
    row = []
    for img in imgs:
        txt = pytesseract.image_to_string(img, lang="eng", config="--psm 10")
        if txt not in nums:
            row.append("")
        else:
            row.append(txt)
        if(len(row) >= 9):
            Arr.append(row)
            row = []
    return Arr

src2 = r"431.webp"

SqrLength, SqrHeight = dimensions(src2)

for i in create_puzzle(find_imgs(src2)):
    print(i)

#           Puzzle
#   5|3|0   0|7|0   0|0|0
#   6|0|0   1|9|5   0|0|0
#   0|9|8   0|0|0   0|6|0

#   8|0|0   0|6|0   0|0|3
#   4|0|0   8|0|3   0|0|1
#   7|0|0   0|2|0   0|0|6

#   0|6|0   0|0|0   2|8|0
#   0|0|0   4|1|9   0|0|5
#   0|0|0   0|8|0   0|7|9

#   Output (8)
#['5\n', '3\n', '', '', '', '', '', '', '']             missing the 7
#['6\n', '', '', '1\n', '9\n', '5\n', '', '', '']       All good
#['', '9\n', '', '', '', '', '', '6\n', '']             missing the 8
#['', '', '', '', '6\n', '', '', '', '3\n']             missing the 8
#['', '', '', '', '', '3\n', '', '', '']                missing 4, 8 and 1 (see if the box is moving too far up)
#['', '', '', '', '2\n', '', '', '', '6\n']             missing the 7
#['', '6\n', '', '', '', '', '2\n', '', '']             missing the 8
#['', '', '', '', '', '9\n', '', '', '']                mssing 4, 1, 5
#['', '', '', '', '', '', '', '', '9\n']                missing the 8 and 7

#output (9)                                             Missing:
#['5\n', '3\n', '', '', '', '', '', '', '']             7
#['6\n', '', '', '1\n', '9\n', '5\n', '', '', '']       None
#['', '9\n', '6\n', '', '', '', '', '6\n', '']          Read the 8 as the 6???
#['6\n', '', '', '', '6\n', '', '', '', '3\n']          Read the 8 as a 6. 
#['', '', '', '', '', '3\n', '', '', '1\n']             4, 8
#['', '', '', '', '2\n', '', '', '', '6\n']             7
#['', '6\n', '', '', '', '', '2\n', '', '']             8
#['', '', '', '', '', '', '', '', '3\n']                Missed 4, 1, 9 and read the 5 as a 9
#['', '', '', '', '', '', '', '', '9\n']                8, 7

