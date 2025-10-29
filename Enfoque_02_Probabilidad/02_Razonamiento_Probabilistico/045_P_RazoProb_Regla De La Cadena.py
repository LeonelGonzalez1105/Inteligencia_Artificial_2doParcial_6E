# --- 1. Definir la Estructura de una Red Bayesiana ---
# (Solo las conexiones, no las CPTs)
#    A --> C --> E
#    |     ^
#    v     |
#    B --> D
#
#    F --> E (F es "otro padre" del hijo de C)

# Usamos un diccionario para representar las conexiones (quiénes son mis padres)
network_structure = {
    'A': [],
    'B': ['A'],
    'C': ['A', 'D'],
    'D': ['B'],
    'E': ['C', 'F'],
    'F': []
}

# --- 2. El "Algoritmo": Encontrar el Manto de Markov ---

def find_markov_blanket(node, network):
    """
    Encuentra el Manto de Markov de un 'node' dado
    la 'network' (estructura).
    """
    
    print(f"\n--- Encontrando el Manto de Markov para el Nodo '{node}' ---")
    
    markov_blanket = set()
    
    # 1. Añadir los PADRES de 'node'
    parents = network.get(node, [])
    for p in parents:
        markov_blanket.add(p)
    print(f"  1. Padres: {set(parents)}")

    # 2. Encontrar y añadir los HIJOS de 'node'
    children = set()
    for n, n_parents in network.items():
        if node in n_parents:
            children.add(n)
    markov_blanket.update(children)
    print(f"  2. Hijos: {children}")

    # 3. Encontrar y añadir los OTROS PADRES de esos hijos
    other_parents = set()
    for child in children:
        childs_parents = network.get(child, [])
        for cp in childs_parents:
            if cp != node: # No nos añadimos a nosotros mismos
                other_parents.add(cp)
    markov_blanket.update(other_parents)
    print(f"  3. Otros Padres de Hijos: {other_parents}")
    
    print(f"\n  >> Manto de Markov Completo para '{node}': {markov_blanket}")
    return markov_blanket

# --- 3. Ejecutar la Búsqueda ---

# Caso 1: Un nodo en medio (C)
#    A --> C --> E
#    |     ^     ^
#    v     |     |
#    B --> D     F
# Manto(C) = {Padres: A, D}, {Hijos: E}, {Otros Padres de E: F}
# Manto(C) = {A, D, E, F}
find_markov_blanket('C', network_structure)

# Caso 2: Un nodo raíz (A)
# Manto(A) = {Padres: }, {Hijos: B, C}, {Otros Padres de B: }, {Otros Padres de C: D}
# Manto(A) = {B, C, D}
find_markov_blanket('A', network_structure)