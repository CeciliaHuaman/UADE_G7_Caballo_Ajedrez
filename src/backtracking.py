from __future__ import annotations  # Ensures compatibility with type hints for future versions of Python
import pygame  # Imports Pygame for graphical interface and event handling
import time  # Imports time for measuring execution time
import abc  # Imports abc for defining abstract base classes
from src.utils.tablero import Board, BoardPosition, Piece, SQ_SIZE  # Imports required classes and constants

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

def solveKT(n: int, bkalg: BacktrackingAlgorithm) -> None:
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

    x_position, y_position = bkalg._piece.position  # Gets the starting position of the knight
    board[x_position][y_position] = 0  # Marks the starting position as visited

    bkalg.path.append((x_position, y_position))  # Adds starting position to the path
    pos = 1  # Initializes the move count

    if not solveKTUtil(n, board, x_position, y_position, move_x, move_y, pos, bkalg):
        print("Solution does not exist")  # Prints message if no solution is found
        raise SystemExit
    else:
        printSolution(n, board)  # Prints the solution
        
        print(f"--- {time.time() - start_time} seconds ---")  # Displays the execution time

        # Starts Pygame display of the solution path
        for pos, step in enumerate(bkalg.path):
            bkalg.check_events()  # Checks for any Pygame events
            bkalg.move_piece(position=step, pos=pos)  # Moves the piece to the next step in the solution

def solveKTUtil(n: int, board: list[list[int]], curr_x: int, curr_y: int, move_x: list[int], move_y: list[int], pos: int, bkalg: BacktrackingAlgorithm) -> bool:
    '''
        A recursive utility function to solve Knight Tour problem using 
        Branch and Bound with Warnsdorff's heuristic.
    '''
    if pos == n**2:  # If all squares are visited, the tour is complete
        return True

    # Tries all possible moves for the knight from the current position
    for i in range(8):
        new_x = curr_x + move_x[i]
        new_y = curr_y + move_y[i]
        
        if isSafe(new_x, new_y, board, n):  # Checks if the move is valid
            board[new_x][new_y] = pos  # Marks the cell as visited
            bkalg.path.append((new_x, new_y))  # Adds move to path

            if solveKTUtil(n, board, new_x, new_y, move_x, move_y, pos + 1, bkalg):  # Recursive call for next move
                return True

            # Backtracks if no solution is found
            board[new_x][new_y] = -1  # Unmarks the cell
            bkalg.path.pop()  # Removes the move from the path

    return False

class AbstractAlgorithm(abc.ABC):
    _board: Board
    _piece: Piece
    _win: pygame.display
    pause: bool = False
    loop: bool = True

    def run(self) -> None:
        """Runs the algorithm continuously until the user presses 'r' to reset."""
        while True:
            if self.loop:
                self._run()
            if self.check_events():
                self._reset()

    def move_piece(self, position: BoardPosition, pos: int) -> None:
        """Moves the piece to the specified position on the board and updates the display.

        Args:
            position (BoardPosition): New position of the piece on the board.
        """
        self._board.piece.move(position)  # Updates the piece's position
        self._board.update(pos=pos)  # Updates the board display
        pygame.time.wait(400)  # Adds delay for visualization

    def _reset(self) -> None:
        """Resets the board and the piece to their initial state."""
        self._piece.reset_position()  # Resets piece to starting position
        self._board = Board(parent=self._win, piece=self._piece, size=self._board._size, with_legend=True)  # Reinitializes board
        self.loop = True  # Sets loop flag to true

    @abc.abstractmethod
    def _run(self) -> None:
        """Abstract method to be implemented by subclasses."""
        raise NotImplementedError

    def check_events(self) -> bool:
        """Checks for Pygame events (key presses or window close)."""
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

    def __init__(self, piece: Piece, size: int = 8) -> None:
        self._piece = piece  # Sets the piece for the algorithm
        self._size = size  # Sets the board size
        self._win = pygame.display.set_mode((size * SQ_SIZE, size * SQ_SIZE))  # Initializes Pygame display
        self._board = Board(size=self._size, parent=self._win, piece=self._piece, with_legend=True)  # Initializes board with legend
        self.path = list()  # Initializes path to store move sequence
        
    def _run(self) -> None:
        solveKT(n=self._size, bkalg=self)  # Starts the knight's tour algorithm
        self.loop = False  # Stops loop after solving the problem

    def _reset(self) -> None:
        self.path = list()  # Clears path
        super()._reset()  # Calls parent reset method