import random

def vecindario(sol):
    nueva_sol = sol.copy()
    num_cambios = random.randint(1, len(sol) // 2)  # Cambiar entre 1 y la mitad de los valores
    for _ in range(num_cambios):
        indice = random.randint(0, len(sol)-1)  # Selecciona un índice aleatorio
        nueva_sol[indice] = random.randint(1, 5)  # Asigna un nuevo valor aleatorio entre 1 y 5
    return nueva_sol

# Solución inicial
So = [3, 1, 2, 5, 4]
SBest = So.copy()
VBest = sum(x**2 for x in So)

it = 0
max_iteraciones = 100

while it < max_iteraciones and VBest != 0:
    # Generar solución vecina con perturbación múltiple
    nSolucion = vecindario(So)
    VnSolucion = sum(x**2 for x in nSolucion)
    
    # Actualizar mejor solución si hay mejora
    if VnSolucion < VBest:
        VBest = VnSolucion
        SBest = nSolucion.copy()
    
    # Mover a la nueva solución para la siguiente iteración
    So = nSolucion.copy()
    it += 1

print("Mejor valor objetivo encontrado:", VBest)
print("Mejor solución encontrada:", SBest)