from flask import Response, request, jsonify, stream_with_context
import orjson
from ...extensions import redis_client
import json
from app.extensions import db

empreendimentosGD_collection = db["empreendimentosGD"]

def coords_usinas_services():
    try:
        filter_fields = ["SigUF", "NomMunicipio", "SigAgente", "NomTitularEmpreendimento"]
        filters = {}
        for field in filter_fields:
            value = request.args.get(field)
            if value:
                filters[field] = {"$regex": f"^{value}", "$options": "i"}

        if not filters:
            cached = redis_client.get("coordenadas")
            if cached:
                return jsonify(json.loads(cached))

        pipeline = [
            {"$match": filters},
            {"$sort": {"MdaPotenciaInstaladaKW": -1}},  
            {"$project": {
                "_id": 0,
                "coord": [
                    {"$round": [{"$arrayElemAt": ["$location.coordinates", 0]}, 6]},
                    {"$round": [{"$arrayElemAt": ["$location.coordinates", 1]}, 6]}
                ]
            }},
            {"$limit": 27777}
        ]

        cursor = empreendimentosGD_collection.aggregate(pipeline, allowDiskUse=True)

        def generate():
            yield '['
            first = True
            buffer = []
            for i, doc in enumerate(cursor, start=1):
                buffer.append(doc["coord"])
                if len(buffer) >= 500:
                    if not first:
                        yield ','
                    else:
                        first = False
                    yield orjson.dumps(buffer).decode()[1:-1]
                    buffer = []
            if buffer:
                if not first:
                    yield ','
                yield orjson.dumps(buffer).decode()[1:-1]
            yield ']'

        return Response(stream_with_context(generate()), mimetype="application/json")

    except Exception as e:
        return Response(f"Erro no servidor: {str(e)}", status=500, mimetype="text/plain")
