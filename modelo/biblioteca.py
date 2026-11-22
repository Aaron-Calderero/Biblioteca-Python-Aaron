# biblioteca.py: guarda las colecciones de libros y socios
# y permite buscar y añadir elementos.
# No decide reglas de préstamo, no usa input()/print() y no toca ficheros.



class Biblioteca:
    def __init__(self):
        self.libros = []
        self.socios = []

    # ---------- Búsquedas ----------
    def buscar_libro(self, codigo):
        for libro in self.libros:
            if libro.codigo.upper() == codigo.upper():
                return libro
        return None

    def buscar_socio(self, codigo):
        for socio in self.socios:
            if socio.codigo.upper() == codigo.upper():
                return socio
        return None

    def libros_disponibles(self):
        return [libro for libro in self.libros if libro.esta_disponible()]

    def buscar_por_titulo(self, termino):
        return [libro for libro in self.libros if libro.coincide_titulo(termino)]

    def socios_con_libro(self):
        resultado = []
        for socio in self.socios:
            if socio.tiene_libro():
                libro = self.buscar_libro(socio.codigo_libro)
                titulo = libro.titulo if libro else "(libro desconocido)"
                resultado.append((socio, titulo))
        return resultado

    # ---------- Altas ----------
    def agregar_libro(self, libro):
        self.libros.append(libro)

    def agregar_socio(self, socio):
        self.socios.append(socio)
