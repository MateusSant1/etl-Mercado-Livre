import pandas as pd

def parse_price(text):
    if not text:
        return None
    # limpa “R$”, pontos de milhar e troca virgula por ponto decimal
    t = text.replace("R$", "").strip()
    t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except:
        return None

def transformar_lista(raw_list):
    """
    Recebe lista de produtos crus, retorna lista transformada com tipos adequados.
    """
    dados = []
    for item in raw_list:
        preco_num = parse_price(item.get("preco"))
        dados.append({
            "nome": item.get("nome"),
            "preco": preco_num,
            "link": item.get("link"),
            "imagem": item.get("imagem"),
            "avaliacao": item.get("avaliacao"),
            "disponivel": True if item.get("disponibilidade") == "Em estoque" else False
        })
    return pd.DataFrame(dados)
