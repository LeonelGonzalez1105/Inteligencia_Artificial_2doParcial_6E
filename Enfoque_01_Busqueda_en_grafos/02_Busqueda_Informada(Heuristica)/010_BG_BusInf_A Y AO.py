import heapq

def a_star_search(graph, start_node, goal_node, heuristics):
    """
    Implementa la Búsqueda A* (A-Star).

    Args:
        graph (dict): El grafo con costos. 
                      Formato: {'A': [('B', cost), ('C', cost)], ...}
        start_node (str): El nodo de inicio.
        goal_node (str): El nodo objetivo.
        heuristics (dict): Un diccionario con el valor heurístico (h(n))
                           para cada nodo.
    """
    
    # 1. Cola de prioridad. Guardará tuplas de (f(n), g(n), nodo)
    #    f(n) = g(n) + h(n). Lo ponemos primero para que heapq ordene por él.
    priority_queue = []
    
    # 2. Inicializamos g(n) y h(n) para el nodo inicial
    g_start = 0
    h_start = heuristics.get(start_node, 0)
    f_start = g_start + h_start
    
    heapq.heappush(priority_queue, (f_start, g_start, start_node))
    
    # 3. Diccionario para guardar el costo g(n) MÁS BAJO encontrado 
    #    hasta ahora para llegar a cada nodo. (¡Igual que en UCS!)
    g_costs = {start_node: 0}
    
    # 4. Diccionario para reconstruir el camino
    path_from = {start_node: None}
    
    print(f"Iniciando Búsqueda A* desde '{start_node}' para encontrar '{goal_node}'")

    while priority_queue:
        
        # 5. ¡LA CLAVE DE A*!
        # Sacamos el nodo con el MENOR f(n) = g(n) + h(n)
        current_f, current_g, current_node = heapq.heappop(priority_queue)
        
        print(f"\n  Visitando nodo: '{current_node}' "
              f"(f={current_f:.2f}, g={current_g:.2f}, h={current_f-current_g:.2f})")

        # 6. Optimización: Si encontramos un camino MÁS CORTO a este nodo
        #    antes, ignoramos esta versión "más larga".
        if current_g > g_costs.get(current_node, float('inf')):
            continue

        # 7. ¡OBJETIVO ENCONTRADO!
        if current_node == goal_node:
            print(f"¡Objetivo '{goal_node}' alcanzado con costo total {current_g}!")
            
            path = []
            node = goal_node
            while node is not None:
                path.append(node)
                node = path_from[node]
            path.reverse()
            print(f"  Camino encontrado: {' -> '.join(path)}")
            return

        # 8. Exploramos los vecinos
        for neighbor, edge_cost in graph.get(current_node, []):
            
            # 9. Calculamos el nuevo g(n) para este vecino
            new_g = current_g + edge_cost
            
            # 10. ¡Igual que en UCS! Si es un camino MÁS BARATO al vecino...
            if new_g < g_costs.get(neighbor, float('inf')):
                
                # ...actualizamos su g(n)
                g_costs[neighbor] = new_g
                
                # ...calculamos su h(n)
                h_neighbor = heuristics.get(neighbor, 0)
                
                # ...calculamos su f(n)
                f_neighbor = new_g + h_neighbor
                
                # ...guardamos el camino
                path_from[neighbor] = current_node
                
                # ...y lo metemos a la cola de prioridad
                heapq.heappush(priority_queue, (f_neighbor, new_g, neighbor))
                print(f"    -> Encolando vecino: '{neighbor}' (f={f_neighbor:.2f})")
                
    print(f"No se pudo encontrar un camino de '{start_node}' a '{goal_node}'.")

# --- Grafo de ejemplo con COSTOS y HEURÍSTICAS ---
#
#       A
#   (10)/ \(1)
#     /     \
#    B ----- C  <- Objetivo (G)
# (1)\(2) (10)
#   \ /     /
#    D ----/
#
# Queremos ir de A a C
#
# Costos Reales g(n):
# A->B = 10
# A->C = 1
# B->D = 1
# B->C = 2
# D->C = 10
#
# Heurísticas h(n) (Estimación "línea recta" a C):
# h(A) = 3
# h(B) = 2
# h(D) = 8
# h(C) = 0
#
# ----------------------------------------------------
# Camino 1: A -> C
#   f(C) = g(C) + h(C) = 1 + 0 = 1
# Camino 2: A -> B -> C
#   f(B) = g(B) + h(B) = 10 + 2 = 12
#   f(C) = g(C) + h(C) = (10+2) + 0 = 12
# Camino 3: A -> B -> D -> C
#   f(D) = g(D) + h(D) = (10+1) + 8 = 19
#   f(C) = g(C) + h(C) = (10+1+10) + 0 = 21
#
# A* explorará A, luego C (porque f=1) y terminará.
# ----------------------------------------------------

graph_costs = {
    'A': [('B', 10), ('C', 1)], # A->C es súper barato (g=1)
    'B': [('D', 1), ('C', 2)],
    'D': [('C', 10)],
    'C': []
}
heuristic_values = { 'A': 3, 'B': 2, 'D': 8, 'C': 0 }

# --- Ejecutamos el algoritmo ---
a_star_search(graph_costs, 'A', 'C', heuristic_values)

# --- ¿Qué pasaría si la heurística fuera MALA? ---
# h(A) = 3
# h(B) = 2
# h(D) = 8
# h(C) = 0
# ¡PERO A->C cuesta 100 en lugar de 1!
print("\n--- PRUEBA 2: A->C es muy caro ---")
graph_costs_2 = {
    'A': [('B', 10), ('C', 100)], # A->C ahora es carísimo
    'B': [('D', 1), ('C', 2)],
    'D': [('C', 10)],
    'C': []
}
# A* ahora debe encontrar A->B->C
a_star_search(graph_costs_2, 'A', 'C', heuristic_values)