class Socio:
    def __init__(self, codigo, nombre, email, codigo_libro=""):
        self.codigo = codigo
        self.nombre = nombre
        self.email = email
        self.codigo_libro = codigo_libro

    def tiene_libro(self):
        return self.codigo_libro != ""

    def recibir_libro(self, codigo_libro):
        self.codigo_libro = codigo_libro

    def devolver_libro(self):
        codigo = self.codigo_libro
        self.codigo_libro = ""
        return codigo

    def a_linea(self):
        return ";".join([self.codigo, self.nombre, self.email, self.codigo_libro])
