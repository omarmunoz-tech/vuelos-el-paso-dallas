# app.py: la pantalla de la app.
# Los resultados vienen de logica.py; las tarjetas y gráficas de esta app están en diseno.py.

import streamlit as st

# Ejecutar este archivo en Thonny (F5) abre la app en el navegador
if not st.runtime.exists():
    import sys
    from streamlit.web import cli
    sys.argv = ["streamlit", "run", __file__, "--server.runOnSave", "true", "--server.showEmailPrompt", "false"]
    sys.exit(cli.main())

import os
import logica
import diseno

# Carpeta de la app, para encontrar las imágenes
CARPETA = os.path.dirname(__file__)

st.set_page_config(page_title="Vuelos de El Paso a Dallas", page_icon="✈️", layout="wide")
diseno.estilos()

# Las respuestas se calculan una vez y se usan en varias páginas
aerolinea = logica.aerolinea_recomendada(logica.vuelos_dallas)
porcentaje_aerolinea = logica.porcentaje_de_aerolinea(logica.vuelos_dallas, aerolinea)
turno = logica.turno_recomendado(logica.vuelos_dallas)
manana = logica.porcentaje_de_manana(logica.vuelos_dallas)
tarde = logica.porcentaje_de_tarde(logica.vuelos_dallas)
margen = logica.margen_recomendado(logica.vuelos_que_llegaron)


def inicio():
    st.image(os.path.join(CARPETA, "portada.png"), width="stretch")
    st.title("Vuelos de El Paso a Dallas")
    st.markdown("*Qué vuelo reservar para llegar a tiempo a una junta en Dallas.*")
    st.divider()

    columna_1, columna_2, columna_3 = st.columns(3, gap="large")
    with columna_1:
        st.caption("AEROLÍNEA")
        st.markdown(f"## :primary[{aerolinea}]")
        st.write(f"{porcentaje_aerolinea}% de sus vuelos de El Paso a Dallas llegan a tiempo.")
        st.page_link(pagina_1, label="Ver la comparación", icon=":material/arrow_forward:")
    with columna_2:
        st.caption("HORARIO")
        st.markdown(f"## :primary[{turno.capitalize()}]")
        st.write(f"{manana}% de los vuelos que salen antes de las 12:00 llegan a tiempo.")
        st.page_link(pagina_2, label="Ver la comparación", icon=":material/arrow_forward:")
    with columna_3:
        st.caption("MARGEN")
        st.markdown(f"## :primary[{margen} min]")
        st.write(f"Dejando {margen} minutos entre la llegada del vuelo y la junta, llega a tiempo en 9 de cada 10 vuelos.")
        st.page_link(pagina_3, label="Ver el cálculo", icon=":material/arrow_forward:")

    st.divider()
    st.caption(f"Se analizaron los {len(logica.vuelos_dallas):,} vuelos que salieron de El Paso (ELP) a Dallas Love Field (DAL) "
               "y Dallas/Fort Worth (DFW) entre septiembre de 2025 y agosto de 2026. Datos: Bureau of Transportation Statistics.")


def pregunta_1():
    diseno.encabezado("Pregunta 1 · Aerolínea", "¿Con qué aerolínea es más probable llegar a tiempo?",
                      aerolinea, f"{porcentaje_aerolinea}% de sus vuelos de El Paso a Dallas llegan a tiempo, el porcentaje más alto de las tres aerolíneas.")

    nombres = ["American", "Southwest", "Frontier"]
    porcentajes = []
    for nombre in nombres:
        porcentajes.append(logica.porcentaje_de_aerolinea(logica.vuelos_dallas, nombre))
    diseno.grafica_de_barras("Porcentaje de vuelos de ELP a Dallas que llegan a tiempo, por aerolínea", nombres, porcentajes, aerolinea)

    diseno.como_se_calculo([
        ["Separar los vuelos a Dallas", f"De los {len(logica.filas):,} vuelos del archivo se toman los {len(logica.vuelos_dallas):,} que salen de El Paso a Dallas (DAL o DFW)."],
        ["Decidir qué es llegar a tiempo", "Un vuelo llegó a tiempo si su retraso fue de menos de 15 minutos. Si se canceló o se desvió, no llegó a tiempo."],
        ["Sacar el porcentaje de cada aerolínea", "Para cada aerolínea se cuentan sus vuelos y cuántos llegaron a tiempo."],
        ["Elegir la aerolínea", "Se recomienda la aerolínea con el porcentaje más alto."],
    ])


def pregunta_2():
    diseno.encabezado("Pregunta 2 · Horario", "¿Conviene más volar en la mañana o en la tarde?",
                      turno.capitalize(), f"{manana}% de los vuelos de la mañana llegan a tiempo, contra {tarde}% de los de la tarde.")

    if turno == "mañana":
        destacado = "Mañana"
    else:
        destacado = "Tarde"
    diseno.grafica_de_barras("Porcentaje de vuelos de ELP a Dallas que llegan a tiempo, por horario de salida", ["Mañana", "Tarde"], [manana, tarde], destacado)

    diseno.como_se_calculo([
        ["Separar por horario", f"Los {len(logica.vuelos_dallas):,} vuelos a Dallas se dividen en los que salen antes de las 12:00 (mañana) y los que salen a las 12:00 o después (tarde)."],
        ["Sacar el porcentaje de cada horario", "En cada grupo se cuenta cuántos vuelos llegaron a tiempo, con la misma regla de la pregunta 1."],
        ["Elegir el horario", "Se recomienda el horario con el porcentaje más alto."],
    ])


def pregunta_3():
    diseno.encabezado("Pregunta 3 · Margen", "¿Cuánto tiempo dejar entre la llegada del vuelo y la junta?",
                      f"{margen} min", f"Si deja {margen} minutos entre la hora de llegada del vuelo y la junta, llega a tiempo en 9 de cada 10 vuelos.")

    margenes = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    porcentajes = logica.porcentajes_por_margen(logica.vuelos_que_llegaron, margenes)
    diseno.grafica_de_linea("Porcentaje de vuelos de ELP a Dallas con los que llega a tiempo a la junta, según el margen",
                            margenes, porcentajes, margen, f"{margen} min", "Margen (minutos)", 90,
                            "La línea punteada marca 9 de cada 10 vuelos.")

    diseno.como_se_calculo([
        ["Quitar los vuelos que no llegaron", f"De los {len(logica.vuelos_dallas):,} vuelos a Dallas se dejan fuera los cancelados y los desviados: quedan {len(logica.vuelos_que_llegaron):,}."],
        ["Decidir cuándo llega a tiempo a la junta", "Con un margen dado, llega a tiempo si el retraso del vuelo es igual o menor que ese margen."],
        ["Probar márgenes", "Se prueban márgenes de 5 en 5 minutos, empezando en 0, y para cada uno se saca el porcentaje de vuelos con los que llegaría a tiempo."],
        ["Elegir el margen", "El margen recomendado es el primero con el que llega a tiempo en al menos 9 de cada 10 vuelos."],
    ])


pagina_inicio = st.Page(inicio, title="Inicio", icon=":material/home:", default=True)
pagina_1 = st.Page(pregunta_1, title="Aerolínea", icon=":material/flight:")
pagina_2 = st.Page(pregunta_2, title="Horario", icon=":material/schedule:")
pagina_3 = st.Page(pregunta_3, title="Margen", icon=":material/timer:")
pagina = st.navigation([pagina_inicio, pagina_1, pagina_2, pagina_3])

st.logo(os.path.join(CARPETA, "logo.png"), size="large")
with st.sidebar:
    diseno.persona(
        "Mariana",
        "Ingeniera de procesos",
        "Trabaja en una maquiladora de Juárez y vuela seguido de El Paso a Dallas para juntas en el corporativo. Si el vuelo llega tarde, se pierde la junta.",
        "Qué vuelo reservar para llegar a tiempo a la junta.",
    )

pagina.run()
