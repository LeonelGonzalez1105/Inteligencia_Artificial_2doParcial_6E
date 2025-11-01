import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC # El clasificador SVM
from sklearn.datasets import make_moons # Para generar datos no lineales

# --- 1. Generar Datos No Lineales ("Medias Lunas") ---
# X: coordenadas, y: etiquetas (0 o 1)
X, y = make_moons(n_samples=200, noise=0.1, random_state=42)

# --- 2. Crear y Entrenar los Clasificadores SVM ---

# Clasificador 1: SVM Lineal (sin truco de núcleo)
# (Fallará en este problema)
svm_lineal = SVC(kernel='linear', C=1.0)
svm_lineal.fit(X, y)
print("Entrenado SVM con kernel='linear'...")

# Clasificador 2: SVM con Núcleo RBF (Radial Basis Function)
# (Tendrá éxito)
svm_rbf = SVC(kernel='rbf', C=1.0, gamma='auto')
svm_rbf.fit(X, y)
print("Entrenado SVM con kernel='rbf'...")


# --- 3. Función de Ayuda para Visualizar ---
def plot_decision_boundary(clf, X_data, y_data, ax, title):
    """Grafica los datos y la frontera de decisión."""
    # Crear una malla de puntos para evaluar el modelo
    x_min, x_max = X_data[:, 0].min() - 0.5, X_data[:, 0].max() + 0.5
    y_min, y_max = X_data[:, 1].min() - 0.5, X_data[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 50),
                         np.linspace(y_min, y_max, 50))
    
    # Obtener las predicciones para cada punto de la malla
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # Graficar la "zona" de decisión
    ax.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.3)
    # Graficar los puntos de datos
    ax.scatter(X_data[:, 0], X_data[:, 1], c=y_data, cmap=plt.cm.coolwarm,
                s=25, edgecolors='k')
    
    # Resaltar los vectores soporte
    ax.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1],
               s=100, facecolors='none', edgecolors='k',
               label='Vectores Soporte')
    
    ax.set_title(title)
    ax.legend()
    ax.grid(True)

# --- 4. Visualizar los Resultados ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
plt.suptitle('Máquinas de Vectores Soporte (SVM)', fontsize=16)

# Gráfica 1: El SVM Lineal Falla
plot_decision_boundary(svm_lineal, X, y, ax1, 
                       'SVM con Kernel Lineal\n(Falla en datos no lineales)')

# Gráfica 2: El SVM RBF Triunfa
plot_decision_boundary(svm_rbf, X, y, ax2, 
                       'SVM con Kernel "RBF" (Núcleo)\n(Tiene éxito)')

plt.show()