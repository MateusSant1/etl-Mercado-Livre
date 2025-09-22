from extract.extract import extrair_dados
from transform.transform import transformar_lista

def main():
    raw = extrair_dados(limite=200)
    df = transformar_lista(raw)
    print("Transformados:")
    print(df.head())

    # salva CSV
    df = df.drop_duplicates(keep="first")
    df.to_csv("dados_kabum.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    main()
