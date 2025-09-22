import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import time
from transform.transform import normalize_text, parse_price_to_float

def extract_sku_from_link(link):
    """
    Heurística: muitos sites colocam SKU/ID no final da URL (ex: .../produto/12345/nome-do-produto).
    Retorna string identificadora simples (ou None).
    """
    if not link:
        return None
    # pega últimos dígitos da url
    m = re.search(r"(\d{4,})", link)
    if m:
        return m.group(1)
    # fallback: slug da última parte
    last = link.rstrip("/").split("/")[-1]
    if last:
        return last
    return None

def setup_driver(headless=True):
    opts = webdriver.ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

def extrair_dados(limite=200):
    driver = setup_driver(headless=True)
    url = "https://www.kabum.com.br/hardware/placa-de-video-vga"
    driver.get(url)

    wait = WebDriverWait(driver, 20)
    # aguarda algum elemento que contenha preços ou cards
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.productCard")))
    except:
        # fallback: esperar um pouco mais e seguir
        time.sleep(5)

    time.sleep(2)  # garantir JS
    # rolagem para carregar lazy-load (se necessário)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    cards = driver.find_elements(
    By.XPATH, "//div[contains(@class,'productCard') or contains(@class,'card')]"
)
    print(f"Encontrados (DOM) {len(cards)} elementos")

    if not cards:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        possiveis = {tuple(c) for c in [d.get("class") for d in soup.select("div") if d.get("class")]}
        print("⚠ Nenhum card encontrado. Classes disponíveis:", possiveis)

    produtos = []
    vistos_ids = set()   # para SKU/link
    vistos_chaves = set()  # para (nome_normalizado, preco_float)

    for card in cards:
        if len(produtos) >= limite:
            break
        # tenta extrair os campos com robustez
        try:
            nome = None
            try:
                nome = card.find_element(By.CSS_SELECTOR, "span.nameCard").text
            except:
                # alternativa genérica
                nome = card.text.split("\n")[0] if card.text else None

        try:
            estoque = card.find_element(By.XPATH, ".//*[contains(text(),'Esgotado')]")
            disponibilidade = "INDISPONIVEL"
        except:
            disponibilidade = "EM ESTOQUE"

        try:
            link = (
                card.find("a")["href"]
                if hasattr(card, "find")
                else card.find_element(By.TAG_NAME, "a").get_attribute("href")
            )
        except:
            link = None
            try:
                link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            except:
                link = None

            # normalizações
            nome_norm = normalize_text(nome)
            preco_float = parse_price_to_float(preco_text)
            sku = extract_sku_from_link(link)

            # chave de unicidade preferencial: sku ou link
            unique_id = sku or (link or None)
            if unique_id:
                if unique_id in vistos_ids:
                    # já vimos esse produto pelo id/link -> pula
                    continue
            else:
                # fallback: usar (nome_norm, preco_float)
                chave = (nome_norm or "", preco_float)
                if chave in vistos_chaves:
                    continue

        # Esses campos podem ser tratados depois na transform
        produtos.append({
            "nome": nome,
            "preco": preco,
            "categoria": "Hardware",  # fixo por enquanto
            "avaliacao": None,
            "disponibilidade": disponibilidade,
            "link": link,
        })

    driver.quit()
    print(f"{len(produtos)} produtos extraídos (após dedupe no extract).")
    return produtos