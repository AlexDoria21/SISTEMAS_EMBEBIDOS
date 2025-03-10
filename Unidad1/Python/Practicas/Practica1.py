import serial
import random

# Configurar conexión serial con Arduino
arduino = serial.Serial("COM3", 9600, timeout=1)  # Cambia "COM3" según tu puerto

# Parámetros del Algoritmo Genético
N = 5   # Tamaño del vector
POP_SIZE = 10  # Tamaño de la población
GENERATIONS = 50  # Número de iteraciones
MUTATION_RATE = 0.1  # Probabilidad de mutación

# Función objetivo: minimizar la suma de los cuadrados
def fitness(vector):
    return sum(x**2 for x in vector)

# Generar población inicial (valores aleatorios en el rango 0-1023)
def create_population():
    return [[random.randint(0, 1023) for _ in range(N)] for _ in range(POP_SIZE)]

# Selección por torneo
def selection(population):
    return min(random.sample(population, 2), key=fitness)

# Cruza de un punto
def crossover(parent1, parent2):
    point = random.randint(1, N - 1)
    return parent1[:point] + parent2[point:]

# Mutación aleatoria
def mutate(vector):
    if random.random() < MUTATION_RATE:
        idx = random.randint(0, N - 1)
        vector[idx] = random.randint(0, 1023)  # Nueva mutación dentro del rango
    return vector

# Leer datos desde Arduino
def get_arduino_data():
    while True:
        line = arduino.readline().decode().strip()
        if line:
            try:
                return list(map(int, line.split(",")))  # Convertir a lista de enteros
            except ValueError:
                continue

# Obtener los datos del potenciómetro
vector_inicial = get_arduino_data()
print("Vector inicial:", vector_inicial)

# Algoritmo Genético
population = create_population()
for _ in range(GENERATIONS):
    new_population = []
    for _ in range(POP_SIZE):
        parent1 = selection(population)
        parent2 = selection(population)
        offspring = crossover(parent1, parent2)
        offspring = mutate(offspring)
        new_population.append(offspring)
    population = sorted(new_population, key=fitness)

# Mejor solución encontrada
best_solution = population[0]
print("Mejor solución encontrada:", best_solution)
print("Suma de cuadrados mínima:", fitness(best_solution))
