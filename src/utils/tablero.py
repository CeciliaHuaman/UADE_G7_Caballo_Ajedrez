from __future__ import annotations
import pygame
from pathlib import Path
from src.utils.game import SQ_SIZE

BoardPosition = tuple[int, int]

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
