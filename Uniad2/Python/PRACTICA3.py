import serial
import csv
from collections import defaultdict

# Funciones de cálculo manual
def calcular_media(datos):
    return sum(datos)/len(datos) if datos else 0

def calcular_mediana(datos):
    if not datos: return 0
    ordenados = sorted(datos)
    n = len(ordenados)
    mid = n // 2
    return ordenados[mid] if n % 2 != 0 else (ordenados[mid-1] + ordenados[mid])/2

def calcular_moda(datos):
    if not datos: return 0
    frecuencias = defaultdict(int)
    for valor in datos:
        frecuencias[valor] += 1
    max_frec = max(frecuencias.values(), default=0)
    modas = [k for k, v in frecuencias.items() if v == max_frec]
    return modas[0] if modas else 0

# Configuración inicial
ser = serial.Serial('COM3', 115200, timeout=2)
ser.reset_input_buffer()

# Esperar sincronización
print("Esperando inicialización del Arduino...")
while True:
    linea = ser.readline().decode('utf-8', errors='replace').strip()
    if linea == "ARDUINO_INICIADO":
        print("Arduino detectado! Iniciando captura...")
        break

# 1. Capturar datos y guardar en CSV
with open('datos_crudos.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Iteracion', 'Muestra', 'Pot0', 'Pot1', 'Pot2', 'Pot3'])
    
    buffer = bytearray()
    iteracion = 0
    muestra = 0
    MAX_ITERACIONES = 100
    MUESTRAS_POR_ITERACION = 30

    while iteracion < MAX_ITERACIONES:
        # Leer todos los bytes disponibles
        data = ser.read(ser.in_waiting or 1)
        if data:
            buffer.extend(data)
            
            # Procesar líneas completas
            while b'\n' in buffer:
                line_end = buffer.index(b'\n')
                linea_bytes = buffer[:line_end]
                buffer = buffer[line_end+1:]
                
                try:
                    linea = linea_bytes.decode('utf-8', errors='replace').strip()
                    valores = list(map(int, linea.split(',')))
                    
                    if len(valores) == 4:
                        writer.writerow([iteracion, muestra] + valores)
                        muestra += 1
                        
                        if muestra >= MUESTRAS_POR_ITERACION:
                            iteracion += 1
                            muestra = 0
                            print(f"Progreso: {iteracion}/{MAX_ITERACIONES} iteraciones")
                            
                except (ValueError, IndexError) as e:
                    print(f"Error en línea: {linea} | Error: {str(e)}")
                    continue

ser.close()
print("Captura completa! Procesando datos...")

# 2. Procesar datos y generar resultados
pots = defaultdict(list)

with open('datos_crudos.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Saltar encabezado
    
    for row in reader:
        try:
            for i in range(4):
                pots[f'Pot{i}'].append(int(row[2+i]))
        except (IndexError, ValueError):
            continue

# 3. Calcular estadísticas y guardar resultados
with open('resultados.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Potenciometro', 'Maximo', 'Minimo', 'Media', 'Mediana', 'Moda', 'Mejor_Medida'])
    
    for pot in ['Pot0', 'Pot1', 'Pot2', 'Pot3']:
        datos = pots[pot]
        if not datos:
            continue
            
        maximo = max(datos)
        minimo = min(datos)
        media = round(calcular_media(datos), 2)
        mediana = round(calcular_mediana(datos), 2)
        moda = calcular_moda(datos)
        
        # Determinar mejor medida (más cercana a 0)
        medidas = {
            'Maximo': maximo,
            'Minimo': minimo,
            'Media': media,
            'Mediana': mediana,
            'Moda': moda
        }
        mejor_nombre, mejor_valor = min(
            ((k, abs(v)) for k, v in medidas.items()),
            key=lambda x: x[1]
        )
        
        writer.writerow([
            pot,
            maximo,
            minimo,
            media,
            mediana,
            moda,
            f"{mejor_nombre}: {medidas[mejor_nombre]}"
        ])

print("Proceso completado!")
print("Archivos generados:")
print("- datos_crudos.csv: Datos originales")
print("- resultados.csv: Análisis estadístico")