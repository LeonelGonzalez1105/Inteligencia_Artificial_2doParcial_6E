import numpy as np
import matplotlib.pyplot as plt
import math

# --- 1. Definir el Modelo (No Lineal, No Gaussiano opcional) ---

# Estado oculto X = [posición]
# Observación Z = [posición_medida]

NUM_PARTICLES = 1000
NUM_STEPS = 50

# Modelo de Transición (No Lineal) P(xt | xt-1)
# xt = xt-1 + sin(t/5) + ruido_proceso
PROCESS_NOISE_STD = 0.5
def transition_model(x_prev, t):
    return x_prev + math.sin(t / 5.0) + np.random.normal(0, PROCESS_NOISE_STD)

# Modelo de Sensor P(z | xt)
# z = xt + ruido_medicion
MEASUREMENT_NOISE_STD = 1.0
def measurement_model(x_true):
    return x_true + np.random.normal(0, MEASUREMENT_NOISE_STD)

# Función de Verosimilitud (Likelihood) P(z | x_particle)
# (Usamos la densidad de probabilidad Gaussiana)
def likelihood(z_observed, x_particle):
    # P(z | x) = Gaussian(z; mean=x, std=MEASUREMENT_NOISE_STD)
    prob_density = (1.0 / (MEASUREMENT_NOISE_STD * np.sqrt(2 * np.pi))) * \
                   np.exp(-0.5 * ((z_observed - x_particle) / MEASUREMENT_NOISE_STD)**2)
    return prob_density

# --- 2. El "Algoritmo": Filtro de Partículas ---

def particle_filter(observations):
    
    # 1. Inicialización: Partículas alrededor de 0
    particles = np.random.normal(0, 1, NUM_PARTICLES)
    weights = np.ones(NUM_PARTICLES) / NUM_PARTICLES # Pesos iguales al inicio
    
    estimated_positions = [] # Para guardar la media estimada

    print("--- Ejecutando Filtro de Partículas ---")
    
    # 2. Bucle Principal (para cada observación)
    for t, z in enumerate(observations):
        
        # --- PASO A: PREDICCIÓN (Mover Partículas) ---
        particles = np.array([transition_model(p, t) for p in particles])
        
        # --- PASO B: ACTUALIZACIÓN (Ponderar Partículas) ---
        # Calcular P(z | particle) para cada partícula
        weights = np.array([likelihood(z, p) for p in particles])
        
        # Normalizar los pesos (para que sumen 1)
        total_weight = np.sum(weights)
        if total_weight > 0:
            weights /= total_weight
        else:
            # Si todas las partículas son muy improbables, re-inicializar
            print(f"  Advertencia en t={t}: Pesos cero. Re-inicializando.")
            particles = np.random.normal(z, 5, NUM_PARTICLES) # Centrado en la medición
            weights = np.ones(NUM_PARTICLES) / NUM_PARTICLES
            
        # --- ESTIMACIÓN (Opcional): Calcular la media ponderada ---
        mean_estimate = np.sum(particles * weights)
        estimated_positions.append(mean_estimate)
        if t % 10 == 0:
             print(f"  Paso {t}: Medida={z:.2f}, Est Pos={mean_estimate:.2f}")

        # --- PASO C: REMUESTREO (Resampling) ---
        # (Usamos muestreo sistemático o multinomial simple)
        indices = np.random.choice(np.arange(NUM_PARTICLES), size=NUM_PARTICLES, 
                                   replace=True, p=weights)
        particles = particles[indices]
        # (Los pesos se resetean a iguales después del remuestreo)
        weights.fill(1.0 / NUM_PARTICLES) 

    print("Filtrado completado.")
    return estimated_positions, particles # Devuelve últimas partículas

# --- 3. Simulación del Mundo Real ---
np.random.seed(42)
real_states = np.zeros(NUM_STEPS)
observations = np.zeros(NUM_STEPS)
for t in range(1, NUM_STEPS):
    real_states[t] = transition_model(real_states[t-1], t)
observations = np.array([measurement_model(x) for x in real_states])

# --- 4. Ejecutar el Filtro ---
estimated_pos, final_particles = particle_filter(observations)

# --- 5. Graficar Resultados ---
plt.figure(figsize=(12, 6))
plt.plot(real_states, 'g-', label='Posición Real (Oculta)')
plt.scatter(range(NUM_STEPS), observations, marker='x', color='r', label='Mediciones (Ruidosas)', s=20, alpha=0.5)
plt.plot(estimated_pos, 'b--', label='Estimación Filtro Partículas')
# Mostrar la dispersión de las partículas finales
plt.scatter([NUM_STEPS-1]*len(final_particles), final_particles, color='b', s=5, alpha=0.2, label=f'Partículas Finales (N={NUM_PARTICLES})')

plt.title('Filtro de Partículas: Seguimiento 1D No Lineal')
plt.xlabel('Paso de Tiempo')
plt.ylabel('Posición')
plt.legend()
plt.grid(True)
plt.show()