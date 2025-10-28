import random
import time

# --- 1. Definir el "Mundo" (Las máquinas tragamonedas) ---
# (El agente NO conoce estas probabilidades)
PAYOFFS = {'A': 2, 'B': 5, 'C': 1}
PROBS   = {'A': 1.0, 'B': 0.3, 'C': 0.8}
MACHINES = ['A', 'B', 'C']
TOTAL_TRIES = 100

def pull_lever(machine_name):
    """Simula tirar de la palanca de una máquina."""
    if random.random() < PROBS[machine_name]:
        return PAYOFFS[machine_name]
    return 0

# --- 2. Algoritmo "Activo" (con balance Epsilon-Greedy) ---

def run_active_agent(epsilon):
    """
    Simula un agente que explora con probabilidad 'epsilon'.
    Si epsilon=0, es un agente de "Solo Explotación".
    """
    
    # El "cerebro" del agente: guarda el valor promedio aprendido
    Q_values = {'A': 0.0, 'B': 0.0, 'C': 0.0}
    # Contador de cuántas veces ha probado cada una
    counts = {'A': 0, 'B': 0, 'C': 0}
    
    total_reward = 0.0
    
    print(f"\n--- Agente con Epsilon = {epsilon} ---")
    if epsilon == 0:
        print("(Modo: Solo Explotación)")
    else:
        print(f"(Modo: {100-epsilon*100}% Explotación, {epsilon*100}% Exploración)")

    for i in range(TOTAL_TRIES):
        
        # --- LA DECISIÓN: ¿Explorar o Explotar? ---
        if random.random() < epsilon:
            # 1. EXPLORACIÓN (Elegir al azar)
            action = random.choice(MACHINES)
        else:
            # 2. EXPLOTACIÓN (Elegir la mejor *conocida*)
            # (Encuentra la 'key' con el 'value' más alto en Q_values)
            action = max(Q_values, key=Q_values.get)

        # 3. Actuar en el mundo y obtener recompensa
        reward = pull_lever(action)
        total_reward += reward
        
        # 4. Aprender de la experiencia (Actualizar Q-values)
        # (Esto es un simple promedio)
        counts[action] += 1
        Q_values[action] = ((Q_values[action] * (counts[action]-1)) + reward) / counts[action]

    print(f"  Ganancia Total: {total_reward:.2f}")
    print(f"  Valores aprendidos (Q):")
    for m in MACHINES:
        print(f"    {m}: {Q_values[m]:.2f} (Valor Real: {PROBS[m]*PAYOFFS[m]:.2f}) "
              f"probada {counts[m]} veces")
    return total_reward

# --- 3. Ejecutar Simulación ---
# (Semilla para que los resultados sean parecidos, pero no idénticos)
random.seed(42)

# Agente 1: Cero exploración (muy codicioso)
# NOTA: Le damos 1 "prueba" inicial a cada una para que no se atore en 0.
run_active_agent(epsilon=0.0)

# Agente 2: 10% de exploración
run_active_agent(epsilon=0.1)

# Agente 3: 30% de exploración (más caótico)
run_active_agent(epsilon=0.3)