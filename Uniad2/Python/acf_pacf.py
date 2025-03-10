import csv
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Leer datos diferenciados del archivo generado
diff2 = []
with open('temperatura_arima_manual.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Saltar encabezado
    for row in reader:
        if row[3]:  # Columna Diff2
            diff2.append(float(row[3]))

# Convertir a array numpy
datos_d2 = np.array(diff2)

# Configurar parámetros de lags
max_lags = min(len(datos_d2) // 2, 6)  # Máximo 50% del tamaño o 6

# Crear figura
plt.figure(figsize=(12, 6))

# Subplots
ax1 = plt.subplot(121)
ax2 = plt.subplot(122)

# Personalizar gráficas para temperatura
plot_acf(datos_d2, lags=max_lags, ax=ax1, 
        title='Función de Autocorrelación (Temperatura d=2)')
plot_pacf(datos_d2, lags=max_lags, ax=ax2, 
        title='Función de Autocorrelación Parcial (Temperatura d=2)')

# Ajustar y mostrar
plt.tight_layout()
plt.savefig('acf_pacf_temperatura.png')  # Guardar imagen
plt.show()