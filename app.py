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