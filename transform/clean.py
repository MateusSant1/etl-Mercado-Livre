import pandas as pd

def transformar_dados(lista_dados)
    
    dados_transformados = []

    for item in lista_dados:
        preco_formatado = None
        if item.get('preco'):
            preco_formatado = (
                item['preco']
                .replace("R$","")
                .replace(".", "")
                .replace(",", ".")
                .strip()
            )

        dados_transformados.append({
            "nome": item.get("nome"),
            "preco": float(preco_formatado) if preco_formatado else None,
            "link": item.get("link"),
            "imagem": item.get("imagem")
        })

    return dados_transformados
