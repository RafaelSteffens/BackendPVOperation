import pymongo
from pymongo import ASCENDING, DESCENDING
from flask_redis import FlaskRedis

client = None
db = None
redis_client = None
empreendimentosGD_collection = None


def init_mongo(app):
    global client, db
    global empreendimentosGD_collection

    try:
        client = pymongo.MongoClient(app.config['MONGO_URI'], maxPoolSize=200, minPoolSize=10)
        db = client.bdaneel

        empreendimentosGD_collection = db["empreendimentosGD_collection"]

        
        existing = [idx["name"] for idx in empreendimentosGD_collection.list_indexes()]

        def safe_create(spec, name):
            if name not in existing:
                empreendimentosGD_collection.create_index(spec, name=name)

        safe_create([
            ("SigUF", ASCENDING),
            ("NomMunicipio", ASCENDING),
            ("SigAgente", ASCENDING),
            ("NomTitularEmpreendimento", ASCENDING),
            ("MdaPotenciaInstaladaKW", DESCENDING)
        ], "idx_filtros_completo")

        safe_create([("SigAgente", ASCENDING), ("MdaPotenciaInstaladaKW", ASCENDING)], "idx_group_agente")
        safe_create([("SigUF", ASCENDING), ("MdaPotenciaInstaladaKW", ASCENDING)], "idx_group_estado")

    except pymongo.errors.ConfigurationError:
        app.logger.error("Erro na URI do MongoDB.")
        raise


def init_redis(app):
    global redis_client
    try:
        redis_client = FlaskRedis(app)
        redis_client.ping()
    except Exception as err:
        print(f"[EXCEPTION REDIS] : {err}")
        redis_client = None