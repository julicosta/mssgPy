# Usa una imagen base con Python
FROM python:3.11-slim

# Instala dependencias necesarias
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg2 \
    curl \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libgconf-2-4 \
    libxi6 \
    libatk1.0-0 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgtk-3-0 \
    fonts-liberation \
    xdg-utils \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia tu archivo de requisitos
COPY requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt

# Copia tu aplicación
COPY . /app 
WORKDIR /app 

# Comando para ejecutar tu aplicación
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
