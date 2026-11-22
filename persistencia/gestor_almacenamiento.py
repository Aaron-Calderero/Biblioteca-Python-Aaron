# gestiona las acciones de los archivos datos y log


import os
from datetime import datetime
from modelo.libro import Libro
from modelo.socio import Socio
from errores.errores import ErrorAlmacenamiento, DatosCorruptos


class GestorAlmacenamiento:
    def __init__(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ruta_libros = os.path.join(base, "datos", "libros.txt")
        self.ruta_socios = os.path.join(base, "datos", "socios.txt")
        self.ruta_log = os.path.join(base, "log.txt")

    def cargar_libros(self):
        libros = []
        for numero, linea in self._leer_lineas(self.ruta_libros):
            partes = linea.strip().split(";")
            if len(partes) != 6:
                raise DatosCorruptos(self.ruta_libros, numero)
            libros.append(Libro(*partes))
        return libros

    def cargar_socios(self):
        socios = []
        for numero, linea in self._leer_lineas(self.ruta_socios):
            partes = linea.strip().split(";")
            if len(partes) != 4:
                raise DatosCorruptos(self.ruta_socios, numero)
            socios.append(Socio(*partes))
        return socios

    def guardar_datos(self, libros, socios):
        try:
            with open(self.ruta_libros, "w", encoding="utf-8") as fichero:
                for libro in libros:
                    fichero.write(libro.a_linea() + "\n")
            with open(self.ruta_socios, "w", encoding="utf-8") as fichero:
                for socio in socios:
                    fichero.write(socio.a_linea() + "\n")
        except OSError as error:
            raise ErrorAlmacenamiento("No se pudieron guardar los datos") from error

    def registrar_log(self, evento, detalles):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.ruta_log, "a", encoding="utf-8") as fichero:
                fichero.write(f"[{fecha}][{evento}][{detalles}]\n")
        except OSError:
            pass  # si el log falla, el programa sigue funcionando

    def _leer_lineas(self, ruta):
        lineas = []
        try:
            with open(ruta, "r", encoding="utf-8") as fichero:
                for numero, linea in enumerate(fichero, start=1):
                    if linea.strip():
                        lineas.append((numero, linea))
        except FileNotFoundError:
            pass  # si el fichero no existe, empezamos sin datos
        except OSError as error:
            raise ErrorAlmacenamiento(f"No se pudo leer {ruta}") from error
        return lineas
