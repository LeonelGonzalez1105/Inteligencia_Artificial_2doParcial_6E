import numpy as np
import matplotlib.pyplot as plt
import random

# --- 1. Generar Datos Sintéticos ---
# (El algoritmo NO verá estas etiquetas, son solo para la creación)
np.random.seed(42) # Para que los resultados sean reproducibles

def generar_datos(n_puntos_por_cluster=100, k_clusters=3):
    """Genera nubes de puntos 2D para el clustering."""
    X = []
    for _ in range(k_clusters):
        # Elegir un centro aleatorio para la nube
        centro_x = random.randint(-15, 15)
        centro_y = random.randint(-15, 15)
        # Crear puntos alrededor del centro
        puntos = np.random.randn(n_puntos_por_cluster, 2) + [centro_x, centro_y]
        X.append(puntos)
    
    # Mezclar todos los datos en un solo array
    X = np.concatenate(X)
    return X

# --- 2. El Algoritmo k-Means ---

def calcular_distancia(p1, p2):
    """Calcula la distancia Euclidiana entre dos puntos."""
    return np.sqrt(np.sum((p1 - p2)**2))

def inicializar_centroides(X, k):
    """Elige k puntos aleatorios de los datos como centroides iniciales."""
    n_puntos = X.shape[0]
    indices = np.random.choice(n_puntos, k, replace=False)
    return X[indices]

def asignar_clusters(X, centroides):
    """
    Paso de Asignación (E-Step): Asigna cada punto al centroide más cercano.
    Devuelve un array de etiquetas (índices de cluster).
    """
    k = centroides.shape[0]
    etiquetas = np.zeros(X.shape[0], dtype=int)
    
    for i, punto in enumerate(X):
        # Calcular distancia de este punto a cada centroide
        distancias = [calcular_distancia(punto, c) for c in centroides]
        # Asignar la etiqueta del centroide más cercano
        etiquetas[i] = np.argmin(distancias)
        
    return etiquetas

def actualizar_centroides(X, etiquetas, k):
    """
    Paso de Actualización (M-Step): Recalcula los centroides como
    la media de los puntos asignados a ellos.
    """
    nuevos_centroides = np.zeros((k, X.shape[1]))
    
    for j in range(k):
        # Obtener todos los puntos asignados al cluster j
        puntos_del_cluster = X[etiquetas == j]
        
        # Si el cluster no está vacío, calcular su media
        if len(puntos_del_cluster) > 0:
            nuevos_centroides[j] = np.mean(puntos_del_cluster, axis=0)
        else:
            # Si un cluster queda vacío, re-inicializarlo (solución simple)
            nuevos_centroides[j] = X[random.randint(0, X.shape[0]-1)]
            
    return nuevos_centroides

def run_kmeans(X, k, max_iter=100):
    """Ejecuta el algoritmo k-Means completo."""
    print(f"--- Ejecutando k-Means (k={k}) ---")
    centroides = inicializar_centroides(X, k)
    
    for i in range(max_iter):
        # 1. Asignar puntos
        etiquetas = asignar_clusters(X, centroides)
        
        # 2. Actualizar centroides
        nuevos_centroides = actualizar_centroides(X, etiquetas, k)
        
        # 3. Comprobar convergencia
        if np.allclose(centroides, nuevos_centroides):
            print(f"Convergencia alcanzada en la iteración {i+1}.")
            break
            
        centroides = nuevos_centroides
        
    print("k-Means finalizado.")
    return centroides, etiquetas

# --- 3. Ejecutar y Visualizar ---

# Número de clusters que queremos encontrar
K_ELEGIDO = 3
# Generar los datos que el algoritmo "verá"
X_datos = generar_datos(k_clusters=K_ELEGIDO)

# Ejecutar el algoritmo
centroides_finales, etiquetas_finales = run_kmeans(X_datos, K_ELEGIDO)

# --- 4. Visualización ---
plt.figure(figsize=(10, 7))
plt.title('Agrupamiento No Supervisado (k-Means)')

# Graficar los puntos de datos, coloreados por la etiqueta final
# 'c=etiquetas_finales' es la magia: colorea según el array de etiquetas
# 'cmap='viridis'' es un mapa de color (morado, verde, amarillo)
plt.scatter(X_datos[:, 0], X_datos[:, 1], c=etiquetas_finales, cmap='viridis', s=25, alpha=0.7, label='Datos Agrupados')

# Graficar los centroides finales como 'X' rojas
plt.scatter(centroides_finales[:, 0], centroides_finales[:, 1], 
            marker='X', s=300, c='red', edgecolor='black', 
            label='Centroides Finales')

plt.xlabel('Característica X')
plt.ylabel('Característica Y')
plt.legend()
plt.grid(True)
plt.show()