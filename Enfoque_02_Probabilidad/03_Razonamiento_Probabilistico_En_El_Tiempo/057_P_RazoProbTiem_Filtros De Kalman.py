import numpy as np
import matplotlib.pyplot as plt

# --- 1. Definir el Modelo (Lineal-Gaussiano) ---

# Estado oculto X = [posición, velocidad].T (Vector columna)
# Observación Z = [posición_medida]

# Matrices del Filtro de Kalman
dt = 1.0  # Intervalo de tiempo

# Matriz de Transición (F): Cómo evoluciona el estado
# pos(t) = pos(t-1) + vel(t-1)*dt
# vel(t) = vel(t-1)
F = np.array([[1, dt],
              [0, 1]])

# Matriz de Observación (H): Cómo el estado genera la observación
# pos_medida = 1*pos + 0*vel
H = np.array([[1, 0]])

# Covarianza del Ruido del Proceso (Q): Incertidumbre en el movimiento
# (Pequeño ruido en la aceleración)
Q_accel_stddev = 0.1
Q = np.array([[(dt**4)/4, (dt**3)/2],
              [(dt**3)/2,  dt**2]]) * Q_accel_stddev**2

# Covarianza del Ruido de Medición (R): Incertidumbre del sensor
R_measurement_stddev = 1.0
R = np.array([[R_measurement_stddev**2]])


# --- 2. El "Algoritmo": Las Ecuaciones de Kalman ---

def kalman_filter(z, x_est_prev, P_est_prev):
    """
    Realiza un ciclo completo de Predicción y Actualización.
    Args:
        z: La medición actual.
        x_est_prev: La estimación del estado anterior [pos, vel].T
        P_est_prev: La covarianza de la estimación anterior.
    Returns:
        x_est: La nueva estimación del estado.
        P_est: La nueva covarianza.
    """
    # --- PASO 1: PREDICCIÓN ---
    # x_pred = F * x_est_prev
    x_pred = F @ x_est_prev
    # P_pred = F * P_est_prev * F.T + Q
    P_pred = F @ P_est_prev @ F.T + Q

    # --- PASO 2: ACTUALIZACIÓN ---
    # Ganancia de Kalman (K)
    # K = P_pred * H.T * inv(H * P_pred * H.T + R)
    innovation_cov = H @ P_pred @ H.T + R
    K = P_pred @ H.T @ np.linalg.inv(innovation_cov)

    # Estimación Actualizada
    # x_est = x_pred + K * (z - H * x_pred)
    measurement_residual = z - H @ x_pred
    x_est = x_pred + K @ measurement_residual

    # Covarianza Actualizada
    # P_est = (I - K * H) * P_pred
    I = np.eye(P_pred.shape[0]) # Matriz identidad
    P_est = (I - K @ H) @ P_pred

    return x_est, P_est

# --- 3. Simulación ---

# Simular el movimiento REAL (oculto)
np.random.seed(42)
num_steps = 50
real_pos = np.zeros(num_steps)
real_vel = np.ones(num_steps) * 0.5 # Velocidad constante inicial
for t in range(1, num_steps):
    # Añadir un pequeño ruido al movimiento real
    real_vel[t] = real_vel[t-1] + np.random.normal(0, Q_accel_stddev * dt) # Ruido en velocidad
    real_pos[t] = real_pos[t-1] + real_vel[t-1]*dt

# Simular las MEDICIONES RUIDOSAS
measurements = real_pos + np.random.normal(0, R_measurement_stddev, num_steps)

# Inicializar el Filtro de Kalman
x_estimate = np.array([[0], [0]]) # Estimación inicial [pos=0, vel=0].T
P_estimate = np.array([[100, 0], [0, 100]]) # Incertidumbre inicial alta

# Guardar resultados para graficar
estimated_positions = np.zeros(num_steps)
estimated_velocities = np.zeros(num_steps)
uncertainties = np.zeros(num_steps) # Varianza de la posición

# --- 4. Ejecutar el Filtro ---
print("--- Ejecutando Filtro de Kalman ---")
for t in range(num_steps):
    z_t = measurements[t] # Medición en tiempo t
    x_estimate, P_estimate = kalman_filter(z_t, x_estimate, P_estimate)
    
    estimated_positions[t] = x_estimate[0, 0]
    estimated_velocities[t] = x_estimate[1, 0]
    uncertainties[t] = P_estimate[0, 0] # Varianza (diagonal)
    
    if t % 10 == 0:
        print(f"  Paso {t}: Medida={z_t:.2f}, Est Pos={x_estimate[0,0]:.2f}, Est Vel={x_estimate[1,0]:.2f}")

# --- 5. Graficar Resultados ---
plt.figure(figsize=(12, 6))
plt.plot(real_pos, 'g-', label='Posición Real (Oculta)')
plt.scatter(range(num_steps), measurements, marker='x', color='r', label='Mediciones (Ruidosas)', s=20)
plt.plot(estimated_positions, 'b--', label='Estimación Kalman (Posición)')
# Graficar +/- 1 desviación estándar (raíz de la varianza)
plt.fill_between(range(num_steps),
                 estimated_positions - np.sqrt(uncertainties),
                 estimated_positions + np.sqrt(uncertainties),
                 color='blue', alpha=0.2, label='Incertidumbre (±1σ)')

plt.title('Filtro de Kalman: Seguimiento 1D')
plt.xlabel('Paso de Tiempo')
plt.ylabel('Posición')
plt.legend()
plt.grid(True)
plt.show()