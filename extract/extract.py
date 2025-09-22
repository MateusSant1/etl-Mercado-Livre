from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


def extrair_dados(limite: int = 20):
    """
    Extrai dados de produtos da KaBuM usando Selenium (renderiza JS).
    Retorna lista de dicionários crus.
    """
    url = "https://www.kabum.com.br/hardware/placa-de-video-vga"

    # Configuração do navegador (headless = sem abrir janela)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    driver.get(url)
    time.sleep(5)  # espera JS carregar

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Cards de produto
    cards = soup.select("div.productCard")  
    resultados = []

    for card in cards[:limite]:
        # Nome
        nome_tag = card.select_one("span.nameCard")
        nome = nome_tag.get_text(strip=True) if nome_tag else None

        # Preço
        preco_tag = card.select_one("span.priceCard")
        preco = preco_tag.get_text(strip=True) if preco_tag else None

        # Link
        link_tag = card.find("a", href=True)
        link = "https://www.kabum.com.br" + link_tag["href"] if link_tag else None

        # Imagem
        img_tag = card.find("img", src=True)
        imagem = img_tag["src"] if img_tag else None

        # Disponibilidade
        text_card = card.get_text(" ", strip=True).lower()
        if "indisponível" in text_card or "esgotado" in text_card:
            disponibilidade = "Indisponível"
        else:
            disponibilidade = "Em estoque"

        resultados.append({
            "nome": nome,
            "preco": preco,
            "link": link,
            "imagem": imagem,
            "disponibilidade": disponibilidade
        })


    return resultados
