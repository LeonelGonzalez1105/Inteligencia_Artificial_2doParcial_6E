import copy # ¡Necesitamos esto para hacer copias profundas!

# --- Definición del CSP (igual que antes) ---
variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
original_domains = {
    'WA': ['Rojo', 'Verde', 'Azul'],
    'NT': ['Rojo', 'Verde', 'Azul'],
    'SA': ['Rojo', 'Verde', 'Azul'],
    'Q':  ['Rojo', 'Verde', 'Azul'],
    'NSW':['Rojo', 'Verde', 'Azul'],
    'V':  ['Rojo', 'Verde', 'Azul'],
    'T':  ['Rojo', 'Verde', 'Azul']
}
constraints = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'SA', 'Q'],
    'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
    'Q':  ['NT', 'SA', 'NSW'],
    'NSW':['SA', 'Q', 'V'],
    'V':  ['SA', 'NSW'],
    'T':  []
}
# ----------------------------------------------


def forward_check(current_var, current_value, domains, constraints):
    """
    Realiza la Comprobación Hacia Delante.
    Modifica el diccionario 'domains' podando los valores.
    Devuelve True si tiene éxito, False si un dominio queda vacío.
    """
    
    # Recorremos todos los vecinos de la variable que acabamos de asignar
    for neighbor in constraints[current_var]:
        # Si el valor está en el dominio del vecino...
        if current_value in domains[neighbor]:
            
            # ...lo eliminamos
            domains[neighbor].remove(current_value)
            
            # ¡LA CLAVE! ¿Dejamos a este vecino sin opciones?
            if not domains[neighbor]:
                # ¡Sí! Dominio vacío. Esto es un fallo.
                return False
                
    # Si sobrevivimos al bucle, la poda fue exitosa
    return True


def backtracking_fc_recursive(assignment, domains, variables, constraints):
    """
    Función recursiva de backtracking CON Forward Checking.
    """
    
    # 1. Caso Base: ¿Están todas las variables asignadas?
    if len(assignment) == len(variables):
        print("¡SOLUCIÓN COMPLETA ENCONTRADA!")
        return assignment

    # 2. Seleccionar la siguiente variable sin asignar
    var_to_assign = None
    for v in variables:
        if v not in assignment:
            var_to_assign = v
            break
            
    print(f"  Asignando variable: {var_to_assign}")

    # 3. Probar cada valor del dominio actual (¡que puede estar podado!)
    for value in domains[var_to_assign]:
        
        print(f"    -> Probando valor: {value} para {var_to_assign}")
        
        # 4. Hacemos una COPIA de los dominios antes de podarlos
        # (Así, si este 'value' falla, no afectamos la prueba del siguiente valor)
        domains_copy = copy.deepcopy(domains)
        
        # 5. ¡Ejecutamos el Forward Checking!
        if forward_check(var_to_assign, value, domains_copy, constraints):
            # ¡Éxito! La poda no resultó en dominios vacíos.
            print(f"      [Asignación: {var_to_assign} = {value}] (OK)")
            
            # Asignamos el valor
            assignment[var_to_assign] = value
            
            # 6. Llamada Recursiva: Pasamos los dominios YA PODADOS
            result = backtracking_fc_recursive(assignment, domains_copy, variables, constraints)
            
            if result is not None:
                return result
            
            # 7. BACKTRACK: Deshacemos la asignación
            print(f"    <- [BACKTRACK] Quitamos {var_to_assign} = {value}")
            del assignment[var_to_assign]
        else:
            # El Forward Check falló (creó un dominio vacío)
            print(f"      (Forward Check falló para {value}. Saltando valor)")

    # 8. Si probamos todos los valores y ninguno funcionó
    print(f"  ¡Fallo! No hay valores válidos para {var_to_assign}. Retrocediendo...")
    return None

# --- Función principal para iniciar la búsqueda ---
def solve_csp_fc(variables, domains, constraints):
    print("Iniciando Búsqueda con Comprobación Hacia Delante (FC)...")
    solution = backtracking_fc_recursive({}, domains, variables, constraints)
    
    if solution:
        print("\n--- Solución Final ---")
        for var, val in sorted(solution.items()):
            print(f"{var}: {val}")
    else:
        print("\nNo se encontró solución.")

# --- Ejecutamos el algoritmo ---
solve_csp_fc(variables, original_domains, constraints)