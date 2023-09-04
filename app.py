# app.py
import streamlit as st
import consultar  

# Crear un menú lateral 
st.sidebar.title("Menú")

# Establecer una variable de estado para controlar la página actual
pagina_actual = st.sidebar.radio("Selecciona una opción:", ["Inicio", "Consultar"])

# Contenido de la página de inicio
pagina_inicio = """
# Infecciones Respiratorias Agudas

En esta aplicación, presentamos los resultados de un extenso proceso de investigación y desarrollo
centrado en el análisis de datos relacionados con infecciones respiratorias agudas. A lo largo de este proyecto,
hemos explorado y aplicado técnicas avanzadas de aprendizaje automático, incluyendo K-Means y T-SNE,
con el objetivo de mejorar la planificación de medidas de salud pública y fortalecer las campañas de prevención en Argentina.

El análisis de infecciones respiratorias agudas es de suma importancia, ya que estas afecciones afectan significativamente
la salud de la población y requieren una gestión efectiva por parte de las autoridades de salud pública. Esta aplicación
proporciona una herramienta valiosa para visualizar y comprender los patrones de incidencia de estas infecciones en diferentes
provincias de Argentina, lo que permite una toma de decisiones más informada y la implementación de estrategias más efectivas
para proteger la salud de la población.

Te invitamos a explorar las diferentes funcionalidades de esta aplicación y a utilizarla como una herramienta de apoyo en la
toma de decisiones relacionadas con la salud pública y la prevención de infecciones respiratorias agudas en Argentina.
"""

# Mostrar la página de inicio por defecto
if pagina_actual == "Inicio":
    st.markdown(pagina_inicio, unsafe_allow_html=True)

# Si se selecciona "Consultar", mostrar la página de consulta
if pagina_actual == "Consultar":
    consultar.mostrar_pagina_consultar()