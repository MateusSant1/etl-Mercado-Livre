import pandas as pd
import requests

def resolver_categoria(category_id: str) -> str:
    """
    Converte o código da categoria (ex: 'MLB1652') em nome legível (ex: 'Notebooks').
    Faz uma chamada à API de categorias.
    """
    if not category_id:
        return "Não informada"
    url = f"https://api.mercadolibre.com/categories/{category_id}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json().get("name", "Desconhecida")
    except Exception:
        return "Erro ao buscar"

def transformar_dados(raw_list: list) -> pd.DataFrame:
    """
    Recebe a lista bruta da API e transforma em DataFrame organizado.
    """
    df = pd.DataFrame(raw_list)

    # Selecionar só os campos relevantes
    campos = ["id", "title", "price", "available_quantity", 
              "category_id", "condition", "permalink", "sold_quantity"]
    df = df[campos]

    # Renomear colunas para português
    df = df.rename(columns={
        "id": "produto_id",
        "title": "produto",
        "price": "preco_brl",
        "available_quantity": "estoque",
        "condition": "condicao",
        "permalink": "link",
        "sold_quantity": "vendidos"
    })

    # Converter tipos
    df["preco_brl"] = pd.to_numeric(df["preco_brl"], errors="coerce")
    df["estoque"] = pd.to_numeric(df["estoque"], errors="coerce")
    df["vendidos"] = pd.to_numeric(df["vendidos"], errors="coerce")

    # Adicionar nome da categoria
    df["categoria"] = df["category_id"].apply(resolver_categoria)

    # Reordenar colunas
    ordem = ["produto_id", "produto", "preco_brl", "estoque", "vendidos", 
             "condicao", "categoria", "link"]
    return df[ordem]