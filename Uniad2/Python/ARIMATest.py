import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

# Leer datos manualmente
timestamps = []
temperaturas = []

with open('temperatura.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Saltar encabezado
    for row in reader:
        timestamps.append(datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"))
        temperaturas.append(float(row[1]))

serie_temp = np.array(temperaturas)

# Función de análisis 
def analisis_arima_manual(serie, nombre):
    print(f"\nAnálisis ADF para {nombre}:")
    
    # Prueba en serie original
    result = adfuller(serie)
    print(f'[Original] Estadístico ADF: {result[0]:.3f}')
    print(f'[Original] p-valor: {result[1]:.3f}')

    
    # Primera diferenciación
    diff1 = np.diff(serie, n=1)
    result_d1 = adfuller(diff1)
    print(f'\n[1ra Diferenciación] Estadístico ADF: {result_d1[0]:.3f}')
    print(f'[1ra Diferenciación] p-valor: {result_d1[1]:.3f}')

    
    # Segunda diferenciación
    diff2 = np.diff(diff1, n=1)
    result_d2 = adfuller(diff2)
    print(f'\n[2da Diferenciación] Estadístico ADF: {result_d2[0]:.3f}')
    print(f'[2da Diferenciación] p-valor: {result_d2[1]:.3f}')
    

    # Gráficos
    fig, ax = plt.subplots(1, 3, figsize=(18,4))
    
    # Serie original
    ax[0].plot(timestamps, serie, 'bo-')
    ax[0].set_title('Serie Original')
    
    # Primera diferenciación
    ax[1].plot(timestamps[1:], diff1, 'go-')
    ax[1].set_title('1ra Diferenciación')
    
    # Segunda diferenciación
    ax[2].plot(timestamps[2:], diff2, 'ro-')
    ax[2].set_title('2da Diferenciación')
    
    plt.tight_layout()
    plt.show()
    
    return diff1, diff2

# Ejecutar análisis
diff1, diff2 = analisis_arima_manual(serie_temp, 'Temperatura')

# Guardar resultados
with open('temperatura_arima_manual.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # Escribir encabezados
    writer.writerow(['Timestamp', 'Temperatura', 'Diff1', 'Diff2'])
    
    # Escribir datos
    for i in range(len(timestamps)):
        row = [
            timestamps[i].strftime("%Y-%m-%d %H:%M:%S"),
            temperaturas[i],
            diff1[i-1] if i > 0 else '',
            diff2[i-2] if i > 1 else ''
        ]
        writer.writerow(row)