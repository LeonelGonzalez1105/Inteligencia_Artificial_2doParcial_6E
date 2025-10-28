# --- 1. Definir la Red (Probabilidades y Utilidades) ---

# Nodos de Azar (Óvalos)
# P(Dificultad_Examen)
prob_examen = {
    'Fácil': 0.6,
    'Difícil': 0.4
}

# Nodo de Utilidad (Rombo)
# U(Acción, Dificultad_Examen)
tabla_utilidad = {
    'Estudiar': {
        'Fácil': 80,
        'Difícil': 100
    },
    'Ir_Fiesta': {
        'Fácil': 50,
        'Difícil': -200
    }
}

# Nodo de Decisión (Rectángulo)
# Opciones que el agente puede tomar
decisiones_posibles = ['Estudiar', 'Ir_Fiesta']

# --- 2. El "Algoritmo": Calcular la Máxima Utilidad Esperada (MEU) ---

def calcular_mejor_decision(decisiones, probs_azar, tabla_utilidad):
    """
    Calcula la EU para cada decisión y elige la mejor.
    """
    
    mejor_decision = None
    max_eu = -float('inf')
    
    print("--- Agente de IA evaluando decisiones ---")
    
    # Iterar sobre cada ACCIÓN que podemos tomar
    for decision in decisiones:
        
        print(f"\nCalculando EU para la decisión: '{decision}'")
        expected_utility = 0.0
        
        # Calcular EU = Suma[ P(resultado) * U(decision, resultado) ]
        
        # Iterar sobre cada posible ESTADO DE AZAR
        for estado_azar, probabilidad in probs_azar.items():
            
            # Obtener la utilidad de esta combinación
            utilidad = tabla_utilidad[decision][estado_azar]
            
            # Sumar al promedio ponderado
            expected_utility += probabilidad * utilidad
            
            print(f"  -> P({estado_azar})={probabilidad} * "
                  f"U({decision}, {estado_azar})={utilidad}  "
                  f"[Contribución: {probabilidad * utilidad:.2f}]")
            
        print(f"  UTILIDAD ESPERADA (EU) TOTAL para '{decision}': {expected_utility:.2f}")
        
        # Comprobar si esta es la mejor decisión hasta ahora
        if expected_utility > max_eu:
            max_eu = expected_utility
            mejor_decision = decision

    return mejor_decision, max_eu

# --- 3. Ejecutar la decisión ---
decision_final, eu_final = calcular_mejor_decision(decisiones_posibles, 
                                                   prob_examen, 
                                                   tabla_utilidad)

print("\n--- Decisión Final del Agente ---")
print(f"La decisión óptima es: **{decision_final}**")
print(f"Con una Utilidad Esperada de: {eu_final:.2f}")