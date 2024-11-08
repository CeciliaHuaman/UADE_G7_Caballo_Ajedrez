from __future__ import annotations
import pygame
from pathlib import Path
import abc

pygame.init()
pygame.font.init()


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




BoardPosition = tuple[int, int]

SQ_SIZE = 80

class Board:

    def __init__(
        self, size, parent: pygame.Surface, piece: Piece, with_legend: bool = False
    ) -> None:
        self._size = size
        self._board = [[-1 for _ in range(size)] for _ in range(size)]
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
        surface = pygame.Surface((self._size*SQ_SIZE, self._size*SQ_SIZE))
        font = pygame.font.Font(None, 24)
        font_color = (64, 64, 64)
        for i in range(len(self._board)):
            for j in range(len(self._board)):
                if (i + j) % 2 == 0:
                    color = (209, 139, 71)
                else:
                    color = (255, 206, 158)
                tile_surface = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
                tile_surface.fill(color=color)
                if self._board[i][j] >= 0:
                    color = (0, 130, 0)
                    tile_surface.fill(color=color)
                    text = font.render(str(self._board[i][j]), True, "white")
                    text_rect = text.get_rect(center=(SQ_SIZE // 2, SQ_SIZE // 2))
                    tile_surface.blit(text, text_rect)
                if self._board[i][j] < -1:
                    color = (130, 0, 0)
                    tile_surface.fill(color=color)
                    text = font.render("ERR", True, "white")
                    text_rect = text.get_rect(center=(SQ_SIZE // 2, SQ_SIZE // 2))
                    tile_surface.blit(text, text_rect)

                surface.blit(tile_surface,(j * SQ_SIZE, i * SQ_SIZE))

        if self._with_legend:
            for i in range(self._size):
                text = font.render(str(i + 1),True, font_color)
                text_rect = text.get_rect(center=(20, i * SQ_SIZE + 20))
                surface.blit(text, text_rect)

                text = font.render(chr(65 + i),True, font_color)
                text_rect = text.get_rect(center=(i * SQ_SIZE + 65, (self._size*SQ_SIZE)-20))
                surface.blit(text, text_rect)
        return surface

    def update(self, pos: int) -> None:
        position = self.piece.position
        self._set_checked(position, pos=pos)
        board = self.surface
        self.piece.draw(board_surface=board)
        self._parent.blit(board, (0, 0))
        pygame.display.flip()

    @property
    def matrix(self) -> list[list[int]]:
        return self._board

    def _set_checked(self, position: BoardPosition, pos: int) -> None:
        if self._board[position[1]][position[0]] == -1:
            self._board[position[1]][position[0]] = pos
        else:
            self._board[position[1]][position[0]] = -2


class Piece:

    def __init__(self, image_path: Path, start_pos: BoardPosition = (0, 0)) -> None:
        self._position = start_pos
        self._start_pos = start_pos
        assert image_path.exists()
        image = pygame.image.load(image_path)
        self._image = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
        image = pygame.transform.scale(image, (SQ_SIZE * 0.8, SQ_SIZE * 0.8))
        self._image.blit(image, image.get_rect(center=(SQ_SIZE // 2, SQ_SIZE // 2)))

    def draw(self, board_surface: pygame.Surface):
        pixel_x = self._position[0] * SQ_SIZE  # Column index times tile size for X
        pixel_y = self._position[1] * SQ_SIZE  # Row index times tile size for Y

        # Draw the image at the calculated pixel position on the main surface
        board_surface.blit(self._image, (pixel_x, pixel_y))

    def move(self, position: BoardPosition) -> None:
        """This function moves a piece to a given position on the board

        Args:
            position (BoardPosition): The position on the board where the piece needs to be moved to
        """
        self._position = position

    def reset_position(self) -> None:
        self._position = self._start_pos

    @property
    def position(self) -> BoardPosition:
        return self._position


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

class Game:
    def __init__(self, algorithm: AbstractAlgorithm) -> None:
        self._algorithm = algorithm
        pygame.display.set_caption("Chess backtraking TPO")

    def run(self) -> None:
        self._algorithm.run()
