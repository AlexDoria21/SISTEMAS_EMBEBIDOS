import random

def vecindario(sol):
    # Copiar la solución para no modificar la original
    nueva_sol = sol.copy()
    # Seleccionar un índice aleatorio
    indice = random.randint(0, len(sol)-1)
    # Generar un nuevo valor aleatorio entre 1 y 5
    nuevo_valor = random.randint(1, 5)
    # Modificar la solución en el índice seleccionado
    nueva_sol[indice] = nuevo_valor
    return nueva_sol

# Solución inicial
So = [3, 1, 2, 5, 4]
SBest = So.copy()
VBest = sum(x**2 for x in So)

it = 0
max_iteraciones = 100

while it < max_iteraciones and VBest != 0:
    # Generar solución vecina
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