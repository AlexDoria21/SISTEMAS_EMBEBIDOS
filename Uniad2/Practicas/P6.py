import serial
import csv
import time
from datetime import datetime

class SistemaTermico:
    def __init__(self):
        self.alpha = 0.4
        self.umbral = 26
        self.datos = []
        self.suavizados = []
        self.inicio = time.time()
        
        # Configurar comunicación serial
        self.arduino = serial.Serial('COM3', 115200, timeout=60)
        time.sleep(2)  # Esperar inicialización
        
        # Archivo de registro
        self.archivo = open('registro_termico.csv', 'w', newline='')
        self.escritor = csv.writer(self.archivo)
        self.escritor.writerow(['Hora', 'Mediana', 'Suavizado', 'Estado_AC'])
        
    def calcular_mediana(self, datos):
        ordenados = sorted(datos)
        n = len(ordenados)
        return (ordenados[n//2-1] + ordenados[n//2])/2 if n%2 == 0 else ordenados[n//2]
    
    def limpiar_dato(self, valor, ventana=4):
        # Usar últimas 4 horas para limpieza
        contexto = self.datos[-ventana:] + [valor]
        contexto_limpio = [v for v in contexto if v is not None]
        
        if len(contexto_limpio) < 3:
            return valor
        
        ordenados = sorted(contexto_limpio)
        q1 = ordenados[len(ordenados)//4]
        q3 = ordenados[3*len(ordenados)//4]
        iqr = q3 - q1
        lim_inf = q1 - 1.5*iqr
        lim_sup = q3 + 1.5*iqr
        
        return valor if lim_inf <= valor <= lim_sup else self.calcular_mediana(contexto_limpio)
    
    def suavizar(self, valor):
        if not self.suavizados:
            return valor
        return self.alpha * valor + (1 - self.alpha) * self.suavizados[-1]
    
    def controlar_ac(self, temperatura):
        if temperatura > self.umbral:
            self.arduino.write(b'L')
            return True
        else:
            self.arduino.write(b'l')
            return False
    
    def ejecutar(self):
        try:
            while (time.time() - self.inicio) < 86400:  # 24 horas
                if self.arduino.in_waiting:
                    linea = self.arduino.readline().decode().strip()
                    try:
                        mediana = float(linea)
                        mediana_limpia = self.limpiar_dato(mediana)
                        
                        # Suavizado exponencial
                        suavizado = self.suavizar(mediana_limpia)
                        self.suavizados.append(suavizado)
                        
                        # Control y registro
                        estado = self.controlar_ac(suavizado)
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        
                        self.escritor.writerow([
                            timestamp,
                            round(mediana, 1),
                            round(suavizado, 2),
                            estado
                        ])
                        
                        print(f"[{timestamp}] Mediana: {mediana:.1f}°C | Suavizado: {suavizado:.1f}°C | AC: {'ON' if estado else 'OFF'}")
                        
                    except ValueError:
                        continue
        finally:
            self.arduino.close()
            self.archivo.close()
            print("Registro completado")

if __name__ == "__main__":
    sistema = SistemaTermico()
    sistema.ejecutar()