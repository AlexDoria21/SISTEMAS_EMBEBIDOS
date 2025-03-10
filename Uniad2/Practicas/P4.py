import csv
from datetime import datetime
import matplotlib.pyplot as plt

def leer_csv(archivo):
    datos = []
    try:
        with open(archivo, 'r') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                timestamp = datetime.strptime(fila['Timestamp'], '%Y-%m-%d %H:%M:%S')
                temperatura = float(fila['Temperatura']) if fila['Temperatura'] else None
                datos.append((timestamp, temperatura))
        return datos
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'")
        exit()

def tratar_valores_vacios(datos):
    vacios = [i for i, (_, temp) in enumerate(datos) if temp is None]
    
    for i in vacios:
        tiempo_actual = datos[i][0]
        
        # Buscar valores anterior y posterior
        anterior = next((d for d in reversed(datos[:i]) if d[1] is not None), None)
        posterior = next((d for d in datos[i+1:] if d[1] is not None), None)
        
        if anterior and posterior:
            # Calcular diferencia de tiempo
            delta_t = (posterior[0] - anterior[0]).total_seconds()
            t = (tiempo_actual - anterior[0]).total_seconds()
            
            # Interpolación lineal sin math
            valor = anterior[1] + (posterior[1] - anterior[1]) * (t / delta_t)
            datos[i] = (tiempo_actual, valor)
            
    return datos

def calcular_iqr(datos):
    temps = [d[1] for d in datos if d[1] is not None]
    temps.sort()
    n = len(temps)
    
    # Cálculo de percentiles sin math
    q1_index = int(n * 0.25)
    q3_index = int(n * 0.75)
    q1 = temps[q1_index] if n > 0 else 0
    q3 = temps[q3_index] if n > 0 else 0
    
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr

def detectar_outliers(datos, lim_inf, lim_sup):
    return [i for i, (_, temp) in enumerate(datos) if temp and (temp < lim_inf or temp > lim_sup)]

def suavizado_exponencial(datos, alpha=0.3):
    if not datos:
        return []
    
    suavizados = []
    previo = datos[0][1] if datos[0][1] is not None else 0
    
    for ts, temp in datos:
        if temp is None:
            suavizados.append((ts, previo))
            continue
            
        suavizado = alpha * temp + (1 - alpha) * previo
        suavizados.append((ts, suavizado))
        previo = suavizado
    
    return suavizados

def graficar(datos, suavizados):
    tiempos = [d[0] for d in datos]
    orig = [d[1] for d in datos]
    suav = [s[1] for s in suavizados]
    
    plt.figure(figsize=(12, 6))
    plt.plot(tiempos, orig, 'b-o', label='Original', markersize=5)
    plt.plot(tiempos, suav, 'r-', linewidth=2, label='Suavizado')
    plt.title('Temperatura - Datos Originales vs Suavizados')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperatura (°C)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    # 1. Leer y procesar datos
    datos = leer_csv('temperatura.csv')
    datos_limpios = tratar_valores_vacios(datos)
    
    # 2. Detección de outliers
    lim_inf, lim_sup = calcular_iqr(datos_limpios)
    outliers = detectar_outliers(datos_limpios, lim_inf, lim_sup)
    
    print(f"Límites IQR: [{lim_inf:.2f}, {lim_sup:.2f}]")
    print(f"Outliers detectados: {len(outliers)}")
    
    # 3. Tratamiento de outliers
    for i in outliers:
        datos_limpios[i] = (datos_limpios[i][0], None)
    datos_finales = tratar_valores_vacios(datos_limpios)
    
    # 4. Aplicar suavizado y guardar
    suavizados = suavizado_exponencial(datos_finales)
    
    # 5. Graficar y guardar resultados
    graficar(datos_finales, suavizados)
    
    with open('temperatura_procesada.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Original', 'Suavizado'])
        for (orig, suav) in zip(datos_finales, suavizados):
            writer.writerow([
                orig[0].strftime('%Y-%m-%d %H:%M:%S'),
                f"{orig[1]:.2f}" if orig[1] else '',
                f"{suav[1]:.2f}"
            ])

if __name__ == "__main__":
    main()