import random
import time

def objective_function(x):
    """
    Esta es nuestra "montaña". Tiene dos cimas:
    - Una cima PEQUEÑA (máximo local) en x=5, altura=50
    - Una cima GRANDE (máximo global) en x=20, altura=100
    """
    if x < 10:
        # Ecuación de una parábola invertida centrada en 5
        return -(x - 5)**2 + 50  
    else:
        # Ecuación de una parábola invertida centrada en 20
        return -(x - 20)**2 + 100 

def get_neighbors(current_x, step_size):
    """
    Genera los "vecinos" (los pasos que podemos probar).
    En este caso, un paso a la izquierda y uno a la derecha.
    """
    return [current_x - step_size, current_x + step_size]

def hill_climbing(start_x, step_size, max_iterations=1000):
    """
    Implementa la Búsqueda de Ascensión de Colinas.
    """
    
    current_x = start_x
    current_value = objective_function(current_x)
    
    print(f"Iniciando Ascensión de Colinas en x={current_x} "
          f"(Valor: {current_value:.2f})")
    
    for i in range(max_iterations):
        print(f"  Iter {i}: Posición actual x={current_x:.1f}, "
              f"Valor={current_value:.2f}")
        
        # 1. Encontrar al "mejor vecino"
        best_neighbor = None
        best_neighbor_value = -float('inf') # Empezamos con el peor valor posible
        
        for neighbor_x in get_neighbors(current_x, step_size):
            neighbor_value = objective_function(neighbor_x)
            print(f"    -> Probando vecino x={neighbor_x:.1f}, "
                  f"Valor={neighbor_value:.2f}")
            
            if neighbor_value > best_neighbor_value:
                best_neighbor = neighbor_x
                best_neighbor_value = neighbor_value

        # 2. Decidir si nos movemos
        # ¡LA CLAVE! Si el mejor vecino NO es mejor que donde ya estoy...
        if best_neighbor_value <= current_value:
            # ¡Cima alcanzada! (O atorados en un máximo local)
            print(f"\n¡Cima encontrada! No hay vecinos mejores.")
            print(f"Resultado final: x={current_x:.1f}, "
                  f"Valor={current_value:.2f}")
            return (current_x, current_value)
        else:
            # 3. Movernos a la mejor posición
            print(f"  --> Moviendo a x={best_neighbor:.1f} "
                  f"(Valor: {best_neighbor_value:.2f})")
            current_x = best_neighbor
            current_value = best_neighbor_value
            
        time.sleep(0.1) # Pausa para poder leer la salida

    print(f"\nSe alcanzó el límite de iteraciones.")
    print(f"Resultado final: x={current_x:.1f}, Valor={current_value:.2f}")
    return (current_x, current_value)

# --- PRUEBA 1: Empezando cerca del MÁXIMO LOCAL ---
print("--- PRUEBA 1: Empezando en x=0 (cerca de la cima local en 5) ---")
hill_climbing(start_x=0, step_size=1)

# --- PRUEBA 2: Empezando cerca del MÁXIMO GLOBAL ---
print("\n\n--- PRUEBA 2: Empezando en x=15 (cerca de la cima global en 20) ---")
hill_climbing(start_x=15, step_size=1)