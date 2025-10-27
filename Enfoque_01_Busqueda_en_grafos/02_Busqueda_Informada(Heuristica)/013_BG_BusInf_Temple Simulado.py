import random
import math
import time

def objective_function(x):
    """
    Nuestra "montaña" con dos cimas:
    - Máximo Local: x=5, altura=50
    - Máximo Global: x=20, altura=100
    """
    if x < 10:
        return -(x - 5)**2 + 50
    else:
        return -(x - 20)**2 + 100

def get_random_neighbor(current_x, step_size):
    """
    Genera UN vecino ALEATORIO.
    A diferencia de Hill Climbing, no los prueba todos, solo uno.
    """
    if random.random() > 0.5:
        return current_x + step_size
    else:
        return current_x - step_size

def simulated_annealing(start_x, step_size, 
                        initial_temp, cooling_rate, final_temp):
    """
    Implementa la Búsqueda de Temple Simulado.
    """
    
    T = initial_temp
    current_x = start_x
    current_value = objective_function(current_x)
    
    # Guardamos la MEJOR solución encontrada HASTA AHORA
    global_best_x = current_x
    global_best_value = current_value
    
    print(f"Iniciando Temple Simulado en x={current_x} (Valor: {current_value:.2f})")
    print(f"Temperatura inicial: {T:.2f}, Enfriamiento: {cooling_rate}\n")
    
    iter_count = 0
    
    # 1. El bucle se ejecuta mientras estemos "calientes"
    while T > final_temp:
        iter_count += 1
        
        # 2. Elegir UN vecino al azar
        neighbor_x = get_random_neighbor(current_x, step_size)
        
        # (Control simple de límites para que no se vaya al infinito)
        if not (-10 < neighbor_x < 30):
            continue
            
        neighbor_value = objective_function(neighbor_x)
        
        # 3. Calcular la diferencia de "calidad" o "energía"
        delta_value = neighbor_value - current_value
        
        # 4. Decidir si nos movemos
        if delta_value > 0:
            # ¡Es un movimiento MEJOR! Siempre lo aceptamos.
            current_x = neighbor_x
            current_value = neighbor_value
            print(f"  Iter {iter_count} (T={T:.2f}): Movimiento MEJOR a x={current_x:.1f} "
                  f"(Valor: {current_value:.2f})")
        else:
            # Es un movimiento PEOR. Decidimos con probabilidad.
            
            # 5. Calcular la probabilidad de aceptación
            # e^(delta / T)
            accept_prob = math.exp(delta_value / T)
            
            # 6. Lanzar la moneda
            if random.random() < accept_prob:
                # ¡Aceptamos el mal movimiento!
                current_x = neighbor_x
                current_value = neighbor_value
                print(f"  Iter {iter_count} (T={T:.2f}): *** Aceptando movimiento PEOR a "
                      f"x={current_x:.1f} (Valor: {current_value:.2f}) "
                      f"con Prob={accept_prob:.3f} ***")
            else:
                # Rechazamos el mal movimiento
                pass # Nos quedamos donde estábamos

        # 7. Actualizar la mejor solución global (como en Búsqueda Tabú)
        if current_value > global_best_value:
            global_best_x = current_x
            global_best_value = current_value
            print(f"      ¡Nuevo MÁXIMO GLOBAL encontrado! "
                  f"x={global_best_x:.1f}, Valor={global_best_value:.2f}")
            
        # 8. ¡Enfriar la temperatura!
        T = T * cooling_rate
        
        if iter_count % 10 == 0:
            time.sleep(0.1)

    print(f"\nTemple Simulado finalizado (Temperatura < {final_temp}).")
    print(f"Mejor solución global encontrada: x={global_best_x:.1f}, "
          f"Valor={global_best_value:.2f}")
    return (global_best_x, global_best_value)

# --- PRUEBA: Empezando en x=0 (donde Hill Climbing se atoró) ---
# Le damos una temperatura inicial alta (100)
# y un enfriamiento lento (0.95)
print("--- PRUEBA TEMPLE SIMULADO: Empezando en x=0 ---")
simulated_annealing(start_x=0, 
                    step_size=1, 
                    initial_temp=100.0, 
                    cooling_rate=0.95, 
                    final_temp=0.1)