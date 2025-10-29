import random
import numpy as np

# --- 1. Definir el HMM (Modelo del Mundo) ---

STATES = ['Lluvioso', 'Soleado']
OBSERVATIONS = ['Lleva', 'No Lleva']
START_PROB = {'Lluvioso': 0.5, 'Soleado': 0.5} # P(X_0)

TRANSITION_MODEL = { # P(X_t | X_{t-1})
    'Lluvioso': { 'Lluvioso': 0.7, 'Soleado': 0.3 },
    'Soleado': { 'Lluvioso': 0.2, 'Soleado': 0.8 }
}

SENSOR_MODEL = { # P(E_t | X_t)
    'Lluvioso': { 'Lleva': 0.9, 'No Lleva': 0.1 },
    'Soleado': { 'Lleva': 0.2, 'No Lleva': 0.8 }
}

# --- Helper: Muestrear de una distribución ---
def sample_from_prob(distribution):
    rand_val = random.random()
    cumulative_prob = 0.0
    for outcome, prob in distribution.items():
        cumulative_prob += prob
        if rand_val < cumulative_prob:
            return outcome
    # fallback needed due to potential floating point issues
    return list(distribution.keys())[-1]

# --- 2. Simular el HMM para generar datos ---
def simulate_hmm(hmm_params, num_steps):
    """
    Genera una secuencia de estados ocultos y observaciones
    siguiendo las reglas del HMM.
    """
    states = hmm_params['states']
    start_prob = hmm_params['start_prob']
    T_model = hmm_params['transition_model']
    S_model = hmm_params['sensor_model']

    hidden_states = []
    observed_data = []

    # Día 0
    current_state = sample_from_prob(start_prob)
    hidden_states.append(current_state)
    observation = sample_from_prob(S_model[current_state])
    observed_data.append(observation)

    # Días 1 hasta num_steps-1
    for _ in range(1, num_steps):
        # Transición al siguiente estado oculto
        next_state = sample_from_prob(T_model[current_state])
        hidden_states.append(next_state)
        # Generar observación desde el nuevo estado
        observation = sample_from_prob(S_model[next_state])
        observed_data.append(observation)
        current_state = next_state # Actualizar estado para el siguiente ciclo

    return hidden_states, observed_data

# --- 3. Algoritmo de Viterbi (para inferencia) ---
#    (Mismo código que en el tema anterior)
def viterbi_algorithm(observations, states, start_prob, T_model, S_model):
    T = len(observations)
    delta = [{s: 0.0 for s in states} for _ in range(T)]
    psi = [{s: None for s in states} for _ in range(T)]
    # Inicialización
    obs_0 = observations[0]
    for s in states:
        delta[0][s] = start_prob[s] * S_model[s][obs_0]
    # Recursión
    for t in range(1, T):
        obs_t = observations[t]
        for s_t in states:
            max_prob = -1.0
            best_prev_s = None
            for s_prev in states:
                prob = delta[t-1][s_prev] * T_model[s_prev][s_t] # No multiplicar por sensor aquí
                if prob > max_prob:
                    max_prob = prob
                    best_prev_s = s_prev
            # Guardar max prob * P(obs|estado actual) y puntero
            delta[t][s_t] = max_prob * S_model[s_t][obs_t] # Multiplicar por sensor aquí
            psi[t][s_t] = best_prev_s
    # Terminación
    prob_max_seq = max(delta[T-1].values())
    best_last_state = max(states, key=lambda s: delta[T-1][s])
    # Backtracking
    sequence = [None] * T
    sequence[T-1] = best_last_state
    for t in range(T-2, -1, -1):
        sequence[t] = psi[t+1][sequence[t+1]]
    return sequence, prob_max_seq

# --- 4. Ejecutar la Simulación e Inferencia ---

# Parámetros del HMM
hmm_parameters = {
    'states': STATES,
    'observations': OBSERVATIONS,
    'start_prob': START_PROB,
    'transition_model': TRANSITION_MODEL,
    'sensor_model': SENSOR_MODEL
}

# Generar una secuencia de 7 días
NUM_DIAS = 7
print(f"--- Simulando el HMM por {NUM_DIAS} días ---")
estados_reales, observaciones_generadas = simulate_hmm(hmm_parameters, NUM_DIAS)

print(f"Secuencia de Estados Ocultos (Clima Real): \t{estados_reales}")
print(f"Secuencia de Observaciones Visibles (Paraguas): \t{observaciones_generadas}")

# Ahora, usar Viterbi para *adivinar* los estados ocultos *solo*
# viendo las observaciones generadas.
print("\n--- Aplicando Viterbi para inferir el Clima (Estado Oculto) ---")
print(f"Usando solo las observaciones: {observaciones_generadas}")

secuencia_inferida, prob_inferida = viterbi_algorithm(
    observaciones_generadas,
    STATES,
    START_PROB,
    TRANSITION_MODEL,
    SENSOR_MODEL
)

print(f"\nSecuencia de Clima Inferida por Viterbi: \t{secuencia_inferida}")
print(f"Clima Real (para comparar): \t\t\t{estados_reales}")

# Calcular la precisión
correctos = sum(1 for real, inferido in zip(estados_reales, secuencia_inferida) if real == inferido)
precision = correctos / NUM_DIAS
print(f"\nPrecisión de la inferencia: {correctos}/{NUM_DIAS} = {precision*100:.2f}%")