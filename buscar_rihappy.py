import requests

def buscar_produto(busca):
    url = "https://www.rihappy.com.br/_v/segment/graphql/v1"
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
    resultados = []

    for produto in products:
        nome = produto.get("productName", "sem nome")
        codigo_interno = produto.get("productReference", "sem código interno")
        items = produto.get("items", [])
        imagens = items[0].get("images", []) if items else []
        imagem_produto = imagens[0].get("imageUrl", "sem imagem") if imagens else "sem imagem"
        ean = items[0].get("ean", "sem EAN") if items else "sem EAN"

        resultados.append({
            "nome": nome,
            "codigo_interno": codigo_interno,
            "imagem": imagem_produto,
            "ean": ean
        })

    return resultados
