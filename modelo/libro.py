class Libro:

    def __init__(self, codigo,  titulo, autor, anio, categoria, codigo_socio = None):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.anio = int(anio)
        self.categoria = categoria
        self.codigo_socio = codigo_socio