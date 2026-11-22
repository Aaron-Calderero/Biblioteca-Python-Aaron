# Realiza las operaciones y comprueba las reglas.
# Recibe peticiones del menú, usa el modelo (Biblioteca) y el almacenamiento.
# Si algo no es válido, lanza una excepción de errores/errores.py.

from modelo.libro import Libro
from modelo.socio import Socio
from errores.errores import (
    ErrorBiblioteca, LibroNoEncontrado, SocioNoEncontrado, LibroNoDisponible,
    SocioConLibro, SocioSinLibro, DatoInvalido, ElementoDuplicado)


class GestorBiblioteca:
    def __init__(self, biblioteca, almacenamiento):
        self.biblioteca = biblioteca
        self.almacenamiento = almacenamiento
        self.biblioteca.libros = almacenamiento.cargar_libros()
        self.biblioteca.socios = almacenamiento.cargar_socios()
        almacenamiento.registrar_log(
            "INICIO",
            f"Cargados {len(self.biblioteca.libros)} libros "
            f"y {len(self.biblioteca.socios)} socios")

    # ---------- Consultas (el menú no toca el modelo directamente) ----------
    def obtener_libros(self):
        return self.biblioteca.libros

    def obtener_socios(self):
        return self.biblioteca.socios

    def libros_disponibles(self):
        return self.biblioteca.libros_disponibles()

    def buscar_por_titulo(self, termino):
        return self.biblioteca.buscar_por_titulo(termino)

    def socios_con_libro(self):
        return self.biblioteca.socios_con_libro()

    # ---------- Préstamos ----------
    def prestar_libro(self, codigo_libro, codigo_socio):
        try:
            libro = self.biblioteca.buscar_libro(codigo_libro)
            socio = self.biblioteca.buscar_socio(codigo_socio)
            if libro is None:
                raise LibroNoEncontrado(codigo_libro)
            if socio is None:
                raise SocioNoEncontrado(codigo_socio)
            if not libro.esta_disponible():
                raise LibroNoDisponible(libro.codigo, libro.codigo_socio)
            if socio.tiene_libro():
                raise SocioConLibro(socio.codigo, socio.codigo_libro)
            libro.prestar(socio.codigo)
            socio.recibir_libro(libro.codigo)
            self.almacenamiento.registrar_log(
                "PRESTAMO", f"Libro {libro.codigo} prestado al socio {socio.codigo}")
            return libro, socio
        except ErrorBiblioteca as error:
            self.almacenamiento.registrar_log("ERROR_PRESTAMO", str(error))
            raise

    def devolver_libro(self, codigo_socio):
        try:
            socio = self.biblioteca.buscar_socio(codigo_socio)
            if socio is None:
                raise SocioNoEncontrado(codigo_socio)
            if not socio.tiene_libro():
                raise SocioSinLibro(socio.codigo)
            codigo_libro = socio.devolver_libro()
            libro = self.biblioteca.buscar_libro(codigo_libro)
            if libro is not None:
                libro.devolver()
            self.almacenamiento.registrar_log(
                "DEVOLUCION", f"Libro {codigo_libro} devuelto por el socio {socio.codigo}")
            return codigo_libro, socio
        except ErrorBiblioteca as error:
            self.almacenamiento.registrar_log("ERROR_DEVOLUCION", str(error))
            raise

    # ---------- Altas ----------
    def anadir_socio(self, codigo, nombre, email):
        if not codigo or not nombre or not email:
            raise DatoInvalido(f"Todos los campos son obligatorios (código: {codigo})", codigo)
        if self.biblioteca.buscar_socio(codigo) is not None:
            raise ElementoDuplicado("socio", codigo)
        self.biblioteca.agregar_socio(Socio(codigo, nombre, email))
        self.almacenamiento.registrar_log("ALTA_SOCIO", f"Socio {codigo} - {nombre}")

    def anadir_libro(self, codigo, titulo, autor, anio, categoria):
        if not codigo or not titulo or not autor or not categoria:
            raise DatoInvalido(f"Todos los campos son obligatorios (código: {codigo})", codigo)
        if self.biblioteca.buscar_libro(codigo) is not None:
            raise ElementoDuplicado("libro", codigo)
        if not anio.isdigit():
            raise DatoInvalido(f"El año debe ser un número (código: {codigo})", codigo)
        self.biblioteca.agregar_libro(Libro(codigo, titulo, autor, anio, categoria))
        self.almacenamiento.registrar_log("ALTA_LIBRO", f"Libro {codigo} - {titulo}")

    # ---------- Salir ----------
    def guardar_datos(self):
        self.almacenamiento.guardar_datos(
            self.biblioteca.libros, self.biblioteca.socios)
        self.almacenamiento.registrar_log("FIN", "Datos guardados en los ficheros")
