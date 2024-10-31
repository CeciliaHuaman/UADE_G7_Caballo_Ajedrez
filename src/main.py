from utils.tablero import Game, movementAlgorithm
from backtracking import solveKT

if __name__ == "__main__":
    n = 8
    
    # Ejecuto el algoritmo y le asigno a movements el resultado
    movements = solveKT(n)
    board_algorithm = movementAlgorithm(size=n, movements=movements)
    game = Game(algorithm=board_algorithm)
    game.run()
