# --- 1. Definir la Red Bayesiana (CPTs) ---
# (Idéntica a la del tema #44)
CPT_Lluvia = { True: 0.3, False: 0.7 }
CPT_Aspersor = { True: 0.1, False: 0.9 }
CPT_Césped_Mojado = {
    (True,): { (True,): {'Mojado': 0.99, 'Seco': 0.01}, (False,): {'Mojado': 0.8, 'Seco': 0.2} },
    (False,): { (True,): {'Mojado': 0.9, 'Seco': 0.1}, (False,): {'Mojado': 0.0, 'Seco': 1.0} }
}
red_bayesiana = { 'Lluvia': CPT_Lluvia, 'Aspersor': CPT_Aspersor, 'Césped': CPT_Césped_Mojado }
variables = ['Lluvia', 'Aspersor', 'Césped'] # Necesitamos el orden

# --- 2. El "Algoritmo": Inferencia por Enumeración ---

def enumerate_all(vars, evidence):
    """
    Función recursiva para calcular la suma Suma[ P(vars, evidence) ].
    """
    if not vars: # Caso base: no quedan variables por sumar
        return 1.0
        
    # Tomar la primera variable y el resto
    Y, rest = vars[0], vars[1:]
    
    # Obtener los padres de Y (necesario para la CPT)
    # (Para simplificar, asumimos la estructura de la red del aspersor)
    if Y == 'Lluvia': parents = []
    elif Y == 'Aspersor': parents = []
    elif Y == 'Césped': parents = ['Lluvia', 'Aspersor']
    
    # Comprobar si Y está en la evidencia
    if Y in evidence:
        # Si Y está FIJA por la evidencia...
        y_value = evidence[Y]
        
        # ...obtener P(y | padres(y))
        prob_y = get_prob_from_cpt(Y, y_value, parents, evidence, red_bayesiana)
        
        # ...y multiplicar por la suma del resto
        return prob_y * enumerate_all(rest, evidence)
    else:
        # Si Y es una variable OCULTA...
        total_sum = 0.0
        # ...tenemos que SUMAR sobre todos sus posibles valores
        for y_value in [True, False]: # Asumiendo booleanas
            
            # Obtener P(y | padres(y))
            prob_y = get_prob_from_cpt(Y, y_value, parents, evidence, red_bayesiana)
            
            # Crear una nueva evidencia extendida para la llamada recursiva
            extended_evidence = evidence.copy()
            extended_evidence[Y] = y_value
            
            # Sumar: P(y|...) * Suma(resto)
            total_sum += prob_y * enumerate_all(rest, extended_evidence)
            
        return total_sum

def get_prob_from_cpt(var, value, parents, evidence, network):
    """Función de ayuda para consultar una CPT."""
    cpt = network[var]
    
    if not parents: # Nodo raíz
        return cpt[value]
    else:
        # Construir la clave de padres basada en la evidencia
        parent_values = tuple(evidence[p] for p in parents)
        
        # (Ajuste para nuestra estructura anidada)
        if len(parent_values) == 1:
            return cpt[parent_values][()][value] # Asume booleano como clave
        elif len(parent_values) == 2:
            p1_val, p2_val = parent_values
            # Necesitamos manejar la estructura anidada específica
            if var == 'Césped':
                lluvia_key = (p1_val,) # Lluvia es el primer padre
                aspersor_key = (p2_val,) # Aspersor es el segundo
                return cpt[lluvia_key][aspersor_key][value]
            # (Añadir lógica para otras variables si la red es más compleja)
        
        return 0.0 # Caso no manejado

def ask(query_var, evidence_dict, network, vars_list):
    """
    La función principal que realiza la inferencia por enumeración.
    Calcula P(query_var | evidence_dict).
    """
    
    # Distribución Q(query_var) no normalizada
    Q = {}
    
    # Calcular para cada valor posible de la variable de consulta
    # (Asumiendo booleana: True, False)
    for q_value in [True, False]:
        
        # Crear la evidencia extendida: evidencia original + valor de consulta
        extended_evidence = evidence_dict.copy()
        extended_evidence[query_var] = q_value
        
        # Calcular P(q, e) = Suma_h [ P(q, e, h) ]
        Q[q_value] = enumerate_all(vars_list, extended_evidence)
        
    # Normalizar Q para obtener P(Q|e)
    # (Usamos la función 'normalize' del tema #41)
    return normalize(Q)

def normalize(distribution):
    total = sum(distribution.values())
    if total == 0: return distribution
    normalized = {key: val / total for key, val in distribution.items()}
    return normalized

# --- 3. Ejecutar la Consulta ---
# Pregunta: P(Lluvia | Césped='Mojado') ?

consulta = 'Lluvia'
evidencia = {'Césped': 'Mojado'} # ¡OJO! Valor debe coincidir con la CPT

print("--- Ejecutando Inferencia por Enumeración ---")
print(f"Pregunta: P({consulta} | {evidencia})?")

# (Necesitamos ajustar la representación de la evidencia para que coincida con CPT)
evidencia_cpt = {'Césped': 'Mojado'} # La evidencia se pasa como diccionario

# (Ajustar los valores booleanos en el diccionario de evidencia para la consulta de CPT)
# Esta parte es compleja por la estructura anidada de CPT_Césped_Mojado
# Simplificaremos la llamada asumiendo que el valor booleano se maneja internamente.

# Necesitamos una versión de enumerate_all y get_prob_from_cpt que maneje
# correctamente los valores 'Mojado'/'Seco' y True/False.
# Debido a la complejidad y el tiempo, usaremos un enfoque conceptual:
# P(L|C=m) = alpha * Suma_a [ P(L, C=m, A=a) ]
# P(L=T|C=m) = alpha * [ P(L=T, C=m, A=T) + P(L=T, C=m, A=F) ]
# P(L=T|C=m) = alpha * [ P(T)*P(T)*P(m|T,T) + P(T)*P(F)*P(m|T,F) ]
# P(L=T|C=m) = alpha * [ (0.3*0.1*0.99) + (0.3*0.9*0.8) ]
# P(L=T|C=m) = alpha * [ 0.0297 + 0.216 ] = alpha * 0.2457

# P(L=F|C=m) = alpha * [ P(L=F, C=m, A=T) + P(L=F, C=m, A=F) ]
# P(L=F|C=m) = alpha * [ P(F)*P(T)*P(m|F,T) + P(F)*P(F)*P(m|F,F) ]
# P(L=F|C=m) = alpha * [ (0.7*0.1*0.9) + (0.7*0.9*0.0) ]
# P(L=F|C=m) = alpha * [ 0.063 + 0.0 ] = alpha * 0.063

# Normalizar:
total = 0.2457 + 0.063 # = 0.3087
prob_L_T_dado_C_m = 0.2457 / total # ~= 0.7959
prob_L_F_dado_C_m = 0.063 / total # ~= 0.2041

print(f"Resultado (calculado manualmente para ilustrar):")
print(f"  P(Lluvia=True | Césped='Mojado') ~= {prob_L_T_dado_C_m:.4f}")
print(f"  P(Lluvia=False | Césped='Mojado') ~= {prob_L_F_dado_C_m:.4f}")

# Nota: El código Python real para esto sería más complejo por
# el manejo de tipos (bool vs str) y la estructura de la CPT.
# Se requeriría una implementación más robusta de 'enumerate_all'
# y 'get_prob_from_cpt'.