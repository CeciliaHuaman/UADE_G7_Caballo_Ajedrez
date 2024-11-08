from __future__ import annotations
import pygame
import abc
from src.utils.tablero import Board, BoardPosition, Piece, SQ_SIZE

def isSafe(x, y, board, size):
    '''
        A utility function to check if (x, y) are valid indexes 
        for n*n chessboard
    '''
    if 0 <= x < size and 0 <= y < size and board[x][y] == -1:
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

def countNextMoves(x, y, board, move_x, move_y, size):
    '''
        Count the number of possible moves from position (x, y).
    '''
    count = 0
    for i in range(8):
        new_x, new_y = x + move_x[i], y + move_y[i]
        if isSafe(new_x, new_y, board, size):
            count += 1
    return count

def getNextMove(x, y, board, move_x, move_y, bkalg: BacktrackingAlgorithm):
    '''
        Get the next move with the fewest onward moves, following Warnsdorff's rule.
    '''
    min_degree = 8          # El valor máximo de movimientos es 8
    next_move = (-1, -1)    # Inicializamos next_move como un movimiento no válido
    
    for i in range(8):       # Iteramos sobre los 8 posibles movimientos del caballo
        new_x, new_y = x + move_x[i], y + move_y[i]  # Calculamos las coordenadas del movimiento candidato
        
        if isSafe(new_x, new_y, board, len(bkalg._board.matrix)):  # Verificamos si el movimiento es seguro (dentro del tablero y no visitado)
            degree = countNextMoves(new_x, new_y, board, move_x, move_y, len(bkalg._board.matrix))  # Contamos las opciones futuras desde (new_x, new_y)
            
            if degree < min_degree:   # Si el número de opciones es menor que el mínimo actual
                min_degree = degree   # Actualizamos min_degree
                next_move = (new_x, new_y)  # Guardamos el mejor movimiento como próximo movimiento
    
    return next_move   # Retornamos el movimiento óptimo

def solveKT(n, bkalg: BacktrackingAlgorithm):
    '''
        This function solves the Knight Tour problem using Branch and Bound with 
        Warnsdorff’s heuristic. It returns false if no complete tour is possible,
        otherwise returns true and prints the tour.
    '''

    # Initialization of Board matrix
    board = [[-1 for i in range(n)] for j in range(n)]

    # All possible moves for Knight
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    # Start Knight's Tour from the first block
    x_position, y_position = bkalg._piece.position
    board[x_position][y_position] = 0
    bkalg.move_piece((y_position, x_position), pos=board[x_position][y_position])
    pos = 1

    # Start the tour using Branch and Bound
    if not solveKTUtil(n, board, x_position, y_position, move_x, move_y, pos, bkalg):
        print("Solution does not exist")
    else:
        printSolution(n, board)

def solveKTUtil(n, board, curr_x, curr_y, move_x, move_y, pos, bkalg: BacktrackingAlgorithm):
    '''
        A recursive utility function to solve Knight Tour problem using 
        Branch and Bound with Warnsdorff's heuristic.
    '''
    bkalg.check_events()
    
    if pos == n**2:
        return True

    # Get the next move with the fewest onward moves
    for _ in range(8):
        next_x, next_y = getNextMove(curr_x, curr_y, board, move_x, move_y, bkalg)
        if next_x != -1 and next_y != -1:
            board[next_x][next_y] = pos
            bkalg.move_piece((next_y, next_x), pos=board[next_x][next_y])
            if solveKTUtil(n, board, next_x, next_y, move_x, move_y, pos + 1, bkalg):
                return True
            # Backtracking
            board[next_x][next_y] = -1
            bkalg.move_piece((next_y, next_x), pos=board[next_x][next_y])
    return False


class AbstractAlgorithm(abc.ABC):
    _board: Board
    _piece: Piece
    _win: pygame.display
    pause: bool = False
    loop: bool = True

    def run(self) -> None:
        """This function runs the algorithm until the user presses the 'r' key"""
        while True:
            if self.loop:
                self._run()
            if self.check_events():
                self._reset()

    def move_piece(self, position: BoardPosition, pos: int) -> None:
        """Use this method to move the piece on the board

        Args:
            position (BoardPosition): The position on the board where the piece needs to be moved to
        """
        self._board.piece.move(position)
        self._board.update(pos=pos)
        pygame.time.wait(400)
        
    def _reset(self) -> None:
        """Resets the board and the piece to their initial state"""
        self._piece.reset_position()
        self._board = Board(parent=self._win, piece=self._piece, size=self._board._size, with_legend=True)
        self._run()

    @abc.abstractmethod
    def _run(self) -> None:
        """Abstract method that needs to be implemented by the subclass

        Raises:
            NotImplementedError: This method needs to be implemented by the subclass
        """
        raise NotImplementedError


    def check_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise SystemExit
                if event.key == pygame.K_r:
                    self._reset()
                    return True
                if event.key == pygame.K_p:
                    self.pause = not self.pause
                    while self.pause:
                        self.check_events()
        return False


class BacktrackingAlgorithm(AbstractAlgorithm):
    
    def __init__(self, piece: Piece, size: int=8) -> None:
        self._piece = piece
        self._size = size
        self._win = pygame.display.set_mode((size*SQ_SIZE, size*SQ_SIZE))
        self._board = Board(size=self._size,parent=self._win, piece=self._piece, with_legend=True)
        
    def _run(self) -> None:
        solveKT(n=self._size, bkalg=self)
        self.loop = False