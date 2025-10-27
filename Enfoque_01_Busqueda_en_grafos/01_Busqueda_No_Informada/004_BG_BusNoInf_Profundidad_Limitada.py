def dls(graph, start_node, goal_node, limit, depth=0, visited=None):
    """
    Implementa la Búsqueda en Profundidad Limitada (DLS).

    Args:
        graph (dict): El grafo como lista de adyacencia.
        start_node (str): El nodo que estamos visitando actualmente.
        goal_node (str): El nodo objetivo que buscamos.
        limit (int): La profundidad máxima a explorar.
        depth (int, optional): La profundidad actual. Inicia en 0.
        visited (set, optional): Conjunto de nodos visitados (para ciclos).
    
    Returns:
        bool: True si se encontró el objetivo, False si no.
    """
    
    # 1. Inicializar 'visited' en la primera llamada (solo para grafos con ciclos)
    if visited is None:
        visited = set()
        print(f"Iniciando DLS desde '{start_node}' para buscar '{goal_node}' "
              f"con límite={limit}")

    # 2. Marcar el nodo actual como visitado
    visited.add(start_node)
    print(f"  (Profundidad: {depth}) Visitando nodo: {start_node}")

    # 3. Comprobar si es el objetivo
    if start_node == goal_node:
        print(f"¡Objetivo '{goal_node}' encontrado en profundidad {depth}!")
        return True  # ¡Éxito!

    # 4. ¡La clave de DLS! Comprobar si hemos llegado al límite
    if depth == limit:
        print(f"    -> Límite de profundidad {limit} alcanzado. Retrocediendo.")
        return False  # Cortamos la búsqueda por esta rama

    # 5. Si no hemos llegado al límite, exploramos vecinos (recursión)
    for neighbor in graph.get(start_node, []):
        
        # Omitimos visitar nodos que ya están en nuestro camino actual
        if neighbor not in visited:
            
            # 6. Llamada recursiva, incrementando la profundidad
            # Si CUALQUIERA de las llamadas recursivas encuentra el objetivo...
            if dls(graph, neighbor, goal_node, limit, depth + 1, visited):
                return True # ...propagamos el éxito hacia arriba

    # 7. Si exploramos todos los vecinos y nadie encontró el objetivo
    print(f"    (Profundidad: {depth}) No hay más caminos desde '{start_node}'. Retrocediendo.")
    return False

# --- Definimos nuestro grafo de ejemplo ---
#       'A'
#      /   \
#     'B'   'C'
#    / \     /
#   'D' 'E' 'F'
graph_example = {
    'A': ['B', 'C'],
    'B': ['D', 'E'], # Quitamos las aristas ('A') para hacerlo un árbol simple
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

# --- Ejecutamos el algoritmo (Prueba 1: Límite muy corto) ---
print("--- PRUEBA 1: Límite = 1 (No debería encontrar 'E') ---")
found = dls(graph_example, 'A', 'E', limit=1)
print(f"Resultado final: Objetivo encontrado = {found}\n")

# --- Ejecutamos el algoritmo (Prueba 2: Límite suficiente) ---
print("--- PRUEBA 2: Límite = 2 (Sí debería encontrar 'E') ---")
found = dls(graph_example, 'A', 'E', limit=2)
print(f"Resultado final: Objetivo encontrado = {found}\n")