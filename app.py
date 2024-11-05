from flask import Flask, request, jsonify
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from flask_cors import CORS  # Importar CORS para habilitarlo

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

def setup_driver():
    options = Options()
    options.headless = True  # Activa el modo sin encabezado
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Inicializar ChromeDriver en modo sin encabezado
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

@app.route('/upload_json', methods=['POST'])
def upload_json():
    # Recibir JSON desde la solicitud
    app.logger.info("Solicitud recibida en /upload_json")
    messages = request.get_json()
    app.logger.info(f"Contenido del JSON recibido: {messages}")
    
    if not messages:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Configuración del driver de Selenium para WhatsApp Web
    driver = setup_driver()

    try:
        # Abre WhatsApp Web
        driver.get("https://web.whatsapp.com")
        app.logger.info("Esperando para escanear el código QR...")
        time.sleep(50)  # Tiempo para escanear el código QR

        # Enviar los mensajes
        for item in messages:
            phone = item['phone']
            message = item['message']
            driver.get(f"https://web.whatsapp.com/send?phone={phone}&text={message}")
            time.sleep(10)  # Espera a que se cargue la página

            # Hacer clic en el botón de enviar
            send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            send_button.click()
            time.sleep(5)  # Esperar un momento antes de enviar el siguiente mensaje

        return jsonify({"status": "Mensajes enviados exitosamente"}), 200
    
    except Exception as e:
        app.logger.error(f"Error al enviar mensajes: {e}")
        return jsonify({"error": str(e)}), 500
    
    finally:
        driver.quit()

import os

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
