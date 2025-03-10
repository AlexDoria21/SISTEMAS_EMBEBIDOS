import serial
import csv

# Configurar el puerto serie (ajusta según tu sistema)
arduino = serial.Serial('COM3', 115200, timeout=10)

# Esperar a que Arduino envíe datos
print("Esperando datos de Arduino...")

# Crear o abrir archivo CSV
with open('temperatura_dht11.csv', 'w', newline='') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(["Hora", "Temperatura (°C)"])

    for _ in range(12):  # Recibe datos por 12 horas
        linea = arduino.readline().decode().strip()
        if linea:
            datos = linea.split(": ")
            if len(datos) == 2:
                writer.writerow([datos[0], datos[1]])
                print(f"Guardado: {datos[0]} - {datos[1]}°C")

# Cerrar conexión
arduino.close()
print("Datos guardados en 'temperatura_dht11.csv'")
