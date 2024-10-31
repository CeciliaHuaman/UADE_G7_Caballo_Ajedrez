from utils.tablero import Game, movementAlgorithm

if __name__ == "__main__":
    # Ejecuto el algoritmo y le asigno a movements el resultado
    movements = [
        (0,0),
        (0,1),
        (0,2),
        (0,3),
        (0,4),
        (0,5),
        (0,6),
        (1,4),
        (2,5),
    ]

    board_algorithm = movementAlgorithm(movements=movements)
    game = Game(algorithm=board_algorithm)
    game.run()