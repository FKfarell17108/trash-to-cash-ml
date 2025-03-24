import cv2
import numpy as np
import tensorflow as tf
import os
import json

# Load model
model = tf.keras.models.load_model('nn_sampah_classifier.h5')

# Preprocessing function
def preprocess_image(image_path, target_size=(64, 64)):
    img = cv2.imread(image_path)
    if img is None:
        return None
    img = cv2.resize(img, target_size)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.flatten() / 255.0  # Normalisasi
    return img

# Prediction function
def predict_image_nn(image_path, model):
    img = preprocess_image(image_path)
    if img is None:
        return {"error": "Gambar tidak dapat dibaca"}
    img = img.reshape(1, -1)
    prediction = model.predict(img, verbose=0)[0][0]
    predicted_class = 'Anorganik' if prediction < 0.5 else 'Organik'
    return {"prediction": predicted_class, "probability": float(prediction)}

# Main execution
if __name__ == "__main__":
    image_dir = "images/"
    if not os.path.exists(image_dir):
        print(f"Folder {image_dir} tidak ditemukan!")
    else:
        for img_file in os.listdir(image_dir):
            if img_file.endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(image_dir, img_file)
                result = predict_image_nn(img_path, model)
                print(f"Hasil untuk {img_file}:")
                print(json.dumps(result, indent=2))