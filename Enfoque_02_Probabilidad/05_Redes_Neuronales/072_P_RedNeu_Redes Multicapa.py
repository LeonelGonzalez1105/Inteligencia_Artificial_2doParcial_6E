import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam

# --- 1. Definir los Datos (El Problema XOR) ---
# (NO Linealmente Separable)
X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([0, 1, 1, 0])

print("--- Datos del Problema XOR (No Lineal) ---")
print("Entradas (X):")
print(X_xor)
print("Salidas (y):")
print(y_xor)

# --- 2. Definir la Arquitectura de la Red Multicapa ---

model = Sequential()
model.add(Input(shape=(2,))) # Capa de Entrada: 2 neuronas

# --- ¡LA CLAVE! La Capa Oculta ---
# 4 neuronas en esta capa (un número común para XOR)
# 'relu' es la función de activación no-lineal
model.add(Dense(4, activation='relu'))

# --- Capa de Salida ---
# 1 neurona de salida
# 'sigmoid' comprime la salida entre 0 y 1 (perfecto para 0/1)
model.add(Dense(1, activation='sigmoid'))

print("\n--- Arquitectura del Modelo (MLP) ---")
model.summary()

# --- 3. Compilar y Entrenar el Modelo ---
# Compilar: Configurar el proceso de aprendizaje
# 'adam': Un optimizador eficiente (el motor de aprendizaje)
# 'binary_crossentropy': La función de "pérdida" (error) para 0/1
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print("\n--- Entrenando la Red Multicapa... ---")
# 'epochs': Cuántas veces ver todos los datos (miles)
# 'verbose=0': Para que no imprima 5000 líneas
model.fit(X_xor, y_xor, epochs=5000, verbose=0)
print("¡Entrenamiento finalizado!")

# --- 4. Evaluar y Predecir ---
print("\n--- Resultados ---")

# Evaluar la precisión final
loss, accuracy = model.evaluate(X_xor, y_xor, verbose=0)
print(f"Precisión del modelo: {accuracy * 100:.2f}%")

# Ver las predicciones
predictions = model.predict(X_xor)
print("\nPredicciones (Salida de la Sigmoide):")
for entrada, prediccion in zip(X_xor, predictions):
    print(f"Entrada: {entrada} -> Predicción: {prediccion[0]:.4f} "
          f"(Más cercano a: {round(prediccion[0])})")