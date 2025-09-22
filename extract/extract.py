from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def extrair_dados(limite=20):
    print("Iniciando ETL da KaBuM com Selenium...")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.kabum.com.br/computadores/notebooks")  # Categoria notebooks

    # Esperar até que os produtos carreguem
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.productCard")))

    produtos = driver.find_elements(By.CSS_SELECTOR, "div.productCard")
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

        data.append({
            "nome": nome,
            "preco": preco,
            "link": link
        })

    driver.quit()
    return pd.DataFrame(data)


if __name__ == "__main__":
    df = extrair_dados(limite=20)
    print(df.head())
    df.to_csv("kabum_notebooks.csv", index=False, encoding="utf-8-sig")
    print("CSV gerado com sucesso!")
