import random

# --- Parámetros del Algoritmo Genético ---
TARGET_PHRASE = "HOLA"
VALID_GENES = " ABCDEFGHIJKLMNOPQRSTUVWXYZ" # El "alfabeto" que podemos usar
POPULATION_SIZE = 100
MUTATION_RATE = 0.05 # 5% de probabilidad de mutar

# 1. Funciones de ayuda
def create_random_individual():
    """Crea un 'ADN' aleatorio."""
    return [random.choice(VALID_GENES) for _ in range(len(TARGET_PHRASE))]

def calculate_fitness(individual):
    """
    Función de Aptitud (Fitness).
    Cuenta cuántas letras coinciden con el objetivo.
    """
    fitness = 0
    for i in range(len(TARGET_PHRASE)):
        if individual[i] == TARGET_PHRASE[i]:
            fitness += 1
    return fitness

# 2. Funciones de Reproducción
def crossover(parent1, parent2):
    """
    Mezcla el ADN de dos padres (Cruce de un solo punto).
    """
    child = []
    # Elegir un punto al azar para "cortar" el ADN
    split_point = random.randint(0, len(TARGET_PHRASE) - 1)
    
    # Primera parte del Padre 1
    child.extend(parent1[:split_point])
    # Segunda parte del Padre 2
    child.extend(parent2[split_point:])
    
    return child

def mutate(individual):
    """
    Muta el ADN con una pequeña probabilidad.
    """
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            # Reemplazar el gen por uno nuevo aleatorio
            individual[i] = random.choice(VALID_GENES)
    return individual

# 3. Función de Selección (Torneo)
def selection(population_with_fitness):
    """
    Selecciona a un padre usando "Selección por Torneo".
    Toma 2 al azar y elige al mejor de los 2.
    """
    tournament_size = 2
    # Tomamos 2 competidores al azar de la población
    competitors = random.sample(population_with_fitness, tournament_size)
    
    # Los ordenamos por fitness (el segundo elemento de la tupla)
    competitors.sort(key=lambda item: item[1], reverse=True)
    
    # Devolvemos al ganador (el 'ADN', que es el primer elemento)
    return competitors[0][0] 

# --- El Algoritmo Principal ---
def run_genetic_algorithm():
    
    # 1. Inicialización: Crear la población inicial
    population = [create_random_individual() for _ in range(POPULATION_SIZE)]
    
    generation = 0
    
    while True:
        generation += 1
        
        # 2. Evaluación (Fitness)
        pop_with_fitness = []
        for individual in population:
            fitness = calculate_fitness(individual)
            pop_with_fitness.append((individual, fitness))
            
        # 3. Comprobar si ganamos
        # Ordenamos la población para encontrar al mejor
        pop_with_fitness.sort(key=lambda item: item[1], reverse=True)
        best_individual, best_fitness = pop_with_fitness[0]
        
        print(f"Generación {generation}: Mejor Individuo={''.join(best_individual)} "
              f"Fitness={best_fitness}/{len(TARGET_PHRASE)}")

        if best_fitness == len(TARGET_PHRASE):
            print(f"\n¡Solución encontrada en {generation} generaciones!")
            break
            
        # 4. Crear la nueva generación (Selección y Reproducción)
        new_population = []
        
        # (Guardamos al mejor 10% - Elitismo)
        elitism_count = int(POPULATION_SIZE * 0.1)
        new_population.extend([ind for ind, fit in pop_with_fitness[:elitism_count]])

        # Llenamos el resto de la población con hijos
        while len(new_population) < POPULATION_SIZE:
            # 5. Selección
            parent1 = selection(pop_with_fitness)
            parent2 = selection(pop_with_fitness)
            
            # 6. Cruce (Crossover)
            child = crossover(parent1, parent2)
            
            # 7. Mutación
            child = mutate(child)
            
            new_population.append(child)
            
        # 8. Reemplazo
        population = new_population

# --- Ejecutamos el algoritmo ---
run_genetic_algorithm()