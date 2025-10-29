import numpy as np

# --- 1. Definir los Estados ---
states = ['Soleado', 'Lluvioso']
state_to_index = {state: i for i, state in enumerate(states)} # Mapeo a índices (0, 1)

# --- 2. El "Algoritmo": Definir la Matriz de Transición T ---
# T[i, j] = P(Estado j mañana | Estado i hoy)

# Filas: Estado actual (0: Soleado, 1: Lluvioso)
# Columnas: Siguiente estado (0: Soleado, 1: Lluvioso)
transition_matrix = np.array([
    # Hoy Soleado
    [0.8, 0.2],  # Mañana: 80% Soleado, 20% Lluvioso
    # Hoy Lluvioso
    [0.4, 0.6]   # Mañana: 40% Soleado, 60% Lluvioso
])

# --- 3. Uso Conceptual ---
def check_markov_property(matrix, current_state_index):
    """
    Verifica que las probabilidades para el siguiente estado
    solo dependen del estado actual.
    """
    next_state_probs = matrix[current_state_index, :]
    print(f"\n--- Comprobando Hipótesis de Markov ---")
    print(f"Si el estado actual es '{states[current_state_index]}':")
    print(f"  La distribución de probabilidad para el *siguiente* estado es:")
    for next_state, prob in zip(states, next_state_probs):
        print(f"    P(Mañana={next_state} | Hoy={states[current_state_index]}) = {prob:.2f}")
    # ¡No necesitamos saber nada más del pasado!

# --- 4. Ejecutar ---
print("--- Matriz de Transición (Modelo de Markov) ---")
print(transition_matrix)

# Demostración: Predecir mañana si hoy está Soleado
check_markov_property(transition_matrix, state_to_index['Soleado'])
# Demostración: Predecir mañana si hoy está Lluvioso
check_markov_property(transition_matrix, state_to_index['Lluvioso'])