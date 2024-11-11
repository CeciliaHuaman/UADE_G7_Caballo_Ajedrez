SQ_SIZE = 80  # Tamaño de cada casilla del tablero
import pygame  # Importa el módulo Pygame para la gestión de la interfaz gráfica
import sys  # Importa el módulo sys para manejar la salida del programa

from src.backtracking import AbstractAlgorithm  # Importa la clase AbstractAlgorithm del módulo backtracking

# Inicializa los módulos de Pygame y la fuente para los textos
pygame.init()  
pygame.font.init()

# Configuración de la pantalla, colores y fuentes

WIDTH, HEIGHT = 600, 400  # Ancho y alto de la pantalla
WHITE = (255, 255, 255)  # Color blanco
BLACK = (0, 0, 0)  # Color negro
BLUE = (0, 100, 255)  # Color azul
BACK = (255, 206, 158)  # Color de fondo
FONT = pygame.font.Font(None, 24)  # Fuente de texto con tamaño 24

# Clase principal del juego que maneja la ejecución del algoritmo
class Game:
    def __init__(self, algorithm: AbstractAlgorithm) -> None:
        # Inicializa el juego con un algoritmo pasado como parámetro
        self._algorithm = algorithm
        pygame.display.set_caption("Chess backtracking TPO")  # Establece el título de la ventana
        
    def run(self) -> None:
        # Ejecuta el algoritmo en un bucle
        self._algorithm.run()

# Clase que maneja la interfaz de entrada del usuario para configurar el juego
class GameInput:
    def __init__(self):
        # Configura la pantalla de entrada con las dimensiones especificadas
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess backtracking TPO Options")  # Título de la ventana
        
        # Inicializa los textos vacíos para los campos de entrada
        self.size_text = ''
        self.x_text = ''
        self.y_text = ''
        self.opt_text = ''
        
        # Establece qué campo de entrada está activo (el que el usuario está editando)
        self.active_input = None
        
        # Diccionario con la configuración de cada campo de entrada (posición, tamaño, texto y etiqueta)
        self.inputs = {
            "size": {"rect": pygame.Rect(260, 70, 80, 32), "text": '', "label": "Tamaño del tablero: "},
            "x": {"rect": pygame.Rect(260, 120, 80, 32), "text": '', "label": "Posición inicial Fila: "},
            "y": {"rect": pygame.Rect(260, 170, 80, 32), "text": '', "label": "Posición inicial Columna: "},
            "opt": {"rect": pygame.Rect(260, 270, 80, 32), "text": '', "label": "Ingrese su opcion: "}
        }

    def run(self):
        # Bucle principal de la interfaz de entrada
        while True:
            # Rellena la pantalla con el color de fondo definido
            self.screen.fill(BACK)
            
            # Recorre todos los eventos que ocurren
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Cierra Pygame si el usuario cierra la ventana
                    sys.exit()  # Sale del programa
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Si el usuario hace clic, se gestiona el evento del mouse
                    self.handle_mouse_event(event)
                elif event.type == pygame.KEYDOWN:
                    # Si el usuario presiona una tecla, se gestiona el evento de la tecla
                    self.handle_key_event(event)
            
            # Dibuja los campos de entrada en la pantalla
            self.draw_inputs()
            pygame.display.flip()  # Actualiza la pantalla

            # Si todos los campos tienen texto, devuelve los valores ingresados
            if all(input_data["text"] for input_data in self.inputs.values()):
                return int(self.inputs["size"]["text"]), int(self.inputs["x"]["text"]), int(self.inputs["y"]["text"]), int(self.inputs["opt"]["text"])

    def handle_mouse_event(self, event):
        # Gestiona el evento de clic en el mouse
        for key, input_data in self.inputs.items():
            # Si el clic es dentro del área del campo de entrada, lo activa
            if input_data["rect"].collidepoint(event.pos):
                self.active_input = key  # Activa el campo correspondiente

    def handle_key_event(self, event):
        # Gestiona la entrada de texto en el campo activo
        if self.active_input:
            if event.key == pygame.K_BACKSPACE:
                # Si se presiona "Backspace", elimina el último carácter del campo activo
                self.inputs[self.active_input]["text"] = self.inputs[self.active_input]["text"][:-1]
            elif event.key in range(pygame.K_0, pygame.K_9 + 1):
                # Si se presiona una tecla numérica, agrega el carácter al campo de texto activo
                self.inputs[self.active_input]["text"] += event.unicode

    def draw_inputs(self):

        tittle_label = FONT.render("Chess Knight's Tour Options", True, BLACK)
        self.screen.blit(tittle_label, (150, 15))

        # Dibuja todos los campos de entrada en la pantalla
        for key, input_data in self.inputs.items():

            if key == "opt":
                {
                    # Draw the options for algorithm selection
                    self.draw_algorithm_options()
                }

            # Renderiza la etiqueta del campo de entrada (por ejemplo, "Tamaño del tablero")
            label_surface = FONT.render(input_data["label"], True, BLACK)
            
            # Dibuja la etiqueta en la pantalla
            self.screen.blit(label_surface, (input_data["rect"].x - 210, input_data["rect"].y + 10 ))

            # Dibuja el borde del campo de entrada, azul si está activo, negro si no lo está
            pygame.draw.rect(self.screen, BLUE if self.active_input == key else BLACK, input_data["rect"], 2)

            # Renderiza el texto ingresado en el campo de entrada
            text_surface = FONT.render(input_data["text"], True, BLACK)

            # Dibuja el texto dentro del campo de entrada (en el lugar correspondiente)
            self.screen.blit(text_surface, (input_data["rect"].x + 5, input_data["rect"].y + 5))
        

    def draw_algorithm_options(self):
        # Render and position the question label
        question_label = FONT.render("¿Qué algoritmo quiere utilizar?", True, BLACK)
        self.screen.blit(question_label, (50, 210))
        opt1_label = FONT.render("1- Backtracking Básico", True, BLACK)
        self.screen.blit(opt1_label, (60, 235))
        opt2_label = FONT.render("2- Branch & Bound", True, BLACK)
        self.screen.blit(opt2_label, (60, 255))