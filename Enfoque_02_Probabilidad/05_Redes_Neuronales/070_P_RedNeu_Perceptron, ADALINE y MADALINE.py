import numpy as np
import matplotlib.pyplot as plt

# --- 1. Definición de la Clase PERCEPTRÓN ---
# (Usa la Regla de Aprendizaje del Perceptrón)

class Perceptron:
    """Implementa un Perceptrón simple."""
    
    def __init__(self, learning_rate=0.1, n_iterations=100):
        self.lr = learning_rate
        self.n_iters = n_iterations
        self.weights = None
        self.bias = 0
        
    def activation(self, x):
        """Función de Activación (Escalón)"""
        return 1 if x >= 0 else 0

    def fit(self, X, y):
        """Entrena el Perceptrón usando la Regla de Aprendizaje."""
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features) # Inicializar pesos a 0
        
        for _ in range(self.n_iters):
            for i in range(n_samples):
                xi = X[i]
                target = y[i]
                
                # 1. Calcular salida lineal
                linear_output = np.dot(xi, self.weights) + self.bias
                # 2. Obtener predicción (salida 0 o 1)
                prediction = self.activation(linear_output)
                
                # 3. Calcular error (basado en la predicción 0/1)
                error = target - prediction
                
                # 4. Actualizar pesos SOLO SI hay error
                if error != 0:
                    update = self.lr * error
                    self.weights += update * xi
                    self.bias += update
                    
    def predict(self, X):
        """Predice la clase para nuevas entradas."""
        linear_output = np.dot(X, self.weights) + self.bias
        # Convertir la función de activación a numpy para que funcione en arrays
        y_predicted = np.vectorize(self.activation)(linear_output)
        return y_predicted

# --- 2. Definición de la Clase ADALINE ---
# (Usa la Regla Delta / Widrow-Hoff)
# [Image of ADALINE neuron model]

class ADALINE:
    """Implementa una neurona ADALINE (Adaptive Linear Neuron)."""
    
    def __init__(self, learning_rate=0.01, n_iterations=100):
        self.lr = learning_rate
        self.n_iters = n_iterations
        self.weights = None
        self.bias = 0
        
    def activation(self, x):
        """Función de Activación (Escalón) - SOLO para predicción final."""
        return 1 if x >= 0 else 0

    def linear_output(self, X):
        """Calcula la salida lineal (antes de la activación)."""
        return np.dot(X, self.weights) + self.bias

    def fit(self, X, y):
        """Entrena el ADALINE usando la Regla Delta (Gradiente Descendente)."""
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        
        for _ in range(self.n_iters):
            # 1. Calcular salida lineal PARA TODOS los datos
            z = self.linear_output(X)
            
            # 2. ¡LA CLAVE! Calcular el error sobre la SALIDA LINEAL (z),
            #    no sobre la predicción 0/1.
            error = y - z
            
            # 3. Actualizar pesos usando Gradiente Descendente
            #    (Se actualiza siempre, no solo en errores)
            self.weights += self.lr * X.T.dot(error)
            self.bias += self.lr * np.sum(error)
            
    def predict(self, X):
        """Predice la clase usando la función escalón."""
        linear_output = self.linear_output(X)
        y_predicted = np.vectorize(self.activation)(linear_output)
        return y_predicted

# --- 3. Definición de MADALINE (Conceptual) ---
# (Multiple ADALINE)
# [Image of MADALINE network structure for XOR]
# El entrenamiento de MADALINE (Regla MRI) es muy complejo.
# Aquí, "cablearemos" una red MADALINE con pesos YA CONOCIDOS
# para demostrar su CAPACIDAD (resolver XOR), que Perceptrón y ADALINE no pueden.

class MADALINE_XOR:
    """
    Implementa una red MADALINE con pesos fijos para resolver XOR.
    XOR = (x1 OR x2) AND (NOT (x1 AND x2))
    """
    def __init__(self):
        # Usaremos la lógica de un Perceptrón/ADALINE para cada neurona
        
        # Capa Oculta
        # h1 (Neurona OR)
        self.weights_h1 = np.array([1, 1])
        self.bias_h1 = -0.5 # (1*1 + 0*1) - 0.5 = 0.5 -> 1
        
        # h2 (Neurona NAND - NOT AND)
        self.weights_h2 = np.array([-1, -1])
        self.bias_h2 = 1.5 # (1*1*(-1) + 1*1*(-1)) + 1.5 = -0.5 -> 0
        
        # Capa de Salida
        # o1 (Neurona AND)
        self.weights_o1 = np.array([1, 1])
        self.bias_o1 = -1.5 # (1*1 + 1*1) - 1.5 = 0.5 -> 1

    def activation(self, x):
        return 1 if x >= 0 else 0
        
    def predict(self, X):
        predictions = []
        for xi in X:
            # Calcular salida de la capa oculta
            h1_out = self.activation(np.dot(xi, self.weights_h1) + self.bias_h1)
            h2_out = self.activation(np.dot(xi, self.weights_h2) + self.bias_h2)
            
            # Entrada a la capa de salida
            hidden_out = np.array([h1_out, h2_out])
            
            # Calcular salida final
            final_out = self.activation(np.dot(hidden_out, self.weights_o1) + self.bias_o1)
            predictions.append(final_out)
        return np.array(predictions)
        
    def fit(self, X, y):
        # Esta es la parte compleja (MRI/MRII) que omitimos
        print("MADALINE (XOR) está pre-cableado. No se ejecuta 'fit'.")

# --- 4. Función de Ayuda para Graficar ---

def plot_decision_boundary(clf, X, y, ax, title):
    """Grafica la frontera de decisión de un clasificador."""
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))
    
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.coolwarm)
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm,
                s=50, edgecolors='k')
    ax.set_title(title)
    ax.grid(True)
    
# --- 5. Datos de Prueba (Problemas Lógicos) ---

# AND (Linealmente Separable)
X_and = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_and = np.array([0, 0, 0, 1])

# OR (Linealmente Separable)
X_or = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_or = np.array([0, 1, 1, 1])

# XOR (NO Linealmente Separable)
X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([0, 1, 1, 0])

# --- 6. Ejecutar y Visualizar Todo ---

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(21, 6))

# --- Demo 1: Perceptrón (resuelve AND) ---
print("Entrenando Perceptrón en datos 'AND'...")
perceptron = Perceptron(learning_rate=0.1, n_iterations=20)
perceptron.fit(X_and, y_and)
plot_decision_boundary(perceptron, X_and, y_and, ax1, 
                       "1. Perceptrón (Resuelve AND)\n(Linealmente Separable)")

# --- Demo 2: ADALINE (resuelve OR) ---
print("Entrenando ADALINE en datos 'OR'...")
adaline = ADALINE(learning_rate=0.01, n_iterations=100)
adaline.fit(X_or, y_or)
plot_decision_boundary(adaline, X_or, y_or, ax2, 
                       "2. ADALINE (Resuelve OR)\n(Linealmente Separable)")