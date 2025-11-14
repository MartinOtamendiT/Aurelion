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
    5: "Ver análisis exploratorio de datos",
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
        ### Objetivo general.
        * Analizar el comportamiento de las ventas, clientes y productos de la tienda Aurelion durante el período enero–junio 2024 para identificar patrones, impulsores de ingresos y oportunidades de mejora operativa, comercial y estratégica mediante técnicas de análisis descriptivo y bivariado.

        ### Objetivos específicos.
        1. Identificar los principales factores que influyen en el importe total de las ventas. Evaluar la relación entre precio unitario, cantidad por ítem y el valor final de cada transacción. Cuantificar cuánto aporta cada variable a los ingresos y detectar patrones de compra.

        2. Analizar la sensibilidad del cliente ante variaciones de precio. Examinar la relación entre precio y cantidad comprada para determinar si existe elasticidad o comportamiento inelástico. Segmentar clientes según su comportamiento frente al precio.

        3. Evaluar el desempeño de las categorías de productos y su aporte a los ingresos. Comparar ingresos, precios y volumen de ventas entre las categorías “Alimentos” y “Limpieza”. Identificar productos de alta rotación y su contribución al negocio.

        4. Determinar las diferencias en ventas según la ubicación geográfica. Analizar el volumen de ventas y los ingresos generados por cada ciudad. Detectar oportunidades de crecimiento y optimización de inventario por zona.

        5. Examinar los patrones de uso de los métodos de pago. Identificar los medios de pago más utilizados por categoría y por ciudad.
        Evaluar si existen oportunidades para mejorar la eficiencia operativa o incentivar métodos digitales.

        6. Analizar la evolución temporal de las ventas y detectar patrones estacionales.
        Revisar tendencias mensuales en los ingresos y detectar picos, caídas y ciclos de demanda.
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
        # Carga de datos
        ventas = pd.read_excel("./data/ventas.xlsx")
        productos = pd.read_excel("./data/productos_corregidos.xlsx")
        clientes = pd.read_excel("./data/clientes.xlsx")
        detalle_ventas = pd.read_excel("./data/detalle_ventas.xlsx")

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
        Puede descargarse el DataFrame limpio y listo en formato CSV para análisis posteriores con el siguiente botón:
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
        Para esta etapa, dividiremos el análisis en 3 partes de acuerdo con el tipo de variable:
        * Análisis de variables numéricas.
        * Análisis de variables categóricas.
        * Análisis de variables de fechas.
        
        Las variables de identificación únicas (id_venta, id_producto y id_cliente) no las 
        tomaremos en cuenta para este análisis, dado que no son variables numéricas ni categóricas 
        con significado analítico (solo sirven para identificar).
        """)

        # ----------------------------------------------------------------------
        st.subheader("Análisis de variables numéricas")
        # Grafiación de histogramas de variables numéricas.
        for col in ["precio_unitario", "importe"]:
            st.markdown(f"#### 📈 Variable: {col}")

            # Estadísticas descriptivas
            desc = df_unified[col].describe()
            # Obtención de media y mediana.
            mean, median = desc["mean"], desc["50%"]

            # Histograma
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.histplot(df_unified[col].dropna().unique(), kde=True, ax=ax)
            ax.axvline(mean, color='r', linestyle='--', label='Media')
            ax.axvline(median, color='darkblue', linestyle='-', label='Mediana')
            ax.set_title(f"Distribución de {col}")
            plt.legend()
            st.pyplot(fig)
            st.write(f"Min: {desc['min']}, Max: {desc['max']}, Media: {desc['mean']}, Mediana: {desc['50%']}, Std: {desc['std']}\n")

            # Interpretación de sesgo.
            if mean > median:
                interpretacion = "Distribución sesgada a la derecha (valores altos poco frecuentes)."
            elif mean < median:
                interpretacion = "Distribución sesgada a la izquierda (valores bajos poco frecuentes)."
            else:
                interpretacion = "Distribución aproximadamente simétrica."
            st.write(f"{interpretacion}\n")
        
        st.markdown("""
        Dados los gráficos anteriores, hemos notado lo siguiente:
        * precio_unitario: Los precios de los productos parecen tener una distribución bimodal
            (dos picos), uno alrededor de \$1500-\$2000 y otro cerca de \$4000.

        * importe: El importe (calculado como cantidad * precio_unitario) muestra una ligera
            asimetría positiva (cola derecha), lo que es normal. La mayoría de los importes por
            ítem están por debajo de \$10,000, aunque algunos llegan hasta casi \$25,000.
        """)

        st.markdown("""
        Dado que la columna "cantidad" solo tiene 5 valores posibles, se ha tomado la decisión 
        de realizar un gráfico de barras para su análisis.
        """)
        sns.barplot(x=df_unified["cantidad"].value_counts().index, y=df_unified["cantidad"].value_counts().values)
        plt.ylabel("Frecuencia")
        plt.xlabel("Cantidad")
        plt.title("Gráfico de barras de la cantidad de productos por venta")
        st.pyplot(plt)
        st.write("""
        Se puede observar que los clientes suelen llevar entre 2 y 4 productos por ítem de venta, 
        siendo 2 la cantidad más frecuente.
        """)
        # ----------------------------------------------------------------------
        st.subheader("Análisis de variables categóricas")

        st.markdown("""Realizaremos el análisis de las columnas de \"categoria\", \"medio_pago\" 
        y \"ciudad\" para todos sus valores posibles.
        """)
        for col in ["categoria", "medio_pago", "ciudad"]:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.barplot(x=df_unified[col].value_counts().index, y=df_unified[col].value_counts().values)
            plt.ylabel("Frecuencia")
            plt.xlabel(col.capitalize())
            plt.title(f"Gráfico de barras de la variable {col}")
            st.pyplot(plt)
        st.markdown("""
        Dados los gráficos anteriores hemos notado lo siguiente:
        * categoria: Existe un claro dominio de la categoría "Alimentos", que representa 286 
                    de las 343 ventas de ítems, frente a 57 de "Limpieza".
        * medio_pago: El medio de pago más utilizado es el "efectivo" (111 transacciones), 
                    seguido de cerca por "qr" (91). Los valores de "transferencia" (72) y "tarjeta" 
                    (69) son menos comunes.
        * ciudad: Las ventas están más concentradas en "Rio Cuarto" (104 ventas), 
                    con una presencia significativa en "Alta Gracia" (65) y "Cordoba" (65).
        """)

        st.markdown("""
        Dada la alta cantidad de valores que pueden tener las columnas de nombre_cliente 
                    y nombre_producto, tomaremos solo el top 5 de cada una y el resto lo 
                    clasificaremos como "Otros".
        """)
        for col in ["nombre_cliente", "nombre_producto"]:
            # Obtiene el top 5 de valores más frecuentes.
            top = df_unified[col].value_counts().head(5)
            # Agrupa los demás valores como "Otros".
            grouped_values = df_unified[col].apply(lambda x: x if x in top.index else 'Otros')
            
            fig, ax = plt.subplots(figsize=(6, 4))
            colors = sns.color_palette('mako') 
            plt.pie(grouped_values.value_counts().values, labels=grouped_values.value_counts().index, colors=colors, autopct='%.0f%%', counterclock=False)
            plt.title(f"Gráfico de pastel de la variable {col}")
            st.pyplot(plt)
        st.markdown("""
        Dados los gráficos anteriores hemos notado lo siguiente:
        * nombre_cliente: "Agustina Flores" es la cliente con más compras, impactando en 
                    un 4% de las ventas. Le sigue "Olivia Gómez" con el mismo porcentaje, 
                    mientras que "Diego Diaz", "Bruno Diaz" y "Camila Ruiz" han empatado con 
                    un 3% de las ventas.
        * nombre_producto: El producto más vendido es el "Queso Rallado 150g" con un 3%, 
                    seguido por un empate de varios productos como "Salsa de Tomate", "Desodorante", 
                    "Ron" y "Lavandina" con un 2% en cada caso.
        """)

        # ----------------------------------------------------------------------
        st.subheader("Análisis de variables de fechas")

        st.markdown("""
        Realizaremos gráficos de líneas para analizar el comportamiento de las variables de fecha.
        """)
        for col in ["fecha_venta", "fecha_alta_cliente"]:
            st.markdown(f"#### 📈 Variable: {col}")
            df_fecha = pd.to_datetime(df_unified[col].dropna())
            if df_fecha.empty:
                print(f"⚠️ No hay datos válidos de fecha en {col}.\n")
                continue

            df_mes = df_fecha.dt.to_period("M").value_counts().sort_index()
            st.write(f"Fechas válidas: {len(df_fecha)} registros.")

            # Línea de tiempo mensual
            fig, ax = plt.subplots(figsize=(6, 4))
            df_mes.plot(ax=ax)
            ax.set_title(f"Evolución temporal de {col}")
            ax.set_xlabel("Mes")
            ax.set_ylabel("Frecuencia")
            st.pyplot(fig)
        st.markdown("""
        Dados los gráficos anteriores hemos notado lo siguiente:
        * fecha_venta: Las ventas en el conjunto de datos cubren desde el 2 de enero de 2024 
                    hasta el 28 de junio de 2024. El gráfico muestra una alta cantidad de ventas 
                    en Enero y Mayo, donde en este último se registra el máximo de ventas. 
                    Por otro lado, se registra en Abril una gran caída de las ventas.

        * fecha_alta_cliente: Los clientes en este conjunto de datos fueron dados de alta 
                    entre el 1 de enero de 2023 y el 10 de abril de 2023. Se nota que el máximo 
                    de registros realizados fue en Enero y conforme avanzó el año 2023 la cantidad 
                    de registros disminuyó progresivamente.
        """)
        
        
    elif selected_section == "6. Análisis bivariado":
        df_unified = pd.read_csv("./data/df_unified_clean.csv")
        st.header("6️⃣ Análisis bivariado")

        st.markdown("""Empezaremos realizando la matriz de correlación de 
                    las variables numéricas. Para ello, primero haremos un filtro de estod tipos.""")
        st.code("""df_numeric = df_unified.select_dtypes(include=["int64", "float64"])""", language="python")
        df_numeric = df_unified.select_dtypes(include=["int64", "float64"])

        st.markdown("""Procedemos a calcular la matriz de correlación.""")
        corr_matrix = df_numeric.corr(method='pearson')
        st.write("📊 MATRIZ DE CORRELACIÓN (coeficientes de Pearson):\n")
        st.write(corr_matrix.round(3))

        st.markdown("""Para poder visualizar mejor los valores obtenidos, 
                    se procede a realizar un mapa de calor.""")
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap="YlGnBu", fmt=".2f", linewidths=0.5)
        plt.title("Matriz de correlación entre variables - Tienda Aurrelion")
        plt.tight_layout()
        st.pyplot(plt)
        plt.clf()

        st.markdown("""Dada la naturaleza de los datos, se realiza el análisis 
                    de la correlación entre las variables de "cantidad", 
                    "precio_unitario" e "importe".
        """)
        numeric_cols = ['cantidad', 'precio_unitario', 'importe'] 
        corr_matrix = df_unified[numeric_cols].corr() 
        plt.figure(figsize=(8, 6)) 
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='viridis', cbar=True, 
        annot_kws={"size": 12}) 
        plt.title('Mapa de Calor de Correlación', fontsize=16) 
        plt.xticks(rotation=45, ha='right', fontsize=10) 
        plt.yticks(rotation=0, fontsize=10) 
        plt.tight_layout() 
        st.pyplot(plt)
        plt.clf()
        
        st.markdown("""
        Dado el gráfico anterior, se observan los siguientes hallazgos: 
        * Existe una correlación positiva moderada ($r = 0.60$) entre cantidad e importe. 
                    Esto confirma que el volumen de artículos por transacción es el principal 
                    impulsor del ingreso total. 
        * La correlación entre precio_unitario e importe es positiva moderada ($r = 0.68$). 
                    Esto es consecuencia de la fórmula aplicada para calcular el importe 
                    (importe = precio_unitario x cantidad).
        * Existe una correlación negativa débil ($r = -0.07$) entre el precio_unitario y 
                    la cantidad comprada. Los clientes compran más unidades de productos más baratos.
        """)

        st.markdown("""Ahora se procederá a realizar un análisis del importe 
                    (ingresos totales) de acuerdo a la categoría del producto.""")
        ventas_por_categoria = df_unified.groupby('categoria')['importe'].sum().sort_values(ascending=False) 
        plt.figure(figsize=(10, 7)) 
        colors_cat = sns.color_palette('viridis', len(ventas_por_categoria)) 
        ventas_por_categoria.plot(kind='bar', color=colors_cat) 
        plt.title('Ingresos Totales por Categoría', fontsize=16) 
        plt.ylabel('Ingresos Totales (Importe)', fontsize=12) 
        plt.xlabel('Categoría', fontsize=12) 
        plt.xticks(rotation=45, ha='right', fontsize=10) 
        plt.grid(axis='y', linestyle='--', alpha=0.7) 
        plt.tight_layout() 
        st.pyplot(plt)
        plt.clf()
        st.markdown("""
        Se observa el siguiente hallazgo:
        * La categoría "Alimentos" es la que genera, con diferencia, el mayor volumen de 
                    ingresos totales para el negocio. Esto sugiere que se tiene una oportunidad 
                    de diversificación para productos de "Limpieza" con el objetivo de incrementar 
                    los ingresos de esta categoría.
        """)

        st.markdown("""Ahora se procederá a realizar un análisis de los ingresos totales por ciudad.""")
        ventas_por_ciudad = df_unified.groupby('ciudad')['importe'].sum().sort_values(ascending=False) 
        plt.figure(figsize=(10, 7)) 
        colors_city = sns.color_palette('plasma', len(ventas_por_ciudad)) 
        ventas_por_ciudad.plot(kind='bar', color=colors_city) 
        plt.title('Ingresos Totales por Ciudad\n(Categórico vs. Numérico)', fontsize=16) 
        plt.ylabel('Ingresos Totales (Importe)', fontsize=12) 
        plt.xlabel('Ciudad', fontsize=12) 
        plt.xticks(rotation=45, ha='right', fontsize=10) 
        plt.grid(axis='y', linestyle='--', alpha=0.7) 
        plt.tight_layout() 
        st.pyplot(plt)
        plt.clf()
        st.markdown("""
        De acuerdo a la información presentada en la base de datos, se observa que todas 
                    las ciudades corresponden a distintas sucursales de la tienda Aurelion 
                    en Argentina. De acuerdo con el gráfico, se tiene que:
        * "Rio Cuarto" es la ciudad que reporta el mayor volumen de ingresos totales. 
        * "Cordoba" y "Altagracia" muestran niveles de ingresos muy similares entre sí, 
                    mientras que "Mendiolaza" es la de menor rendimiento. 

        Para continuar con este análisis por ciudad, se procederá a realizar un gráfico 
                    que tomará en cuenta los medios de pago utilizados.
        """)

        # Crear tabla de contingencia: Ciudad vs Medio de Pago (suma del importe)
        tabla_ciudad_pago = pd.crosstab(df_unified['ciudad'], df_unified['medio_pago'],
                                        values=df_unified['importe'], aggfunc='sum').fillna(0)

        # Ordenar por total de ingresos en cada ciudad (descendente)
        tabla_ciudad_pago = tabla_ciudad_pago.loc[tabla_ciudad_pago.sum(axis=1).sort_values(ascending=False).index]

        # Gráfico de barras apiladas
        plt.figure(figsize=(12, 8))

        tabla_ciudad_pago.plot(
            kind='bar',
            stacked=True,
            figsize=(12, 8),
            colormap='mako'  # mantiene coherencia con tu estilo
        )

        plt.title('Ingresos por Medio de Pago en cada Ciudad', fontsize=16)
        plt.ylabel('Ingresos Totales (Importe)', fontsize=12)
        plt.xlabel('Ciudad', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.legend(title='Medio de Pago', fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        st.pyplot(plt)
        plt.clf()
        st.markdown("""
        De acuerdo con el gráfico anterior, se observa los siguiente:
        * El método de pago más común es "Efectivo" dado que a pesar de no ser el más frecuente, 
                    está presente en todas las ciudades. 
        * Adicionalmente, se observa que en las dos ciudades con mayores ingresos 
                    (Río Cuarto y Alta Gracia) el método de pago más utilizado es el "QR". 
                    Mientras que en las 2 ciudades con menor ingreso, la presencia del "QR" es 
                    prácticamente nula.
        * En todas las ciudades se observa que se utiliza "Transferencia" y "Tarjeta", 
                    pero no con tanta regularidad como los demás métodos de pago.
        * Esto coincide con el hallazgo encontrado en el análisis univariado de "método_pago", 
                    en el cual el método de pago más utilizado es "Efectivo".

        Para continuar con el análisis del medio de pago, se procederá a realizar un gráfico que 
                    lo compara con la categoría del producto.
        """)

        # Crear tabla de contingencia
        contingency_table = pd.crosstab(df_unified['categoria'], df_unified['medio_pago'])

        plt.figure(figsize=(12, 8))

        contingency_table.plot(
            kind='bar',
            stacked=True,
            figsize=(12, 8),
            colormap='mako' 
        )

        plt.title('Medio de Pago por Categoría', fontsize=16)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.xlabel('Categoría', fontsize=12)
        plt.xticks(rotation=0, fontsize=10)
        plt.legend(title='Medio de Pago', fontsize=10)
        plt.tight_layout()
        st.pyplot(plt)
        plt.clf()
        st.markdown("""
        De acuerdo con el gráfico anterior, se encontró lo siguiente. 
        * El método de pago utilizado con mayor frecuencia es el "Efectivo", seguido del "QR". 
                    Mientras que los métodos utilizados con menor frecuencia en menor proporción 
                    son "Tarjeta" y "Transferencia".
        * Se observa mucho mejor lo encontrado en el análisis univariado para "método_pago".
        """)

        st.markdown("""A continuación, se muestra la evolución de los ingresos totales por mes en el año 2024.""")
        # Asegurarse de que fecha_venta es el índice para remuestrear
        df_unified['fecha_venta'] = pd.to_datetime(df_unified['fecha_venta'])
        df_time = df_unified.set_index('fecha_venta') 
        # Remuestrear por mes ('M') y sumar los importes 
        ventas_mensuales = df_time['importe'].resample('M').sum() 
        plt.figure(figsize=(12, 7)) 
        ventas_mensuales.plot(kind='line', marker='o', linestyle='-', color='dodgerblue') 
        plt.title('Ingresos Totales por mes 2024', fontsize=16) 
        plt.ylabel('Ingresos Totales (Importe)', fontsize=12) 
        plt.xlabel('Mes', fontsize=12) 
        plt.grid(True, linestyle='--', alpha=0.7) 
        plt.tight_layout() 
        st.pyplot(plt)
        plt.clf()
        st.markdown("""Se observa una clara tendencia en el aumento de los ingresos en el mes 
                    de Enero del 2024 y una fuerte caída en Abril. Al siguiente mes (Mayo), 
                    se observa una gran recuperación de los ingresos (y el pico más alto). 
                    Esto indica una estacionalidad de los ingresos de acuerdo con una temporada 
                    alta en los meses de Enero y Mayo, y una temporada baja en Abril.
        """)
        
        st.markdown("""
        Próximamente, se realizará una predicción con los datos del año 2024 para 
        el año 2025, con la intención de comprender la estacionalidad de las ventas y 
        posibles oportunidades para incrementar los ingresos.
                    
        Para ello, por el momento se generan datos aleatorios de Enero a Diciembre para 
        el año 2025 para simular la existencia de datos de este año.
        """)
        ventas_2024 = pd.read_excel("./data/ventas.xlsx")
        ventas_2025 = ventas_2024.copy()
        num_filas = len(ventas_2024['fecha'])
        # Definir el rango de fechas para 2025
        fecha_inicio = pd.to_datetime('2025-01-01')
        fecha_fin = pd.to_datetime('2025-12-31')
        rango_dias = (fecha_fin - fecha_inicio).days

        # Generar fechas aleatorias
        # Creamos una serie de días aleatorios dentro del rango 2025
        dias_aleatorios = np.random.randint(0, rango_dias + 1, size=num_filas)

        # Sumamos los días aleatorios a la fecha de inicio para obtener las fechas finales
        fechas_aleatorias_2025 = fecha_inicio + pd.to_timedelta(dias_aleatorios, unit='D')

        # Reemplazar la columna 'Fecha' con las nuevas fechas aleatorias de 2025
        ventas_2025['fecha'] = fechas_aleatorias_2025

        # Mostrar el resultado (las primeras 5 filas)
        st.write("\nDataFrame con fechas aleatorias de 2025 reemplazadas:")
        st.write(ventas_2025.head())

        # Convertir la columna 'fecha' a tipo datetime
        ventas_2024["fecha"] = pd.to_datetime(ventas_2024["fecha"])
        ventas_2025["fecha"] = pd.to_datetime(ventas_2025["fecha"])

        # Extraer el mes de la fecha
        ventas_2024["mes"] = ventas_2024["fecha"].dt.month
        ventas_2025["mes"] = ventas_2025["fecha"].dt.month

        # Agrupar por mes y contar ventas (o sumar montos si tienes una columna de totales)
        ventas_2024_mes = ventas_2024.groupby("mes").size()
        ventas_2025_mes = ventas_2025.groupby("mes").size()

        # Alinear ambos años para asegurar que todos los meses estén presentes
        meses = range(1, 13)
        ventas_2024_mes = ventas_2024_mes.reindex(meses, fill_value=0)
        ventas_2025_mes = ventas_2025_mes.reindex(meses, fill_value=0)

        # Preparar datos para el gráfico
        categorias = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        ventas_2024 = ventas_2024_mes.values
        ventas_2025 = ventas_2025_mes.values

        x = np.arange(len(categorias))  # posiciones para cada categoría
        width = 0.35  # ancho de cada barra

        # Crear el gráfico
        plt.figure(figsize=(10, 6))
        plt.bar(x - width/2, ventas_2024, width=width, label='2024', color='darkcyan')
        plt.bar(x + width/2, ventas_2025, width=width, label='2025', color='indigo')

        # Personalizar
        plt.title("Comparación de Ventas 2024 vs 2025")
        plt.xlabel("Mes")
        plt.ylabel("Número de Ventas")
        plt.xticks(x, categorias)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(plt)


    elif selected_section == "7. Conclusiones":
        st.header("7️⃣ Conclusiones")
        
        st.markdown("""
        1. Impulsores Clave de Ingresos y Categorías.
            * Ingresos (Importe): Los ingresos totales están impulsados por una combinación de la cantidad de productos comprados ($r = 0.60$) y el precio unitario de los mismos ($r = 0.68$).
            * Dominio de Alimentos: La categoría "Alimentos" es el generador dominante de ingresos (286 ítems vendidos vs. 57 de "Limpieza"). Esto sugiere que "Alimentos" es el pilar del negocio, mientras que "Limpieza" representa una clara oportunidad de diversificación y crecimiento.

        2. Comportamiento del Cliente y Sensibilidad al Precio.
            * Sensibilidad al Precio: Se detecta una ligera sensibilidad al precio. El análisis de correlación ($r = -0.07$) indica que los clientes tienden a comprar más unidades de productos que tienen un precio unitario más bajo.
            * Volumen de Compra: El patrón de compra más habitual es llevar 2 unidades por ítem de venta, aunque el rango común se sitúa entre 2 y 4 unidades.
            * Clientes Principales: Aunque el análisis de clientes muestra una base diversificada, "Agustina Flores" y "Olivia Gómez" destacan ligeramente como las compradoras más frecuentes (ambas con un 4% del total de ítems).
            
        3. Perspectivas Geográficas y Métodos de Pago.
            * Rendimiento por Ciudad: "Rio Cuarto" es la sucursal que genera mayores ingresos totales y registra la mayor cantidad de ventas (104). "Mendiolaza" es la de menor rendimiento.
            * Patrón de Métodos de Pago: Este es uno de los hallazgos más significativos:
                * A nivel general, el "Efectivo" es el método más usado (111 transacciones), seguido de cerca por el "QR" (91).
                * Sin embargo, el "QR" es el método preferido en las dos ciudades con mayores ingresos (Río Cuarto y Alta Gracia).
                * Por el contrario, el "QR" es prácticamente inexistente en las ciudades con menor rendimiento. Esto sugiere una correlación entre la adopción de pagos digitales (QR) y un mayor volumen de ingresos por sucursal.

        4. Estacionalidad y Tendencias.
            * Estacionalidad de Ventas: El análisis de fecha_venta (Ene-Jun 2024) revela una fuerte estacionalidad. Se observan picos de ventas e ingresos en enero y mayo, con una caída notable en abril.
            * Adquisición de Clientes: La adquisición de los clientes analizados (fecha_alta_cliente) tuvo su auge en enero de 2023 y disminuyó progresivamente a lo largo de ese año.

        5. Análisis de Productos.
            * Producto Estrella: El producto individual más vendido es el "Queso Rallado 150g" (3% de los ítems).
            * Distribución de Precios: Los precios de los productos no son uniformes; muestran una distribución bimodal, sugiriendo dos grupos principales de productos (uno de menor precio, $1500-$2000, y uno de mayor precio, $4000$).
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