import numpy as np

# --- 0. Funciones de Ayuda para Conversión de Datos ---
# Hopfield funciona mejor con bipolar (-1, 1)
# Hamming funciona con binario (0, 1)

def to_bipolar(binary_pattern):
    """Convierte un array de (0, 1) a (-1, 1)."""
    return (binary_pattern * 2) - 1

def to_binary(bipolar_pattern):
    """Convierte un array de (-1, 1) a (0, 1)."""
    return ((bipolar_pattern + 1) / 2).astype(int)

# --- 1. Regla de Hebb (Implementada dentro de Hopfield) ---
def hebbian_learning(bipolar_patterns):
    """
    Calcula la matriz de pesos usando la Regla de Hebb.
    W = Suma( x * x^T )
    """
    print("  -> Aplicando Regla de Hebb para calcular pesos...")
    n_features = bipolar_patterns.shape[1]
    W = np.zeros((n_features, n_features))
    
    for x in bipolar_patterns:
        W += np.outer(x, x) # x * x^T
        
    np.fill_diagonal(W, 0) # Sin auto-conexiones
    return W

# --- 2. Red de Hopfield (Memoria Auto-Asociativa) ---
class HopfieldNetwork:
    """Recupera patrones bipolares ruidosos."""
    def __init__(self):
        self.W = None

    def fit(self, X_train_bipolar):
        """Almacena patrones usando la Regla de Hebb."""
        # ¡Aquí es donde se usa la Regla de Hebb!
        self.W = hebbian_learning(X_train_bipolar)

    def predict(self, X_noisy_bipolar, max_iter=10):
        """Recupera (limpia) un patrón ruidoso."""
        print("  -> Red de Hopfield iniciando recuperación...")
        s = X_noisy_bipolar.copy()
        
        for i in range(max_iter):
            s_old = s.copy()
            # Actualizar neuronas (asincrónicamente)
            for j in range(len(s)):
                h = np.dot(self.W[j, :], s) # Suma ponderada
                s[j] = 1 if h >= 0 else -1 # Función de activación (signo)
            
            if np.array_equal(s, s_old):
                print(f"     Red estabilizada en la iteración {i+1}.")
                return s
        return s

# --- 3. Red de Hamming (Clasificador de Prototipo) ---
class HammingNetwork:
    """Clasifica un patrón binario al prototipo más cercano."""
    def __init__(self, prototypes_binary):
        self.prototypes = prototypes_binary
        self.n_prototypes = prototypes_binary.shape[0]

    def predict(self, x_input_binary):
        """Encuentra el prototipo con la menor distancia de Hamming."""
        print("  -> Red de Hamming iniciando clasificación...")
        min_dist = np.inf
        best_prototype_idx = -1
        
        for i in range(self.n_prototypes):
            proto = self.prototypes[i]
            # Distancia de Hamming = número de bits diferentes
            dist = np.sum(x_input_binary != proto)
            print(f"     Distancia a Prototipo {i} ({proto}): {dist}")
            
            if dist < min_dist:
                min_dist = dist
                best_prototype_idx = i
                
        print(f"     Ganador: Prototipo {best_prototype_idx} (distancia {min_dist})")
        return self.prototypes[best_prototype_idx]

# --- 4. El Ejemplo Unificado ---

# --- Datos Base (Binarios 0, 1) ---
# (Dos prototipos simples)
P1_bin = np.array([0, 0, 0, 1, 1, 1])
P2_bin = np.array([1, 1, 1, 0, 0, 0])
prototipos_binarios = np.array([P1_bin, P2_bin])

# --- Datos de Entrada (Ruidosos) ---
# Es una versión de P1 con un bit erróneo
X_ruidoso_bin = np.array([0, 0, 1, 1, 1, 1])

print("--- DEMO: Hopfield (Auto-Asociación) vs. Hamming (Clasificación) ---")
print(f"Prototipo 1 (P1): {P1_bin}")
print(f"Prototipo 2 (P2): {P2_bin}")
print(f"Entrada Ruidosa (X): {X_ruidoso_bin} (Es P1 con un error)\n")

# --- DEMO HAMMING ---
print("--- Tarea 1: Clasificación con Red de Hamming ---")
hamming_net = HammingNetwork(prototipos_binarios)
resultado_hamming = hamming_net.predict(X_ruidoso_bin)
print(f"  Resultado Hamming: La entrada se CLASIFICA como -> {resultado_hamming}\n")

# --- DEMO HOPFIELD (usando Regla de Hebb) ---
print("--- Tarea 2: Reconstrucción con Red de Hopfield ---")

# 1. Convertir prototipos a bipolar para el entrenamiento
P1_bipolar = to_bipolar(P1_bin)
P2_bipolar = to_bipolar(P2_bin)
prototipos_bipolares = np.array([P1_bipolar, P2_bipolar])

# 2. Entrenar la red Hopfield (aquí se usa Hebb)
hopfield_net = HopfieldNetwork()
hopfield_net.fit(prototipos_bipolares) # ¡Aquí se ejecuta la Regla de Hebb!

# 3. Convertir la entrada ruidosa a bipolar
X_ruidoso_bipolar = to_bipolar(X_ruidoso_bin)

# 4. Predecir (recuperar)
resultado_hopfield_bipolar = hopfield_net.predict(X_ruidoso_bipolar)

# 5. Convertir el resultado de vuelta a binario para comparar
resultado_hopfield_bin = to_binary(resultado_hopfield_bipolar)
print(f"  Resultado Hopfield: La entrada se RECONSTRUYE como -> {resultado_hopfield_bin}\n")

# --- 4. Máquina de Boltzmann (Explicación Conceptual) ---
print("--- 4. Máquina de Boltzmann (Conceptual) ---")
print("Una Máquina de Boltzmann es como una Red de Hopfield 'ruidosa' (estocástica).")
print("En lugar de ir 'directo' al patrón estable, usa probabilidades y 'Temple Simulado'")
print("(como el algoritmo #13) para encontrar el estado de más baja energía.")
print("Esto le permite escapar de 'memorias falsas' (óptimos locales) donde Hopfield")
print("a veces se atasca. Su entrenamiento (aprendizaje) es mucho más complejo.")