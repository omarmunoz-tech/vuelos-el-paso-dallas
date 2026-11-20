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
aerolinea = logica.aerolinea_recomendada(logica.vuelos_dallas, logica.aerolineas)
porcentaje_aerolinea = logica.porcentaje_de_aerolinea(logica.vuelos_dallas, aerolinea)
horario = logica.horario_recomendado(logica.vuelos_dallas, logica.horarios)
manana = logica.porcentaje_de_horario(logica.vuelos_dallas, "Mañana")
tarde = logica.porcentaje_de_horario(logica.vuelos_dallas, "Tarde")
margen = logica.margen_recomendado(logica.vuelos_que_llegaron, logica.margenes)
no_llegan = logica.porcentaje_que_no_llego(logica.vuelos_dallas)

# Cómo se escribe en la app cada margen de logica.margenes (en minutos)
nombres_de_margen = {30: "30 minutos", 60: "1 hora", 90: "1 hora y media", 120: "2 horas"}


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
        st.markdown(f"## :primary[{horario}]")
        st.write(f"{manana}% de los vuelos que salen antes de las 12:00 llegan a tiempo.")
        st.page_link(pagina_2, label="Ver la comparación", icon=":material/arrow_forward:")
    with columna_3:
        st.caption("MARGEN")
        st.markdown(f"## :primary[{nombres_de_margen[margen]}]")
        st.write(f"{nombres_de_margen[margen].capitalize()} de margen cubre el retraso de 9 de cada 10 vuelos que llegan.")
        st.page_link(pagina_3, label="Ver la comparación", icon=":material/arrow_forward:")

    st.divider()
    st.caption(f"Se analizaron los {len(logica.vuelos_dallas):,} vuelos que salieron de El Paso (ELP) a Dallas Love Field (DAL) "
               "y Dallas/Fort Worth (DFW) entre septiembre de 2025 y agosto de 2026. Datos: Bureau of Transportation Statistics.")


def pregunta_1():
    vuelos_american = logica.vuelos_de_aerolinea(logica.vuelos_dallas, "American")
    vuelos_southwest = logica.vuelos_de_aerolinea(logica.vuelos_dallas, "Southwest")
    vuelos_frontier = logica.vuelos_de_aerolinea(logica.vuelos_dallas, "Frontier")
    no_llegan_aerolinea = logica.porcentaje_que_no_llego(logica.vuelos_de_aerolinea(logica.vuelos_dallas, aerolinea))
    no_llegan_american = logica.porcentaje_que_no_llego(vuelos_american)

    diseno.encabezado("Pregunta 1 · Aerolínea", "¿Con qué aerolínea es más probable llegar a tiempo?",
                      aerolinea, f"Llega a tiempo en {porcentaje_aerolinea}% de sus vuelos de El Paso a Dallas, contra "
                      f"{logica.porcentaje_de_aerolinea(logica.vuelos_dallas, 'American')}% de American, y cancela o desvía menos vuelos: "
                      f"{no_llegan_aerolinea}% contra {no_llegan_american}%.")

    diseno.grafica_de_barras("Porcentaje de vuelos de ELP a Dallas que llegan a tiempo, por aerolínea",
                             logica.aerolineas, logica.porcentajes_aerolineas, aerolinea)

    diseno.como_se_calculo([
        ["Separar los vuelos a Dallas", f"De los {len(logica.filas):,} vuelos del archivo se toman los {len(logica.vuelos_dallas):,} que salen de El Paso a Dallas (DAL o DFW)."],
        ["Dejar fuera a Frontier", f"Frontier solo tiene {len(vuelos_frontier)} vuelos a Dallas, muy pocos para compararla con American ({len(vuelos_american):,}) y Southwest ({len(vuelos_southwest):,})."],
        ["Decidir qué es llegar a tiempo", "Un vuelo llegó a tiempo si su retraso fue de menos de 15 minutos. Si se canceló o se desvió, no llegó a tiempo."],
        ["Sacar los porcentajes de cada aerolínea", "Para cada aerolínea se cuentan sus vuelos, cuántos llegaron a tiempo y cuántos se cancelaron o se desviaron."],
        ["Elegir la aerolínea", "Se recomienda la aerolínea con el porcentaje a tiempo más alto."],
    ])


def pregunta_2():
    diseno.encabezado("Pregunta 2 · Horario", "¿Conviene más volar en la mañana o en la tarde?",
                      horario, f"{manana}% de los vuelos de la mañana llegan a tiempo, contra {tarde}% de los de la tarde.")

    diseno.grafica_de_barras("Porcentaje de vuelos de ELP a Dallas que llegan a tiempo, por horario de salida",
                             logica.horarios, logica.porcentajes_horarios, horario)

    diseno.como_se_calculo([
        ["Separar por horario", f"Los {len(logica.vuelos_dallas):,} vuelos a Dallas se dividen en los que salen antes de las 12:00 (mañana) y los que salen a las 12:00 o después (tarde)."],
        ["Sacar el porcentaje de cada horario", "En cada grupo se cuenta cuántos vuelos llegaron a tiempo, con la misma regla de la pregunta 1."],
        ["Elegir el horario", "Se recomienda el horario con el porcentaje más alto."],
    ])


def pregunta_3():
    diseno.encabezado("Pregunta 3 · Margen", "¿Con cuánta anticipación debe llegar el vuelo?",
                      nombres_de_margen[margen],
                      f"Con un vuelo programado para aterrizar {nombres_de_margen[margen]} antes de cuando necesita salir del aeropuerto "
                      "hacia la junta, llega a tiempo en 9 de cada 10 vuelos que no se cancelan ni se desvían. "
                      f"El margen no cubre las cancelaciones ni los desvíos: le pasan al {no_llegan}% de los vuelos.")

    nombres = []
    for opcion in logica.margenes:
        nombres.append(nombres_de_margen[opcion])
    diseno.grafica_de_barras("Porcentaje de vuelos de ELP a Dallas que llegan dentro del margen, sin contar cancelados ni desviados",
                             nombres, logica.porcentajes_margenes, nombres_de_margen[margen], en_orden_de_la_lista=True)

    diseno.como_se_calculo([
        ["Quitar los vuelos que no llegaron", f"De los {len(logica.vuelos_dallas):,} vuelos a Dallas se dejan fuera los cancelados y los desviados ({no_llegan}%), porque para ellos no sirve ningún margen: quedan {len(logica.vuelos_que_llegaron):,}."],
        ["Definir el margen", "Es el tiempo entre la hora programada de llegada del vuelo y la hora a la que tiene que salir del aeropuerto hacia la junta. El trayecto del aeropuerto a la junta va aparte."],
        ["Sacar el porcentaje de cada margen", "Para 30 minutos, 1 hora, 1 hora y media y 2 horas se cuenta cuántos de esos vuelos llegaron con un retraso igual o menor que el margen."],
        ["Elegir el margen", "Se recomienda el margen más corto con el que al menos 9 de cada 10 de esos vuelos llegan dentro del margen."],
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
