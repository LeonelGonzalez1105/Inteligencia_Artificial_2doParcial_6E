# --- 1. Definir la Red Bayesiana (las CPTs) ---

# P(Lluvia)
# Nodo raíz, sin padres. Es una prob. a priori.
CPT_Lluvia = {
    True: 0.3, # 30% de prob. de que llueva
    False: 0.7
}

# P(Aspersor)
# Nodo raíz, sin padres. (Asumimos que no depende de la lluvia)
CPT_Aspersor = {
    True: 0.1, # 10% de prob. de que esté encendido
    False: 0.9
}

# P(Césped_Mojado | Lluvia, Aspersor)
# Nodo hijo, depende de DOS padres.
CPT_Césped_Mojado = {
    # Caso 1: Lluvia = True
    (True,): {
        # Aspersor = True
        (True,): {'Mojado': 0.99, 'Seco': 0.01}, # Lluvia y aspersor
        # Aspersor = False
        (False,): {'Mojado': 0.8, 'Seco': 0.2}  # Solo lluvia
    },
    # Caso 2: Lluvia = False
    (False,): {
        # Aspersor = True
        (True,): {'Mojado': 0.9, 'Seco': 0.1},  # Solo aspersor
        # Aspersor = False
        (False,): {'Mojado': 0.0, 'Seco': 1.0}   # Nada
    }
}

# --- 2. El "Algoritmo": Regla de la Cadena Bayesiana ---

def calculate_joint_probability(evento, red):
    """
    Calcula la probabilidad conjunta de un evento completo
    usando la Regla de la Cadena de la red.
    
    Args:
        evento (dict): Un escenario completo. 
                       Ej. {'Lluvia': True, 'Aspersor': False, 'Césped': 'Mojado'}
        red (dict): Un diccionario con las CPTs
    """
    
    # Obtener los valores del evento
    l = evento['Lluvia']
    a = evento['Aspersor']
    c = evento['Césped']
    
    # 1. Obtener P(Lluvia)
    prob_L = red['Lluvia'][l]
    
    # 2. Obtener P(Aspersor)
    prob_A = red['Aspersor'][a]
    
    # 3. Obtener P(Césped | Lluvia, Aspersor)
    # Esta consulta usa la estructura anidada de la CPT
    prob_C_dado_L_A = red['Césped'][(l,)][(a,)][c]
    
    # 4. Calcular P(L, A, C) = P(L) * P(A) * P(C|L,A)
    joint_prob = prob_L * prob_A * prob_C_dado_L_A
    
    return joint_prob

# --- 3. Definir las CPTs de nuestra red ---
red_bayesiana = {
    'Lluvia': CPT_Lluvia,
    'Aspersor': CPT_Aspersor,
    'Césped': CPT_Césped_Mojado
}

# --- 4. Ejecutar una consulta ---
# Pregunta: ¿Cuál es la probabilidad de que...
#          NO llueva, SÍ esté el aspersor, y el CÉSPED esté MOJADO?
evento_1 = {
    'Lluvia': False,
    'Aspersor': True,
    'Césped': 'Mojado'
}

prob_1 = calculate_joint_probability(evento_1, red_bayesiana)

print("--- Cálculo de Probabilidad Conjunta (Regla de Cadena) ---")
print(f"Evento: {evento_1}")
print(f"Cálculo: P(L=F) * P(A=T) * P(C='Mojado' | L=F, A=T)")
print(f"Cálculo: {CPT_Lluvia[False]} * {CPT_Aspersor[True]} * {CPT_Césped_Mojado[(False, )][(True, )]['Mojado']}")
print(f"Probabilidad: {0.7 * 0.1 * 0.9:.4f} (6.3%)")
print(f"Resultado de la función: {prob_1:.4f}")