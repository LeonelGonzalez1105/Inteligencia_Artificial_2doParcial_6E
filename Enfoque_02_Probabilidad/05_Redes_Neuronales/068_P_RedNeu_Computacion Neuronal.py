import numpy as np

def step_function(suma_ponderada):
    """Función de Activación (Escalón)"""
    if suma_ponderada > 0:
        return 1
    else:
        return 0

def neurona(entradas, pesos, bias):
    """
    Simula el cálculo de una única neurona (Perceptrón).
    """
    
    # 1. Asegurarse de que tenemos el mismo número de entradas y pesos
    if len(entradas) != len(pesos):
        raise ValueError("El número de entradas y pesos debe ser el mismo.")
        
    # 2. Calcular la Suma Ponderada (Producto Punto)
    # (x1*w1) + (x2*w2) + ...
    suma_ponderada = np.dot(entradas, pesos)
    
    # 3. Añadir el Bias
    suma_con_bias = suma_ponderada + bias
    
    # 4. Aplicar la Función de Activación
    salida = step_function(suma_con_bias)
    
    return salida

# --- Configuración para simular una compuerta AND ---
# ¿Cómo encontramos estos números? ¡Con un algoritmo de entrenamiento!
# Pero por ahora, los pondremos a mano.
# Si x1=1 y x2=1, queremos que (x1*w1 + x2*w2 + b) > 0
# Si no, queremos que sea <= 0

# Pesos: Le damos la misma importancia a ambas entradas
W_AND = np.array([1.0, 1.0]) 

# Bias: Este es el truco. Debe ser negativo.
# Si ponemos -1.5:
# (0*1 + 0*1) - 1.5 = -1.5 (-> 0)
# (0*1 + 1*1) - 1.5 = -0.5 (-> 0)
# (1*1 + 0*1) - 1.5 = -0.5 (-> 0)
# (1*1 + 1*1) - 1.5 = +0.5 (-> 1) ¡Funciona!
B_AND = -1.5

# --- Probar nuestra neurona AND ---
print("--- Probando una Neurona configurada como compuerta AND ---")

entrada_0_0 = np.array([0, 0])
salida_0_0 = neurona(entrada_0_0, W_AND, B_AND)
print(f"Entrada: [0, 0] -> Salida: {salida_0_0}")

entrada_0_1 = np.array([0, 1])
salida_0_1 = neurona(entrada_0_1, W_AND, B_AND)
print(f"Entrada: [0, 1] -> Salida: {salida_0_1}")

entrada_1_0 = np.array([1, 0])
salida_1_0 = neurona(entrada_1_0, W_AND, B_AND)
print(f"Entrada: [1, 0] -> Salida: {salida_1_0}")

entrada_1_1 = np.array([1, 1])
salida_1_1 = neurona(entrada_1_1, W_AND, B_AND)
print(f"Entrada: [1, 1] -> Salida: {salida_1_1}")

assert salida_0_0 == 0 and salida_0_1 == 0 and salida_1_0 == 0 and salida_1_1 == 1
print("\n¡Éxito! La neurona se comporta como una compuerta AND.")