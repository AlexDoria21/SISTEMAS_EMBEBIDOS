import serial
import csv
import time
import numpy as np
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

class SistemaTermicoARIMA:
    def __init__(self):
        self.alpha = 0.4
        self.umbral = 26
        self.datos = []
        self.suavizados = []
        self.historico = []  # Para ARIMA
        self.inicio = time.time()
        
        # Configuración serial
        self.arduino = serial.Serial('COM3', 115200, timeout=60)
        time.sleep(2)
        
        # Archivo de registro mejorado
        self.archivo = open('registro_arima.csv', 'w', newline='')
        self.escritor = csv.writer(self.archivo)
        self.escritor.writerow(['Hora', 'Mediana', 'Suavizado', 'Estado_AC', 'Pronostico_ARIMA', 'd_optimo'])
        
    def calcular_mediana(self, datos):
        return np.median(datos)
    
    def test_estacionariedad(self, serie, significancia=0.05):
        resultado = adfuller(serie)
        return resultado[1] < significancia
    
    def diferencia_serie(self, datos, orden=1):
        return np.diff(datos, n=orden)
    
    def determinar_d_optimo(self, datos, max_d=2):
        d = 0
        serie_actual = datos.copy()
        while d <= max_d:
            if self.test_estacionariedad(serie_actual):
                return d
            serie_actual = self.diferencia_serie(serie_actual)
            d += 1
        return d
    
    def pronosticar_arima(self, datos_entrenamiento, orden=(1,1,1)):
        try:
            modelo = ARIMA(datos_entrenamiento, order=orden)
            modelo_ajustado = modelo.fit()
            pronostico = modelo_ajustado.forecast(steps=1)
            return pronostico[0], orden[1]  # Devuelve pronóstico y d usado
        except Exception as e:
            print(f"Error ARIMA: {str(e)}")
            return None, 0
    
    def ejecutar(self):
        try:
            while (time.time() - self.inicio) < 86400:  # 24 horas
                if self.arduino.in_waiting:
                    linea = self.arduino.readline().decode().strip()
                    try:
                        mediana = float(linea)
                        self.historico.append(mediana)
                        
                        # Paso 1: Determinar diferenciación necesaria
                        d_optimo = self.determinar_d_optimo(self.historico)
                        
                        # Paso 2: Preparar datos para ARIMA
                        datos_arima = self.historico.copy()
                        if d_optimo > 0:
                            datos_arima = self.diferencia_serie(datos_arima, d_optimo)
                        
                        # Paso 3: Realizar pronóstico si hay suficientes datos
                        pronostico, _ = self.pronosticar_arima(datos_arima, (1,d_optimo,1))
                        
                        # Control preventivo con ARIMA
                        estado_ac = False
                        if pronostico:
                            if pronostico > self.umbral:
                                self.arduino.write(b'L')
                                estado_ac = True
                            else:
                                self.arduino.write(b'l')
                        
                        # Registro completo
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        self.escritor.writerow([
                            timestamp,
                            round(mediana, 1),
                            round(np.mean(self.suavizados[-3:]) if self.suavizados else 0.0),
                            estado_ac,
                            round(pronostico, 1) if pronostico else '',
                            d_optimo
                        ])
                        
                        print(f"[{timestamp}] Mediana: {mediana:.1f} | "
                            f"Pronóstico: {pronostico if pronostico else 'N/A'} | "
                            f"d: {d_optimo}")
                        
                    except ValueError:
                        continue
        finally:
            self.arduino.close()
            self.archivo.close()
            print("Registro ARIMA completado")

if __name__ == "__main__":
    sistema = SistemaTermicoARIMA()
    sistema.ejecutar()