from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
from app.extensions import db
from app.models.registroAneel import RegistroAneel
from .cache_services import cache_services

empreendimentosGD_collection = db["empreendimentosGD"]
empreendimentosGD_EXCEPTION_collection = db["empreendimentosGD_EXCEPTION_collection"]

def import_csv_data():
    try:
        empreendimentosGD_collection.drop()
        empreendimentosGD_EXCEPTION_collection.drop()

        reader_csv = pd.read_csv(
            "https://dadosabertos.aneel.gov.br/dataset/5e0fafd2-21b9-4d5b-b622-40438d40aba2/resource/b1bd71e7-d0ad-4214-9053-cbd58e9564a7/download/empreendimento-geracao-distribuida.csv",
            chunksize=50000,
            encoding="latin1",
            sep=";",
            low_memory=False
        )

        futures = [] 
        with ThreadPoolExecutor(max_workers=3) as executor:
            for idx, chunk in enumerate(reader_csv, start=1):
                future = executor.submit(processing_chunk, chunk, idx)
                futures.append(future)

            for future in as_completed(futures):
                future.result()  

        cache_services()

    except Exception as sub_err:
        print(f"[ERRO] Falha ao importar e salvar csv: {sub_err}")


def processing_chunk(chunk, id_chunk):
    try:
        records = chunk.to_dict(orient="records")
        buffer = []

        for row in records:
            try:
                dado = RegistroAneel(**row).dict(by_alias=True)
                buffer.append(dado)

                if len(buffer) >= 5000:
                    empreendimentosGD_collection.insert_many(buffer, ordered=False)
                    buffer.clear()

            except Exception as err:
                print(f"[EXCEPTION] Registro inválido no chunk {id_chunk}: {err}")
                try:
                    row["_erro"] = str(err)
                    row["_chunk"] = id_chunk
                    empreendimentosGD_EXCEPTION_collection.insert_one(row)
                except Exception as sub_err:
                    print(f"[ERRO] Falha ao salvar exceção no chunk {id_chunk}: {sub_err}")
                    continue

        if buffer:
            empreendimentosGD_collection.insert_many(buffer, ordered=False)

    except Exception as e:
        print(f"[ERRO] Falha ao processar chunk {id_chunk}: {e}")





# from flask import Flask, jsonify
# import requests
# import subprocess
# import os
# from datetime import datetime

# MONGO_URI = (
#     "mongodb://localhost:27017/bdaneel"
#     "?connectTimeoutMS=60000"
#     "&socketTimeoutMS=60000"
#     "&maxPoolSize=50"
#     "&waitQueueTimeoutMS=60000"
#     "&serverSelectionTimeoutMS=60000"
# )
# DB_NAME = "bdaneel"
# COLLECTION_NAME = "empreendimentosGD_collection"

# CSV_URL = "https://dadosabertos.aneel.gov.br/dataset/5e0fafd2-21b9-4d5b-b622-40438d40aba2/resource/b1bd71e7-d0ad-4214-9053-cbd58e9564a7/download/empreendimento-geracao-distribuida.csv"

# LOCAL_FILE = "empreendimentosGD.csv"


# def import_csv_data():

#     try:
#         response = requests.get(CSV_URL, stream=True)
#         response.raise_for_status()
        
#         with open(LOCAL_FILE, "wb") as f:
#             for chunk in response.iter_content(chunk_size=1024*1024):  
#                 f.write(chunk)

#         comando = f'''
#         mongoimport --uri "{MONGO_URI}" \
#         --collection {COLLECTION_NAME} \
#         --type csv \
#         --headerline \
#         --file "{LOCAL_FILE}" \
#         --drop
#         '''

#         resultado = subprocess.run(
#             comando,
#             shell=True,
#             check=True,
#             capture_output=True,
#             text=True
#         )

#         os.remove(LOCAL_FILE)

#         return jsonify({"status": "ok", "mensagem": resultado.stdout})

#     except subprocess.CalledProcessError as e:
#         return jsonify({"status": "erro", "detalhes": e.stderr})
#     except Exception as e:
#         return jsonify({"status": "erro", "detalhes": str(e)})