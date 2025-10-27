import collections

# --- Definimos las estructuras de la Frontera ---

class QueueFrontier:
    """Implementa una frontera tipo Cola (FIFO) para BFS."""
    def __init__(self):
        self.frontier = collections.deque()
    
    def add(self, node):
        self.frontier.append(node)
        
    def remove(self):
        return self.frontier.popleft()
        
    def is_empty(self):
        return len(self.frontier) == 0

class StackFrontier:
    """Implementa una frontera tipo Pila (LIFO) para DFS."""
    def __init__(self):
        self.frontier = [] # Usamos una lista normal
    
    def add(self, node):
        self.frontier.append(node)
        
    def remove(self):
        return self.frontier.pop() # ¡La única diferencia!
        
    def is_empty(self):
        return len(self.frontier) == 0

# --- Algoritmo Genérico de Búsqueda en Grafos ---

def generic_graph_search(graph, start_node, goal_node, frontier_object):
    """
    Implementa el algoritmo genérico de Búsqueda en Grafos.
    
    Args:
        graph (dict): El grafo como lista de adyacencia.
        start_node (str): El nodo de inicio.
        goal_node (str): El nodo objetivo.
        frontier_object: Una instancia de QueueFrontier (BFS) o StackFrontier (DFS).
    """
    
    # 1. El conjunto de "Explorados" o "Visitados".
    # Esta es la "memoria" que nos protege de los ciclos.
    visited = set()
    
    # 2. La Frontera (el tipo de objeto define la estrategia)
    frontier = frontier_object
    
    # 3. Guardamos los "padres" para reconstruir el camino
    path_from = {start_node: None}
    
    # 4. Empezamos con el nodo inicial
    frontier.add(start_node)
    
    print(f"Iniciando búsqueda genérica desde '{start_node}'...")

    # 5. Bucle principal
    while not frontier.is_empty():
        
        # 6. Sacamos un nodo de la frontera
        # (Si es Cola -> saca el más viejo. Si es Pila -> saca el más nuevo)
        current_node = frontier.remove()
        
        print(f"  -> Explorando: '{current_node}'")
        
        # 7. Si es el objetivo, ¡terminamos!
        if current_node == goal_node:
            print(f"¡Objetivo '{goal_node}' encontrado!")
            
            # Reconstruir camino
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = path_from[current_node]
            path.reverse()
            return path

        # 8. ¡LA CLAVE DEL GRAFO!
        # Si ya lo exploramos, lo ignoramos para evitar ciclos.
        if current_node in visited:
            print(f"    (Nodo '{current_node}' ya explorado, ignorando)")
            continue
            
        # 9. Si no, lo marcamos como explorado
        visited.add(current_node)
        
        # 10. Añadimos a sus vecinos a la frontera
        for neighbor in graph.get(current_node, []):
            
            # Solo añadimos si NO está visitado Y NO está ya en el camino
            # (path_from es una forma de saber si ya lo descubrimos)
            if neighbor not in path_from:
                path_from[neighbor] = current_node # Guardamos el camino
                frontier.add(neighbor)
                print(f"    -> Descubierto vecino: '{neighbor}'")

    print(f"Objetivo '{goal_node}' no encontrado.")
    return None

# --- Grafo de ejemplo CON CICLOS ---
#       'A' ----- 'B'
#      / | \     /
#     /  |  \   /
#    'C'-'D'--'E'
graph_with_cycles = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'E'],
    'C': ['A', 'D'],
    'D': ['A', 'C', 'E'],
    'E': ['B', 'D']
}

# --- PRUEBA 1: Usando la Cola (BFS) ---
print("--- PRUEBA CON BÚSQUEDA EN ANCHURA (BFS) ---")
frontier_bfs = QueueFrontier()
path_bfs = generic_graph_search(graph_with_cycles, 'A', 'E', frontier_bfs)
if path_bfs:
    print(f"Camino BFS: {' -> '.join(path_bfs)}\n")

# --- PRUEBA 2: Usando la Pila (DFS) ---
print("--- PRUEBA CON BÚSQUEDA EN PROFUNDIDAD (DFS) ---")
frontier_dfs = StackFrontier()
path_dfs = generic_graph_search(graph_with_cycles, 'A', 'E', frontier_dfs)
if path_dfs:
    print(f"Camino DFS: {' -> '.join(path_dfs)}\n")