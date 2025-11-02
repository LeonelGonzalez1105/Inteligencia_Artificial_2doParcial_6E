import numpy as np
import matplotlib.pyplot as plt

# --- 1. Definir los Datos de los Problemas Lógicos ---

# Problema AND (Linealmente Separable)
X_and = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_and = np.array([0, 0, 0, 1]) # Clases (0 o 1)

# Problema XOR (NO Linealmente Separable)
X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([0, 1, 1, 0]) # Clases (0 o 1)

# --- 2. Función de Ayuda para Graficar ---
def plot_data(X, y, ax, title):
    """Grafica los puntos de datos con sus clases."""
    # Colores: 'red' para clase 0, 'blue' para clase 1
    colors = ['red' if label == 0 else 'blue' for label in y]
    ax.scatter(X[:, 0], X[:, 1], c=colors, s=150, edgecolors='k')
    
    # Añadir anotaciones para claridad
    for i, txt in enumerate(['(0,0)', '(0,1)', '(1,0)', '(1,1)']):
        ax.annotate(txt, (X[i, 0]+0.05, X[i, 1]+0.05))
        
    ax.set_title(title)
    ax.set_xlabel('Entrada X1')
    ax.set_ylabel('Entrada X2')
    ax.grid(True)
    ax.set_xticks([-0.5, 0, 1, 1.5])
    ax.set_yticks([-0.5, 0, 1, 1.5])

# --- 3. Visualización ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
plt.suptitle('Demostración de Separabilidad Lineal', fontsize=16)

# --- Gráfica 1: AND (Separable) ---
plot_data(X_and, y_and, ax1, 'Problema AND (Linealmente Separable)')
# Dibujamos una línea recta que SÍ los separa
# (Ej: y = -x + 1.5)
line_x = np.array([-0.5, 1.5])
line_y = -line_x + 1.5
ax1.plot(line_x, line_y, 'g--', linewidth=3, label='Línea Separadora Válida')
ax1.legend()


# --- Gráfica 2: XOR (No Separable) ---
plot_data(X_xor, y_xor, ax2, 'Problema XOR (NO Linealmente Separable)')
# (No dibujamos línea porque ninguna es posible)
ax2.legend()


plt.show()