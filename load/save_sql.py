import csv

def carregar_dados(lista_dados, arquivo="produtos.csv"):
    if not lista_dados:
        return

    with open(arquivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nome", "preco", "link", "imagem"])
        writer.writeheader()
        writer.writerows(lista_dados)