import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# 1. Cargar datos
df = pd.read_csv('./data/df_expanded.csv')
df['fecha_venta'] = pd.to_datetime(df['fecha_venta'])

# 2. Agregación Mensual
monthly_sales = df.set_index('fecha_venta').resample('ME')['importe'].sum().reset_index()
monthly_sales.columns = ['date', 'sales']

# 3. Función de Ingeniería de Características
def create_features(data, lags=[1, 2, 3, 6, 12]):
    df_feat = data.copy()
    df_feat['month'] = df_feat['date'].dt.month
    df_feat['year'] = df_feat['date'].dt.year
    # Lags y media móvil
    for lag in lags:
        df_feat[f'lag_{lag}'] = df_feat['sales'].shift(lag)
    df_feat['rolling_mean_3'] = df_feat['sales'].shift(1).rolling(window=3).mean()
    return df_feat

df_features = create_features(monthly_sales)
df_model = df_features.dropna().reset_index(drop=True)

# 4. Entrenamiento y Predicción Recursiva
features = ['month', 'year', 'lag_1', 'lag_2', 'lag_3', 'lag_6', 'lag_12', 'rolling_mean_3']
model_full = RandomForestRegressor(n_estimators=100, random_state=42)
model_full.fit(df_model[features], df_model['sales'])

# Generar fechas futuras
last_date = df_model['date'].max()
future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), end='2025-12-31', freq='ME')

history_df = df_model[['date', 'sales']].copy()
future_predictions = []

for date in future_dates:
    # Crear fila temporal para generar features
    new_row = pd.DataFrame([{'date': date, 'sales': np.nan}])
    temp_df = pd.concat([history_df, new_row], ignore_index=True)
    temp_df_feat = create_features(temp_df)
    
    # Predecir
    current_X = temp_df_feat.iloc[[-1]][features]
    pred_sales = model_full.predict(current_X)[0]
    
    # Guardar y actualizar historia
    future_predictions.append({'date': date, 'pred_sales': pred_sales})
    history_df = pd.concat([history_df, pd.DataFrame([{'date': date, 'sales': pred_sales}])], ignore_index=True)

df_future = pd.DataFrame(future_predictions)
