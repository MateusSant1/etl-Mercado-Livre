from extract.extract import extrair_dados
from transform.transform import transformar_lista
from load.load import carregar_dados

def main():
    print("Iniciando ETL da KaBuM com Selenium...")

    # Extract
    raw = extrair_dados(limite=20)
    print(f"{len(raw)} produtos extraídos.")

    # Transform
    df = transformar_lista(raw)
    print("Transformados:")
    print(df.head())

    # Load
    carregar_dados(df)
    print("Arquivos CSV e Excel gerados com sucesso!")

if __name__ == "__main__":
    main()

