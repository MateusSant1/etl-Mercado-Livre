import pandas as pd
import re
import unicodedata
from datetime import datetime

def remover_acentos(texto):
    """Remove acentos e caracteres não alfanuméricos, mantém apenas letras/números/espaco"""
    if not texto:
        return None
    texto = unicodedata.normalize("NFKD", texto)
    # Remove acentos, pontuação e deixa em UPPER
    texto = re.sub(r'[^A-Z0-9 ]', '', texto.upper())
    # Remove espaços duplicados e aparas
    return re.sub(r'\s+', ' ', texto).strip()

def padronizar_categoria(cat):
    """Normaliza categorias para CELULAR / NOTEBOOK / OUTROS"""
    if not cat:
        return None
    cat = remover_acentos(cat)
    if "SMARTPHONE" in cat or "CELULAR" in cat:
        return "CELULAR"
    if "NOTEBOOK" in cat or "LAPTOP" in cat:
        return "NOTEBOOK"
    return cat

def parse_price(preco):
    """Limpa valores monetários (R$, pontos, espaços) e converte para float"""
    if not preco:
        return None
    preco = re.sub(r"[^\d,]", "", preco)   # remove tudo exceto números e vírgula
    try:
        return float(preco.replace(",", "."))  # converte para float
    except ValueError:
        return None

def transformar_lista(lista):
    """
    Transforma lista de dicionários brutos em DataFrame limpo e deduplicado
    - Remove acentos
    - Padroniza categorias
    - Deduplica por NOME + PRECO
    """
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

    df = pd.DataFrame(transformados)

    # 🔹 Deduplicação forte
    if not df.empty:
        # 1️⃣ Deduplica por NOME + PRECO (mais seguro)
        df = df.drop_duplicates(subset=["NOME", "PRECO"], keep="first")

        # 2️⃣ Deduplica por NOME caso preço não esteja preenchido
        df = df.drop_duplicates(subset=["NOME"], keep="first")

        # 3️⃣ Limpeza final de espaços invisíveis (garantia extra)
        df["NOME"] = df["NOME"].str.replace(r"\s+", " ", regex=True).str.strip()
        df["CATEGORIA"] = df["CATEGORIA"].str.replace(r"\s+", " ", regex=True).str.strip()

    return df
