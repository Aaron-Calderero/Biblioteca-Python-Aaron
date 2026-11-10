class Socio:
    SEPARADOR = ";"

    def __init__(self, codigo, nombre, email, codigo_libro=None):
        self.codigo = codigo
        self.nombre = nombre
        self.email = email
        self.codigo_libro = codigo_libro

    def tiene_libro(self):
        return self.codigo_libro is not None

    def recibir_libro(self, codigo_libro):
        self.codigo_libro = codigo_libro

    def devolver_libro(self):
        codigo = self.codigo_libro
        self.codigo_libro = None
        return codigo

    def a_linea(self):
        libro = self.codigo_libro if self.codigo_libro is not None else "None"
        return self.SEPARADOR.join([self.codigo, self.nombre, self.email, libro])

    @classmethod
    def desde_linea(cls, linea):
        codigo, nombre, email, libro = linea.strip().split(cls.SEPARADOR)
        codigo_libro = None if libro in ("None", "") else libro
        return cls(codigo, nombre, email, codigo_libro)

    def __str__(self):
        libro = self.codigo_libro if self.tiene_libro() else "ninguno"
        return f"{self.codigo:<6} {self.nombre:<25} {self.email:<30} Libro: {libro}"