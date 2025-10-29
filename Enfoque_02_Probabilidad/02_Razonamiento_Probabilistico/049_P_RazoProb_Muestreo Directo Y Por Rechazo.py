import random

# --- 1. Definir la Red Bayesiana (CPTs) ---
# (Usaremos una estructura de CPT más fácil de consultar)

# P(Lluvia)
F_Lluvia = {'True': 0.3, 'False': 0.7}

# P(Aspersor)
F_Aspersor = {'True': 0.1, 'False': 0.9}

# P(Césped | Lluvia, Aspersor)
# (Lluvia, Aspersor)
F_Césped = {
    ('True',  'True'):  {'Mojado': 0.99, 'Seco': 0.01},
    ('True',  'False'): {'Mojado': 0.8,  'Seco': 0.2},
    ('False', 'True'):  {'Mojado': 0.9,  'Seco': 0.1},
    ('False', 'False'): {'Mojado': 0.0,  'Seco': 1.0}
}

NETWORK = {
    'Lluvia': F_Lluvia,
    'Aspersor': F_Aspersor,
    'Césped': F_Césped
}

# Orden topológico (padres primero)
TOPOLOGICAL_ORDER = ['Lluvia', 'Aspersor', 'Césped']

# --- 2. Algoritmo de Muestreo (Helper) ---

def sample_from_prob(distribution):
    """Lanza un dado ponderado y devuelve el resultado."""
    rand_val = random.random()
    cumulative_prob = 0.0
    for outcome, prob in distribution.items():
        cumulative_prob += prob
        if rand_val < cumulative_prob:
            return outcome
    return list(distribution.keys())[-1] # Por si hay errores de redondeo

# --- 3. Algoritmo de MUESTREO DIRECTO ---

def direct_sample(network, order):
    """
    Genera UN evento completo (muestra) de la red.
    """
    sample_event = {} # El evento que estamos construyendo
    
    for var in order:
        if var == 'Lluvia':
            # 1. Muestrear de P(Lluvia)
            val = sample_from_prob(network['Lluvia'])
            sample_event['Lluvia'] = val
            
        elif var == 'Aspersor':
            # 2. Muestrear de P(Aspersor)
            val = sample_from_prob(network['Aspersor'])
            sample_event['Aspersor'] = val
            
        elif var == 'Césped':
            # 3. Muestrear de P(Césped | Lluvia, Aspersor)
            # Obtenemos los valores de los padres (¡que ya muestreamos!)
            parent_l = sample_event['Lluvia']
            parent_a = sample_event['Aspersor']
            
            # Elegir la CPT correcta
            relevant_cpt = network['Césped'][(parent_l, parent_a)]
            
            # Muestrear de esa CPT
            val = sample_from_prob(relevant_cpt)
            sample_event['Césped'] = val
            
    return sample_event

# --- 4. Algoritmo de MUESTREO POR RECHAZO ---

def rejection_sampling(query_var, evidence, network, num_samples):
    """
    Calcula P(query_var | evidence) usando muestreo por rechazo.
    """
    print(f"\n--- Ejecutando Muestreo por Rechazo ---")
    print(f"Consulta: P({query_var} | {evidence})")
    print(f"Total de muestras a generar: {num_samples}")
    
    counts = {} # Contador para la variable de consulta (ej. {'True': 0, 'False': 0})
    total_accepted = 0 # Contador de muestras que aceptamos
    
    for _ in range(num_samples):
        # 1. Generar Muestra (usando Muestreo Directo)
        sample = direct_sample(network, TOPOLOGICAL_ORDER)
        
        # 2. Rechazar/Aceptar
        matches = True
        for var, val in evidence.items():
            if sample[var] != val:
                matches = False
                break
        
        if matches:
            # 3. ACEPTAR la muestra
            total_accepted += 1
            
            # Contar el valor de la variable de consulta
            query_val = sample[query_var]
            counts[query_val] = counts.get(query_val, 0) + 1
            
    # 4. Calcular el resultado final (Normalizar)
    if total_accepted == 0:
        print("¡Error! Ninguna muestra coincidió con la evidencia.")
        return None
        
    print(f"  Muestras aceptadas (que coincidieron): {total_accepted}")
    print(f"  Tasa de rechazo: {(num_samples - total_accepted) / num_samples * 100:.2f}%")

    final_distribution = {val: count / total_accepted 
                          for val, count in counts.items()}
    
    return final_distribution

# --- 5. Ejecutar ---

# Primero, mostramos cómo funciona el Muestreo Directo
print("--- 1. Muestreo Directo (Simulación) ---")
print("Generando 5 muestras de la red:")
for i in range(5):
    print(f"  Muestra {i+1}: {direct_sample(NETWORK, TOPOLOGICAL_ORDER)}")

# Segundo, usamos el Muestreo por Rechazo para inferencia
resultado = rejection_sampling(
    query_var='Lluvia',              # P(Lluvia...
    evidence={'Césped': 'Mojado'},  # ... | Césped='Mojado')
    network=NETWORK,
    num_samples=100000               # Probar con 100,000 simulaciones
)

if resultado:
    print(f"\n--- Resultado de la Consulta (Aproximado) ---")
    print(resultado)