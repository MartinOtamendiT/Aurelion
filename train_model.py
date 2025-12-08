import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt

def forecast_recursive(model, df_historical, features):
    """
    Realiza una predicción recursiva (multi-step forecast) para 18 meses.

    Args:
        model: Modelo de regresión entrenado (RandomForestRegressor).
        df_historical: DataFrame con datos históricos y features calculados (hasta Jun 2024).
        features: Lista de nombres de columnas a usar como features.

    Returns:
        DataFrame con las predicciones futuras.
    """
    # 7. Retomar el entrenamiento con TODOS los datos (modelo_full)
    X_all = df_historical[features]
    y_all = df_historical['sales']
    model_full = RandomForestRegressor(n_estimators=100, random_state=42)
    model_full.fit(X_all, y_all)
    
    # Iniciar desde el mes siguiente al último dato
    last_date = df_historical['date'].max()
    # Generar fechas futuras: Julio 2024 hasta Diciembre 2025
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), end='2025-12-31', freq='M')
    
    # Copia del historial base (solo 'date' y 'sales') para actualizar en el loop
    history_df = df_historical[['date', 'sales']].copy() 
    future_predictions = []

    for date in future_dates:
        # Añadir fila vacía temporal al historial para calcular los lags del nuevo mes
        new_row = pd.DataFrame([{'date': date, 'sales': np.nan}])
        temp_df = pd.concat([history_df, new_row], ignore_index=True)
        
        # Recalcular features (esto llena los lags de la última fila con valores del historial)
        temp_df_feat = create_features(temp_df) 
        current_X = temp_df_feat.iloc[[-1]][features]
        
        # Predecir
        pred_sales = model_full.predict(current_X)[0]
        
        # Guardar predicción
        future_predictions.append({'date': date, 'pred_sales': pred_sales})
        
        # Actualizar el historial con la predicción para el siguiente paso recursivo
        history_df = pd.concat([history_df, pd.DataFrame([{'date': date, 'sales': pred_sales}])], ignore_index=True)

    return pd.DataFrame(future_predictions)

def plot_forecast(df_historical_sales, df_future_forecast):
    """
    Grafica las ventas históricas y el pronóstico futuro.

    Args:
        df_historical_sales: DataFrame con la columna 'date' y 'sales' (datos reales).
        df_future_forecast: DataFrame con la columna 'date' y 'pred_sales' (pronóstico).
    """
    plt.figure(figsize=(14, 7))
    
    # Histórico (Datos reales)
    plt.plot(df_historical_sales['date'], df_historical_sales['sales'], 
             label='Ventas Históricas (2017 - Jun 2024)', color='dodgerblue', linewidth=2)
    
    # Pronóstico (Datos predichos)
    plt.plot(df_future_forecast['date'], df_future_forecast['pred_sales'], 
             label='Pronóstico (Jul 2024 - Dic 2025)', color='darkorange', linestyle='--', marker='o', markersize=4)
    
    # Línea divisoria entre historia y futuro
    last_historical_date = df_historical_sales['date'].max()
    plt.axvline(x=last_historical_date, color='grey', linestyle=':', linewidth=1.5, label='Inicio del Pronóstico')

    plt.title('📈 Pronóstico de Ventas Mensuales Totales (2017 - 2025)', fontsize=16)
    plt.xlabel('Fecha', fontsize=12)
    plt.ylabel('Ventas Totales ($)', fontsize=12)
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 1. Cargar y Preparar Datos
df = pd.read_csv('./data/df_expanded.csv')
df['fecha_venta'] = pd.to_datetime(df['fecha_venta'])
monthly_sales = df.set_index('fecha_venta').resample('ME')['importe'].sum().reset_index()
monthly_sales.columns = ['date', 'sales']

# 2. Función de Ingeniería de Features
def create_features(data, lags=[1, 2, 3, 6, 12]):
    df_feat = data.copy()
    df_feat['month'] = df_feat['date'].dt.month
    df_feat['year'] = df_feat['date'].dt.year
    for lag in lags:
        df_feat[f'lag_{lag}'] = df_feat['sales'].shift(lag)
    df_feat['rolling_mean_3'] = df_feat['sales'].shift(1).rolling(window=3).mean()
    return df_feat

df_features = create_features(monthly_sales)
df_model = df_features.dropna().reset_index(drop=True)

# 3. División Entrenamiento / Validación
train = df_model[df_model['date'] < '2024-01-01']
val = df_model[df_model['date'] >= '2024-01-01']

features = ['month', 'year', 'lag_1', 'lag_2', 'lag_3', 'lag_6', 'lag_12', 'rolling_mean_3']
target = 'sales'

# 4. Entrenar y Evaluar
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(train[features], train[target])

val_preds = model.predict(val[features])
print(f"Validation MAE: {mean_absolute_error(val[target], val_preds):,.2f}")
print(f"Validation RMSE: {np.sqrt(mean_squared_error(val[target], val_preds)):,.2f}")

# 5. Entrenar Modelo Final con TODOS los datos y Exportar
model_full = RandomForestRegressor(n_estimators=100, random_state=42)
model_full.fit(df_model[features], df_model[target])

# Exportar modelo
joblib.dump(model_full, 'sales_forecasting_model.pkl')
print("Modelo guardado exitosamente como 'sales_forecasting_model.pkl'")

# 🚀 Ejecución de la Predicción
df_future = forecast_recursive(model, df_model, features)
print("\n--- Predicciones (Julio 2024 - Dic 2025) ---")
print(df_future.head())
print(df_future.tail())

# Exportar Predicciones
df_future.to_csv('./data/sales_predictions_2024_2025_final.csv', index=False)
print("\nPredicciones guardadas en './data/sales_predictions_2024_2025_final.csv'")

# Visualización
plot_forecast(monthly_sales, df_future)