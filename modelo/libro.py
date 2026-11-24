class Libro:
    def __init__(self, codigo, titulo, autor, anio, categoria, codigo_socio=""):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self.categoria = categoria
        self.codigo_socio = codigo_socio

    def esta_disponible(self):
        return self.codigo_socio == ""

    def prestar(self, codigo_socio):
        self.codigo_socio = codigo_socio

    def devolver(self):
        self.codigo_socio = ""

    def coincide_titulo(self, termino):
        return termino.strip().lower() in self.titulo.lower()

    def a_linea(self):
        return ";".join([self.codigo, self.titulo, self.autor,
                         self.anio, self.categoria, self.codigo_socio])

    def __str__(self):
        if self.esta_disponible():
            estado = "Disponible"
        else:
            estado = "Prestado por socio: " + self.codigo_socio
        return f"{self.codigo:<6} {self.titulo:<38} {self.autor:<24} {self.anio:<5} {estado}"
