import csv
import io
import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
import streamlit_mermaid as stmd
import textwrap
import matplotlib.pyplot as plt
import seaborn as sns

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
    5: "Ver análisis exploratorio",
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
        options[5], use_container_width=True, 
        on_click=navigate_to, args=(5,)
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

# Función para mostrar info de un DataFrame de forma mejorada en Streamlit.
def show_df_info(df):
    """
    Muestra una versión mejorada de df.info() en Streamlit,
    usando st.metric y un st.dataframe.
    """
    
    st.write(f"**<class 'pandas.core.frame.DataFrame'>**")
    
    # --- Métricas Resumidas (Filas, Columnas, Memoria) ---
    col1, col2, col3 = st.columns(3)
    
    # 1. Total de Filas (RangeIndex)
    col1.metric("Total de Filas (Entries)", f"{df.shape[0]}")
    
    # 2. Total de Columnas
    col2.metric("Total de Columnas", f"{df.shape[1]}")

    # 3. Uso de Memoria
    try:
        # deep=True da el uso de memoria real, especialmente para 'object'
        mem_usage = df.memory_usage(deep=True).sum()
        if mem_usage < 1024**2:
            mem_str = f"{mem_usage / 1024:.2f} KB"
        elif mem_usage < 1024**3:
            mem_str = f"{mem_usage / 1024**2:.2f} MB"
        else:
            mem_str = f"{mem_usage / 1024**3:.2f} GB"
        col3.metric("Uso de Memoria (deep)", mem_str)
    except Exception:
        # Fallback por si 'deep=True' falla en algún tipo de dato
        col3.metric("Uso de Memoria", "No disponible")

    # --- Tabla de Columnas (El núcleo de df.info()) ---
    st.markdown("**Desglose de Columnas:**")
    
    info_df = pd.DataFrame({
        "Non-Null Count": df.count(),
        "Dtype": df.dtypes
    }).reset_index().rename(columns={"index": "Columna"})
    
    # Añadir la columna '#' para replicar el formato de df.info()
    info_df.index.name = "#"
    info_df = info_df.reset_index()

    st.dataframe(info_df, use_container_width=True)
    
    # --- Resumen de Dtypes (Información extra útil) ---
    st.markdown("**Resumen de Tipos de Dato (Dtypes):**")
    st.dataframe(df.dtypes.value_counts().rename("Conteo"), use_container_width=True)

# Función para mostrar el EDA.
def see_eda():
    """Función que muestra el análisis exploratorio de datos"""
    st.title("Análisis Exploratorio de Datos (EDA) de la tienda Aurelion")
    
    # Introducción y objetivos
    st.markdown("""
    ## Objetivos del Análisis
    Este análisis exploratorio de datos tiene como objetivo principal estudiar:
    - Análisis de ventas por periodos (comparativas por mes, trimestre, año)
    - Volumen total de ventas (número de transacciones, cantidad de productos vendidos)
    - Total de ingresos o facturación
    - Número de clientes únicos
    - Ventas por ciudad
    """)
    
    # Carga de datos
    ventas = pd.read_excel("./data/ventas.xlsx")
    productos = pd.read_excel("./data/productos_corregidos.xlsx")
    clientes = pd.read_excel("./data/clientes.xlsx")
    detalle_ventas = pd.read_excel("./data/detalle_ventas.xlsx")
    
    with st.expander("ℹ️ Información sobre las fuentes de datos"):
        st.markdown("""
        Este análisis utiliza datos de cuatro fuentes principales:
        - **ventas.xlsx**: Registro de transacciones de ventas
        - **productos_corregidos.xlsx**: Catálogo de productos con categorías corregidas
        - **clientes.xlsx**: Base de datos de clientes
        - **detalle_ventas.xlsx**: Detalles específicos de cada venta
        """)

    # Secciones del EDA
    sections = [
        "1. Definición del problema",
        "2. Importación e inspección inicial de los datos",
        "3. Limpieza y transformación de los datos",
        "4. Tratamiento de datos atípicos",
        "5. Análisis univariado",
        "6. Análisis bivariado",
        "7. Conclusiones"
    ]
    # Barra lateral de navegación (similar a see_documentation)
    with st.sidebar:
        st.header("📊 Navegación EDA")
        # Campo de búsqueda para el contenido del EDA
        search_term = st.text_input("🔍 Buscar en el EDA", "")
        # Radio para seleccionar secciones (apariencia similar a see_documentation)
        selected_section = st.radio("Secciones:", sections)
        st.markdown("---")
        st.markdown("### 📌 Estadísticas")
        st.markdown(f"- **Secciones totales:** {len(sections)}")

    # Contenedor principal (paralelo a see_documentation)
    main_container = st.container()

    # Mostrar aviso si existe término de búsqueda
    if search_term:
        st.info(f"🔍 Mostrando resultados para: '{search_term}'")

    if selected_section == "1. Definición del problema":
        st.header("1️⃣ Definición del problema")
        st.markdown("""
            Objetivo: Análisis de ventas por periodos (comparativas por mes, trimestre, año), 
            por volumen total de ventas (número de transacciones, cantidad de productos vendidos),
            total de ingresos o facturación, número de clientes únicos, ventas por género.
        """)

    elif selected_section == "2. Importación e inspección inicial de los datos":
        st.header("2️⃣ Importación e inspección inicial de los datos")

        st.subheader("Importación de librerías y carga de datos")

        code_importation = """
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    ventas = pd.read_excel("./data/ventas.xlsx")
    productos = pd.read_excel("./data/productos_corregidos.xlsx")
    clientes = pd.read_excel("./data/clientes.xlsx")
    detalle_ventas = pd.read_excel("./data/detalle_ventas.xlsx")
        """
        st.code(code_importation, language='python')

        st.subheader("Inspección inicial de los datos")
        #--------------------------------------------------------------------------------------------------
        st.markdown("""
            #### Inspección de la tabla "detalle_ventas"
        """)
        st.dataframe(detalle_ventas.head(5))
        show_df_info(detalle_ventas)
        st.write(f"Shape of detalle_ventas: {detalle_ventas.shape}")
        st.divider()

        #--------------------------------------------------------------------------------------------------
        st.markdown("""
            #### Inspección de la tabla "ventas"
        """)
        st.dataframe(ventas.head(5))
        show_df_info(ventas)
        st.write(f"Shape of ventas: {ventas.shape}")
        st.divider()
        
        #--------------------------------------------------------------------------------------------------
        st.markdown("""
            #### Inspección de la tabla "productos"
        """)
        st.dataframe(productos.head(5))
        show_df_info(productos)
        st.write(f"Shape of productos: {productos.shape}")
        st.divider()
        
        #--------------------------------------------------------------------------------------------------
        st.markdown("""
            #### Inspección de la tabla "clientes"
        """)
        st.dataframe(clientes.head(5))
        show_df_info(clientes)
        st.write(f"Shape of clientes: {clientes.shape}")
        st.divider()
        
        #--------------------------------------------------------------------------------------------------
        st.subheader("Integración de datos")
        st.markdown("""
            Con base en la inspección inicial de los datos, hemos concluido que es posible la unificación de los 4 dataframes bajo las siguientes premisas:
            * Unir ventas y detalle_ventas en id_venta.
            * Unir productos y detalle_ventas en id_producto.
            * Unir clientes y ventas en id_cliente.
            A continuación se muestra la unificación con base en nuestras observaciones:
        """)
        
        code_integration = """
    df_unified = ventas.merge(detalle_ventas, on="id_venta", suffixes=("_ventas", "_dventas"))
    df_unified = df_unified.merge(productos, on="id_producto", suffixes=("_dventas", "_producto"))
    df_unified = df_unified.merge(clientes, on="id_cliente", suffixes=("_ventas", "_cliente"))

    df_unified.head()
        """
        st.code(code_integration, language="python")

        df_unified = ventas.merge(detalle_ventas, on="id_venta", suffixes=("_ventas", "_dventas"))
        df_unified = df_unified.merge(productos, on="id_producto", suffixes=("_dventas", "_producto"))
        df_unified = df_unified.merge(clientes, on="id_cliente", suffixes=("_ventas", "_cliente"))

        df_unified.head()
        
        st.dataframe(df_unified.head())
        
        st.markdown("Podemos observar más a detalle los nombres de las columnas para eliminar aquellas que estén duplicadas.")
        show_df_info(df_unified)
        st.write(f"Shape of df_unified: {df_unified.shape}")

        st.markdown("""
            Nótese que son 19 columnas en total y de ellas, se tienen duplicados de 
            **nombre_cliente**, **email**, **nombre_producto** y **precio_unitario**. 
            Procederemos a remover los duplicados.
        """)

        code_delete_duplicates = """
    df_unified = df_unified.T.drop_duplicates().T
    df_unified.info()
    print(f"Shape of df_unified: {df_unified.shape}")
        """
        st.code(code_delete_duplicates, language="python")
        df_unified = df_unified.T.drop_duplicates().T
        show_df_info(df_unified)
        st.write(f"Shape of df_unified: {df_unified.shape}")

        st.markdown("""
            Ahora tenemos 15 columnas. Nótese también que al usar la transpuesta para eliminar 
            columnas duplicadas, se han cambiado todos los tipos de datos a "object". 
            Esto se corregirá en la siguiente estapa. Mientras procederemos a renombrar 
            aquellas columnas que no fueron eliminadas.
        """)

        code_rename = """
    df_unified = df_unified.T.drop_duplicates().T
    df_unified.info()
    print(f"Shape of df_unified: {df_unified.shape}")
        """
        st.code(code_rename, language="python")

        df_unified = df_unified.rename(
            columns={
                "nombre_cliente_ventas": "nombre_cliente",
                "email_ventas": "email",
                "nombre_producto_dventas": "nombre_producto",
                "precio_unitario_dventas": "precio_unitario",
            }
        )
        show_df_info(df_unified)

        #--------------------------------------------------------------------------------------------------
        st.subheader("Cálculo de estadísticas descriptivas básicas")
        df_description = df_unified.describe(include='all')
        st.dataframe(df_description)

    elif selected_section == "3. Limpieza y transformación de los datos":
        #Importar el DataFrame unificado no limpio.
        df_unified = pd.read_csv("./data/df_unified_not_clean.csv")

        st.header("3️⃣ Limpieza y transformación de los datos")
        st.subheader("Corrección de tipos de datos")
    
        st.markdown("""
        Sabemos que en el proceso de integración de datos, los tipos de datos de las 
        columnas del dataframe fueron cambiadas, por tanto, procederemos a esta 
        corrección. Primero visualizaremos nuevamente nuestros datos.
        """)
        
        st.code("df_unified.head(5)", language="python")
        st.dataframe(df_unified.head(5))
        
        # ----------------------------------------------------------------------
        st.markdown("Procederemos a la correción del tipo utilizando \"astype\":")
        
        code_astype = """
    df_unified = df_unified.astype(
        {
            "id_venta": "int",
            "fecha": "datetime64[ns]",
            "id_cliente": "int",
            "nombre_cliente": "string",
            "email": "string",
            "medio_pago": "string",
            "id_producto": "int",
            "nombre_producto": "string",
            "cantidad": "int",
            "precio_unitario": "float",
            "importe": "float",
            "categoria": "string",
            "categoria_corregida": "string",
            "ciudad": "string",
            "fecha_alta": "datetime64[ns]"
        }
    )
    """
        # Limpiamos el código de caracteres extraños (espacios 'no-breaking')
        st.code(code_astype.replace('\u00a0', ' '), language="python")
        
        # --- Ejecución del código ---
        try:
            df_unified = df_unified.astype(
                {
                    "id_venta": "int",
                    "fecha": "datetime64[ns]",
                    "id_cliente": "int",
                    "nombre_cliente": "string",
                    "email": "string",
                    "medio_pago": "string",
                    "id_producto": "int",
                    "nombre_producto": "string",
                    "cantidad": "int",
                    "precio_unitario": "float",
                    "importe": "float",
                    "categoria": "string",
                    "categoria_corregida": "string",
                    "ciudad": "string",
                    "fecha_alta": "datetime64[ns]"
                }
            )
            st.success("Tipos de datos corregidos exitosamente.")
        except Exception as e:
            st.error(f"Error al convertir tipos de datos: {e}")
            st.warning("El DataFrame puede estar en un estado inconsistente. "
                    "Revisa los datos de origen o el código 'astype'.")
            return None # Detiene la ejecución si la conversión falla
        
        # ----------------------------------------------------------------------
        st.markdown("Vamos a comprobar los cambios con dtypes:")
        
        st.code("df_unified.dtypes", language="python")
        
        # --- Ejecución del código ---
        # Convertimos la serie de dtypes a un DataFrame para mostrarlo bien
        dtypes_df = df_unified.dtypes.reset_index().rename(
            columns={'index': 'Columna', 0: 'Dtype'}
        )
        st.dataframe(dtypes_df, use_container_width=True)

        # ----------------------------------------------------------------------
        st.subheader("Tratamiento de datos ausentes")
        # ----------------------------------------------------------------------
        
        st.markdown("""
        Verificaremos si tenemos datos nulos en nuestro dataframe y la cantidad 
        existente por columna.
        """)
        
        code_nulls = """
    # Tratamiento de datos ausentes
    print("Valores nulos por columna:")
    print(df_unified.isna().sum())
    """
        st.code(code_nulls, language="python")

        # --- Ejecución del código ---
        st.markdown("**Valores nulos por columna:**")
        null_counts = df_unified.isna().sum().reset_index().rename(
            columns={'index': 'Columna', 0: 'Conteo Nulos'}
        )
        st.dataframe(null_counts, use_container_width=True)

        st.markdown("Dado que no hay valores nulos en el dataframe, procederemos al siguiente paso.")

        # ----------------------------------------------------------------------
        st.subheader("Tratamiento de inconsistencias de formato")
        # ----------------------------------------------------------------------
        
        st.markdown("Primero, echaremos un vistazo nuevamente al dataframe.")
        
        st.code("df_unified.tail(5)", language="python")
        
        # --- Ejecución del código ---
        st.dataframe(df_unified.tail(5))
        
        # ----------------------------------------------------------------------
        st.markdown("""
        A simple vista los datos se alinean con lo que buscamos, incluyendo las fechas 
        en el formato internacional ISO 8601. Por tanto, solo procederemos a cambiar 
        el nombre de la columna "fecha" a "fecha_venta" para evitar confusiones con 
        "fecha_alta", y a "fecha_alta" le añadiremos el sufijo "cliente" para tener 
        un mejor descriptor de la columna.
        """)
        
        code_rename_1 = """
    df_unified = df_unified.rename(
        columns={
            "fecha": "fecha_venta",
            "fecha_alta": "fecha_alta_cliente"
        }
    )
    df_unified.info()
    """
        st.code(code_rename_1.replace('\u00a0', ' '), language="python")
        
        # --- Ejecución del código ---
        df_unified = df_unified.rename(
            columns={
                "fecha": "fecha_venta",
                "fecha_alta": "fecha_alta_cliente"
            }
        )
        # Usamos la función de ayuda que creamos en el paso anterior
        show_df_info(df_unified)

        # ----------------------------------------------------------------------
        st.markdown("""
        De igual forma, procederemos a eliminar "categoría" y renombrar 
        "categoría_corregida", dado el proceso que se le aplicó en el sprint 1.
        """)
        
        code_drop_cat = """
    df_unified = df_unified.drop(columns=["categoria"])
    df_unified = df_unified.rename(columns={"categoria_corregida": "categoria"})
    df_unified.info()
    """
        st.code(code_drop_cat, language="python")
        
        # --- Ejecución del código ---
        df_unified = df_unified.drop(columns=["categoria"])
        df_unified = df_unified.rename(columns={"categoria_corregida": "categoria"})
        show_df_info(df_unified)

        # ----------------------------------------------------------------------
        st.subheader("Eliminación de duplicados")
        # ----------------------------------------------------------------------
        
        st.markdown("Ahora procederemos a eliminar filas duplicadas.")
        
        code_drop_dups = """
    print(f"Duplicados antes: {df_unified.duplicated().sum()}")
    df_unified = df_unified.drop_duplicates()
    print(f"Duplicados después: {df_unified.duplicated().sum()}")
    print(f"Total de filas: {df_unified.shape[0]}")
    """
        st.code(code_drop_dups, language="python")
        
        # --- Ejecución del código ---
        dups_antes = df_unified.duplicated().sum()
        st.write(f"Duplicados antes: **{dups_antes}**")
        
        df_unified = df_unified.drop_duplicates()
        
        dups_despues = df_unified.duplicated().sum()
        st.write(f"Duplicados después: **{dups_despues}**")
        st.write(f"Total de filas: **{df_unified.shape[0]}**")
        
        st.markdown("Se puede observar que no teníamos duplicados en el dataframe.")

    elif selected_section == "4. Tratamiento de datos atípicos":
        df_unified = pd.read_csv("./data/df_unified_not_clean.csv")
        st.header("4️⃣ Tratamiento de datos atípicos")
        
        st.markdown("""
        Dada la naturaleza de nuestros datos, las columnas de tipo string y datetime serán descartadas 
        para este paso, pues solo son indicios de la variabilidad de nuestros datos y representación 
        de la frecuencia de compra de un cliente. De igual forma, las columnas que corresponden a id's 
        serán descartadas. Solo consideraremos las siguientes columnas para el análisis:
        * cantidad
        * precio_unitario      
        * importe
        """)
        
        # Análisis de outliers
        columnas_analisis = ["cantidad", "precio_unitario", "importe"]
        for col in columnas_analisis:
            Q1 = df_unified[col].quantile(0.25)
            Q3 = df_unified[col].quantile(0.75)
            IQR = Q3 - Q1
            limite_inferior = Q1 - 1.5 * IQR
            limite_superior = Q3 + 1.5 * IQR
            outliers = df_unified[(df_unified[col] < limite_inferior) | (df_unified[col] > limite_superior)]
            
            st.subheader(f"Análisis de outliers en {col}")
            st.write(f"Número de outliers: {outliers.shape[0]}")
            
            # Crear boxplot
            fig, ax = plt.subplots(figsize=(8,2))
            sns.boxplot(x=df_unified[col])
            plt.title(f"Boxplot de {col}")
            st.pyplot(fig)
            plt.close()
        
        st.markdown("""Nótamos que la única columa con Outliers es la de "importe". Vamos a realizar un análisis más al respecto.""")
        st.dataframe(df_unified[df_unified["importe"] > 20000])
        
        st.markdown("""
        Dado lo anterior, podemos concluir que el hecho de que el valor de importe de los Outliers 
        sea alto es consecuencia directa de la cantidad de productos comprados por el cliente, y que 
        todos estos valores son resultado de la multiplicación de las columnas "precio_unitario" y 
        "cantidad". Por tanto, los Outliers no son ningún error y vale la pena preservarlos para los 
        análisis posteriores.
        """)

        st.markdown("""
        Por último, obtendremos nuevamente las estadísticas descriptivas.
        """)

        st.dataframe(df_unified.describe(include='all'))

        st.markdown("""
        Puede descargarse el DataFrame limpio y listo para análisis posteriores con el siguiente botón:
        """)
        st.download_button(
            label="Descargar DataFrame limpio",
            data="./data/df_unified_clean.csv",
            file_name="" \
            "df_unified_clean.csv",
            mime="text/csv",
            icon=":material/download:",
        )

    elif selected_section == "5. Análisis univariado":
        df_unified = pd.read_csv("./data/df_unified_clean.csv")
        st.header("5️⃣ Análisis univariado")
        st.markdown("""
        Esta sección analiza el comportamiento de los productos en el mercado,
        identificando los más populares y las categorías más exitosas.
        """)
        
        
    elif selected_section == "6. Análisis bivariado":
        df_unified = pd.read_csv("./data/df_unified_clean.csv")
        st.header("6️⃣ Análisis bivariado (asociaciones y correlaciones)")
        
        # Correlación entre variables numéricas
        numeric_cols = ['cantidad', 'precio_unitario', 'importe']
        corr_matrix = df_unified[numeric_cols].corr()
        
        st.subheader("📊 Mapa de Calor de Correlación")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='viridis',
                   cbar=True, annot_kws={"size": 12})
        plt.title('Mapa de Calor de Correlación\n(Numérico vs. Numérico)', fontsize=16)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(rotation=0, fontsize=10)
        st.pyplot(fig)
        plt.close()
        
        st.markdown("""
        * **Hallazgo Principal**: Existe una correlación positiva fuerte (r = 0.81) entre cantidad e importe.
        * **Hallazgo Secundario**: La correlación entre precio_unitario e importe es moderada (r = 0.44).
        * **Hallazgo Nulo**: No existe correlación (r = -0.06) entre el precio_unitario y la cantidad comprada.
        """)
        
        # Ingresos por Categoría
        st.subheader("📊 Ingresos Totales por Categoría")
        ventas_por_categoria = df_unified.groupby('categoria')['importe'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 7))
        colors_cat = sns.color_palette('viridis', len(ventas_por_categoria))
        ventas_por_categoria.plot(kind='bar', color=colors_cat)
        plt.title('Ingresos Totales por Categoría', fontsize=16)
        plt.ylabel('Ingresos Totales (Importe)', fontsize=12)
        plt.xlabel('Categoría', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
        plt.close()
        
        # Ingresos por Ciudad
        st.subheader("📊 Ingresos Totales por Ciudad")
        ventas_por_ciudad = df_unified.groupby('ciudad')['importe'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 7))
        colors_city = sns.color_palette('plasma', len(ventas_por_ciudad))
        ventas_por_ciudad.plot(kind='bar', color=colors_city)
        plt.title('Ingresos Totales por Ciudad', fontsize=16)
        plt.ylabel('Ingresos Totales (Importe)', fontsize=12)
        plt.xlabel('Ciudad', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
        plt.close()
        
        # Distribución de Precios por Categoría
        st.subheader("📊 Distribución de Precios por Categoría")
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.boxplot(x='categoria', y='precio_unitario', data=df_unified, palette='viridis')
        plt.title('Distribución de Precios Unitarios por Categoría', fontsize=16)
        plt.ylabel('Precio Unitario', fontsize=12)
        plt.xlabel('Categoría', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
        plt.close()
        
        # Relación entre Categoría y Medio de Pago
        st.subheader("📊 Relación entre Categoría y Medio de Pago")
        contingency_table = pd.crosstab(df_unified['categoria'], df_unified['medio_pago'])
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.heatmap(contingency_table, annot=True, fmt='d', cmap='YlGnBu',
                   cbar=True, annot_kws={"size": 12})
        plt.title('Frecuencia de Medio de Pago por Categoría', fontsize=16)
        plt.ylabel('Categoría', fontsize=12)
        plt.xlabel('Medio de Pago', fontsize=12)
        plt.yticks(rotation=0, fontsize=10)
        st.pyplot(fig)
        plt.close()

    elif selected_section == "7. Conclusiones":
        st.header("7️⃣ Conclusiones")
        
        st.markdown("""
        El análisis bivariado revela varias tendencias importantes sobre el comportamiento 
        de las ventas en la tienda Aurelion:

        1. **Impulsores de Ingresos (Correlación)**
           * El importe total de una venta está fuertemente influenciado tanto por el precio unitario (r = 0.68) 
             como por la cantidad de artículos comprados (r = 0.60)
           * Esto sugiere que tanto el precio de los artículos como el volumen de la cesta son factores clave 
             para los ingresos

        2. **Comportamiento del Cliente (Elasticidad)**
           * No existe correlación significativa (r = -0.07) entre el precio_unitario y la cantidad
           * Esto indica que los clientes de Aurelion no compran menos unidades de un producto simplemente 
             porque este sea más caro

        3. **Rendimiento por Categoría y Ciudad**
           * **Categoría**: "Alimentos" es, con diferencia, la que genera el mayor volumen de ingresos
           * **Ubicación**: "Rio Cuarto" es la ciudad que reporta el mayor volumen de ingresos, seguida 
             de "Cordoba" y "Carlos Paz"

        4. **Distribución de Precios vs. Métodos de Pago**
           * **Precios**: La categoría "Perfumería" tiene la mediana de precio más alta y la mayor dispersión
           * **Método de Pago**: El método preferido varía según la categoría y el rango de precios

        5. **Estacionalidad de las Ventas**
           * Se observa una clara tendencia ascendente desde principios de año
           * El pico de ventas se alcanza en junio
           * Hay una caída notable en julio, sugiriendo un patrón estacional
        """)
        
        

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
    elif st.session_state.selected_option == 5:
        see_eda()
    else:
        test_page()