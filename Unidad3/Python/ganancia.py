import numpy as np

# Dimensiones de la matriz
filas = 3
columnas = 4

# Valores máximos y mínimos
V_max = np.array([50, 120, 200, 1200])
V_min = np.array([10, 20, 30, 200])

# Generar valores aleatorios para Importancia_Dsensor en el rango [0.1, 0.4]
Importancia_Dsensor = np.random.uniform(0.1, 0.4, size=4)

# Cálculo de la satisfacción
Satisfaccion = (V_max - Importancia_Dsensor) / (V_max - V_min)

# Modificar la última columna
Satisfaccion[-1] = 1 - Satisfaccion[-1]

# Cálculo de la ganancia
ganancia = Satisfaccion * Importancia_Dsensor

# Imprimir matrices
print("Matriz de valores aleatorios (Importancia_Dsensor):")
print(Importancia_Dsensor)

print("\nMatriz de satisfacción:")
print(Satisfaccion)

print("\nMatriz de ganancia de satisfacción:")
print(ganancia)