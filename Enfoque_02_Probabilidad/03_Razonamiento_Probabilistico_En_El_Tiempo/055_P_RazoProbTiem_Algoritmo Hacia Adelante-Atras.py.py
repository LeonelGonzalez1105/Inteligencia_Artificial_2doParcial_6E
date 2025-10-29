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

# --- 2. Algoritmo Hacia Delante (Forward Pass) ---
#    Calcula alpha_t = P(X_t , E_{1:t})

def forward_algorithm(observations, states, start_prob, T_model, S_model):
    """Calcula los mensajes forward (alpha) para toda la secuencia."""
    T = len(observations)
    alpha = [{s: 0.0 for s in states} for _ in range(T)] # Lista de diccionarios

    # Paso 1: Inicialización (t=0)
    # alpha_0(s) = P(X_0=s) * P(E_0 | X_0=s)
    obs_0 = observations[0]
    for s in states:
        alpha[0][s] = start_prob[s] * S_model[s][obs_0]

    # Paso 2: Recursión (t=1 hasta T-1)
    # alpha_t(s_t) = P(E_t|s_t) * Suma_s_{t-1} [ P(s_t | s_{t-1}) * alpha_{t-1}(s_{t-1}) ]
    for t in range(1, T):
        obs_t = observations[t]
        for s_t in states: # Estado actual
            sum_term = 0.0
            for s_prev in states: # Estado anterior
                sum_term += T_model[s_prev][s_t] * alpha[t-1][s_prev]

            alpha[t][s_t] = S_model[s_t][obs_t] * sum_term

    return alpha # Devuelve la lista de alphas NO normalizados

# --- 3. Algoritmo Hacia Atrás (Backward Pass) ---
#    Calcula beta_k = P(E_{k+1:t} | X_k)

def backward_algorithm(observations, states, T_model, S_model):
    """Calcula los mensajes backward (beta) para toda la secuencia."""
    T = len(observations)
    beta = [{s: 0.0 for s in states} for _ in range(T)] # Lista de diccionarios

    # Paso 1: Inicialización (t=T-1)
    # beta_{T-1}(s) = 1 (por definición)
    for s in states:
        beta[T-1][s] = 1.0

    # Paso 2: Recursión (t=T-2 hasta 0)
    # beta_k(s_k) = Suma_s_{k+1} [ P(s_{k+1} | s_k) * P(E_{k+1} | s_{k+1}) * beta_{k+1}(s_{k+1}) ]
    for t in range(T-2, -1, -1): # Itera hacia atrás
        obs_next = observations[t+1] # Evidencia del SIGUIENTE paso
        for s_k in states: # Estado actual (k)
            sum_term = 0.0
            for s_next in states: # Estado siguiente (k+1)
                prob_transition = T_model[s_k][s_next]
                prob_evidence = S_model[s_next][obs_next]
                beta_next = beta[t+1][s_next]
                sum_term += prob_transition * prob_evidence * beta_next

            beta[t][s_k] = sum_term

    return beta # Devuelve la lista de betas

# --- 4. Algoritmo de Suavizado (Smoothing) ---
#    Calcula P(X_k | E_{1:t}) = alpha * alpha_k * beta_k

def forward_backward_smoothing(observations, states, start_prob, T_model, S_model):
    """Calcula las probabilidades suavizadas para cada paso de tiempo k."""
    T = len(observations)
    
    # Calcular mensajes forward y backward
    alpha = forward_algorithm(observations, states, start_prob, T_model, S_model)
    beta = backward_algorithm(observations, states, T_model, S_model)
    
    smoothed = [{s: 0.0 for s in states} for _ in range(T)]

    print("\n--- Mensajes Calculados ---")
    print("Alpha (Forward):")
    for t, a_t in enumerate(alpha): print(f"  t={t}: {a_t}")
    print("Beta (Backward):")
    for t, b_t in enumerate(beta): print(f"  t={t}: {b_t}")

    # Combinar y Normalizar para cada k
    for k in range(T):
        unnormalized_prob = {}
        normalizer = 0.0
        for s_k in states:
            # P(X_k, E_{1:t}) = alpha_k(s_k) * beta_k(s_k)
            product = alpha[k][s_k] * beta[k][s_k]
            unnormalized_prob[s_k] = product
            normalizer += product
        
        # Normalizar para obtener P(X_k | E_{1:t})
        if normalizer > 0:
            for s_k in states:
                smoothed[k][s_k] = unnormalized_prob[s_k] / normalizer
                
    return smoothed

# --- 5. Ejecutar la Simulación ---

# La evidencia que recibimos (la misma de antes)
evidencia_dias = ['Lleva', 'Lleva', 'No Lleva']
T_total = len(evidencia_dias)

print(f"--- Ejecutando Suavizado (Forward-Backward) ---")
print(f"Evidencia E(1:{T_total}): {evidencia_dias}")

# Ejecutar el algoritmo completo
probabilidades_suavizadas = forward_backward_smoothing(
    evidencia_dias,
    STATES,
    START_PROB,
    TRANSITION_MODEL,
    SENSOR_MODEL
)

# --- 6. Mostrar Resultados ---
print("\n--- Resultados del Suavizado P(X_k | E_1:3) ---")
for k, dist in enumerate(probabilidades_suavizadas):
    print(f"Día k={k+1}: ", end="")
    for state, prob in dist.items():
        print(f"P({state})={prob:.3f} ", end="")
    print()

# Compara con el resultado del Filtrado para el último día (k=3)
# Deberían ser iguales
print(f"\n(Resultado del Filtrado para el día 3 fue: P(Lluvioso)=0.178, P(Soleado)=0.822)")