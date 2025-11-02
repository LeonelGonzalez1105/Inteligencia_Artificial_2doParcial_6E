import numpy as np
import matplotlib.pyplot as plt

# --- 1. Definición de las Funciones de Activación ---

def step_function(x):
    """Función Escalón (Perceptrón)"""
    return np.where(x > 0, 1, 0)

def sigmoid_function(x):
    """Función Sigmoide (Logística)"""
    return 1 / (1 + np.exp(-x))

def tanh_function(x):
    """Función Tangente Hiperbólica"""
    return np.tanh(x)

def relu_function(x):
    """Función ReLU (Unidad Lineal Rectificada)"""
    return np.maximum(0, x)

# --- 2. Generar Datos para Graficar ---
# Creamos un array de -10 a 10 con 100 puntos
x = np.linspace(-10, 10, 100)

# Calcular las salidas para cada función
y_step = step_function(x)
y_sigmoid = sigmoid_function(x)
y_tanh = tanh_function(x)
y_relu = relu_function(x)

# --- 3. Visualización (El "Algoritmo" en acción) ---
plt.figure(figsize=(14, 10))
plt.suptitle('Funciones de Activación Principales', fontsize=16)

# Gráfica 1: Escalón (Step)
plt.subplot(2, 2, 1) # (filas, columnas, índice)
plt.plot(x, y_step, 'b-', label='Step Function')
plt.title('Función Escalón (Step)')
plt.grid(True)
plt.legend()

# Gráfica 2: Sigmoide
plt.subplot(2, 2, 2)
plt.plot(x, y_sigmoid, 'g-', label='Sigmoid')
plt.title('Función Sigmoide (Rango: 0 a 1)')
plt.grid(True)
plt.legend()

# Gráfica 3: Tanh
plt.subplot(2, 2, 3)
plt.plot(x, y_tanh, 'r-', label='Tanh')
plt.title('Función Tanh (Rango: -1 a 1)')
plt.grid(True)
plt.legend()

# Gráfica 4: ReLU
plt.subplot(2, 2, 4)
plt.plot(x, y_relu, 'm-', label='ReLU')
plt.title('Función ReLU (Rango: 0 a $\infty$) - (Más usada)')
plt.grid(True)
plt.legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ajustar para el supertítulo
plt.show()