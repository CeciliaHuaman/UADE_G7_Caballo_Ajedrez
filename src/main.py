from src.utils.game import Game,GameInput
from src.utils.tablero import Piece
from src.backtracking import BacktrackingAlgorithm
from src.branch_bound import BNBAlgorithm
from pathlib import Path

if __name__ == "__main__":

    # Inicializar Pygame y mostrar la pantalla de entrada
    input_screen = GameInput()
    size, x, y, opt = input_screen.run()
    
    piece = Piece(start_pos=(x,y), image_path=Path("src/utils/knight_white.png"))
    
    algorithm = BacktrackingAlgorithm(piece=piece, size=size) if opt == 1 else BNBAlgorithm(piece=piece, size=size)
    game = Game(algorithm=algorithm)
    game.run()
