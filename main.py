import os
from datetime import datetime
from modelo.libro import Libro
from modelo.socio import Socio
from errores.errores import ErrorBiblioteca

BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_LIBROS = os.path.join(BASE, "datos", "libros.txt")
RUTA_SOCIOS = os.path.join(BASE, "datos", "socios.txt")
RUTA_LOG = os.path.join(BASE, "log.txt")


def registrar_log(evento, detalles):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(RUTA_LOG, "a", encoding="utf-8") as fichero:
        fichero.write(f"[{fecha}][{evento}][{detalles}]\n")


def cargar_libros():
    libros = []
    with open(RUTA_LIBROS, "r", encoding="utf-8") as fichero:
        for linea in fichero:
            if linea.strip():
                libros.append(Libro.desde_linea(linea))
    return libros


def cargar_socios():
    socios = []
    with open(RUTA_SOCIOS, "r", encoding="utf-8") as fichero:
        for linea in fichero:
            if linea.strip():
                socios.append(Socio.desde_linea(linea))
    return socios


def guardar_datos(libros, socios):
    with open(RUTA_LIBROS, "w", encoding="utf-8") as fichero:
        for libro in libros:
            fichero.write(libro.a_linea() + "\n")
    with open(RUTA_SOCIOS, "w", encoding="utf-8") as fichero:
        for socio in socios:
            fichero.write(socio.a_linea() + "\n")


def buscar_libro(libros, codigo):
    for libro in libros:
        if libro.codigo.upper() == codigo.upper():
            return libro
    return None


def buscar_socio(socios, codigo):
    for socio in socios:
        if socio.codigo.upper() == codigo.upper():
            return socio
    return None


def mostrar_cabecera_libros():
    print(f"{'COD':<6} {'TÍTULO':<38} {'AUTOR':<24} {'AÑO':<5} ESTADO")
    print("-" * 90)


def mostrar_libros(libros):
    if not libros:
        print("No hay libros que mostrar.")
        return
    mostrar_cabecera_libros()
    for libro in libros:
        print(libro)
    print(f"\nTotal: {len(libros)} libros")


def listar_todos(libros):
    mostrar_libros(libros)


def listar_disponibles(libros):
    mostrar_libros([libro for libro in libros if libro.esta_disponible()])


def buscar_por_titulo(libros):
    termino = input("Término a buscar en el título: ")
    if not termino.strip():
        print("Debes escribir algún término.")
        return
    encontrados = [libro for libro in libros if libro.coincide_titulo(termino)]
    if encontrados:
        mostrar_libros(encontrados)
    else:
        print("No existe ningún libro con ese término en el título.")


def prestar_libro(libros, socios):
    codigo_libro = input("Código del libro: ").strip()
    codigo_socio = input("Código del socio: ").strip()
    try:
        libro = buscar_libro(libros, codigo_libro)
        socio = buscar_socio(socios, codigo_socio)
        if libro is None:
            raise ErrorBiblioteca("El libro no existe", codigo_libro)
        if socio is None:
            raise ErrorBiblioteca("El socio no existe", codigo_socio)
        if not libro.esta_disponible():
            raise ErrorBiblioteca(f"El libro ya lo tiene el socio {libro.codigo_socio}", libro.codigo)
        if socio.tiene_libro():
            raise ErrorBiblioteca(f"El socio ya tiene el libro {socio.codigo_libro}", socio.codigo)
        libro.prestar(socio.codigo)
        socio.recibir_libro(libro.codigo)
        print(f"Préstamo realizado: '{libro.titulo}' para {socio.nombre}.")
        registrar_log("PRESTAMO", f"Libro {libro.codigo} prestado al socio {socio.codigo}")
    except ErrorBiblioteca as error:
        print(f"Error: {error.mensaje} (código: {error.codigo})")
        registrar_log("ERROR_PRESTAMO", f"{error.mensaje} - código {error.codigo}")


def devolver_libro(libros, socios):
    codigo_socio = input("Código del socio: ").strip()
    try:
        socio = buscar_socio(socios, codigo_socio)
        if socio is None:
            raise ErrorBiblioteca("El socio no existe", codigo_socio)
        if not socio.tiene_libro():
            raise ErrorBiblioteca("El socio no tiene ningún libro prestado", socio.codigo)
        codigo_libro = socio.devolver_libro()
        libro = buscar_libro(libros, codigo_libro)
        if libro is not None:
            libro.devolver()
        print(f"Libro {codigo_libro} devuelto por {socio.nombre}.")
        registrar_log("DEVOLUCION", f"Libro {codigo_libro} devuelto por el socio {socio.codigo}")
    except ErrorBiblioteca as error:
        print(f"Error: {error.mensaje} (código: {error.codigo})")
        registrar_log("ERROR_DEVOLUCION", f"{error.mensaje} - código {error.codigo}")


def mostrar_socios_con_libro(libros, socios):
    con_libro = [socio for socio in socios if socio.tiene_libro()]
    if not con_libro:
        print("Ningún socio tiene libros prestados.")
        return
    print(f"{'COD':<6} {'SOCIO':<25} LIBRO")
    print("-" * 70)
    for socio in con_libro:
        libro = buscar_libro(libros, socio.codigo_libro)
        titulo = libro.titulo if libro else "(libro desconocido)"
        print(f"{socio.codigo:<6} {socio.nombre:<25} {socio.codigo_libro} - {titulo}")


def anadir_socio(socios):
    codigo = input("Código del nuevo socio: ").strip()
    nombre = input("Nombre: ").strip()
    email = input("Email: ").strip()
    try:
        if not codigo or not nombre or not email:
            raise ErrorBiblioteca("Todos los campos son obligatorios", codigo)
        if buscar_socio(socios, codigo) is not None:
            raise ErrorBiblioteca("Ya existe un socio con ese código", codigo)
        socios.append(Socio(codigo, nombre, email))
        print(f"Socio {nombre} añadido.")
        registrar_log("ALTA_SOCIO", f"Socio {codigo} - {nombre}")
    except ErrorBiblioteca as error:
        print(f"Error: {error.mensaje} (código: {error.codigo})")


def anadir_libro(libros):
    codigo = input("Código del nuevo libro: ").strip()
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    anio = input("Año: ").strip()
    categoria = input("Categoría: ").strip()
    try:
        if not codigo or not titulo or not autor or not categoria:
            raise ErrorBiblioteca("Todos los campos son obligatorios", codigo)
        if buscar_libro(libros, codigo) is not None:
            raise ErrorBiblioteca("Ya existe un libro con ese código", codigo)
        if not anio.isdigit():
            raise ErrorBiblioteca("El año debe ser un número", codigo)
        libros.append(Libro(codigo, titulo, autor, anio, categoria))
        print(f"Libro '{titulo}' añadido.")
        registrar_log("ALTA_LIBRO", f"Libro {codigo} - {titulo}")
    except ErrorBiblioteca as error:
        print(f"Error: {error.mensaje} (código: {error.codigo})")


def anadir_elemento(libros, socios):
    tipo = input("¿Qué quieres añadir? (1 = socio, 2 = libro): ").strip()
    if tipo == "1":
        anadir_socio(socios)
    elif tipo == "2":
        anadir_libro(libros)
    else:
        print("Opción no válida.")


def mostrar_menu():
    print("\n===== BIBLIOTECA =====")
    print("1. Mostrar todos los libros")
    print("2. Mostrar libros disponibles")
    print("3. Buscar libro por título")
    print("4. Prestar un libro")
    print("5. Devolver un libro")
    print("6. Mostrar socios con libro")
    print("7. Añadir socio o libro")
    print("8. Salir\n")


def main():
    libros = cargar_libros()
    socios = cargar_socios()
    print(f"Información cargada: {len(libros)} libros y {len(socios)} socios.")
    registrar_log("INICIO", f"Cargados {len(libros)} libros y {len(socios)} socios")

    opcion = ""
    while opcion != "8":
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()
        print()
        if opcion == "1":
            listar_todos(libros)
        elif opcion == "2":
            listar_disponibles(libros)
        elif opcion == "3":
            buscar_por_titulo(libros)
        elif opcion == "4":
            prestar_libro(libros, socios)
        elif opcion == "5":
            devolver_libro(libros, socios)
        elif opcion == "6":
            mostrar_socios_con_libro(libros, socios)
        elif opcion == "7":
            anadir_elemento(libros, socios)
        elif opcion == "8":
            guardar_datos(libros, socios)
            registrar_log("FIN", "Datos guardados en los ficheros")
            print("Datos guardados. ¡Hasta pronto!")
        else:
            print("Opción no válida, elige un número del 1 al 8.")


if __name__ == "__main__":
    main()