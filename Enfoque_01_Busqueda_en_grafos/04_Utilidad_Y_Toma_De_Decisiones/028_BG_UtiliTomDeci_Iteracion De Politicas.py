import time
import copy
import random

# --- 1. Definir el MDP (El Mundo) ---
# (Usamos exactamente el mismo mundo que en el #27)

GRID = [
    ['_', '_', '_', 'G'],  # Fila 0
    ['_', 'X', '_', 'P'],  # Fila 1
    ['_', '_', '_', '_']   # Fila 2
]
ROWS = len(GRID)
COLS = len(GRID[0])

REWARDS = {'G': 1.0, 'P': -1.0, '_': -0.04, 'X': 0}
ACTIONS = ['N', 'E', 'S', 'W']
TRANSITION_PROBS = {'main': 0.8, 'left': 0.1, 'right': 0.1}
GAMMA = 0.9

# (Funciones de ayuda 'get_neighbors' y 'get_action_value' 
#  son las mismas que en el #27)

def get_neighbors(s, a):
    r, c = s
    if a == 'N': moves = {'main': (r-1, c), 'left': (r, c-1), 'right': (r, c+1)}
    elif a == 'S': moves = {'main': (r+1, c), 'left': (r, c+1), 'right': (r, c-1)}
    elif a == 'E': moves = {'main': (r, c+1), 'left': (r-1, c), 'right': (r+1, c)}
    elif a == 'W': moves = {'main': (r, c-1), 'left': (r+1, c), 'right': (r-1, c)}
    return moves

def get_state_value(s, V_k):
    """Calcula el valor de un estado, dada una acción FIJA (policy[s]).
       Esta es la Ecuación de Bellman SIN el max."""
    r, c = s
    
    # 1. Obtener la acción fija del plan actual
    action = policy[s] 
    if not action: # Si no hay política (terminal), valor es 0
        return 0.0

    action_value = 0.0
    moves = get_neighbors(s, action)
    
    for move_type, (next_r, next_c) in moves.items():
        prob = TRANSITION_PROBS[move_type]
        if next_r < 0 or next_r >= ROWS or \
           next_c < 0 or next_c >= COLS or \
           GRID[next_r][next_c] == 'X':
            s_prime = (r, c)
        else:
            s_prime = (next_r, next_c)
        action_value += prob * V_k[s_prime]
        
    return action_value

# (Necesitamos 'get_action_value' del #27 para el paso de Mejora)
def get_action_q_value(s, a, V_k):
    """Calcula el valor Q(s,a) = Suma[ T * Vk(s') ]"""
    r, c = s
    action_value = 0.0
    moves = get_neighbors(s, a)
    for move_type, (next_r, next_c) in moves.items():
        prob = TRANSITION_PROBS[move_type]
        if next_r < 0 or next_r >= ROWS or \
           next_c < 0 or next_c >= COLS or \
           GRID[next_r][next_c] == 'X':
            s_prime = (r, c)
        else:
            s_prime = (next_r, next_c)
        action_value += prob * V_k[s_prime]
    return action_value

def print_policy(P):
    """Imprime la política de forma bonita."""
    for r in range(ROWS):
        row_str = ""
        for c in range(COLS):
            val = GRID[r][c]
            if val == 'X':
                row_str += "  WALL  "
            elif val == 'G' or val == 'P':
                row_str += f"  {val}     "
            else:
                row_str += f"  {P[(r, c)]:>5}  "
        print(row_str)
    print("-" * 30)

# --- 2. El Algoritmo: Iteración de Políticas ---

# Inicializar un plan (política) aleatorio
policy = {}
V = {} # Valores de la política
for r in range(ROWS):
    for c in range(COLS):
        V[(r, c)] = 0.0 # Inicializar valores a 0
        if GRID[r][c] in ['_', 'X']:
            policy[(r, c)] = random.choice(ACTIONS)
        else:
            policy[(r, c)] = None # Estados terminales no tienen acción

print("--- Política Inicial (Aleatoria) ---")
print_policy(policy)

policy_stable = False
iteration = 0

while not policy_stable:
    iteration += 1
    print(f"\n======= ITERACIÓN DE POLÍTICA #{iteration} =======")
    
    # --- PASO 1: EVALUACIÓN de la Política ---
    # (Iteramos hasta que V converja para ESTA política)
    
    print("  Paso 1: Evaluación de Política...")
    V_k = V.copy() # Usar los valores de la política anterior como inicio
    while True:
        delta = 0
        V_kplus1 = {}
        for r in range(ROWS):
            for c in range(COLS):
                s = (r, c)
                state_char = GRID[r][c]
                
                if state_char == 'X':
                    V_kplus1[s] = 0.0
                    continue
                if state_char == 'G' or state_char == 'P':
                    V_kplus1[s] = REWARDS[state_char]
                    continue
                
                # Ecuación de Bellman (sin max)
                reward = REWARDS[state_char]
                v = reward + (GAMMA * get_state_value(s, V_k))
                V_kplus1[s] = v
                
                delta = max(delta, abs(v - V_k[s]))
                
        V_k = V_kplus1
        if delta < 1e-4: # Convergencia de valores
            break
    
    V = V_k # Guardamos los valores finales de esta política
    # (Opcional: imprimir valores V aquí)
    print("    Valores V(s) para esta política calculados.")

    # --- PASO 2: MEJORA de la Política ---
    print("  Paso 2: Mejora de Política...")
    policy_stable = True # Asumir que es estable hasta que se demuestre lo contrario
    
    for r in range(ROWS):
        for c in range(COLS):
            s = (r, c)
            if GRID[r][c] not in ['_', 'X']:
                continue

            old_action = policy[s]
            
            # Encontrar la mejor acción (mirando un paso adelante)
            best_action = None
            max_q_val = -float('inf')
            
            for a in ACTIONS:
                q_val = get_action_q_value(s, a, V)
                if q_val > max_q_val:
                    max_q_val = q_val
                    best_action = a
                    
            # Actualizar la política
            policy[s] = best_action
            
            # Comprobar si la política cambió
            if old_action != best_action:
                policy_stable = False
                
    print_policy(policy)

print("\n--- Política Óptima Final Encontrada ---")
print_policy(policy)