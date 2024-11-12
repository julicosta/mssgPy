from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, jsonify
import logging

app = Flask(__name__)

# Función para configurar el driver de Selenium
def setup_driver():
    options = Options()
    options.headless = True  # Ejecutar en modo headless
    options.add_argument("--no-sandbox")  # Permite ejecutar el navegador sin restricciones
    options.add_argument("--disable-dev-shm-usage")  # Evita problemas con memoria compartida
    options.add_argument("--disable-gpu")  # Deshabilita la GPU (no se necesita en un entorno sin cabeza)
    options.add_argument("--window-size=1920x1080")  # Tamaño de ventana (necesario en headless)
    options.add_argument("--remote-debugging-port=9222")  # Evita problemas con DevTools

    try:
        app.logger.info("Inicializando ChromeDriver...")
        # Usando ChromeDriverManager para instalar el driver compatible
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        app.logger.info("ChromeDriver inicializado exitosamente.")
        return driver
    except Exception as e:
        app.logger.error(f"Error al inicializar el driver: {e}")
        raise

# Ruta de ejemplo para verificar el funcionamiento del driver
@app.route('/upload_json', methods=['POST'])
def upload_json():
    try:
        driver = setup_driver()
        # Aquí puedes usar el driver para interactuar con el navegador
        driver.get("http://www.google.com")
        return jsonify({"status": "success", "message": "Página cargada correctamente."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Configuración de logging para mejor visibilidad de los errores
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=8080)
