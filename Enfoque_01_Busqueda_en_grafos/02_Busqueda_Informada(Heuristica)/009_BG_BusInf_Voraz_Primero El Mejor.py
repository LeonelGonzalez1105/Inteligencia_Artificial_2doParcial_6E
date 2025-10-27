import heapq

def greedy_best_first_search(graph, start_node, goal_node, heuristics):
    """
    Implementa la Búsqueda Voraz Primero el Mejor (Greedy Best-First Search).

    Args:
        graph (dict): El grafo como lista de adyacencia.
        start_node (str): El nodo de inicio.
        goal_node (str): El nodo objetivo.
        heuristics (dict): Un diccionario con el valor heurístico (h(n))
                           para cada nodo.
    """
    
    # 1. Una cola de prioridad.
    # Guardará tuplas de (valor_heuristico, nodo).
    priority_queue = []
    
    # 2. Calcular la heurística del nodo inicial y añadirlo a la cola.
    h_start = heuristics.get(start_node, float('inf'))
    heapq.heappush(priority_queue, (h_start, start_node))
    
    # 3. Un conjunto para guardar los nodos que YA hemos explorado
    visited = set()
    
    # 4. Un diccionario para reconstruir el camino
    path_from = {start_node: None}
    
    print(f"Iniciando Búsqueda Voraz desde '{start_node}' para encontrar '{goal_node}'")

    while priority_queue:
        
        # 5. ¡LA CLAVE VORAZ!
        # Sacamos el nodo con el MENOR valor HEURÍSTICO (h(n))
        current_h, current_node = heapq.heappop(priority_queue)
        
        print(f"\n  Visitando nodo: '{current_node}' (Heurística: {current_h})")
        
        # 6. Si ya lo exploramos (porque encontramos un camino peor antes),
        # lo ignoramos.
        if current_node in visited:
            continue
            
        visited.add(current_node)

        # 7. ¡OBJETIVO ENCONTRADO!
        if current_node == goal_node:
            print(f"¡Objetivo '{goal_node}' alcanzado!")
            
            # Reconstruir el camino
            path = []
            node = goal_node
            while node is not None:
                path.append(node)
                node = path_from[node]
            path.reverse()
            print(f"  Camino encontrado: {' -> '.join(path)}")
            return
        
        # 8. Exploramos los vecinos
        for neighbor in graph.get(current_node, []):
            
            if neighbor not in visited:
                # 9. Obtenemos la heurística del vecino
                h_neighbor = heuristics.get(neighbor, float('inf'))
                
                # 10. Lo metemos a la cola de prioridad
                heapq.heappush(priority_queue, (h_neighbor, neighbor))
                
                # Guardamos el camino
                # (Nota: si ya tenía un padre, esto lo puede sobrescribir)
                path_from[neighbor] = current_node
                print(f"    -> Encolando vecino: '{neighbor}' (Heurística: {h_neighbor})")
                
    print(f"No se pudo encontrar un camino de '{start_node}' a '{goal_node}'.")

# --- Grafo de ejemplo ---
#       A
#      / \
#     B   C
#    / \ / \
#   D  E F  G  <-- Objetivo
#
# A->B->E->G (Camino 1)
# A->C->F (Camino 2)
# A->C->G (Camino 3 - El que debería encontrar)
graph_example = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [],
    'E': ['G'],
    'F': [],
    'G': []
}

# --- Valores Heurísticos (h(n)) "inventados" ---
# (La distancia "estimada" desde cada nodo hasta G)
heuristic_values = {
    'A': 10,
    'B': 8,   # A B parece un poco mejor que C
    'C': 9,
    'D': 100, # D es un callejón sin salida (hacemos su h() alta)
    'E': 4,   # E parece muy bueno
    'F': 5,   # F parece bueno
    'G': 0    # El objetivo siempre tiene h=0
}

# --- Ejecutamos el algoritmo ---
greedy_best_first_search(graph_example, 'A', 'G', heuristic_values)