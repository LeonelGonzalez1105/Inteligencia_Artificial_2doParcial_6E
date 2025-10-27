import random
import time

def objective_function(x):
    """
    Nuestra "montaña" con dos cimas:
    - Máximo Local: x=5, altura=50
    - Máximo Global: x=20, altura=100
    """
    # Rango extendido para que no dé error si se sale
    if x < -10 or x > 30: 
        return -float('inf')
    if x < 10:
        return -(x - 5)**2 + 50
    else:
        return -(x - 20)**2 + 100

def get_neighbors(current_x, step_size):
    """Genera los vecinos: un paso a la izquierda y uno a la derecha."""
    return [current_x - step_size, current_x + step_size]

def local_beam_search(k, step_size, search_range, max_iterations=100):
    """
    Implementa la Búsqueda de Haz Local (Local Beam Search).
    
    Args:
        k (int): El "ancho del haz", es decir, el número de 
                 estados que mantenemos.
        step_size (float): Cuánto nos movemos a la izquierda/derecha.
        search_range (tuple): Rango (min_x, max_x) para generar estados iniciales.
    """
    
    # 1. Generar k estados iniciales aleatorios
    current_states = [random.uniform(search_range[0], search_range[1]) 
                      for _ in range(k)]
    # Evaluar los estados iniciales
    current_states_with_values = [(x, objective_function(x)) 
                                  for x in current_states]
    
    # Guardamos el mejor global
    global_best_x, global_best_value = max(current_states_with_values, 
                                           key=lambda item: item[1])

    print(f"Iniciando Búsqueda de Haz Local con k={k}")
    
    for i in range(max_iterations):
        print(f"\n--- Iteración {i} ---")
        print(f"  Haz actual (x, valor): "
              f"{[(x, round(v, 2)) for x, v in current_states_with_values]}")
        
        all_neighbors = []
        
        # 2. Generar TODOS los vecinos de TODOS los estados en el haz
        for x, value in current_states_with_values:
            for neighbor_x in get_neighbors(x, step_size):
                all_neighbors.append((neighbor_x, objective_function(neighbor_x)))
        
        # 3. Quitar duplicados (opcional pero bueno)
        # Usamos un dict para quedarnos con el mejor valor para una x duplicada
        unique_neighbors = {x: v for x, v in all_neighbors}
        sorted_neighbors = sorted(unique_neighbors.items(), 
                                  key=lambda item: item[1], 
                                  reverse=True) # Ordenar de MEJOR a PEOR
        
        # 4. Seleccionar los k MEJORES vecinos
        next_states_with_values = sorted_neighbors[:k]
        
        # 5. Comprobar si hemos mejorado
        best_new_x, best_new_value = next_states_with_values[0]
        
        if best_new_value > global_best_value:
            global_best_x = best_new_x
            global_best_value = best_new_value
            print(f"  *** ¡Nuevo MÁXIMO GLOBAL encontrado! "
                  f"x={global_best_x:.2f}, Valor={global_best_value:.2f} ***")
        elif best_new_value <= current_states_with_values[0][1]:
            # Si el mejor de los NUEVOS no es mejor que el mejor de los VIEJOS,
            # podríamos estar en una cima.
            print(f"\nBúsqueda estancada. Cima encontrada.")
            break

        # 6. El nuevo haz reemplaza al viejo
        current_states_with_values = next_states_with_values
        
        time.sleep(0.5)

    print(f"\nBúsqueda de Haz Local finalizada.")
    print(f"Mejor solución global encontrada: x={global_best_x:.2f}, "
          f"Valor={global_best_value:.2f}")
    return (global_best_x, global_best_value)

# --- PRUEBA: Empezando con k=3 estados aleatorios ---
# Le damos un rango de 0 a 10, para forzar que algunos
# empiecen en la colina "mala" (la local)
print("--- PRUEBA HAZ LOCAL: k=3, Empezando entre x=0 y x=10 ---")
local_beam_search(k=3, step_size=1, search_range=(0, 10))