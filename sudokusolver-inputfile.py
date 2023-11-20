# Project started November 1st by me as Sudoku Solver/Generator. This may take months as its just a fun side project and I don't know how hard it will end up being
# The sudoku generator paired with an easy solver is in my final engineering project! 
# Decided to go all out and not stop until every sudoku is solveable 
# The user input is in the format of a file containing sudokus where 0 represents empty slots or you can modify the array below
import time
import copy
from pystyle import Colors
'''
# Here is a blank board to copy!
board = [['.','.','.','.','.','.','.','.','.'], 
         ['.','.','.','.','.','.','.','.','.'],
         ['.','.','.','.','.','.','.','.','.'],
         ['.','.','.','.','.','.','.','.','.'],
         ['.','.','.','.','.','.','.','.','.'],
         ['.','.','.','.','.','.','.','.','.'],
         ['.','.','.','.','.','.','.','.','.'],
         ['.','.','.','.','.','.','.','.','.'],
         ['.','.','.','.','.','.','.','.','.']]
'''
board = [['.','.','5','8','.','.','.','.','.'], 
         ['.','9','.','5','2','.','.','1','.'],
         ['.','.','.','.','6','4','.','.','7'],
         ['.','.','8','.','.','.','.','3','9'],
         ['.','3','7','.','.','.','6','4','.'],
         ['9','4','.','.','.','.','8','.','.'],
         ['3','.','.','6','8','.','.','.','.'],
         ['.','2','.','.','4','1','.','8','.'],
         ['.','.','.','.','.','2','1','.','.']]

boxDict = {1:['00','01','02','10','11','12','20','21','22'],2:['03','04','05','13','14','15','23','24','25'],3:['06','07','08','16','17','18','26','27','28'],4:['30','31','32','40','41','42','50','51','52'],5:['33','34','35','43','44','45','53','54','55'],6:['36','37','38','46','47','48','56','57','58'],7:['60','61','62','70','71','72','80','81','82'],8:['63','64','65','73','74','75','83','84','85'],9:['66','67','68','76','77','78','86','87','88']}
count = 0
globalcount =0

def printBoard(board): # Prints the board "sudoku style"
    for iindex,i in enumerate(board):
        if(iindex%3==0): print('|----------------------------------------------------------|')  
        for jindex,j in enumerate(i):
            if(jindex%3==0):
                print('|    ',end='')
            if(jindex==8):
                print(j+'   ',end='')
                continue
            print(j+ '    ',end='')
        print('|\n|                   |                   |                  |')
    print('|-----------------------------------------------------------') 
          

def isAlreadyInRow(board,num,rowNum): # Checks if a number is already in a row
    for i in board[rowNum]:
        if(i==str(num)):
            return True
    return False



def isAlreadyInColumn(board,num,columnNum): # Checks if a number is already in a column
    columnList = []
    for iindex,i in enumerate(board):
        for jindex,j in enumerate(i):
            if(jindex==columnNum):
                columnList.append(j)
    if(str(num) in columnList):
        return True
    return False

def getBox(boxDict,posX,posY): # gets the box of a certain x and y pos
    for i in boxDict:
        for j in boxDict[i]:
                if(int(j[0])==posX and int(j[1])==posY):
                    return i
                
def isAlreadyInBox(board,num,box,boxDict): # Checks if a number is already in a box.
    pointList = boxDict[box]
    for i in pointList:
        if(board[int(i[0])][int(i[1])]==str(num)):
            return True
    return False

def checkBoardFull(board): #Checks if the sudoku board is full.
    for i in board:
        for j in i:
            if(j=='.'):
                return False
    return True


def doRowCheck(board,possibleValuesList):
    '''
    This will check if a certain cell contains a possible number that only appears once in the row.
    '''
    for iindex,i in enumerate(possibleValuesList):
        dict = {}
        if(len(i)>1):
            row,col,possibleValues  = i[0][0],i[0][1],i[1][:]
            for value in possibleValues: dict[value] = 0
            for iindex2,i2 in enumerate(possibleValues):
                for jindex,j in enumerate(possibleValuesList):
                    if(len(j)>1):
                        if(i2 in j[1] and j[0][0]==row): 
                            dict[i2] += 1
            for k in dict:
                if(dict[k]==1): 
                    board[row][col] = str(k)
        

def doColumnCheck(board,possibleValuesList):
    '''
    This will check if a certain cell contains a possible number that only appears once in the column.
    '''
    for iindex,i in enumerate(possibleValuesList):
        dict = {}
        if(len(i)>1):
            row,col,possibleValues  = i[0][0],i[0][1],i[1][:]
            for value in possibleValues: dict[value] = 0
            for iindex2,i2 in enumerate(possibleValues):
                for jindex,j in enumerate(possibleValuesList):
                    if(len(j)>1):
                        if(i2 in j[1] and j[0][1]==col): 
                            dict[i2] += 1
            for k in dict:
                if(dict[k]==1): 
                    board[row][col] = str(k)
                    
def doBoxCheck(board,possibleValuesList,boxDict): 
    '''
    This will check if a certain cell contains a possible number that only appears once in the box.
    '''
    for iindex,i in enumerate(possibleValuesList):
        dict = {}
        if(len(i)>1):
            row,col,possibleValues  = i[0][0],i[0][1],i[1][:]
            boxNum = getBox(boxDict,row,col)
            for value in possibleValues: dict[value] = 0
            for iindex2,i2 in enumerate(possibleValues):
                for jindex,j in enumerate(possibleValuesList):
                    if(len(j)>1):
                        if(i2 in j[1] and getBox(boxDict,j[0][0],j[0][1])==boxNum):
                            dict[i2] += 1
            for k in dict:
                if(dict[k]==1): 
                    board[row][col] = str(k)
                    

def playCrossRoad(board,possibleValuesList,index,indexcrossroad,num):
    '''
    This function chooses a path at cross roads. This is the highest tier of sudoku solving and typically expert and master levels require this. 
    The program reaches a point where a box can be 1 of 2 possible values. This chooses 1 path and returns the index and value chosen. Now on the higher level this may need to be called inside a while True loop.
    '''
    count=-1
    for iindex,i in enumerate(possibleValuesList):
        if(len(i)>1):
            if(len(i[1])==num):
                count+=1
                if(count==indexcrossroad):
                    board[i[0][0]][i[0][1]] = str(i[1][index])
                    return i[0][0],i[0][1],i[1][index]

# example = [[[2,3],[1,2,3]], ]
def solveSudoku(board): 
    '''
     This function primarily will create a list of lists of lists containing the coordinate and possible values for every square(like the sudoku "notes" but for the program)
     It will also fill in squares with only 1 possible value. This is the most basic brute force sudoku solver and can solve a lot of sudokus with around 30-45 spaces blank.
     Then it calls functions to check rows columns and boxes. The logic of sudoku is that every square must contain all 9 numbers. The functions at the bottom implement this.
    '''
    count = 0
    possibleValuesList = [[]]
    for iindex,i in enumerate(board):
        for jindex,j in enumerate(i):
            possibleValues = []
            if(j=='.'):
                for k in range(1,10):
                    if(isAlreadyInBox(board,k,getBox(boxDict,iindex,jindex),boxDict) or isAlreadyInColumn(board,k,jindex) or isAlreadyInRow(board,k,iindex)):
                        continue
                    possibleValues.append(k)
                if(len(possibleValues)==1):
                    board[iindex][jindex] = str(possibleValues[0])
                possibleValuesList[count].append([iindex,jindex])
                possibleValuesList[count].append(possibleValues)
                count+=1
                possibleValuesList.append([])
    doRowCheck(board,possibleValuesList)
    doColumnCheck(board,possibleValuesList)
    doBoxCheck(board,possibleValuesList,boxDict)
    if(guimode=='1'):print(possibleValuesList)
    return possibleValuesList

def trySolve(board): # Loops through the solveBoard. Counts and breaks were implemented to reduce the solving time.
    count=0
    for i in range(81):
        previousBoard = [row[:] for row in board]
        possibleValuesList = solveSudoku(board)
        if(checkBoardFull(board)):break
        if(board==previousBoard):count+=1
        else: count=0
        if(count>3):break
    return possibleValuesList

filename = input('Enter a filename: ').strip()
guimode = input('Enter gui mode(1 or 2): ')

with open(filename,'r') as file:
    for line in file:
        lines = line.split()
        a = lines[1]
        difficulty = lines[2]
        if(a!='n'):
            board = [[]]
            countIndex = 0
            for iindex,i in enumerate(a):
                if(iindex%9==0 and iindex!=0):
                    board.append([])
                    countIndex+=1
                if(i=='0'):board[countIndex].append('.')
                else:board[countIndex].append(i)

    

        firstboard = [row[:] for row in board]
        time1 = time.time()
        count = 0
        possibleValuesList = trySolve(board)
        if(checkBoardFull(board)==False):
            
            indexcrossroad = 0
            valuetotry = 2
            beforeboard = [row[:] for row in board]
            counter = 0
            prevcount=0
            while(checkBoardFull(board)==False and counter<81):
                prevValuesList = copy.deepcopy(possibleValuesList)
                counter+=1
                values = playCrossRoad(board,possibleValuesList,0,indexcrossroad,2)
                if(values!=None):posX,posY,numTried=values
                possibleValuesList = trySolve(board)
                if(checkBoardFull(board)==False):
                    board = [row[:] for row in beforeboard]
                    possibleValuesList = trySolve(board)
                    values = playCrossRoad(board,possibleValuesList,1,indexcrossroad,2)
                    if(values!=None):posX,posY,numTried=values
                    possibleValuesList = trySolve(board)
                    if(checkBoardFull(board)==False):
                        board = [row[:] for row in beforeboard]
                        possibleValuesList = trySolve(board)
                        values = playCrossRoad(board,possibleValuesList,0,indexcrossroad,3)
                        if(values!=None):posX,posY,numTried=values
                        possibleValuesList = trySolve(board)
                        if(checkBoardFull(board)==False):
                            board = [row[:] for row in beforeboard]
                            possibleValuesList = trySolve(board)
                            values = playCrossRoad(board,possibleValuesList,1,indexcrossroad,3)
                            if(values!=None):posX,posY,numTried=values
                            possibleValuesList = trySolve(board)

                            if(checkBoardFull(board)==False):
                                board = [row[:] for row in beforeboard]
                                possibleValuesList = trySolve(board)
                                values = playCrossRoad(board,possibleValuesList,2,indexcrossroad,3)
                                if(values!=None):posX,posY,numTried=values
                                possibleValuesList = trySolve(board)
                                if(checkBoardFull(board)==False):
                                            indexcrossroad+=1
                if(prevValuesList==possibleValuesList):prevcount+=1
                else:prevcount=1
                if(prevcount==3):break

        if(checkBoardFull(board)==False):
            board = [row[:] for row in beforeboard]
            
    
            indexcrossroad = 0
            valuetotry = 2
            beforeboard = [row[:] for row in board]
            counter = 0
            prevcount=0
            while(checkBoardFull(board)==False and counter<81):
                prevValuesList = copy.deepcopy(possibleValuesList)
                counter+=1
                values = playCrossRoad(board,possibleValuesList,0,indexcrossroad,2)
                if(values!=None):posX,posY,numTried=values
                possibleValuesList = trySolve(board)
                if(checkBoardFull(board)==False):
                    board = [row[:] for row in beforeboard]
                    possibleValuesList = trySolve(board)
                    values = playCrossRoad(board,possibleValuesList,1,indexcrossroad,2)
                    if(values!=None):posX,posY,numTried=values
                    possibleValuesList = trySolve(board)
                    if(checkBoardFull(board)==False):
                        indexcrossroad+=1
                if(prevValuesList==possibleValuesList):prevcount+=1
                else:prevcount=1
                if(prevcount==3):break
            
            indexcrossroad = 0
            valuetotry = 3
            counter = 0
            prevcount=0
            while(checkBoardFull(board)==False and counter<81):
                prevValuesList = copy.deepcopy(possibleValuesList)
                counter+=1
                values = playCrossRoad(board,possibleValuesList,0,indexcrossroad,3)
                if(values!=None):posX,posY,numTried=values
                possibleValuesList = trySolve(board)
                if(checkBoardFull(board)==False):
                    board = [row[:] for row in beforeboard]
                    possibleValuesList = trySolve(board)
                    values = playCrossRoad(board,possibleValuesList,1,indexcrossroad,3)
                    if(values!=None):posX,posY,numTried=values
                    possibleValuesList = trySolve(board)
                    if(checkBoardFull(board)==False):
                        board = [row[:] for row in beforeboard]
                        possibleValuesList = trySolve(board)
                        values = playCrossRoad(board,possibleValuesList,2,indexcrossroad,3)
                        if(values!=None):posX,posY,numTried=values
                        possibleValuesList = trySolve(board)
                        if(checkBoardFull(board)==False):
                            indexcrossroad+=1
                if(prevValuesList==possibleValuesList):prevcount+=1
                else:prevcount=1
                if(prevcount==3):break
            

        time2 = time.time()
        if(guimode=='1'):
            print(time2-time1)
            printBoard(firstboard)
            print('-----------')
            print('Here is the solution: \n')
            printBoard(board)
        else:
            if(checkBoardFull(board)): print(f'{Colors.green}Solved sudoku {Colors.white}{a}{Colors.green} with a difficulty of {Colors.cyan}{difficulty}{Colors.green} in {time2-time1:.4f} seconds!')
            else:print(f'{Colors.red}Failed sudoku {Colors.white}{a}{Colors.red} with a difficulty of {Colors.cyan}{difficulty}{Colors.red} in {time2-time1:.4f} seconds!')

        if(checkBoardFull(board)):
            with open('solved.txt', 'a') as solved:
                solved.write(f'{a} {difficulty} {time2-time1} {board}\n')
        else:
            with open('unsolved.txt','a') as unsolved:
                unsolved.write(f'{a} {difficulty} {time2-time1}\n')




