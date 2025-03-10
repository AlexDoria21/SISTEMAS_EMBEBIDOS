import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calc_suavizado_exponencial(serie, alfa):
    new_serie = np.zeros_like(serie)
    new_serie[0] = serie[0]
    for t in range(1, len(serie)):
        new_serie[t] = alfa * serie[t] + (1 - alfa) * new_serie[t-1]
    return new_serie

df = pd.read_csv('temperatura3_0.csv', parse_dates=['Timestamp'])
datos_temp = df['Temperatura'].values

alfa = 0.3
temp_suavizada = calc_suavizado_exponencial(datos_temp, alfa)

plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], datos_temp, 'b-', label='Datos Reales')
plt.plot(df['Timestamp'], temp_suavizada, 'r--', label=f'Suavizado (α={alfa})')
plt.title('Evolución de la Temperatura')
plt.ylabel('°C')
plt.legend()
plt.grid(True)
plt.show()

df['Temp_Suavizada'] = temp_suavizada
df.to_csv('temperatura_suavizada3_0.csv', index=False)