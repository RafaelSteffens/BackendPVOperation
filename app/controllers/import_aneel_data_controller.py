from flask import Blueprint, jsonify

from ..services.import_save_empreendimentosaneel_bd import import_csv_data
from app.extensions import db

from ..services.cache_services import cache_services

bp = Blueprint('main', __name__)


@bp.route('/api/aneel/import')
def import_aneel_data():
    result = import_csv_data()
    
    if result.get("status") == "error":
        return jsonify({"error": result["message"]}), 500
    
    return jsonify({"mensagem": "Dados inseridos com sucesso no MongoDB!"}), 200



@bp.route('/ping-db')
def ping_db():
    try:
        cache_services()
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