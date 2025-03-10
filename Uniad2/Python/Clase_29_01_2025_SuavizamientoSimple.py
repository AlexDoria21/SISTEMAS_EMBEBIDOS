
import numpy as np
import matplotlib.pyplot as plt

def calc_suavizado_exponencial(serie, alfa):
    # El parámetro alfa controla el peso que se le da a los datos
    # valores cercanos a 1 hacen que los datos recientes tengan más influencia
    # valores cercanos a 0 dan más importancia a los datos antiguos

    new_serie = np.zeros_like(serie) # reserva memoria y rellena con ceros
    new_serie[0] = serie[0]  # El primer valor suavizado es el primer valor de la serie real
    for t in range(1, len(serie)): #calcula los nuevos valores para la serie suavizada
        new_serie[t] = alfa * serie[t] + (1 - alfa) * new_serie[t-1]
    return new_serie


# Serie de tiempo a suavizar
datos = np.array([100, 132, 105, 133, 141, 137, 156, 136, 157, 124, 132, 142])  # Corresponde a los valores reales

alfa = 0.7
serie_suavizada = calc_suavizado_exponencial(datos, alfa)

#x = [i for i in range(1, len(serie_suavizada)+1)]
x = []
for i in range(1, len(serie_suavizada)+1):  #generar el total de valores que se usaran para tabular
    # y graficar las series
    x.append(i)

plt.figure(figsize=(12, 6))
plt.plot(x, datos, label='REAL', color='blue')
plt.plot(x, serie_suavizada, label='SUAVIZADA', color='green')
plt.title('Comparación de Series')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()
