import pandas as pd
import re
import unicodedata
from datetime import datetime

def remover_acentos(texto):
    if not texto:
        return None
    texto = unicodedata.normalize("NFKD", texto)
    return re.sub(r'[^A-Z0-9 ]', '', texto.upper())

def padronizar_categoria(cat):
    if not cat:
        return None
    cat = cat.upper()
    if "SMARTPHONE" in cat or "CELULAR" in cat:
        return "CELULAR"
    if "NOTEBOOK" in cat or "LAPTOP" in cat:
        return "NOTEBOOK"
    return cat

def parse_price(preco):
    if not preco:
        return None
    preco = preco.replace("R$", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(preco)
    except:
        return None

def transformar_lista(lista):
    transformados = []
    data_coleta = datetime.now().strftime("%Y-%m-%d")
    
    for item in lista:
        transformados.append({
            "NOME": remover_acentos(item.get("nome")),
            "PRECO": parse_price(item.get("preco")),
            "CATEGORIA": padronizar_categoria(item.get("categoria")),
            "AVALIACAO": item.get("avaliacao"),
            "DISPONIBILIDADE": remover_acentos(item.get("disponibilidade")),
            "DATA_COLETA": data_coleta
        })
    return pd.DataFrame(transformados)
