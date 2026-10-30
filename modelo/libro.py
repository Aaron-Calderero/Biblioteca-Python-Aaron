class Libro:
    SEPARADOR = ";"

    def __init__(self, codigo, titulo, autor, anio, categoria, codigo_socio=None):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.anio = int(anio)
        self.categoria = categoria
        self.codigo_socio = codigo_socio

    def esta_disponible(self):
        return self.codigo_socio is None

    def prestar(self, codigo_socio):
        self.codigo_socio = codigo_socio

    def devolver(self):
        self.codigo_socio = None

    def coincide_titulo(self, termino):
        return termino.strip().lower() in self.titulo.lower()

    def a_linea(self):
        socio = self.codigo_socio if self.codigo_socio is not None else "None"
        campos = [self.codigo, self.titulo, self.autor, str(self.anio), self.categoria, socio]
        return self.SEPARADOR.join(campos)

    @classmethod
    def desde_linea(cls, linea):
        codigo, titulo, autor, anio, categoria, socio = linea.strip().split(cls.SEPARADOR)
        codigo_socio = None if socio in ("None", "") else socio
        return cls(codigo, titulo, autor, anio, categoria, codigo_socio)

    def __str__(self):
        estado = "Disponible" if self.esta_disponible() else f"Prestado a {self.codigo_socio}"
        return f"{self.codigo:<6} {self.titulo[:38]:<38} {self.autor[:24]:<24} {self.anio:<5} {estado}"