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

# El agente NO conoce estas recompensas (excepto al aterrizar)
HIDDEN_REWARDS = {'G': 1.0, 'P': -1.0, '_': -0.04, 'X': 0}
# El agente NO conoce este modelo de transición
HIDDEN_TRANSITION_MODEL = {'main': 0.8, 'left': 0.1, 'right': 0.1}
ACTIONS = ['N', 'E', 'S', 'W']
GAMMA = 0.9

# --- 2. La "Política Fija" ($\pi$) del Agente Pasivo ---
# (Un plan simple: "Intenta ir al Este, y si no puedes, ve al Norte")
FIXED_POLICY = {
    (0,0): 'E', (0,1): 'E', (0,2): 'E', # Fila 1
    (1,0): 'E', (1,2): 'E',             # Fila 2
    (2,0): 'E', (2,1): 'E', (2,2): 'N', (2,3): 'N'
    # Los estados terminales (G, P) y Muros (X) no necesitan política
}

# --- 3. El "Simulador del Mundo" ---
# Esto es lo único con lo que el agente puede interactuar.
def simulate_step(s, a):
    """
    El agente da (s, a) y el mundo (simulador) le devuelve (s', r).
    El agente NO PUEDE ver la lógica interna de esta función.
    """
    r_s, c_s = s
    
    # Simular la transición ruidosa
    rand_val = random.random()
    if a == 'N': moves = {'main': (r_s-1, c_s), 'left': (r_s, c_s-1), 'right': (r_s, c_s+1)}
    elif a == 'S': moves = {'main': (r_s+1, c_s), 'left': (r_s, c_s+1), 'right': (r_s, c_s-1)}
    elif a == 'E': moves = {'main': (r_s, c_s+1), 'left': (r_s-1, c_s), 'right': (r_s+1, c_s)}
    elif a == 'W': moves = {'main': (r_s, c_s-1), 'left': (r_s+1, c_s), 'right': (r_s-1, c_s)}

    if rand_val < HIDDEN_TRANSITION_MODEL['main']:
        (next_r, next_c) = moves['main']
    elif rand_val < (HIDDEN_TRANSITION_MODEL['main'] + HIDDEN_TRANSITION_MODEL['left']):
        (next_r, next_c) = moves['left']
    else:
        (next_r, next_c) = moves['right']
        
    # Comprobar límites y muros
    if next_r < 0 or next_r >= ROWS or \
       next_c < 0 or next_c >= COLS or \
       GRID[next_r][next_c] == 'X':
        s_prime = (r_s, c_s) # Choca y se queda en el lugar
    else:
        s_prime = (next_r, next_c)
        
    # Obtener la recompensa del nuevo estado
    reward = HIDDEN_REWARDS[GRID[s_prime[0]][s_prime[1]]]
    
    return s_prime, reward

# --- 4. El "Algoritmo" del Agente (TD Learning) ---

def run_passive_td_learning(policy, episodes=10000, alpha=0.1):
    
    # 1. Inicialización: V(s) = 0 para todos
    V = {}
    for r in range(ROWS):
        for c in range(COLS):
            V[(r, c)] = 0.0

    print("Iniciando aprendizaje TD Pasivo...")
    
    # 2. Bucle de "Episodios" (correr la prueba muchas veces)
    for i in range(episodes):
        
        # Empezar en un estado aleatorio no-terminal
        while True:
            s = (random.randint(0, ROWS-1), random.randint(0, COLS-1))
            if GRID[s[0]][s[1]] == '_':
                break
        
        # 3. Ejecutar un episodio (seguir la política hasta el final)
        while GRID[s[0]][s[1]] == '_':
            
            # 4. Obtener la acción de la POLÍTICA FIJA
            a = policy[s]
            
            # 5. Obtener (s', r) del mundo (¡la experiencia!)
            s_prime, r = simulate_step(s, a)
            
            # 6. ¡LA CLAVE! Calcular el "Error TD"
            # error = (premio_real + premio_futuro_estimado) - (premio_antiguo_estimado)
            td_target = r + GAMMA * V[s_prime]
            td_error = td_target - V[s]
            
            # 7. Actualizar el Valor (aprender)
            V[s] = V[s] + alpha * td_error
            
            # 8. Moverse al siguiente estado
            s = s_prime
            
        if (i+1) % 2000 == 0:
            print(f"  Episodios completados: {i+1}/{episodes}")

    print("¡Aprendizaje finalizado!")
    return V

# --- 5. Ejecutar y Mostrar Resultados ---
V_aprendidos = run_passive_td_learning(FIXED_POLICY)

print("\n--- Valores V(s) Aprendidos por el Agente Pasivo ---")
for r in range(ROWS):
    row_str = ""
    for c in range(COLS):
        val_char = GRID[r][c]
        if val_char == 'X':
            row_str += "  WALL  "
        elif val_char == 'G':
            row_str += f" {HIDDEN_REWARDS['G']:6.3f} "
        elif val_char == 'P':
            row_str += f" {HIDDEN_REWARDS['P']:6.3f} "
        else:
            row_str += f" {V_aprendidos[(r, c)]:6.3f} "
    print(row_str)