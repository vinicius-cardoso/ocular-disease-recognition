import os
import glob
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model

import warnings
warnings.filterwarnings("ignore")

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

def classify_single_image(model, image_path, class_labels):
    """
    Classify a single image using a trained Keras model.

    Parameters:
    - model: Trained Keras model.
    - image_path: Path to the image file to classify.
    - class_labels: List of class labels.

    Returns:
    - predicted_label: The predicted class label.
    - probability: Probability of the predicted class.
    """

    # Load and preprocess the image
    image = tf.io.read_file(image_path)
    image = tf.image.decode_image(image, channels=3)
    image = tf.image.resize(image, [256, 256])  # Resize to match model input
    image = image / 255.0  # Normalize to [0, 1] range
    image = tf.expand_dims(image, axis=0)  # Add batch dimension

    # Predict with the model
    predictions = model.predict(image)
    predicted_index = np.argmax(predictions[0])  # Get the index of the highest probability
    probability = predictions[0][predicted_index] * 100  # Get the probability of the predicted class

    # Get the class label
    predicted_label = class_labels[predicted_index]

    return predicted_label, probability

# Convert labels to one-hot encodings
label_encoder = LabelEncoder()
label = label_encoder.fit_transform(df['class'])
df['class'] = label

# check number assigned to each class
# Get the class names and corresponding integer encodings
class_names = label_encoder.classes_
class_numbers = label_encoder.transform(label_encoder.classes_)

# Print class names with the assigned numbers
class_dict = dict(zip(class_names, class_numbers))

best_model = load_model(MODEL_PATH)
class_names = label_encoder.classes_

# Exemplo de uso
predicted_label, probability = classify_single_image(best_model, IMAGE_PATH, class_names)

print(f"Predicted Label: {predicted_label}")
print(f"Probability: {probability:.2f}%")
