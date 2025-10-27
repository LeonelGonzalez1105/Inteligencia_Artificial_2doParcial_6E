def dls_helper(graph, current_node, goal_node, limit, depth):
    """
    Función de ayuda (Helper) que realiza la DLS para una profundidad dada.
    Esta versión es más simple y solo devuelve True/False.
    """
    
    # 1. Imprimimos la visita (para ver el proceso)
    print(f"  (Límite: {limit}, Profundidad: {depth}) Visitando: {current_node}")

    # 2. Comprobar si es el objetivo
    if current_node == goal_node:
        print(f"¡Objetivo '{goal_node}' encontrado!")
        return True  # ¡Éxito!

    # 3. Comprobar si hemos llegado al límite
    if depth == limit:
        #print(f"    -> Límite alcanzado.")
        return False  # Cortamos la búsqueda

    # 4. Exploramos vecinos (recursión)
    for neighbor in graph.get(current_node, []):
        
        # 5. Llamada recursiva, incrementando la profundidad
        # (Para este ejemplo simple de árbol, no usamos 'visited'
        # para que veas cómo se re-explora. Si tuvieras ciclos,
        # necesitarías pasar un 'visited' para el *camino actual*).
        
        if dls_helper(graph, neighbor, goal_node, limit, depth + 1):
            return True # Propagamos el éxito

    # 6. No se encontró en esta rama
    return False

# --- Función principal de IDDFS ---

def iddfs(graph, start_node, goal_node, max_allowed_depth):
    """
    Implementa la Búsqueda en Profundidad Iterativa (IDDFS).
    
    Args:
        graph (dict): El grafo como lista de adyacencia.
        start_node (str): El nodo de inicio.
        goal_node (str): El nodo objetivo.
        max_allowed_depth (int): El número máximo de iteraciones.
    """
    
    print(f"Iniciando IDDFS desde '{start_node}' para buscar '{goal_node}'"
          f" (Profundidad máx: {max_allowed_depth})\n")
    
    # 1. El bucle iterativo: probamos límite 0, 1, 2, ...
    for limit in range(max_allowed_depth + 1):
        
        print(f"--- INICIANDO BÚSQUEDA CON LÍMITE = {limit} ---")
        
        # 2. Llamamos a DLS con el límite actual
        # "Olvidamos" todo lo de la iteración anterior.
        if dls_helper(graph, start_node, goal_node, limit, depth=0):
            print(f"\nBúsqueda exitosa. Objetivo encontrado en la iteración "
                  f"con límite de profundidad {limit}.")
            return True
        
        print(f"--- Fin de la búsqueda con límite {limit}. Objetivo no encontrado. ---\n")

    print(f"Búsqueda fallida. Objetivo no encontrado "
          f"dentro de la profundidad máxima {max_allowed_depth}.")
    return False


# --- Definimos nuestro grafo de ejemplo (árbol) ---
#       'A'
#      /   \
#     'B'   'C'
#    / \     /
#   'D' 'E' 'F'
graph_example = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

# --- Ejecutamos el algoritmo ---
# Buscamos 'E', que está en profundidad 2
iddfs(graph_example, 'A', 'E', max_allowed_depth=3)