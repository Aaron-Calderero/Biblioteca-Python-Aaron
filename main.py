from modelo.libro import Libro
from modelo.socio import Socio

libro = Libro("L001", "El Quijote", "Cervantes", 1605, "Novela")
socio = Socio("S001", "Ana", "ana@mail.com")

print(libro.titulo, libro.codigo_socio)
print(socio.nombre, socio.codigo_libro)