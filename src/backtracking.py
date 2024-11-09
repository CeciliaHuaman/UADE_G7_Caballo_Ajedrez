from __future__ import annotations
import pygame
import abc
from src.utils.tablero import Board, BoardPosition, Piece, SQ_SIZE

def isSafe(x, y, board, size):
    '''
        A utility function to check if i,j are valid indexes 
        for N*N chessboard
    '''
    if 0 <= x < size and 0 <= y < size and board[x][y] == -1:
        return True
    return False

def solveKT(n, bkalg: AbstractAlgorithm):
    '''
        This function solves the Knight Tour problem using 
        Backtracking. This function mainly uses solveKTUtil() 
        to solve the problem. It returns false if no complete 
        tour is possible, otherwise return true and prints the 
        tour. 
        Please note that there may be more than one solutions, 
        this function prints one of the feasible solutions.
    '''

    # Initialization of Board matrix
    board = [[-1 for i in range(n)]for i in range(n)]

    # move_x and move_y define next move of Knight.
    # move_x is for next value of x coordinate
    # move_y is for next value of y coordinate
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    # Start Knight's Tour from the first block
    x_position, y_position = bkalg._piece.position
    board[x_position][y_position] = 0
    bkalg.move_piece((y_position, x_position), pos=board[x_position][y_position])
    pos = 1

    # Checking if solution exists or not
    if not solveKTUtil(n, board, x_position, y_position, move_x, move_y, pos, bkalg):
        print("Solution does not exist")

def solveKTUtil(n, board, curr_x, curr_y, move_x, move_y, pos, bkalg: AbstractAlgorithm):
    '''
        A recursive utility function to solve Knight Tour problem using 
        Branch and Bound with Warnsdorff's heuristic.
    '''
    bkalg.check_events()
    
    if(pos == n**2):
        return True

    # Try all next moves from the current coordinate x, y
    for i in range(8):
        new_x = curr_x + move_x[i]
        new_y = curr_y + move_y[i]
        if(isSafe(new_x, new_y, board,len(bkalg._board.matrix))):
            board[new_x][new_y] = pos
            bkalg.move_piece((new_y, new_x), pos=board[new_x][new_y])
            if(solveKTUtil(n, board, new_x, new_y, move_x, move_y, pos+1,bkalg)):
                return True

            # Backtracking
            board[new_x][new_y] = -1
            bkalg.move_piece((new_y, new_x), pos=board[new_x][new_y])
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