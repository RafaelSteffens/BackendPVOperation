from flask import Blueprint, jsonify, current_app

from app.services.saveEmpreendimentosInBD import importar_csv
from app.extensions import db

bp = Blueprint('main', __name__)

# @bp.route("/atualizaDados")
# def LogicaParaAtualizarDados():
#     baixa  novo arquivo.
#     importar_csv()


@bp.route('/searchAneelBD')
def add_cliente():
    print("============================ENTROU NA ROTA==================================")
    importar_csv()
    return jsonify({"mensagem": "Dados inseridos com sucesso no MongoDB!"})


@bp.route('/ping-db')
def ping_db():
    try:
        # Testa a collection 'empreendimentoGD'
        empreendimentoGD_collections = db['empreendimentoGD'].count_documents({})
        return jsonify({
            "status": "success",
            "message": "Conexão ativa",
            "docs_count": empreendimentoGD_collections
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500