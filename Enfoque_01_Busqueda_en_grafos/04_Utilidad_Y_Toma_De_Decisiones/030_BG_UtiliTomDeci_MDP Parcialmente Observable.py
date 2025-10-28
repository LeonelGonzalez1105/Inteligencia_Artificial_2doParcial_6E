import collections

# --- 1. Definir el POMDP ---

# S: Estados (las 4 habitaciones)
STATES = ['S0', 'S1', 'S2', 'S3']
# O: Observaciones
OBSERVATIONS = ['Ver Puerta', 'Ver Muro']
# A: Acciones
ACTIONS = ['Mover Derecha']

# T(s, a, s'): Modelo de Transición (Mover Derecha)
# P(s_destino | s_origen, 'Mover Derecha')
TRANSITION_MODEL = {
    'S0': {'S0': 0.2, 'S1': 0.8},  # 80% éxito (a S1), 20% fallo (en S0)
    'S1': {'S1': 0.2, 'S2': 0.8},
    'S2': {'S2': 0.2, 'S3': 0.8},
    'S3': {'S3': 1.0}             # Se queda en S3 (límite)
}

# E(s, o): Modelo de Observación P(o | s)
OBSERVATION_MODEL = {
    'S0': {'Ver Puerta': 0.1, 'Ver Muro': 0.9}, # Falsa alarma
    'S1': {'Ver Puerta': 0.1, 'Ver Muro': 0.9}, # Falsa alarma
    'S2': {'Ver Puerta': 0.9, 'Ver Muro': 0.1}, # ¡Aquí está la puerta!
    'S3': {'Ver Puerta': 0.1, 'Ver Muro': 0.9}  # Falsa alarma
}

# --- 2. El "Algoritmo": El Ciclo de Actualización de Creencia ---

def pomdp_cycle(belief_state, action, observation):
    """
    Realiza un ciclo completo de actualización de creencia.
    
    Args:
        belief_state (dict): La creencia P(s) *antes* de la acción.
        action (str): La acción tomada (ej. 'Mover Derecha').
        observation (str): La observación recibida (ej. 'Ver Muro').
    """
    
    print(f"\n--- INICIANDO CICLO POMDP ---")
    print(f"Creencia Actual P(s): \t{belief_state}")
    print(f"Acción Tomada: \t\t{action}")
    
    # --- PASO 1: PREDICCIÓN (Actualización de Acción) ---
    # El agente "imagina" a dónde se movió. La creencia se "desenfoca".
    # P(s') = Suma_s [ T(s'|s,a) * P(s) ]
    
    predicted_belief = {s: 0.0 for s in STATES}
    
    for s_prior, prob_s_prior in belief_state.items():
        # Para cada estado donde *podríamos* haber estado...
        
        # ...vemos a dónde nos lleva la acción
        for s_posterior, prob_trans in TRANSITION_MODEL[s_prior].items():
            
            # Acumulamos la probabilidad de terminar en 's_posterior'
            predicted_belief[s_posterior] += prob_trans * prob_s_prior

    print(f"Creencia Predicha P(s'): \t{predicted_belief} (desenfocada)")
    
    # --- PASO 2: OBSERVACIÓN y ACTUALIZACIÓN ---
    # El agente "enfoca" su creencia usando la observación.
    # P(s'|o) = Normalizador * P(o|s') * P(s')
    
    print(f"Observación Recibida: \t{observation}")
    
    new_belief_unnormalized = {}
    normalizer = 0.0
    
    for state, prob_state in predicted_belief.items():
        
        # P(o|s')
        prob_o_given_s = OBSERVATION_MODEL[state][observation]
        
        # P(o|s') * P(s')
        likelihood = prob_o_given_s * prob_state
        new_belief_unnormalized[state] = likelihood
        
        # Acumular el normalizador P(o)
        normalizer += likelihood
        
    # Normalizar para que sume 1
    final_belief = {s: 0.0 for s in STATES}
    if normalizer > 0:
        for state, val in new_belief_unnormalized.items():
            final_belief[state] = val / normalizer
            
    # Redondear para legibilidad
    final_belief_rounded = {s: round(p, 3) for s, p in final_belief.items()}
    print(f"Creencia Final P(s'|o): \t{final_belief_rounded} (enfocada)")
    
    return final_belief

# --- 3. Simulación ---

# Creencia inicial: 50/50 en S0 o S1
current_belief = {'S0': 0.5, 'S1': 0.5, 'S2': 0.0, 'S3': 0.0}

# --- CICLO 1 ---
# Acción: Mover Derecha
# Observación: "Ver Muro" (mala suerte, no vio la puerta)
current_belief = pomdp_cycle(current_belief, 
                             action='Mover Derecha', 
                             observation='Ver Muro')

# --- CICLO 2 ---
# El robot vuelve a intentarlo desde su nueva creencia
# Acción: Mover Derecha
# Observación: "Ver Puerta" (¡la encontró!)
current_belief = pomdp_cycle(current_belief, 
                             action='Mover Derecha', 
                             observation='Ver Puerta')