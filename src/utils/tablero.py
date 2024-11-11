from __future__ import annotations  # Ensures compatibility with type hints for future versions of Python
import pygame  # Imports the Pygame library for graphics and event handling
from pathlib import Path  # Imports Path for handling file paths
from src.utils.game import SQ_SIZE  # Imports SQ_SIZE constant for square size

BoardPosition = tuple[int, int]  # Defines a type alias for a position on the board

class Board:

    def __init__(
        self, size, parent: pygame.Surface, piece: Piece, with_legend: bool = False
    ) -> None:
        self._size = size  # Sets the board size
        self._board = [[-1 for _ in range(size)] for _ in range(size)]  # Initializes the board matrix with -1 (unvisited cells)
        self._parent = parent  # Sets the parent Pygame surface where the board will be drawn
        self._with_legend = with_legend  # Determines if row and column legends are displayed
        self.surface  # Accesses the surface property to initialize the board display
        self.piece = piece  # Sets the piece to be displayed on the board

    @property
    def surface(self) -> pygame.Surface:
        """This function creates a chess board with alternating colors

        Returns:
            pygame.Surface: A Pygame surface representing the chessboard
        """
        surface = pygame.Surface((self._size * SQ_SIZE, self._size * SQ_SIZE))  # Creates a new Pygame surface for the board
        font = pygame.font.Font(None, 24)  # Loads a default font for text rendering
        font_color = (64, 64, 64)  # Sets color for text (legends)
        
        # Loops through each cell to create the checkerboard pattern
        for i in range(len(self._board)):
            for j in range(len(self._board)):
                if (i + j) % 2 == 0:  # Alternates color for each cell based on position
                    color = (209, 139, 71)  # Dark tile color
                else:
                    color = (255, 206, 158)  # Light tile color
                tile_surface = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)  # Creates a surface for each tile
                tile_surface.fill(color=color)  # Fills the tile with the selected color
                
                if self._board[i][j] >= 0:  # If a move number is recorded in the tile, displays it
                    color = (0, 130, 0)  # Color for a tile with a recorded move
                    tile_surface.fill(color=color)  # Fills the tile with the recorded move color
                    text = font.render(str(self._board[i][j]), True, "white")  # Renders the move number as text
                    text_rect = text.get_rect(center=(SQ_SIZE // 2, SQ_SIZE // 2))  # Centers the text on the tile
                    tile_surface.blit(text, text_rect)  # Draws the text on the tile
                
                if self._board[i][j] < -1:  # Indicates an error if the board has invalid data
                    color = (130, 0, 0)  # Color for error indication
                    tile_surface.fill(color=color)  # Fills the tile with the error color
                    text = font.render("ERR", True, "white")  # Renders "ERR" as error text
                    text_rect = text.get_rect(center=(SQ_SIZE // 2, SQ_SIZE // 2))  # Centers the error text
                    tile_surface.blit(text, text_rect)  # Draws the error text on the tile

                surface.blit(tile_surface, (j * SQ_SIZE, i * SQ_SIZE))  # Places each tile on the main surface

        if self._with_legend:  # Adds row and column legends if enabled
            for i in range(self._size):
                text = font.render(str(i + 1), True, font_color)  # Renders row number
                text_rect = text.get_rect(center=(20, i * SQ_SIZE + 20))  # Positions row legend on the left
                surface.blit(text, text_rect)  # Draws row legend on the board surface

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
        if self._board[position[0]][position[1]] == -1:
            self._board[position[0]][position[1]] = pos
        else:
            self._board[position[0]][position[1]] = -2


class Piece:

    def __init__(self, image_path: Path, start_pos: BoardPosition = (0, 0)) -> None:
        self._position = start_pos  # Sets the initial position of the piece
        self._start_pos = start_pos  # Stores the start position for reset
        assert image_path.exists()  # Verifies that the image file exists
        image = pygame.image.load(image_path)  # Loads the image from the specified path
        self._image = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)  # Creates a Pygame surface for the piece
        image = pygame.transform.scale(image, (SQ_SIZE * 0.8, SQ_SIZE * 0.8))  # Scales the image to fit the tile
        self._image.blit(image, image.get_rect(center=(SQ_SIZE // 2, SQ_SIZE // 2)))  # Centers the image on the piece surface

    def draw(self, board_surface: pygame.Surface):
        pixel_x = self._position[1] * SQ_SIZE  # Calculates x position in pixels based on column index
        pixel_y = self._position[0] * SQ_SIZE  # Calculates y position in pixels based on row index
        board_surface.blit(self._image, (pixel_x, pixel_y))  # Draws the piece on the board surface at calculated position

    def move(self, position: BoardPosition) -> None:
        """Moves the piece to a specified position on the board

        Args:
            position (BoardPosition): The new position of the piece
        """
        self._position = position  # Updates the piece's position

    def reset_position(self) -> None:
        self._position = self._start_pos  # Resets the piece to its starting position

    @property
    def position(self) -> BoardPosition:
        return self._position  # Returns the current position of the piece