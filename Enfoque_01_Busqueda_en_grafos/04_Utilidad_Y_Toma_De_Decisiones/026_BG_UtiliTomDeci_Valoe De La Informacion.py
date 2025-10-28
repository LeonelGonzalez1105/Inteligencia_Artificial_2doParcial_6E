# --- 1. Definir la Red (Probabilidades y Utilidades) ---

# Problema: "Lanzar Producto"
# Usamos la utilidad neutral (U($) = $)
decisiones = ['Lanzar', 'No Lanzar']

probs_azar = {
    'Alta Demanda': 0.7,
    'Baja Demanda': 0.3
}

tabla_utilidad = {
    'Lanzar': {
        'Alta Demanda': 100000,
        'Baja Demanda': -80000
    },
    'No Lanzar': {
        'Alta Demanda': 0,
        'Baja Demanda': 0
    }
}

# --- 2. Algoritmo ---

def calcular_vpi(decisiones, probs_azar, tabla_utilidad):
    """
    Calcula el Valor de la Información Perfecta (VPI).
    """
    
    # --- PASO 1: Calcular la MEU (sin información) ---
    max_eu_original = -float('inf')
    
    for decision in decisiones:
        eu_decision = 0.0
        for estado, prob in probs_azar.items():
            eu_decision += prob * tabla_utilidad[decision][estado]
            
        if eu_decision > max_eu_original:
            max_eu_original = eu_decision

    print(f"Paso 1: Máxima Utilidad Esperada (MEU) original = ${max_eu_original:,.2f}")

    # --- PASO 2: Calcular la EU_PI (con información perfecta) ---
    eu_perfect_info = 0.0
    
    # Iteramos sobre los posibles "futuros" que el oráculo nos puede decir
    for estado, prob in probs_azar.items():
        
        # Para este futuro, ¿cuál es la mejor decisión que podemos tomar?
        mejor_utilidad_en_este_estado = -float('inf')
        for decision in decisiones:
            utilidad = tabla_utilidad[decision][estado]
            if utilidad > mejor_utilidad_en_este_estado:
                mejor_utilidad_en_este_estado = utilidad
        
        # Sumamos esa "mejor utilidad" al promedio, ponderada por la prob
        # de que ese futuro ocurra
        eu_perfect_info += prob * mejor_utilidad_en_este_estado

    print(f"Paso 2: Utilidad Esperada con Info Perfecta (EU_PI) = ${eu_perfect_info:,.2f}")

    # --- PASO 3: Calcular VPI ---
    vpi = eu_perfect_info - max_eu_original
    return vpi

# --- 3. Ejecutar el cálculo ---
print("--- Calculando el Valor de la Información Perfecta (VPI) ---")
valor_informacion = calcular_vpi(decisiones, probs_azar, tabla_utilidad)

print("\n--- Resultado ---")
print(f"El VPI es: ${valor_informacion:,.2f}")
print("Esto es lo máximo que deberíamos pagar por un estudio de mercado perfecto.")