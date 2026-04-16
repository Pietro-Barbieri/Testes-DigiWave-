from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://pietro-barbieri:qkIVVDFckjQugYmB@cluster0.jame5bn.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client["digiwave"]
imoveis_col    = db["imoveis"]
localidades_col = db["localidades"]


@app.route("/")
def index():
    return send_from_directory("frontend_build", "index.html")


# ──────────────── IMÓVEIS ────────────────

@app.route("/imoveis", methods=["GET"])
def get_imoveis():
    imoveis = list(imoveis_col.find({}, {"_id": 0}))
    return jsonify(imoveis)


@app.route("/imoveis", methods=["POST"])
def add_imovel():
    novo = request.json
    imovel = {
        "titulo":   novo.get("titulo"),
        "preco":    novo.get("preco"),
        "cidade":   novo.get("cidade"),
        "bairro":   novo.get("bairro"),
        "rua":      novo.get("rua"),
        "endereco": novo.get("endereco"),
        "contato":  novo.get("contato"),
        "imagem":   novo.get("imagem"),
    }
    imoveis_col.insert_one(imovel)
    return jsonify({"message": "ok"})


@app.route("/imoveis/<int:index>", methods=["PUT"])
def update_imovel(index):
    imoveis = list(imoveis_col.find({}, {"_id": 1}))
    if 0 <= index < len(imoveis):
        dados = request.json
        imoveis_col.update_one(
            {"_id": imoveis[index]["_id"]},
            {"$set": {
                "titulo":   dados.get("titulo"),
                "preco":    dados.get("preco"),
                "cidade":   dados.get("cidade"),
                "bairro":   dados.get("bairro"),
                "rua":      dados.get("rua"),
                "endereco": dados.get("endereco"),
                "contato":  dados.get("contato"),
                "imagem":   dados.get("imagem"),
            }}
        )
        return jsonify({"message": "Atualizado"})
    return jsonify({"error": "Não encontrado"}), 404


@app.route("/imoveis/<int:index>", methods=["DELETE"])
def delete_imovel(index):
    imoveis = list(imoveis_col.find({}, {"_id": 1}))
    if 0 <= index < len(imoveis):
        imoveis_col.delete_one({"_id": imoveis[index]["_id"]})
        return jsonify({"message": "Deletado"})
    return jsonify({"error": "Não encontrado"}), 404


# ──────────────── LOCALIDADES ────────────────

@app.route("/localidades", methods=["GET"])
def get_localidades():
    doc = localidades_col.find_one({}, {"_id": 0})
    if not doc:
        doc = {"cidades": [], "bairros": [], "ruas": []}
    return jsonify(doc)


@app.route("/localidades", methods=["PUT"])
def update_localidades():
    dados = request.json
    localidades_col.update_one(
        {},
        {"$set": {
            "cidades": dados.get("cidades", []),
            "bairros": dados.get("bairros", []),
            "ruas":    dados.get("ruas",    []),
        }},
        upsert=True
    )
    return jsonify({"message": "ok"})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)