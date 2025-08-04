from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor


import pandas as pd
from app.extensions import db
from app.models.registroAneel import RegistroAneel
from datetime import datetime
from .cache_services import cache_services

empreendimentosGD_collection = db["empreendimentosGD"]
empreendimentosGD_EXCEPTION_collection = db["empreendimentosGD_EXCEPTION_collection"]

def importar_csv():
    try:
        print("=================================== INÍCIO DA IMPORTAÇÃO ===========================")
        horainicial  =datetime.now()
        empreendimentosGD_collection.drop()

        leitorCSV = pd.read_csv(
            "https://dadosabertos.aneel.gov.br/dataset/5e0fafd2-21b9-4d5b-b622-40438d40aba2/resource/b1bd71e7-d0ad-4214-9053-cbd58e9564a7/download/empreendimento-geracao-distribuida.csv",
            chunksize=50000,
            encoding="latin1",
            sep=";",
            low_memory=False
        )

        # with ProcessPoolExecutor(max_workers=7) as executor:
        #     for idx, chunk in enumerate(leitorCSV, start=1):
        #         executor.submit(processar_chunk, chunk, idx)
        with ThreadPoolExecutor(max_workers=7) as executor:
            for idx, chunk in enumerate(leitorCSV, start=1):
                executor.submit(processar_chunk, chunk, idx)



        horafinal =datetime.now()
        tempo_total = horafinal - horainicial
        print(f"Tempo total: {tempo_total.total_seconds()/60:.2f} minutos")

        cache_services()
        horafinal_cache =datetime.now()
        tempo_total_cache = horafinal_cache - horafinal
        print(f"Tempo total: {tempo_total_cache.total_seconds()/60:.2f} minutos")

    except Exception as sub_err:
        print(f"[ERRO] Falha ao importar e salvar csv: {sub_err}")


def processar_chunk(chunk, idx):
    try:
        records = chunk.to_dict(orient="records")
        buffer = []
        
        inseridos = 0

        for row in records:
            try:
                dado = RegistroAneel(**row).dict(by_alias=True)
                buffer.append(dado)

                if len(buffer) >= 5000:
                    empreendimentosGD_collection.insert_many(buffer, ordered=False)
                    inseridos += len(buffer)
                    buffer.clear()

            except Exception as err:
                print(f"[EXCEPTION] Registro inválido no chunk {idx}: {err}")
                try:
                    row["_erro"] = str(err)
                    row["_chunk"] = idx
                    empreendimentosGD_EXCEPTION_collection.insert_one(row)
                except Exception as sub_err:
                    print(f"[ERRO] Falha ao salvar exceção no chunk {idx}: {sub_err}")
                    continue

        # Insere o que sobrou
        if buffer:
            empreendimentosGD_collection.insert_many(buffer, ordered=False)
            inseridos += len(buffer)

        print(f"[SUCESSO] Chunk {idx} -> {inseridos} registros inseridos")

    except Exception as e:
        print(f"[ERRO] Falha ao processar chunk {idx}: {e}")







# from flask import Flask, jsonify
# import requests
# import subprocess
# import os
# from datetime import datetime



# # Configurações Mongo
# MONGO_URI = (
#     "mongodb://mongo-server:27017/bdaneel"
#     "?connectTimeoutMS=60000"
#     "&socketTimeoutMS=60000"
#     "&maxPoolSize=50"
#     "&waitQueueTimeoutMS=60000"
#     "&serverSelectionTimeoutMS=60000"
# )
# DB_NAME = "bdaneel"
# COLLECTION_NAME = "empreendimentosGD_EXCEPTION_collection"

# # URL oficial do CSV da ANEEL
# CSV_URL = "https://dadosabertos.aneel.gov.br/dataset/5e0fafd2-21b9-4d5b-b622-40438d40aba2/resource/b1bd71e7-d0ad-4214-9053-cbd58e9564a7/download/empreendimento-geracao-distribuida.csv"

# # Arquivo local temporário
# LOCAL_FILE = "empreendimentosGD.csv"


# def importar_csv():
#     print("=================================== INÍCIO DA IMPORTAÇÃO ===========================")
#     horainicial  =datetime.now()

#     try:
#         # 1. Baixar o CSV da ANEEL em blocos para evitar estourar RAM
#         response = requests.get(CSV_URL, stream=True)
#         response.raise_for_status()
        
#         with open(LOCAL_FILE, "wb") as f:
#             for chunk in response.iter_content(chunk_size=1024*1024):  # 1 MB por vez
#                 f.write(chunk)

#         # 2. Comando mongoimport
#         comando = f'''
#         mongoimport --uri "{MONGO_URI}" \
#         --collection {COLLECTION_NAME} \
#         --type csv \
#         --headerline \
#         --file "{LOCAL_FILE}" \
#         --drop
#         '''

#         # 3. Executar importação
#         resultado = subprocess.run(
#             comando,
#             shell=True,
#             check=True,
#             capture_output=True,
#             text=True
#         )

#         # 4. Apagar arquivo temporário
#         os.remove(LOCAL_FILE)

        
#         horafinal =datetime.now()
#         tempo_total = horafinal - horainicial
#         print(f"Tempo total: {tempo_total.total_seconds()/60:.2f} minutos")
#         print("=================================== IMPORTAÇÃO CONCLUÍDA ===========================")

#         return jsonify({"status": "ok", "mensagem": resultado.stdout})

#     except subprocess.CalledProcessError as e:
#         return jsonify({"status": "erro", "detalhes": e.stderr})
#     except Exception as e:
#         return jsonify({"status": "erro", "detalhes": str(e)})