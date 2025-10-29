import numpy as np
import matplotlib.pyplot as plt

# --- 1. Simulación de un Proceso ESTACIONARIO (Ruido Blanco) ---

def simulate_stationary(num_steps=100, mean=0, std_dev=1):
    """Simula ruido blanco Gaussiano."""
    print("\n--- Simulando Proceso Estacionario (Ruido Blanco) ---")
    # Genera números aleatorios de una distribución normal
    data = np.random.normal(mean, std_dev, num_steps)
    print(f"  Primeros 10 puntos: {data[:10]}")
    return data

# --- 2. Simulación de un Proceso NO ESTACIONARIO (Caminata Aleatoria) ---

def simulate_non_stationary(num_steps=100, step_std_dev=1):
    """Simula una caminata aleatoria."""
    print("\n--- Simulando Proceso NO Estacionario (Caminata Aleatoria) ---")
    steps = np.random.normal(0, step_std_dev, num_steps)
    # Empieza en 0 y acumula los pasos
    data = np.cumsum(steps)
    print(f"  Primeros 10 puntos: {data[:10]}")
    return data

# --- 3. "Algoritmo": Comprobación Visual y Estadística Simple ---

def check_stationarity_simple(data, window_size=20):
    """Comprueba (visualmente) si la media y varianza cambian."""
    
    means = []
    variances = []
    num_windows = len(data) // window_size
    
    print(f"\n  Calculando media y varianza en ventanas de tamaño {window_size}:")
    for i in range(num_windows):
        window = data[i*window_size : (i+1)*window_size]
        means.append(np.mean(window))
        variances.append(np.var(window))
        print(f"    Ventana {i+1}: Media={means[-1]:.2f}, Varianza={variances[-1]:.2f}")
        
    # Graficar
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    fig.suptitle('Análisis de Estacionariedad Simple')
    
    axes[0].plot(data, label='Datos')
    axes[0].set_ylabel('Valor')
    axes[0].legend()
    axes[0].grid(True)
    
    axes[1].plot(means, label='Media Móvil', marker='o')
    axes[1].set_ylabel('Media')
    axes[1].legend()
    axes[1].grid(True)
    
    axes[2].plot(variances, label='Varianza Móvil', marker='o', color='r')
    axes[2].set_ylabel('Varianza')
    axes[2].set_xlabel('Número de Ventana')
    axes[2].legend()
    axes[2].grid(True)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ajustar para el título
    plt.show()

# --- 4. Ejecutar ---

# Datos estacionarios
stationary_data = simulate_stationary(num_steps=200)
check_stationarity_simple(stationary_data)

# Datos no estacionarios
non_stationary_data = simulate_non_stationary(num_steps=200)
check_stationarity_simple(non_stationary_data)