import time

# --- 1. Definir el MDP (El Mundo) ---

# Nuestro mundo es una cuadrícula de 3x4
# _ = Estado normal
# G = Meta (Premio)
# P = Pozo (Castigo)
# X = Muro (No se puede entrar)
GRID = [
    ['_', '_', '_', 'G'],  # Fila 0
    ['_', 'X', '_', 'P'],  # Fila 1
    ['_', '_', '_', '_']   # Fila 2
]
ROWS = len(GRID)
COLS = len(GRID[0])

# Recompensas R(s)
REWARDS = {
    'G': 1.0,   # Premio gordo
    'P': -1.0,  # Castigo
    '_': -0.04, # "Costo de vida" (incentiva a terminar rápido)
    'X': 0      # No se puede entrar
}

# Acciones (A)
ACTIONS = ['N', 'E', 'S', 'W'] # Norte, Este, Sur, Oeste

# Probabilidades de Transición T(s, a, s')
# (Acciones "ruidosas")
TRANSITION_PROBS = {
    'main': 0.8,  # Prob de ir en la dirección deseada
    'left': 0.1,  # Prob de ir a la "izquierda" de la deseada
    'right': 0.1  # Prob de ir a la "derecha" de la deseada
}

# Factor de Descuento (Gamma)
GAMMA = 0.9

# --- 2. El Algoritmo: Iteración de Valores ---

def get_neighbors(s, a):
    """Devuelve los 3 posibles estados s' (main, left, right) a los que 
    una acción 'a' puede llevar desde el estado 's'."""
    r, c = s
    
    # Define la "izquierda" y "derecha" relativas a la acción 'a'
    if a == 'N':
        moves = {'main': (r-1, c), 'left': (r, c-1), 'right': (r, c+1)}
    elif a == 'S':
        moves = {'main': (r+1, c), 'left': (r, c+1), 'right': (r, c-1)}
    elif a == 'E':
        moves = {'main': (r, c+1), 'left': (r-1, c), 'right': (r+1, c)}
    elif a == 'W':
        moves = {'main': (r, c-1), 'left': (r+1, c), 'right': (r-1, c)}
        
    return moves

def get_action_value(s, a, V_k):
    """Calcula la parte de la suma:  Suma[ T(s, a, s') * Vk(s') ]"""
    r, c = s
    action_value = 0.0
    
    moves = get_neighbors(s, a)
    
    for move_type, (next_r, next_c) in moves.items():
        prob = TRANSITION_PROBS[move_type]
        
        # --- Lógica de Muros y Límites ---
        # Si la movida se sale del grid o es un muro, se "choca" y 
        # se queda en el estado original 's'
        if next_r < 0 or next_r >= ROWS or \
           next_c < 0 or next_c >= COLS or \
           GRID[next_r][next_c] == 'X':
            
            s_prime = (r, c) # Se queda en el mismo lugar
        else:
            s_prime = (next_r, next_c) # Estado destino
        
        # Sumar P(s'|s,a) * V_k(s')
        action_value += prob * V_k[s_prime]
        
    return action_value

def print_values(V):
    """Imprime la cuadrícula de valores de forma bonita."""
    for r in range(ROWS):
        row_str = ""
        for c in range(COLS):
            val = GRID[r][c]
            if val == 'X':
                row_str += "  WALL  "
            else:
                row_str += f" {V[(r, c)]:6.3f} "
        print(row_str)
    print("-" * 30)

def run_value_iteration(max_iterations=100, tolerance=1e-4):
    """
    Ejecuta el algoritmo principal de Iteración de Valores.
    """
    
    # 1. Inicialización: Vk(s) = 0 para todos los estados
    V_k = {}
    for r in range(ROWS):
        for c in range(COLS):
            V_k[(r, c)] = 0.0

    print("--- Iteración 0 (Valores Iniciales) ---")
    print_values(V_k)
    
    # 2. Bucle de Iteración
    for k in range(max_iterations):
        V_kplus1 = {} # Nuevo conjunto de valores
        max_delta = 0 # Para comprobar la convergencia
        
        # 3. Aplicar la Ecuación de Bellman a cada estado
        for r in range(ROWS):
            for c in range(COLS):
                s = (r, c)
                state_char = GRID[r][c]
                
                # Si es un muro, su valor es 0
                if state_char == 'X':
                    V_kplus1[s] = 0.0
                    continue
                
                # Si es un estado terminal (Meta o Pozo), su valor
                # es solo su recompensa (no hay futuro)
                if state_char == 'G' or state_char == 'P':
                    V_kplus1[s] = REWARDS[state_char]
                    continue
                
                # --- Ecuación de Bellman para estados normales ---
                
                # R(s)
                reward = REWARDS[state_char]
                
                # max_a [ Suma[ T * Vk ] ]
                max_action_value = -float('inf')
                for a in ACTIONS:
                    val = get_action_value(s, a, V_k)
                    if val > max_action_value:
                        max_action_value = val
                        
                # V_k+1(s) = R(s) + gamma * max_a [...]
                V_kplus1[s] = reward + (GAMMA * max_action_value)
                
                # Comprobar convergencia
                delta = abs(V_kplus1[s] - V_k[s])
                if delta > max_delta:
                    max_delta = delta

        # Actualizar V_k para la siguiente iteración
        V_k = V_kplus1
        
        if k % 5 == 0 or max_delta < tolerance:
            print(f"--- Iteración {k+1} (Delta={max_delta:.5f}) ---")
            print_values(V_k)
            
        # 4. Condición de Parada
        if max_delta < tolerance:
            print(f"Convergencia alcanzada en la iteración {k+1}.")
            break
            
    return V_k

# --- 3. Ejecutar el Algoritmo ---
valores_finales = run_value_iteration()