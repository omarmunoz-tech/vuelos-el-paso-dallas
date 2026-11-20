# logica.py: el análisis de la app.
# Solo ciclos, condicionales, listas y funciones.
# Las tres preguntas siguen los mismos pasos: sacar un porcentaje para cada opción
# con una función, guardar los porcentajes en una lista para la gráfica y elegir
# la opción que conviene.

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


def porcentaje_que_no_llego(vuelos):
    # Porcentaje de vuelos que no llegaron a Dallas: se cancelaron o se desviaron.
    # Ejemplo: porcentaje_que_no_llego(vuelos_dallas) regresa 2.4
    no_llego = 0
    for vuelo in vuelos:
        if vuelo["cancelado"] == "Sí" or vuelo["desviado"] == "Sí":
            no_llego = no_llego + 1
    return round(no_llego / len(vuelos) * 100, 1)


# Pregunta 1: ¿con qué aerolínea es más probable llegar a tiempo a Dallas?
# Frontier se deja fuera: solo tiene 39 vuelos a Dallas, muy pocos para
# compararla con American (2554) y Southwest (1763).

def vuelos_de_aerolinea(vuelos, aerolinea):
    # Los vuelos de una aerolínea.
    # Ejemplo: len(vuelos_de_aerolinea(vuelos_dallas, "Frontier")) regresa 39
    vuelos_de_la_aerolinea = []
    for vuelo in vuelos:
        if vuelo["aerolinea"] == aerolinea:
            vuelos_de_la_aerolinea.append(vuelo)
    return vuelos_de_la_aerolinea


def porcentaje_de_aerolinea(vuelos, aerolinea):
    # Porcentaje a tiempo de los vuelos de una aerolínea.
    # Ejemplos: porcentaje_de_aerolinea(vuelos_dallas, "Southwest") regresa 79.1
    #           porcentaje_de_aerolinea(vuelos_dallas, "American") regresa 76.3
    return porcentaje_a_tiempo(vuelos_de_aerolinea(vuelos, aerolinea))


def aerolinea_recomendada(vuelos, aerolineas):
    # La aerolínea con el porcentaje a tiempo más alto.
    # American 76.3, Southwest 79.1: se queda con Southwest.
    mejor = ""
    mayor = 0
    for aerolinea in aerolineas:
        porcentaje = porcentaje_de_aerolinea(vuelos, aerolinea)
        if porcentaje > mayor:
            mayor = porcentaje
            mejor = aerolinea
    return mejor


aerolineas = ["American", "Southwest"]

porcentajes_aerolineas = []
for aerolinea in aerolineas:
    porcentajes_aerolineas.append(porcentaje_de_aerolinea(vuelos_dallas, aerolinea))


# Pregunta 2: ¿conviene más volar en la mañana o en la tarde?
# Las horas vienen como texto con dos dígitos ("09:30"),
# así que comparar el texto da el mismo orden que comparar la hora.

def porcentaje_de_horario(vuelos, horario):
    # Porcentaje a tiempo de los vuelos de un horario:
    # "Mañana" si salen antes de las 12:00, "Tarde" si salen a las 12:00 o después.
    # Ejemplos: porcentaje_de_horario(vuelos_dallas, "Mañana") regresa 85.2
    #           porcentaje_de_horario(vuelos_dallas, "Tarde") regresa 68.6
    vuelos_del_horario = []
    for vuelo in vuelos:
        if vuelo["hora_salida_programada"] < "12:00":
            horario_del_vuelo = "Mañana"
        else:
            horario_del_vuelo = "Tarde"
        if horario_del_vuelo == horario:
            vuelos_del_horario.append(vuelo)
    return porcentaje_a_tiempo(vuelos_del_horario)


def horario_recomendado(vuelos, horarios):
    # El horario con el porcentaje a tiempo más alto.
    # Mañana 85.2, Tarde 68.6: se queda con Mañana.
    mejor = ""
    mayor = 0
    for horario in horarios:
        porcentaje = porcentaje_de_horario(vuelos, horario)
        if porcentaje > mayor:
            mayor = porcentaje
            mejor = horario
    return mejor


horarios = ["Mañana", "Tarde"]

porcentajes_horarios = []
for horario in horarios:
    porcentajes_horarios.append(porcentaje_de_horario(vuelos_dallas, horario))


# Pregunta 3: ¿con cuánta anticipación debe llegar el vuelo?
# El margen es el tiempo, en minutos, entre la hora programada de llegada del vuelo
# y la hora a la que necesita salir del aeropuerto hacia la junta.
# El margen sirve para los retrasos, no para las cancelaciones: se calcula con los
# vuelos que sí llegaron. De los 4356 vuelos a Dallas, quedan 4253.

vuelos_que_llegaron = []
for vuelo in vuelos_dallas:
    if vuelo["cancelado"] == "No" and vuelo["desviado"] == "No":
        vuelos_que_llegaron.append(vuelo)


def porcentaje_dentro_del_margen(vuelos, margen):
    # Porcentaje de vuelos que llegaron con un retraso igual o menor que el margen.
    # Ejemplos: porcentaje_dentro_del_margen(vuelos_que_llegaron, 30) regresa 86.3
    #           porcentaje_dentro_del_margen(vuelos_que_llegaron, 60) regresa 92.4
    dentro = 0
    for vuelo in vuelos:
        if vuelo["retraso_llegada_min"] <= margen:
            dentro = dentro + 1
    return round(dentro / len(vuelos) * 100, 1)


def margen_recomendado(vuelos, margenes):
    # El margen más corto con el que al menos 9 de cada 10 vuelos llegan dentro del margen.
    # Los márgenes van de menor a mayor, así que es el primero que llega a 90.
    # 30 minutos: 86.3, 60 minutos: 92.4: se queda con 60.
    recomendado = 0
    for margen in margenes:
        if recomendado == 0 and porcentaje_dentro_del_margen(vuelos, margen) >= 90:
            recomendado = margen
    return recomendado


margenes = [30, 60, 90, 120]

porcentajes_margenes = []
for margen in margenes:
    porcentajes_margenes.append(porcentaje_dentro_del_margen(vuelos_que_llegaron, margen))
