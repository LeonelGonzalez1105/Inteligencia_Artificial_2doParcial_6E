import numpy as np

# --- 1. Definir el HMM/DBN (Modelo del Mundo) ---

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

# --- Helper: Normalización ---
def normalize(dist):
    total = sum(dist.values())
    if total == 0: return {k: 1.0/len(dist) for k in dist} # Distribución uniforme si todo es 0
    return {key: val / total for key, val in dist.items()}

# --- 2. Algoritmo de Filtrado (Forward con Normalización) ---
#    Calcula P(X_t | E_{1:t})
def forward_filtering(observations, states, start_prob, T_model, S_model):
    T = len(observations)
    belief_history = [{s: 0.0 for s in states} for _ in range(T)]
    # Inicialización
    obs_0 = observations[0]
    alpha_0_unnorm = {s: start_prob[s] * S_model[s][obs_0] for s in states}
    belief_history[0] = normalize(alpha_0_unnorm)
    # Recursión
    for t in range(1, T):
        obs_t = observations[t]
        alpha_t_unnorm = {}
        for s_t in states:
            sum_term = sum(T_model[s_prev][s_t] * belief_history[t-1][s_prev] for s_prev in states)
            alpha_t_unnorm[s_t] = S_model[s_t][obs_t] * sum_term
        belief_history[t] = normalize(alpha_t_unnorm)
    return belief_history

# --- 3. Algoritmo de Predicción ---
#    Calcula P(X_{t+k} | E_{1:t})
def predict_future(filtered_belief_t, k_steps, T_model, states):
    current_belief = filtered_belief_t.copy()
    for _ in range(k_steps):
        next_belief = {s_next: sum(T_model[s_current][s_next] * current_belief[s_current] for s_current in states)
                       for s_next in states}
        current_belief = normalize(next_belief)
    return current_belief

# --- 4. Algoritmo de Suavizado (Forward-Backward) ---
#    Calcula P(X_k | E_{1:t})
def forward_algorithm_unnorm(observations, states, start_prob, T_model, S_model):
    T = len(observations)
    alpha = [{s: 0.0 for s in states} for _ in range(T)]
    obs_0 = observations[0]
    for s in states: alpha[0][s] = start_prob[s] * S_model[s][obs_0]
    for t in range(1, T):
        obs_t = observations[t]
        for s_t in states:
            sum_term = sum(T_model[s_prev][s_t] * alpha[t-1][s_prev] for s_prev in states)
            alpha[t][s_t] = S_model[s_t][obs_t] * sum_term
    return alpha

def backward_algorithm(observations, states, T_model, S_model):
    T = len(observations)
    beta = [{s: 1.0 for s in states} for _ in range(T)]
    for t in range(T-2, -1, -1):
        obs_next = observations[t+1]
        for s_k in states:
            beta[t][s_k] = sum(T_model[s_k][s_next] * S_model[s_next][obs_next] * beta[t+1][s_next]
                               for s_next in states)
    return beta

def forward_backward_smoothing(observations, states, start_prob, T_model, S_model):
    T = len(observations)
    alpha = forward_algorithm_unnorm(observations, states, start_prob, T_model, S_model)
    beta = backward_algorithm(observations, states, T_model, S_model)
    smoothed = [{s: 0.0 for s in states} for _ in range(T)]
    for k in range(T):
        unnormalized_prob = {s_k: alpha[k][s_k] * beta[k][s_k] for s_k in states}
        smoothed[k] = normalize(unnormalized_prob)
    return smoothed

# --- 5. Algoritmo de Explicación (Viterbi) ---
#    Calcula argmax_{x_{1:t}} P(X_{1:t} | E_{1:t})
def viterbi_algorithm(observations, states, start_prob, T_model, S_model):
    """Encuentra la secuencia de estados más probable."""
    T = len(observations)
    # delta[t][s] = max prob de la secuencia hasta t terminando en s
    delta = [{s: 0.0 for s in states} for _ in range(T)]
    # psi[t][s] = el estado anterior más probable que lleva a s en t
    psi = [{s: None for s in states} for _ in range(T)]

    # Inicialización (t=0)
    obs_0 = observations[0]
    for s in states:
        delta[0][s] = start_prob[s] * S_model[s][obs_0]

    # Recursión (t=1 hasta T-1)
    for t in range(1, T):
        obs_t = observations[t]
        for s_t in states: # Estado actual
            max_prob = -1.0
            best_prev_s = None
            for s_prev in states: # Estado anterior
                # Prob = P(obs_t|s_t) * P(s_t|s_prev) * delta_{t-1}(s_prev)
                prob = T_model[s_prev][s_t] * delta[t-1][s_prev]
                if prob > max_prob:
                    max_prob = prob
                    best_prev_s = s_prev

            # Guardar el max prob y el puntero
            delta[t][s_t] = S_model[s_t][obs_t] * max_prob
            psi[t][s_t] = best_prev_s

    # Terminación: Encontrar el final de la mejor secuencia
    best_last_state = max(states, key=lambda s: delta[T-1][s])
    prob_max_seq = delta[T-1][best_last_state] # Probabilidad de la secuencia

    # Backtracking: Reconstruir la secuencia
    sequence = [None] * T
    sequence[T-1] = best_last_state
    for t in range(T-2, -1, -1):
        sequence[t] = psi[t+1][sequence[t+1]]

    return sequence, prob_max_seq


# --- 6. Ejecutar y Mostrar Resultados ---

# La evidencia que recibimos
evidencia_dias = ['Lleva', 'Lleva', 'No Lleva']
T_total = len(evidencia_dias)

print(f"--- Ejecutando Inferencia en el Tiempo ---")
print(f"Evidencia E(1:{T_total}): {evidencia_dias}\n")

# --- Tarea 1: Filtrado ---
print("--- 1. Filtrado P(X_t | E_{1:t}) ---")
creencias_filtradas = forward_filtering(evidencia_dias, STATES, START_PROB, TRANSITION_MODEL, SENSOR_MODEL)
for t, belief in enumerate(creencias_filtradas):
    print(f"Día t={t+1}: ", end="")
    for state, prob in belief.items(): print(f"P({state})={prob:.3f} ", end="")
    print()

# --- Tarea 2: Predicción ---
print("\n--- 2. Predicción P(X_{t+k} | E_{1:t}) ---")
creencia_dia_3 = creencias_filtradas[-1]
prediccion_dia_4 = predict_future(creencia_dia_3, 1, TRANSITION_MODEL, STATES)
print(f"Predicción para Día t={T_total+1} (k=1): ", end="")
for state, prob in prediccion_dia_4.items(): print(f"P({state})={prob:.3f} ", end="")
print()

# --- Tarea 3: Suavizado ---
print("\n--- 3. Suavizado P(X_k | E_{1:t}) ---")
probabilidades_suavizadas = forward_backward_smoothing(evidencia_dias, STATES, START_PROB, TRANSITION_MODEL, SENSOR_MODEL)
for k, belief in enumerate(probabilidades_suavizadas):
    print(f"Día k={k+1}: ", end="")
    for state, prob in belief.items(): print(f"P({state})={prob:.3f} ", end="")
    print()

# --- Tarea 4: Explicación ---
print("\n--- 4. Explicación (Secuencia más probable) ---")
secuencia_optima, prob_secuencia = viterbi_algorithm(evidencia_dias, STATES, START_PROB, TRANSITION_MODEL, SENSOR_MODEL)
print(f"La secuencia de clima más probable es: {secuencia_optima}")
print(f"(Probabilidad de esta secuencia: {prob_secuencia:.6f})")