import requests
from bs4 import BeautifulSoup

def extrair_dados(limite: int = 20):
    """
    Extrai vários itens da listagem da KaBuM, com avaliação se disponível.
    Retorna lista de dicionários com dados crus.
    """
    # Categoria exemplo: placas de vídeo
    url = "https://www.kabum.com.br/hardware/placa-de-video-vga"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    cards = soup.select("div.productCard")  # ou outro seletor de card de produto
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

        # Avaliação (nota) — se houver
        # Tenta alguns seletores possíveis
        avaliacao = None
        rating_tag = card.select_one("span.reviewCard")  # exemplo de seletor que pode existir
        if rating_tag:
            avaliacao = rating_tag.get_text(strip=True)
        else:
            # procurar por outro seletor de avaliação, se existir
            alt_tag = card.select_one(".rating-stars")  # pode variar
            if alt_tag:
                avaliacao = alt_tag.get_text(strip=True)

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
            "avaliacao": avaliacao,
            "disponibilidade": disponibilidade
        })

    return resultados
