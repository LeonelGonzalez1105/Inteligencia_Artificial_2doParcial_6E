import collections
import copy

# --- Definición del CSP (igual que antes) ---
variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
original_domains = {
    'WA': ['Rojo', 'Verde'], # ¡DOMINIO LIMITADO PARA VER EL EFECTO!
    'NT': ['Rojo', 'Verde', 'Azul'],
    'SA': ['Rojo', 'Verde', 'Azul'],
    'Q':  ['Rojo', 'Verde', 'Azul'],
    'NSW':['Rojo', 'Verde'], # ¡DOMINIO LIMITADO!
    'V':  ['Rojo', 'Verde', 'Azul'],
    'T':  ['Rojo', 'Verde', 'Azul']
}
constraints_dict = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'SA', 'Q'],
    'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
    'Q':  ['NT', 'SA', 'NSW'],
    'NSW':['SA', 'Q', 'V'],
    'V':  ['SA', 'NSW'],
    'T':  []
}
# ----------------------------------------------

def get_all_arcs(constraints):
    """Crea la lista inicial de trabajo (cola) para AC-3."""
    queue = collections.deque()
    for var in constraints:
        for neighbor in constraints[var]:
            queue.append((var, neighbor))
    return queue

def revise(domains, var1, var2):
    """
    Revisa el arco (var1, var2).
    Elimina valores de domain[var1] si no tienen "soporte" en domain[var2].
    """
    revised = False
    values_to_remove = []

    # Para cada valor 'x' en el dominio de var1...
    for x in domains[var1]:
        has_support = False
        # ...buscar si existe un valor 'y' en var2 que sea compatible
        for y in domains[var2]:
            if x != y: # La restricción es "no ser iguales"
                has_support = True
                break
        
        # Si 'x' no tiene ningún 'y' compatible, es un valor imposible
        if not has_support:
            values_to_remove.append(x)
            revised = True

    # Eliminar los valores imposibles
    for val in values_to_remove:
        domains[var1].remove(val)
        
    return revised # Devuelve True si se eliminó algo

def ac3(variables, domains, constraints):
    """
    Implementa el algoritmo AC-3 para propagar restricciones.
    Modifica 'domains' in-situ.
    Devuelve False si encuentra una inconsistencia (dominio vacío).
    """
    
    # 1. Crear la cola inicial con todos los arcos
    queue = get_all_arcs(constraints)
    print(f"Iniciando AC-3... Tamaño inicial de la cola: {len(queue)}")
    
    # 2. Mientras la cola no esté vacía
    while queue:
        # a. Sacar un arco (var_i, var_j)
        (var_i, var_j) = queue.popleft()
        
        # b. Revisar el arco
        if revise(domains, var_i, var_j):
            print(f"  -> Revisando ({var_i}, {var_j}): Dominio de {var_i} "
                  f"cambió a {domains[var_i]}")
            
            # c. Si el dominio de var_i se quedó vacío, no hay solución
            if not domains[var_i]:
                print("¡INCONSISTENCIA! Dominio vacío encontrado.")
                return False
                
            # d. Añadir de nuevo los arcos de los vecinos de var_i
            for var_k in constraints[var_i]:
                if var_k != var_j:
                    queue.append((var_k, var_i))
                    
    print("AC-3 finalizado. Dominios podados.")
    return True

# --- Ejecutamos el algoritmo ---
print("--- Dominios Originales (Limitados) ---")
print(original_domains)

# Hacemos una copia para no destruir el original
domains_copy = copy.deepcopy(original_domains)

# 1. Pre-procesamiento con AC-3
ac3_success = ac3(variables, domains_copy, constraints_dict)

if ac3_success:
    print("\n--- Dominios Podados por AC-3 ---")
    print(domains_copy)
    
    # 2. (Opcional) Resolver con el backtracking simple
    # ... (Aquí llamaríamos a la función 'solve_csp' del #18,
    #      pero pasándole los 'domains_copy' ya podados) ...
    # solve_csp(variables, domains_copy, constraints_dict)
else:
    print("\nEl problema no tiene solución (detectado por AC-3).")