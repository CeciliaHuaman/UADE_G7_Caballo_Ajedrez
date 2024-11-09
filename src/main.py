from src.utils.game import Game
from src.utils.tablero import Piece
from src.backtracking import BacktrackingAlgorithm
from src.branch_bound import BNBAlgorithm
from pathlib import Path

if __name__ == "__main__":
    size = int(input("Ingrese el tamanio del tablero: "))
    x = int(input(f"Ingrese la position en X (entre 0 y {size-1}): "))
    y = int(input(f"Ingrese la position en Y (entre 0 y {size-1}): "))
    opt = int(input("Que algoritmo quiere utilizar?\n1- Backtracking Basico\n2- Backtracking Branch & Bound\nIngrese su opcion: "))
    piece = Piece(start_pos=(x,y), image_path=Path("src/utils/knight_white.png"))
    algorithm = BacktrackingAlgorithm(piece=piece, size=size) if opt == 1 else BNBAlgorithm(piece=piece, size=size)
    game = Game(algorithm=algorithm)
    game.run()