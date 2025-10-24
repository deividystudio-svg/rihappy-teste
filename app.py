from flask import Flask, render_template, request
import requests
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
import base64

app = Flask(__name__)

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

        # Gerar código de barras em memória
        barcode_base64 = None
        if codigo_interno != "sem código interno":
            buffer = BytesIO()
            Code128(codigo_interno, writer=ImageWriter()).write(buffer)
            barcode_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        resultados.append({
            "nome": nome,
            "codigo_interno": codigo_interno,
            "imagem": imagem_produto,
            "ean": ean,
            "barcode": barcode_base64
        })

    return resultados

@app.route("/", methods=["GET", "POST"])
def index():
    produtos = []
    if request.method == "POST":
        termo = request.form.get("termo")
        produtos = buscar_produto(termo)
    return render_template("index.html", produtos=produtos)

if __name__ == "__main__":
    app.run(debug=True)
