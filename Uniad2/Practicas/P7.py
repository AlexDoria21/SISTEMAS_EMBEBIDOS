import serial
import csv
import numpy as np
from collections import deque
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# Configuración
ALPHA = 0.4
UMBRAL = 26
DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
VENTANA_IQR = 15
HISTORICO_ARIMA = 24  # 24 datos horarios para ARIMA

arduino = serial.Serial('COM3', 115200, timeout=5)
buffer = deque(maxlen=VENTANA_IQR)
historico_arima = deque(maxlen=HISTORICO_ARIMA)
nvector = []
dia = 0
lectura_actual = 0
modelo_arima = None
d_actual = 0

def suavizado_exponencial(valor_actual, valor_anterior, alpha):
    return alpha * valor_actual + (1 - alpha) * valor_anterior

def test_estacionariedad(serie):
    resultado = adfuller(serie)
    return resultado[1] < 0.05  # p-valor < 0.05 = estacionaria

def determinar_d_optimo(serie):
    d = 0
    temp_serie = serie.copy()
    while d <= 2:  # Máximo 2 diferenciaciones
        if test_estacionariedad(temp_serie):
            return d
        temp_serie = np.diff(temp_serie)
        d += 1
    return d

def entrenar_arima(datos, d):
    try:
        modelo = ARIMA(datos, order=(1, d, 1))  # ARIMA(1,d,1)
        modelo_ajustado = modelo.fit()
        return modelo_ajustado
    except Exception as e:
        print(f"Error ARIMA: {str(e)}")
        return None

def pronosticar_arima(modelo):
    try:
        return modelo.forecast(steps=1)[0]
    except:
        return None

with open('datos_arima.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Día', 'Hora', 'Mediana', 'Suavizado', 'd', 'Pronóstico', 'Estado LED'])
    
    try:
        while True:
            linea = arduino.readline().decode().strip()
            
            if not linea or "ERROR" in linea:
                buffer.append(np.nan)
                continue
                
            try:
                mediana = float(linea)
                buffer.append(mediana)
                historico_arima.append(mediana)
            except ValueError:
                continue
                
            # Limpieza de datos
            datos_limpios = np.where(np.isnan(buffer), np.nanmedian(buffer), buffer)
            
            # Suavizado exponencial
            valor_actual = datos_limpios[-1]
            suavizado = suavizado_exponencial(valor_actual, nvector[-1], ALPHA) if nvector else valor_actual
            nvector.append(suavizado)
            
            # Análisis ARIMA cada hora completa
            pronostico = None
            if len(historico_arima) == HISTORICO_ARIMA and lectura_actual % 1 == 0:
                # Paso 1: Determinar diferenciación necesaria
                d_actual = determinar_d_optimo(list(historico_arima))
                
                # Paso 2: Entrenar modelo
                modelo_arima = entrenar_arima(list(historico_arima), d_actual)
                
                # Paso 3: Pronosticar
                if modelo_arima:
                    pronostico = pronosticar_arima(modelo_arima)
            
            # Control predictivo
            estado = "Apagado"
            if not np.isnan(suavizado):
                umbral_ajustado = UMBRAL
                if pronostico:
                    umbral_ajustado = UMBRAL - 0.7 if pronostico > UMBRAL else UMBRAL
                
                if suavizado > umbral_ajustado:
                    arduino.write(b'L')
                    estado = "Encendido"
                else:
                    arduino.write(b'l')
                    estado = "Apagado"
            
            # Registro de datos
            writer.writerow([
                DIAS[dia],
                f"{lectura_actual:02d}:00",
                round(mediana, 1),
                round(suavizado, 2),
                d_actual,
                round(pronostico, 2) if pronostico else '',
                estado
            ])
            
            print(f"{DIAS[dia]} [{lectura_actual:02d}:00] " 
                f"d={d_actual} | Temp: {suavizado:.1f}°C | "
                f"Pronóstico: {pronostico:.1f if pronostico else 'N/A'} | "
                f"LED: {estado}")
            
            # Actualizar ciclo
            lectura_actual = (lectura_actual + 1) % 24
            if lectura_actual == 0:
                dia = (dia + 1) % 7
                buffer.clear()
                nvector = []

    except KeyboardInterrupt:
        arduino.close()
        print("Monitoreo finalizado")