import serial
import csv
import time

# Configura el puerto serie (ajústalo según tu sistema)
arduino_port = "COM3"  # En Windows (cambiar si es diferente)
baud_rate = 9600

# Inicia la comunicación serie
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Espera a que el puerto se estabilice

# Nombre del archivo CSV
csv_filename = "potenciometros.csv"

# Abre el archivo CSV en modo escritura
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Moda_Pot1", "Moda_Pot2", "Moda_Pot3", "Moda_Pot4"])  # Encabezado

    try:
        while True:
            # Lee una línea del puerto serie y la decodifica
            line = ser.readline().decode('utf-8').strip()
            print(f"Datos recibidos: {line}")

            # Separa los valores y los convierte en enteros
            values = line.split(",")
            if len(values) == 4:  # Verifica que haya 4 valores
                writer.writerow(values)

    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")

# Cierra el puerto serie
ser.close()
