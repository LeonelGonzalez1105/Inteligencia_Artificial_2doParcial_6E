import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

# --- 1. Definir el Modelo ---

# Parámetros de nuestra creencia a priori P(theta)
# Beta(a, b). a=1, b=1 es un "previo uniforme" (no sabemos nada).
# a = "caras imaginarias" + 1
# b = "cruces imaginarias" + 1
a_prior = 1.0
b_prior = 1.0

# Simulación de nuestros datos (los lanzamientos que observamos)
datos = ['Cara', 'Cara', 'Cruz', 'Cara', 'Cara', 
         'Cara', 'Cruz', 'Cara', 'Cara', 'Cara'] # 8 Caras, 2 Cruces

# --- 2. El "Algoritmo": Actualización Bayesiana Iterativa ---

def bayesian_learning_update(data_sequence, a_prior, b_prior):
    """
    Actualiza la creencia (distribución Beta) iterativamente.
    """
    
    a = a_prior
    b = b_prior
    
    print("--- Ejecutando Aprendizaje Bayesiano (Modelo Beta-Binomial) ---")
    print(f"Creencia Inicial: Beta(a={a}, b={b}) (Uniforme)")
    
    # Preparar el gráfico
    plt.figure(figsize=(12, 8))
    x = np.linspace(0, 1, 100) # Eje X (posibles valores de theta)
    
    # Graficar el Prior
    plt.plot(x, beta.pdf(x, a, b), 'k--', label=f'Prior: Beta({a}, {b})')
    
    # Contadores para la actualización
    H = 0
    T = 0
    
    # 3. Iterar sobre los datos
    for i, data_point in enumerate(data_sequence):
        
        # Actualizar contadores
        if data_point == 'Cara':
            H += 1
        else:
            T += 1
            
        # 4. Calcular el Posterior (la "magia" del modelo conjugado)
        # Posterior P(theta | D) = Beta(a + H, b + T)
        a_posterior = a_prior + H
        b_posterior = b_prior + T
        
        # Graficar la creencia actualizada (solo algunas para no saturar)
        if (i+1) % 2 == 0 or i == len(data_sequence) - 1:
            label_str = f'Posterior (Tras {H}H, {T}T): Beta({a_posterior}, {b_posterior})'
            plt.plot(x, beta.pdf(x, a_posterior, b_posterior), 
                     label=label_str, alpha=0.7 + 0.3 * (i/len(data_sequence)))
            
    print(f"\nCreencia Final (Posterior): Beta(a={a_posterior}, b={b_posterior})")
    
    # Mostrar el gráfico
    plt.title('Aprendizaje Bayesiano: Actualización de Creencias sobre el Sesgo de una Moneda')
    plt.xlabel('Valor de $\\theta$ (Probabilidad de "Cara")')
    plt.ylabel('Densidad de Probabilidad (Nuestra Creencia)')
    plt.legend()
    plt.grid(True)
    plt.show()

# --- 3. Ejecutar ---
bayesian_learning_update(datos, a_prior, b_prior)