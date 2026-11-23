# datos.py: lee un archivo CSV de la carpeta de la app.
# cargar(nombre) regresa una lista con una fila por renglón del archivo.
# Cada fila es un diccionario: fila["nombre_de_columna"] da el valor de esa columna.
# Las columnas con puros números llegan como números; las celdas vacías llegan como None.
# Este archivo no se modifica.

import os


def tipo_de_columna(valores):
    tipo = "entero"
    for valor in valores:
        if valor == "":
            continue
        try:
            int(valor)
        except ValueError:
            try:
                float(valor)
                tipo = "decimal"
            except ValueError:
                return "texto"
    return tipo


def convertir(valor, tipo):
    if valor == "":
        return None
    if tipo == "entero":
        return int(valor)
    if tipo == "decimal":
        return float(valor)
    return valor


def cargar(nombre):
    if nombre == "":
        raise ValueError("Falta el nombre del archivo: en logica.py, ARCHIVO debe tener el nombre del CSV de la base de datos que te fue asignada.")
    # El archivo está en la misma carpeta que datos.py
    ruta = os.path.join(os.path.dirname(__file__), nombre)
    if not os.path.isfile(ruta):
        raise FileNotFoundError("No hay un archivo llamado " + nombre + " en la carpeta de la app.")
    archivo = open(ruta, encoding="utf-8")
    columnas = archivo.readline().strip().split(",")
    renglones = []
    for linea in archivo:
        renglones.append(linea.strip().split(","))
    archivo.close()

    tipos = []
    for i in range(len(columnas)):
        valores = []
        for renglon in renglones:
            valores.append(renglon[i])
        tipos.append(tipo_de_columna(valores))

    filas = []
    for renglon in renglones:
        fila = {}
        for i in range(len(columnas)):
            fila[columnas[i]] = convertir(renglon[i], tipos[i])
        filas.append(fila)
    return filas
