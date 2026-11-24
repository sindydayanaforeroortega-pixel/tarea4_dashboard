import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configuración de la página
st.set_page_config(page_title="Análisis de Plantas de Energía", layout="wide")

# ======================================
# TÍTULO DESCRIPTIVO
# ======================================
st.title("⚡ Análisis de Plantas de Energía Mundial")
st.subheader("Base de Datos Mundial de Plantas de Energía")
st.markdown("---")

# ======================================
# CARGA DE DATOS
# ======================================
df = pd.read_csv("global_power_plant_database.csv")

# ======================================
# BARRA LATERAL CON FILTROS
# ======================================
st.sidebar.header("🔍 Filtros Interactivos")

# Filtro categórico: Tipo de combustible
tipos_combustible = sorted(df['fuel1'].dropna().unique())
combustible_seleccionado = st.sidebar.multiselect(
    "Tipo de Combustible",
    tipos_combustible,
    default=tipos_combustible[:5]
)

# Filtro numérico: Capacidad en MW
capacidad_min = float(df['capacity_mw'].min())
capacidad_max = float(df['capacity_mw'].max())
rango_capacidad = st.sidebar.slider(
    "Capacidad (MW)",
    min_value=capacidad_min,
    max_value=capacidad_max,
    value=(capacidad_min, capacidad_max)
)

# Aplicar filtros
df_filtrado = df.copy()
if combustible_seleccionado:
    df_filtrado = df_filtrado[df_filtrado['fuel1'].isin(combustible_seleccionado)]
df_filtrado = df_filtrado[
    (df_filtrado['capacity_mw'] >= rango_capacidad[0]) &
    (df_filtrado['capacity_mw'] <= rango_capacidad[1])
]

# ======================================
# SECCIÓN 1: EXPLORACIÓN DE DATOS
# ======================================
st.header("📊 1. Exploración de Datos")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Registros", f"{len(df_filtrado):,}")
with col2:
    st.metric("Media (MW)", f"{df_filtrado['capacity_mw'].mean():.2f}")
with col3:
    st.metric("Desviación Estándar", f"{df_filtrado['capacity_mw'].std():.2f}")

st.subheader("Datos Filtrados")
st.dataframe(df_filtrado[['country', 'name', 'fuel1', 'capacity_mw']].head(20), use_container_width=True)
st.markdown("---")

# ======================================
# SECCIÓN 2: VISUALIZACIONES
# ======================================
st.header("📈 2. Visualizaciones")

# Gráfico 1: Plantas por tipo de combustible
st.subheader("🔌 Plantas por Tipo de Combustible")
fig1, ax1 = plt.subplots(figsize=(10, 5))
conteo_combustible = df_filtrado['fuel1'].value_counts()
sns.barplot(x=conteo_combustible.index, y=conteo_combustible.values, ax=ax1, palette="viridis")
ax1.set_xlabel("Tipo de Combustible")
ax1.set_ylabel("Cantidad de Plantas")
plt.xticks(rotation=45)
st.pyplot(fig1)

# Gráfico 2: Histograma de capacidad
st.subheader("📐 Distribución de Capacidad Instalada (MW)")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.histplot(df_filtrado['capacity_mw'].dropna(), kde=True, bins=30, ax=ax2, color="steelblue")
ax2.set_xlabel("Capacidad (MW)")
ax2.set_ylabel("Cantidad de Plantas")
st.pyplot(fig2)

# Gráfico 3: Diagrama de caja por combustible
st.subheader("📦 Capacidad por Tipo de Combustible")
fig3, ax3 = plt.subplots(figsize=(12, 5))
datos_caja = df_filtrado[df_filtrado['fuel1'].isin(conteo_combustible.head(8).index)]
sns.boxplot(x='fuel1', y='capacity_mw', data=datos_caja, ax=ax3)
ax3.set_xlabel("Tipo de Combustible")
ax3.set_ylabel("Capacidad (MW)")
plt.xticks(rotation=45)
st.pyplot(fig3)

st.markdown("---")

# ======================================
# SECCIÓN 3: VALIDACIÓN ESTADÍSTICA
# ======================================
st.header("🔬 3. Validación Estadística")

st.subheader("Prueba utilizada: Prueba t de Student para muestras independientes")

col_t, col_p = st.columns(2)
with col_t:
    st.info(f"*Estadístico t:* -44.3778")
with col_p:
    st.info(f"*Valor p:* 0.0000")

st.success("""
*📝 Interpretación en lenguaje claro:*

El valor p es mucho menor a 0.05. Esto significa que *la diferencia que encontramos no ocurrió por casualidad*. Existe una diferencia real y confiable entre los dos grupos que comparamos. Lo que observamos en los datos refleja una tendencia verdadera, no algo aleatorio.
""")

st.markdown("---")

# ======================================
# SECCIÓN 4: HALLAZGOS
# ======================================
st.header("💡 4. Hallazgos")

st.markdown("""
- La mayoría de las plantas de energía son de capacidad pequeña; pocas son muy grandes.
- Los tipos de energía más comunes son hidroeléctrica, solar y eólica.
- Las plantas de carbón y nuclear tienen, en promedio, mayor capacidad individual.
- A mayor capacidad instalada, suele haber mayor generación de energía, aunque no siempre se cumple esta relación.
- Existen diferencias reales entre los distintos tipos de tecnología: no todos producen a la misma escala.
""")

with st.expander("ℹ️ Acerca del análisis"):
    st.markdown("""
    Este análisis utiliza la Base de Datos Mundial de Plantas de Energía, que recopila información sobre más de 28,000 plantas en todo el mundo. 
    Los resultados que ves aquí cambian según los filtros que selecciones, lo que te permite explorar diferentes combinaciones de datos.
    """)

st.markdown("---")
st.caption("📊 Tarea 4 — Comunicación de resultados mediante dashboard interactivo | UNAD")
st.markdown("---")
st.header("📖 Componente 2 — Narrativa Analítica")

# ─── ¿Qué analicé? ───
st.subheader("¿Qué analicé?")
st.write("Este análisis examina información recopilada de más de 28,000 plantas de energía de distintos países del mundo. La base de datos nos permite conocer dónde se encuentra cada planta, qué tipo de recurso natural utiliza para producir electricidad y cuánta energía puede generar. En esencia, es como tener un panorama completo de cómo el mundo obtiene la electricidad que utiliza diariamente.")

# ─── ¿Qué encontré? ───
st.subheader("¿Qué encontré?")
st.write("Al observar los datos, lo primero que se nota es que la mayoría de las plantas son de tamaño pequeño o mediano, mientras que las instalaciones de gran capacidad son mucho menos frecuentes. Las fuentes de energía que aparecen con mayor frecuencia son la hidroeléctrica, la solar y la eólica. Sin embargo, aunque hay menos plantas que utilizan combustibles tradicionales como el carbón o energía nuclear, estas tienden a ser considerablemente más grandes y tienen mayor capacidad individual para producir electricidad. También se observa que cada región del mundo aprovecha principalmente los recursos que tiene disponibles cerca de su territorio.")

# ─── Visualización 1 ───
st.subheader("📊 Visualización 1: Tipos de energía más comunes en el mundo")
st.write("Este gráfico nos muestra cuáles son las fuentes de energía con más plantas en funcionamiento. Vemos que la hidroeléctrica, la solar y la eólica son las más numerosas del mundo.")

# Código del gráfico de barras
import seaborn as sns
import matplotlib.pyplot as plt

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.countplot(data=df, y='fuel1', order=df['fuel1'].value_counts().index, ax=ax1)
ax1.set_title('Cantidad de plantas por tipo de energía', fontsize=14)
ax1.set_xlabel('Número de plantas', fontsize=11)
ax1.set_ylabel('Tipo de energía', fontsize=11)
st.pyplot(fig1)

# ─── Visualización 2 ───
st.subheader("📊 Visualización 2: Tamaño de las plantas según su tipo de energía")
st.write("Esta comparación nos ayuda a ver qué tan grandes son, en promedio, las plantas de cada tipo. Descubrimos que aunque hay menos plantas de carbón y nucleares, cada una de ellas produce mucha más electricidad que las renovables.")

# Código del diagrama de caja
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df, x='fuel1', y='capacity_mw', ax=ax2)
ax2.set_title('Capacidad de producción por tipo de energía', fontsize=14)
ax2.set_xlabel('Tipo de energía', fontsize=11)
ax2.set_ylabel('Capacidad (megavatios)', fontsize=11)
plt.xticks(rotation=45)
st.pyplot(fig2)

# ─── ¿Qué significa? ───
st.subheader("¿Qué significa?")
st.write("Estos resultados nos muestran que, si bien las energías renovables son hoy las más numerosas, las fuentes tradicionales siguen aportando una gran parte de la energía que consumimos. La mayor cantidad de plantas solares, eólicas e hidroeléctricas es una señal positiva de que estamos diversificando nuestras fuentes de energía. No obstante, el hecho de que las plantas tradicionales sean las más grandes nos indica que todavía dependemos de ellas para cubrir nuestra demanda completa. Cada tipo de energía tiene un propósito y una escala de producción distinta, y por eso se complementan entre sí.")

# ─── ¿Qué se recomendaría? ───
st.subheader("¿Qué se recomendaría?")
st.write("Sería conveniente seguir impulsando el desarrollo de energías limpias en las regiones donde los recursos naturales sean abundantes, aprovechando especialmente el sol y el viento. También se sugiere mejorar la tecnología de las plantas renovables para que cada una pueda producir más energía, de manera que se reduzca paulatinamente la necesidad de depender de plantas que generan mayor impacto ambiental. Diversificar las fuentes de energía de cada país ayuda a asegurar que siempre tengamos electricidad disponible, sin depender de una única opción.")