from src.utils.tablero import Piece,Game,BacktrackingAlgorithm

if __name__ == "__main__":
    size = int(input("Ingrese el tamanio del tablero: "))
    x = int(input(f"Ingrese la position en X (entre 0 y {size-1}): "))
    y = int(input(f"Ingrese la position en Y (entre 0 y {size-1}): "))
    piece = Piece(start_pos=(x,y))
    game = Game(algorithm=BacktrackingAlgorithm(piece=piece, size=size))
    game.run()
