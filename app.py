import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Análisis de la Base de Datos Mundial de Plantas de Energía", layout="wide")

@st.cache_data
def cargar_datos():
    df = pd.read_csv("global_power_plant_database.csv")
    return df

with st.spinner("Cargando información... un momento por favor"):
    df = cargar_datos()

st.title("Análisis de la Base de Datos Mundial de Plantas de Energía")
st.markdown("---")

with st.sidebar:
    st.header("Filtros")
    lista_energias = sorted(df["fuel1"].dropna().unique())
    energia_seleccionada = st.selectbox("Tipo de energía", lista_energias)
    
    valor_min = float(df["capacity_mw"].min())
    valor_max = float(df["capacity_mw"].max())
    rango = st.slider("Capacidad en MW", min_value=valor_min, max_value=valor_max,
                      value=(valor_min, valor_max))

df_filtrado = df[
    (df["fuel1"] == energia_seleccionada) &
    (df["capacity_mw"] >= rango[0]) &
    (df["capacity_mw"] <= rango[1])
]

st.header("1. Exploración de datos")
st.write("Este análisis explora una base de datos con información de más de 28,000 plantas de energía en todo el mundo.")

st.subheader("Datos filtrados según tus selecciones")
st.dataframe(df_filtrado)

st.subheader("Métricas del conjunto actual")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de plantas", f"{len(df_filtrado):,}")
with col2:
    st.metric("Capacidad promedio", f"{df_filtrado['capacity_mw'].mean():.1f} MW")
with col3:
    st.metric("Desviación estándar", f"{df_filtrado['capacity_mw'].std():.1f} MW")

st.header("2. Visualizaciones")

st.subheader("Gráfico 1: Cantidad de plantas por tipo de energía")
conteo = df_filtrado["fuel1"].value_counts()
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x=conteo.index, y=conteo.values, palette="viridis", ax=ax1)
ax1.set_xlabel("Fuente de energía")
ax1.set_ylabel("Número de plantas registradas")
plt.xticks(rotation=45)
st.pyplot(fig1)
st.info("Gráfico desarrollado en Tarea 3 Parte 3 — Se actualiza según los filtros seleccionados.")

st.subheader("Gráfico 2: Capacidad promedio por tipo de energía")
capacidad_prom = df_filtrado.groupby("fuel1")["capacity_mw"].mean().sort_values(ascending=False)
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x=capacidad_prom.index, y=capacidad_prom.values, palette="coolwarm", ax=ax2)
ax2.set_xlabel("Fuente de energía")
ax2.set_ylabel("Capacidad promedio (MW)")
plt.xticks(rotation=45)
st.pyplot(fig2)
st.info("Gráfico desarrollado en Tarea 3 Parte 3 — Se actualiza según los filtros seleccionados.")

st.subheader("Gráfico 3: Distribución de capacidad instalada")
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.histplot(df_filtrado["capacity_mw"].dropna(), bins=30, kde=True, ax=ax3)
ax3.set_xlabel("Capacidad en MW")
ax3.set_ylabel("Cantidad de plantas")
st.pyplot(fig3)
st.info("Gráfico desarrollado en Tarea 3 Parte 3 — Se actualiza según los filtros seleccionados.")

st.header("3. Validación estadística")

st.subheader("Prueba t de Student: Plantas renovables vs. no renovables")
st.write("- Estadístico t: -44.3778  (Resultado calculado en Tarea 3 Parte 1)")
st.write("- Valor p: 0.0000")
st.write("- Nivel de confianza: 95% (alfa = 0.05)")
st.success("En lenguaje claro: El valor p es menor a 0.05, por lo tanto existe una diferencia real y significativa entre la capacidad promedio de plantas renovables y no renovables. Esta diferencia no es por casualidad; hay evidencia estadística que confirma que las plantas no renovables tienen, en promedio, mayor capacidad instalada que las renovables.")

st.subheader("Prueba Chi-cuadrado: Tipo de energía por región")
st.write("- Valor Chi-cuadrado: 44.00  (Resultado calculado en Tarea 3 Parte 1)")
st.write("- Grados de libertad: 12")
st.write("- Valor p: 0.0000")
st.success("En lenguaje claro: El valor p es menor a 0.05, por lo tanto existe una relación real entre el tipo de energía y la región. No todos los tipos de plantas se distribuyen igual en el mundo; el lugar influye en qué tipo de energía se utiliza más. Esta relación no es por azar.")

st.header("4. Hallazgos principales")
st.markdown("""
- Las energías renovables son las más abundantes en cantidad de instalaciones.
- Las plantas de energía no renovable tienen significativamente mayor capacidad instalada en promedio.
- La mayoría de las instalaciones son de pequeña o mediana capacidad.
- Existe una relación entre el tipo de energía y la región geográfica del mundo.
- Al usar los filtros, puedes ver cómo cambian estos resultados según el tipo de energía y su tamaño.
""")

st.markdown("---")
st.caption("UNAD — Tarea 4 | Fuente de datos: Global Power Plant Database")
st.header("📖 Componente 2 — Narrativa Analítica")

# ─── ¿Qué analicé? ───
st.subheader("¿Qué analicé?")
st.write("Examiné información de más de 28,000 plantas de energía de distintos países del mundo. Estos datos nos dicen dónde está ubicada cada planta, qué tipo de recurso natural usa para producir electricidad y cuánta energía puede generar. Es como tener un panorama completo de cómo el mundo obtiene su electricidad.")

# ─── ¿Qué encontré? ───
st.subheader("¿Qué encontré?")
st.write("La mayoría de las plantas son pequeñas o medianas; muy pocas son enormes. Las fuentes de energía que más aparecen son la hidroeléctrica, la solar y la eólica. Sin embargo, las plantas que usan carbón o energía nuclear, aunque son menos, suelen ser mucho más grandes y producen más electricidad cada una. También noté que cada región aprovecha principalmente los recursos que tiene cerca.")

# ─── Visualización 1 ───
st.subheader("📊 Tipos de energía más comunes en el mundo")
st.write("Este gráfico nos muestra cuáles son las fuentes de energía con más plantas en funcionamiento. Se ve claramente que la hidroeléctrica, la solar y la eólica son las que más abundan en el mundo.")

import seaborn as sns
import matplotlib.pyplot as plt

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.countplot(data=df, y='fuel1', order=df['fuel1'].value_counts().index, ax=ax1)
ax1.set_title('Cantidad de plantas por tipo de energía', fontsize=14)
ax1.set_xlabel('Número de plantas', fontsize=11)
ax1.set_ylabel('Tipo de energía', fontsize=11)
st.pyplot(fig1)

# ─── Visualización 2 ───
st.subheader("📊 Tamaño de las plantas según su tipo de energía")
st.write("Al comparar el tamaño de las plantas, vemos que las que usan carbón o energía nuclear suelen ser mucho más grandes que las demás. Esto significa que aunque hay menos de estas plantas, cada una produce mucha más electricidad que la mayoría de las plantas renovables.")

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df, x='fuel1', y='capacity_mw', ax=ax2)
ax2.set_title('Capacidad de producción por tipo de energía', fontsize=14)
ax2.set_xlabel('Tipo de energía', fontsize=11)
ax2.set_ylabel('Capacidad de producción (megavatios)', fontsize=11)
plt.xticks(rotation=45)
st.pyplot(fig2)

# ─── ¿Qué significa? ───
st.subheader("¿Qué significa esto?")
st.write("Que haya más plantas solares y eólicas es una buena señal de que estamos usando más energía limpia. Pero que las plantas tradicionales sean las más grandes nos dice que todavía dependemos de ellas para tener suficiente electricidad. No todas las fuentes de energía funcionan igual: unas son muchas pero pequeñas, y otras son pocas pero muy grandes.")

# ─── ¿Qué se recomendaría? ───
st.subheader("¿Qué se recomendaría?")
st.write("Conviene seguir aprovechando el sol y el viento en los lugares donde abundan. También sería bueno mejorar las plantas renovables para que cada una pueda producir más energía. Si diversificamos nuestras fuentes, no dependemos de una sola opción y el suministro de electricidad será más seguro y estable para todos.")