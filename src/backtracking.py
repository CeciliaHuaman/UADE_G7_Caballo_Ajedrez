def isSafe(x, y, board, n):
    '''
        A utility function to check if i,j are valid indexes 
        for N*N chessboard
    '''
    return 0 <= x < n and 0 <= y < n and board[x][y] == -1

def solveKT(n):
    '''
        This function solves the Knight Tour problem using 
        Backtracking. It returns a list of tuples with the 
        knight's path if a solution exists, otherwise it 
        returns an empty list.
    '''
    # Initialization of Board matrix
    board = [[-1 for _ in range(n)] for _ in range(n)]
    
    # move_x and move_y define next move of Knight.
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    # Since the Knight is initially at the first block
    board[0][0] = 0
    path = [(0, 0)]  # Initialize path with starting position

    # Checking if solution exists or not
    if solveKTUtil(n, board, 0, 0, move_x, move_y, 1, path):
        return path  # Return path if solution exists
    else:
        return []  # Return empty list if no solution exists


def solveKTUtil(n, board, curr_x, curr_y, move_x, move_y, pos, path):
    '''
        A recursive utility function to solve Knight Tour 
        problem and store the path in a list of tuples.
    '''
    if pos == n**2:
        return True

    # Try all next moves from the current coordinate x, y
    for i in range(8):
        new_x = curr_x + move_x[i]
        new_y = curr_y + move_y[i]
        if isSafe(new_x, new_y, board, n):
            board[new_x][new_y] = pos
            path.append((new_x, new_y))  # Append position to path

            if solveKTUtil(n, board, new_x, new_y, move_x, move_y, pos + 1, path):
                return True

            # Backtracking
            board[new_x][new_y] = -1
            path.pop()  # Remove position from path
    return False