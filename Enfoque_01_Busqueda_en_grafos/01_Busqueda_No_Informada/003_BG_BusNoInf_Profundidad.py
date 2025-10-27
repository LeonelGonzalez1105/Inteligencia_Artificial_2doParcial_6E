def dfs_recursive(graph, start_node, visited=None):
    """
    Implementa la Búsqueda en Profundidad (DFS) usando recursión.

    Args:
        graph (dict): El grafo representado como una lista de adyacencia.
        start_node (str): El nodo desde el cual comenzar la búsqueda.
        visited (set, optional): Un conjunto para rastrear nodos visitados.
                                 Se pasa entre llamadas recursivas.
    """
    
    # 1. Inicializar el conjunto de visitados si es la primera llamada
    if visited is None:
        visited = set()
        print(f"Iniciando DFS recursivo desde: {start_node}")

    # 2. Marcar el nodo actual como visitado y procesarlo (imprimirlo)
    visited.add(start_node)
    print(f"  Visitando nodo: {start_node}")

    # --- (Opcional) Aquí podrías comprobar si 'start_node' es tu objetivo ---
    # if start_node == 'OBJETIVO':
    #     print("¡Objetivo encontrado!")
    #     # Aquí podrías tener que manejar cómo "devolver" que lo encontraste
    # ---------------------------------------------------------------------

    # 3. Explorar los vecinos
    for neighbor in graph.get(start_node, []):
        
        # 4. ¡La clave de DFS!
        # Si al vecino NO lo hemos visitado...
        if neighbor not in visited:
            
            # 5. ...hacemos la llamada recursiva.
            # El algoritmo se va "profundo" por este vecino ANTES
            # de continuar con los otros vecinos del nodo actual.
            dfs_recursive(graph, neighbor, visited)
            print(f"    ...Retrocediendo (backtracking) a: {start_node}")


# --- Definimos nuestro grafo de ejemplo (el mismo de BFS) ---
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
dfs_recursive(graph_example, 'A')