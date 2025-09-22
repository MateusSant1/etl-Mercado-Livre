from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import time


def descobrir_selector(driver, wait):
    """
    Detecta dinamicamente o seletor válido da KaBuM.
    Retorna o primeiro seletor que funcione.
    """
    candidatos = [
        "div[data-testid='product-card']",
        "div.productCard",
        "div.sc-ff8a9791-7",  # classe dinâmica
    ]

    # Testa candidatos conhecidos
    for selector in candidatos:
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
            produtos = driver.find_elements(By.CSS_SELECTOR, selector)
            if produtos:
                print(f"✔ Usando seletor conhecido: {selector}")
                return selector
        except:
            continue

    # Se nenhum funcionar → tenta achar dinamicamente
    print("⚠ Nenhum seletor padrão funcionou, tentando detectar dinamicamente...")
    todos_divs = driver.find_elements(By.CSS_SELECTOR, "div")

    for div in todos_divs:
        try:
            texto = div.text
            if "R$" in texto:  # preço presente
                imagens = div.find_elements(By.TAG_NAME, "img")
                if imagens:
                    print("✔ Seletor dinâmico encontrado!")
                    classes = div.get_attribute("class")
                    if classes:
                        seletor_css = "div." + ".".join(classes.split())
                        print(f"✔ Seletor dinâmico construído: {seletor_css}")
                        return seletor_css
        except:
            continue

    return None


def extrair_dados(limite=20):
    print("Iniciando ETL da KaBuM com Selenium...")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.kabum.com.br/computadores/notebooks")

    wait = WebDriverWait(driver, 20)

    seletor = descobrir_selector(driver, wait)
    if not seletor:
        print("❌ Não foi possível encontrar seletor de produtos.")
        driver.quit()
        return pd.DataFrame()

    produtos = driver.find_elements(By.CSS_SELECTOR, seletor)
    print(f"🔎 {len(produtos)} produtos encontrados.")

    data = []
    for produto in produtos[:limite]:
        try:
            nome = produto.find_element(By.CSS_SELECTOR, "span.nameCard").text
        except:
            nome = None

        try:
            preco = produto.find_element(By.CSS_SELECTOR, "span.priceCard").text
        except:
            preco = None

        try:
            link = produto.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        except:
            link = None

        try:
            imagem = produto.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
        except:
            imagem = None

        data.append({
            "nome": nome,
            "preco": preco,
            "link": link,
            "imagem": imagem
        })

    driver.quit()
    return pd.DataFrame(data)


if __name__ == "__main__":
    df = extrair_dados(limite=20)
    print(df.head())
    df.to_csv("kabum_notebooks.csv", index=False, encoding="utf-8-sig")
    print("CSV gerado com sucesso!")
