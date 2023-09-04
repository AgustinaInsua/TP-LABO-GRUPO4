# consultar.py
import streamlit as st
from backend import *

def mostrar_pagina_consultar():
    st.title('Consultar prioridad en provincias')

    # Utiliza CSS personalizado para alinear los elementos a la izquierda
    st.markdown(
        """
        <style>
        .st-ek {
            max-width: 800px;  /* Ajusta el ancho a tu preferencia */
            margin: auto;      /* Centra el contenido horizontalmente */
            text-align: left;  /* Alinea el texto a la izquierda */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    provincia_seleccionada = st.selectbox('Selecciona una provincia de Argentina', ['Buenos Aires', 'CABA', 'Catamarca', 'Chaco', 'Chubut', 'Córdoba', 'Corrientes', 'Entre Ríos', 'Formosa', 'Jujuy','La Pampa', 'La Rioja', 'Mendoza', 'Misiones', 'Neuquén', 'Río Negro', 'Salta', 'San Juan', 'San Luis', 'Santa Cruz', 'Santa Fe', 'Santiago del Estero', 'Tierra del Fuego', 'Tucumán'])
    
    enfermedad_seleccionada = st.selectbox('Seleccione una enfermedad',['Bronquiolitis en menores de 2 años', 'Enfermedad tipo influenza (ETI)', 'Neumonía'] )

    edad_ingresada= st.number_input('Ingrese su edad', min_value=0, max_value=120, value=1) 

    # Clasificar la edad del usuario en grupos
    if 0 <= edad_ingresada <= 1:
       grupo_edad_id = 1  # Bebés 0 a 23 meses
    elif 2 <= edad_ingresada <= 14:
       grupo_edad_id = 2  # Niños 2 a 14 años
    elif 15 <= edad_ingresada <= 24:
       grupo_edad_id = 3  # Jóvenes 15 a 24 años
    elif 25 <= edad_ingresada <= 64:
       grupo_edad_id = 4  # Adultos 25 a 64 años
    else:
       grupo_edad_id = 5  # Adultos mayores > 65 años

    if st.button('Consultar'):
       provincia_id = mapear_provincia_a_id(provincia_seleccionada) 
       enfermedad_id = mapear_enfermedad_a_id(enfermedad_seleccionada)
       resultado = consultar_riesgo_de_enfermarse(provincia_id, grupo_edad_id, enfermedad_id, provincia_seleccionada, enfermedad_seleccionada )  
     
     # Establecer una clase CSS en función de la prioridad
       
       if "Prioridad alta" in resultado:
           st.markdown(
               f'<p class="error-message" style="font-size: 26px;">{resultado}</p>', 
               unsafe_allow_html=True
            )
       elif "Prioridad baja" in resultado:
            st.markdown(                
                f'<p class="success-message" style="font-size: 26px;">{resultado}</p>', 
                unsafe_allow_html=True
            )
       else:                     
           st.write(resultado, key="resultado")

       # Agregar CSS personalizado
       st.markdown(
           """
           <style>
           .error-message {
           color: red;
           }
           .success-message {
           color: green;
           }
           </style>
           """,
           unsafe_allow_html=True,
        )

       
