# logica.py: el análisis de la app.
# Solo ciclos, condicionales, listas y funciones.

from datos import cargar

# Nombre del archivo de la base de datos
ARCHIVO = "vuelos_el_paso.csv"

filas = cargar(ARCHIVO)


# Los vuelos que salen de El Paso a cualquiera de los dos aeropuertos de Dallas.
# De los 32739 vuelos del archivo, quedan 4356.

vuelos_dallas = []
for vuelo in filas:
    if vuelo["tipo"] == "Salida":
        if vuelo["destino"] == "Dallas (DAL)" or vuelo["destino"] == "Dallas/Fort Worth (DFW)":
            vuelos_dallas.append(vuelo)


def porcentaje_a_tiempo(vuelos):
    # Porcentaje de vuelos que llegaron a tiempo: con menos de 15 minutos de retraso.
    # Un vuelo cancelado o desviado no llegó a tiempo.
    # Ejemplo: porcentaje_a_tiempo(vuelos_dallas) regresa 77.4
    a_tiempo = 0
    for vuelo in vuelos:
        if vuelo["cancelado"] == "No" and vuelo["desviado"] == "No":
            if vuelo["retraso_llegada_min"] < 15:
                a_tiempo = a_tiempo + 1
    return round(a_tiempo / len(vuelos) * 100, 1)


# Pregunta 1: ¿con qué aerolínea es más probable llegar a tiempo a Dallas?

def porcentaje_de_aerolinea(vuelos, aerolinea):
    # Porcentaje a tiempo de los vuelos de una aerolínea.
    # Ejemplos: porcentaje_de_aerolinea(vuelos_dallas, "Southwest") regresa 79.1
    #           porcentaje_de_aerolinea(vuelos_dallas, "American") regresa 76.3
    vuelos_de_aerolinea = []
    for vuelo in vuelos:
        if vuelo["aerolinea"] == aerolinea:
            vuelos_de_aerolinea.append(vuelo)
    return porcentaje_a_tiempo(vuelos_de_aerolinea)


def aerolinea_recomendada(vuelos):
    # La aerolínea con el porcentaje a tiempo más alto.
    # American 76.3, Southwest 79.1, Frontier 69.2: se queda con Southwest.
    # Ejemplo: aerolinea_recomendada(vuelos_dallas) regresa "Southwest"
    mejor = ""
    mayor = 0
    for aerolinea in ["American", "Southwest", "Frontier"]:
        porcentaje = porcentaje_de_aerolinea(vuelos, aerolinea)
        if porcentaje > mayor:
            mayor = porcentaje
            mejor = aerolinea
    return mejor


# Pregunta 2: ¿conviene más volar en la mañana o en la tarde?
# Las horas vienen como texto con dos dígitos ("09:30"),
# así que comparar el texto da el mismo orden que comparar la hora.

def porcentaje_de_manana(vuelos):
    # Porcentaje a tiempo de los vuelos que salen antes de las 12:00.
    # Ejemplo: porcentaje_de_manana(vuelos_dallas) regresa 85.2
    vuelos_de_manana = []
    for vuelo in vuelos:
        if vuelo["hora_salida_programada"] < "12:00":
            vuelos_de_manana.append(vuelo)
    return porcentaje_a_tiempo(vuelos_de_manana)


def porcentaje_de_tarde(vuelos):
    # Porcentaje a tiempo de los vuelos que salen a las 12:00 o después.
    # Ejemplo: porcentaje_de_tarde(vuelos_dallas) regresa 68.6
    vuelos_de_tarde = []
    for vuelo in vuelos:
        if vuelo["hora_salida_programada"] >= "12:00":
            vuelos_de_tarde.append(vuelo)
    return porcentaje_a_tiempo(vuelos_de_tarde)


def turno_recomendado(vuelos):
    # El turno con el porcentaje a tiempo más alto.
    # Ejemplo: turno_recomendado(vuelos_dallas) regresa "mañana" (85.2 contra 68.6)
    turno = "tarde"
    if porcentaje_de_manana(vuelos) > porcentaje_de_tarde(vuelos):
        turno = "mañana"
    return turno


# Pregunta 3: ¿cuánto tiempo dejar entre la llegada del vuelo y la junta?

# Los vuelos a Dallas que sí llegaron: sin cancelados ni desviados.
# De los 4356 vuelos a Dallas, quedan 4253.

vuelos_que_llegaron = []
for vuelo in vuelos_dallas:
    if vuelo["cancelado"] == "No" and vuelo["desviado"] == "No":
        vuelos_que_llegaron.append(vuelo)


def porcentaje_dentro_del_margen(vuelos, margen):
    # Porcentaje de vuelos que llegaron con un retraso igual o menor que el margen.
    # Ejemplos: porcentaje_dentro_del_margen(vuelos_que_llegaron, 0) regresa 64.0 (llegaron sin retraso o antes)
    #           porcentaje_dentro_del_margen(vuelos_que_llegaron, 15) regresa 79.9
    dentro = 0
    for vuelo in vuelos:
        if vuelo["retraso_llegada_min"] <= margen:
            dentro = dentro + 1
    return round(dentro / len(vuelos) * 100, 1)


def porcentajes_por_margen(vuelos, margenes):
    # El porcentaje dentro del margen para cada margen de la lista.
    # Ejemplo: porcentajes_por_margen(vuelos_que_llegaron, [0, 15, 30]) regresa [64.0, 79.9, 86.3]
    porcentajes = []
    for margen in margenes:
        porcentajes.append(porcentaje_dentro_del_margen(vuelos, margen))
    return porcentajes


def margen_recomendado(vuelos):
    # Prueba márgenes de 5 en 5 minutos hasta que al menos el 90% de los vuelos llegue dentro del margen:
    # 0: 64.0%, 5: 71.0%, 10: 76.6%, 15: 79.9% ... 40: 88.8%, 45: 89.9%, 50: 90.8%
    # Ejemplo: margen_recomendado(vuelos_que_llegaron) regresa 50
    margen = 0
    while porcentaje_dentro_del_margen(vuelos, margen) < 90:
        margen = margen + 5
    return margen
