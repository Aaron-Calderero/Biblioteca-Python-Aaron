from modelo.libro import Libro
from modelo.socio import Socio

libros = [Libro(*l.strip().split(";")) for l in open("datos/libros.txt", encoding="utf-8")]
socios = [Socio(*l.strip().split(";")) for l in open("datos/socios.txt", encoding="utf-8")]

print("Se ha cargado la información de los libros.")