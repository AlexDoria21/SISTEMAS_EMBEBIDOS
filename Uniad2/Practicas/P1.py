import serial
import csv

# Configura el puerto serie (ajusta el puerto según tu sistema)
arduino = serial.Serial('COM3', 115200, timeout=2)

# Esperar a que Arduino envíe datos
print("Esperando datos de Arduino...")
arduino.readline()  # Omitir la primera línea vacía si es necesario

# Leer datos desde Arduino
estadisticas = []
for _ in range(4):  # Solo recibimos 4 líneas (una por potenciómetro)
    linea = arduino.readline().decode().strip()
    if linea:
        estadisticas.append(linea.split(','))

# Cerrar conexión
arduino.close()

# Guardar en CSV
with open('estadisticas_potenciometros.csv', 'w', newline='') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(["Potenciómetro", "Mínimo", "Máximo", "Media", "Mediana", "Moda"])
    writer.writerows(estadisticas)

print("Datos guardados en 'estadisticas_potenciometros.csv'")
