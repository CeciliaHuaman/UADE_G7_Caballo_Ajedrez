from __future__ import annotations  # Importa anotaciones de futuras versiones de Python
import pygame  # Importa la librería pygame
from src.backtracking import AbstractAlgorithm, isSafe, printSolution  # Importa clases y funciones del módulo backtracking
from src.utils.tablero import Board, BoardPosition, Piece, SQ_SIZE  # Importa clases y constantes del módulo utils.tablero
import math  # Importa la librería math
import time  # Importa la librería time

def distanciaHaciaBordes(x, y, n):  # Define una función para calcular la distancia hacia los bordes
    center = (n - 1) / 2  # Calcula el centro del tablero
    dx = x - center  # Calcula la distancia en el eje x desde el centro
    dy = y - center  # Calcula la distancia en el eje y desde el centro
    distance = (dx * dx + dy * dy) ** 0.5  # Calcula la distancia euclidiana
    return distance  # Retorna la distancia

def bound(moves):  # Define una función para limitar los movimientos
    if len(moves) >= 4:  # Si hay 4 o más movimientos
        moves = moves[:1]  # Limita los movimientos a solo el primero
    return moves  # Retorna los movimientos limitados

def branch(curr_x, curr_y, n, board, move_x, move_y):  # Define la función principal del algoritmo branch and bound
    priority_queue = []  # Inicializa una cola de prioridad

    for i in range(8):  # Itera sobre los 8 posibles movimientos
        new_x = curr_x + move_x[i]  # Calcula la nueva posición x
        new_y = curr_y + move_y[i]  # Calcula la nueva posición y
        if isSafe(new_x, new_y, board, size=len(board)):  # Verifica si la nueva posición es segura
            distance = distanciaHaciaBordes(new_x, new_y, n)  # Calcula la distancia hacia los bordes
            priority_queue.append((distance, new_x, new_y))  # Añade el movimiento a la cola de prioridad
    
    priority_queue.sort(reverse=True, key=lambda move: move[0])  # Ordena los movimientos de mayor a menor distancia al centro
    
    return bound(priority_queue)  # Retorna los movimientos limitados

def solveKT(n, bkalg: BNBAlgorithm):  # Define una función para resolver el problema del Caballo de Tour
    start_time = time.time()  # Registra el tiempo de inicio

    board = [[-1 for i in range(n)] for i in range(n)]  # Inicializa el tablero con -1 en todas las posiciones

    move_x = [2, 1, -1, -2, -2, -1, 1, 2]  # Define los posibles movimientos en el eje x
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]  # Define los posibles movimientos en el eje y

    x_position, y_position = bkalg._piece.position  # Obtiene la posición inicial del caballo
    board[x_position][y_position] = 0  # Marca la posición inicial del caballo en el tablero
    bkalg.path.append((x_position, y_position))  # Añade la posición inicial a la ruta

    pos = 1  # Inicializa la posición en 1

    if not solveKTUtil(n, board, x_position, y_position, move_x, move_y, pos, bkalg):  # Llama a la función solveKTUtil para resolver el problema
        print("Solution does not exist")  # Imprime un mensaje si no existe solución
    else:
        print(f"--- {time.time() - start_time} seconds ---")  # Imprime el tiempo tomado para encontrar la solución
        printSolution(n, board)  # Imprime la solución
        for pos, step in enumerate(bkalg.path):  # Itera sobre los pasos de la ruta
            bkalg.check_events()  # Verifica los eventos
            bkalg.move_piece(position=step, pos=pos)  # Mueve la pieza a la posición correspondiente

def solveKTUtil(n, board, curr_x, curr_y, move_x, move_y, pos, bkalg: BNBAlgorithm):  # Define una función utilitaria para resolver el problema del Caballo de Tour

    if pos == n**2:  # Si la posición es igual al cuadrado del tamaño del tablero
        return True  # Retorna True
    
    cola_prioridad = branch(curr_x, curr_y, n, board, move_x, move_y)  # Obtiene la cola de prioridad de movimientos

    for _, new_x, new_y in cola_prioridad:  # Itera sobre los movimientos en la cola de prioridad
        board[new_x][new_y] = pos  # Marca la nueva posición en el tablero
        bkalg.path.append((new_x, new_y))  # Añade la nueva posición a la ruta
        if solveKTUtil(n, board, new_x, new_y, move_x, move_y, pos + 1, bkalg):  # Llama recursivamente a solveKTUtil
            return True  # Retorna True si se encuentra una solución
        board[new_x][new_y] = -1  # Desmarca la posición en el tablero
        bkalg.path.pop()  # Elimina la última posición de la ruta
    return False  # Retorna False si no se encuentra una solución

class BNBAlgorithm(AbstractAlgorithm):  # Define la clase BNBAlgorithm que hereda de AbstractAlgorithm

    def __init__(self, piece: Piece, size: int = 8) -> None:  # Inicializa la clase con una pieza y un tamaño de tablero
        self._piece = piece  # Asigna la pieza a un atributo de la clase
        self._size = size  # Asigna el tamaño del tablero a un atributo de la clase
        self._win = pygame.display.set_mode((size * SQ_SIZE, size * SQ_SIZE))  # Crea una ventana de pygame
        self._board = Board(size=self._size, parent=self._win, piece=self._piece, with_legend=True)  # Inicializa el tablero
        self.path = list()  # Inicializa la lista de caminos

    def _run(self) -> None:  # Define el método para ejecutar el algoritmo
        solveKT(n=self._size, bkalg=self)  # Llama a la función solveKT para resolver el problema
        self.loop = False  # Establece el bucle en False

    def _reset(self) -> None:  # Define el método para reiniciar el algoritmo
        self.path = list()  # Reinicia la lista de caminos
        super()._reset()  # Llama al método _reset de la clase padre