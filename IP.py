from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import socket
import time
import threading

# Função para obter o IP do computador
def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

# Função para fechar o navegador
def close_browser(driver):
    try:
        driver.quit()
        print("Navegador fechado com sucesso.")
    except Exception as e:
        print(f"Erro ao fechar o navegador: {e}")

# Caminho para o seu WebDriver (ajuste conforme necessário)
webdriver_path='C:\\Users\henrique.salvador\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

# Configurar o serviço do ChromeDriver
service = Service(webdriver_path)

# Configurar as opções do Chrome
options = webdriver.ChromeOptions()

# URL da página web no IP específico (ajuste conforme necessário)
target_url = 'http:\\192.168.1.237'  # Substitua pelo URL desejado

# Obter o IP do computador
ip_address = get_ip_address()
print(f"Obtido IP do computador: {ip_address}")

# Inicializar o WebDriver
try:
    driver = webdriver.Chrome(service=service, options=options)
    print("WebDriver inicializado com sucesso.")
except Exception as e:
    print(f"Erro ao inicializar o WebDriver: {e}")

# Iniciar o temporizador para fechar o navegador após 20 segundos
timer = threading.Timer(2, close_browser, [driver])
timer.start()

# Abrir a página web
try:
    driver.get(target_url)
    print(f"Página {target_url} aberta com sucesso.")
except Exception as e:
    print(f"Erro ao abrir a página: {e}")

# Localizar o campo de input pelo atributo name
try:
    input_element = driver.find_element(By.NAME, 'S_IP')
    print("Campo de input localizado com sucesso.")
except Exception as e:
    print(f"Erro ao localizar o campo de input: {e}")

# Inserir o IP no campo de input
try:
    input_element.clear()
    input_element.send_keys(ip_address)
    print(f"IP {ip_address} inserido no campo de input com sucesso.")
except Exception as e:
    print(f"Erro ao inserir o IP no campo de input: {e}")

    # Aguardar alguns segundos se necessário
    time.sleep(2)

# Localizar e clicar no botão Set
try:
    set_button = driver.find_element(By.CSS_SELECTOR, "input[value='Set']")
    set_button.click()
    print("Botão Set clicado com sucesso.")
except Exception as e:
    print(f"Erro ao clicar no botão Set: {e}")

# Aguardar alguns segundos se necessário
# time.sleep(2)

# Localizar e clicar no botão Restart
# try:
#     restart_button = driver.find_element(By.CSS_SELECTOR, "input[value='Restart']")
#     restart_button.click()
#     print("Botão Restart clicado com sucesso.")
# except Exception as e:
#     print(f"Erro ao clicar no botão Restart: {e}")

# Esperar alguns segundos para visualização (opcional)
# time.sleep(2)

# Fechar o navegador
try:
    driver.quit()
    print("Navegador fechado com sucesso.")
except Exception as e:
    print(f"Erro ao fechar o navegador: {e}")

