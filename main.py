from extract.extract import extrair_kabum
from transform.clean import transformar_dados

def main():
    termo = "notebook"
    limite = 10

    # 1) Extrair
    raw = extrair_kabum(termo, limite)

    # 2) Transformar
    df = transformar_dados(raw)

    # 3) Exportar
    df.to_csv(f"kabum_{termo}.csv", index=False, encoding="utf-8-sig")
    df.to_excel(f"kabum_{termo}.xlsx", index=False)

    print("Arquivos gerados com sucesso!")

if __name__ == "__main__":
    main()
