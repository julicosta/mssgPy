import json
import time
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from flask import Flask, request, jsonify
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

@app.route('/upload_json', methods=['POST'])
def upload_json():
    # Recibir JSON desde la solicitud
    messages = request.get_json()
    if not messages:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Configuración del driver de Selenium para WhatsApp Web
    options = Options()
    options.add_argument('--headless')  # Modo headless para servidores
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(executable_path='/path/to/chromedriver')  # Ajusta la ruta de tu chromedriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Abre WhatsApp Web
        driver.get("https://web.whatsapp.com")
        print("Esperando para escanear el código QR...")
        time.sleep(30)  # Tiempo para escanear el código QR

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
        print(f"Error al enviar mensajes: {e}")
        return jsonify({"error": str(e)}), 500
    
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
