# Menggunakan versi Python yang ringan
FROM python:3.10-slim

# Menentukan folder kerja di dalam server
WORKDIR /app

# Mengcopy dan menginstall library
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Mengcopy seluruh file kodemu
COPY . .

# Membuka port 8080
EXPOSE 8080

# Menjalankan Gunicorn di port 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
