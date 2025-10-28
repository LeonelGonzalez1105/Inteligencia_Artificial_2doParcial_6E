import random
import time

# --- 1. Definir el "Mundo" (¡SECRETO para el agente!) ---
# (Misma configuración que el MDP)
GRID = [
    ['_', '_', '_', 'G'],  # Fila 0
    ['_', 'X', '_', 'P'],  # Fila 1
    ['_', '_', '_', '_']   # Fila 2
]
ROWS = len(GRID)
COLS = len(GRID[0])

HIDDEN_REWARDS = {'G': 1.0, 'P': -1.0, '_': -0.04, 'X': 0}
HIDDEN_TRANSITION_MODEL = {'main': 0.8, 'left': 0.1, 'right': 0.1}
ACTIONS = ['N', 'E', 'S', 'W']
GAMMA = 0.9
ALPHA = 0.1 # Tasa de aprendizaje
EPSILON = 0.1 # 10% de exploración

# (Simulador del mundo - idéntico al del #33)
def simulate_step(s, a):
    r_s, c_s = s
    if GRID[r_s][c_s] in ['G', 'P']: return s, 0 # Es terminal
    
    moves = {}
    if a == 'N': moves = {'main': (r_s-1, c_s), 'left': (r_s, c_s-1), 'right': (r_s, c_s+1)}
    elif a == 'S': moves = {'main': (r_s+1, c_s), 'left': (r_s, c_s+1), 'right': (r_s, c_s-1)}
    elif a == 'E': moves = {'main': (r_s, c_s+1), 'left': (r_s-1, c_s), 'right': (r_s+1, c_s)}
    elif a == 'W': moves = {'main': (r_s, c_s-1), 'left': (r_s+1, c_s), 'right': (r_s-1, c_s)}

    rand_val = random.random()
    if rand_val < HIDDEN_TRANSITION_MODEL['main']: (next_r, next_c) = moves['main']
    elif rand_val < (HIDDEN_TRANSITION_MODEL['main'] + HIDDEN_TRANSITION_MODEL['left']): (next_r, next_c) = moves['left']
    else: (next_r, next_c) = moves['right']
        
    if next_r < 0 or next_r >= ROWS or \
       next_c < 0 or next_c >= COLS or \
       GRID[next_r][next_c] == 'X':
        s_prime = (r_s, c_s)
    else: s_prime = (next_r, next_c)
    reward = HIDDEN_REWARDS[GRID[s_prime[0]][s_prime[1]]]
    return s_prime, reward

# --- 2. El "Algoritmo" del Agente (Q-Learning) ---

def choose_action(s, Q_table, epsilon):
    """Elige una acción usando Epsilon-Greedy."""
    if random.random() < epsilon:
        # Exploración (acción aleatoria)
        return random.choice(ACTIONS)
    else:
        # Explotación (mejor acción conocida)
        return max(Q_table[s], key=Q_table[s].get)

def get_max_q_value(s_prime, Q_table):
    """Obtiene el max_a' Q(s', a') para el siguiente estado."""
    if GRID[s_prime[0]][s_prime[1]] in ['G', 'P']:
        return 0 # Estados terminales no tienen valor futuro
        
    return max(Q_table[s_prime].values())

def run_q_learning(episodes=20000):
    
    # 1. Inicialización: Q(s, a) = 0 para todos
    Q_table = {}
    for r in range(ROWS):
        for c in range(COLS):
            Q_table[(r, c)] = {a: 0.0 for a in ACTIONS}

    print("Iniciando Q-Learning (Agente Activo)...")
    
    # 2. Bucle de "Episodios"
    for i in range(episodes):
        
        # Empezar en un estado aleatorio no-terminal
        while True:
            s = (random.randint(0, ROWS-1), random.randint(0, COLS-1))
            if GRID[s[0]][s[1]] == '_':
                break
        
        # 3. Ejecutar un episodio
        while GRID[s[0]][s[1]] == '_':
            
            # 4. Elegir acción (Activo: Epsilon-Greedy)
            a = choose_action(s, Q_table, EPSILON)
            
            # 5. Obtener (s', r) del mundo
            s_prime, r = simulate_step(s, a)
            
            # 6. ¡LA ACTUALIZACIÓN Q-LEARNING!
            # Q(s,a) <-- Q(s,a) + alpha * [r + gamma * max_a'(Q(s',a')) - Q(s,a)]
            
            # TD Target = r + gamma * max_a'(Q(s',a'))
            td_target = r + GAMMA * get_max_q_value(s_prime, Q_table)
            
            # Error = td_target - Q(s,a)
            td_error = td_target - Q_table[s][a]
            
            # 7. Aprender
            Q_table[s][a] = Q_table[s][a] + ALPHA * td_error
            
            # 8. Moverse
            s = s_prime
            
        if (i+1) % 5000 == 0:
            print(f"  Episodios completados: {i+1}/{episodes}")

    print("¡Aprendizaje finalizado!")
    return Q_table

# --- 3. Ejecutar y Extraer Política ---
Q_table_final = run_q_learning()

print("\n--- Política Óptima (Plan) Aprendida ---")
policy = {}
for r in range(ROWS):
    row_str = ""
    for c in range(COLS):
        s = (r, c)
        val_char = GRID[r][c]
        if val_char == 'X':
            row_str += "  WALL  "
        elif val_char in ['G', 'P']:
            row_str += f"  {val_char}     "
        else:
            # Extraer la mejor acción de la Q-Table
            best_action = max(Q_table_final[s], key=Q_table_final[s].get) # <-- ¡CORREGIDO!
            policy[s] = best_action
            row_str += f"  {best_action:^5}  "
    print(row_str)