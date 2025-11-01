# Importamos la librería Keras, que es la API de alto nivel de TensorFlow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input


def build_deep_neural_network():
    """
    Define la arquitectura de una Red Neuronal Profunda.
    Esta red es "profunda" porque tiene más de una capa oculta.
    """
    
    print("--- 1. Definiendo la Arquitectura de la Red Neuronal Profunda ---")
    
    # "Sequential" significa que apilaremos las capas una encima de otra
    model = Sequential()

    # --- Capa de Entrada ---
    # Le decimos a la red qué forma tienen los datos de entrada.
    # Ej: una imagen "aplanada" de 28x28 píxeles = 784 entradas.
    model.add(Input(shape=(784,)))

    # --- 1ra Capa Oculta (Profundidad 1) ---
    # "Dense" significa que cada neurona se conecta con todas las de la capa anterior.
    # 128 neuronas en esta capa.
    # 'relu' (Rectified Linear Unit) es la Función de Activación (tema #68) más común.
    model.add(Dense(128, activation='relu'))
    
    # --- 2da Capa Oculta (Profundidad 2) ---
    # ¡Esto es lo que la hace "PROFUNDA"! Estamos apilando otra capa.
    # Esta capa aprende combinaciones de las 128 características de la capa anterior.
    model.add(Dense(64, activation='relu'))

    # --- Capa de Salida ---
    # 10 neuronas de salida (una para cada clase: 0, 1, 2, ..., 9).
    # 'softmax' es una función de activación que convierte las 10 salidas
    # en una distribución de probabilidad (ej. 90% seguro que es un '7').
    model.add(Dense(10, activation='softmax'))
    
    print("¡Arquitectura definida!")
    
    return model

# --- 2. Crear el Modelo y Mostrar Resumen ---
deep_model = build_deep_neural_network()

# "Compilar" el modelo (esto prepara el "motor" de entrenamiento)
# 'adam' es un optimizador popular (relacionado con Retropropagación)
# 'sparse_categorical_crossentropy' es la "función de pérdida" para este problema
deep_model.compile(optimizer='adam', 
                   loss='sparse_categorical_crossentropy', 
                   metrics=['accuracy'])

# Imprimir el resumen de la arquitectura
print("\n--- 3. Resumen del Modelo (Arquitectura) ---")
deep_model.summary()