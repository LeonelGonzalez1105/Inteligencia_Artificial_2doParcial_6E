import collections

def bfs(graph, start_node):
    """
    Implementa la Búsqueda en Anchura (BFS) en un grafo.

    Args:
        graph (dict): El grafo representado como una lista de adyacencia.
        start_node (str): El nodo desde el cual comenzar la búsqueda.
    """
    
    # 1. Un conjunto (set) para guardar los nodos que ya hemos visitado.
    # Usamos un set para que la comprobación de "ya lo visité?" sea súper rápida.
    visited = set()
    
    # 2. Una cola (queue) para llevar el orden de visita.
    # Usamos collections.deque porque es muy eficiente para sacar (pop) 
    # y meter (append) elementos por ambos lados.
    # Empezamos la cola con nuestro nodo inicial.
    queue = collections.deque([start_node])
    
    # 3. Marcamos el nodo inicial como visitado
    visited.add(start_node)
    
    print(f"Iniciando BFS desde el nodo: {start_node}")

    # 4. El bucle principal: mientras la cola NO esté vacía...
    while queue:
        
        # 5. Sacamos el primer nodo de la cola (FIFO)
        # Este es el nodo que vamos a "explorar" ahora.
        node = queue.popleft()
        print(f"  Visitando nodo: {node}")

        # --- (Opcional) Aquí podrías comprobar si 'node' es tu objetivo ---
        # if node == 'OBJETIVO':
        #     print("¡Objetivo encontrado!")
        #     return
        # -----------------------------------------------------------------

        # 6. Obtenemos todos los vecinos del nodo actual
        # Usamos .get(node, []) para evitar errores si un nodo no tiene vecinos
        for neighbor in graph.get(node, []):
            
            # 7. Si al vecino NO lo hemos visitado antes...
            if neighbor not in visited:
                
                # 8. Lo marcamos como visitado (para no volver a encolarlo)
                visited.add(neighbor)
                
                # 9. Lo añadimos al FINAL de la cola para visitarlo después
                queue.append(neighbor)
                print(f"    -> Encolando vecino: {neighbor}")

# --- Definimos nuestro grafo de ejemplo ---
#       'A'
#      /   \
#     'B'   'C'
#    / \     /
#   'D' 'E' 'F'
graph_example = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B'],
    'F': ['C']
}

# --- Ejecutamos el algoritmo ---
bfs(graph_example, 'A')