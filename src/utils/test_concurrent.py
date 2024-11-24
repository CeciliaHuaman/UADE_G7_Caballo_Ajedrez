import math
import concurrent.futures
import time

def generate_inputs(size):
    total_inputs = []
    for i in range(size):
        for j in range(size):
            total_inputs.append({ "size": size, "row": i, "column": j })
    return total_inputs

def isSafe(n, x, y, board):
    '''
        A utility function to check if (x, y) are valid indexes
        for n*n chessboard
    '''
    if 0 <= x < n and 0 <= y < n and board[x][y] == -1:
        return True
    return False

def printSolution(n, board):
    '''
        A utility function to print Chessboard matrix
    '''
    for i in range(n):
        for j in range(n):
            print(board[i][j], end=' ')
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

def branch(curr_x, curr_y, n, board, move_x, move_y, explored_nodes):

    priority_queue = []

    for i in range(8):
        new_x = curr_x + move_x[i]
        new_y = curr_y + move_y[i]
        explored_nodes[0] += 1
        if isSafe(len(board),new_x, new_y, board):
            # Prioriza movimientos más alejados del centro
            distance = distanceToWalls(new_x, new_y, n)
            priority_queue.append((distance, new_x, new_y))

    # Ordena los movimientos de mayor a menor distancia al centro
    priority_queue.sort(reverse=True, key=lambda move: move[0])

    return bound(priority_queue)

def solveKTUtil(n, board, curr_x, curr_y, move_x, move_y, pos, start_time, timeout, tracking_board, explored_nodes):
    '''
        A recursive utility function to solve Knight Tour problem using
        Branch and Bound with Warnsdorff's heuristic.
    '''

    end_time = time.time()

    if pos == n**2 or end_time - start_time >= timeout:
        return True

    cola_prioridad = branch(curr_x, curr_y, n, board, move_x, move_y, explored_nodes)
    # print(f"( {next_x} , {next_y} ) - {pos}")
    # print()

    # time.sleep(0.5)

    for _, new_x, new_y in cola_prioridad:
        board[new_x][new_y] = pos
        tracking_board.append({"x": new_x, "y": new_y, "pos": pos, "board": board})
        if(solveKTUtil(n, board, new_x, new_y, move_x, move_y, pos+1, start_time, timeout, tracking_board, explored_nodes)):
            return True
        tracking_board.append({"x": new_x, "y": new_y, "pos": pos, "board": board})
        board[new_x][new_y] = -1
    return False

def solveKT_parallel(n, x_pos, y_pos, timeout):
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
    success = solveKTUtil(n, board, x_pos, y_pos, move_x, move_y, pos, start_time, timeout, tracking_board, explored_nodes)

    end_time = time.time()

    # Retornar el resultado con información adicional
    return {
        "Start X": x_pos,
        "Start Y": y_pos,
        "Solution Found": False if end_time - start_time >= timeout else success,
        "Execution Time": end_time - start_time,
        "Final Board": board,
        "Tracking Board": tracking_board if end_time - start_time >= timeout else None,
        "Explored Nodes": explored_nodes[0]
    }

def get_case_knigth_tour_by_size_board_and_position(n, pos_x, pos_y, timeout=60):
    result = solveKT_parallel(n, pos_x, pos_y, timeout)
    print("Resultado para posición inicial (", result["Start X"], ",", result["Start Y"], "):")
    print("  - Solución encontrada:", result["Solution Found"])
    print("  - Tiempo de ejecución:", result["Execution Time"], "segundos")
    print("  - Nodos explorados:", result["Explored Nodes"])
    print("  - Tablero final:")
    printSolution(n, result["Final Board"])
    return result


def get_cases_knigth_tour_by_size_board(n, timeout=60):
    # Lista de posiciones iniciales para probar en paralelo

    result = []

    list_boards = []
    start_positions = generate_inputs(n)  # Puedes modificar o ampliar esta lista

    # Ejecutamos en paralelo usando ProcessPoolExecutor
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Mapeamos las posiciones iniciales a solveKT_parallel sin usar lambda
        futures = [executor.submit(solveKT_parallel, n, pos["row"], pos["column"], timeout) for pos in start_positions]

        # Obtener los resultados a medida que se completan
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print("Resultado para posición inicial (", result["Start X"], ",", result["Start Y"], "):")
            print("  - Solución encontrada:", result["Solution Found"])
            print("  - Tiempo de ejecución:", result["Execution Time"], "segundos")
            print("  - Nodos explorados:", result["Explored Nodes"])
            print("  - Tablero final:")
            printSolution(n, result["Final Board"])
            print()
            list_boards.append(result)

    return list_boards


if __name__ == "__main__":
    list_boards = get_cases_knigth_tour_by_size_board(8, timeout=120)