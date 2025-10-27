import heapq

def ucs(graph, start_node, goal_node):
    """
    Implementa la Búsqueda de Costo Uniforme (UCS) en un grafo con pesos.

    Args:
        graph (dict): El grafo como lista de adyacencia con pesos.
                      Formato: {'A': [('B', 5), ('C', 1)], ...}
                      o también: {'A': [(5, 'B'), (1, 'C')], ...}
                      ¡Vamos a usar (costo, vecino) para que funcione bien con heapq!
        start_node (str): El nodo de inicio.
        goal_node (str): El nodo objetivo que queremos alcanzar.
    """
    
    # 1. Una cola de prioridad (min-heap).
    # Guardará tuplas de (costo_acumulado, nodo).
    # heapq siempre ordena por el primer elemento de la tupla.
    priority_queue = []
    heapq.heappush(priority_queue, (0, start_node))  # (Costo 0 para llegar al inicio)

    # 2. Un diccionario para guardar el costo MÁS BAJO encontrado 
    # hasta ahora para llegar a cada nodo.
    costs = {start_node: 0}
    
    # 3. Un diccionario para reconstruir el camino al final.
    # Guarda: {nodo_hijo: nodo_padre}
    path_from = {start_node: None}
    
    print(f"Iniciando UCS desde '{start_node}' para encontrar '{goal_node}'")

    # 4. Mientras la cola de prioridad NO esté vacía...
    while priority_queue:
        
        # 5. Sacamos el nodo con el MENOR costo acumulado
        current_cost, current_node = heapq.heappop(priority_queue)
        
        print(f"\n  Visitando nodo: '{current_node}' (Costo acumulado: {current_cost})")

        # 6. (Opcional) Si un nodo se procesa con un costo mayor al ya guardado,
        # significa que encontramos un camino más rápido antes. Lo ignoramos.
        if current_cost > costs.get(current_node, float('inf')):
            print(f"    (Ignorando, ya encontramos un camino más barato a '{current_node}')")
            continue

        # 7. ¡OBJETIVO ENCONTRADO!
        if current_node == goal_node:
            print(f"¡Objetivo '{goal_node}' alcanzado con costo total: {current_cost}!")
            
            # --- Reconstruir el camino ---
            path = []
            node = goal_node
            while node is not None:
                path.append(node)
                node = path_from[node]
            path.reverse()  # Le damos la vuelta para que sea inicio -> fin
            print(f"  Camino encontrado: {' -> '.join(path)}")
            return
        
        # 8. Exploramos los vecinos
        for edge_cost, neighbor in graph.get(current_node, []):
            
            # 9. Calculamos el nuevo costo para llegar a ESE vecino
            new_cost = current_cost + edge_cost
            
            # 10. ¡La clave de UCS!
            # Si no lo hemos visitado O encontramos un camino MÁS BARATO...
            if neighbor not in costs or new_cost < costs[neighbor]:
                
                # ...actualizamos su costo
                costs[neighbor] = new_cost
                
                # ...guardamos de dónde venimos
                path_from[neighbor] = current_node
                
                # ...y lo metemos a la cola de prioridad
                heapq.heappush(priority_queue, (new_cost, neighbor))
                print(f"    -> Encolando vecino: '{neighbor}' (Nuevo costo: {new_cost})")
                
    print(f"No se pudo encontrar un camino de '{start_node}' a '{goal_node}'.")

# --- Definimos nuestro grafo de ejemplo con COSTOS ---
#       'A'
#     (1)/ \(5)
#     /     \
#   'C'-(3)-'B'
#    |       |
# (10)|     (2)
#    |       |
#   'D'-(1)-'E'
#
# Queremos ir de 'A' a 'E'
# Camino A->B->E = 5 + 2 = 7
# Camino A->C->B->E = 1 + 3 + 2 = 6  (¡Más barato!)
# Camino A->C->D->E = 1 + 10 + 1 = 12

graph_example_ucs = {
    'A': [(1, 'C'), (5, 'B')],
    'B': [(2, 'E')],
    'C': [(3, 'B'), (10, 'D')],
    'D': [(1, 'E')],
    'E': [], # 'E' es un nodo final en este ejemplo
}

# --- Ejecutamos el algoritmo ---
ucs(graph_example_ucs, 'A', 'E')