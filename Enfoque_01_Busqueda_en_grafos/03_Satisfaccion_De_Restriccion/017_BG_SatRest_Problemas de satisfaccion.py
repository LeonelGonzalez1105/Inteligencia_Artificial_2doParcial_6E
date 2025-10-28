def setup_australia_map_csp():
    """
    Define el Problema de Satisfacción de Restricciones (CSP)
    para colorear el mapa de Australia.
    """
    
    # 1. Variables (V)
    # Los 7 estados y territorios de Australia
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']

    # 2. Dominios (D)
    # Los colores disponibles para cada variable
    # Usamos un diccionario para que cada variable tenga su propio dominio
    # (aunque en este caso, todos son iguales)
    domains = {
        'WA': ['Rojo', 'Verde', 'Azul'],
        'NT': ['Rojo', 'Verde', 'Azul'],
        'SA': ['Rojo', 'Verde', 'Azul'],
        'Q':  ['Rojo', 'Verde', 'Azul'],
        'NSW':['Rojo', 'Verde', 'Azul'],
        'V':  ['Rojo', 'Verde', 'Azul'],
        'T':  ['Rojo', 'Verde', 'Azul']
    }

    # 3. Restricciones (C)
    # Definidas como una lista de tuplas (variable1, variable2)
    # que significa "variable1 y variable2 no pueden ser iguales"
    # (Estos son los países que son vecinos)
    constraints = [
        ('WA', 'NT'),
        ('WA', 'SA'),
        ('NT', 'SA'),
        ('NT', 'Q'),
        ('SA', 'Q'),
        ('SA', 'NSW'),
        ('SA', 'V'),
        ('Q',  'NSW'),
        ('NSW', 'V')
    ]
    
    print("--- Problema CSP del Mapa de Australia Definido ---")
    print(f"Variables: {variables}")
    print(f"Dominios: {domains['WA']}") # Solo mostramos uno
    print(f"Restricciones (Vecinos): {len(constraints)} pares")
    
    # Devolvemos las 3 partes del problema
    return variables, domains, constraints

# --- Ejecutamos la configuración ---
# Esta función solo "prepara" el problema.
# No lo resuelve.
variables, domains, constraints = setup_australia_map_csp()

# (Opcional) Una función de ayuda que usará el próximo algoritmo
def check_constraint(var1_value, var2_value):
    """
    Verifica si dos valores violan la restricción (ser iguales).
    """
    return var1_value != var2_value

print("\n(Este script solo define el problema. El siguiente lo resolverá)")