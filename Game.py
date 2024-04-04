import copy
from queue import PriorityQueue
import timeit
import math,time

#Defining the Board
board = [[''for _ in range(12)] for _ in range(12)]
ccc = 1

# File Reading
with open('./input.txt', 'r') as f:
    # Read the agent name
    gagent = f.readline().rstrip()
    ##
    #Definign Rival
    if (gagent=="X"):
        grival="O"
    else:
        grival="X"

    print("agent",gagent)
    print("rival",grival)

    # Read the time-remaining
    line = f.readline().rstrip()
    parts=line.split()
    time1=float(parts[0])
    time2=float(parts[1])
    print("time1",time1)
    print("time2",time2)

    #Initial State of Board
    for i in range(12):
        line = f.readline().rstrip()
        for j in range(12):
            board[i][j] = line[j]
        
def Print_Grid(board):
    print("    0   1   2   3   4   5   6   7   8   9  10   11")
    # for row in board:
    for i in range(len(board)):
        row=board[i]
        if(i<10):
            print(" ", end="")
        print(i, end='  ')
        print('   '.join(row))

def Moves(agent, board):
    agentspos = set()  # Convert agentspos to a set
    legalpos = set()
    for i in range(12):
        for j in range(12):
            if board[i][j] == agent:
                agentspos.add((i, j))  # Add position to the set
   
    # Defining Rival
    if agent == "X":
        rival = "O"
    else:
        rival = "X"

    for pos in agentspos:
        # print("Finding valid moves for position:",pos)
        row, column = pos

        counter = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        # For every instance of our agent, we need to compute in 8 directions
        for i in range(8):
            rchange = 0
            cchange = 0

            # 0 = Top Left
            if i == 0:
                rchange = 0
                cchange = 1

            # 1 = Top Centre
            if i == 1:
                rchange = 1
                cchange = 0

            # 2 = Top Right
            if i == 2:
                rchange = 0
                cchange = -1

            # 3 = Middle Left
            if i == 3:
                rchange = -1
                cchange = 0

            # 4 = Middle Right
            if i == 4:
                rchange = 1
                cchange = 1

            # 5 = Bottom Left
            if i == 5:
                rchange = 1
                cchange = -1

            # 6 = Bottom Centre
            if i == 6:
                rchange = -1
                cchange = 1

            # 7 = Bottom Right
            if i == 7:
                rchange = -1
                cchange = -1

            r = row + rchange
            c = column + cchange

            # If after calculation, current cell(neighbor of given instance of agent) is not in the board
            if r < 0 or c < 0 or r > 11 or c > 11:
                continue

            # If after calculation, current cell(neighbor of given instance of agent) is same as agent
            if board[r][c] == agent:
                continue

            # If after calculation, current cell(neighbor of given instance of agent) is dot
            if board[r][c] == ".":
                continue

            # If after calculation, current cell(neighbor of given instance of agent) is same as rival
            if board[r][c] == rival:
                # status True depicts that I want to terminate direction

                while r >= 0 and c >= 0 and r <= 11 and c <= 11:
                    r = r + rchange
                    c = c + cchange
                    if not (r >= 0 and c >= 0 and r <= 11 and c <= 11):
                        break

                    # Valid Position Found
                    if board[r][c] == '.':
                        newpos = (r, c)
                        legalpos.add(newpos)
                        # print(newpos, end=" ")
                        break

                    # Recursive Search in same direction
                    if board[r][c] == rival:
                        continue

                    else:
                        # Cell contains agent variety
                        break
    return legalpos


def flipping(move, oldboard, agent):
    board=copy.deepcopy(oldboard)
    rchosen, cchosen = move
    
    board[rchosen][cchosen] = agent
    
    #Defining Rival
    if (agent=="X"):
        rival="O"
    else:
        rival="X"

    counter=0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1,1),(-1,-1)]

    #For newly placed agent, backtracking to flip
    for i in range(8):

        r=rchosen
        c=cchosen
        #intially row-change and column-change are both 0
        rchange = directions[i][0]
        cchange = directions[i][1]
      
        #Based on direction, r an c value changes to get new cell
        r=r+rchange
        c=c+cchange

        #If after calculation, current cell(neighbor of given instance of agent) is not in the board
        if(r<0 or c<0 or r>11 or c>11):
            continue
    
        # If after calculation, current cell(neighbor of given instance of agent) is same as agent
        if(board[r][c] == agent):
            continue

        # If after calculation, current cell(neighbor of given instance of agent) is dot
        if(board[r][c] == "."):
            continue
    
        # If after calculation, current cell(neighbor of given instance of agent) is same as rival
        if(board[r][c] == rival):
            #status True depicts that I want to terminate direction
        
            r=r+rchange
            c=c+cchange

            while(r>=0 and c>=0 and r<=11 and c<=11):
                
                #Valid Position Found
                if(board[r][c] == agent):
                    while(not (r==rchosen and c==cchosen)):
                    
                        r=r-rchange
                        c=c-cchange
                        
                        board[r][c]= agent

                    # status= True
                    break

                #Recursive Search in same direction
                if(board[r][c] == rival):
                    r=r+rchange
                    c=c+cchange
                    continue

                #Cell contains dots
                else:
                    # status=True
                    break
    return board

def utility(board,agent):
    rival = 'O' if agent == 'X' else 'X'
   
    # Weight Index
    mobility_weight = 2  # Weight for mobility
    corner_weight = 10  # Weight for corner occupancy
    edge_weight= 5

    #Number of pieces of each player:
    piece_count, corner_count, edge_count = 0, 0, 0
    for i in range(12):
        for j in range(12):
            piece = board[i][j]
            if(piece == agent):
                piece_count += 1
            elif(piece == rival):
                piece_count -= 1
            if(i==j==0 or i==j==11):
                if(piece == agent):
                    corner_count += 1
                elif piece == rival:
                    corner_count -= 1
            if(i==0 or i==11 or j==0 or j==11):
                if(piece == agent):
                    edge_count += 1
                elif piece == rival:
                    edge_count -= 1
    
    #Number of possible moves
    possibility_agent= Moves(agent,board)
    possibility_rival= Moves(rival,board)

    #Cummulative Computation
    piece_score= piece_count
    mobility_score=mobility_weight*(len(possibility_agent)-len(possibility_rival))
    corner_score=corner_weight*corner_count
    edge_score=edge_weight*edge_count
    utilscore=piece_score+mobility_score+corner_score+edge_score

    return utilscore

def evaluate(board):
    #Number of pieces of each player:
    counto=0
    countx=1
    
    for i in range(12):
        for j in range(12):
            if(board[i][j] ==   'O'):
                counto+=1
            elif(board[i][j] == 'X'):
                countx+=1

    if(counto>countx):
        return float(math.inf)
    
    elif(countx>counto):
        return float(-math.inf)
    else:
        if(gagent == 'O' and time1>time2 ):
            return float(math.inf)
        if(gagent == 'O' and time1<time2 ):
            return float(-math.inf)
        if(gagent == 'X' and time1>time2 ):
            return float(-math.inf)
        if(gagent == 'X' and time1<time2 ):
            return float(math.inf)
        if(counto==countx and time1==time2):
            return float(-math.inf)


def cornercal(player,board):
    corners=[(0,0),(0,11),(11,0),(11,11)]
    count=0
    for corner in corners:
        if(board[corner[0]][corner[1]]==player):
            count+=1
    return count

def edgecal(player,board):
    count=0
    for i in range(12):
        for j in range(12):
            if((i==0 or j==0 or i==11 or j==11)and board[i][j]==player):
                count+=1
    return count

def terminal_test(board):
    xarray = Moves('X',board)
    oarray = Moves('O',board)

    if(len(xarray)==0 and len(oarray)==0):
        return True
    else:
        return False

def max_val(board,alpha,beta,agent, moves,depth):
    if agent=='X':
        rival='O'
    else:
        rival='X'

    bestmove=None
    
    if(depth==0 or not moves):
        return utility(board, agent), None
    
    v= float(-math.inf)
    for currmove in moves:
        new_board_max=flipping(currmove,board,agent)
        tempv,move = min_val(new_board_max,alpha,beta,rival, Moves(rival, new_board_max),depth-1)
       
        if(tempv>v):
            v=tempv
            bestmove=currmove
        alpha = max(alpha,v)
        if(beta<=alpha):
            break

    return v,bestmove

def min_val(board,alpha,beta,agent,moves,depth):
    if agent=='X':
        rival='O'
    else:
        rival='X'
    bestmove=None
    
    if(depth==0 or not moves):
        return utility(board, agent), None
    
    v= float(math.inf)
    for currmove in moves:
        new_board_min=flipping(currmove,board,agent)
        tempv,move = max_val(new_board_min,alpha,beta,rival,Moves(rival,new_board_min),depth-1)
        if(tempv<v):
            v=tempv
            bestmove=currmove
        beta = min(beta,v)
        if(beta<=alpha):
            break
    return v,bestmove

def alpha_beta(board,agent,moves,depth):
    alpha = float(-math.inf)
    beta= float(math.inf)
    
    if agent == 'X': #I am X
        rival= 'O'
    else:   #I am O
        rival = 'X'

    v, action= max_val(board,alpha,beta,agent,moves,depth)

    return action, v

depth= 4
moves = Moves(gagent,board)

if(time1<120):
    depth-=1

if(time1<60):
    depth-=1

if(time1<20):
    depth-=1

if(len(moves)<10):
    depth+=1
    
if(time1>time2):
    depth+=1
value = 0
if(time1<0.5):
    move= list(moves)[0]

else:
    move, value=alpha_beta(board,gagent,moves,depth)

output=[None,None]
output[0]=chr(move[1]+ord('a'))
output[1]=move[0]+1
result = ''.join(map(str, output))
with open('output.txt', 'w') as file:
        file.write(''.join(map(str, output)))       
      
start = timeit.default_timer()

