import serial
import csv
import numpy as np
from collections import deque
from datetime import datetime

# Configuración
ALPHA = 0.4
UMBRAL = 26
DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
VENTANA_IQR = 15  # Reducido por frecuencia de lecturas

arduino = serial.Serial('COM3', 115200, timeout=5)
buffer = deque(maxlen=VENTANA_IQR)
nvector = []
dia = 0
lectura_actual = 0

def limpiar_datos(datos):
    # Interpolación lineal
    for i in range(len(datos)):
        if np.isnan(datos[i]):
            antes = np.nanmax(datos[:i]) if i>0 else np.nan
            despues = np.nanmin(datos[i:]) if i<len(datos) else np.nan
            datos[i] = np.nanmean([antes, despues])
    
    # Detección outliers con IQR
    q1, q3 = np.nanpercentile(datos, [25, 75])
    iqr = q3 - q1
    lim_inf = q1 - 1.5*iqr
    lim_sup = q3 + 1.5*iqr
    mediana = np.nanmedian(datos)
    
    return np.where((datos < lim_inf) | (datos > lim_sup), mediana, datos)

def suavizado_exponencial(valor, anterior, alpha):
    return alpha * valor + (1 - alpha) * anterior

with open('datos_dht11.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Día', 'Hora', 'Mediana', 'Suavizado', 'Estado LED'])
    
    try:
        while True:
            linea = arduino.readline().decode().strip()
            
            if not linea or "ERROR" in linea:
                buffer.append(np.nan)
                continue
                
            try:
                mediana = float(linea)
                buffer.append(mediana)
            except ValueError:
                continue
                
            # Limpieza de datos
            datos_limpios = limpiar_datos(np.array(buffer, dtype=float))
            valor_actual = datos_limpios[-1] if not np.isnan(datos_limpios[-1]) else np.nanmedian(datos_limpios)
            
            # Suavizado exponencial
            if nvector:
                suavizado = suavizado_exponencial(valor_actual, nvector[-1], ALPHA)
            else:
                suavizado = valor_actual
            nvector.append(suavizado)
            
            # Control LED
            estado = "Apagado"
            if not np.isnan(suavizado):
                if suavizado > UMBRAL:
                    arduino.write(b'L')
                    estado = "Encendido"
                else:
                    arduino.write(b'l')
                    estado = "Apagado"
            
            # Registro CSV
            writer.writerow([
                DIAS[dia],
                f"{lectura_actual:02d}:00",
                round(mediana, 1),
                round(suavizado, 2),
                estado
            ])
            
            print(f"{DIAS[dia]} [{lectura_actual:02d}:00] Temp: {suavizado:.1f}°C | LED: {estado}")
            
            # Actualizar ciclo diario
            lectura_actual = (lectura_actual + 1) % 24
            if lectura_actual == 0:
                dia = (dia + 1) % 7
                buffer.clear()
                nvector = []

    except KeyboardInterrupt:
        arduino.close()
        print("Monitoreo finalizado")