import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
import os 
# --- 0. Configuración y Carga de Datos --- 
# Nombre del archivo de entrada 
file_name = './data/df_unified_clean.csv' 
if not os.path.exists(file_name): 
    print(f"Error: No se encontró el archivo '{file_name}'.") 
    print("Asegúrate de que el archivo CSV esté en la misma carpeta que este script.") 
else: 
    print(f"Cargando datos desde '{file_name}'...") 
    df = pd.read_csv(file_name) 
    # Conversión crucial de tipos de datos 
    try: 
        df['fecha_venta'] = pd.to_datetime(df['fecha_venta']) 
        df['fecha_alta_cliente'] = pd.to_datetime(df['fecha_alta_cliente']) 
        print("Columnas de fecha convertidas a datetime.") 
    except Exception as e: 
        print(f"Advertencia: No se pudieron convertir las columnas de fecha. {e}") 
print("\n--- Iniciando generación de gráficos ---") 
# --- 1. Gráfico Numérico vs. Numérico (Heatmap de Correlación) --- 
print("Generando Gráfico 1: Mapa de Calor de Correlación...") 
numeric_cols = ['cantidad', 'precio_unitario', 'importe'] 
corr_matrix = df[numeric_cols].corr() 
plt.figure(figsize=(8, 6)) 
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='viridis', cbar=True, 
annot_kws={"size": 12}) 
plt.title('Mapa de Calor de Correlación\n(Numérico vs. Numérico)', fontsize=16) 
plt.xticks(rotation=45, ha='right', fontsize=10) 
plt.yticks(rotation=0, fontsize=10) 
plt.tight_layout() 
plt.savefig('correlacion_numerica.png') 
plt.clf() # Limpiar la figura actual 

# --- 2. Gráfico Categórico vs. Numérico (Barras: Ventas por Categoría) --- 
print("Generando Gráfico 2: Ingresos Totales por Categoría...") 
ventas_por_categoria = df.groupby('categoria')['importe'].sum().sort_values(ascending=False) 
plt.figure(figsize=(10, 7)) 
colors_cat = sns.color_palette('viridis', len(ventas_por_categoria)) 
ventas_por_categoria.plot(kind='bar', color=colors_cat) 
plt.title('Ingresos Totales por Categoría\n(Categórico vs. Numérico)', fontsize=16) 
plt.ylabel('Ingresos Totales (Importe)', fontsize=12) 
plt.xlabel('Categoría', fontsize=12) 
plt.xticks(rotation=45, ha='right', fontsize=10) 
plt.grid(axis='y', linestyle='--', alpha=0.7) 
plt.tight_layout() 
plt.savefig('ventas_por_categoria.png') 
plt.clf() 
# --- 3. Gráfico Categórico vs. Numérico (Barras: Ventas por Ciudad) --- 
print("Generando Gráfico 3: Ingresos Totales por Ciudad...") 
ventas_por_ciudad = df.groupby('ciudad')['importe'].sum().sort_values(ascending=False) 
plt.figure(figsize=(10, 7)) 
colors_city = sns.color_palette('plasma', len(ventas_por_ciudad)) 
ventas_por_ciudad.plot(kind='bar', color=colors_city) 
plt.title('Ingresos Totales por Ciudad\n(Categórico vs. Numérico)', fontsize=16) 
plt.ylabel('Ingresos Totales (Importe)', fontsize=12) 
plt.xlabel('Ciudad', fontsize=12) 
plt.xticks(rotation=45, ha='right', fontsize=10) 
plt.grid(axis='y', linestyle='--', alpha=0.7) 
plt.tight_layout() 
plt.savefig('ventas_por_ciudad.png') 
plt.clf() 
# --- 4. Gráfico Categórico vs. Numérico (Boxplot: Distribución de Precios) --- 
print("Generando Gráfico 4: Distribución de Precios por Categoría...") 
plt.figure(figsize=(10, 7)) 
sns.boxplot(x='categoria', y='precio_unitario', data=df, palette='viridis') 
plt.title('Distribución de Precios Unitarios por Categoría', fontsize=16) 
plt.ylabel('Precio Unitario', fontsize=12) 
plt.xlabel('Categoría', fontsize=12) 
plt.xticks(rotation=45, ha='right', fontsize=10) 
plt.grid(axis='y', linestyle='--', alpha=0.7) 
plt.tight_layout() 
plt.savefig('distribucion_precios_categoria.png') 
plt.clf() 
# --- 5. Gráfico Categórico vs. Categórico (Heatmap: Categoría vs. Medio de Pago) --- 
print("Generando Gráfico 5: Relación entre Categoría y Medio de Pago...") 
contingency_table = pd.crosstab(df['categoria'], df['medio_pago']) 
plt.figure(figsize=(10, 7)) 
sns.heatmap(contingency_table, annot=True, fmt='d', cmap='YlGnBu', 
cbar=True, annot_kws={"size": 12}) 
plt.title('Frecuencia de Medio de Pago por Categoría\n(Categórico vs. Categórico)', fontsize=16) 
plt.ylabel('Categoría', fontsize=12) 
plt.xlabel('Medio de Pago', fontsize=12) 
plt.yticks(rotation=0, fontsize=10) 
plt.tight_layout() 
plt.savefig('categoria_vs_mediopago_heatmap.png') 
plt.clf() 
# --- 6. Gráfico Serie Temporal (Líneas: Evolución de Ventas) --- 
print("Generando Gráfico 6: Evolución de Ingresos Totales (Series Temporales)...") 
# Asegurarse de que fecha_venta es el índice para remuestrear 
df_time = df.set_index('fecha_venta') 
# Remuestrear por mes ('M') y sumar los importes 
ventas_mensuales = df_time['importe'].resample('M').sum() 
plt.figure(figsize=(12, 7)) 
ventas_mensuales.plot(kind='line', marker='o', linestyle='-', color='dodgerblue') 
plt.title('Ingresos Totales por Mes\n(Serie Temporal)', fontsize=16) 
plt.ylabel('Ingresos Totales (Importe)', fontsize=12) 
plt.xlabel('Mes', fontsize=12) 
plt.grid(True, linestyle='--', alpha=0.7) 
plt.tight_layout() 
plt.savefig('evolucion_ventas_mensuales.png') 
plt.clf() 
print("\n--- ¡Análisis completado! ---") 
print(f"Se generaron 6 archivos .png en la carpeta: {os.getcwd()}")