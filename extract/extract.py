mport requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def get_search_page(term, page=1):
    """
    Retorna HTML da página de busca do Kabum para 'term' e 'page'.
    Ajuste a URL se o site usar outra estrutura.
    """
    # URL exemplo (ajuste caso o site use outra estrutura)
    url = f"https://www.kabum.com.br/busca/{term}?page_number={page}"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.text

def extract_product_links_from_search(html, base_url="https://www.kabum.com.br"):
    soup = BeautifulSoup(html, "lxml")
    links = []
    # seletor genérico: procurar por tags <a> com href que contenham '/produto/' ou '/produto/'
    for a in soup.select("a[href]"):
        href = a["href"]
        if "/produto/" in href or "/produto" in href or "/produto/" in href.lower():
            full = urljoin(base_url, href)
            links.append(full)
    # fallback: procurar por links das classes de listagem (ajuste conforme HTML)
    if not links:
        for a in soup.select(".productCard a[href]"):
            links.append(urljoin(base_url, a["href"]))
    # deduplicar mantendo ordem
    seen = set()
    uniq = []
    for l in links:
        if l not in seen:
            uniq.append(l); seen.add(l)
    return uniq

def extrair_produto(url):
    """
    Extrai campos principais de uma página de produto.
    Retorna dict com: nome, preco (string), categoria (string), avaliacao (string), disponibilidade (string), url.
    """
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # Nome do produto: testar seletores com fallback
    nome = None
    nome_selectors = [
        "h1.product-name",         # exemplo hipotético
        "h1#product-name",
        "h1",
        ".product-title",
        ".prateleira-titulo"       # coloque mais se identificar no site
    ]
    for sel in nome_selectors:
        tag = soup.select_one(sel)
        if tag and tag.get_text(strip=True):
            nome = tag.get_text(strip=True)
            break

    # Preço: várias possibilidades (inteiro + centavos separados)
    preco = None
    preco_selectors = [
        ".price", 
        ".product-price__value",
        ".preco .valor", 
        ".price__SalesPrice", 
        ".sku-best-price"
    ]
    for sel in preco_selectors:
        tag = soup.select_one(sel)
        if tag:
            preco = tag.get_text(" ", strip=True)
            break

    # Categoria: breadcrumb
    categoria = None
    try:
        crumbs = [c.get_text(strip=True) for c in soup.select(".breadcrumb a, .breadcrumb li, .product-breadcrumb a")]
        if crumbs:
            categoria = " > ".join(crumbs[-2:]) if len(crumbs) >= 2 else crumbs[-1]
    except Exception:
        categoria = None

    # Avaliação (rating)
    avaliacao = None
    rating_selectors = [
        ".rating .value", 
        ".product-review__rating",
        ".stars", 
        ".rating-average"
    ]
    for sel in rating_selectors:
        tag = soup.select_one(sel)
        if tag:
            avaliacao = tag.get_text(" ", strip=True)
            break

    # Disponibilidade
    disponibilidade = None
    if soup.select_one(".buy-button") or soup.select_one(".add-to-cart"):
        disponibilidade = "Em estoque"
    elif soup.select_one(".unavailable") or soup.select_one(".out-of-stock"):
        disponibilidade = "Indisponível"
    else:
        # tentar detectar texto explicito
        text = soup.get_text(" ", strip=True).lower()
        if "indisponível" in text or "esgotado" in text or "sem estoque" in text:
            disponibilidade = "Indisponível"
        else:
            disponibilidade = "Possivelmente em estoque"

    return {
        "nome": nome,
        "preco": preco,
        "categoria": categoria,
        "avaliacao": avaliacao,
        "disponibilidade": disponibilidade,
        "url": url
    }

def crawl_search(term, pages=1, delay=(1,2)):
    """
    Faz crawl das primeiras 'pages' páginas de busca e extrai produtos.
    delay: tupla (min,max) segundos entre requisições aos produtos.
    """
    produtos = []
    for p in range(1, pages+1):
        html = get_search_page(term, page=p)
        links = extract_product_links_from_search(html)
        print(f"[page {p}] {len(links)} links encontrados")
        for link in links:
            try:
                produto = extrair_produto(link)
                produtos.append(produto)
            except Exception as e:
                print("Erro ao extrair", link, e)
            time.sleep(random.uniform(*delay))
    return produtos