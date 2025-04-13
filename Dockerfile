# Gunakan image Python resmi sebagai base
FROM python:3.9-slim

# Set working directory di dalam container
WORKDIR /app

# Salin requirements.txt dan instal dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file proyek
COPY . .

# Expose port untuk Flask
EXPOSE 5000

# Perintah untuk menjalankan aplikasi
CMD ["python", "API/app.py"]
