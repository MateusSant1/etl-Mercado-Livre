from extract import crawl_search
from transform import transformar_lista
import pandas as pd

def main():
    termo = "notebook"
    paginas = 1
    produtos = crawl_search(termo, pages=paginas, delay=(1.0, 2.0))
    df = transformar_lista(produtos)
    df.to_csv(f"resultado_kabum_{termo}.csv", index=False, encoding="utf-8-sig")
    df.to_excel(f"resultado_kabum_{termo}.xlsx", index=False)
    print("Arquivos salvos:", f"resultado_kabum_{termo}.csv")

if __name__ == "__main__":
    main()