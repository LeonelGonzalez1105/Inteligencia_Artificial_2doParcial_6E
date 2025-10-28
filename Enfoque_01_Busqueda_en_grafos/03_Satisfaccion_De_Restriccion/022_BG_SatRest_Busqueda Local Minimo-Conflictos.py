import random

# --- Definición del CSP (igual que antes) ---
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

def get_conflicted_variables(assignment, constraints):
    """Devuelve una lista de todas las variables que están en conflicto."""
    conflicted_vars = []
    for var in assignment:
        for neighbor in constraints[var]:
            # Si el vecino ya está asignado (siempre lo estará) y tiene mi mismo valor
            if neighbor in assignment and assignment[neighbor] == assignment[var]:
                conflicted_vars.append(var)
                break # Solo necesito añadir la variable una vez
    return conflicted_vars

def count_conflicts(variable, value, assignment, constraints):
    """
    Cuenta cuántos conflictos causaría asignar 'value' a 'variable',
    dada la asignación actual.
    """
    count = 0
    for neighbor in constraints[variable]:
        if assignment[neighbor] == value:
            count += 1
    return count

def min_conflicts(variables, domains, constraints, max_steps=1000):
    """
    Implementa el algoritmo de Mínimos-Conflictos.
    """
    
    # 1. Generar una asignación inicial aleatoria completa
    current_assignment = {}
    for var in variables:
        current_assignment[var] = random.choice(domains[var])
        
    print(f"Iniciando Mínimos-Conflictos...")
    print(f"Asignación inicial (aleatoria): {current_assignment}")
    
    # 2. Bucle de Reparación
    for i in range(max_steps):
        
        # 3. Comprobar si es una solución
        conflicted_vars = get_conflicted_variables(current_assignment, constraints)
        
        if not conflicted_vars:
            print(f"\n¡Solución encontrada en {i} pasos!")
            return current_assignment
            
        # 4. Seleccionar una variable en conflicto AL AZAR
        var_to_fix = random.choice(conflicted_vars)
        
        # 5. Encontrar el valor de MÍNIMOS-CONFLICTOS
        min_count = float('inf')
        best_values = [] # Puede haber empates
        
        # 6. Evaluar cada valor posible para esa variable
        for value in domains[var_to_fix]:
            conflicts_count = count_conflicts(var_to_fix, value, current_assignment, constraints)
            
            if conflicts_count < min_count:
                min_count = conflicts_count
                best_values = [value]
            elif conflicts_count == min_count:
                best_values.append(value)
                
        # 7. Asignar el nuevo valor (rompiendo empates al azar)
        new_value = random.choice(best_values)
        current_assignment[var_to_fix] = new_value
        
        if i % 10 == 0: # Imprimir el progreso de vez en cuando
            print(f"  Paso {i}: Arreglando '{var_to_fix}', "
                  f"Total conflictos: {len(conflicted_vars)}")

    print(f"\nSe alcanzó el límite de {max_steps} pasos. No se encontró solución.")
    return None

# --- Ejecutamos el algoritmo ---
solution = min_conflicts(variables, domains, constraints)

if solution:
    print("\n--- Solución Final ---")
    for var, val in sorted(solution.items()):
        print(f"{var}: {val}")