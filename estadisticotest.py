import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1️⃣ Leer los archivos Excel
ventas_2024 = pd.read_excel("./data/ventas.xlsx")
ventas_2025 = ventas_2024.copy()
num_filas = len(ventas_2024['fecha'])
# 3. Definir el rango de fechas para 2025
fecha_inicio = pd.to_datetime('2025-01-01')
fecha_fin = pd.to_datetime('2025-12-31')
rango_dias = (fecha_fin - fecha_inicio).days

# 4. Generar fechas aleatorias
# Creamos una serie de días aleatorios dentro del rango 2025
dias_aleatorios = np.random.randint(0, rango_dias + 1, size=num_filas)

# Sumamos los días aleatorios a la fecha de inicio para obtener las fechas finales
fechas_aleatorias_2025 = fecha_inicio + pd.to_timedelta(dias_aleatorios, unit='D')

# 5. Reemplazar la columna 'Fecha' con las nuevas fechas aleatorias de 2025
ventas_2025['fecha'] = fechas_aleatorias_2025

# 6. Mostrar el resultado (las primeras 5 filas)
print("\nDataFrame con fechas aleatorias de 2025 reemplazadas:")
print(ventas_2025.head())

# OPCIONAL: Guardar el resultado en un nuevo archivo Excel
# df.to_excel("ventas_2025_aleatorias.xlsx", index=False)

# 2️⃣ Convertir la columna 'fecha' a tipo datetime
ventas_2024["fecha"] = pd.to_datetime(ventas_2024["fecha"])
ventas_2025["fecha"] = pd.to_datetime(ventas_2025["fecha"])

# 3️⃣ Extraer el mes de la fecha
ventas_2024["mes"] = ventas_2024["fecha"].dt.month
ventas_2025["mes"] = ventas_2025["fecha"].dt.month

# 4️⃣ Agrupar por mes y contar ventas (o sumar montos si tienes una columna de totales)
ventas_2024_mes = ventas_2024.groupby("mes").size()
ventas_2025_mes = ventas_2025.groupby("mes").size()

# 5️⃣ Alinear ambos años para asegurar que todos los meses estén presentes
meses = range(1, 13)
ventas_2024_mes = ventas_2024_mes.reindex(meses, fill_value=0)
ventas_2025_mes = ventas_2025_mes.reindex(meses, fill_value=0)

# 6️⃣ Preparar datos para el gráfico
categorias = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
              'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
ventas_2024 = ventas_2024_mes.values
ventas_2025 = ventas_2025_mes.values

x = np.arange(len(categorias))  # posiciones para cada categoría
width = 0.35  # ancho de cada barra

# 7️⃣ Crear el gráfico
plt.figure(figsize=(10, 6))
plt.bar(x - width/2, ventas_2024, width=width, label='2024', color='cornflowerblue')
plt.bar(x + width/2, ventas_2025, width=width, label='2025', color='salmon')

# 8️⃣ Personalizar
plt.title("Comparación de Ventas 2024 vs 2025")
plt.xlabel("Mes")
plt.ylabel("Número de Ventas")
plt.xticks(x, categorias)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()