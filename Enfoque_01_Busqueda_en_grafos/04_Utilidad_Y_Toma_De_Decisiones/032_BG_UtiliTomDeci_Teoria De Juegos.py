# --- 1. Definir el Juego (Dilema del Prisionero) ---
# Matriz de pagos: { (pago_jugador1, pago_jugador2) }

payoff_matrix = {
    # Jugador 1: 'Callar'
    'Callar': {
        # Jugador 2: 'Callar'
        'Callar': (5, 5),
        # Jugador 2: 'Confesar'
        'Confesar': (0, 10) 
    },
    # Jugador 1: 'Confesar'
    'Confesar': {
        # Jugador 2: 'Callar'
        'Callar': (10, 0),
        # Jugador 2: 'Confesar'
        'Confesar': (1, 1)
    }
}

actions_p1 = ['Callar', 'Confesar']
actions_p2 = ['Callar', 'Confesar']

# --- 2. El "Algoritmo": Encontrar Equilibrios de Nash ---

def find_nash_equilibrium(matrix, actions1, actions2):
    
    print("Buscando Equilibrios de Nash...")
    equilibriums = []

    # Iterar sobre CADA celda de la matriz
    for a1 in actions1:
        for a2 in actions2:
            
            # Obtener el pago de esta celda (nuestra estrategia actual)
            (payoff1, payoff2) = matrix[a1][a2]
            
            # Asumir que es un equilibrio hasta que se demuestre lo contrario
            is_nash = True
            
            # --- Comprobar si el Jugador 1 puede mejorar *unilateralmente* ---
            # (Manteniendo 'a2' fijo)
            for other_a1 in actions1:
                if other_a1 == a1:
                    continue
                
                (new_payoff1, _) = matrix[other_a1][a2]
                if new_payoff1 > payoff1:
                    is_nash = False # ¡P1 puede mejorar!
                    break
            
            if not is_nash:
                continue # Esta celda no es, pasar a la siguiente

            # --- Comprobar si el Jugador 2 puede mejorar *unilateralmente* ---
            # (Manteniendo 'a1' fijo)
            for other_a2 in actions2:
                if other_a2 == a2:
                    continue
                    
                (_, new_payoff2) = matrix[a1][other_a2]
                if new_payoff2 > payoff2:
                    is_nash = False # ¡P2 puede mejorar!
                    break
            
            # Si NINGUNO pudo mejorar, es un Equilibrio de Nash
            if is_nash:
                equilibriums.append((a1, a2))
                
    return equilibriums

# --- 3. Ejecutar ---
equilibrios = find_nash_equilibrium(payoff_matrix, actions_p1, actions_p2)

print(f"\nMatriz de Pagos:")
print(f"       Callar      Confesar")
print(f"Callar: {payoff_matrix['Callar']['Callar']}    {payoff_matrix['Callar']['Confesar']}")
print(f"Confesar: {payoff_matrix['Confesar']['Callar']}   {payoff_matrix['Confesar']['Confesar']}")

if equilibrios:
    print(f"\nEquilibrio(s) de Nash encontrado(s): {equilibrios}")
else:
    print("\nNo se encontraron Equilibrios de Nash.")