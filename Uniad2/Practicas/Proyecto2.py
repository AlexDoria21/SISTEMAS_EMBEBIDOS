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
        self.w = []  # Lista para w
        self.w_suavizado = []  # Lista para w suavizado
        self.inicio = time.time()
        
        # Configuración serial
        self.arduino = serial.Serial('COM3', 115200, timeout=60)
        time.sleep(2)
        
        # Archivo de registro
        self.archivo = open('registro_arima.csv', 'w', newline='')
        self.escritor = csv.writer(self.archivo)
        self.escritor.writerow(['Hora', 'Mediana', 'w', 'w_Suavizado', 'Estado_AC', 'Pronostico_ARIMA', 'd_optimo'])
    
    def calcular_mediana(self, datos):
        return np.median(datos)
    
    def suavizamiento_exponencial(self, lista, alpha):
        if not lista:
            return None
        suavizado = lista[0]  # Valor inicial
        resultado = [suavizado]
        for i in range(1, len(lista)):
            suavizado = alpha * lista[i] + (1 - alpha) * suavizado
            resultado.append(suavizado)
        return resultado[-1]  # Último valor suavizado
    
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
            return pronostico[0], orden[1]
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
                        
                        # Calcular w como la diferencia entre valores consecutivos
                        w_actual = abs(mediana - self.historico[-2]) if len(self.historico) > 1 else 0
                        self.w.append(w_actual)
                        
                        # Aplicar suavizamiento exponencial a w
                        w_suavizado = self.suavizamiento_exponencial(self.w, self.alpha)
                        self.w_suavizado.append(w_suavizado)
                        
                        # Determinar diferenciación necesaria para ARIMA
                        d_optimo = self.determinar_d_optimo(self.historico)
                        
                        # Preparar datos para ARIMA
                        datos_arima = self.historico.copy()
                        if d_optimo > 0:
                            datos_arima = self.diferencia_serie(datos_arima, d_optimo)
                        
                        # Realizar pronóstico si hay suficientes datos
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
                            round(w_actual, 3),
                            round(w_suavizado, 3) if w_suavizado else 0.0,
                            estado_ac,
                            round(pronostico, 1) if pronostico else '',
                            d_optimo
                        ])
                        
                        print(f"[{timestamp}] Mediana: {mediana:.1f} | w: {w_actual:.3f} | w_suavizado: {w_suavizado:.3f} | Pronóstico: {pronostico if pronostico else 'N/A'} | d: {d_optimo}")
                        
                    except ValueError:
                        continue
        finally:
            self.arduino.close()
            self.archivo.close()
            print("Registro ARIMA completado")

if __name__ == "__main__":
    sistema = SistemaTermicoARIMA()
    sistema.ejecutar()
