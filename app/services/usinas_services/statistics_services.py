from flask import  jsonify
from app.extensions import db
from ...extensions import redis_client
import json

empreendimentosGD_collection = db["empreendimentosGD"]

def statistics_services():
    cached = redis_client.get("statistics")
    if cached:
        return jsonify(json.loads(cached))

    def aggregate_by(field):
        return list(empreendimentosGD_collection.aggregate([
            {"$group": {"_id": f"${field}", "potencia_total": {"$sum": "$MdaPotenciaInstaladaKW"}}},
            {"$sort": {"potencia_total": -1}}
        ]))

    def add_percentage_share(data, total):
        for item in data:
            item['percentual'] = round((item['potencia_total'] / total) * 100, 1) if total > 0 else 0
        return data

    by_state = aggregate_by("SigUF")
    by_distributor = aggregate_by("SigAgente")

    grand_total = sum(item['potencia_total'] for item in by_state)

    enriched_state = add_percentage_share(by_state, grand_total)
    enriched_distributor = add_percentage_share(by_distributor, grand_total)

    response = {
        "por_estado": enriched_state,
        "por_distribuidora": enriched_distributor,
        "total_geral": grand_total
    }

    redis_client.set("statistics", json.dumps(response))

    return jsonify(response)
