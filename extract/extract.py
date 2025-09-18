# transform.py
import pandas as pd
import re

def parse_price(text):
    if not text:
        return None
    # limpar texto: manter números, vírgula e ponto
    t = re.sub(r"[^\d,\.]", "", text)
    # trocar vírgula por ponto quando apropriado
    t = t.replace(".", "").replace(",", ".") if t.count(",") <= 1 else t.replace(",", "")
    try:
        return float(t)
    except:
        return None

def transformar_lista(raw_list):
    df = pd.DataFrame(raw_list)
    # normalizar colunas
    if "preco" in df.columns:
        df["preco_brl"] = df["preco"].apply(parse_price)
    else:
        df["preco_brl"] = None
    df["disponivel"] = df["disponibilidade"].apply(lambda x: True if isinstance(x, str) and "estoque" in x.lower() else False)
    # renomear
    df = df.rename(columns={"nome":"produto"})
    cols = ["produto","preco_brl","categoria","avaliacao","disponivel","url"]
    for c in cols:
        if c not in df.columns:
            df[c] = None
    return df[cols]
