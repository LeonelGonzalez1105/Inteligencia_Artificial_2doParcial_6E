import collections

# --- 1. Algoritmo de Probabilidad a Priori ---

def calculate_prior_probability(dataset, event):
    """
    Calcula la probabilidad a priori P(event) de un evento
    basado en las frecuencias de un dataset.
    
    Args:
        dataset (list): Una lista de todos los resultados observados.
        event (any): El resultado específico que queremos contar.
    """
    
    print(f"--- 1. Calculando Probabilidad a Priori P({event}) ---")
    
    # Contar cuántas veces ocurrió el evento
    count = 0
    for outcome in dataset:
        if outcome == event:
            count += 1
            
    # Obtener el número total de observaciones
    total_observations = len(dataset)
    
    if total_observations == 0:
        return 0.0
        
    # P(event) = (Veces que ocurrió) / (Total de observaciones)
    prior_prob = count / total_observations
    
    print(f"  Observaciones totales: {total_observations}")
    print(f"  Ocurrencias de '{event}': {count}")
    print(f"  Resultado P({event}) = {count}/{total_observations} = {prior_prob:.4f}\n")
    
    return prior_prob

# --- 2. Algoritmo de Probabilidad Condicionada ---

def calculate_conditional_probability(dataset, event_A, given_B_col, given_B_val):
    """
    Calcula la probabilidad condicionada P(A|B) desde un dataset.
    
    Args:
        dataset (list of tuples): Ej. [('Perro', 'Amistoso'), ...]
        event_A (str): El evento que buscamos (ej. 'Perro')
        given_B_col (int): El índice de la columna de la evidencia (ej. 1)
        given_B_val (str): El valor de la evidencia (ej. 'Amistoso')
    """
    
    print(f"--- 2. Calculando Probabilidad Condicionada P({event_A} | Comportamiento='{given_B_val}') ---")
    
    # 1. Restringir el universo: Filtrar el dataset
    new_universe = []
    for item in dataset:
        if item[given_B_col] == given_B_val:
            new_universe.append(item)
            
    total_given_B = len(new_universe)
    
    if total_given_B == 0:
        return 0.0

    # 2. Contar A dentro del nuevo universo
    count_A_in_B = 0
    for item in new_universe:
        if item[0] == event_A: # Asumimos que el evento A está en la col 0
            count_A_in_B += 1
            
    # P(A|B) = (Casos de A y B) / (Total de casos de B)
    conditional_prob = count_A_in_B / total_given_B
    
    print(f"  Universo original: {len(dataset)} casos")
    print(f"  Nuevo universo (solo '{given_B_val}'): {total_given_B} casos")
    print(f"  Ocurrencias de '{event_A}' en el nuevo universo: {count_A_in_B}")
    print(f"  Resultado P({event_A} | '{given_B_val}') = {count_A_in_B}/{total_given_B} = {conditional_prob:.4f}\n")
    
    return conditional_prob

# --- 3. Algoritmo de Normalización ---

def normalize(distribution):
    """
    Normaliza un diccionario de valores (creencias no normalizadas)
    para que sumen 1.0.
    
    Args:
        distribution (dict): Ej. {'Gripe': 0.08, 'Alergia': 0.01, ...}
    """
    
    print(f"--- 3. Normalizando una Distribución ---")
    print(f"  Valores (no normalizados): {distribution}")
    
    # 1. Sumar todos los valores (Esta es P(B))
    total = sum(distribution.values())
    
    if total == 0:
        return distribution
        
    print(f"  Suma (Constante P(B)): {total:.4f}")
    
    # 2. Dividir cada valor entre la suma
    normalized_dist = {}
    for key, value in distribution.items():
        normalized_dist[key] = value / total
        
    print(f"  Resultado P(A|B): {normalized_dist}\n")
    return normalized_dist

# --- Ejecución de todos los algoritmos ---

if __name__ == "__main__":
    
    # --- Demostración 1: Probabilidad a Priori ---
    animal_data = [
        'Perro', 'Gato', 'Perro', 'Gato', 'Perro', 
        'Perro', 'Gato', 'Otro', 'Perro', 'Gato'
    ]
    prob_perro = calculate_prior_probability(animal_data, 'Perro')
    
    
    # --- Demostración 2: Probabilidad Condicionada ---
    animal_data_detailed = [
        ('Perro', 'Amistoso'), ('Gato', 'Distante'), ('Perro', 'Amistoso'),
        ('Perro', 'Asustado'), ('Gato', 'Amistoso'), ('Perro', 'Distante'),
        ('Gato', 'Distante'), ('Gato', 'Amistoso'), ('Perro', 'Amistoso'),
        ('Otro', 'Amistoso')
    ]
    prob_perro_dado_amistoso = calculate_conditional_probability(
        animal_data_detailed, 
        'Perro',           # Evento A
        1,                 # Columna de la evidencia (Comportamiento)
        'Amistoso'         # Evidencia B
    )

    # --- Demostración 3: Normalización ---
    unnormalized_beliefs = {
        'Gripe': 0.08,  # P(Gripe, Fiebre)
        'Alergia': 0.01, # P(Alergia, Fiebre)
        'Sano': 0.01    # P(Sano, Fiebre)
    }
    prob_dado_fiebre = normalize(unnormalized_beliefs)