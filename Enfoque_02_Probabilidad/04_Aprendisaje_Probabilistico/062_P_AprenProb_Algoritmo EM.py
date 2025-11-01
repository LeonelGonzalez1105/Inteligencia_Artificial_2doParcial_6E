import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm # Para la función de densidad Gaussiana (pdf)

# --- 1. Simulación: Generar los Datos (El "Mundo Real") ---
# (El algoritmo EM NO verá estos parámetros)
np.random.seed(42)
N = 300 # Número total de puntos
# Grupo A (Oculto)
mean_A_real = 10
std_A_real = 2
data_A = np.random.normal(mean_A_real, std_A_real, int(N * 0.4)) # 40%
# Grupo B (Oculto)
mean_B_real = 20
std_B_real = 3
data_B = np.random.normal(mean_B_real, std_B_real, int(N * 0.6)) # 60%

# Mezclamos los datos. ¡El algoritmo solo ve esto!
X = np.concatenate((data_A, data_B))
np.random.shuffle(X)

# --- 2. Algoritmo EM para Mezcla Gaussiana (GMM) ---

def run_em_gmm(X_data, k=2, max_iterations=100, tolerance=1e-4):
    """
    Implementa el algoritmo EM para una Mezcla de k Gaussianas en 1D.
    """
    
    # --- a. Inicialización (Adivinanzas Aleatorias) ---
    print("Iniciando EM...")
    # Adivinamos medias iniciales eligiendo puntos al azar
    means = np.random.choice(X_data, k, replace=False)
    # Adivinamos varianzas iniciales (usamos la varianza total)
    variances = np.array([np.var(X_data)] * k)
    # Adivinamos pesos iniciales (uniformes)
    weights = np.array([1/k] * k)
    
    print(f"Parámetros Iniciales (Adivinanza):")
    print(f"  Medias: {means}")
    print(f"  Varianzas: {variances}")
    
    for i in range(max_iterations):
        
        # --- b. E-Step (Paso de Expectativa) ---
        # Calcular "responsabilidades" P(Grupo k | punto x_n)
        
        # P(x_n | Grupo k) * P(Grupo k)
        likelihoods = np.zeros((X_data.shape[0], k))
        for j in range(k):
            likelihoods[:, j] = weights[j] * norm.pdf(X_data, means[j], np.sqrt(variances[j]))
            
        # Normalizar para obtener responsabilidades
        sum_likelihoods = np.sum(likelihoods, axis=1, keepdims=True)
        responsibilities = likelihoods / (sum_likelihoods + 1e-10) # Añadir epsilon
        
        # --- c. M-Step (Paso de Maximización) ---
        # Re-calcular parámetros usando las responsabilidades como pesos
        
        # Nk = Suma de responsabilidades para el grupo k
        Nk = np.sum(responsibilities, axis=0)
        
        # Nuevas Medias (Promedio Ponderado)
        new_means = np.sum(X_data[:, np.newaxis] * responsibilities, axis=0) / Nk
        
        # Nuevas Varianzas (Varianza Ponderada)
        new_variances = np.sum(responsibilities * (X_data[:, np.newaxis] - new_means)**2, axis=0) / Nk
        
        # Nuevos Pesos
        new_weights = Nk / X_data.shape[0]
        
        # --- d. Comprobar Convergencia ---
        mean_diff = np.sum(np.abs(new_means - means))
        if mean_diff < tolerance:
            print(f"\nConvergencia alcanzada en la iteración {i+1}.")
            break
            
        # Actualizar parámetros para la siguiente iteración
        means, variances, weights = new_means, new_variances, new_weights

    print("--- EM Finalizado ---")
    return means, variances, weights

# --- 3. Ejecutar y Visualizar ---

# Ejecutar el algoritmo
means_em, variances_em, weights_em = run_em_gmm(X, k=2)

print("\n--- Parámetros Reales (Ocultos) ---")
print(f"Medias: [{mean_A_real}, {mean_B_real}], Varianzas: [{std_A_real**2:.2f}, {std_B_real**2:.2f}], Pesos: [0.4, 0.6]")

print("\n--- Parámetros Aprendidos por EM ---")
# (El orden puede estar invertido, ej. A=20, B=10)
print(f"Medias: {means_em}, Varianzas: {variances_em}, Pesos: {weights_em}")

# --- 4. Visualización ---
plt.figure(figsize=(12, 6))
# Histograma de los datos (lo que el algoritmo ve)
plt.hist(X, bins=30, density=True, alpha=0.6, label='Datos Observados (Mezclados)')

# Graficar las Gaussianas aprendidas
x_axis = np.linspace(X.min(), X.max(), 100)
for i in range(len(means_em)):
    label = f'Grupo {i+1} (Aprendido por EM)\n$\mu$={means_em[i]:.2f}, $\sigma^2$={variances_em[i]:.2f}'
    plt.plot(x_axis, weights_em[i] * norm.pdf(x_axis, means_em[i], np.sqrt(variances_em[i])), 
             'r--', linewidth=2, label=label)

plt.title('Algoritmo EM para Mezcla de Gaussianas (GMM)')
plt.xlabel('Valor del Dato')
plt.ylabel('Densidad')
plt.legend()
plt.grid(True)
plt.show()