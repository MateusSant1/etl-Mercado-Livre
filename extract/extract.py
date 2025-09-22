from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import time

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # rodar sem abrir janela
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def extrair_dados(limite=200):
    url = "https://www.kabum.com.br/hardware/placa-de-video-vga"
    driver = setup_driver()
    driver.get(url)

    wait = WebDriverWait(driver, 15)
    time.sleep(3)  # aguarda JS inicial

    produtos = []

    # === 1) PRIMEIRA TENTATIVA: SELETORES FIXOS ===
    try:
        cards = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.productCard"))
        )
        print(f"✔ Seletores fixos funcionaram: {len(cards)} produtos encontrados.")
    except:
        cards = []
        print("⚠ Nenhum produto encontrado com seletores fixos.")
    
    # === 2) FALLBACK DINÂMICO ===
    if not cards:
        print("⚠ Tentando detectar seletor dinamicamente...")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        dynamic_cards = []
        for div in soup.find_all("div"):
            # Heurística: divs que têm preço dentro
            if div.find(string=re.compile(r"R\$")):
                dynamic_cards.append(div)
        if dynamic_cards:
            print(f"✔ Seletor dinâmico encontrado: {len(dynamic_cards)} produtos.")
            cards = dynamic_cards
        else:
            print("❌ Não foi possível detectar seletor de produtos.")
    
    # === 3) EXTRAÇÃO DOS DADOS ===
    for card in cards[:limite]:
        try:
            nome = (
                card.find("span", class_=re.compile("nameCard")).get_text(strip=True)
                if hasattr(card, "find")
                else card.find_element(By.CSS_SELECTOR, "span.nameCard").text
            )
        except:
            nome = None

        try:
            preco = (
                card.find("span", class_=re.compile("priceCard")).get_text(strip=True)
                if hasattr(card, "find")
                else card.find_element(By.CSS_SELECTOR, "span.priceCard").text
            )
        except:
            preco = None

        try:
            link = (
                card.find("a")["href"]
                if hasattr(card, "find")
                else card.find_element(By.TAG_NAME, "a").get_attribute("href")
            )
        except:
            link = None

            if not nome or not preco:
                continue

        # Esses campos podem ser tratados depois na transform
        produtos.append({
            "nome": nome,
            "preco": preco,
            "categoria": "Hardware",  # fixo por enquanto
            "avaliacao": None,
            "disponibilidade": "Em estoque" if preco else "Indisponível",
            "link": link,
        })

    driver.quit()
    return produtos
