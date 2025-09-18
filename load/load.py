import csv

def carregar_dados(df, arquivo_csv="kabum_produtos.csv", arquivo_excel="kabum_produtos.xlsx"):
    """
    Salva os dados em CSV e Excel.
    """
    df.to_csv(arquivo_csv, index=False, encoding="utf-8-sig")
    df.to_excel(arquivo_excel, index=False)
