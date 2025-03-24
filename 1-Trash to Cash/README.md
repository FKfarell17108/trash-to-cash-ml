# 1 - Trash to Cash

Model ini untuk proyek Trash to Cash. Repositori ini berisi klasifikasi berbasis Neural Network untuk mengidentifikasi sampah organik dan anorganik. Model ini dirancang untuk keperluan pengujian dan integrasi backend. Dataset bersumber dari Roboflow (CC BY 4.0).

## Isi Folder

- `src/inference.py`: Skrip inferensi untuk prediksi gambar.
- `src/nn_sampah_classifier.h5`: Model Neural Network yang telah dilatih (unduh via Google Drive: [tambahkan link setelah upload]).
- `images/`: Folder untuk menyimpan gambar uji.
- `notebook/klasifikasi_sampah.ipynb`: Notebook Colab untuk pelatihan dan pengembangan.
- `requirements.txt`: Daftar dependensi Python.
- `README.md`: Dokumentasi ini.
- `LICENSE`: File lisensi MIT.

## Cara Penggunaan

1.  **Instal Dependensi:**

    ```bash
    pip install -r requirements.txt
    ```

2.  Pastikan Git LFS terinstal jika mengunduh `nn_sampah_classifier.h5` dari repositori:

    ```bash
    git lfs install
    ```

3.  **Siapkan Gambar dan Model:**

    -   Tambahkan gambar ke folder `images/` (contoh: `1.jpg`, `2.jpeg`).
    -   Gambar akan diresize ke 64x64 piksel untuk klasifikasi.
    -   Pastikan `nn_sampah_classifier.h5` ada di folder `src/`.

4.  **Jalankan Inferensi:**

    ```bash
    python src/inference.py
    ```

    -   Output berupa JSON dengan prediksi dan probabilitas untuk setiap gambar.

## Spesifikasi Input

-   **Klasifikasi Biner:**
    -   Gambar diresize ke 64x64 piksel dan diflatten menjadi vektor 12,288 elemen (RGB).
    -   Normalisasi piksel ke rentang \[0, 1].
    -   Format gambar: `.jpg`, `.jpeg`, atau `.png`.

## Struktur Output

-   **Klasifikasi Biner:**

    ```json
    {
        "prediction": "Organik",
        "probability": 0.87
    }
    ```

    atau

    ```json
    {
        "prediction": "Anorganik",
        "probability": 0.32
    }
    ```

## Modelling

-   **Arsitektur:** Neural Network dengan 3 layer:
    -   Input: 12,288 elemen (flatten dari 64x64x3).
    -   Hidden Layer 1: 128 neuron, aktivasi ReLU.
    -   Hidden Layer 2: 64 neuron, aktivasi ReLU.
    -   Output: 1 neuron, aktivasi Sigmoid (threshold 0.5).
-   **Pelatihan:**
    -   Optimizer: Adam (learning rate 0.001).
    -   Loss: Binary Crossentropy.
    -   Epoch: Maksimal 15.
    -   Batch Size: 32.
    -   Target Akurasi: Minimal 85% pada data test.

## Integrasi Backend

-   **Format Model:**
    -   Model disimpan dalam format HDF5 (`nn_sampah_classifier.h5`), kompatibel dengan TensorFlow/Keras.
    -   Backend dapat memuat model menggunakan `tf.keras.models.load_model()`.
-   **API Endpoint:** Gunakan Flask untuk membuat API:
    -   Setup Flask:
        ```bash
        pip install flask
        ```
    -   `app.py`:
        ```python
        from flask import Flask, request, jsonify
        import cv2
        import numpy as np
        import tensorflow as tf
        import os

        app = Flask(__name__)
        model = tf.keras.models.load_model('src/nn_sampah_classifier.h5')

        def preprocess_image(image_path, target_size=(64, 64)):
            img = cv2.imread(image_path)
            if img is None:
                return None
            img = cv2.resize(img, target_size)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = img.flatten() / 255.0
            return img

        def predict_image_nn(image_path, model):
            img = preprocess_image(image_path)
            if img is None:
                return {"error": "Gambar tidak dapat dibaca"}
            img = img.reshape(1, -1)
            prediction = model.predict(img, verbose=0)[0][0]
            predicted_class = 'Anorganik' if prediction < 0.5 else 'Organik'
            return {"prediction": predicted_class, "probability": float(prediction)}

        @app.route('/predict', methods=['POST'])
        def predict():
            if 'file' not in request.files:
                return jsonify({"error": "Tidak ada file yang diunggah"}), 400
            file = request.files['file']
            temp_path = "temp_image.jpg"
            file.save(temp_path)
            result = predict_image_nn(temp_path, model)
            os.remove(temp_path)
            return jsonify(result)

        if __name__ == '__main__':
            app.run(host='0.0.0.0', port=5000)
        ```
    -   Jalankan API:
        ```bash
        python app.py
        ```
    -   Pengujian dengan cURL:
        ```bash
        curl -X POST -F "file=@images/1.jpg" http://localhost:5000/predict
        ```

## Penggunaan oleh Frontend

-   Endpoint: `POST /predict`
-   Input: `form-data` dengan key `file` berisi gambar.
-   Output: JSON dengan `prediction` dan `probability`.
-   Frontend dapat mengirimkan gambar via HTTP request (contoh dengan JavaScript):

    ```javascript
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    fetch('http://localhost:5000/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => console.log(data));
    ```

## Dependensi (`requirements.txt`)

-   tensorflow==2.10.0
-   numpy
-   opencv-python
-   flask

## Lisensi

MIT License

Copyright (c) 2025 CC25-SF039

Lihat file `LICENSE` untuk detail. Dataset dari Roboflow di bawah CC BY 4.0.

## Atribusi

-   Dataset: Klasifikasi Sampah Organik dan Anorganik oleh Skripsi Aji (CC BY 4.0).
-   Link: https://universe.roboflow.com/skripsi-aji/klasifikasi-sampah-organik-dan-anorganik/dataset/35

## Catatan

-   **File Besar:** `nn_sampah_classifier.h5` mungkin >100 MB. Unduh dari Google Drive: [tambahkan link].
-   **Versi TensorFlow:** Disarankan 2.10.0 untuk kompatibilitas. Sesuaikan jika perlu.
-   **Kontak:** farellkurniawan17108@gmail.com.