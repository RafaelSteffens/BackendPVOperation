from flask import Blueprint, jsonify, current_app

from app.services.saveEmpreendimentosInBD import importar_csv
from app.extensions import db
import pandas as pd

bp = Blueprint('main', __name__)


@bp.route('/api/searchAneelBD')
def add_cliente():
    importar_csv()
    return jsonify({"mensagem": "Dados inseridos com sucesso no MongoDB!"}), 200



@bp.route('/ping-db')
def ping_db():
    try:
        empreendimentoGD_collections = db['empreendimentosGD'].count_documents({})
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