import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # backend sin ventana, necesario para guardar en terminal
import matplotlib.pyplot as plt

# 1. Cargar datos del CSV
try:
    df = pd.read_csv('resultados/fibonacci_datos_analisis.csv')
    df = df.dropna()
    
    # Extraer variables (x = n, y = pasos)
    x = df['longitud_entrada'].values
    y = df['pasos'].values

    # 2. Regresión Polinomial de Grado 2 (Cuadrática)
    coefs = np.polyfit(x, y, 2)
    p = np.poly1d(coefs)

    # 3. Graficación
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='blue', s=100, label='Datos Experimentales (Simulación)')
    
    # Línea de tendencia
    x_line = np.linspace(min(x), max(x), 100)
    plt.plot(x_line, p(x_line), color='red', linewidth=2, label=f'Regresión: {p}')

    plt.title('Análisis Empírico: Complejidad de la Máquina de Turing', fontsize=14)
    plt.xlabel('Tamaño de Entrada (n símbolos "1")', fontsize=12)
    plt.ylabel('Número de Pasos Ejecutados', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Guardar imagen
    plt.savefig('resultados/grafica_fibonacci_final.png')
    print("Gráfica guardada en resultados/grafica_fibonacci_final.png")

    print(f"Ecuación del tiempo: T(n) = {coefs[0]:.2f}n² + {coefs[1]:.2f}n + {coefs[2]:.2f}")
    print("Conclusión: La complejidad asintótica es O(n²)")

except Exception as e:
    print(f"Error al procesar: {e}")