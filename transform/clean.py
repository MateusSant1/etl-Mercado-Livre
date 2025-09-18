import pandas as pd

def transformar_dados(raw_data: list[dict]) -> pd.DataFrame:
    """
    Transforma lista de dicionários em DataFrame pandas,
    fazendo ajustes básicos.
    """

    df = pd.DataFrame(raw_data)

    # Limpeza simples do preço (remover R$, converter para float se possível)
    if "preco" in df.columns:
        df["preco"] = df["preco"].str.replace("R$", "", regex=False).str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
        df["preco"] = pd.to_numeric(df["preco"], errors="coerce")

    return df
