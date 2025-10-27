import time

# --- El "Mundo" (El mapa que el agente NO puede ver) ---
# Tiene un "callejón sin salida" costoso en 'C'
# y el camino óptimo A -> B -> D -> G
# Los costos están en las aristas.
WORLD_MAP = {
    'A': {'B': 1, 'C': 1},
    'B': {'A': 1, 'D': 1},
    'C': {'A': 1, 'F': 10}, # 'F' es un callejón sin salida caro
    'D': {'B': 1, 'G': 1},
    'F': {'C': 10},
    'G': {} # El Objetivo
}
GOAL_STATE = 'G'

# --- Función de Heurística Inicial (Una mala suposición) ---
# El agente cree que todo está "cerca" (ej. h=1)
def initial_heuristic(state, goal):
    if state == goal:
        return 0
    return 1 # Una heurística muy simple y mala

# --- El Agente (El algoritmo LRTA*) ---

def online_lrta_search(start_state, goal_state):
    
    # 1. El "cerebro" (memoria) del agente.
    #    Guarda la heurística aprendida H[s]
    H_learned = {}
    
    current_state = start_state
    path_taken = [current_state]
    
    print(f"Agente iniciando en: '{current_state}'")
    
    while current_state != goal_state:
        print(f"\nAgente está en: '{current_state}'")
        
        # 2. Inicializar H[s] si es la primera vez que visita este estado
        if current_state not in H_learned:
            H_learned[current_state] = initial_heuristic(current_state, goal_state)
            
        # 3. Mirar a los vecinos y calcular f(s')
        best_next_state = None
        min_f_cost = float('inf')
        
        print("  Agente mira a su alrededor...")
        # (El agente "pregunta" al mundo por sus opciones)
        possible_actions = WORLD_MAP.get(current_state, {}).items()
        
        if not possible_actions:
            print("  ¡CALLEJÓN SIN SALIDA! Retrocediendo.")
            # (En un LRTA* real, el "path_taken" nos ayudaría a
            #  saber a dónde retroceder. Aquí simplificamos.)
            break 
            
        for neighbor, step_cost in possible_actions:
            
            # Inicializar H[s'] del vecino si no lo conoce
            if neighbor not in H_learned:
                H_learned[neighbor] = initial_heuristic(neighbor, goal_state)
            
            # 4. Calcular el costo f(s') = costo_real + H_aprendida[s']
            f_cost = step_cost + H_learned[neighbor]
            
            print(f"    -> Opción: Moverse a '{neighbor}'. "
                  f"Costo = {step_cost} (paso) + {H_learned[neighbor]} (H aprendida) "
                  f"= {f_cost}")
            
            if f_cost < min_f_cost:
                min_f_cost = f_cost
                best_next_state = neighbor

        # 5. "Aprender" - Actualizar la heurística del estado actual
        print(f"  [APRENDIZAJE]: Agente actualiza H['{current_state}'] = {min_f_cost}")
        H_learned[current_state] = min_f_cost
        
        # 6. "Actuar" - Moverse al mejor estado
        current_state = best_next_state
        path_taken.append(current_state)
        print(f"  [ACCIÓN]: Agente se mueve a '{current_state}'")
        time.sleep(1)

    print(f"\n¡Objetivo '{goal_state}' alcanzado!")
    print(f"Camino real tomado: {' -> '.join(path_taken)}")
    print(f"Heurísticas finales aprendidas: {H_learned}")
    return path_taken

# --- Ejecutamos la simulación ---
# La primera vez, el agente podría cometer un error
print("--- PRIMERA EJECUCIÓN (Aprendiendo de Cero) ---")
online_lrta_search('A', 'G')

# Si lo ejecutáramos de nuevo, ¡usaría las H aprendidas
# y (probablemente) tomaría el camino óptimo a la primera!