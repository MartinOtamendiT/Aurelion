import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime

# Inicialización del Estado de Sesión.
# Se inicializa el estado para la opción seleccionada.
if 'selected_option' not in st.session_state:
    # El valor de None será indicaivo de regresar al menú principal
    st.session_state.selected_option = None

# Diccionario de opciones. Asocia cada opción con una clave utilizada por selected_option.
options = {
    1: "Ver productos",
    2: "Ver ventas",
    3: "Ver clientes",
    0: "Salir",
}


# --- Función de Navegación ---
def navigate_to(option):
    """Función para cambiar la opción seleccionada y permitir la navegación a la página."""
    st.session_state.selected_option = option

# --- 3. Vistas de la Aplicación ---
def main_menu():
    """Función que muestra el menú principal"""
    st.title("Tienda Aurelion")
    st.info("Seleccione una de las siguientes opciones:")

    st.button(
        options[1], use_container_width=True, 
        on_click=navigate_to, args=(1,)
    )
    st.button(
        options[2], use_container_width=True, 
        on_click=navigate_to, args=(2,)
    )
    st.button(
        options[3], use_container_width=True, 
        on_click=navigate_to, args=(3,)
    )
    st.button(
        options[0], use_container_width=True, 
        on_click=navigate_to, args=(0,)
    )

    st.markdown("---")


def test_page():
    """Función que permite probar el cambio de página"""
    
    st.markdown(f"Ha elegido la opción: {options[st.session_state.selected_option]}")

    st.markdown("---")

    # Botón para regresar al menú principal
    st.button(
        "⬅️ Volver al Menú Principal",
        on_click=navigate_to, args=(None,)
    )

def see_products():
    """Función que muestra los productos disponibles en la tienda"""
    # Extracción de datos desde archivo excel
    ventas = pd.read_excel("./data/productos_corregidos.xlsx")
    # Construcción de lista de categorias.
    categories = np.insert(ventas["categoria_corregida"].unique(), 0, "Todas las categorias")
    # Captura de selección de categoría.
    selected_category = st.selectbox("Selecciona categoria:", categories)
    # Eliminación de columna "categoria" para evitar confusión.
    ventas = ventas.drop(columns=["categoria"])
    # Filtro de dataframe con la columna "categoria"
    if selected_category == "Todas las categorias":
        st.dataframe(ventas)
    else:
        st.dataframe(ventas[ventas["categoria_corregida"] == selected_category])
    
    st.markdown("---")
    # Botón para regresar al menú principal
    st.button(
        "⬅️ Volver al Menú Principal",
        on_click=navigate_to, args=(None,)
    )

def see_clients():
    """Función que muestra la información de los clientes"""
    # Extracción de datos desde archivo excel
    clientes = pd.read_excel("./data/clientes.xlsx")

    clientes["antiguedad"] = datetime.now() - clientes["fecha_alta"]

    selected_cities = st.multiselect(
        "Selecciona las ciudades de origen de los clientes:",
        options=clientes["ciudad"].unique(),
        default=clientes["ciudad"].unique()
    )
    st.dataframe(clientes[clientes["ciudad"].isin(selected_cities)].drop(columns=["ciudad"]))

    st.markdown("---")
    # Botón para regresar al menú principal
    st.button(
        "⬅️ Volver al Menú Principal",
        on_click=navigate_to, args=(None,)
    )

def see_sales():
    """Función que muestra la información de las ventas"""
    # Extracción de datos desde archivo excel
    ventas = pd.read_excel("./data/ventas.xlsx")
    detalle_ventas = pd.read_excel("./data/detalle_ventas.xlsx")
    clients = pd.read_excel("./data/clientes.xlsx")

    ventas_completas = ventas.merge(detalle_ventas, on="id_venta", suffixes=("_ventas", "_dventas")).merge(clients[["id_cliente", "ciudad"]], on="id_cliente")

    selected_cities = st.multiselect(
        "Selecciona las ciudades de origen de los clientes:",
        options=clients["ciudad"].unique(),
        default=clients["ciudad"].unique()
    )

    # Construcción de lista de categorias.
    medios_pago = np.insert(ventas["medio_pago"].unique(), 0, "Todos los medios de pago")
    selected_medio_pago = st.selectbox("Selecciona el medio de pago:", medios_pago)

    selected_id_venta = st.number_input('Ingresa el ID de la venta:', min_value=int(ventas_completas["id_venta"].min()), max_value=int(ventas_completas["id_venta"].max()), value=int(ventas_completas["id_venta"].min()), step=1)
    if selected_medio_pago == "Todos los medios de pago":
        st.dataframe(ventas_completas[ventas_completas["ciudad"].isin(selected_cities) & (ventas_completas["id_venta"] == selected_id_venta)].drop(columns=["ciudad"]))
    else:
        st.dataframe(ventas_completas[ventas_completas["ciudad"].isin(selected_cities) & (ventas_completas["medio_pago"] == selected_medio_pago) & (ventas_completas["id_venta"] == selected_id_venta)].drop(columns=["ciudad"]))

    st.markdown("---")
    # Botón para regresar al menú principal
    st.button(
        "⬅️ Volver al Menú Principal",
        on_click=navigate_to, args=(None,)
    )



# Ejecutar la aplicación
if __name__ == "__main__":
    if st.session_state.selected_option == None:
        main_menu()
    elif st.session_state.selected_option == 1:
        see_products()
    elif st.session_state.selected_option == 2:
        see_sales()
    elif st.session_state.selected_option == 3:
        see_clients()
    else:
        test_page()