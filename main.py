from extract.extract import extrair_dados
from transform.transform import transformar_lista
from load.load import carregar_dados

def main():
    termo = "placa-de-video"
    limite = 20

    print("Extraindo dados da KaBuM …")
    raw = extrair_dados(limite=limite)
    print(f"{len(raw)} produtos extraídos.")

    df = transformar_lista(raw)
    print("Transformados (primeiros ~5):")
    print(df.head())

    carregar_dados(df)
    print("CSV gerado com sucesso.")

if __name__ == "__main__":
    main()
