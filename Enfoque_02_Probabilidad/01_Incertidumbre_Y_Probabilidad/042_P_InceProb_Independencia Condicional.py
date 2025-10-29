# --- 1. Definir las CPTs (Tablas de Probabilidad Condicional) ---

# P(Alarma | Humo)
# La alarma solo se preocupa por el humo, ¡no por el fuego!
# Esta definición ES la independencia condicional.
CPT_Alarma_dado_Humo = {
    # Humo = True
    True: { 'Suena': 0.95, 'No Suena': 0.05 },
    # Humo = False
    False: { 'Suena': 0.01, 'No Suena': 0.99 } # (ej. batería baja)
}

# --- 2. El "Algoritmo": Una función que consulta el modelo ---

def get_prob_alarma(evidencia_humo, evidencia_fuego):
    """
    Calcula P(Alarma='Suena' | Humo=evidencia_humo, Fuego=evidencia_fuego)
    
    Esta función demuestra que la 'evidencia_fuego' es irrelevante
    debido a la estructura del modelo.
    """
    
    print(f"  Calculando P(Alarma | Humo={evidencia_humo}, Fuego={evidencia_fuego})...")
    
    # 3. La lógica: El modelo MIRA el estado del Humo...
    if evidencia_humo == True:
        # El Humo es True, consultamos esa parte de la CPT
        prob = CPT_Alarma_dado_Humo[True]['Suena']
        
    elif evidencia_humo == False:
        # El Humo es False, consultamos esa parte
        prob = CPT_Alarma_dado_Humo[False]['Suena']
        
    # ...¡Pero NUNCA MIRA el estado del Fuego!
    # El parámetro 'evidencia_fuego' no se usa.
    
    print(f"    -> Resultado: {prob}")
    return prob

# --- 3. Demostración ---

print("Demostrando que P(Alarma | Humo, Fuego) = P(Alarma | Humo)\n")

# --- Escenario 1: Sabemos que SÍ hay humo ---
print("Caso 1: Hay Humo (C = True)")

# P(A | C=True, B=True)
p1 = get_prob_alarma(evidencia_humo=True, evidencia_fuego=True)

# P(A | C=True, B=False)
p2 = get_prob_alarma(evidencia_humo=True, evidencia_fuego=False)

# P(A | C=True)
p_base = CPT_Alarma_dado_Humo[True]['Suena']
print(f"  P(Alarma | Humo=True) = {p_base} (Valor base)")

# La demostración
assert p1 == p_base and p2 == p_base
print("\n  >> Conclusión: P(A|C,B) = P(A|C,no B) = P(A|C). ¡Son independientes!\n")


# --- Escenario 2: Sabemos que NO hay humo ---
print("Caso 2: No Hay Humo (C = False)")

# P(A | C=False, B=True)
p3 = get_prob_alarma(evidencia_humo=False, evidencia_fuego=True)

# P(A | C=False, B=False)
p4 = get_prob_alarma(evidencia_humo=False, evidencia_fuego=False)

# P(A | C=False)
p_base_2 = CPT_Alarma_dado_Humo[False]['Suena']
print(f"  P(Alarma | Humo=False) = {p_base_2} (Valor base)")

assert p3 == p_base_2 and p4 == p_base_2
print("\n  >> Conclusión: La independencia se mantiene.\n")