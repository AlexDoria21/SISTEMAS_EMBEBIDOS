import csv

min_suma = float('inf')
mejor_fila = None

with open('datos.csv', 'r') as file:
    lector = csv.reader(file)
    next(lector)  # Saltar encabezado
    
    for fila in lector:
        suma_actual = float(fila[5])
        if suma_actual < min_suma:
            min_suma = suma_actual
            mejor_fila = fila

print("\nMejor resultado:")
print(f"Timestamp: {mejor_fila[0]}")
print(f"Valores: {mejor_fila[1:5]}")
print(f"Suma mínima de cuadrados: {min_suma}")