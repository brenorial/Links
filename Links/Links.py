import customtkinter as ctk
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import threading
import time

# URLs dos sites a serem verificados
urls = [
    "http://10.80.8.23:4200/login",
    "http://10.80.8.23/ppd/",
    "http://10.69.112.15:8080/oviyam2/",
    "http://suporte.riosaude.rio.br/",
    "http://10.69.112.15:8080/vitai/pages/login.do",
]

def check_website(url):
    options = Options()
    options.add_argument('--headless')  # Execução sem interface gráfica
    navegador = webdriver.Chrome(options=options)
    
    try:
        navegador.set_page_load_timeout(10)  # Timeout de 10 segundos para carregamento da página
        navegador.get(url)
        time.sleep(5)  # Permanece na página por 5 segundos
        return "O site está acessível"
    except (WebDriverException, TimeoutException):
        return "O site não está acessível"
    finally:
        navegador.quit()

def verificar_sites():
    for url in urls:
        status = check_website(url)
        # Atualiza a UI em tempo real
        app.update_status(url, status)
        time.sleep(1)  # Espera um segundo entre cada verificação

def start_verification_thread():
    # Inicia a verificação em uma thread separada para evitar congelamento da UI
    thread = threading.Thread(target=verificar_sites)
    thread.start()

class VerificadorSitesApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x300")
        self.root.title("Verificador de Sites")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Label do título
        self.title_label = ctk.CTkLabel(root, text="Verificador de Links", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=5)

        # Botão para verificar
        self.check_button = ctk.CTkButton(root, text="Verificar", command=start_verification_thread)
        self.check_button.pack(pady=20)

        # Inicializa os labels para resultados
        self.result_labels = {}
        for idx, url in enumerate(urls):
            label = ctk.CTkLabel(root, text=f"{url}: Aguardando verificação...", font=("Arial", 14))
            label.pack(pady=5)
            self.result_labels[url] = label

    def update_status(self, url, status):
        self.result_labels[url].configure(text=f"{url}: {status}")

# Configuração da aplicação principal
root = ctk.CTk()
app = VerificadorSitesApp(root)
root.mainloop()
