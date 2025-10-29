# --- 1. Definir la Red (CPTs como "Factores") ---
# (Idéntica a la del tema #44)
F_Lluvia = { True: 0.3, False: 0.7 }
F_Aspersor = { True: 0.1, False: 0.9 }
# Factor P(C|L,A). Usaremos una función para consultarlo.
def get_prob_C_dado_L_A(c_val, l_val, a_val):
    if c_val == 'Mojado':
        if l_val == True:
            return 0.99 if a_val == True else 0.8
        else: # Lluvia = False
            return 0.9 if a_val == True else 0.0
    else: # Césped = Seco
        # (Inverso de Mojado)
        return 1.0 - get_prob_C_dado_L_A('Mojado', l_val, a_val)

# --- 2. El "Algoritmo": Pasos de Eliminación ---

def variable_elimination(query_var, evidence, hidden_vars, network_factors):
    """
    Realiza la inferencia usando Eliminación de Variables (conceptual).
    """
    
    print("--- Ejecutando Eliminación de Variables ---")
    print(f"Consulta: P({query_var} | {evidence})")
    print(f"Variables Ocultas a eliminar: {hidden_vars}")
    
    # --- PASO 1: Inicializar Factores ---
    # (En una implementación real, aquí tendríamos objetos 'Factor')
    # Usaremos funciones lambda para representar factores dinámicos
    
    # Factor inicial para P(L)
    factor_L = lambda l: network_factors['Lluvia'][l]
    
    # Factor inicial para P(A)
    factor_A = lambda a: network_factors['Aspersor'][a]

    # Factor inicial P(C|L,A), pero FIJANDO C a la evidencia
    c_evidence = evidence['Césped']
    factor_C_dado_L_A = lambda l, a: get_prob_C_dado_L_A(c_evidence, l, a)
    
    print("  Factores iniciales definidos.")
    
    # --- PASO 2: Eliminar la variable oculta 'A' ---
    print("  Eliminando variable 'Aspersor' (A)...")
    
    # a. Unir factores que mencionan 'A': f(A) y f(C|L,A) -> f(L, A, C=true)
    #    (Conceptual: f_joined(l, a) = factor_A(a) * factor_C_dado_L_A(l, a))
    
    # b. Sumar sobre 'A': Suma_a [ f(A) * f(C=true|L,A) ] -> f(L, C=true)
    #    Creamos un nuevo factor que ya no depende de 'A'
    factor_L_C_sin_A = {} # Guardará { L_val: probabilidad }
    
    for l_val in [True, False]: # Para cada valor posible de L
        sum_over_a = 0.0
        for a_val in [True, False]: # Sumamos sobre A
            prob_a = factor_A(a_val)
            prob_c_dado_l_a = factor_C_dado_L_A(l_val, a_val)
            sum_over_a += prob_a * prob_c_dado_l_a
            
        factor_L_C_sin_A[l_val] = sum_over_a
        
    print(f"    Nuevo factor creado f(L, C=true) (sin A): {factor_L_C_sin_A}")

    # --- PASO 3: Unir factores restantes y Normalizar ---
    # Factores restantes: f(L) y f(L, C=true)
    print("  Uniendo factores restantes...")
    
    unnormalized_result = {}
    for l_val in [True, False]:
        prob_l = factor_L(l_val)
        prob_l_c_sin_a = factor_L_C_sin_A[l_val]
        
        # P(L, C=true) = P(L) * Suma_a[ P(a) * P(C=true|L,a) ]
        unnormalized_result[l_val] = prob_l * prob_l_c_sin_a

    print(f"    Resultado (no normalizado) P(L, C=true): {unnormalized_result}")

    # Normalizar (usando la función del tema #41)
    def normalize(distribution):
        total = sum(distribution.values())
        if total == 0: return distribution
        return {key: val / total for key, val in distribution.items()}

    final_result = normalize(unnormalized_result)
    
    return final_result

# --- 3. Definir la Red y Ejecutar ---
network_data = {
    'Lluvia': F_Lluvia,
    'Aspersor': F_Aspersor
    # La CPT de Césped está en la función get_prob...
}

resultado = variable_elimination(
    query_var='Lluvia', 
    evidence={'Césped': 'Mojado'}, 
    hidden_vars=['Aspersor'], 
    network_factors=network_data
)

print("\n--- Resultado Final (Normalizado) ---")
print(f"P(Lluvia | Césped='Mojado'): {resultado}")