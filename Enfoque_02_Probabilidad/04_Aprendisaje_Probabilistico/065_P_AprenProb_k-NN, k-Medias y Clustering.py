import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# --- 0. Generar Datos Sintéticos ---
# Vamos a crear 3 grupos de datos con etiquetas conocidas.
np.random.seed(42)
k_grupos = 3

# Generar 3 "manchas" (blobs) de datos
data_0 = np.random.randn(100, 2) + np.array([5, 5])
data_1 = np.random.randn(100, 2) + np.array([-5, -5])
data_2 = np.random.randn(100, 2) + np.array([5, -5])

# X son las coordenadas (lo que "vemos")
X_datos = np.concatenate((data_0, data_1, data_2))
# y son las etiquetas verdaderas (lo que queremos predecir/ignorar)
y_etiquetas_reales = np.array([0]*100 + [1]*100 + [2]*100)


# ===================================================================
#  PARTE 1: CLUSTERING NO SUPERVISADO (k-Medias / k-Means)
#  Objetivo: Encontrar grupos en datos NO ETIQUETADOS.
# ===================================================================

def calcular_distancia(p1, p2):
    """Calcula la distancia Euclidiana."""
    return np.sqrt(np.sum((p1 - p2)**2))

def asignar_clusters(X, centroides):
    """(E-Step) Asigna cada punto al centroide más cercano."""
    etiquetas = np.zeros(X.shape[0], dtype=int)
    for i, punto in enumerate(X):
        distancias = [calcular_distancia(punto, c) for c in centroides]
        etiquetas[i] = np.argmin(distancias)
    return etiquetas

def actualizar_centroides(X, etiquetas, k):
    """(M-Step) Mueve el centroide a la media de sus puntos."""
    nuevos_centroides = np.zeros((k, X.shape[1]))
    for j in range(k):
        puntos_del_cluster = X[etiquetas == j]
        if len(puntos_del_cluster) > 0:
            nuevos_centroides[j] = np.mean(puntos_del_cluster, axis=0)
    return nuevos_centroides

def run_kmeans(X, k, max_iter=100):
    """Ejecuta el algoritmo k-Means completo."""
    print(f"--- Ejecutando k-Means (k={k}) ---")
    centroides = X[np.random.choice(X.shape[0], k, replace=False)] # Inicialización
    
    for i in range(max_iter):
        etiquetas = asignar_clusters(X, centroides)
        nuevos_centroides = actualizar_centroides(X, etiquetas, k)
        if np.allclose(centroides, nuevos_centroides):
            break
        centroides = nuevos_centroides
        
    print("k-Means finalizado.")
    return centroides, etiquetas

# ===================================================================
#  PARTE 2: CLASIFICACIÓN SUPERVISADA (k-Vecinos Más Cercanos / k-NN)
#  Objetivo: Predecir la etiqueta de un NUEVO punto
#            basado en datos ETIQUETADOS.
# ===================================================================

def predecir_knn(X_train, y_train, punto_nuevo, k):
    """
    Predice la clase de un 'punto_nuevo' usando k-NN.
    """
    
    # 1. Calcular distancias a TODOS los puntos de entrenamiento
    distancias = [calcular_distancia(punto_nuevo, p_train) for p_train in X_train]
    
    # 2. Encontrar los k índices más cercanos
    #    (np.argsort ordena las distancias y devuelve los índices)
    k_indices_cercanos = np.argsort(distancias)[:k]
    
    # 3. Obtener las etiquetas de esos k vecinos
    k_etiquetas_cercanas = [y_train[i] for i in k_indices_cercanos]
    
    # 4. Hacer una "votación" (encontrar la etiqueta más común)
    #    Counter(...).most_common(1) devuelve [('etiqueta', conteo)]
    prediccion = Counter(k_etiquetas_cercanas).most_common(1)[0][0]
    
    return prediccion

# --- 3. Ejecución y Visualización ---

# --- Visualización 1: k-Means ---
# ¡Observa que k-Means NO usa 'y_etiquetas_reales'!
print("Ejecutando Parte 1: k-Means (No Supervisado)")
centroides_kmeans, etiquetas_kmeans = run_kmeans(X_datos, k=3)

plt.figure(figsize=(18, 8))
plt.subplot(1, 2, 1) # Gráfica 1 de 2
plt.title(f'Parte 1: Clustering k-Means (No Supervisado)\n(Descubrió los grupos)')
# Coloreamos los puntos según las etiquetas que k-Means ENCONTRÓ
plt.scatter(X_datos[:, 0], X_datos[:, 1], c=etiquetas_kmeans, cmap='viridis', s=25, alpha=0.7)
plt.scatter(centroides_kmeans[:, 0], centroides_kmeans[:, 1], 
            marker='X', s=300, c='red', edgecolor='black', label='Centroides Finales')
plt.legend()
plt.grid(True)

# --- Visualización 2: k-NN ---
print("\nEjecutando Parte 2: k-NN (Supervisado)")
K_VECINOS = 5

# Puntos de prueba (nuevos datos que queremos clasificar)
puntos_prueba = np.array([
    [0, 0],     # Debería ser 'Grupo 1' (azul)
    [5, -10],   # Debería ser 'Grupo 2' (verde)
    [8, 8]      # Debería ser 'Grupo 0' (morado)
])
etiquetas_prueba = []

# ¡k-NN SÍ usa 'X_datos' y 'y_etiquetas_reales' para "entrenar"!
for punto in puntos_prueba:
    pred = predecir_knn(X_datos, y_etiquetas_reales, punto, k=K_VECINOS)
    etiquetas_prueba.append(pred)
    print(f"  Punto de prueba {punto} -> Predicción k-NN: Grupo {pred}")

plt.subplot(1, 2, 2) # Gráfica 2 de 2
plt.title(f'Parte 2: Clasificación k-NN (Supervisado)\n(Predijo nuevos puntos)')
# Coloreamos los puntos según sus etiquetas REALES
plt.scatter(X_datos[:, 0], X_datos[:, 1], c=y_etiquetas_reales, cmap='viridis', s=25, alpha=0.3, label='Datos de Entrenamiento')
# Graficar los nuevos puntos con su predicción
plt.scatter(puntos_prueba[:, 0], puntos_prueba[:, 1], 
            c=etiquetas_prueba, cmap='viridis', 
            marker='*', s=500, edgecolor='red', linewidth=2,
            label=f'Predicciones k-NN (k={K_VECINOS})')
plt.legend()
plt.grid(True)

plt.suptitle('Diferencia entre k-Means (Clustering) y k-NN (Clasificación)')
plt.show()