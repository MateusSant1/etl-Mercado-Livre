import requests
from bs4 import BeautifulSoup

def extrair_kabum(termo: str, limite: int = 20):
    """
    Extrai produtos da KaBuM com base no termo buscado.
    Retorna lista de dicionários com dados crus.
    """

    url = f"https://www.kabum.com.br/hardware/placa-de-video-vga"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise exception (f"Erro ao acessar a página")
    

    soup = BeautifulSoup(resp.text, "html.parser")

    

    produtos = []


    cards = soup.select("div.productCard")
    for card in cards:
        nome = card.select_one("span.nameCard").get_text(strip=True) if card.select_one("span.nameCard") else None
        preco = card.select_one("span.priceCard").get_text(strip=True) if card.select_one("span.priceCard") else None
        link = "https://www.kabum.com.br" + card.a["href"] if card.a else None
        imagem = card.img["src"] if card.img else None

        produtos.append({
            "nome": nome,
            "preco": preco,
            "link": link,
            "imagem": imagem
        })

    return produtos
