# diseno.py: piezas visuales de la app (tarjetas, pasos, gráficas).
# app.py las usa para mostrar los resultados; aquí no se calcula nada.

import html
import streamlit as st
import altair as alt

AZUL = "#38bdf8"        # color principal (el mismo que primaryColor en .streamlit/config.toml)
GRIS = "#2b3f63"        # barras que no se destacan
TEXTO = "#e6edf7"

ESTILOS = """
<style>
[data-testid="stMainBlockContainer"]{padding-left:3rem;padding-right:3rem;max-width:none}
[data-testid="stSidebarNavLink"]{min-height:44px;padding-top:6px;padding-bottom:6px}
[data-testid="stSidebarNavLink"] p{font-size:17px}
[data-testid="stSidebarNavLink"] [data-testid="stIconMaterial"]{font-size:21px}
.d-eyebrow{font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:#38bdf8;font-weight:600}
.d-persona{background:#13233f;border:1px solid #22395f;border-radius:16px;padding:18px}
.d-persona .d-para{display:block;font-size:11px;margin-bottom:14px;padding-bottom:12px;border-bottom:1px solid #22395f}
.d-persona .d-fila{display:flex;gap:12px;align-items:center}
.d-avatar{flex:none;width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#7dd3fc,#2563eb);
  display:flex;align-items:center;justify-content:center;font-family:'Sora',sans-serif;font-weight:700;color:#0b1628;font-size:17px}
.d-persona .d-nombre{font-weight:600;color:#fff;font-size:15px;line-height:1.2}
.d-persona .d-rol{font-size:13px;color:#9fb3cf;line-height:1.35;margin-top:2px}
.d-persona .d-contexto{font-size:14px;color:#cfdaea;margin:14px 0 12px;line-height:1.5}
.d-decision{border-left:3px solid #38bdf8;background:rgba(56,189,248,.09);padding:10px 12px;border-radius:0 10px 10px 0;font-size:14px;color:#e6edf7;line-height:1.45}
.d-decision .d-eyebrow{display:block;font-size:10.5px;margin-bottom:3px}
.d-pregunta{font-family:'Sora',sans-serif;font-size:38px;font-weight:700;color:#fff;line-height:1.18;margin:8px 0 24px}
.d-caja{border-radius:20px;padding:24px 28px 26px;
  background:linear-gradient(135deg,rgba(56,189,248,.22) 0%,rgba(56,189,248,.07) 55%,rgba(56,189,248,.03) 100%);
  border:1px solid rgba(56,189,248,.45)}
.d-caja .d-valor{font-family:'Sora',sans-serif;font-size:44px;font-weight:700;color:#38bdf8;line-height:1.05;margin:8px 0 10px}
.d-caja .d-texto{font-size:16.5px;color:#e6edf7;line-height:1.5;text-wrap:pretty}
.d-seccion{font-family:'Sora',sans-serif;font-size:19px;font-weight:600;color:#fff;line-height:1.3;margin:0 0 4px}
.d-pasos .d-seccion{margin-bottom:18px}
.d-paso{position:relative;display:flex;gap:16px;padding-bottom:20px}
.d-paso:not(:last-child)::before{content:"";position:absolute;left:15px;top:36px;bottom:2px;width:2px;background:#24426e}
.d-paso .d-num{flex:none;width:32px;height:32px;border-radius:50%;border:2px solid #38bdf8;background:#0b1628;color:#38bdf8;
  font-family:'Sora',sans-serif;font-weight:700;font-size:14px;display:flex;align-items:center;justify-content:center}
.d-paso .d-t{font-weight:600;color:#fff;font-size:15.5px;margin-top:5px}
.d-paso .d-d{color:#a9bad3;font-size:15px;line-height:1.5;margin-top:3px}
</style>
"""


def estilos():
    # Carga los estilos de las tarjetas. Se llama una vez, al principio de app.py.
    st.html(ESTILOS)


def persona(nombre, rol, contexto, decision):
    # La tarjeta de la persona para quien es la app.
    st.html(
        '<div class="d-persona">'
        '<div class="d-eyebrow d-para">Esta app es para</div>'
        '<div class="d-fila">'
        f'<div class="d-avatar">{html.escape(nombre[0])}</div>'
        f'<div><div class="d-nombre">{html.escape(nombre)}</div><div class="d-rol">{html.escape(rol)}</div></div>'
        '</div>'
        f'<div class="d-contexto">{html.escape(contexto)}</div>'
        f'<div class="d-decision"><span class="d-eyebrow">Su decisión</span>{html.escape(decision)}</div>'
        '</div>'
    )


def encabezado(etiqueta, pregunta, valor, texto):
    # Arriba de cada pregunta: la etiqueta, la pregunta y la caja con la respuesta.
    st.html(
        f'<div class="d-eyebrow">{html.escape(etiqueta)}</div>'
        f'<div class="d-pregunta">{html.escape(pregunta)}</div>'
        '<div class="d-caja">'
        '<div class="d-eyebrow">Respuesta</div>'
        f'<div class="d-valor">{html.escape(valor)}</div>'
        f'<div class="d-texto">{html.escape(texto)}</div>'
        '</div>'
    )
    st.space("small")


def como_se_calculo(pasos):
    # Los pasos del cálculo, numerados.
    # pasos es una lista de listas [título, explicación], una por paso.
    filas = ""
    for i in range(len(pasos)):
        filas = filas + (
            '<div class="d-paso">'
            f'<div class="d-num">{i + 1}</div>'
            f'<div><div class="d-t">{html.escape(pasos[i][0])}</div><div class="d-d">{html.escape(pasos[i][1])}</div></div>'
            '</div>'
        )
    st.html(f'<div class="d-pasos"><div class="d-seccion">Cómo se calculó</div>{filas}</div>')


def grafica_de_barras(titulo, nombres, valores, destacado):
    # Barras horizontales con el valor al lado; la barra de `destacado` va en azul y las demás en gris.
    datos = []
    for i in range(len(nombres)):
        datos.append({"nombre": nombres[i], "valor": valores[i], "etiqueta": f"{valores[i]}%", "destacado": nombres[i] == destacado})
    base = alt.Chart(alt.Data(values=datos)).encode(
        y=alt.Y("nombre:N", sort="-x", title=None, axis=alt.Axis(labelFontSize=15, labelColor=TEXTO, labelPadding=12, domain=False, ticks=False)),
        x=alt.X("valor:Q", title=None, axis=None, scale=alt.Scale(domain=[0, 100])),
    )
    barras = base.mark_bar(cornerRadiusEnd=6, height=26).encode(
        color=alt.condition("datum.destacado", alt.value(AZUL), alt.value(GRIS)),
    )
    etiquetas = base.mark_text(align="left", dx=10, fontSize=16, fontWeight="bold", color=TEXTO).encode(text="etiqueta:N")
    grafica = (barras + etiquetas).properties(height=48 * len(nombres), padding={"left": 8, "right": 8, "top": 4, "bottom": 4})
    st.html(f'<div class="d-seccion">{html.escape(titulo)}</div>')
    st.altair_chart(grafica.configure_view(stroke=None), width="stretch")
    st.space("small")


def grafica_de_linea(titulo, xs, ys, x_destacado, etiqueta_destacado, titulo_x, meta, nota_meta):
    # Línea con un punto por valor. El punto de `x_destacado` va más grande, con su etiqueta,
    # y la línea punteada marca la meta.
    datos = []
    for i in range(len(xs)):
        datos.append({"x": xs[i], "y": ys[i]})
    minimo = min(ys) // 10 * 10
    base = alt.Chart(alt.Data(values=datos)).encode(
        x=alt.X("x:Q", title=titulo_x, axis=alt.Axis(values=xs, grid=False)),
        y=alt.Y("y:Q", title=None, scale=alt.Scale(domain=[minimo, 100]), axis=alt.Axis(labelExpr="datum.value + '%'", tickCount=5)),
    )
    area = base.mark_area(color=AZUL, opacity=0.12, clip=True)
    linea = base.mark_line(color=AZUL, strokeWidth=3) + base.mark_point(color=AZUL, filled=True, size=36)
    linea_meta = alt.Chart(alt.Data(values=[{"y": meta}])).mark_rule(strokeDash=[4, 4], color="#7b8fae").encode(y="y:Q")
    punto = alt.Chart(alt.Data(values=[{"x": x_destacado, "y": ys[xs.index(x_destacado)], "etiqueta": etiqueta_destacado}])).encode(x="x:Q", y="y:Q")
    marca = punto.mark_point(color="#ffffff", filled=True, size=200) + punto.mark_text(dy=-18, fontSize=15, fontWeight="bold", color=TEXTO).encode(text="etiqueta:N")
    grafica = (area + linea + linea_meta + marca).properties(height=280, padding={"left": 8, "right": 12, "top": 8, "bottom": 4})
    st.html(f'<div class="d-seccion">{html.escape(titulo)}</div>')
    st.altair_chart(grafica.configure_view(stroke=None), width="stretch")
    st.caption(nota_meta)
    st.space("small")
