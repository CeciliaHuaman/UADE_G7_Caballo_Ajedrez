
import time  # Imports time for measuring execution time


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

def solveKT(n: int,x_position, y_position) -> None:
    '''
        This function solves the Knight Tour problem using 
        Backtracking. This function mainly uses solveKTUtil() 
        to solve the problem. It returns false if no complete 
        tour is possible, otherwise return true and prints the 
        tour. 
        Please note that there may be more than one solutions, 
        this function prints one of the feasible solutions.
    '''
    start_time = time.time()  # Records the start time

    board = [[-1 for _ in range(n)] for _ in range(n)]  # Initializes the board with -1 (unvisited)
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]  # Potential knight moves in x-direction
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]  # Potential knight moves in y-direction

    board[x_position][y_position] = 0  # Marks the starting position as visited

    pos = 1  # Initializes the move count

    if not solveKTUtil(n, board, x_position, y_position, move_x, move_y, pos,start_time):
        print("Solution does not exist")  # Prints message if no solution is found
    else:
        # printSolution(n, board)  # Prints the solution
        print(f"--- {time.time() - start_time} seconds ---")  # Displays the execution time



def solveKTUtil(n: int, board: list[list[int]], curr_x: int, curr_y: int, move_x: list[int], move_y: list[int], pos: int,startTime) -> bool:
    '''
        A recursive utility function to solve Knight Tour problem using 
        Branch and Bound with Warnsdorff's heuristic.
    '''

    if time.time() - startTime > 30:
        raise TimeoutError("Tiempo maximo excedido")
    if pos == n**2:  # If all squares are visited, the tour is complete
        return True

    # Tries all possible moves for the knight from the current position
    for i in range(8):
        new_x = curr_x + move_x[i]
        new_y = curr_y + move_y[i]
        
        if isSafe(new_x, new_y, board, n):  # Checks if the move is valid
            board[new_x][new_y] = pos  # Marks the cell as visited

            if solveKTUtil(n, board, new_x, new_y, move_x, move_y, pos + 1, startTime):  # Recursive call for next move
                return True

            # Backtracks if no solution is found
            board[new_x][new_y] = -1  # Unmarks the cell

    return False

if __name__ == "__main__":
    
    # board size
    n=10
    # initial position of the Knight
    for i in range(n):
        for j in range(n):
            # Function Call
            try:
                solveKT(n,i,j)
            except TimeoutError as e:
                print(str(e))

