from flask import Blueprint, jsonify
from app.extensions import db
from ..extensions import redis_client
import json

bp = Blueprint("estatisticas", __name__)
empreendimentosGD_collection = db["empreendimentosGD"]

@bp.route("/api/estatisticas", methods=["GET"])
def estatisticas():
    cached = redis_client.get("statistics")
    if cached:
        print("tem cacheeeee", cached)
        return jsonify(json.loads(cached))

    por_estado = list(empreendimentosGD_collection.aggregate([
        {"$group": {"_id": "$SigUF", "potencia_total": {"$sum": "$MdaPotenciaInstaladaKW"}}},
        {"$sort": {"potencia_total": -1}}
    ]))
    
    por_distribuidora = list(empreendimentosGD_collection.aggregate([
        {"$group": {"_id": "$SigAgente", "potencia_total": {"$sum": "$MdaPotenciaInstaladaKW"}}},
        {"$sort": {"potencia_total": -1}}
    ]))


    total_geral = sum(item['potencia_total'] for item in por_estado)  
    
    def adicionar_percentual(lista):
        for item in lista:
            item['percentual'] = round((item['potencia_total'] / total_geral) * 100, 1) if total_geral > 0 else 0
        return lista

    por_estado_com_percent = adicionar_percentual(por_estado)
    por_distribuidora_com_percent = adicionar_percentual(por_distribuidora)

    return jsonify({
        "por_estado": por_estado_com_percent,
        "por_distribuidora": por_distribuidora_com_percent,
        "total_geral": total_geral 
    })
