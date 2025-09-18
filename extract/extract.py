import requests

def extrair_api(termo: str, limite: int = 10, token: str = None):
    """
    Extrai dados do Mercado Livre via API.
    
    Parâmetros:
        termo (str): termo de busca (ex: 'notebook')
        limite (int): quantidade de resultados a retornar
        token (str, opcional): Access Token OAuth do Mercado Livre
    
    Retorna:
        dict: resposta JSON da API
    """
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&limit={limite}"

    # Cabeçalhos obrigatórios
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }

    # Se você já tiver token, adiciona no header
    if token:
        headers["Authorization"] = f"Bearer {token}"

    resp = requests.get(url, headers=headers)

    # Levanta erro se algo deu errado (401, 404 etc.)
    resp.raise_for_status()

    return resp.json()
