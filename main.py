from extract.extract import extrair_dados
from transform.transform import transformar_dados
from load.load import carregar_dados

def main():
    print("Iniciando ETL da Kabum...")

    # Extract
    dados_extraidos = extrair_dados()
    print(f"Extraídos {len(dados_extraidos)} produtos.")

    # Transform
    dados_transformados = transformar_dados(dados_extraidos)
    print("Transformados:", dados_transformados[:3], "...")  # mostra só os 3 primeiros

    # Load
    carregar_dados(dados_transformados)
    print("Dados salvos em produtos.csv com sucesso!")

if __name__ == "__main__":
    main()