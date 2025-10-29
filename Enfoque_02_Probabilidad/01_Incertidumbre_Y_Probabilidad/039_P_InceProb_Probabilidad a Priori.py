def calculate_prior_probability(dataset, event):
    """
    Calcula la probabilidad a priori P(event) de un evento
    basado en las frecuencias de un dataset.
    
    Args:
        dataset (list): Una lista de todos los resultados observados.
        event (any): El resultado específico que queremos contar.
    """
    
    print(f"--- Calculando P({event}) ---")
    
    # 1. Contar cuántas veces ocurrió el evento
    count = 0
    for outcome in dataset:
        if outcome == event:
            count += 1
            
    # 2. Obtener el número total de observaciones
    total_observations = len(dataset)
    
    if total_observations == 0:
        return 0.0 # Evitar división por cero
        
    # 3. Calcular la probabilidad
    # P(event) = (Veces que ocurrió) / (Total de observaciones)
    prior_prob = count / total_observations
    
    print(f"  Observaciones totales: {total_observations}")
    print(f"  Ocurrencias de '{event}': {count}")
    print(f"  Probabilidad a Priori P({event}) = {count}/{total_observations} = {prior_prob:.4f}")
    
    return prior_prob

# --- Nuestro Conjunto de Datos ---
# Registros de animales que entraron al refugio esta semana
animal_data = [
    'Perro', 'Gato', 'Perro', 'Gato', 'Perro', 
    'Perro', 'Gato', 'Otro', 'Perro', 'Gato'
]

# --- Ejecutar el "algoritmo" ---
prob_perro = calculate_prior_probability(animal_data, 'Perro')
prob_gato = calculate_prior_probability(animal_data, 'Gato')
prob_otro = calculate_prior_probability(animal_data, 'Otro')