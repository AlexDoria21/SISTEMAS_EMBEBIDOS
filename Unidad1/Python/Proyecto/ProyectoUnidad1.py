import serial
import random

# Configuración de la conexión serial
arduino = serial.Serial("COM3", 9600, timeout=1)  # Cambiar "COM3" según tu puerto

# Parámetros del Algoritmo Genético
n = 10  # Tamaño de la población
m = 5   # Tamaño de los vectores
mutation_rate = 0.005  # Probabilidad de mutación (0.5%)
generations = 50  # Total de generaciones

# Funciones de optimización (Objetivos de minimización o maximización)

def fitness_suma_cuadrados(vector):
    return sum(x**2 for x in vector)

def fitness_one_max(vector):
    return sum(1 for x in vector if x == 1)

def fitness_valor_absoluto(vector):
    return sum(abs(x) for x in vector)

# Función de fitness principal (se puede cambiar según el objetivo)
def fitness(vector):
    return fitness_suma_cuadrados(vector)  # O cambiar por otra función

# Generar población inicial
def create_population():
    return [[random.randint(0, 1023) for _ in range(m)] for _ in range(n)]

# Selección por torneo binario
def selection(population):
    return min(random.sample(population, 2), key=fitness)

# Cruce de un punto
def crossover(parent1, parent2):
    point = random.randint(1, m - 1)
    return parent1[:point] + parent2[point:]

# Mutación aleatoria
def mutate(vector):
    if random.random() < mutation_rate:
        idx = random.randint(0, m - 1)
        vector[idx] = random.randint(0, 1023)  # Nueva mutación dentro del rango
    return vector

# Selección ambiental: selecciona los n mejores individuos
def environmental_selection(population, offspring):
    combined_population = population + offspring
    return sorted(combined_population, key=fitness)[:n]

# Leer datos desde Arduino
def get_arduino_data():
    while True:
        line = arduino.readline().decode().strip()
        if line:
            try:
                return list(map(int, line.split(",")))  # Convertir a lista de enteros
            except ValueError:
                continue

# Algoritmo Genético
def genetic_algorithm():
    # Obtener datos del potenciómetro desde Arduino
    vector_inicial = get_arduino_data()
    print("Vector inicial:", vector_inicial)

    # Crear población inicial
    population = create_population()

    for gen in range(generations):
        new_population = []
        for _ in range(n):
            parent1 = selection(population)
            parent2 = selection(population)
            offspring = crossover(parent1, parent2)
            offspring = mutate(offspring)
            new_population.append(offspring)

        # Aplicar selección ambiental
        population = environmental_selection(population, new_population)

        # Obtener mejor solución en esta generación
        best_solution = population[0]

        # Calcular valores para cada función de fitness
        fit_suma_cuadrados = fitness_suma_cuadrados(best_solution)
        fit_one_max = fitness_one_max(best_solution)
        fit_valor_absoluto = fitness_valor_absoluto(best_solution)

        # Mostrar los resultados de esta generación
        print(f"\n Generación {gen+1}:")
        print(f"    Mejor solución: {best_solution}")
        print(f"    Suma de cuadrados (mín.): {fit_suma_cuadrados}")
        print(f"    One Max Problem (máx.): {fit_one_max}")
        print(f"    Valor absoluto (mín.): {fit_valor_absoluto}")
        print("-" * 50)

    # Mejor solución encontrada al final del proceso
    best_solution = population[0]

    print("\n Mejor solución encontrada ")
    print(f" Vector óptimo: {best_solution}")
    print(f" Suma de cuadrados (mín.): {fitness_suma_cuadrados(best_solution)}")
    print(f" One Max Problem (máx.): {fitness_one_max(best_solution)}")
    print(f" Valor absoluto (mín.): {fitness_valor_absoluto(best_solution)}")

# Ejecutar el algoritmo genético
genetic_algorithm()
