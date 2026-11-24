from persistencia.gestor_almacenamiento import GestorAlmacenamiento
from modelo.biblioteca import Biblioteca
from controlador.gestor_biblioteca import GestorBiblioteca
from vista.menu import Menu

# arranca el programa y une algunos archivos para que funcione 

def main():
    # ficheros y log
    almacenamiento = GestorAlmacenamiento()
    # colecciones
    biblioteca = Biblioteca()
    # operaciones y reglas
    controlador = GestorBiblioteca(biblioteca, almacenamiento)
    # usuario
    menu = Menu(controlador)
    menu.ejecutar()


if __name__ == "__main__":
    main()
