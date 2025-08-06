from flask import  request, jsonify
from ...extensions import redis_client
import json
from app.extensions import db

empreendimentosGD_collection = db["empreendimentosGD"]


def list_filters_services():
    uf = request.args.get("SigUF")
    city = request.args.get("NomMunicipio")

    filters = {}

    if uf:
        filters["SigUF"] = uf
    if city:
        filters["NomMunicipio"] = city

    if not filters:
        cached = redis_client.get("filters")
        if cached:
            return jsonify(json.loads(cached))

    return jsonify({
        "SigUF": empreendimentosGD_collection.distinct("SigUF"),
        "NomMunicipio": empreendimentosGD_collection.distinct("NomMunicipio", {"SigUF": uf}) if uf else [],
        "SigAgente": empreendimentosGD_collection.distinct("SigAgente", filters) 
    })
