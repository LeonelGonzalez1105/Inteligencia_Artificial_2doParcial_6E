import random

# --- 1. Definir los Parámetros del HMM ---

# P(X_0) - Probabilidades Iniciales (Creencia del primer día)
START_PROB = {'Lluvioso': 0.5, 'Soleado': 0.5}

# P(X_t | X_{t-1}) - Matriz de Transición (El clima es persistente)
TRANSITION_MODEL = {
    'Lluvioso': { 'Lluvioso': 0.7, 'Soleado': 0.3 }, # Si llovió hoy, 70% de que llueva mañana
    'Soleado':  { 'Lluvioso': 0.2, 'Soleado': 0.8 }  # Si estuvo soleado hoy, 80% de que siga soleado
}

# P(E_t | X_t) - Matriz de Emisión/Sensor (El guardia no es perfecto)
SENSOR_MODEL = {
    'Lluvioso': { 'Lleva': 0.9, 'No Lleva': 0.1 }, # Si llueve, 90% de que lleve paraguas
    'Soleado':  { 'Lleva': 0.2, 'No Lleva': 0.8 }  # Si está soleado, 20% de que lo lleve (por si acaso)
}

# --- 2. Helper: Muestreador Ponderado ---

def sample_from_prob(distribution):
    """
    Toma un diccionario de {resultado: prob} y devuelve un resultado
    basado en un lanzamiento de dado ponderado.
    """
    rand_val = random.random() # Un número aleatorio entre 0.0 y 1.0
    cumulative_prob = 0.0
    
    for outcome, prob in distribution.items():
        cumulative_prob += prob
        if rand_val < cumulative_prob:
            return outcome
            
    return list(distribution.keys())[-1] # Fallback

# --- 3. El "Algoritmo": Simulador de HMM ---

def simulate_hmm(start_prob, T_model, S_model, num_steps):
    """
    Genera una secuencia de estados ocultos y observaciones
    siguiendo las reglas del HMM.
    """
    
    hidden_states = []
    observed_data = []

    # --- Día 0: Inicialización ---
    # 1. Muestrear el estado inicial oculto
    current_state = sample_from_prob(start_prob)
    hidden_states.append(current_state)
    
    # 2. Muestrear la primera observación basada en el estado inicial
    observation = sample_from_prob(S_model[current_state])
    observed_data.append(observation)

    # --- Días 1 a N: Bucle de Markov ---
    for _ in range(1, num_steps):
        
        # 3. Transición: Muestrear el *siguiente estado oculto*
        #    basado en el estado oculto *actual*
        next_state = sample_from_prob(T_model[current_state])
        hidden_states.append(next_state)
        
        # 4. Emisión: Muestrear la *observación visible*
        #    basada en el *nuevo estado oculto*
        observation = sample_from_prob(S_model[next_state])
        observed_data.append(observation)
        
        # Actualizar el estado para el siguiente ciclo
        current_state = next_state 

    return hidden_states, observed_data

# --- 4. Ejecutar la Simulación ---
NUM_DIAS = 10
print(f"--- Simulando un HMM (Clima y Paraguas) por {NUM_DIAS} días ---")

# Generar las secuencias
estados_reales, observaciones_generadas = simulate_hmm(
    START_PROB, 
    TRANSITION_MODEL, 
    SENSOR_MODEL, 
    NUM_DIAS
)

print("\n--- Resultados de la Simulación ---")
print("Estados Ocultos (Lo que realmente pasó con el clima):")
print(estados_reales)

print("\nObservaciones (Lo que 'vimos' - el paraguas):")
print(observaciones_generadas)

print("\n(Nota: La tarea de un algoritmo de inferencia, como Viterbi,")
print("sería adivinar la primera lista usando solo la segunda lista.)")