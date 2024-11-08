SQ_SIZE = 80

import pygame
from src.backtracking import AbstractAlgorithm

pygame.init()
pygame.font.init()


class Game:
    def __init__(self, algorithm: AbstractAlgorithm) -> None:
        self._algorithm = algorithm
        pygame.display.set_caption("Chess backtraking TPO")

    def run(self) -> None:
        
        self._algorithm.run()