import numpy as np
import matplotlib.pyplot as plt

# --- 1. Generar Datos Sintéticos (Colores RGB) ---
# Vamos a crear 3 grupos de colores (rojos, verdes, azules)
np.random.seed(42)
N_puntos_por_clase = 50
# Grupo 1: Rojos (R alto, G/B bajos)
data_reds = np.random.rand(N_puntos_por_clase, 3) * [1.0, 0.2, 0.2] + [0.5, 0, 0]
# Grupo 2: Verdes (G alto, R/B bajos)
data_greens = np.random.rand(N_puntos_por_clase, 3) * [0.2, 1.0, 0.2] + [0, 0.5, 0]
# Grupo 3: Azules (B alto, R/G bajos)
data_blues = np.random.rand(N_puntos_por_clase, 3) * [0.2, 0.2, 1.0] + [0, 0, 0.5]

# Mezclamos todos los datos (el algoritmo solo ve esta lista)
X_data = np.concatenate((data_reds, data_greens, data_blues))
# También guardamos los colores reales para la visualización
y_colors = np.concatenate((
    [[1,0,0]] * N_puntos_por_clase, # Etiquetas Rojas
    [[0,1,0]] * N_puntos_por_clase, # Etiquetas Verdes
    [[0,0,1]] * N_puntos_por_clase  # Etiquetas Azules
))
# Barajar los datos y las etiquetas juntos
shuffle_idx = np.random.permutation(len(X_data))
X_data = X_data[shuffle_idx]
y_colors = y_colors[shuffle_idx]


# --- 2. El Algoritmo: Mapa Autoorganizado (SOM) ---

class SOM:
    def __init__(self, map_width, map_height, input_dim, learning_rate, radius):
        self.map_width = map_width
        self.map_height = map_height
        self.input_dim = input_dim # Dimensión de los datos (ej. 3 para RGB)
        self.lr = learning_rate
        self.radius = radius # Radio de vecindad inicial
        
        # Inicializar los pesos (el "mapa") aleatoriamente
        # Cada neurona (pixel) del mapa tiene un vector de pesos de 3D (RGB)
        self.weights = np.random.rand(map_width, map_height, input_dim)

    def _find_bmu(self, x):
        """Encuentra la Unidad de Mejor Coincidencia (BMU) para un dato x."""
        min_dist = np.inf
        bmu_idx = (0, 0)
        for i in range(self.map_width):
            for j in range(self.map_height):
                w = self.weights[i, j, :]
                dist = np.linalg.norm(x - w) # Distancia Euclidiana
                if dist < min_dist:
                    min_dist = dist
                    bmu_idx = (i, j)
        return bmu_idx

    def _update_weights(self, x, bmu_idx, t, max_iter):
        """Actualiza los pesos del BMU y sus vecinos."""
        
        # Encoger el radio y la tasa de aprendizaje con el tiempo
        current_radius = self.radius * (1 - t / max_iter)
        current_lr = self.lr * (1 - t / max_iter)
        
        for i in range(self.map_width):
            for j in range(self.map_height):
                w = self.weights[i, j, :]
                # Distancia en la *cuadrícula* (mapa 2D)
                dist_to_bmu = np.linalg.norm(np.array([i, j]) - np.array(bmu_idx))
                
                # Si está dentro del radio de vecindad...
                if dist_to_bmu <= current_radius:
                    # Calcular la influencia (más cerca = más influencia)
                    influence = np.exp(- (dist_to_bmu**2) / (2 * current_radius**2))
                    
                    # Actualizar el peso (tirar de él hacia el dato x)
                    new_w = w + current_lr * influence * (x - w)
                    self.weights[i, j, :] = new_w / np.linalg.norm(new_w) # Normalizar (para colores)

    def fit(self, X, num_iterations):
        """Entrena el SOM."""
        print(f"--- Entrenando SOM ({self.map_width}x{self.map_height}) ---")
        max_iter = num_iterations
        for t in range(max_iter):
            if (t+1) % 100 == 0:
                print(f"  Iteración {t+1}/{max_iter}...")
            # 1. Muestreo: Tomar un dato al azar
            x = X[np.random.randint(0, len(X))]
            
            # 2. Competición: Encontrar BMU
            bmu_idx = self._find_bmu(x)
            
            # 3. Actualización (Cooperación)
            self._update_weights(x, bmu_idx, t, max_iter)
        print("Entrenamiento finalizado.")

# --- 3. Ejecutar y Visualizar ---
MAP_SIZE = 20 # 20x20
som = SOM(map_width=MAP_SIZE, map_height=MAP_SIZE, input_dim=3, 
          learning_rate=0.5, radius=MAP_SIZE/2)

som.fit(X_data, num_iterations=1000)

# --- 4. Visualización ---
print("\nVisualizando el Mapa Autoorganizado...")
# El resultado es el mapa de pesos 'som.weights'
# Cada pixel (i,j) tiene un color (R,G,B)
plt.figure(figsize=(8, 8))
plt.title('Mapa Autoorganizado de Kohonen (SOM)\n(Agrupando Colores RGB)')
# 'imshow' muestra una matriz como una imagen
plt.imshow(som.weights)
plt.xlabel('Neurona X')
plt.ylabel('Neurona Y')
plt.show()

# --- Visualización 2: Mapa de calor de BMUs ---
# Ver dónde "cayeron" los datos de entrenamiento
print("Visualizando mapa de calor de datos...")
heatmap = np.zeros((MAP_SIZE, MAP_SIZE))
for x, color in zip(X_data, y_colors):
    bmu_idx = som._find_bmu(x)
    heatmap[bmu_idx] += 1 # Contar cuántos puntos cayeron aquí

plt.figure(figsize=(8, 8))
plt.title('Mapa de Calor de BMUs\n(Dónde se agruparon los datos)')
plt.imshow(heatmap, cmap='hot')
plt.colorbar(label='Número de Puntos Mapeados')
plt.show()