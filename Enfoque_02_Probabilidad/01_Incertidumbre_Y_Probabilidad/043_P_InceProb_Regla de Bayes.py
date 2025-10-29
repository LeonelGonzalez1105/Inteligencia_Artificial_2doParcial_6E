def bayes_rule(prior_H, likelihood_E_given_H, prob_E):
    """
    Calcula la probabilidad posterior P(H|E) usando la Regla de Bayes.
    
    P(H|E) = (P(E|H) * P(H)) / P(E)
    """
    
    # 1. Calcular el numerador: P(E|H) * P(H)
    # Esta es la probabilidad conjunta P(E, H)
    numerator = likelihood_E_given_H * prior_H
    
    # 2. Dividir por el denominador (P(E))
    if prob_E == 0:
        return 0.0 # La evidencia era imposible
        
    posterior_prob = numerator / prob_E
    
    return posterior_prob

# --- 1. Definir los componentes del problema del test médico ---

# H = Tienes la enfermedad
# E = El test da Positivo

# P(H): Probabilidad a Priori de tener la enfermedad
prior_H = 0.01
# P(¬H): Probabilidad a Priori de NO tenerla
prior_not_H = 1.0 - prior_H # 0.99

# P(E|H): Verosimilitud (Likelihood) - Test positivo si estás enfermo
likelihood_E_given_H = 0.99 # (True Positive Rate)

# P(E|¬H): Verosimilitud - Test positivo si estás SANO
likelihood_E_given_not_H = 0.01 # (False Positive Rate)

# --- 2. Calcular P(E), la constante de normalización ---
# P(E) = P(E, H) + P(E, ¬H)
# P(E) = P(E|H) * P(H) + P(E|¬H) * P(¬H)
#      (La prob. de un positivo verdadero) + (La prob. de un falso positivo)

prob_E = (likelihood_E_given_H * prior_H) + (likelihood_E_given_not_H * prior_not_H)

print("--- Calculando la Regla de Bayes ---")
print(f"Probabilidad a Priori P(H): {prior_H:.4f} (1%)")
print(f"Verosimilitud P(E|H) [Test + | Enfermo]: {likelihood_E_given_H:.4f} (99%)")
print(f"Verosimilitud P(E|¬H) [Test + | Sano]: {likelihood_E_given_not_H:.4f} (1%)")
print(f"Probabilidad total de dar Positivo P(E): {prob_E:.4f}")

# --- 3. Ejecutar el "algoritmo" (Regla de Bayes) ---

# P(H|E) = P(Enfermo | Positivo)
posterior_prob = bayes_rule(prior_H, likelihood_E_given_H, prob_E)

print("\n--- Resultado ---")
print(f"Probabilidad Posterior P(H|E) = P(Enfermo | Positivo) = {posterior_prob:.4f}")