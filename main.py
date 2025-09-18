from extract import extrair_api
from transform import transformar_dados

def main():
    termo = "notebook"   # termo de busca
    limite = 20          # quantos anúncios buscar

    # 1) Extrair
    raw = extrair_api(termo, limite)

    # 2) Transformar
    df = transformar_dados(raw)

    # 3) Exportar para CSV
    df.to_csv(f"resultado_{termo}.csv", index=False, encoding="utf-8-sig")

    # Também pode exportar para Excel
    df.to_excel(f"resultado_{termo}.xlsx", index=False)

    print("Arquivos gerados com sucesso!")

if __name__ == "__main__":
    main()