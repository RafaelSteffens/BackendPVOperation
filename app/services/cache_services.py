import json
from ..extensions import db, redis_client

empreendimentosGD_collection = db["empreendimentosGD"]

def cache_services():
    redis_client.flushdb()
    savePlants()
    saveFilters()
    saveCoordenadas()
    saveStatistics()

def savePlants():
    try: 
        page = 1
        per_page = 50
        skip = (page - 1) * per_page
        filtros = {}

        cursor = empreendimentosGD_collection.find(filtros, {"_id": 0}).skip(skip).limit(per_page)
        total = empreendimentosGD_collection.count_documents(filtros)

        payload = {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
            "filters_applied": filtros,
            "data": list(cursor)
        }

        redis_client.set("plants_page_1", json.dumps(payload, default=str))

    except Exception as e:
        print("Exception:", str(e))

def saveFilters():
    try: 
        filtros = {}

        payload = {
            "SigUF": empreendimentosGD_collection.distinct("SigUF"),
            "SigAgente": empreendimentosGD_collection.distinct("SigAgente", filtros)
        }

        redis_client.set("filters", json.dumps(payload))
    except Exception as e:
        print("Exception: ", str(e))  

def saveCoordenadas():
    try: 
        filtros = {}

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
        coordenadas = [doc["coord"] for doc in cursor]

        redis_client.set("coordenadas", json.dumps(list(coordenadas)))
    except Exception as e:
        print("Exception:", str(e))

def saveStatistics():
    try: 
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

        payload = {
            "por_estado": adicionar_percentual(por_estado),
            "por_distribuidora": adicionar_percentual(por_distribuidora),
            "total_geral": total_geral 
        }

        redis_client.set("statistics", json.dumps(payload))
    except Exception as e:
        print("Exception:", str(e))
