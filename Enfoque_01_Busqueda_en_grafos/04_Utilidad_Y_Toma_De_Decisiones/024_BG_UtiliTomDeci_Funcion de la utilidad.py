import math

# --- 1. Definimos las Funciones de Utilidad (Personalidades) ---

def utilidad_cautelosa(money):
    """
    Agente AVERSO AL RIESGO.
    U(x) = sqrt(x). La felicidad "se aplana".
    Ganar 20k vs 10k le da menos felicidad extra que ganar 10k vs 0.
    """
    if money < 0: return -float('inf')
    if money == 0: return 0
    return math.sqrt(money)

def utilidad_neutral(money):
    """
    Agente NEUTRAL AL RIESGO (un robot o "Spock").
    U(x) = x. La utilidad es exactamente igual al dinero.
    Solo le importa el valor esperado.
    """
    return money

def utilidad_apostador(money):
    """
    Agente AMANTE DEL RIESGO.
    U(x) = x^2. La felicidad "se dispara" con ganancias altas.
    La emoción de la gran ganancia supera el riesgo de la pérdida.
    """
    return money**2

# --- 2. Definimos el "Algoritmo" (Fórmula de Utilidad Esperada) ---

def calculate_expected_utility(options, utility_function):
    """
    Calcula la EU de una acción (opción).
    options: es una lista de tuplas (probabilidad, resultado_monetario)
    """
    expected_utility = 0.0
    
    for probability, outcome in options:
        # Aplicamos la "personalidad" al resultado
        utility_of_outcome = utility_function(outcome)
        
        # Ponderamos por la probabilidad
        expected_utility += probability * utility_of_outcome
        
    return expected_utility

# --- 3. Definimos el Problema (Las Opciones) ---

# Opción A: 100% de probabilidad de 20,000
option_A = [(1.0, 20000.0)]

# Opción B: 50% de 50,000 y 50% de 0
option_B = [(0.5, 50000.0), (0.5, 0.0)]

# --- 4. Simulamos la Decisión para cada Agente ---

agentes = [
    ("Agente Cauteloso", utilidad_cautelosa),
    ("Agente Neutral", utilidad_neutral),
    ("Agente Apostador", utilidad_apostador)
]

print("--- Simulación de Toma de Decisiones ---\n")

for name, utility_func in agentes:
    
    print(f"** Analizando para: {name} (U = {utility_func.__name__}) **")
    
    # Calcular la utilidad de cada opción PARA ESTE AGENTE
    eu_A = calculate_expected_utility(option_A, utility_func)
    eu_B = calculate_expected_utility(option_B, utility_func)
    
    print(f"  Utilidad Esperada (Opción A - Segura): {eu_A:.2f}")
    print(f"  Utilidad Esperada (Opción B - Riesgosa): {eu_B:.2f}")
    
    if eu_A > eu_B:
        print(f"  DECISIÓN: ¡Elegir Opción A (la segura)!\n")
    else:
        print(f"  DECISIÓN: ¡Elegir Opción B (la riesgosa)!\n")