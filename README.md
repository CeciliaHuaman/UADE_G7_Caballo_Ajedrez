uade-g7-caballo-ajedrez

Versión: 0.1.0

### Autores: 

- Cecilia Huaman
- Mathias Del Vecchio
- Guillermo Cerna

Descripción

Este proyecto, llamado Chess Backtracking TPO, implementa un recorrido del caballo en un tablero de ajedrez utilizando algoritmos de Backtracking y Branch and Bound en el contexto de un Trabajo Práctico Obligatorio (TPO). La solución permite explorar el comportamiento de estos algoritmos en diferentes configuraciones de tamaño de tablero y posiciones iniciales, y se enfoca en la eficiencia a través de la optimización del recorrido.

Requisitos

Python: 3.10 o superior
Poetry: Utilizado para gestionar las dependencias y el entorno virtual del proyecto.

Instalación

### Clonar el repositorio:
    git clone https://github.com/tu_usuario/uade-g3-caballo-ajedrez.git
    cd uade-g3-caballo-ajedrez

Instalar dependencias: Este proyecto utiliza Poetry para manejar dependencias. Si no tienes Poetry instalado, puedes instalarlo ejecutando:
    pip install poetry
Configurar el entorno: Ejecuta el siguiente comando para instalar las dependencias especificadas en pyproject.toml:
    poetry install
Iniciar el entorno virtual: Activa el entorno virtual de Poetry:
    poetry shell

### Uso
Este proyecto cuenta con una interfaz gráfica construida en Pygame que permite seleccionar:

El tamaño del tablero
La posición inicial del caballo
El algoritmo de recorrido (Backtracking o Branch and Bound)
Para ejecutar el proyecto:

python src/main.py
Estructura del Proyecto

src/: Contiene el código fuente del proyecto.
README.md: Explica el proyecto y los pasos de configuración.
pyproject.toml: Archivo de configuración de Poetry para gestionar las dependencias y el entorno de desarrollo.
Dependencias

pygame: Usado para crear la interfaz gráfica del proyecto y visualizar el recorrido del caballo en el tablero.
pygame-textinput: Facilita la entrada de texto en la interfaz gráfica.
Contribución

Este es un proyecto académico, pero si deseas contribuir, puedes abrir un pull request o reportar problemas en el repositorio.
