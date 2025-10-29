import random

# --- 1. Define the Network (CPTs as before) ---
F_Lluvia = {'True': 0.3, 'False': 0.7}
F_Aspersor = {'True': 0.1, 'False': 0.9}
F_Césped = {
    ('True',  'True'):  {'Mojado': 0.99, 'Seco': 0.01},
    ('True',  'False'): {'Mojado': 0.8,  'Seco': 0.2},
    ('False', 'True'):  {'Mojado': 0.9,  'Seco': 0.1},
    ('False', 'False'): {'Mojado': 0.0,  'Seco': 1.0}
}
NETWORK = {'Lluvia': F_Lluvia, 'Aspersor': F_Aspersor, 'Césped': F_Césped}
VARIABLES = ['Lluvia', 'Aspersor', 'Césped'] # Order doesn't strictly matter here

# --- 2. Helper: Sample a variable given its Markov Blanket ---
def sample_conditional(var, current_sample, network):
    """
    Samples a value for 'var' conditioned on the values
    in 'current_sample' (representing the Markov Blanket values).
    P(Var | MB(Var)) = alpha * P(Var | Parents(Var)) * Product[ P(Child | Parents(Child)) ]
    """
    
    # We need to calculate the probability for each value of 'var'
    # P(Var=True | MB) vs P(Var=False | MB)
    
    dist = {} # The conditional distribution to sample from
    
    for value in ['True', 'False']: # Assuming boolean variables
        
        # Make a temporary sample assuming var=value
        temp_sample = current_sample.copy()
        temp_sample[var] = value
        
        prob = 1.0
        
        # Factor 1: P(Var | Parents(Var))
        if var == 'Lluvia':
            prob *= network['Lluvia'][value]
        elif var == 'Aspersor':
            prob *= network['Aspersor'][value]
        elif var == 'Césped':
            # This case won't happen if Césped is evidence, but included for generality
            prob *= network['Césped'][(temp_sample['Lluvia'], temp_sample['Aspersor'])][value]
            
        # Factor 2: Product over Children P(Child | Parents(Child))
        # Find children of 'var'
        children = []
        if var == 'Lluvia' or var == 'Aspersor':
            children.append('Césped')
            
        for child in children:
            if child == 'Césped':
                 prob *= network['Césped'][(temp_sample['Lluvia'], temp_sample['Aspersor'])][temp_sample['Césped']]
                 
        dist[value] = prob

    # Normalize the distribution
    total = sum(dist.values())
    if total == 0: return random.choice(['True', 'False']) # Avoid division by zero
    normalized_dist = {val: p / total for val, p in dist.items()}
    
    # Sample from the normalized distribution
    # (Using the helper from previous topics)
    rand_val = random.random()
    cumulative = 0.0
    for outcome, probability in normalized_dist.items():
        cumulative += probability
        if rand_val < cumulative:
            return outcome
    return list(normalized_dist.keys())[-1]


# --- 3. Algorithm: Gibbs Sampling ---
def gibbs_sampling(query_var, evidence, network, burn_in, num_samples):
    """
    Estimates P(query_var | evidence) using Gibbs Sampling.
    """
    print(f"\n--- Ejecutando Gibbs Sampling (MCMC) ---")
    print(f"Consulta: P({query_var} | {evidence})")
    
    # 1. Initialization: Random state + Fix evidence
    current_state = {}
    non_evidence_vars = []
    for var in VARIABLES:
        if var in evidence:
            current_state[var] = evidence[var]
        else:
            current_state[var] = random.choice(['True', 'False'])
            non_evidence_vars.append(var)
            
    print(f"Estado inicial (aleatorio + evidencia): {current_state}")
    
    samples = [] # Store samples after burn-in
    
    # 2. Iterate (Burn-in + Sampling)
    total_iterations = burn_in + num_samples
    print(f"Ejecutando {total_iterations} iteraciones ({burn_in} burn-in + {num_samples} muestras)...")
    
    for i in range(total_iterations):
        # a. Pick a non-evidence variable
        var_to_sample = random.choice(non_evidence_vars)
        
        # b. Resample it conditioned on its Markov Blanket (current state)
        new_value = sample_conditional(var_to_sample, current_state, network)
        current_state[var_to_sample] = new_value
        
        # c. Collect sample after burn-in
        if i >= burn_in:
            samples.append(current_state.copy()) # Store a copy
            
    print("Muestreo completado.")
    
    # 3. Estimate probability from samples
    counts = {} # {'True': 0, 'False': 0}
    for sample in samples:
        query_val = sample[query_var]
        counts[query_val] = counts.get(query_val, 0) + 1
        
    if not samples: return None
    
    final_distribution = {val: count / len(samples)
                          for val, count in counts.items()}
                          
    return final_distribution

# --- 4. Ejecutar ---
resultado = gibbs_sampling(
    query_var='Lluvia',
    evidence={'Césped': 'Mojado'},
    network=NETWORK,
    burn_in=1000,       # Let it run 1000 times before collecting
    num_samples=10000   # Collect 10,000 samples
)

if resultado:
    print(f"\n--- Resultado de la Consulta (Aproximado por Gibbs) ---")
    print(resultado)