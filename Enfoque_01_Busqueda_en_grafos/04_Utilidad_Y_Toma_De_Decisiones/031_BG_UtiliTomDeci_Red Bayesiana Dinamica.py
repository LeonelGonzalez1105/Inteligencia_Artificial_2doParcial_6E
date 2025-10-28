# --- 1. Definir la DBN (los modelos) ---

# P(X_0) - Red Previa (Creencia inicial)
# Empezamos 50/50 sin saber nada.
belief = {
    'Lluvioso': 0.5,
    'Soleado': 0.5
}

# P(X_t | X_{t-1}) - Modelo de Transición
# El clima es "persistente"
transition_model = {
    # Si ayer estuvo Lluvioso (X_{t-1})
    'Lluvioso': { 'Lluvioso': 0.7, 'Soleado': 0.3 }, # 70% de que siga lloviendo
    # Si ayer estuvo Soleado (X_{t-1})
    'Soleado': { 'Lluvioso': 0.2, 'Soleado': 0.8 }  # 20% de que empiece a llover
}

# P(E_t | X_t) - Modelo de Sensor/Observación
sensor_model = {
    # Si hoy está Lluvioso (X_t)
    'Lluvioso': { 'Lleva': 0.9, 'No Lleva': 0.1 }, # 90% prob de que lleve paraguas
    # Si hoy está Soleado (X_t)
    'Soleado': { 'Lleva': 0.2, 'No Lleva': 0.8 }  # 20% prob de que lo lleve
}

# --- 2. El "Algoritmo": Filtrado (Forward Algorithm) ---

def forward_filter_step(prior_belief, evidence, T_model, S_model):
    """
    Realiza un ciclo completo de Predicción y Actualización.
    """
    
    # --- PASO 1: PREDICCIÓN (Time Update) ---
    # P(X_t) = Suma_xt-1 [ P(X_t | xt-1) * P(xt-1) ]
    
    predicted_belief = {'Lluvioso': 0.0, 'Soleado': 0.0}
    
    for state_prior, prob_prior in prior_belief.items():
        for state_posterior, prob_trans in T_model[state_prior].items():
            
            # Acumulamos la probabilidad de este estado posterior
            predicted_belief[state_posterior] += prob_trans * prob_prior
            
    print(f"  Predicción P(Clima) (antes de ver): {predicted_belief}")

    # --- PASO 2: ACTUALIZACIÓN (Measurement Update) ---
    # P(X_t|e) = alfa * P(e|X_t) * P(X_t)
    
    updated_belief_unnorm = {'Lluvioso': 0.0, 'Soleado': 0.0}
    normalizer = 0.0
    
    for state, prob_predicted in predicted_belief.items():
        
        # P(e|X_t)
        prob_evidence_given_state = S_model[state][evidence]
        
        # P(e|X_t) * P(X_t)
        likelihood = prob_evidence_given_state * prob_predicted
        updated_belief_unnorm[state] = likelihood
        
        # Sumar al normalizador
        normalizer += likelihood
        
    # Normalizar
    final_belief = {'Lluvioso': 0.0, 'Soleado': 0.0}
    if normalizer > 0:
        for state, val in updated_belief_unnorm.items():
            final_belief[state] = val / normalizer
            
    return final_belief

# --- 3. Simulación a través del tiempo ---

# La evidencia que recibimos día a día
evidencia_dias = ['Lleva', 'Lleva', 'No Lleva']

print(f"--- Simulación de DBN (Espía del Clima) ---")
print(f"Creencia Inicial (Día 0): {belief}\n")

current_belief = belief

for i, evidencia in enumerate(evidencia_dias):
    
    print(f"--- Día {i+1} ---")
    print(f"Evidencia Observada: '{evidencia}'")
    
    # Ejecutar el algoritmo de filtrado
    current_belief = forward_filter_step(current_belief, 
                                         evidencia, 
                                         transition_model, 
                                         sensor_model)
                                         
    print(f"Creencia Final P(Clima | Evidencia 1:{i+1}): "
          f"Lluvioso: {current_belief['Lluvioso']:.3f}, "
          f"Soleado: {current_belief['Soleado']:.3f}\n")