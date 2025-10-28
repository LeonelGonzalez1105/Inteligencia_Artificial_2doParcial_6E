# --- Re-definimos el CSP del mapa de Australia ---
variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']

domains = {
    'WA': ['Rojo', 'Verde', 'Azul'],
    'NT': ['Rojo', 'Verde', 'Azul'],
    'SA': ['Rojo', 'Verde', 'Azul'],
    'Q':  ['Rojo', 'Verde', 'Azul'],
    'NSW':['Rojo', 'Verde', 'Azul'],
    'V':  ['Rojo', 'Verde', 'Azul'],
    'T':  ['Rojo', 'Verde', 'Azul']
}

# Creamos un "diccionario de restricciones" para que sea más fácil de consultar
# {'WA': ['NT', 'SA'], 'NT': ['WA', 'SA', 'Q'], ...}
constraints = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'SA', 'Q'],
    'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
    'Q':  ['NT', 'SA', 'NSW'],
    'NSW':['SA', 'Q', 'V'],
    'V':  ['SA', 'NSW'],
    'T':  []
}

# --- Función de Ayuda para Comprobar Restricciones ---

def is_consistent(variable, value, assignment, constraints):
    """
    Comprueba si asignar 'value' a 'variable' es consistente
    con las asignaciones ya hechas ('assignment').
    """
    # Recorremos todos los vecinos de la variable actual
    for neighbor in constraints[variable]:
        # Si el vecino YA está asignado...
        if neighbor in assignment:
            # ...comprobamos si nuestro valor es IGUAL al del vecino
            if assignment[neighbor] == value:
                # ¡Conflicto! Violamos la restricción.
                return False
    
    # Si terminamos el bucle sin encontrar conflictos, es consistente.
    return True

# --- El Algoritmo de Backtracking ---

def backtracking_search_recursive(assignment, variables, domains, constraints):
    """
    Función recursiva principal de backtracking.
    
    Args:
        assignment (dict): Las asignaciones hechas hasta ahora.
    """
    
    # 1. Caso Base: ¿Están todas las variables asignadas?
    if len(assignment) == len(variables):
        print("¡SOLUCIÓN COMPLETA ENCONTRADA!")
        return assignment  # ¡Éxito!
    
    # 2. Seleccionar la siguiente variable sin asignar
    # (Por simplicidad, elegimos la primera que no esté en 'assignment')
    var_to_assign = None
    for v in variables:
        if v not in assignment:
            var_to_assign = v
            break
            
    print(f"  Asignando variable: {var_to_assign}")

    # 3. Probar cada valor del dominio para esa variable
    for value in domains[var_to_assign]:
        
        print(f"    -> Probando valor: {value} para {var_to_assign}")
        
        # 4. Comprobar consistencia
        if is_consistent(var_to_assign, value, assignment, constraints):
            
            # 5. Si es consistente, la ASIGNAMOS
            assignment[var_to_assign] = value
            print(f"      [Asignación: {var_to_assign} = {value}] (OK)")
            
            # 6. Llamada Recursiva: Intentamos resolver el resto del problema
            result = backtracking_search_recursive(assignment, variables, domains, constraints)
            
            # Si la llamada recursiva tuvo éxito, propagamos la solución
            if result is not None:
                return result
            
            # 7. ¡BACKTRACK!
            # Si 'result' fue None, significa que la rama falló.
            # Deshacemos la asignación y probamos el siguiente valor.
            print(f"    <- [BACKTRACK] Quitamos {var_to_assign} = {value}")
            del assignment[var_to_assign]
        else:
            print(f"      (Conflicto con vecinos. Saltando valor {value})")

    # 8. Si probamos todos los valores y ninguno funcionó
    print(f"  ¡Fallo! No hay valores válidos para {var_to_assign}. Retrocediendo...")
    return None

# --- Función principal para iniciar la búsqueda ---
def solve_csp(variables, domains, constraints):
    print("Iniciando Búsqueda de Vuelta Atrás (Backtracking)...")
    # Empezamos con un diccionario de asignaciones vacío
    solution = backtracking_search_recursive({}, variables, domains, constraints)
    
    if solution:
        print("\n--- Solución Final ---")
        for var, val in sorted(solution.items()):
            print(f"{var}: {val}")
    else:
        print("\nNo se encontró solución.")

# --- Ejecutamos el algoritmo ---
solve_csp(variables, domains, constraints)