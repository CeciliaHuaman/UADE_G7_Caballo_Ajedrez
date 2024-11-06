from __future__ import annotations
import pygame
from random import randint
import abc
import time



# Python3 program to solve Knight Tour problem using Branch and Bound with Warnsdorff’s heuristic

# Chessboard Size
n = 8

def isSafe(x, y, board):
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

def countNextMoves(x, y, board, move_x, move_y):
    '''
        Count the number of possible moves from position (x, y).
    '''
    count = 0
    for i in range(8):
        new_x, new_y = x + move_x[i], y + move_y[i]
        if isSafe(new_x, new_y, board):
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
        
        if isSafe(new_x, new_y, board):  # Verificamos si el movimiento es seguro (dentro del tablero y no visitado)
            degree = countNextMoves(new_x, new_y, board, move_x, move_y)  # Contamos las opciones futuras desde (new_x, new_y)
            
            if degree < min_degree:   # Si el número de opciones es menor que el mínimo actual
                min_degree = degree   # Actualizamos min_degree
                next_move = (new_x, new_y)  # Guardamos el mejor movimiento como próximo movimiento
    
    return next_move   # Retornamos el movimiento óptimo

def solveKT(n, x_position, y_position, bkalg: BacktrackingAlgorithm):
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
    board[x_position][y_position] = 0
    bkalg._move_piece((x_position, y_position))
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

    if pos == n**2:
        return True

    # Get the next move with the fewest onward moves
    for i in range(8):
        next_x, next_y = getNextMove(curr_x, curr_y, board, move_x, move_y, bkalg)
        if next_x != -1 and next_y != -1:
            board[next_x][next_y] = pos
            bkalg._move_piece((next_x, next_y))
            time.sleep(2)
            if solveKTUtil(n, board, next_x, next_y, move_x, move_y, pos + 1, bkalg):
                return True
            # Backtracking
            board[next_x][next_y] = -1
    return False




BoardPosition = tuple[int, int]

WIN = pygame.display.set_mode((720, 720))
SQ_SIZE = 90


class Board:

    def __init__(
        self, parent: pygame.Surface, piece: Piece, with_legend: bool = False
    ) -> None:
        self._board = [[0 for _ in range(8)] for _ in range(8)]
        self._parent = parent
        self._with_legend = with_legend
        self.surface
        self.piece = piece

    @property
    def surface(self) -> pygame.Surface:
        """This function creates a chess board with alternating colors

        Returns:
            list[list[tuple[int, int, int]]]: A list of lists representing the chess board
        """
        # Create a chess board with alternating colors for
        surface = pygame.Surface((720, 720))
        for i in range(len(self._board)):
            for j in range(len(self._board)):
                if (i + j) % 2 == 0:
                    color = (209, 139, 71)
                else:
                    color = (255, 206, 158)
                if self._board[i][j] == 1:
                    color = (0, 130, 0)
                if self._board[i][j] > 1:
                    color = (130, 0, 0)
                pygame.draw.rect(
                    surface=surface,
                    color=color,
                    rect=(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE),
                )

        if self._with_legend:
            font = pygame.font.Font(None, 28)
            font_color = (64, 64, 64)
            for i in range(8):
                text = font.render(text=str(i + 1), antialias=True, color=font_color)
                text_rect = text.get_rect(center=(20, i * SQ_SIZE + 20))
                surface.blit(text, text_rect)

                text = font.render(text=chr(97 + i), antialias=True, color=font_color)
                text_rect = text.get_rect(center=(i * SQ_SIZE + 65, 700))
                surface.blit(text, text_rect)
        return surface

    def update(self) -> None:
        position = self.piece.position
        board = self.surface
        board.blit(self.piece.surface, (position[0] * SQ_SIZE, position[1] * SQ_SIZE))
        self._set_checked(position)
        self._parent.blit(board, (0, 0))
        pygame.display.update()

    @property
    def matrix(self) -> list[list[int]]:
        return self._board

    def _set_checked(self, position: BoardPosition) -> None:
        self._board[position[1]][position[0]] += 1


class Piece:

    def __init__(self, start_pos: BoardPosition = (0, 0)) -> None:
        self._surface = self._get_surface()
        self._position = start_pos

    def _get_surface(self) -> pygame.Surface:
        """This function loads the knight piece from a png file

        Returns:
            pygame.Surface: The knight piece as a pygame surface object
        """
        piece = pygame.Surface((SQ_SIZE, SQ_SIZE))
        piece.set_colorkey((0, 0, 0))
        knight = pygame.image.load("./src/utils/chess_horse.svg")
        knight = pygame.transform.scale(knight, (SQ_SIZE * 0.8, SQ_SIZE * 0.8))
        piece.blit(knight, (SQ_SIZE * 0.1, SQ_SIZE * 0.1))
        return piece

    def move(self, position: BoardPosition) -> None:
        """This function moves a piece to a given position on the board

        Args:
            position (BoardPosition): The position on the board where the piece needs to be moved to
        """
        self._position = position

    @property
    def position(self) -> BoardPosition:
        return self._position

    @property
    def surface(self) -> pygame.Surface:
        return self._surface
    

pause = False

def check_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return True
            if event.key == pygame.K_p:
                global pause
                pause = not pause
                while pause:
                    check_events()
    return False


class AbstractAlgorithm(abc.ABC):
    _board: Board
    _piece: Piece

    def run(self) -> None:
        """This function runs the algorithm until the user presses the 'r' key"""
        while True:
            self._run()
            pause = True
            if check_events():
                self._reset()

    def _move_piece(self, position: BoardPosition) -> None:
        """Use this method to move the piece on the board

        Args:
            position (BoardPosition): The position on the board where the piece needs to be moved to
        """
        self._board.piece.move(position)
        self._board.update()
        pygame.time.wait(500)
        
    def _reset(self) -> None:
        """Resets the board and the piece to their initial state"""
        self._board = Board(parent=WIN, piece=self._piece)

    @abc.abstractmethod
    def _run(self) -> None:
        """Abstract method that needs to be implemented by the subclass

        Raises:
            NotImplementedError: This method needs to be implemented by the subclass
        """
        raise NotImplementedError


class RandomAlgorithm(AbstractAlgorithm):

    def __init__(self, piece: Piece=Piece()) -> None:
        self._piece = piece
        self._board = Board(parent=WIN, piece=self._piece)

    def _run(self) -> None:
        """This method moves the piece to a random position on the board"""
        while True:
            position = self._get_random_position()
            self._move_piece(position)
            # Only useful for the RandomAlgorithm
            if check_events():
                self._reset()

    def _get_random_position(self) -> BoardPosition:
        """Generates a random position for the piece on the board

        Returns:
            BoardPosition: A tuple representing the position on the board
        """
        position = (randint(0, 7), randint(0, 7))
        return position



class BacktrackingAlgorithm(AbstractAlgorithm):
    
    def __init__(self, piece: Piece=Piece()) -> None:
        self._piece = piece
        self._board = Board(parent=WIN, piece=self._piece)
        
        solveKT(8, 2, 4, self)

    def _run(self) -> None:
        if check_events():
            self._reset()

class Game:
    def __init__(self, algorithm: AbstractAlgorithm) -> None:
        self._algorithm = algorithm

    def run(self) -> None:
        pygame.init()
        self._algorithm.run()
        pygame.quit()


if __name__ == "__main__":
    game = Game(algorithm=BacktrackingAlgorithm())
    game.run()
