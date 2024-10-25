import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Función para descargar el archivo JSON desde Google Drive
def download_json_from_google_drive(file_id):
    # URL modificada para descargar el archivo
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    response.raise_for_status()  # Verifica si la solicitud fue exitosa
    return response.json()  # Esto debería funcionar ahora con un JSON válido

# Especifica la ruta al chromedriver
service = Service(executable_path='C:/Users/julia/Desktop/chromedriver-script/chromedriver-win64/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Abre WhatsApp Web
driver.get("https://web.whatsapp.com")

# Esperar tiempo suficiente para escanear el código QR manualmente (ajusta el tiempo si es necesario)
print("Esperando para que escanees el código QR...")
time.sleep(30)  # Espera 30 segundos o ajusta según necesites

# ID del archivo en Google Drive
file_id = '1eb8GRs8u6eCGkh1YiIKHTC-CevonC5Z1'  # Reemplaza esto con tu ID de archivo
messages = download_json_from_google_drive(file_id)

# Enviar los mensajes
for item in messages:
    phone = item['phone']
    message = item['message']
    
    # Abrir el chat de WhatsApp
    driver.get(f"https://web.whatsapp.com/send?phone={phone}&text={message}")
    time.sleep(10)  # Esperar a que se cargue la página

    # Hacer clic en el botón de enviar
    send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
    send_button.click()
    time.sleep(5)  # Esperar un momento antes de enviar el siguiente mensaje

# Cierra el driver
driver.quit()
