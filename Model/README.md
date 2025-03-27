#  Klasifikasi Organik & Anorganik

##  Tentang Proyek

Model ini dikembangkan untuk mengklasifikasikan data menjadi kategori organik dan anorganik berdasarkan fitur tabular. Model telah dilatih menggunakan Neural Network (Sequential Model) dan disimpan dalam format `.pkl` (Joblib) dan `.h5` (Keras) agar dapat digunakan oleh tim Backend dengan Express.js.

##  Struktur Direktori

Berikut adalah struktur file dalam repository ini:

```
/
├── models/
│   ├── model.pkl           # Model dalam format Joblib
│   ├── model.h5            # Model dalam format Keras
│   ├── preprocessing.pkl   # Parameter preprocessing
├── notebooks/
│   ├── Model_Klasifikasi.ipynb   # Notebook pelatihan model
├── requirements.txt        # Daftar dependency Python
└── README.md               # Dokumentasi ini
```

## ⚙️ Instalasi & Persiapan

Sebelum menjalankan model, pastikan telah menginstal dependensi yang diperlukan.

1.  Buat virtual environment (Opsional):

    ```bash
    python -m venv venv
    source venv/bin/activate   # Mac/Linux
    venv\Scripts\activate      # Windows
    ```

2.  Instal dependensi:

    ```bash
    pip install -r requirements.txt
    ```

    Isi `requirements.txt`:

    ```
    numpy
    joblib
    tensorflow
    keras
    scikit-learn
    ```

3.  Pastikan model dan preprocessing tersedia di folder `models/`.

##  Cara Menggunakan Model

Tim Backend dapat menggunakan model ini dalam Express.js dengan library `@tensorflow/tfjs-node` (untuk `.h5`) atau joblib (untuk `.pkl`).

###  Menggunakan Model `.pkl` dengan Python

```python
import numpy as np
import joblib

# Load model dan preprocessing
model = joblib.load('models/model.pkl')
preprocessing = joblib.load('models/preprocessing.pkl')

# Contoh input data (HARUS sesuai format pelatihan)
sample_input = np.array([[0.5, 0.8, 0.3]])  # Gantilah dengan input asli

# Prediksi
prediction = model.predict(sample_input)
label = (prediction > 0.5).astype(int)
print("Predicted Label:", label)
```

## Menggunakan Model `.h5` dalam Express.js

Untuk Backend menggunakan Node.js, install library berikut:

```bash
npm install @tensorflow/tfjs-node
```

Kemudian, gunakan kode berikut di Express.js:

```javascript
const tf = require('@tensorflow/tfjs-node');

(async () => {
    const model = await tf.loadLayersModel('file://models/model.h5');

    // Contoh input (HARUS sesuai format pelatihan)
    const inputTensor = tf.tensor2d([[0.5, 0.8, 0.3]], [1, 3]);
    const prediction = model.predict(inputTensor);
    prediction.print();
})();
```

## Troubleshooting

1.  Model tidak bisa di-load di Express.js?

    ✔️ Pastikan model dalam format `.h5` dan di-load dengan `@tensorflow/tfjs-node`.

2.  Error input shape tidak sesuai?

    ✔️ Pastikan jumlah fitur input sama dengan jumlah fitur saat pelatihan.

3.  Prediksi tidak sesuai harapan?

    ✔️ Pastikan preprocessing (standarisasi/min-max scaling) dilakukan sama seperti saat pelatihan.

## Kesimpulan

* Model ini tersedia dalam `.pkl` dan `.h5`.
* Gunakan joblib (Python) untuk `.pkl` dan `@tensorflow/tfjs-node` (Node.js) untuk `.h5`.
* Pastikan input data sesuai preprocessing yang digunakan saat pelatihan.
* Dokumentasi ini dapat diperbarui jika ada perubahan pada model atau backend.

Jangan lupa untuk menghubungi tim ML jika ada pertanyaan atau kendala!
