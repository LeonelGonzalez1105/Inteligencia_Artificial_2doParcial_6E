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

def is_consistent_cbj(variable, value, assignment, constraints):
    """
    Comprueba si un valor es consistente Y devuelve CON QUIÉN entra en conflicto.
    """
    conflicts = set()
    for neighbor in constraints[variable]:
        if neighbor in assignment and assignment[neighbor] == value:
            conflicts.add(neighbor)
    
    if conflicts:
        return (False, conflicts)
    return (True, conflicts) # conflicts está vacío

def backtracking_cbj_recursive(assignment, variables, domains, constraints):
    """
    Función recursiva de CBJ.
    Retorna:
    - ('SUCCESS', assignment) si se encuentra solución.
    - ('FAILURE', conflict_set) si falla.
    """
    
    # 1. Caso Base: Éxito
    if len(assignment) == len(variables):
        return ('SUCCESS', assignment)

    # 2. Seleccionar variable
    var = None
    for v in variables:
        if v not in assignment:
            var = v
            break
            
    # 3. Este es el conjunto de conflictos que 'var' acumulará
    my_total_conflict_set = set()
    
    # 4. Probar cada valor
    for value in domains[var]:
        
        # 5. Comprobar consistencia con el pasado
        (consistent, conflicts) = is_consistent_cbj(var, value, assignment, constraints)
        
        if consistent:
            # 6. Asignar
            assignment[var] = value
            
            # 7. Llamada Recursiva
            (status, data) = backtracking_cbj_recursive(assignment, variables, domains, constraints)
            
            # 8. Analizar el resultado de la recursión
            if status == 'SUCCESS':
                return ('SUCCESS', data) # ¡Éxito! Propagarlo
            
            # 9. ¡La recursión falló! 'data' es el conflict_set_from_below
            conflict_set_from_below = data
            
            # 10. ¡LA CLAVE DEL "SALTO"!
            # ¿Es 'var' (yo) el responsable del fallo de abajo?
            if var in conflict_set_from_below:
                # SÍ. El fallo se debe a mí.
                # Debo seguir probando mis otros valores.
                # Pero primero, guardo los conflictos que me reportaron.
                conflict_set_from_below.remove(var)
                my_total_conflict_set.update(conflict_set_from_below)
                print(f"  (Conflicto en '{var}' reportado desde abajo. "
                      f"Probando siguiente valor.)")
            else:
                # NO. El fallo no tiene que ver conmigo.
                # (Ej. Falló 'V' por 'SA', y yo soy 'NSW').
                # No tiene sentido que yo pruebe otros valores ('Verde', 'Azul').
                # Debo fallar INMEDIATAMENTE y pasar el conflicto hacia arriba.
                print(f"  ¡SALTO! Variable '{var}' no está en "
                      f"{conflict_set_from_below}. Saltando...")
                del assignment[var] # Deshacer mi asignación
                return ('FAILURE', conflict_set_from_below) # Pasar el mismo set

            # 11. Deshacer la asignación para probar el siguiente valor
            del assignment[var]
            
        else:
            # El valor falló la comprobación simple (pasado)
            my_total_conflict_set.update(conflicts)

    # 12. Si el bucle 'for' termina, probé todos mis valores y fallaron.
    print(f"  Fallo en '{var}'. Todos los valores probados. "
          f"Reportando conflictos: {my_total_conflict_set}")
    return ('FAILURE', my_total_conflict_set)

# --- Función principal para iniciar la búsqueda ---
def solve_csp_cbj(variables, domains, constraints):
    print("Iniciando Búsqueda con Salto Dirigido por Conflictos (CBJ)...")
    (status, data) = backtracking_cbj_recursive({}, variables, domains, constraints)
    
    if status == 'SUCCESS':
        print("\n--- Solución Final ---")
        for var, val in sorted(data.items()):
            print(f"{var}: {val}")
    else:
        print("\nNo se encontró solución.")

# --- Ejecutamos el algoritmo ---
solve_csp_cbj(variables, original_domains, constraints)