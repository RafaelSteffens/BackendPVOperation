from flask import Blueprint, jsonify
from app.extensions import db

bp = Blueprint("estatisticas", __name__)
ANEEL_EMPREEDIMENTOS_COLLECTION = db["empreendimentosGD"]

@bp.route("/api/estatisticas", methods=["GET"])
def estatisticas():
    por_estado = list(ANEEL_EMPREEDIMENTOS_COLLECTION.aggregate([
        {"$group": {"_id": "$SigUF", "potencia_total": {"$sum": "$MdaPotenciaInstaladaKW"}}},
        {"$sort": {"potencia_total": -1}}
    ]))

    por_distribuidora = list(ANEEL_EMPREEDIMENTOS_COLLECTION.aggregate([
        {"$group": {"_id": "$SigAgente", "potencia_total": {"$sum": "$MdaPotenciaInstaladaKW"}}},
        {"$sort": {"potencia_total": -1}}
    ]))

    return jsonify({
        "por_estado": por_estado,
        "por_distribuidora": por_distribuidora
    })
