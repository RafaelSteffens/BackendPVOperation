# app/extensions.py
import pymongo
from flask import current_app

client = None
db = None

# collections
empreendimentosGD_collection = None


def init_mongo(app):
    global client, db
    global empreendimentosGD_collection

    try:
        client = pymongo.MongoClient(app.config['MONGO_URI'])
        db = client.bdaneel
        
    except pymongo.errors.ConfigurationError:
        app.logger.error("Erro na URI do MongoDB.")
        raise
