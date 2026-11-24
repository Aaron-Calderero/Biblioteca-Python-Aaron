# gestiona la vista del menu junto a sus acciones

from errores.errores import ErrorBiblioteca


class Menu:
    def __init__(self, controlador):
        self.controlador = controlador

    # ---------- Bucle principal ----------
    def ejecutar(self):
        print(f"Información cargada: {len(self.controlador.obtener_libros())} libros "
              f"y {len(self.controlador.obtener_socios())} socios.")
        opcion = ""
        while opcion != "8":
            self.mostrar_menu()
            opcion = input("Elige una opción: ").strip()
            print()
            if opcion == "1":
                self.mostrar_libros(self.controlador.obtener_libros())
            elif opcion == "2":
                self.mostrar_libros(self.controlador.libros_disponibles())
            elif opcion == "3":
                self.buscar_por_titulo()
            elif opcion == "4":
                self.prestar_libro()
            elif opcion == "5":
                self.devolver_libro()
            elif opcion == "6":
                self.mostrar_socios_con_libro()
            elif opcion == "7":
                self.anadir_elemento()
            elif opcion == "8":
                opcion = self.salir(opcion)
            else:
                print("Opción no válida, elige un número del 1 al 8.")

    # ---------- Mostrar menu ----------
    def mostrar_menu(self):
        print("\n===== BIBLIOTECA =====")
        print("1. Mostrar todos los libros")
        print("2. Mostrar libros disponibles")
        print("3. Buscar libro por título")
        print("4. Prestar un libro")
        print("5. Devolver un libro")
        print("6. Mostrar socios con libro")
        print("7. Añadir socio o libro")
        print("8. Salir\n")

    # ---------- Mostrar mensaje de error ----------
    def mostrar_error(self, error):
        print(f"Error: {error}")

    # ---------- Mostrar libros ----------
    def mostrar_libros(self, libros):
        if not libros:
            print("No hay libros que mostrar.")
            return
        print(f"{'COD':<6} {'TÍTULO':<38} {'AUTOR':<24} {'AÑO':<5} ESTADO")
        print("-" * 90)
        for libro in libros:
            print(libro)
        print(f"\nTotal: {len(libros)} libros")

    def buscar_por_titulo(self):
        termino = input("Término a buscar en el título: ")
        if not termino.strip():
            print("Debes escribir algún término.")
            return
        encontrados = self.controlador.buscar_por_titulo(termino)
        if encontrados:
            self.mostrar_libros(encontrados)
        else:
            print("No existe ningún libro con ese término en el título.")

    # ---------- Préstamos ----------
    def prestar_libro(self):
        codigo_libro = input("Código del libro: ").strip()
        codigo_socio = input("Código del socio: ").strip()
        try:
            libro, socio = self.controlador.prestar_libro(codigo_libro, codigo_socio)
            print(f"Préstamo realizado: '{libro.titulo}' para {socio.nombre}.")
        except ErrorBiblioteca as error:
            self.mostrar_error(error)

    def devolver_libro(self):
        codigo_socio = input("Código del socio: ").strip()
        try:
            codigo_libro, socio = self.controlador.devolver_libro(codigo_socio)
            print(f"Libro {codigo_libro} devuelto por {socio.nombre}.")
        except ErrorBiblioteca as error:
            self.mostrar_error(error)

    def mostrar_socios_con_libro(self):
        lista = self.controlador.socios_con_libro()
        if not lista:
            print("Ningún socio tiene libros prestados.")
            return
        print(f"{'COD':<6} {'SOCIO':<25} LIBRO")
        print("-" * 70)
        for socio, titulo in lista:
            print(f"{socio.codigo:<6} {socio.nombre:<25} {socio.codigo_libro} - {titulo}")

    # ---------- Añadir socio o libro ----------
    def anadir_elemento(self):
        tipo = input("¿Qué quieres añadir? (1 = socio, 2 = libro): ").strip()
        if tipo == "1":
            self.anadir_socio()
        elif tipo == "2":
            self.anadir_libro()
        else:
            print("Opción no válida.")

    def anadir_socio(self):
        codigo = input("Código del nuevo socio: ").strip()
        nombre = input("Nombre: ").strip()
        email = input("Email: ").strip()
        try:
            self.controlador.anadir_socio(codigo, nombre, email)
            print(f"Socio {nombre} añadido.")
        except ErrorBiblioteca as error:
            self.mostrar_error(error)

    def anadir_libro(self):
        codigo = input("Código del nuevo libro: ").strip()
        titulo = input("Título: ").strip()
        autor = input("Autor: ").strip()
        anio = input("Año: ").strip()
        categoria = input("Categoría: ").strip()
        try:
            self.controlador.anadir_libro(codigo, titulo, autor, anio, categoria)
            print(f"Libro '{titulo}' añadido.")
        except ErrorBiblioteca as error:
            self.mostrar_error(error)

    # ---------- Salir ----------
    def salir(self, opcion):
        try:
            self.controlador.guardar_datos()
            print("Datos guardados. ¡Hasta pronto!")
            return opcion
        except ErrorBiblioteca as error:
            self.mostrar_error(error)
            return ""
