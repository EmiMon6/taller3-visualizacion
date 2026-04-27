# ============================================================
# TALLER #3: Visualización en Python
# Curso: ADM-3083 — Herramientas y Visualización
# Profesor: Juan Felipe Nájera Puente
# Integrantes:David Ayala| Emilio Montoya


# Librerias
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np
import ssl

# Desactivar la verificación SSL para poder descargar el dataset de seaborn en macOS
ssl._create_default_https_context = ssl._create_unverified_context

# linea para que el contenido ocupe todo el ancho de la hoja
st.set_page_config(layout="wide")

# decorador de streamlit para optimizar el rendimiento
# proposito: indicarle a streamlit que debe almacenar en cache (guardar en memoria)
# esto ayuda al rendimiento, velocidad y eficiencia de recurso
@st.cache_data
# funcion para cargar el dataset tips de seaborn
def cargar_datos():
    df = sns.load_dataset("tips")
    return df

# cargar los datos
tips = cargar_datos()

# ─────────────────────────────────────────────
# SIDEBAR — Panel de control
# ─────────────────────────────────────────────

# sidebar - panel de control para filtros
st.sidebar.header("Panel de Filtros")

# selector de ejercicio a mostrar
ejercicio_seleccionado = st.sidebar.radio(
    "Selecciona el ejercicio a visualizar",
    options=[
        "Ejercicio #1: Gráfico de Barras",
        "Ejercicio #2: Gráfico de Dispersión",
        "Ejercicio #3: Histograma",
        "Ejercicio #4: Barras Agrupado"
    ]
)

# selector del paso del makeover
paso_seleccionado = st.sidebar.selectbox(
    "Selecciona el paso del Makeover",
    options=["Paso 1: Por defecto", "Paso 2", "Paso 3", "Paso 4", "Paso Final"]
)

st.sidebar.markdown("---")

# filtro de día de la semana (aplica a ejercicios 1 y 4)
dias_disponibles = ["Thur", "Fri", "Sat", "Sun"]
dias_seleccionados = st.sidebar.multiselect(
    "Filtrar días (Ejercicios 1 y 4)",
    options=dias_disponibles,
    default=dias_disponibles
)

# filtro de umbral para propinas excepcionales (aplica a ejercicio 2)
umbral_percentil = st.sidebar.slider(
    "Percentil para propinas excepcionales (Ejercicio 2)",
    min_value=70,
    max_value=99,
    value=85,
    step=1
)

st.sidebar.markdown("---")
st.sidebar.caption("Dataset: Tips | Seaborn | ADM-3083")

# ─────────────────────────────────────────────
# TÍTULO PRINCIPAL
# ─────────────────────────────────────────────

# titulo principal del dashboard
st.title("Taller #3 — Visualización en Python")
st.markdown("**ADM-3083 Herramientas y Visualización** | Storytelling with Data | Dataset: `tips` (Seaborn)")
st.markdown("---")

# ─────────────────────────────────────────────
# PREPARACIÓN DE DATOS COMUNES
# ─────────────────────────────────────────────

# orden cronológico de días de la semana
orden_dias = ["Thur", "Fri", "Sat", "Sun"]

# mapeo de nombres en español
nombres_dias = {"Thur": "Jueves", "Fri": "Viernes", "Sat": "Sábado", "Sun": "Domingo"}

# colores base para todos los ejercicios
color_enfasis = "#0072B2"   # azul — elemento de foco
color_contexto = "#CCCCCC"  # gris — elemento de contexto
color_fondo = "#B0C4DE"     # azul suave — histograma


# ════════════════════════════════════════════════════════════
# EJERCICIO #1 — GRÁFICO DE BARRAS
# ════════════════════════════════════════════════════════════

if ejercicio_seleccionado == "Ejercicio #1: Gráfico de Barras":

    # encabezado del ejercicio
    st.header("Ejercicio #1: Gráfico de Barras")

    # contexto del análisis en markdown
    st.markdown("""
    **Contexto:** Somos analistas para el gerente de un restaurante.  
    Necesita saber **qué día de la semana tiene la cuenta promedio más alta** para decidir dónde enfocar sus promociones.

    **Pregunta de negocio:** ¿Cuál es el día de la semana con la cuenta promedio (`total_bill`) más alta?
    """)

    st.markdown("---")

    # filtrar días según selección del sidebar
    tips_filtrado = tips[tips["day"].isin(dias_seleccionados)]

    # calcular promedio de total_bill por día y reindexar al orden seleccionado
    dias_ordenados = [d for d in orden_dias if d in dias_seleccionados]
    promedio_por_dia = (
        tips_filtrado.groupby("day")["total_bill"]
        .mean()
        .reindex(dias_ordenados)
        .reset_index()
    )
    promedio_por_dia.columns = ["dia", "promedio"]

    # identificar el día con el promedio más alto
    dia_maximo = promedio_por_dia.loc[promedio_por_dia["promedio"].idxmax(), "dia"]

    # asignar color de énfasis al día máximo y gris al resto
    colores_e1 = [
        color_enfasis if dia == dia_maximo else color_contexto
        for dia in promedio_por_dia["dia"]
    ]

    # mostrar métricas rápidas en columnas
    col1, col2, col3 = st.columns(3)
    col1.metric("Día con mayor cuenta promedio", nombres_dias.get(dia_maximo, dia_maximo))
    col2.metric("Cuenta promedio más alta", f"${promedio_por_dia['promedio'].max():.2f}")
    col3.metric("Cuenta promedio más baja", f"${promedio_por_dia['promedio'].min():.2f}")

    st.markdown("---")

    # ── PASO 1: Por defecto ───────────────────────────────────────────────────
    if paso_seleccionado == "Paso 1: Por defecto":

        st.subheader("Paso 1: Gráfico por defecto")
        st.write("Gráfico base sin ninguna personalización. Colores sin significado, sin orden lógico, sin etiquetas y con ruido visual.")

        # grafico por defecto con seaborn sin personalización
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.barplot(data=tips_filtrado, x="day", y="total_bill", ax=ax)
        ax.set_title("total_bill por day")
        st.pyplot(fig)
        plt.close()

    # ── PASO 2: Calcular promedio y ordenar ───────────────────────────────────
    elif paso_seleccionado == "Paso 2":

        st.subheader("Paso 2: Calcular promedio y ordenar días")
        st.write("Calculamos explícitamente el promedio por día y ordenamos en secuencia semanal para dar coherencia narrativa.")

        # mostrar tabla de promedios calculados
        tabla_promedios = promedio_por_dia.copy()
        tabla_promedios["dia_esp"] = tabla_promedios["dia"].map(nombres_dias)
        tabla_promedios["promedio"] = tabla_promedios["promedio"].round(2)
        st.dataframe(tabla_promedios[["dia_esp", "promedio"]].rename(
            columns={"dia_esp": "Día", "promedio": "Promedio ($)"}
        ), use_container_width=True)

        # grafico con orden aplicado
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.bar(promedio_por_dia["dia"], promedio_por_dia["promedio"], color="#AAAAAA")
        ax.set_title("Paso 2: Días ordenados cronológicamente")
        st.pyplot(fig)
        plt.close()

    # ── PASO 3: Colores con intención ─────────────────────────────────────────
    elif paso_seleccionado == "Paso 3":

        st.subheader("Paso 3: Colores con intención — atributo pre-atentivo")
        st.write("Azul para el día con mayor cuenta (énfasis), gris para el resto (contexto). El color guía la atención sin necesitar explicación.")

        # grafico con colores aplicados
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.bar(promedio_por_dia["dia"], promedio_por_dia["promedio"], color=colores_e1)
        ax.set_title("Paso 3: Colores con intención")
        st.pyplot(fig)
        plt.close()

    # ── PASO 4: Limpiar ruido ─────────────────────────────────────────────────
    elif paso_seleccionado == "Paso 4":

        st.subheader("Paso 4: Limpiar ruido visual")
        st.write("Eliminamos bordes, grid y el eje Y. Cada elemento decorativo que no aporta información compite con el mensaje.")

        # grafico limpio sin ruido
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.bar(promedio_por_dia["dia"], promedio_por_dia["promedio"], color=colores_e1)

        # eliminar bordes innecesarios
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

        # ocultar eje y — las etiquetas harán ese trabajo
        ax.yaxis.set_visible(False)

        ax.set_title("Paso 4: Ruido eliminado")
        st.pyplot(fig)
        plt.close()

    # ── PASO FINAL ────────────────────────────────────────────────────────────
    elif paso_seleccionado == "Paso Final":

        st.subheader("Paso Final: Visualización Final")

        # grafico final completo
        fig, ax = plt.subplots(figsize=(11, 6))

        # barras con colores de intención
        bars = ax.bar(
            [nombres_dias[d] for d in promedio_por_dia["dia"]],
            promedio_por_dia["promedio"],
            color=colores_e1,
            width=0.6
        )

        # etiquetas dentro de cada barra
        for bar in bars:
            fc = bar.get_facecolor()
            # detectar si es la barra de énfasis (azul) o contexto (gris)
            es_enfasis = fc[0] < 0.5
            color_etq = "white" if es_enfasis else "#555555"
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() / 2,
                f"${bar.get_height():.2f}",
                ha="center", va="center",
                fontsize=13, fontweight="bold",
                color=color_etq
            )

        # eliminar ruido visual
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_color("#CCCCCC")
        ax.yaxis.set_visible(False)
        ax.tick_params(axis="x", length=0, labelsize=13, colors="#555555")

        # título narrativo — el hallazgo
        ax.set_title(
            "El domingo genera la cuenta promedio más alta de la semana",
            loc="left", fontsize=17, fontweight="bold", color="#2c2c2c", pad=30
        )

        # subtítulo descriptivo — el contexto
        fig.suptitle(
            "Cuenta promedio (USD) por día de la semana | Dataset: Tips (Seaborn)",
            x=0.125, y=0.96, ha="left", fontsize=12, color="#888888"
        )

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()


# ════════════════════════════════════════════════════════════
# EJERCICIO #2 — GRÁFICO DE DISPERSIÓN
# ════════════════════════════════════════════════════════════

elif ejercicio_seleccionado == "Ejercicio #2: Gráfico de Dispersión":

    # encabezado del ejercicio
    st.header("Ejercicio #2: Gráfico de Dispersión")

    # contexto del análisis
    st.markdown("""
    **Contexto:** Queremos entender la relación entre el costo de la cuenta (`total_bill`) y la propina (`tip`).  
    **Pregunta de negocio:** ¿A mayor cuenta, mayor propina? ¿Hay clientes excepcionalmente generosos?
    """)

    st.markdown("---")

    # calcular porcentaje de propina por observación
    tips_e2 = tips.copy()
    tips_e2["pct_propina"] = tips_e2["tip"] / tips_e2["total_bill"]

    # calcular umbral de propina excepcional usando el percentil seleccionado en el sidebar
    umbral_excepcional = tips_e2["pct_propina"].quantile(umbral_percentil / 100)

    # crear columna booleana para identificar propinas excepcionales
    tips_e2["es_excepcional"] = tips_e2["pct_propina"] > umbral_excepcional

    # separar en contexto y enfoque
    contexto_e2 = tips_e2[~tips_e2["es_excepcional"]]
    excepcionales_e2 = tips_e2[tips_e2["es_excepcional"]]

    # mostrar métricas rápidas
    col1, col2, col3 = st.columns(3)
    col1.metric("Propinas excepcionales identificadas", int(tips_e2["es_excepcional"].sum()))
    col2.metric("Umbral de propina excepcional", f"{umbral_excepcional:.1%} del total")
    col3.metric("Propina promedio del grupo excepcional", f"${excepcionales_e2['tip'].mean():.2f}")

    st.markdown("---")

    # ── PASO 1: Por defecto ───────────────────────────────────────────────────
    if paso_seleccionado == "Paso 1: Por defecto":

        st.subheader("Paso 1: Scatter plot por defecto")
        st.write("Todos los puntos con el mismo color y tamaño. No hay foco, no hay historia.")

        # scatter por defecto sin personalización
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.scatter(tips_e2["total_bill"], tips_e2["tip"])
        ax.set_title("total_bill vs tip")
        ax.set_xlabel("total_bill")
        ax.set_ylabel("tip")
        st.pyplot(fig)
        plt.close()

    # ── PASO 2: Criterio de propina excepcional ───────────────────────────────
    elif paso_seleccionado == "Paso 2":

        st.subheader("Paso 2: Definir el criterio de 'propina excepcional'")
        st.write(f"""
        Usamos el **percentil {umbral_percentil}** del porcentaje de propina (`tip / total_bill`) como umbral.  
        El porcentaje normaliza por el tamaño de la cuenta: $5 de propina en una cuenta de $6 es más generoso que $5 en una cuenta de $50.
        """)

        # mostrar la distribución del porcentaje de propina
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.hist(tips_e2["pct_propina"], bins=25, color="#AAAAAA", edgecolor="white")
        ax.axvline(umbral_excepcional, color="#E69F00", linewidth=2.5, linestyle="--")
        ax.text(umbral_excepcional + 0.01, ax.get_ylim()[1] * 0.85,
                f"Umbral: {umbral_excepcional:.1%}", color="#E69F00", fontsize=11, fontweight="bold")
        ax.set_title("Distribución del porcentaje de propina")
        ax.set_xlabel("Porcentaje de propina (tip / total_bill)")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        st.pyplot(fig)
        plt.close()

    # ── PASO 3: Colores con intención ─────────────────────────────────────────
    elif paso_seleccionado == "Paso 3":

        st.subheader("Paso 3: Diferenciar con color y tamaño")
        st.write("Gris para la tendencia general (contexto), naranja para las propinas excepcionales (enfoque).")

        # scatter con colores aplicados
        fig, ax = plt.subplots(figsize=(9, 5))

        # puntos de contexto: gris, pequeños, semi-transparentes
        ax.scatter(contexto_e2["total_bill"], contexto_e2["tip"],
                   color=color_contexto, s=40, alpha=0.6, label="Tendencia general")

        # puntos de enfoque: naranja, más grandes
        ax.scatter(excepcionales_e2["total_bill"], excepcionales_e2["tip"],
                   color="#E69F00", s=90, alpha=0.9, zorder=5, label="Propina excepcional")

        ax.set_title("Paso 3: Colores y tamaño aplicados")
        ax.legend()
        st.pyplot(fig)
        plt.close()

    # ── PASO 4: Limpiar ruido ─────────────────────────────────────────────────
    elif paso_seleccionado == "Paso 4":

        st.subheader("Paso 4: Limpiar ruido visual")
        st.write("Eliminamos bordes innecesarios y agregamos un grid horizontal sutil.")

        # scatter limpio
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.scatter(contexto_e2["total_bill"], contexto_e2["tip"],
                   color=color_contexto, s=40, alpha=0.6)
        ax.scatter(excepcionales_e2["total_bill"], excepcionales_e2["tip"],
                   color="#E69F00", s=90, alpha=0.9, zorder=5)

        # eliminar bordes superior y derecho
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#DDDDDD")
        ax.spines["bottom"].set_color("#DDDDDD")

        # grid horizontal sutil
        ax.yaxis.grid(True, linestyle="--", alpha=0.4, color="#EEEEEE")
        ax.set_axisbelow(True)

        ax.set_title("Paso 4: Ruido eliminado")
        st.pyplot(fig)
        plt.close()

    # ── PASO FINAL ────────────────────────────────────────────────────────────
    elif paso_seleccionado == "Paso Final":

        st.subheader("Paso Final: Visualización Final")

        # grafico final completo
        fig, ax = plt.subplots(figsize=(11, 7))

        # puntos de contexto: gris, pequeños, semi-transparentes
        ax.scatter(contexto_e2["total_bill"], contexto_e2["tip"],
                   color=color_contexto, s=45, alpha=0.55, label="Tendencia general")

        # puntos de enfoque: naranja, más grandes con borde
        ax.scatter(excepcionales_e2["total_bill"], excepcionales_e2["tip"],
                   color="#E69F00", s=110, alpha=0.95, zorder=5,
                   edgecolors="#c47d00", linewidths=0.8,
                   label=f"Propina excepcional (>{umbral_excepcional:.0%} del total)")

        # eliminar ruido visual
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#DDDDDD")
        ax.spines["bottom"].set_color("#DDDDDD")
        ax.yaxis.grid(True, linestyle="--", alpha=0.35, color="#EEEEEE")
        ax.set_axisbelow(True)

        # etiquetas de ejes descriptivas
        ax.set_xlabel("Total de la cuenta (USD)", fontsize=12, color="#555555", labelpad=10)
        ax.set_ylabel("Propina (USD)", fontsize=12, color="#555555", labelpad=10)
        ax.tick_params(colors="#777777", labelsize=11)

        # leyenda limpia sin recuadro
        ax.legend(frameon=False, fontsize=11, loc="upper left", labelcolor="#555555")

        # anotación del criterio utilizado
        ax.text(0.98, 0.05,
                f"Criterio: propina > {umbral_excepcional:.0%}\ndel total de la cuenta (p{umbral_percentil})",
                transform=ax.transAxes, ha="right", va="bottom",
                fontsize=9.5, color="#999999", style="italic")

        # título narrativo — el hallazgo
        ax.set_title(
            "Propina y cuenta se mueven juntas, pero un grupo\nde clientes es excepcionalmente generoso",
            loc="left", fontsize=16, fontweight="bold", color="#2c2c2c", pad=28
        )

        # subtítulo descriptivo
        fig.suptitle(
            "Relación entre total de cuenta y propina | Dataset: Tips (Seaborn)",
            x=0.125, y=0.97, ha="left", fontsize=11.5, color="#888888"
        )

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()


# ════════════════════════════════════════════════════════════
# EJERCICIO #3 — HISTOGRAMA
# ════════════════════════════════════════════════════════════

elif ejercicio_seleccionado == "Ejercicio #3: Histograma":

    # encabezado del ejercicio
    st.header("Ejercicio #3: Histograma")

    # contexto del análisis
    st.markdown("""
    **Contexto:** Necesitamos entender cómo se distribuyen las cuentas del restaurante.  
    **Pregunta de negocio:** ¿Dónde se concentra la mayoría del gasto de los clientes?
    """)

    st.markdown("---")

    # calcular el promedio de cuentas
    promedio_cuenta = tips["total_bill"].mean()

    # número de bins seleccionado en el sidebar (usamos el umbral_percentil como slider reutilizado)
    # para el histograma usamos un slider dedicado visible al usuario
    num_bins = st.sidebar.slider("Número de bins (Ejercicio 3)", min_value=5, max_value=50, value=20, step=1)

    # mostrar métricas rápidas
    col1, col2, col3 = st.columns(3)
    col1.metric("Promedio de cuentas", f"${promedio_cuenta:.2f}")
    col2.metric("Cuenta mínima", f"${tips['total_bill'].min():.2f}")
    col3.metric("Cuenta máxima", f"${tips['total_bill'].max():.2f}")

    st.markdown("---")

    # ── PASO 1: Por defecto ───────────────────────────────────────────────────
    if paso_seleccionado == "Paso 1: Por defecto":

        st.subheader("Paso 1: Histograma por defecto")
        st.write("Bins arbitrarios, colores sin significado, sin referencia del promedio. No comunica ningún hallazgo concreto.")

        # histograma por defecto sin personalización
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.hist(tips["total_bill"])
        ax.set_title("Distribución de cuentas")
        st.pyplot(fig)
        plt.close()

    # ── PASO 2: Ajuste de bins ────────────────────────────────────────────────
    elif paso_seleccionado == "Paso 2":

        st.subheader("Paso 2: Ajuste de bins")
        st.write("Comparamos distintas cantidades de bins para encontrar el número que mejor revela la forma de la distribución.")

        # comparar 3 cantidades de bins lado a lado
        fig, axes = plt.subplots(1, 3, figsize=(14, 4))

        for ax, bins in zip(axes, [5, 20, 40]):
            ax.hist(tips["total_bill"], bins=bins, color="#AAAAAA", edgecolor="white")
            ax.set_title(f"bins = {bins}")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)

        fig.suptitle("Comparación de número de bins", fontsize=13)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        st.info("✅ bins = 20 muestra la forma con claridad, sin ser ni demasiado granular ni demasiado agrupado.")

    # ── PASO 3: Línea de promedio ─────────────────────────────────────────────
    elif paso_seleccionado == "Paso 3":

        st.subheader("Paso 3: Línea de promedio y anotación")
        st.write("Marcamos el promedio con una línea vertical de referencia. Esto ancla al espectador en 'qué es mucho o poco'.")

        # histograma con línea de promedio
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.hist(tips["total_bill"], bins=num_bins, color="#AAAAAA", edgecolor="white")

        # línea vertical del promedio
        ax.axvline(promedio_cuenta, color=color_enfasis, linewidth=2.5, linestyle="--")

        # anotación del valor
        ax.text(promedio_cuenta + 0.5, ax.get_ylim()[1] * 0.85,
                f"Promedio\n${promedio_cuenta:.2f}",
                color=color_enfasis, fontsize=11, fontweight="bold")

        ax.set_title("Paso 3: Línea de promedio + anotación")
        st.pyplot(fig)
        plt.close()

    # ── PASO 4: Limpiar ruido ─────────────────────────────────────────────────
    elif paso_seleccionado == "Paso 4":

        st.subheader("Paso 4: Limpiar ruido visual")
        st.write("Mejoramos el color de las barras, eliminamos bordes y añadimos un grid horizontal sutil.")

        # histograma limpio
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.hist(tips["total_bill"], bins=num_bins, color=color_fondo, edgecolor="white", linewidth=0.5)
        ax.axvline(promedio_cuenta, color=color_enfasis, linewidth=2.5, linestyle="--")

        # eliminar bordes innecesarios
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#DDDDDD")
        ax.spines["bottom"].set_color("#DDDDDD")

        # grid horizontal sutil
        ax.yaxis.grid(True, linestyle="--", alpha=0.3, color="#EEEEEE")
        ax.set_axisbelow(True)

        ax.set_title("Paso 4: Ruido eliminado")
        st.pyplot(fig)
        plt.close()

    # ── PASO FINAL ────────────────────────────────────────────────────────────
    elif paso_seleccionado == "Paso Final":

        st.subheader("Paso Final: Visualización Final")

        # grafico final completo
        fig, ax = plt.subplots(figsize=(11, 6.5))

        # histograma con bins ajustados y color base neutro
        ax.hist(tips["total_bill"], bins=num_bins, color=color_fondo, edgecolor="white", linewidth=0.5)

        # línea vertical del promedio
        ax.axvline(promedio_cuenta, color=color_enfasis, linewidth=2.5, linestyle="--", zorder=5)

        # anotación del promedio con flecha
        ax.annotate(
            f"Promedio: ${promedio_cuenta:.2f}",
            xy=(promedio_cuenta, ax.get_ylim()[1] * 0.7),
            xytext=(promedio_cuenta + 5, ax.get_ylim()[1] * 0.75),
            fontsize=12, fontweight="bold", color=color_enfasis,
            arrowprops=dict(arrowstyle="->", color=color_enfasis, lw=1.5)
        )

        # eliminar ruido visual
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#DDDDDD")
        ax.spines["bottom"].set_color("#DDDDDD")
        ax.yaxis.grid(True, linestyle="--", alpha=0.3, color="#EEEEEE")
        ax.set_axisbelow(True)

        # etiquetas de ejes descriptivas
        ax.set_xlabel("Total de la cuenta (USD)", fontsize=12, color="#555555", labelpad=10)
        ax.set_ylabel("Número de mesas", fontsize=12, color="#555555", labelpad=10)
        ax.tick_params(colors="#777777", labelsize=11)

        # título narrativo — el hallazgo
        ax.set_title(
            "La mayoría de las mesas gasta entre $10 y $20,\npero el gasto promedio llega a $19.79",
            loc="left", fontsize=16, fontweight="bold", color="#2c2c2c", pad=28
        )

        # subtítulo descriptivo
        fig.suptitle(
            "Distribución de cuentas (USD) | Dataset: Tips (Seaborn)",
            x=0.125, y=0.97, ha="left", fontsize=11.5, color="#888888"
        )

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()


# ════════════════════════════════════════════════════════════
# EJERCICIO #4 — GRÁFICO DE BARRAS AGRUPADO
# ════════════════════════════════════════════════════════════

elif ejercicio_seleccionado == "Ejercicio #4: Barras Agrupado":

    # encabezado del ejercicio
    st.header("Ejercicio #4: Gráfico de Barras Agrupado")

    # contexto del análisis
    st.markdown("""
    **Contexto:** Comparamos la cuenta promedio por día de la semana, diferenciando entre hombres y mujeres.  
    **Pregunta de negocio:** ¿Las mujeres gastan más o menos que los hombres? ¿Varía por día?
    """)

    st.markdown("---")

    # filtrar días según selección del sidebar
    tips_e4 = tips[tips["day"].isin(dias_seleccionados)]

    # calcular promedio de total_bill por día y género
    dias_ordenados_e4 = [d for d in orden_dias if d in dias_seleccionados]
    promedio_genero = (
        tips_e4.groupby(["day", "sex"])["total_bill"]
        .mean()
        .reset_index()
    )
    promedio_genero.columns = ["dia", "genero", "promedio"]

    # mantener solo días seleccionados y ordenar
    promedio_genero = promedio_genero[promedio_genero["dia"].isin(dias_ordenados_e4)].copy()
    promedio_genero["dia"] = pd.Categorical(
        promedio_genero["dia"], categories=dias_ordenados_e4, ordered=True
    )
    promedio_genero = promedio_genero.sort_values("dia")

    # separar por género
    female = promedio_genero[promedio_genero["genero"] == "Female"].reset_index(drop=True)
    male = promedio_genero[promedio_genero["genero"] == "Male"].reset_index(drop=True)

    # posición de las barras en el eje x
    x = np.arange(len(dias_ordenados_e4))
    ancho = 0.35  # ancho de cada barra

    # colores con intención: female es el foco, male es el contexto
    color_female = color_enfasis  # azul — enfoque
    color_male = color_contexto   # gris — contexto

    # mostrar métricas rápidas
    col1, col2, col3 = st.columns(3)
    col1.metric("Promedio Female (todos los días)", f"${female['promedio'].mean():.2f}")
    col2.metric("Promedio Male (todos los días)", f"${male['promedio'].mean():.2f}")
    col3.metric("Diferencia promedio", f"${abs(female['promedio'].mean() - male['promedio'].mean()):.2f}")

    st.markdown("---")

    # ── PASO 1: Por defecto ───────────────────────────────────────────────────
    if paso_seleccionado == "Paso 1: Por defecto":

        st.subheader("Paso 1: Gráfico agrupado por defecto")
        st.write("Ambas series compiten por la atención con colores igualmente llamativos. No hay foco ni contexto.")

        # grafico agrupado por defecto con seaborn
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.barplot(data=tips_e4, x="day", y="total_bill", hue="sex", ax=ax)
        ax.set_title("total_bill por día y género")
        st.pyplot(fig)
        plt.close()

    # ── PASO 2: Preparar datos y ordenar ──────────────────────────────────────
    elif paso_seleccionado == "Paso 2":

        st.subheader("Paso 2: Preparar y ordenar los datos")
        st.write("Calculamos el promedio por día y género, y ordenamos los días en secuencia semanal.")

        # mostrar tabla de promedios
        tabla_e4 = promedio_genero.copy()
        tabla_e4["dia_esp"] = tabla_e4["dia"].map(nombres_dias)
        tabla_e4["promedio"] = tabla_e4["promedio"].round(2)
        st.dataframe(
            tabla_e4[["dia_esp", "genero", "promedio"]].rename(
                columns={"dia_esp": "Día", "genero": "Género", "promedio": "Promedio ($)"}
            ),
            use_container_width=True
        )

        # grafico agrupado ordenado
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.bar(x - ancho/2, male["promedio"], ancho, color="#AAAAAA", label="Male")
        ax.bar(x + ancho/2, female["promedio"], ancho, color="#888888", label="Female")
        ax.set_xticks(x)
        ax.set_xticklabels([nombres_dias.get(d, d) for d in dias_ordenados_e4])
        ax.legend()
        ax.set_title("Paso 2: Datos ordenados por día")
        st.pyplot(fig)
        plt.close()

    # ── PASO 3: Colores con intención ─────────────────────────────────────────
    elif paso_seleccionado == "Paso 3":

        st.subheader("Paso 3: Colores con intención")
        st.write("Female = azul (foco principal), Male = gris (contexto/línea base).")

        # grafico con colores de intención aplicados
        fig, ax = plt.subplots(figsize=(9, 5))

        # barras de contexto: male — gris
        ax.bar(x - ancho/2, male["promedio"], ancho, color=color_male, label="Male (contexto)")

        # barras de enfoque: female — azul
        ax.bar(x + ancho/2, female["promedio"], ancho, color=color_female, label="Female (foco)")

        ax.set_xticks(x)
        ax.set_xticklabels([nombres_dias.get(d, d) for d in dias_ordenados_e4])
        ax.legend()
        ax.set_title("Paso 3: Colores con intención")
        st.pyplot(fig)
        plt.close()

    # ── PASO 4: Limpiar ruido + etiquetas ─────────────────────────────────────
    elif paso_seleccionado == "Paso 4":

        st.subheader("Paso 4: Limpiar ruido y agregar etiquetas")
        st.write("Eliminamos bordes, eje Y y colocamos etiquetas diferenciadas por color sobre cada barra.")

        # grafico limpio con etiquetas
        fig, ax = plt.subplots(figsize=(9, 5))
        barras_male = ax.bar(x - ancho/2, male["promedio"], ancho, color=color_male)
        barras_female = ax.bar(x + ancho/2, female["promedio"], ancho, color=color_female)

        # etiquetas sobre barras male: gris, más pequeñas
        for bar in barras_male:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    f"${bar.get_height():.1f}", ha="center", va="bottom",
                    fontsize=10, color="#999999")

        # etiquetas sobre barras female: azul, negrita
        for bar in barras_female:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    f"${bar.get_height():.1f}", ha="center", va="bottom",
                    fontsize=10, fontweight="bold", color=color_female)

        # eliminar ruido visual
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.yaxis.set_visible(False)
        ax.set_xticks(x)
        ax.set_xticklabels([nombres_dias.get(d, d) for d in dias_ordenados_e4])

        ax.set_title("Paso 4: Etiquetas y ruido eliminado")
        st.pyplot(fig)
        plt.close()

    # ── PASO FINAL ────────────────────────────────────────────────────────────
    elif paso_seleccionado == "Paso Final":

        st.subheader("Paso Final: Visualización Final")

        # grafico final completo
        fig, ax = plt.subplots(figsize=(12, 6.5))

        # barras de contexto: male — gris claro
        barras_male = ax.bar(x - ancho/2, male["promedio"], ancho, color=color_male)

        # barras de enfoque: female — azul
        barras_female = ax.bar(x + ancho/2, female["promedio"], ancho, color=color_female)

        # etiquetas sobre barras male (contexto): gris, más tenues
        for bar in barras_male:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.35,
                f"${bar.get_height():.1f}",
                ha="center", va="bottom",
                fontsize=10, color="#999999"
            )

        # etiquetas sobre barras female (enfoque): azul, negrita
        for bar in barras_female:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.35,
                f"${bar.get_height():.1f}",
                ha="center", va="bottom",
                fontsize=11, fontweight="bold", color=color_female
            )

        # leyenda personalizada con mpatches — sin depender del sistema automático
        parche_female = mpatches.Patch(color=color_female, label="Female (foco)")
        parche_male = mpatches.Patch(color=color_male, label="Male (contexto)")
        ax.legend(handles=[parche_female, parche_male],
                  frameon=False, fontsize=11, loc="upper left", labelcolor="#555555")

        # eliminar ruido visual
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_color("#CCCCCC")
        ax.yaxis.set_visible(False)
        ax.tick_params(axis="x", length=0, labelsize=13, colors="#555555")
        ax.set_xticks(x)
        ax.set_xticklabels([nombres_dias.get(d, d) for d in dias_ordenados_e4])

        # título narrativo — el hallazgo
        ax.set_title(
            "Los hombres gastan consistentemente más que las mujeres,\nexcepto el viernes donde la diferencia se invierte",
            loc="left", fontsize=16, fontweight="bold", color="#2c2c2c", pad=28
        )

        # subtítulo descriptivo
        fig.suptitle(
            "Cuenta promedio (USD) por día y género | Dataset: Tips (Seaborn)",
            x=0.125, y=0.97, ha="left", fontsize=11.5, color="#888888"
        )

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()


# ─────────────────────────────────────────────
# PIE DE PÁGINA — Bibliografía y referencias
# ─────────────────────────────────────────────

st.markdown("---")
with st.expander("📚 Bibliografía y Referencias"):
    st.markdown("""
    **Referencia principal**
    - Knaflic, C. N. (2015). *Storytelling with Data: A Data Visualization Guide for Business Professionals*. Wiley.

    **Documentación oficial**
    - Waskom, M. (2021). Seaborn: https://seaborn.pydata.org/
    - Hunter, J. D. (2007). Matplotlib: https://matplotlib.org/stable/
    - pandas Development Team (2024). pandas: https://pandas.pydata.org/docs/

    **Dataset**
    - Tips dataset (Seaborn). Fuente original: Bryant, P. G. & Smith, M. (1995). *Practical Data Analysis: Case Studies in Business Statistics*. Irwin Publishing.

    **Curso**
    - ADM-3083 Herramientas y Visualización | Profesor: Juan Felipe Nájera Puente
    """)
