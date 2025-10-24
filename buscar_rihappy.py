import requests
from barcode import Code128
from barcode.writer import ImageWriter

# Input do usuário
busca = input("Digite o nome ou código do produto: ")

# Endpoint GraphQL da RiHappy
url = "https://www.rihappy.com.br/_v/segment/graphql/v1"

# Payload filtrando apenas produtos vendidos e entregues pela RiHappy
payload = {
    "operationName": "productSearchV3",
    "variables": {
        "query": busca,
        "map": "vendido-por,ft",
        "fullText": busca,
        "from": 0,
        "to": 20,
        "orderBy": "OrderByScoreDESC",
        "facetsBehavior": "default",
        "hiddenUnavailableItems": False,
        "selectedFacets": [
            {"key": "vendido-por", "value": "rihappy"}
        ]
    },
    "extensions": {
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "efcfea65b452e9aa01e820e140a5b4a331adfce70470d2290c08bc4912b45212",
            "sender": "vtex.store-resources@0.x",
            "provider": "vtex.search-graphql@0.x"
        }
    }
}

res = requests.post(url, json=payload)
data = res.json()

products = data.get("data", {}).get("productSearch", {}).get("products", [])

if not products:
    print("Nenhum produto encontrado.")
else:
    for produto in products:
        nome = produto.get("productName", "sem nome")
        codigo_interno = produto.get("productReference", "sem código interno")
        items = produto.get("items", [])
        imagens = items[0].get("images", []) if items else []
        
        if imagens:
            imagem_produto = imagens[0].get("imageUrl", "sem imagem")
        else:
            imagem_produto = "sem imagem"
        
        # Pegar EAN do primeiro item
        if items and "ean" in items[0]:
            ean = items[0]["ean"]
        else:
            ean = "sem EAN"

        print("\n--- Produto encontrado ---")
        print(f"Nome: {nome}")
        print(f"EAN: {ean}")
        print(f"Código interno: {codigo_interno}")
        print(f"Imagem do produto: {imagem_produto}")

        # Gerar código de barras a partir do código interno
        if codigo_interno != "sem código interno":
            barcode_image = f"{codigo_interno}.png"
            Code128(codigo_interno, writer=ImageWriter()).write(open(barcode_image, "wb"))
            print(f"Código de barras gerado: {barcode_image}")
        else:
            print("Não foi possível gerar código de barras (código interno ausente).")

print("\nPesquisa finalizada! 😎")