import random
import copy

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
# (Simulador del mundo - idéntico al del #35)
def simulate_step(s, a):
    r_s, c_s = s
    if GRID[r_s][c_s] in ['G', 'P']: return s, 0
    moves = {}
    if a == 'N': moves = {'main': (r_s-1, c_s), 'left': (r_s, c_s-1), 'right': (r_s, c_s+1)}
    elif a == 'S': moves = {'main': (r_s+1, c_s), 'left': (r_s, c_s+1), 'right': (r_s, c_s-1)}
    elif a == 'E': moves = {'main': (r_s, c_s+1), 'left': (r_s-1, c_s), 'right': (r_s+1, c_s)}
    elif a == 'W': moves = {'main': (r_s, c_s-1), 'left': (r_s+1, c_s), 'right': (r_s-1, c_s)}
    rand_val = random.random()
    if rand_val < 0.8: (next_r, next_c) = moves['main']
    elif rand_val < 0.9: (next_r, next_c) = moves['left']
    else: (next_r, next_c) = moves['right']
    if next_r < 0 or next_r >= ROWS or next_c < 0 or next_c >= COLS or GRID[next_r][next_c] == 'X':
        s_prime = (r_s, c_s)
    else: s_prime = (next_r, next_c)
    reward = HIDDEN_REWARDS[GRID[s_prime[0]][s_prime[1]]]
    return s_prime, reward
ACTIONS = ['N', 'E', 'S', 'W']
GAMMA = 0.9

# --- 2. El "Algoritmo": Búsqueda de Política ---

def initialize_policy():
    """Crea una política aleatoria P(a|s) = 0.25 para todo."""
    policy = {}
    for r in range(ROWS):
        for c in range(COLS):
            if GRID[r][c] == '_':
                policy[(r, c)] = {'N': 0.25, 'E': 0.25, 'S': 0.25, 'W': 0.25}
    return policy

def choose_action_from_policy(s, policy):
    """Elige una acción basada en las probabilidades de la política."""
    actions = list(policy[s].keys())
    probabilities = list(policy[s].values())
    return random.choices(actions, weights=probabilities, k=1)[0]

def evaluate_policy(policy, num_episodes=50, max_steps=100):
    """Calcula la recompensa total promedio de una política."""
    total_reward = 0
    for _ in range(num_episodes):
        s = (2, 0) # Empezar siempre desde (2,0)
        episode_reward = 0
        discount = 1.0
        for _ in range(max_steps):
            if GRID[s[0]][s[1]] != '_':
                break
            a = choose_action_from_policy(s, policy)
            s_prime, r = simulate_step(s, a)
            episode_reward += r * discount
            discount *= GAMMA
            s = s_prime
        total_reward += episode_reward
    return total_reward / num_episodes

def mutate_policy(policy):
    """"Muta" la política un poquito."""
    new_policy = copy.deepcopy(policy)
    # Elegir un estado al azar para mutar
    s_to_mutate = random.choice(list(new_policy.keys()))
    
    # Elegir dos acciones al azar para "intercambiar" probabilidad
    a1, a2 = random.sample(ACTIONS, 2)
    
    # Mover un poquito de prob de a1 a a2
    amount = 0.1 # "Tasa de mutación"
    if new_policy[s_to_mutate][a1] >= amount:
        new_policy[s_to_mutate][a1] -= amount
        new_policy[s_to_mutate][a2] += amount
        
    return new_policy

def run_policy_search(search_iterations=1000):
    
    # 1. Empezar con una política aleatoria
    current_policy = initialize_policy()
    current_best_reward = evaluate_policy(current_policy)
    
    print("Iniciando Búsqueda de Política...")
    print(f"Iter 0: Mejor Recompensa = {current_best_reward:.3f}")
    
    # 2. Bucle de "Hill Climbing"
    for i in range(search_iterations):
        # 3. Crear una "mutación"
        new_policy = mutate_policy(current_policy)
        
        # 4. Evaluar la mutación
        new_reward = evaluate_policy(new_policy)
        
        # 5. Si es mejor, nos la quedamos
        if new_reward > current_best_reward:
            current_best_reward = new_reward
            current_policy = new_policy
            if i % 100 == 0:
                print(f"  Iter {i}: ¡Mejora! Nueva Recompensa = {current_best_reward:.3f}")

    print("Búsqueda finalizada.")
    return current_policy

# --- 3. Ejecutar y Extraer Política ---
final_policy_probs = run_policy_search()

print("\n--- Política Óptima (Plan) Aprendida ---")
for r in range(ROWS):
    row_str = ""
    for c in range(COLS):
        s = (r, c)
        val_char = GRID[r][c]
        if val_char == 'X': row_str += "  WALL  "
        elif val_char in ['G', 'P']: row_str += f"  {val_char}     "
        else:
            # Extraer la mejor acción (la más probable) de la política
            best_action = max(final_policy_probs[s], key=final_policy_probs[s].get)
            row_str += f"  {best_action:^5}  "
    print(row_str)