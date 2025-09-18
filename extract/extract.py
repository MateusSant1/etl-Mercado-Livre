import requests
from bs4 import BeautifulSoup

def extrair_kabum(termo: str, limite: int = 20):
    """
    Extrai produtos da KaBuM com base no termo buscado.
    Retorna lista de dicionários com dados crus.
    """

    url = f"https://www.kabum.com.br/busca/{termo}"
    headers = {"User-Agent": "Mozilla/5.0"}

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    produtos_html = soup.find_all("div", class_="productCard", limit=limite)

    resultados = []
    for produto in produtos_html:
        nome = produto.find("span", class_="nameCard")
        preco = produto.find("span", class_="priceCard")
        avaliacao = produto.find("span", class_="reviewCard")

        resultados.append({
            "nome": nome.get_text(strip=True) if nome else "N/A",
            "preco": preco.get_text(strip=True) if preco else "N/A",
            "avaliacao": avaliacao.get_text(strip=True) if avaliacao else "Sem avaliação",
            "categoria": termo,  # podemos assumir como a busca feita
            "disponibilidade": "Indisponível" if "indisponível" in produto.get_text().lower() else "Em estoque"
        })

    return resultados
