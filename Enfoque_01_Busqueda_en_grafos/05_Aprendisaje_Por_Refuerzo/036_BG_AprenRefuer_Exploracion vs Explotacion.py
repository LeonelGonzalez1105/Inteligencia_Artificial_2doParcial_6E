import random

# (ACTIONS sería ['N', 'S', 'E', 'W'])
ACTIONS = ['N', 'S', 'E', 'W']
# (Q_table[s] sería {'N': 0.5, 'S': 0.2, 'E': 0.8, 'W': 0.1})

def choose_action(s, Q_table, epsilon):
    """
    Implementa la estrategia Epsilon-Greedy para balancear
    Exploración vs. Explotación.
    
    Args:
        s: El estado actual.
        Q_table: El "cerebro" del agente.
        epsilon (float): La probabilidad de explorar (ej. 0.1 para 10%).
    """
    
    # 1. Tirar un dado
    if random.random() < epsilon:
        # --- 2. FASE DE EXPLORACIÓN ---
        # (El dado fue menor a 0.1)
        # Ignoramos la Q-table y elegimos una acción AL AZAR.
        print(f"  (Acción: Explorando al azar...)")
        return random.choice(ACTIONS)
    else:
        # --- 3. FASE DE EXPLOTACIÓN ---
        # (El dado fue mayor a 0.1)
        # Elegimos la mejor acción que conocemos.
        print(f"  (Acción: Explotando la mejor opción...)")
        # Esto encuentra la 'key' (acción) con el 'value' (Q-value) más alto
        return max(Q_table[s], key=Q_table[s].get)