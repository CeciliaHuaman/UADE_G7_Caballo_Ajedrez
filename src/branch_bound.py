from __future__ import annotations
import pygame
from src.backtracking import AbstractAlgorithm, isSafe, printSolution
from src.utils.tablero import Board, BoardPosition, Piece, SQ_SIZE
import math
import time

def distanciaHaciaBordes(x, y, n):
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
            distance = distanciaHaciaBordes(new_x, new_y, n)
            priority_queue.append((distance, new_x, new_y))
    
    # Ordena los movimientos de mayor a menor distancia al centro
    priority_queue.sort(reverse=True, key=lambda move: move[0])
    
    return bound(priority_queue)

def solveKT(n, bkalg: BNBAlgorithm):
    start_time = time.time()

    board = [[-1 for i in range(n)]for i in range(n)]

    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    x_position, y_position = bkalg._piece.position
    board[x_position][y_position] = 0
    bkalg.path.append((x_position,y_position))

    pos = 1

    if(not solveKTUtil(n, board, x_position, y_position, move_x, move_y, pos, bkalg)):
        print("Solution does not exist")
    else:
        print(f"--- {time.time() - start_time} seconds ---")
        printSolution(n, board)
        for pos, step in enumerate(bkalg.path):
            bkalg.check_events()
            bkalg.move_piece(position=step, pos=pos)


def solveKTUtil(n, board, curr_x, curr_y, move_x, move_y, pos, bkalg: BNBAlgorithm):

    if(pos == n**2):
        return True
    
    cola_prioridad = branch(curr_x, curr_y, n, board, move_x, move_y)

    for _, new_x, new_y in cola_prioridad:
        board[new_x][new_y] = pos
        bkalg.path.append((new_x, new_y))
        if(solveKTUtil(n, board, new_x, new_y, move_x, move_y, pos+1, bkalg)):
            return True
        board[new_x][new_y] = -1
        bkalg.path.pop()
    return False

class BNBAlgorithm(AbstractAlgorithm):

    def __init__(self, piece: Piece, size: int=8) -> None:
        self._piece = piece
        self._size = size
        self._win = pygame.display.set_mode((size * SQ_SIZE, size * SQ_SIZE))
        self._board = Board(size=self._size, parent=self._win, piece=self._piece, with_legend=True)
        self.path = list()

    def _run(self) -> None:
        solveKT(n=self._size, bkalg=self)
        self.loop = False

    def _reset(self) -> None:
        self.path = list()
        super()._reset()