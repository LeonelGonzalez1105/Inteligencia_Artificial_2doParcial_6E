import random

# --- 1. Definir la Red Bayesiana (CPTs) ---
# (Idéntica a la del tema anterior)
F_Lluvia = {'True': 0.3, 'False': 0.7}
F_Aspersor = {'True': 0.1, 'False': 0.9}
F_Césped = {
    ('True',  'True'):  {'Mojado': 0.99, 'Seco': 0.01},
    ('True',  'False'): {'Mojado': 0.8,  'Seco': 0.2},
    ('False', 'True'):  {'Mojado': 0.9,  'Seco': 0.1},
    ('False', 'False'): {'Mojado': 0.0,  'Seco': 1.0}
}
NETWORK = {'Lluvia': F_Lluvia, 'Aspersor': F_Aspersor, 'Césped': F_Césped}
TOPOLOGICAL_ORDER = ['Lluvia', 'Aspersor', 'Césped']

# (Función de ayuda para muestrear - idéntica a la anterior)
def sample_from_prob(distribution):
    rand_val = random.random()
    cumulative_prob = 0.0
    for outcome, prob in distribution.items():
        cumulative_prob += prob
        if rand_val < cumulative_prob:
            return outcome
    return list(distribution.keys())[-1]

# --- 2. Algoritmo de Ponderación de Verosimilitud ---

def weighted_sample(network, order, evidence):
    """
    Genera UNA muestra ponderada consistente con la evidencia.
    Devuelve: (sample_event, weight)
    """
    sample_event = {} # El evento
    weight = 1.0      # El peso
    
    for var in order:
        
        # --- Lógica de Padres (igual que Muestreo Directo) ---
        parents_values = None
        if var == 'Césped':
            parent_l = sample_event['Lluvia']
            parent_a = sample_event['Aspersor']
            parents_values = (parent_l, parent_a)
            relevant_cpt = network[var][parents_values]
        else: # Nodos raíz
            relevant_cpt = network[var]
            
        # --- La Decisión Clave ---
        if var in evidence:
            # 1. ES EVIDENCIA: Fijar el valor y Ponderar
            value = evidence[var]
            sample_event[var] = value
            
            # Multiplicar el peso por P(evidencia | padres)
            prob_evidence = relevant_cpt.get(value, 0.0) # Obtener P(E=e|...)
            weight *= prob_evidence
            
        else:
            # 2. NO ES EVIDENCIA: Muestrear normalmente
            value = sample_from_prob(relevant_cpt)
            sample_event[var] = value
            
    return sample_event, weight

def likelihood_weighting(query_var, evidence, network, num_samples):
    """
    Calcula P(query_var | evidence) usando Ponderación de Verosimilitud.
    """
    print(f"\n--- Ejecutando Ponderación de Verosimilitud ---")
    print(f"Consulta: P({query_var} | {evidence})")
    print(f"Número de muestras: {num_samples}")
    
    # Acumulador de pesos para cada valor de la consulta
    weighted_counts = {} # Ej: {'True': 0.0, 'False': 0.0}

    for _ in range(num_samples):
        # 1. Generar Muestra Ponderada
        sample, weight = weighted_sample(network, TOPOLOGICAL_ORDER, evidence)
        
        # 2. Acumular el peso en el contador correcto
        query_val = sample[query_var]
        weighted_counts[query_val] = weighted_counts.get(query_val, 0.0) + weight
        
    # 3. Normalizar los pesos acumulados
    # (Usamos la función 'normalize' del tema #41)
    def normalize(distribution):
        total = sum(distribution.values())
        if total == 0: return distribution
        return {key: val / total for key, val in distribution.items()}

    final_distribution = normalize(weighted_counts)
    
    return final_distribution

# --- 3. Ejecutar ---

# Primero, mostramos cómo funciona una muestra ponderada
print("--- 1. Muestra Ponderada (Simulación) ---")
print("Generando 5 muestras ponderadas (con evidencia Césped='Mojado'):")
for i in range(5):
    s, w = weighted_sample(NETWORK, TOPOLOGICAL_ORDER, {'Césped': 'Mojado'})
    print(f"  Muestra {i+1}: {s}, Peso={w:.3f}")

# Segundo, usamos el algoritmo completo para inferencia
resultado = likelihood_weighting(
    query_var='Lluvia',              # P(Lluvia...
    evidence={'Césped': 'Mojado'},  # ... | Césped='Mojado')
    network=NETWORK,
    num_samples=100000               # 100,000 muestras
)

if resultado:
    print(f"\n--- Resultado de la Consulta (Aproximado) ---")
    print(resultado)