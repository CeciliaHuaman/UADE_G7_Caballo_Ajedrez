
import math
import time

def isSafe(x: int, y: int, board: list[list[int]], size: int) -> bool:
    '''
    A utility function to check if (x, y) are valid indexes for an N*N chessboard.
    '''
    return 0 <= x < size and 0 <= y < size and board[x][y] == -1  # Checks bounds and if cell is unvisited

def printSolution(n: int, board: list[list[int]]) -> None:
    '''
    A utility function to print the chessboard matrix solution.
    '''
    for i in range(n):
        for j in range(n):
            print(board[i][j], end=' ')  # Prints each cell value
        print()

# def distanceToWalls(x, y, n):
#     center = (n - 1) / 2
#     return math.sqrt((x - center)**2 + (y - center)**2)

def distanceToWalls(x, y, n):
    center = (n - 1) / 2
    dx = x - center
    dy = y - center
    distance = (dx * dx + dy * dy) ** 0.5
    return distance

def bound(moves):
    if len(moves)>=4:
        moves=moves[:1]
    return moves

def branch(curr_x, curr_y, n, board, move_x, move_y):
    
    priority_queue = []

    for i in range(8):
        new_x = curr_x + move_x[i]
        new_y = curr_y + move_y[i]
        if isSafe(new_x, new_y, board, size=len(board)):
            # Prioriza movimientos más alejados del centro
            distance = distanceToWalls(new_x, new_y, n)
            priority_queue.append((distance, new_x, new_y))
    
    # Ordena los movimientos de mayor a menor distancia al centro
    priority_queue.sort(reverse=True, key=lambda move: move[0])
    
    return bound(priority_queue)

def solveKT(n,x_position, y_position):
    start_time = time.time()

    board = [[-1 for i in range(n)]for i in range(n)]

    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    board[x_position][y_position] = 0


    pos = 1

    if(not solveKTUtil(n, board, x_position, y_position, move_x, move_y, pos)):
        print("Solution does not exist")
    else:
        print(f"--- {time.time() - start_time} seconds ---")
        #printSolution(n, board)
        

def solveKTUtil(n, board, curr_x, curr_y, move_x, move_y, pos, ):

    if(pos == n**2):
        return True
    
    cola_prioridad = branch(curr_x, curr_y, n, board, move_x, move_y)

    for _, new_x, new_y in cola_prioridad:
        board[new_x][new_y] = pos

        if(solveKTUtil(n, board, new_x, new_y, move_x, move_y, pos+1)):
            return True
        board[new_x][new_y] = -1
    return False

if __name__ == "__main__":
    
    # board size
    n=5
    # initial position of the Knight
    for i in range(n):
        for j in range(n):
            # Function Call
            solveKT(n,i,j)

    


