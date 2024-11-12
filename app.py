from flask import Flask, request, jsonify
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

def setup_driver():
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")

    # Inicializar ChromeDriver en modo sin cabeza
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        app.logger.error(f"Error al inicializar el driver: {e}")
        raise

@app.route('/upload_json', methods=['POST'])
def upload_json():
    app.logger.info("Solicitud recibida en /upload_json")
    messages = request.get_json()
    app.logger.info(f"Contenido del JSON recibido: {messages}")

    if not messages:
        return jsonify({"error": "No JSON data provided"}), 400

    # Validación de estructura de JSON
    for item in messages:
        if 'phone' not in item or 'message' not in item:
            return jsonify({"error": "Cada entrada debe tener 'phone' y 'message'"}), 400

    driver = setup_driver()

    try:
        # Abre WhatsApp Web
        driver.get("https://web.whatsapp.com")
        app.logger.info("Esperando para escanear el código QR...")
        WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.XPATH, '//canvas[@aria-label="Escanee este código QR"]'))
        )

        for item in messages:
            phone = item['phone']
            message = item['message']
            driver.get(f"https://web.whatsapp.com/send?phone={phone}&text={message}")

            # Espera a que el botón de enviar esté presente
            send_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
            )
            send_button.click()
            time.sleep(5)  # Pausa opcional para asegurar el envío

        return jsonify({"status": "Mensajes enviados exitosamente"}), 200

    except Exception as e:
        app.logger.error(f"Error al enviar mensajes: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        driver.quit()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
