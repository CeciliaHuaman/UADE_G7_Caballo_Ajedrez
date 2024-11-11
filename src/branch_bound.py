from __future__ import annotations  # Ensures compatibility with type hints for future versions of Python
import pygame  # Imports the Pygame library for graphical display and event handling
from src.backtracking import AbstractAlgorithm, isSafe, printSolution  # Imports AbstractAlgorithm class and utility functions
from src.utils.tablero import Board, BoardPosition, Piece, SQ_SIZE  # Imports additional modules and constants

def countNextMoves(x, y, board, move_x, move_y, size):
    '''
        Count the number of possible moves from position (x, y).
    '''
    count = 0  # Initializes move count
    for i in range(8):  # Loops through all possible knight moves
        new_x, new_y = x + move_x[i], y + move_y[i]  # Calculates new coordinates after the move
        if isSafe(new_x, new_y, board, size):  # Checks if the move is within bounds and unvisited
            count += 1  # Increments count if the move is valid
    return count  # Returns the total count of valid moves

def getNextMove(x, y, board, move_x, move_y, bkalg: AbstractAlgorithm):
    '''
        Get the next move with the fewest onward moves, following Warnsdorff's rule.
    '''
    min_degree = 8          # Sets the initial minimum degree to 8 (max possible moves for a knight)
    next_move = (-1, -1)    # Initializes the next move as an invalid position

    for i in range(8):  # Loops through all possible knight moves
        new_x, new_y = x + move_x[i], y + move_y[i]  # Calculates potential move coordinates
        if isSafe(new_x, new_y, board, len(bkalg._board.matrix)):  # Checks if the move is within bounds and unvisited
            degree = countNextMoves(new_x, new_y, board, move_x, move_y, len(bkalg._board.matrix))  # Counts onward moves from the new position
            if degree < min_degree:  # If fewer onward moves than current minimum
                min_degree = degree  # Updates minimum degree
                next_move = (new_x, new_y)  # Sets the current move as the best next move
    return next_move  # Returns the optimal next move

def solveKT(n, bkalg: AbstractAlgorithm):
    '''
        This function solves the Knight Tour problem using Branch and Bound with 
        Warnsdorff’s heuristic. It returns false if no complete tour is possible,
        otherwise returns true and prints the tour.
    '''
    board = [[-1 for i in range(n)] for j in range(n)]  # Initializes the board with -1 (unvisited cells)
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]  # Lists all possible x-coordinates of knight moves
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]  # Lists all possible y-coordinates of knight moves

    # Sets the starting position of the knight and marks it as visited
    x_position, y_position = bkalg._piece.position
    board[x_position][y_position] = 0
    bkalg.move_piece((x_position, y_position), pos=board[x_position][y_position])
    pos = 1  # Position counter

    # Attempts to find a complete tour using the utility function
    if not solveKTUtil(n, board, x_position, y_position, move_x, move_y, pos, bkalg):
        print("Solution does not exist")  # Prints if a tour is not possible
    else:
        printSolution(n, board)  # Prints the complete tour if successful

def solveKTUtil(n, board, curr_x, curr_y, move_x, move_y, pos, bkalg: AbstractAlgorithm):
    '''
        A recursive utility function to solve Knight Tour problem using 
        Branch and Bound with Warnsdorff's heuristic.
    '''
    bkalg.check_events()  # Checks for pygame events

    if pos == n**2:  # Base case: if all cells are visited
        return True

    # Tries each possible next move
    for _ in range(8):
        next_x, next_y = getNextMove(curr_x, curr_y, board, move_x, move_y, bkalg)  # Finds the optimal next move
        if next_x != -1 and next_y != -1:  # If a valid move is found
            board[next_x][next_y] = pos  # Marks the cell as visited with the move number
            bkalg.move_piece((next_x, next_y), pos=board[next_x][next_y])  # Moves the piece in Pygame
            if solveKTUtil(n, board, next_x, next_y, move_x, move_y, pos + 1, bkalg):  # Recursively continues the tour
                return True
            # Backtracking step if no solution is found
            board[next_x][next_y] = -1
            bkalg.move_piece((next_x, next_y), pos=board[next_x][next_y])
    return False  # Returns False if no solution exists from this path

class BNBAlgorithm(AbstractAlgorithm):

    def __init__(self, piece: Piece, size: int=8) -> None:
        self._piece = piece  # Initializes the knight piece
        self._size = size  # Sets the board size
        self._win = pygame.display.set_mode((size * SQ_SIZE, size * SQ_SIZE))  # Creates the pygame window
        self._board = Board(size=self._size, parent=self._win, piece=self._piece, with_legend=True)  # Initializes the board display

    def _run(self) -> None:
        solveKT(n=self._size, bkalg=self)  # Starts the knight’s tour algorithm
        self.loop = False  # Ends the loop after the tour is complete