import numpy as np

# --- 1. Definir el Vocabulario y Modelos Simplificados ---

VOCAB = ['hola', 'mundo', 'adios', '<START>', '<END>'] # <START>/<END> son tokens especiales
VOCAB_INDEX = {word: i for i, word in enumerate(VOCAB)}
N_WORDS = len(VOCAB)

# Modelo de Lenguaje Simple (Probabilidades de Transición) P(W_t | W_{t-1})
# Matriz: T[i, j] = P(Palabra j | Palabra i)
# Filas: Palabra anterior / Columnas: Palabra actual
#            hola mundo adios START END
T = np.array([
    [0.1, 0.7, 0.1, 0.0, 0.1], # hola -> (mundo es probable)
    [0.1, 0.1, 0.7, 0.0, 0.1], # mundo -> (adios es probable)
    [0.3, 0.3, 0.1, 0.0, 0.3], # adios -> (END es probable)
    [0.8, 0.1, 0.1, 0.0, 0.0], # START -> (hola es probable)
    [0.0, 0.0, 0.0, 0.0, 1.0]  # END -> (solo puede quedarse en END)
])
# Convertir a log-probabilidades (más estable numéricamente)
LOG_T = np.log(T + 1e-10) # Añadir epsilon para evitar log(0)

# Puntuaciones Acústicas Simuladas P(Audio_t | W_t)
# (Valores inventados: más alto = mejor "sonó" esa palabra en ese momento)
# Columnas: Tiempo (t=0, t=1, t=2) / Filas: Palabras
#            t=0   t=1   t=2
ACOUSTIC_SCORES = np.array([
    [0.7, 0.1, 0.1], # hola (mejor al principio)
    [0.1, 0.8, 0.1], # mundo (mejor en medio)
    [0.1, 0.1, 0.7], # adios (mejor al final)
    [0.0, 0.0, 0.0], # START (no genera sonido)
    [0.0, 0.0, 0.0]  # END (no genera sonido)
])
LOG_ACOUSTIC = np.log(ACOUSTIC_SCORES + 1e-10)
NUM_STEPS = ACOUSTIC_SCORES.shape[1] # Número de pasos de tiempo

# --- 2. Algoritmo de Viterbi (Adaptado para Palabras) ---
def viterbi_word_recognition(log_acoustic_scores, log_transition_matrix, vocab_map):
    """
    Encuentra la secuencia de palabras más probable usando Viterbi.
    """
    num_steps = log_acoustic_scores.shape[1]
    num_words = log_acoustic_scores.shape[0]
    
    # delta[t, w] = max log-prob de secuencia hasta t terminando en palabra w
    delta = np.full((num_steps, num_words), -np.inf) # Inicializar con log(0)
    # psi[t, w] = palabra anterior más probable que lleva a w en t
    psi = np.zeros((num_steps, num_words), dtype=int)

    # --- Inicialización (t=0) ---
    start_index = vocab_map['<START>']
    for w_idx in range(num_words):
        # Prob = P(W0 | START) + P(Audio0 | W0)  (en log-espacio)
        if w_idx != start_index and w_idx != vocab_map['<END>']:
            delta[0, w_idx] = log_transition_matrix[start_index, w_idx] + \
                              log_acoustic_scores[w_idx, 0]
            psi[0, w_idx] = start_index # El único camino viene de START

    # --- Recursión (t=1 hasta T-1) ---
    for t in range(1, num_steps):
        for w_idx in range(num_words):
             if w_idx == start_index or w_idx == vocab_map['<END>']: continue

             max_log_prob = -np.inf
             best_prev_w_idx = -1

             # Encontrar la mejor palabra anterior
             for prev_w_idx in range(num_words):
                 if prev_w_idx == vocab_map['<END>']: continue # No se puede salir de END

                 # log_prob = delta[t-1, prev_w] + P(W_t=w | W_{t-1}=prev_w)
                 current_log_prob = delta[t-1, prev_w_idx] + \
                                    log_transition_matrix[prev_w_idx, w_idx]

                 if current_log_prob > max_log_prob:
                     max_log_prob = current_log_prob
                     best_prev_w_idx = prev_w_idx

             # delta[t, w] = P(Audio_t | W_t=w) + max_prob_anterior
             delta[t, w_idx] = log_acoustic_scores[w_idx, t] + max_log_prob
             psi[t, w_idx] = best_prev_w_idx

    # --- Terminación ---
    # Considerar la transición a <END>
    end_index = vocab_map['<END>']
    max_log_prob_final = -np.inf
    best_last_word_idx = -1
    for w_idx in range(num_words):
         # log_prob = delta[T-1, w] + P(END | w)
         current_log_prob = delta[num_steps-1, w_idx] + \
                            log_transition_matrix[w_idx, end_index]
         if current_log_prob > max_log_prob_final:
             max_log_prob_final = current_log_prob
             best_last_word_idx = w_idx

    # --- Backtracking ---
    sequence_indices = [0] * num_steps
    sequence_indices[num_steps-1] = best_last_word_idx
    for t in range(num_steps-2, -1, -1):
        sequence_indices[t] = psi[t+1, sequence_indices[t+1]]

    # Convertir índices a palabras
    recognized_sequence = [list(vocab_map.keys())[list(vocab_map.values()).index(idx)]
                           for idx in sequence_indices]

    return recognized_sequence, max_log_prob_final

# --- 3. Ejecutar ---
print("--- Simulando Reconocimiento de Habla (Viterbi) ---")
print("Puntuaciones Acústicas (Log-Prob):")
print(LOG_ACOUSTIC)
print("\nModelo de Lenguaje (Log-Prob Transiciones):")
print(LOG_T)

sequence, log_prob = viterbi_word_recognition(LOG_ACOUSTIC, LOG_T, VOCAB_INDEX)

print(f"\nSecuencia de Palabras Reconocida: {sequence}")
print(f"Log-Probabilidad de la secuencia: {log_prob:.4f}")

# Calcular la secuencia "obvia" solo mirando la acústica
best_acoustic_indices = np.argmax(ACOUSTIC_SCORES[:-2,:], axis=0) # Ignorar START/END
best_acoustic_words = [list(VOCAB_INDEX.keys())[list(VOCAB_INDEX.values()).index(idx)] for idx in best_acoustic_indices]
print(f"\nSecuencia si solo miramos la acústica: {best_acoustic_words}")
print("(Viterbi combina acústica Y lenguaje para encontrar la secuencia global)")