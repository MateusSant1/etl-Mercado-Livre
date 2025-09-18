import pandas as pd

def parse_price(text):
    if not text:
        return None
    # limpa “R$”, pontos de milhar e troca vírgula por ponto
    t = text.replace("R$", "").strip()
    t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except:
        return None

def transformar_lista(raw_list):
    """
    Converte a lista crua em DataFrame limpo.
    """
    dados = []
    for item in raw_list:
        preco_num = parse_price(item.get("preco"))
        dados.append({
            "nome": item.get("nome"),
            "preco": preco_num,
            "link": item.get("link"),
            "imagem": item.get("imagem"),
            "disponivel": True if item.get("disponibilidade") == "Em estoque" else False
        })
    return pd.DataFrame(dados)
