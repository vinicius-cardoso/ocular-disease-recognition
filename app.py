import os
import glob
import numpy as np
import pandas as pd
from PIL import Image
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model
from flask import Flask, render_template, request, redirect, url_for

import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limitar uploads a 16MB

# Criar diretório para uploads, se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DATASET_PATH = './dataset/100/'
IMAGE_PATH = './dataset/100/diabetic_retinopathy_100/10003_left.jpeg'
MODEL_PATH = './best_model_custom.keras'

# Getting the names of classes
class_dirs = [d for d in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, d))]

# create data path and their labeles
data = []
labels = []
extensions = ["jpg", "JPG", "jpeg", "JPEG", "png", "PNG", "bmp", "BMP", "gif", "GIF"]

for i in class_dirs:
    class_label = i
    image_files = []
    for ext in extensions:
        # Search for files with each extension and extend the image_files list
        image_files.extend(glob.glob(os.path.join(DATASET_PATH, i, f"*.{ext}")))

    data.extend(image_files)
    labels.extend([class_label] * len(image_files))

# Create a DataFrame with the image paths and labels
df = pd.DataFrame({
    'filename': data,
    'class': labels
})

# Shuffle the dataset by rows
df = df.sample(frac=1)

# Carregar o modelo
model = load_model(MODEL_PATH)

# Convert labels to one-hot encodings
label_encoder = LabelEncoder()
label = label_encoder.fit_transform(df['class'])
df['class'] = label

# check number assigned to each class
# Get the class names and corresponding integer encodings
class_names = label_encoder.classes_
class_numbers = label_encoder.transform(label_encoder.classes_)

diseases_names_dict = {
    'cataract_100': 'Catarata', 
    'diabetic_retinopathy_100': 'Retinopatia Diabética',
    'glaucoma_100': 'Glaucoma',
    'normal_100': 'Normal'
}

class_names = [diseases_names_dict[nome] for nome in class_names]

# Print class names with the assigned numbers
class_dict = dict(zip(class_names, class_numbers))

best_model = load_model(MODEL_PATH)

def classify_single_image(model, image_path, class_labels):
    """
    Classifica uma única imagem usando um modelo treinado.

    Parâmetros:
    - model: Modelo Keras treinado.
    - image_path: Caminho para o arquivo de imagem.
    - class_labels: Lista de rótulos das classes.

    Retorna:
    - predicted_label: O rótulo da classe previsto.
    - probability: Probabilidade da classe prevista.
    """
    # Carregar e pré-processar a imagem
    image = tf.io.read_file(image_path)
    image = tf.image.decode_image(image, channels=3)
    image = tf.image.resize(image, [256, 256])  # Redimensionar para o input do modelo
    image = image / 255.0  # Normalizar para o intervalo [0, 1]
    image = tf.expand_dims(image, axis=0)  # Adicionar dimensão do batch

    # Fazer a previsão
    predictions = model.predict(image)
    predicted_index = np.argmax(predictions[0])  # Índice da maior probabilidade
    probability = predictions[0][predicted_index] * 100  # Probabilidade da classe prevista

    # Rótulo da classe prevista
    predicted_label = class_labels[predicted_index]

    return predicted_label, probability

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" not in request.files:
            return redirect(request.url)

        file = request.files["image"]

        if file.filename == "":
            return redirect(request.url)

        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Classificar a imagem
            predicted_label, probability = classify_single_image(model, filepath, class_names)

            return render_template(
                "index.html",
                uploaded_image=file.filename,
                predicted_label=predicted_label,
                probability=probability,
            )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
