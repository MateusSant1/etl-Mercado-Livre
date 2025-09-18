import requests

def extrair_api(termo: str, limit: int = 50):
    
    url = "https://api.mercadolibre.com/sites/MLB/search"
    params = {"q": termo, "limit": limit}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()  # dispara erro se a API falhar
    return resp.json().get("results", [])