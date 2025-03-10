import serial
import csv
from datetime import datetime

ser = serial.Serial('COM3', 9600)
archivo_csv = open('temperatura3_0.csv', 'a', newline='')
escritor_csv = csv.writer(archivo_csv)
escritor_csv.writerow(["Timestamp", "Temperatura"])

contador = 0
try:
    while contador < 24:
        linea = ser.readline().decode().strip()
        if linea:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            escritor_csv.writerow([fecha, float(linea)])
            archivo_csv.flush()
            contador += 1
            print(f"Muestra {contador}/24: {linea}°C")
finally:
    ser.close()
    archivo_csv.close()
    print("Datos de temperatura guardados")