import concurrent.futures
import time
# Python3 program to solve Knight Tour problem using Branch and Bound with Warnsdorff’s heuristic
def generate_inputs(size, row=None):
    total_inputs = []
    if row != None:
        for i in range(size):
            total_inputs.append({ "size": size, "row": row, "column": i })

    else:
        for i in range(size):
            for j in range(size):
                total_inputs.append({ "size": size, "row": i, "column": j })

    return total_inputs

def printSolution(n, board):
    '''
        A utility function to print Chessboard matrix
    '''
    for i in range(n):
        for j in range(n):
            print(board[i][j], end=' ')
        print()


def isSafe_backtracking(n, x, y, board):
    '''
        A utility function to check if (x, y) are valid indexes
        for n*n chessboard
    '''
    if 0 <= x < n and 0 <= y < n and board[x][y] == -1:
        return True
    return False

def solveKTUtil_backtracking(n, board, curr_x, curr_y, move_x, move_y, pos, start_time, timeout, tracking_board, omit_tracking, explored_nodes):
    '''
        A recursive utility function to solve Knight Tour problem using
        Branch and Bound with Warnsdorff's heuristic.
    '''

    end_time = time.time()

    if pos == n**2 or end_time - start_time >= timeout:
        return True

    # Get the next move with the fewest onward moves
    for i in range(8):
        new_x = curr_x + move_x[i]
        new_y = curr_y + move_y[i]
        explored_nodes[0] += 1
        if(isSafe_backtracking(n, new_x, new_y, board)):
            board[new_x][new_y] = pos
            if not omit_tracking:
                tracking_board.append({"x": new_x, "y": new_y, "pos": pos, "board": board})

            if(solveKTUtil_backtracking(n, board, new_x, new_y, move_x, move_y, pos+1, start_time, timeout, tracking_board, omit_tracking, explored_nodes)):
                return True

            # Backtracking
            if not omit_tracking:
                tracking_board.append({"x": new_x, "y": new_y, "pos": pos, "board": board})

            board[new_x][new_y] = -1
    return False

def solveKT_parallel_backtracking(n, x_pos, y_pos, timeout, omit_tracking):
    '''
        Esta función ejecuta solveKT para una posición inicial dada y devuelve
        el tiempo de inicio y fin para verificar la duración de la ejecución.
    '''
    board = [[-1 for i in range(n)] for j in range(n)]
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    # Marcar la posición inicial
    board[x_pos][y_pos] = 0
    pos = 1
    start_time = time.time()

    tracking_board = []

    explored_nodes = [0]

    # Ejecutar el recorrido del caballo
    success = solveKTUtil_backtracking(n, board, x_pos, y_pos, move_x, move_y, pos, start_time, timeout, tracking_board, omit_tracking, explored_nodes)

    end_time = time.time()

    # Retornar el resultado con información adicional
    return {
        "Start X": x_pos,
        "Start Y": y_pos,
        "Solution Found": False if end_time - start_time >= timeout else success,
        "Execution Time": end_time - start_time,
        "Final Board": board,
        "Tracking Board": tracking_board if end_time - start_time >= timeout and not omit_tracking else None,
        "Explored Nodes": explored_nodes[0]
    }

def get_case_knigth_tour_backtracking_by_size_board_and_position(n, pos_x, pos_y, timeout=60):
    result = solveKT_parallel_backtracking(n, pos_x, pos_y, timeout)
    print("Resultado para posición inicial (", result["Start X"], ",", result["Start Y"], "):")
    print("  - Solución encontrada:", result["Solution Found"])
    print("  - Tiempo de ejecución:", result["Execution Time"], "segundos")
    print("  - Nodos explorados:", result["Explored Nodes"])
    print("  - Tablero final:")
    printSolution(n, result["Final Board"])
    return result


def get_cases_knigth_tour_backtracking_by_size_board(n, timeout=60, row=None, omit_tracking=False):
    # Lista de posiciones iniciales para probar en paralelo

    result = []

    list_boards = []
    start_positions = generate_inputs(n, row)  # Puedes modificar o ampliar esta lista

    # Ejecutamos en paralelo usando ProcessPoolExecutor
    with concurrent.futures.ProcessPoolExecutor() as pool:
        # Mapeamos las posiciones iniciales a solveKT_parallel_backtracking sin usar lambda
        tasks = [pool.submit(solveKT_parallel_backtracking, n, pos["row"], pos["column"], timeout, omit_tracking) for pos in start_positions]

        # Obtener los resultados a medida que se completan
        for task in concurrent.futures.as_completed(tasks):
            if task.done():
                result = task.result()
                print("Resultado para posición inicial (", result["Start X"], ",", result["Start Y"], "):")
                print("  - Solución encontrada:", result["Solution Found"])
                print("  - Tiempo de ejecución:", result["Execution Time"], "segundos")
                print("  - Nodos explorados:", result["Explored Nodes"])
                print("  - Tablero final:")
                printSolution(n, result["Final Board"])
                print()
                list_boards.append(result)

    return list_boards