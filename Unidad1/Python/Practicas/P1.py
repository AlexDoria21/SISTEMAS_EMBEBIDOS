import serial
import csv
from datetime import datetime

# Configurar puerto serial 
ser = serial.Serial('COM3', 9600)
ser.flushInput()

with open('datos.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Val1", "Val2", "Val3", "Val4", "Suma_Cuadrados"])
    
    try:
        while True:
            # Leer y decodificar datos
            datos = ser.readline().decode().strip().split(',')
            if len(datos) == 4:
                valores = list(map(int, datos))
                suma_cuadrados = sum(v**2 for v in valores)
                
                # Escribir en CSV
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                writer.writerow([timestamp] + valores + [suma_cuadrados])
                
                # Feedback en tiempo real
                print(f"Valores: {valores} - Suma cuadrados: {suma_cuadrados}")
                
    except KeyboardInterrupt:
        ser.close()
        print("Captura detenida")