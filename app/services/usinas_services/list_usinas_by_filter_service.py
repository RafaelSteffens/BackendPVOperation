from flask import request, jsonify
from ...extensions import redis_client
import json
from app.extensions import db

empreendimentosGD_collection = db["empreendimentosGD"]

def list_usinas_by_filter_service():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))
    skip = (page - 1) * per_page

    filters = {}
    filter_fields = ["SigUF", "NomMunicipio", "SigAgente", "NomTitularEmpreendimento"]
    for field in filter_fields:
        value = request.args.get(field)
        if value:
            filters[field] = {"$regex": value, "$options": "i"}

    if not filters and page == 1:
        cached_data = redis_client.get("plants_page_1")
        if cached_data:
            return jsonify(json.loads(cached_data))  

    cursor = empreendimentosGD_collection.find(filters, {"_id": 0}).skip(skip).limit(per_page)
    total = empreendimentosGD_collection.count_documents(filters)

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total + per_page - 1) // per_page,
        "filters_applied": filters,
        "data": list(cursor)
    })
