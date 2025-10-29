import random

def create_distribution(outcomes_with_probs):
    """
    Crea una distribución y se asegura de que sume 1.0.
    """
    total_prob = sum(outcomes_with_probs.values())
    
    # Comprobación de sanidad
    if not 0.999 < total_prob < 1.001:
        print(f"¡Error! Las probabilidades suman {total_prob}, no 1.0")
        return None
        
    return outcomes_with_probs

def sample_from_distribution(distribution, num_samples=1):
    """
    El "algoritmo": Toma 'num_samples' muestras de la distribución
    (lanza un dado ponderado).
    
    Args:
        distribution (dict): El diccionario P(X).
        num_samples (int): Cuántas muestras tomar.
    """
    
    # 1. Separar los resultados y sus probabilidades (pesos)
    outcomes = list(distribution.keys())
    probabilities = list(distribution.values())
    
    # 2. Usar random.choices para muestrear
    # k = número de muestras a tomar
    samples = random.choices(outcomes, weights=probabilities, k=num_samples)
    
    return samples

# --- 1. Definir la Distribución de Probabilidad P(Clima) ---
# Esta es nuestra "regla" del mundo
weather_distribution = create_distribution({
    'Soleado': 0.6,
    'Lluvioso': 0.3,
    'Nublado': 0.1
})

print(f"--- Distribución de Probabilidad P(Clima) ---")
print(weather_distribution)

# --- 2. "Algoritmo" de Muestreo ---
print("\n--- Muestreando 10 días del Clima ---")

# Simular 10 días usando la distribución
simulated_week = sample_from_distribution(weather_distribution, num_samples=10)

print(simulated_week)

# Contar los resultados para ver si se parece a la distribución
from collections import Counter
print("\n--- Frecuencias de la simulación ---")
print(Counter(simulated_week))