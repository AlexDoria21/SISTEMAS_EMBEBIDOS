import serial
import csv

# Configuración del puerto serie y parámetro de suavizado
arduino = serial.Serial('COM3', 115200, timeout=10)
alpha = 0.5  # Factor de suavizado (0 < alpha < 1)

# Diccionario para almacenar los valores suavizados por potenciómetro
suavizado = {
    'media': {1: None, 2: None, 3: None, 4: None},
    'mediana': {1: None, 2: None, 3: None, 4: None}
}

with open('estadisticas_potenciometros.csv', 'w', newline='') as archivo:
    writer = csv.writer(archivo)
    # Encabezados actualizados con métricas suavizadas
    writer.writerow([
        "Iteración", "Potenciómetro", "Mínimo", "Máximo", 
        "Media", "Media_Suavizada", "Mediana", "Mediana_Suavizada", "Moda", "Mejor Medida"
    ])

    for _ in range(20 * 4):  # 20 iteraciones * 4 potenciómetros
        linea = arduino.readline().decode().strip()
        if linea:
            datos = linea.split(",")
            if len(datos) == 7:
                iteracion, pot, minVal, maxVal, media, mediana, moda = map(int, datos)
                
                # Aplicar suavizado exponencial a la media y mediana
                pot_key = pot
                media_actual = media
                mediana_actual = mediana
                
                # Inicializar valores suavizados si es la primera iteración
                if suavizado['media'][pot_key] is None:
                    suavizado['media'][pot_key] = media_actual
                    suavizado['mediana'][pot_key] = mediana_actual
                else:
                    suavizado['media'][pot_key] = alpha * media_actual + (1 - alpha) * suavizado['media'][pot_key]
                    suavizado['mediana'][pot_key] = alpha * mediana_actual + (1 - alpha) * suavizado['mediana'][pot_key]
                
                # Determinar la mejor medida usando los valores suavizados
                media_suavizada = suavizado['media'][pot_key]
                mediana_suavizada = suavizado['mediana'][pot_key]
                
                diferencias = {
                    "Mínimo": abs(minVal - media_suavizada),
                    "Máximo": abs(maxVal - media_suavizada),
                    "Media": abs(media_actual - mediana_suavizada),
                    "Mediana": abs(mediana_actual - media_suavizada),
                    "Moda": abs(moda - media_suavizada) if moda != -1 else float('inf')
                }
                
                mejor_medida = min(diferencias, key=diferencias.get)
                
                # Escribir en el CSV con métricas suavizadas
                writer.writerow([
                    iteracion, pot, minVal, maxVal, 
                    media, round(suavizado['media'][pot_key]), 
                    mediana, round(suavizado['mediana'][pot_key]), 
                    moda, mejor_medida
                ])
                print(f"Iteración {iteracion}, Pot {pot}: Media Suavizada = {round(suavizado['media'][pot_key])}, Mejor -> {mejor_medida}")

arduino.close()
print("Datos guardados en 'estadisticas_potenciometros.csv'")