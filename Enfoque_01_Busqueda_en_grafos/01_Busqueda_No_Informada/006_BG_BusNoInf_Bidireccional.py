import collections

def reconstruct_path(start_node, goal_node, intersection_node, 
                     path_from_start, path_from_goal):
    """
    Ayudante para unir los dos caminos en el nodo de intersección.
    """
    
    # 1. Camino desde el inicio hasta la intersección
    path1 = []
    node = intersection_node
    while node is not None:
        path1.append(node)
        node = path_from_start.get(node) # Usamos .get() por si acaso
    path1.reverse() # Invertir: [start, ..., intersection]
    
    # 2. Camino desde la intersección hasta el final
    path2 = []
    node = path_from_goal.get(intersection_node) # Empezamos con el "siguiente"
    while node is not None:
        path2.append(node)
        node = path_from_goal.get(node)
        
    # El camino final es path1 + path2
    return path1 + path2

def bidirectional_bfs(graph, start_node, goal_node):
    """
    Implementa la Búsqueda Bidireccional usando dos BFS.
    Asume un grafo no dirigido.
    """
    
    # --- Estructuras para la búsqueda DESDE EL INICIO ---
    queue_start = collections.deque([start_node])
    visited_start = {start_node}
    path_from_start = {start_node: None} # {hijo: padre}

    # --- Estructuras para la búsqueda DESDE EL FINAL ---
    queue_goal = collections.deque([goal_node])
    visited_goal = {goal_node}
    path_from_goal = {goal_node: None} # {hijo: padre} (en sentido inverso)

    print(f"Iniciando Búsqueda Bidireccional: '{start_node}' <-> '{goal_node}'")

    # 3. Mientras ambas colas tengan nodos por explorar
    while queue_start and queue_goal:
        
        # --- PASO 1: Expandir un nivel desde el INICIO ---
        if queue_start:
            current_start = queue_start.popleft()
            print(f"  -> Buscando desde INICIO: Visitando '{current_start}'")

            # 4. ¡LA CLAVE! ¿Este nodo ya fue visitado por la OTRA búsqueda?
            if current_start in visited_goal:
                print(f"¡Intersección encontrada en: '{current_start}'!")
                return reconstruct_path(start_node, goal_node, current_start,
                                        path_from_start, path_from_goal)

            for neighbor in graph.get(current_start, []):
                if neighbor not in visited_start:
                    visited_start.add(neighbor)
                    path_from_start[neighbor] = current_start
                    queue_start.append(neighbor)
        
        # --- PASO 2: Expandir un nivel desde el FINAL ---
        if queue_goal:
            current_goal = queue_goal.popleft()
            print(f"  <- Buscando desde FINAL: Visitando '{current_goal}'")

            # 5. ¡LA CLAVE OTRA VEZ! ¿Este nodo ya fue visitado por la OTRA búsqueda?
            if current_goal in visited_start:
                print(f"¡Intersección encontrada en: '{current_goal}'!")
                return reconstruct_path(start_node, goal_node, current_goal,
                                        path_from_start, path_from_goal)

            for neighbor in graph.get(current_goal, []):
                if neighbor not in visited_goal:
                    visited_goal.add(neighbor)
                    path_from_goal[neighbor] = current_goal
                    queue_goal.append(neighbor)

    # 6. Si una cola se vacía, no hay camino
    print("No se encontró un camino entre los nodos.")
    return None

# --- Definimos un grafo de ejemplo (NO DIRIGIDO) ---
#      'A' --- 'B' --- 'C' --- 'D'
#       |       |               |
#      'E' --- 'F' --- 'G' --- 'H'
#
# Queremos ir de 'A' a 'H'
graph_example = {
    'A': ['B', 'E'],
    'B': ['A', 'C', 'F'],
    'C': ['B', 'D'],
    'D': ['C', 'H'],
    'E': ['A', 'F'],
    'F': ['B', 'E', 'G'],
    'G': ['F', 'H'],
    'H': ['D', 'G'],
}

# --- Ejecutamos el algoritmo ---
path = bidirectional_bfs(graph_example, 'A', 'H')
if path:
    print(f"\nCamino más corto encontrado: {' -> '.join(path)}")