# errores.py: todas las excepciones propias de la biblioteca.
# El controlador y la persistencia las lanzan; el menú las captura y las muestra.


class ErrorBiblioteca(Exception):
    """Error base: cualquier fallo esperado de la aplicación."""

    def __init__(self, mensaje, codigo=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo


# ---------- Búsquedas ----------
class LibroNoEncontrado(ErrorBiblioteca):
    def __init__(self, codigo):
        super().__init__(f"El libro no existe (código: {codigo})", codigo)


class SocioNoEncontrado(ErrorBiblioteca):
    def __init__(self, codigo):
        super().__init__(f"El socio no existe (código: {codigo})", codigo)


# ---------- Reglas de préstamo ----------
class LibroNoDisponible(ErrorBiblioteca):
    def __init__(self, codigo_libro, codigo_socio):
        super().__init__(
            f"El libro ya lo tiene el socio {codigo_socio} (código: {codigo_libro})",
            codigo_libro)


class SocioConLibro(ErrorBiblioteca):
    def __init__(self, codigo_socio, codigo_libro):
        super().__init__(
            f"El socio ya tiene el libro {codigo_libro} (código: {codigo_socio})",
            codigo_socio)


class SocioSinLibro(ErrorBiblioteca):
    def __init__(self, codigo_socio):
        super().__init__(
            f"El socio no tiene ningún libro prestado (código: {codigo_socio})",
            codigo_socio)


# ---------- Altas ----------
class DatoInvalido(ErrorBiblioteca):
    """Campo vacío o con formato incorrecto."""


class ElementoDuplicado(ErrorBiblioteca):
    def __init__(self, tipo, codigo):
        super().__init__(f"Ya existe un {tipo} con ese código (código: {codigo})", codigo)


# ---------- Ficheros ----------
class ErrorAlmacenamiento(ErrorBiblioteca):
    """No se pudo leer o guardar un fichero de datos."""


class DatosCorruptos(ErrorAlmacenamiento):
    def __init__(self, ruta, numero_linea):
        super().__init__(f"Línea {numero_linea} mal formada en {ruta}", numero_linea)
