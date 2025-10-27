import collections
import time

def objective_function(x):
    """
    Nuestra "montaña" con dos cimas.
    - Máximo Local: x=5, altura=50
    - Máximo Global: x=20, altura=100
    """
    if x < 10:
        return -(x - 5)**2 + 50  
    else:
        return -(x - 20)**2 + 100 

def get_neighbors(current_x, step_size):
    """Genera vecinos a izquierda y derecha."""
    return [current_x - step_size, current_x + step_size]

def tabu_search(start_x, step_size, tabu_tenure, max_iterations):
    """
    Implementa la Búsqueda Tabú.

    Args:
        start_x (float): El punto de inicio.
        step_size (float): Cuánto nos movemos (ej. 1.0).
        tabu_tenure (int): Cuántas iteraciones un estado permanece "tabú".
        max_iterations (int): Cuántos pasos damos en total.
    """
    
    # 1. La "memoria a corto plazo" (Lista Tabú).
    # Usamos un deque (cola de doble fin) con tamaño máximo.
    # Guardará los *estados* (valores de x) que no podemos visitar.
    tabu_list = collections.deque(maxlen=tabu_tenure)
    
    # 2. Estado actual
    current_x = start_x
    current_value = objective_function(current_x)
    
    # 3. La "memoria a largo plazo" (la mejor solución global)
    best_solution_x = current_x
    best_solution_value = current_value
    
    print(f"Iniciando Búsqueda Tabú en x={current_x} (Valor: {current_value:.2f})")
    print(f"Tenencia Tabú: {tabu_tenure} iteraciones")
    print(f"Mejor Global hasta ahora: {best_solution_value:.2f}\n")
    
    for i in range(max_iterations):
        
        # 4. Encontrar a TODOS los vecinos
        neighbors = get_neighbors(current_x, step_size)
        
        # 5. Filtrar los vecinos que están en la lista tabú
        non_tabu_neighbors = []
        for neighbor_x in neighbors:
            if neighbor_x not in tabu_list:
                non_tabu_neighbors.append(neighbor_x)
        
        # 6. Si TODOS los vecinos son tabú, nos atascamos
        if not non_tabu_neighbors:
            print("  ¡Atascado! Todos los vecinos son tabú. Terminando.")
            break
            
        # 7. ¡LA CLAVE TABÚ!
        # Encontrar el "mejor" de los vecinos NO-TABÚ
        # (aunque sea PEOR que nuestra posición actual)
        best_neighbor_x = non_tabu_neighbors[0]
        best_neighbor_value = objective_function(best_neighbor_x)
        
        if len(non_tabu_neighbors) > 1:
            neighbor2_x = non_tabu_neighbors[1]
            neighbor2_value = objective_function(neighbor2_x)
            if neighbor2_value > best_neighbor_value:
                best_neighbor_x = neighbor2_x
                best_neighbor_value = neighbor2_value
        
        # 8. Movernos a ese vecino
        print(f"  Iter {i}: Posición actual x={current_x:.1f} (Valor: {current_value:.2f})")
        print(f"    -> Vecinos no-tabú: {[round(n, 1) for n in non_tabu_neighbors]}")
        print(f"    --> Moviendo a x={best_neighbor_x:.1f} (Valor: {best_neighbor_value:.2f})")
        
        current_x = best_neighbor_x
        current_value = best_neighbor_value
        
        # 9. Añadir el estado al que nos MOVIMOS a la lista tabú
        tabu_list.append(current_x)
        print(f"    -> Lista Tabú ahora: {[round(n, 1) for n in tabu_list]}")

        # 10. Actualizar la mejor solución global si es necesario
        if current_value > best_solution_value:
            best_solution_x = current_x
            best_solution_value = current_value
            print(f"    ¡¡¡NUEVO MÁXIMO GLOBAL ENCONTRADO!!! {best_solution_value:.2f}")
            
        time.sleep(0.1)

    print("\nBúsqueda Tabú terminada.")
    print(f"Mejor solución global encontrada: x={best_solution_x:.1f}, "
          f"Valor={best_solution_value:.2f}")
    return (best_solution_x, best_solution_value)

# --- PRUEBA: Empezando en el MÁXIMO LOCAL ---
print("--- PRUEBA: Empezando en x=5 (Máximo Local) ---")
# Usamos una tenencia tabú corta (2 turnos)
tabu_search(start_x=5.0, step_size=1.0, tabu_tenure=2, max_iterations=30)