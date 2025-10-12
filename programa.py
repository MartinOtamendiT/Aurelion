import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
import streamlit_mermaid as stmd
import textwrap

# Inicialización del Estado de Sesión.
# Se inicializa el estado para la opción seleccionada.
if 'selected_option' not in st.session_state:
    # El valor de None será indicaivo de regresar al menú principal
    st.session_state.selected_option = None

# Diccionario de opciones. Asocia cada opción con una clave utilizada por selected_option.
options = {
    1: "Ver documentación",
    2: "Ver ventas",
    3: "Ver clientes",
    4: "Ver productos",
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
    st.markdown("Equipo sala 9: Andrea Emilia Gómez Gavilanes, Gester Danna Potosí Rujel, Francisco Alejandro Díaz Pezoa, Martin Otamendi Torres, Mauricio Andre Carpio Rosas, Kelly Lizeth Alomoto Catota.")
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
        options[4], use_container_width=True, 
        on_click=navigate_to, args=(4,)
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
    #st.button(
    #    "⬅️ Volver al Menú Principal",
    #    on_click=navigate_to, args=(None,)
    #)
    

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

def see_documentation():
    """Función que muestra la documentación del documentación.md de manera interactiva"""
    st.title("Documentación del Proyecto: Tienda Aurelion")

    # Leer el contenido del documentación.md
    with open("documentación.md", "r", encoding='utf-8') as file:
        content = file.read()
    
    # Dividir el contenido en secciones (basado en los headers ##)
    sections = content.split("\n## ")
    
    # Preparar las opciones para la navegación
    main_title = sections[0].split("\n")[0].replace("# ", "")
    section_titles = [s.split("\n")[0] for s in sections[1:]]

    # Crear una barra lateral para navegación
    with st.sidebar:
        st.header("📚 Navegación")
        
        # Añadir búsqueda en la documentación
        search_term = st.text_input("🔍 Buscar en la documentación", "")
        
        # Radio buttons para selección de sección con íconos
        selected_section = st.radio(
            "Secciones:",
            section_titles,
            format_func=lambda x: "📌 " + x if x == main_title else "📑 " + x
        )

        st.markdown("---")
        # Mostrar estadísticas de la documentación
        st.markdown("### 📊 Estadísticas")
        st.markdown(f"- **Secciones totales:** {len(section_titles)}")
        st.markdown(f"- **Caracteres totales:** {len(content)}")

    # Contenedor principal para el contenido
    main_container = st.container()
    
    with main_container:
        # Si hay término de búsqueda, resaltarlo en el contenido
        if search_term:
            st.info(f"🔍 Mostrando resultados para: '{search_term}'")

        # Mostrar el contenido de la sección seleccionada
        if selected_section == main_title:
            content_to_show = sections[0]
        else:
            content_to_show = "## " + next(section for section in sections[1:] 
                                         if section.split("\n")[0] == selected_section)

        # Si hay término de búsqueda, resaltar las coincidencias
        if search_term and search_term.strip():
            # Dividir el contenido en líneas para procesar
            lines = content_to_show.split("\n")
            filtered_lines = []
            for line in lines:
                if search_term.lower() in line.lower():
                    # Resaltar el término de búsqueda
                    highlighted = line.replace(
                        search_term,
                        f"**:red[{search_term}]**"
                    )
                    filtered_lines.append(highlighted)
                elif not search_term.strip():  # Si no hay búsqueda, mostrar todo
                    filtered_lines.append(line)
            
            if filtered_lines:
                st.markdown("\n".join(filtered_lines))
            else:
                st.warning("No se encontraron coincidencias en esta sección.")
        else:
            # Mostrar el contenido normal
            st.markdown(content_to_show)

        # Agregar elementos interactivos según el contenido
        if "```" in content_to_show:  # Si hay bloques de código
            st.info("ℹ️ Esta sección contiene ejemplos de código que puedes copiar.")
        
        if "|" in content_to_show:  # Si hay tablas
            st.info("ℹ️ Esta sección contiene tablas con información estructurada.")

        if "###" in content_to_show:  # Si hay subsecciones
            with st.expander("🔍 Ver subsecciones"):
                subsections = [line for line in content_to_show.split("\n") 
                             if line.startswith("###")]
                for subsection in subsections:
                    st.markdown(f"- {subsection.replace('### ', '')}")

        # Mostrar el diagrama solo si la sección seleccionada es la correcta
        if "Información, pasos, diagrama de flujo y pseudocódigo del programa" in selected_section.strip():
            diagram ="""
                flowchart TD
                    A([Inicio])
                    A --> B["Imprimir:<br>1.- Menú:<br>1.- Ver documentación<br>2.- Ver ventas<br>3.- Ver clientes<br>4.- Ver productos<br>0.- Salir"]
                    B --> C["Leer: opcion_usuario"]
                    C --> D{opcion_usuario}

                    %% --- Ver productos ---
                    D -->|1| E["Imprimir: 'Elegiste ver productos'"]
                    E --> F["Extraer datos de 'productos_corregidos.xlsx'"]
                    F --> G["Imprimir: 'Selecciona categoría:' + lista_categorias"]
                    G --> H["Leer: categoria_seleccionada"]

                    H --> I{categoria_seleccionada}
                    I -->|Todas las categorías| J["Filtrar tabla_productos por 'todas las categorías'"]
                    I -->|Alimentos| K["Filtrar tabla_productos por 'Alimentos'"]
                    I -->|Limpieza| L["Filtrar tabla_productos por 'Limpieza'"]

                    J --> M["Imprimir: tabla_productos[id_producto, nombre_producto, precio_unitario, categoria_corregida]"]
                    K --> M
                    L --> M
                    M --> N["Imprimir: 'Regresando al menú principal...'"]
                    N --> B

                    %% --- Ver ventas ---
                    D -->|2| O["Imprimir: 'Elegiste ver ventas'"]
                    O --> P["Extraer datos de 'ventas.xlsx'"]
                    P --> Q["Extraer datos de 'detalle_ventas.xlsx'"]
                    Q --> R["Extraer datos de 'clientes.xlsx'"]
                    R --> S["Unir tablas de ventas, detalle_ventas y clientes"]
                    S --> T["Imprimir: 'Selecciona ciudad de origen de los clientes' + lista_ciudades"]
                    T --> U["Filtrar tabla_ventas_unida por ciudad"]
                    U --> V["Imprimir: 'Selecciona el medio de pago' + lista_medios_pago"]
                    V --> W["Filtrar tabla_ventas_unida por medio_pago"]
                    W --> X["Imprimir: 'Ingresa ID de la venta:'"]
                    X --> Y["Leer: id_venta_ingresado"]
                    Y --> Z["Filtrar tabla_ventas_unida por id_venta_ingresado"]
                    Z --> ZA["Imprimir: tabla con datos de venta, cliente y producto"]
                    ZA --> ZB["Imprimir: 'Regresando al menú principal...'"]
                    ZB --> B

                    %% --- Ver clientes ---
                    D -->|3| AA["Imprimir: 'Elegiste ver clientes'"]
                    AA --> AB["Extraer datos de 'clientes.xlsx'"]
                    AB --> AC["Calcular antigüedad de los clientes"]
                    AC --> AD["Imprimir: 'Selecciona ciudad de origen' + lista_ciudades"]
                    AD --> AE["Filtrar tabla_clientes por ciudad"]
                    AE --> AF["Imprimir: tabla_clientes con id_cliente, nombre_cliente, email, fecha_alta, antigüedad"]
                    AF --> AG["Imprimir: 'Regresando al menú principal...'"]
                    AG --> B

                    %% --- Ver documentación ---
                    D -->|4| BA["Imprimir: 'Elegiste ver documentación'"]
                    BA --> BB["Cargar contenido del archivo 'documentación.md'"]
                    BB --> BC["Extraer títulos de secciones"]
                    BC --> BD["Imprimir: 'Selecciona una sección:' + lista_secciones"]
                    BD --> BE["Leer: seccion_seleccionada"]
                    BE --> BF["Mostrar contenido de la sección seleccionada"]
                    BF --> BG["Si hay subsecciones, mostrar lista de subsecciones"]
                    BG --> BH["Si es la sección correcta, mostrar diagrama de flujo"]
                    BH --> BI["Imprimir: 'Regresando al menú principal...'"]
                    BI --> B

                    %% --- Salir ---
                    D -->|0| HZ([Fin])
            """
            stmd.st_mermaid(diagram)

    st.markdown("---")
    # Botones de navegación
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if section_titles.index(selected_section) > 0:
            prev_section = section_titles[section_titles.index(selected_section) - 1]
            st.button(
                f"⬅️ {prev_section}",
                key="prev_section",
                help=f"Ir a la sección anterior: {prev_section}"
            )
    
    with col2:
        st.button(
            "⬅️ Volver al Menú Principal",
            on_click=navigate_to, args=(None,)
        )
    
    with col3:
        if section_titles.index(selected_section) < len(section_titles) - 1:
            next_section = section_titles[section_titles.index(selected_section) + 1]
            st.button(
                f"➡️ {next_section}",
                key="next_section",
                help=f"Ir a la siguiente sección: {next_section}"
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
        see_documentation()
    elif st.session_state.selected_option == 2:
        see_sales()
    elif st.session_state.selected_option == 3:
        see_clients()
    elif st.session_state.selected_option == 4:
        see_products()
    else:
        test_page()