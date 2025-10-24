from flask import Flask, render_template, request
from buscar_rihappy import buscar_produto

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    produtos = []
    if request.method == "POST":
        termo = request.form.get("termo")
        produtos = buscar_produto(termo)
    return render_template("index.html", produtos=produtos)

if __name__ == "__main__":
    app.run(debug=True)
