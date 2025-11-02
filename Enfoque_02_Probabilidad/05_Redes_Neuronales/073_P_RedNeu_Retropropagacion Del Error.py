import numpy as np

# --- 1. Definir Funciones de Activación y sus Derivadas ---
# (Necesitamos la derivada para la Regla de la Cadena / Backprop)

def sigmoid(x):
    """Función de activación Sigmoide"""
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    """Derivada de la Sigmoide (necesaria para el gradiente)"""
    # x ya está en formato sigmoide (x = sigmoid(z))
    return x * (1 - x)

# --- 2. Definición de la Red Neuronal Multicapa ---

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        
        self.lr = learning_rate
        
        # --- Inicializar Pesos ALEATORIAMENTE ---
        # (¡Esto es crucial! Si empiezan en 0, no aprenden)
        # Pesos entre Entrada (i) y Oculta (h)
        self.weights_i_h = np.random.uniform(size=(input_nodes, hidden_nodes))
        # Pesos entre Oculta (h) y Salida (o)
        self.weights_h_o = np.random.uniform(size=(hidden_nodes, output_nodes))
        
        # Inicializar Biases (a 0 o aleatorio)
        self.bias_h = np.zeros(hidden_nodes)
        self.bias_o = np.zeros(output_nodes)

    def feedforward(self, X):
        """Paso 1: Pase Hacia Adelante (Predicción)"""
        
        # De Entrada a Oculta
        self.hidden_sum = np.dot(X, self.weights_i_h) + self.bias_h
        self.hidden_output = sigmoid(self.hidden_sum)
        
        # De Oculta a Salida
        self.output_sum = np.dot(self.hidden_output, self.weights_h_o) + self.bias_o
        self.final_output = sigmoid(self.output_sum)
        
        return self.final_output

    def backpropagate(self, X, y):
        """Pasos 2, 3 y 4: Calcular Error, Retropropagar y Actualizar"""
        
        # --- Paso 2: Calcular el Error Final ---
        # Error = Objetivo(y) - Predicción(final_output)
        output_error = y - self.final_output
        
        # --- Paso 3: Retropropagar el Error ---
        
        # Gradiente en la Capa de Salida
        # delta = error * derivada_activacion(salida)
        output_delta = output_error * sigmoid_derivative(self.final_output)
        
        # Error de la Capa Oculta (¿cuánta culpa tiene?)
        # (Error de salida propagado "hacia atrás" por los pesos)
        hidden_error = output_delta.dot(self.weights_h_o.T)
        
        # Gradiente en la Capa Oculta
        hidden_delta = hidden_error * sigmoid_derivative(self.hidden_output)
        
        # --- Paso 4: Actualización de Pesos (Descenso del Gradiente) ---
        
        # Actualizar pesos (Oculta -> Salida)
        # (Transponer la salida oculta para alinear matrices)
        self.weights_h_o += self.hidden_output.T.dot(output_delta) * self.lr
        self.bias_o += np.sum(output_delta, axis=0) * self.lr
        
        # Actualizar pesos (Entrada -> Oculta)
        self.weights_i_h += X.T.dot(hidden_delta) * self.lr
        self.bias_h += np.sum(hidden_delta, axis=0) * self.lr

    def train(self, X, y, epochs):
        """Ejecuta el ciclo de entrenamiento."""
        for i in range(epochs):
            # 1. Pase hacia adelante
            self.feedforward(X)
            # 2. Pase hacia atrás (Backprop)
            self.backpropagate(X, y)
            
            if (i+1) % 1000 == 0:
                loss = np.mean(np.square(y - self.final_output))
                print(f"Época {i+1}/{epochs}, Error (Loss): {loss:.6f}")

    def predict(self, X):
        """Predice 0 o 1"""
        output = self.feedforward(X)
        return np.round(output) # Redondear a 0 o 1

# --- 3. Datos del Problema XOR ---
X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
# 'y' debe tener la forma correcta (N_muestras, N_salidas)
y_xor = np.array([[0], [1], [1], [0]])

# --- 4. Crear y Entrenar la Red ---
# (2 entradas, 4 neuronas ocultas, 1 salida)
nn = NeuralNetwork(input_nodes=2, hidden_nodes=4, output_nodes=1, learning_rate=0.1)

print("--- Entrenando Red 'desde cero' con Retropropagación ---")
nn.train(X_xor, y_xor, epochs=10000)

# --- 5. Mostrar Resultados ---
print("\n--- Resultados de la Predicción (XOR) ---")
predictions = nn.predict(X_xor)
for entrada, prediccion in zip(X_xor, predictions):
    print(f"Entrada: {entrada} -> Predicción: {prediccion[0]}")