import numpy as np

class NaiveBayesClassifier:
    
    def __init__(self, laplace_smoothing=1):
        """
        Inicializa el clasificador.
        
        Args:
            laplace_smoothing (int): El 'alpha' para el suavizado.
                                     Previene probabilidades de cero.
        """
        self.laplace_alpha = laplace_smoothing
        self.priors = {}            # P(Clase)
        self.likelihoods = {}       # P(Palabra | Clase)
        self.vocab = set()          # Todas las palabras únicas vistas
        self.classes = set()        # {'Spam', 'No Spam'}

    def fit(self, X_train, y_train):
        """
        Entrena el modelo calculando las probabilidades
        a priori y las verosimilitudes.
        
        Args:
            X_train (list of str): Lista de "documentos" (correos).
            y_train (list of str): Lista de etiquetas ('Spam', 'No Spam').
        """
        print("--- 1. Entrenando el modelo Naïve-Bayes ---")
        
        num_docs = len(X_train)
        
        # --- a. Calcular Probabilidades a Priori P(Clase) ---
        for label in y_train:
            self.classes.add(label)
        
        for cls in self.classes:
            # P(Clase) = (Num. de docs en esta clase) / (Total docs)
            self.priors[cls] = y_train.count(cls) / num_docs

        print(f"  Clases encontradas: {self.classes}")
        print(f"  Probabilidades a Priori P(Clase): {self.priors}")
        
        # --- b. Calcular Verosimilitudes P(Palabra | Clase) ---
        # Contadores de palabras: { 'Spam': {'oferta': 5, ...}, 'No Spam': {...} }
        word_counts = {cls: {} for cls in self.classes}
        # Contador total de palabras por clase
        total_words_in_class = {cls: 0 for cls in self.classes}

        # Llenar la vocabulario y los contadores
        for doc, label in zip(X_train, y_train):
            words = doc.split()
            for word in words:
                self.vocab.add(word)
                # Contar palabra en su clase
                word_counts[label][word] = word_counts[label].get(word, 0) + 1
                total_words_in_class[label] += 1
        
        vocab_size = len(self.vocab)
        print(f"  Tamaño del vocabulario: {vocab_size} palabras únicas.")
        
        # Calcular P(Palabra | Clase) con Suavizado de Laplace
        for cls in self.classes:
            self.likelihoods[cls] = {}
            total_count = total_words_in_class[cls]
            
            # P(w|c) = (count(w,c) + alpha) / (total_count(c) + alpha * vocab_size)
            denominator = total_count + self.laplace_alpha * vocab_size
            
            for word in self.vocab:
                count = word_counts[cls].get(word, 0)
                prob = (count + self.laplace_alpha) / denominator
                self.likelihoods[cls][word] = prob

    def predict(self, X_test):
        """
        Predice la clase para un nuevo conjunto de documentos.
        """
        print("\n--- 2. Realizando Predicciones ---")
        predictions = []
        for doc in X_test:
            
            # --- c. Calcular Puntuaciones (en Log-espacio) ---
            # P(Clase | doc) ~ log(P(Clase)) + Suma( log(P(palabra | Clase)) )
            
            scores = {cls: 0.0 for cls in self.classes}
            words = doc.split()
            
            for cls in self.classes:
                # Empezar con el log-prior
                score = np.log(self.priors[cls])
                
                # Sumar los log-likelihoods
                for word in words:
                    if word in self.vocab: # Ignorar palabras no vistas en el entreno
                        score += np.log(self.likelihoods[cls][word])
                
                scores[cls] = score
                
            # --- d. Elegir la clase con la puntuación más alta ---
            best_class = max(scores, key=scores.get)
            predictions.append(best_class)
            
            print(f"  Documento: '{doc}'")
            print(f"    Puntuaciones (log-prob): {scores}")
            print(f"    -> Predicción: {best_class}")

        return predictions

# --- 3. Datos de Entrenamiento y Prueba ---

# Datos de entrenamiento
train_docs = [
    "oferta exclusiva gana dinero gratis",
    "hola amigo como estas",
    "reunion importante manana",
    "premio gratis te espera",
    "informe de ventas"
]
train_labels = ['Spam', 'No Spam', 'No Spam', 'Spam', 'No Spam']

# Datos de prueba
test_docs = [
    "hola te envio el informe",
    "oferta premio gratis ahora"
]

# --- 4. Ejecutar el Clasificador ---

# Crear y entrenar
clf = NaiveBayesClassifier(laplace_smoothing=1)
clf.fit(train_docs, train_labels)

# Predecir
preds = clf.predict(test_docs)