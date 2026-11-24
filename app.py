import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configuración de la página
st.set_page_config(page_title="Análisis de Plantas de Energía", layout="wide")

# Cargar datos con caché
@st.cache_data
def cargar_datos():
    df = pd.read_csv("global_power_plant_database.csv")
    return df

# Mensaje de carga
with st.spinner("Cargando información... un momento por favor"):
    df = cargar_datos()

# Título principal
st.title("⚡ Análisis de Plantas de Energía del Mundo")
st.markdown("---")

# Barra lateral con filtros
with st.sidebar:
    st.header("🔍 Filtros")
    lista_energias = sorted(df["fuel1"].dropna().unique())
    energia_seleccionada = st.selectbox("Tipo de energía", lista_energias)
    
    valor_min = float(df["capacity_mw"].min())
    valor_max = float(df["capacity_mw"].max())
    rango = st.slider("Capacidad en MW", min_value=valor_min, max_value=valor_max,
                      value=(valor_min, valor_max))

# Sección de introducción
st.header("📋 1. ¿Qué encontramos en estos datos?")
st.write("Este análisis explora una base de datos con información de más de 28,000 plantas de energía en todo el mundo.")
st.write("El objetivo es entender qué fuentes de energía se utilizan con mayor frecuencia, su capacidad de producción y qué patrones existen entre los distintos tipos de plantas.")

st.subheader("Muestra de los datos")
st.dataframe(df.head(5))

# Sección de visualizaciones
st.header("📊 2. Visualizaciones")

st.subheader("¿Qué tipo de energía tiene más plantas en el mundo?")
conteo = df["fuel1"].value_counts()
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x=conteo.index, y=conteo.values, palette="viridis", ax=ax1)
ax1.set_xlabel("Fuente de energía")
ax1.set_ylabel("Número de plantas registradas")
plt.xticks(rotation=45)
st.pyplot(fig1)
st.info("💡 Interpretación: La energía hidroeléctrica y la solar son las que aparecen con mayor frecuencia en la base de datos, lo que sugiere una transición hacia fuentes renovables.")

st.subheader("¿Qué tipo de planta tiene mayor capacidad instalada?")
capacidad_prom = df.groupby("fuel1")["capacity_mw"].mean().sort_values(ascending=False)
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x=capacidad_prom.index, y=capacidad_prom.values, palette="coolwarm", ax=ax2)
ax2.set_xlabel("Fuente de energía")
ax2.set_ylabel("Capacidad promedio (MW)")
plt.xticks(rotation=45)
st.pyplot(fig2)
st.info("💡 Interpretación: Aunque hay menos plantas de carbón y nucleares, cada una tiene una capacidad de producción mucho mayor en promedio que las plantas solares, eólicas o hidroeléctricas.")

# Sección de validación estadística
st.header("📈 3. Validación estadística")
st.subheader("¿La diferencia de capacidad es real o casual?")

datos_hidro = df[df["fuel1"] == "Hydro"]["capacity_mw"].dropna()
datos_solar = df[df["fuel1"] == "Solar"]["capacity_mw"].dropna()
t_stat, valor_p = stats.ttest_ind(datos_hidro, datos_solar, equal_var=False)

st.write(f"- Capacidad promedio hidroeléctrica: *{datos_hidro.mean():.1f} MW*")
st.write(f"- Capacidad promedio solar: *{datos_solar.mean():.1f} MW*")
st.write(f"- Valor de significancia (p): *{valor_p:.2e}*")

if valor_p < 0.05:
    st.success("✅ Conclusión: La diferencia es estadísticamente significativa. Las plantas hidroeléctricas tienen mayor capacidad en promedio que las solares.")
else:
    st.info("✅ Conclusión: No hay suficiente evidencia para afirmar que las capacidades sean diferentes.")

# Hallazgos principales
st.header("📌 4. Hallazgos principales")
st.markdown("""
- 🌍 Las energías renovables son las más numerosas en cantidad de instalaciones.
- ⚡ Las plantas de energía convencional tienen mayor capacidad individual.
- 📊 La mayoría de las instalaciones son de tamaño pequeño o mediano.
""")

# Pie de página
st.markdown("---")
st.caption("📊 UNAD — Tarea 4 | Fuente de datos: Global Power Plant Database")
st.markdown("---")
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