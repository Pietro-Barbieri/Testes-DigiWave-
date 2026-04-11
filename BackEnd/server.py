from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DB_FILE = "db.json"


def read_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)


@app.route("/")
def index():
    return send_from_directory("frontend_build", "index.html")


@app.route("/imoveis", methods=["GET"])
def get_imoveis():
    return jsonify(read_db())


@app.route("/imoveis", methods=["POST"])
def add_imovel():
    data = read_db()
    novo = request.json

    imovel = {
        "titulo": novo.get("titulo"),
        "preco": novo.get("preco"),
        "cidade": novo.get("cidade"),
        "contato": novo.get("contato"),
        "imagem": novo.get("imagem")
    }

    data.append(imovel)
    write_db(data)

    return jsonify({"message": "ok"})


@app.route("/imoveis/<int:index>", methods=["DELETE"])
def delete_imovel(index):
    data = read_db()

    if 0 <= index < len(data):
        data.pop(index)
        write_db(data)
        return jsonify({"message": "Deletado"})

    return jsonify({"error": "Erro"}), 404


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)