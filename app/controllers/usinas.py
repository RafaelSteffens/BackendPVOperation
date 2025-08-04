from flask import Blueprint, Response, request, jsonify, stream_with_context
import orjson
from ..extensions import redis_client
import json

from app.extensions import db


bp = Blueprint("usinas", __name__)
empreendimentosGD_collection = db["empreendimentosGD"]


@bp.route("/api/usinas", methods=["GET"])
def listar_usinas():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))
    skip = (page - 1) * per_page

    filtros = {}
    campos_filtro = ["SigUF", "NomMunicipio", "SigAgente", "NomTitularEmpreendimento"]
    for campo in campos_filtro:
        valor = request.args.get(campo)
        if valor:
            filtros[campo] = {"$regex": valor, "$options": "i"}

    if not filtros and page == 1:
        cached_data = redis_client.get("plants_page_1")
        if cached_data:
            return jsonify(json.loads(cached_data))  

    cursor = empreendimentosGD_collection.find(filtros, {"_id": 0}).skip(skip).limit(per_page)
    total = empreendimentosGD_collection.count_documents(filtros)

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total + per_page - 1) // per_page,
        "filters_applied": filtros,
        "data": list(cursor)
    })


@bp.route("/api/usinas/filtros", methods=["GET"])
def listar_filtros():
    uf = request.args.get("SigUF")
    municipio = request.args.get("NomMunicipio")

    filtros = {}

    if uf:
        filtros["SigUF"] = uf
    if municipio:
        filtros["NomMunicipio"] = municipio

    if not filtros:
        cached = redis_client.get("filters")
        if cached:
            return jsonify(json.loads(cached))

    return jsonify({
        "SigUF": empreendimentosGD_collection.distinct("SigUF"),
        "NomMunicipio": empreendimentosGD_collection.distinct("NomMunicipio", {"SigUF": uf}) if uf else [],
        "SigAgente": empreendimentosGD_collection.distinct("SigAgente", filtros) 
    })


@bp.route("/api/CoordUsinas", methods=["GET"])
def coord_usinas():
    try:
        campos_filtro = ["SigUF", "NomMunicipio", "SigAgente", "NomTitularEmpreendimento"]
        filtros = {}
        for campo in campos_filtro:
            valor = request.args.get(campo)
            if valor:
                filtros[campo] = {"$regex": f"^{valor}", "$options": "i"}

        if not filtros:
            cached = redis_client.get("coordenadas")
            if cached:
                return jsonify(json.loads(cached))

        pipeline = [
            {"$match": filtros},
            {"$sort": {"MdaPotenciaInstaladaKW": -1}},  
            {"$project": {
                "_id": 0,
                "coord": [
                    {"$round": [{"$arrayElemAt": ["$location.coordinates", 0]}, 6]},
                    {"$round": [{"$arrayElemAt": ["$location.coordinates", 1]}, 6]}
                ]
            }},
            {"$limit": 33333}
        ]
        cursor = empreendimentosGD_collection.aggregate(pipeline, allowDiskUse=True)

        def generate():
            yield '['
            first = True
            batch = []
            for i, doc in enumerate(cursor, start=1):
                batch.append(doc["coord"])
                if len(batch) >= 500:
                    if not first:
                        yield ','
                    else:
                        first = False
                    yield orjson.dumps(batch).decode()[1:-1]
                    batch = []
            if batch:
                if not first:
                    yield ','
                yield orjson.dumps(batch).decode()[1:-1]
            yield ']'

        return Response(stream_with_context(generate()), mimetype="application/json")

    except Exception as e:
        return Response(f"Erro no servidor: {str(e)}", status=500, mimetype="text/plain")



