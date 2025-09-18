import csv

def carregar_dados(df, arquivo="kabum_produtos.csv"):
    """
    Salva o DataFrame em CSV.
    """
    df.to_csv(arquivo, index=False, encoding="utf-8-sig")
