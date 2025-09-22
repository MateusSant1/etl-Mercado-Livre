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
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def extrair_dados(limite=200):
    url = "https://www.kabum.com.br/busca/notebook"
    driver = setup_driver()
    driver.get(url)

    wait = WebDriverWait(driver, 15)
    time.sleep(3)  # aguarda JS inicial

    produtos = []
    vistos = set()  # <-- CONJUNTO PARA DEDUPE

    # 1️⃣ Seletores fixos
    try:
        cards = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.productCard"))
        )
        print(f"✔ Seletores fixos funcionaram: {len(cards)} produtos encontrados.")
    except:
        cards = []
        print("⚠ Nenhum produto encontrado com seletores fixos.")
    
    # 2️⃣ Fallback dinâmico (opcional)
    if not cards:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        dynamic_cards = []
        for div in soup.find_all("div"):
            if div.find(string=re.compile(r"R\$")):
                dynamic_cards.append(div)
        if dynamic_cards:
            print(f"✔ Seletor dinâmico encontrado: {len(dynamic_cards)} produtos.")
            cards = dynamic_cards

    # 3️⃣ Extração com dedupe
    for card in cards:
        if len(produtos) >= limite:
            break
        try:
            nome = (
                card.find("span", class_=re.compile("nameCard")).get_text(strip=True)
                if hasattr(card, "find")
                else card.find_element(By.CSS_SELECTOR, "span.nameCard").text
            )
        except:
            continue

        try:
            preco = (
                card.find("span", class_=re.compile("priceCard")).get_text(strip=True)
                if hasattr(card, "find")
                else card.find_element(By.CSS_SELECTOR, "span.priceCard").text
            )
        except:
            continue

        if not nome or not preco:
            continue

        try:
            link = (
                card.find("a")["href"]
                if hasattr(card, "find")
                else card.find_element(By.TAG_NAME, "a").get_attribute("href")
            )
        except:
            link = None

        # ✅ DEDUPLICAÇÃO AQUI
        chave = link or (nome.strip().lower(), preco.strip())
        if chave in vistos:
            continue  # já coletado
        vistos.add(chave)

        produtos.append({
            "nome": nome.strip(),
            "preco": preco.strip(),
            "categoria": "Notebook",
            "avaliacao": None,
            "disponibilidade": "Em estoque" if preco else "Indisponível",
            "link": link,
        })

    driver.quit()
    print(f"Produtos únicos extraídos: {len(produtos)}")
    return produtos
