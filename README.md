# Documentación del proyecto: Tienda Aurelion

## Tema, problema y solución

**Tema:** Análisis interactivo de ventas y clientes mediante una aplicación web.

**Problema:** La empresa necesita una forma sencilla y centralizada de visualizar la información de ventas, productos y clientes sin tener que usar múltiples hojas de Excel.

**Solución:** Desarrollo de una aplicación en Streamlit que integre las 4 bases de datos y permita consultar la información desde un panel interactivo.

## Fuente, definición, estructura, tipos y escala

**Fuente:** El origen de datos es secundario en archivos de Excel (son datos generados con fines educativos).
Generados por el profesor y el equipo los recibe como datos secundarios.

**Definición:** Las bases de datos pertenecen a una tienda llamada “Aurelion”, la información está compuesta por varias tablas con datos sobre las ventas, detalle de ventas, productos y clientes de la tienda.

**Estructura:** los datos de las 4 bases recibidas, son datos estructurados y están en formato de tabla en un archivo Excel (.xlsx). A continuación se encuentra un análisis de los datos en las tablas:

### Tabla "clientes"

| Campo             | Tipo        | Escala    |
|-------------------|-------------|-----------|
| `id_cliente`      | int         | Nominal   |
| `nombre_cliente`  | string      | Nominal   |
| `email`           | string      | Nominal   |
| `ciudad`          | string      | Nominal   |
| `fecha_alta`      | string/date | Intervalo |

### Tabla "detalle_Ventas"

| Campo             | Tipo        | Escala    |
|-------------------|-------------|-----------|
| `id_venta`       | int         | Nominal   |
| `id_producto`     | int         | Nominal   |
| `nombre_producto` | string      | Nominal   |
| `cantidad`        | int         | Razón     |
| `precio_unitario` | int         | Razón     |
| `importe`         | int         | Razón     |

### Tabla "productos"

| Campo             | Tipo        | Escala    |
|-------------------|-------------|-----------|
| `id_producto`     | int         | Nominal   |
| `nombre_producto` | string      | Nominal   |
| `categoria`       | string      | Nominal   |
| `precio_unitario` | int         | Razón     |

### Tabla "ventas"

| Campo             | Tipo        | Escala    |
|-------------------|-------------|-----------|
| `id_venta`        | int         | Nominal   |
| `fecha`           | string/date | Intervalo |
| `id_cliente`      | int         | Nominal   |
| `nombre_cliente`  | string      | Nominal   |
| `email`           | string      | Nominal   |
| `medio_pago`      | string      | Nominal   |

## Información, pasos, diagrama de flujo y pseudocódigo del programa

**Pasos principales:**

1. Cargar los archivos Excel.

2. Unificar las bases con merge() para relacionar ventas con clientes y detalle de ventas.

3. Mostrar los datos en diferentes páginas del menú (productos, ventas, clientes).

4. Permitir filtrado por ciudad, categoría o método de pago. Esto se realiza de acuerdo al botón del menú principal seleccionado.

5. Mostrar resultados con tablas interactivas.

**Pseudocódigo:**

```pseudocode
Inicio
Mostrar menú principal con botones
│
Si usuario elige “Ver productos”:
    Extraer productos.xlsx
    Mostrar lista filtrable de los productos por categoría
    Filtrar tabla de acuerdo con la selección del usuario
    Mostrar tabla filtrada
    Regresar al menú principal
│
Si usuario elige “Ver ventas”:
    Extraer ventas.xlsx, clientes.xlsx y detalle_ventas.xlsx
    Mostrar lista filtrable de las ventas por ciudad, medio de pago y ID de Venta.
    Filtrar tabla de acuerdo con las selecciones del usuario
    Mostrar tabla filtrada
    Regresar al menú principal
│
Si usuario elige “Ver clientes”:
    Extraer clientes.xlsx
    Calcular antigüedad
    Mostrar lista filtrable de los clientes por ciudad
    Filtrar tabla de acuerdo con la selección del usuario
    Mostrar tabla filtrada
    Regresar al menú principal
└─ Fin
```

**Diagrama de flujo:**

[Click aquí para ver la imagen del diagrama de flujo](https://github.com/MartinOtamendiT/Aurelion/blob/main/Aurelion_diagrama_flujo.png)

## Sugerencias y mejoras aplicadas con Copilot

* Corrección de información de la base de datos de productos.xlsx, de la variable de categorias original, agregando una columna de categoria_corregida en un nuevo archivo productos_corregidos.xlsx. En esta nueva BD están los productos clasificados correctamente como Alimentos o Limpieza.

* Generar automáticamente funciones para cada vista (see_products, see_clients, see_sales). (Sugerencia interna del equipo)

* Sugerir estructuras de selectbox, multiselect y button según el contexto. (Revisión con el equipo para seleccionar las más adecuadas)

* Autocompletar el código de extracción y modificación de datos (pd.read_excel) y el merge de DataFrames, en el caso de la pestaña de ventas.

* Mejorar la legibilidad del pseudocódigo y la navegación con st.session_state.

* Mejoras para la documentación del archivo documentación.md

* Habilitar/modificar botones de navegación de la sección de "Ver documentación".

Nota: Algunas sugerencias fueron realizadas por el asistente de autocompletado de código de Copilot.

## Configuración de entorno y ejecución del programa

En esta sección se detallan los pasos necesarios para configurar el entorno y ejecutar la aplicación web interactiva desarrollada con **Streamlit** y **Python**.

### Requisitos Previos

Asegúrate de tener instalado lo siguiente en tu sistema:

* **Python 3.11+**: La aplicación está diseñada para ejecutarse con versiones modernas de Python.
* **Pip** (administrador de paquetes de Python): Generalmente viene incluido con las instalaciones de Python.

---

### Configuración del Entorno

Sigue estos pasos para preparar tu entorno de desarrollo:

#### 1. Clonar o Descargar el Repositorio

Abre tu terminal y utiliza el siguiente comando para clonar el repositorio si estás utilizando Git:

```bash
git clone https://github.com/MartinOtamendiT/Aurelion.git
```

De lo contrario, simplemente descarga los archivos del proyecto y abre tu terminal para moverte al mismo directorio con el siguiente comando:

```bash
cd <NOMBRE_DEL_DIRECTORIO>
```

#### 2. Crear un Entorno Virtual dentro de la carpeta (Recomendado)

Es una práctica estándar aislar las dependencias del proyecto utilizando un entorno virtual. Crealo dentro del directorio del proyecto.

```bash
python -m venv .venv
```

Activa el entorno virtual de la siguiente forma:

* En Linux/macOS:

    ```bash
    source .venv/bin/activate
    ```

* En Windows:

    ```bash
    .venv\Scripts\activate
    ```

#### 3. Instalar Dependencias

Todas las bibliotecas necesarias (incluyendo Streamlit) deben instalarse con el siguiente comando y el archivo "requirements.txt":

```bash
pip install -r requirements.txt
```

### Ejecución de la aplicación

#### 1. Comando de ejecución

Asegúrate de que el entorno virtual esté activo y/o las librerías estén instaladas. Ejecuta el archivo principal de la aplicación (main.py):

```bash
streamlit run programa.py
```

#### 2. Acceso a la aplicación

Al ejecutar el comando, Streamlit iniciará un servidor web local y automáticamente abrirá la aplicación en tu navegador predeterminado.

En caso de que no se abra automáticamente, puedes acceder a ella manualmente a través de la siguiente dirección: `http://localhost:8501`

**Nota**: El puerto predeterminado de Streamlit es 8501. Si ese puerto está ocupado, Streamlit te informará de un puerto alternativo que esté utilizando.

#### 3. Detener la Ejecución

Para detener la aplicación, simplemente vuelve a la terminal donde se está ejecutando el comando streamlit run y presiona:

* Windows/Linux:

    ```bash
    Ctrl + C
    ```

* MacOs:

    ```bash
    Cmd + C
    ```

---

## Análisis exploratorio en Jupyter Notebook

El archivo `analisis_notebook.ipynb` contiene un análisis exploratorio de los datos utilizados en el proyecto. Este notebook permite realizar visualizaciones, estadísticas descriptivas y pruebas rápidas sobre los datos antes de integrarlos en la aplicación principal. Es útil para validar la calidad de los datos, explorar tendencias y probar hipótesis de manera interactiva.

Además, el notebook fue adaptado para ser integrado y visualizado directamente desde la aplicación de Streamlit, facilitando así la experiencia del usuario y permitiendo acceder tanto a la exploración como a la visualización interactiva desde un solo lugar.

---

## URL de despliegue

Puedes acceder a la aplicación de Streamlit desplegada en el siguiente enlace:

[https://aurelion-team9.streamlit.app/](https://aurelion-team9.streamlit.app/)

--

## Predicción del total de ventas (sección de Machine Learning)

### 1. Objetivo

El objetivo principal de este proyecto es predecir las ventas totales mensuales de la tienda para lo que resta del año 2024 (Julio - Diciembre) y todo el año 2025. Se busca utilizar datos históricos para proyectar la demanda futura y ayudar en la toma de decisiones.

### 2. Generación de Dataset Expandido

Para lograr un entrenamiento robusto, se expandió el dataset original (`df_unified_clean.csv`) mediante técnicas de simulación de datos (Synthetic Data Generation).

#### Justificación

El dataset original contenía solo ~340 transacciones recientes, lo cual es insuficiente para capturar estacionalidad anual o tendencias a largo plazo necesarias para un modelo de regresión de series temporales.

#### Proceso Utilizado

1. **Datos Base:** Se extrajeron los perfiles de productos (precios, categorías) y clientes existentes del archivo original.
2. **Tendencia Macroeconómica:** Se utilizó el archivo externo `ventas-totales-supermercados-2.csv` como referencia de la tendencia del mercado argentino (2017-2024). Específicamente, se usó la columna `ventas_precios_constantes` para modelar la "intensidad" o volumen de ventas mensual. Este dataset fue obtenido de una página oficial de datos del gobierno de Argentina, específicamente en los datos de ["Ventas de Supermercado"](https://datos.gob.ar/nl/dataset/sspm-ventas-supermercados).

3. **Simulación:**
    * Se generaron clientes sintéticos con perfiles realistas para complementar a los clientes reales.
    * Se crearon ~20,000 transacciones distribuidas desde Enero 2017 hasta Junio 2024.
    * La frecuencia de ventas sigue la curva de demanda macroeconómica histórica, asegurando que los picos y caídas del mercado se reflejen en los datos simulados.
    * El resultado es el archivo `df_expanded.csv`, que sirve como fuente para el entrenamiento del modelo.

### 3. Algoritmo Elegido y Justificación

Se seleccionó el algoritmo **Random Forest Regressor**.

* **Justificación:** Este modelo es robusto, maneja bien relaciones no lineales y no requiere supuestos estrictos sobre la distribución de los datos. Es eficaz para series temporales cuando se transforman en un problema de regresión supervisada mediante el uso de "lags" (retrasos) como características. Además, reduce el riesgo de sobreajuste en comparación con árboles de decisión individuales al promediar múltiples árboles.

### 4. Entradas (X) y Salida (y)

* **Salida (Target - y):** `sales` (Importe total de ventas mensuales).

* **Entradas (Features - X):**

* Variables temporales: `month` (mes), `year` (año).
* Variables de rezago (Lags): `lag_1`, `lag_2`, `lag_3`, `lag_6`, `lag_12` (Ventas de hace 1, 2, 3, 6 y 12 meses).
* Medias móviles: `rolling_mean_3` (Promedio de ventas de los últimos 3 meses).

### 5. Métricas de Evaluación

Para evaluar el desempeño del modelo en el conjunto de validación (Enero - Junio 2024), se utilizaron las siguientes métricas:

* **MAE (Mean Absolute Error):** Mide el error promedio absoluto entre las ventas predichas y las reales.
* **RMSE (Root Mean Squared Error):** Penaliza más los errores grandes, útil para detectar desviaciones significativas.
* **R² Score:** Indica qué tan bien las variables independientes explican la varianza de la variable dependiente.

### 6. Modelo ML Implementado

Se implementó un modelo `RandomForestRegressor` de la librería `scikit-learn` con los siguientes hiperparámetros base:

* `n_estimators=100`: 100 árboles de decisión.
* `random_state=42`: Para reproducibilidad.

El modelo final fue entrenado con la totalidad de los datos históricos disponibles (hasta Junio 2024) y exportado como `sales_forecasting_model.pkl`.

Puede verse el modelo puesto en producción en la sección de **Predicción de ventas** del Streamlit.

### 7. División Train/Test y Entrenamiento

Se utilizó una estrategia de validación basada en el tiempo (*Time Series Split*):

* **Conjunto de Entrenamiento (Train):** Datos desde el inicio (2018) hasta Diciembre de 2023.
* **Conjunto de Validación (Val):** Datos desde Enero 2024 hasta Junio 2024.

Tras validar el desempeño, el modelo se reentrenó con **todos** los datos disponibles para realizar las proyecciones futuras.

### 8. Predicciones y Métricas Calculadas

**Resultados de Validación (Ene-Jun 2024):**

* **MAE:** ~250,794
* **RMSE:** ~268,810
* **R² Score:** -5.54 (Nota: En periodos cortos de validación con alta volatilidad, el R² puede ser negativo, indicando que el modelo tuvo dificultades para superar una línea base simple en ese tramo específico, aunque capturó la estacionalidad general).

**Predicciones Futuras:**
Se generaron predicciones mes a mes desde Julio 2024 hasta Diciembre 2025 utilizando un enfoque recursivo (las predicciones se convierten en *inputs* para los meses siguientes).
