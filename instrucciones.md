# Instructivo de prompts para Copilot

## Tienda Aurelion — Instrucciones Generales

Este archivo describe las instrucciones y ayudas utilizadas para construir la aplicación Streamlit del proyecto Tienda Aurelion, con funciones de navegación, carga de datos y visualización de documentación interactiva.

🧭 1. Estructura general del programa

- Crea un archivo principal programa.py con la estructura básica de Streamlit.

Importa las librerías necesarias:

* streamlit
* pandas
* numpy
* sys, os
* datetime
* streamlit_mermaid

Configurar una variable de estado (st.session_state) para controlar la navegación entre secciones sin recargar toda la app.

Utiliza st.session_state para guardar la opción seleccionada y así mantener la navegación entre pantallas sin perder el contexto.”

🧩 2. Diccionario de opciones y navegación

Crea un diccionario con las opciones del menú principal, las cuales serán las siguientes:

    0. "Salir"
    1. "Ver documentación"
    2. "Ver ventas"
    3. "Ver clientes"
    4. "Ver productos"

Define la función navigate_to(option) para actualizar st.session_state.selected_option.

Cada botón del menú llama a esta función con un número asociado.

“Puedes asignar cada número del menú a una función y usar una estructura if/elif al final del programa para ejecutar la vista correspondiente.”

🏠 3. Menú principal (main_menu)

- Muestra título, descripción del equipo y botones con st.button().

- Cada botón cambia de vista según la opción seleccionada.

- Utiliza use_container_width=True para que los botones ocupen todo el ancho y se vean consistentes.

📦 4. Vista de productos (see_products)

- Carga datos desde productos_corregidos.xlsx.

- Usa st.selectbox() para seleccionar la categoría.

- Filtra el DataFrame según la categoría elegida.

- Muestra los datos en un st.dataframe().

- Para evitar confusión, elimina la columna original de categoría antes de mostrar los datos corregidos.

👥 5. Vista de clientes (see_clients)

- Carga clientes.xlsx y calcular la antigüedad con:

    - clientes["antiguedad"] = datetime.now() - clientes["fecha_alta"]

    - Usar st.multiselect() para filtrar por ciudad.

    - Muestra los clientes filtrados con st.dataframe().

- Puedes usar datetime.now() para calcular automáticamente la antigüedad en días desde la fecha de alta.

💳 6. Vista de ventas (see_sales)

- Carga ventas.xlsx, detalle_ventas.xlsx y clientes.xlsx.

- Combina los tres dataframes con merge() para formar un DataFrame completo.

- Filtra por ciudad, medio de pago y ID de venta.

- Muestra el resultado filtrado en una tabla.

- Usa np.insert() para agregar la opción ‘Todos los medios de pago’ al inicio del selectbox.

📚 7. Documentación interactiva (see_documentation)

- Lee el archivo documentación.md.

- Separa las secciones por los títulos “##”.

- Muestra una barra lateral con:

    - Navegación por secciones.

    - Buscador de texto.

    - Estadísticas (número de secciones y caracteres totales).

- “Divide el contenido del Markdown con split('\n## ') para permitir navegación por secciones.”

🔁 8. Diagrama Mermaid (streamlit_mermaid)

- Usar el componente streamlit_mermaid para mostrar un diagrama de flujo del funcionamiento del programa.

- Mostrar el diagrama solo si se cumple la condición de que la sección seleccionada sea la de ‘Información, pasos, diagrama de flujo y pseudocódigo del programa’.

🕹️ 9. Control de navegación entre secciones de la documentación

- Agregar tres columnas con botones para:

    - Sección anterior.

    - Volver al menú principal.

    - Sección siguiente.

- Puedes usar st.columns(3) para distribuir los botones de navegación horizontalmente.

💾 10. Ejecución principal

- Usar un bloque if _name_ == "_main_": para ejecutar la app.

- Según st.session_state.selected_option, mostrar la vista correspondiente.

- El valor None representa volver al menú principal, y 0 puede usarse para salir.

🧠 11. Buenas prácticas sugeridas

- Encapsular cada pantalla en una función.

- Evitar recargar datos innecesariamente.

- Usar st.container() para agrupar contenido.

- Mantener nombres descriptivos en variables y funciones.