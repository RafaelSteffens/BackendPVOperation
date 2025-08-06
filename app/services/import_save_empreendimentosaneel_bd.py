from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
import pandas as pd
from app.extensions import db
from app.models.registroAneel import RegistroAneel
from .cache_services import cache_services



empreendimentosGD_collection = db["empreendimentosGD"]
empreendimentosGD_EXCEPTION_collection = db["empreendimentosGD_EXCEPTION_collection"]


def import_csv_data_service():
    print("=== INÍCIO DA IMPORTAÇÃO ===")
    horainicial = datetime.now()
    
    empreendimentosGD_collection.drop()
    empreendimentosGD_EXCEPTION_collection.drop()

    reader_csv = pd.read_csv(
        "https://dadosabertos.aneel.gov.br/dataset/5e0fafd2-21b9-4d5b-b622-40438d40aba2/resource/b1bd71e7-d0ad-4214-9053-cbd58e9564a7/download/empreendimento-geracao-distribuida.csv",
        chunksize=70000,
        encoding="latin1",
        sep=";",
        low_memory=False
    )

    with ProcessPoolExecutor(max_workers=7) as executor:
        for idx, chunk in enumerate(reader_csv, start=1):
            executor.submit(processar_chunk, chunk, idx)
    
    print("Carregando Cache...")
    cache_services()

    tempo_total = (datetime.now() - horainicial).total_seconds()/60
    print(f"Tempo total: {tempo_total:.2f} minutos")
    print("=== IMPORTAÇÃO CONCLUÍDA ===")
    

def processar_chunk(chunk, idx):
    try:
        buffer = []
        for row in chunk.to_dict(orient="records"):
            try:
                dado = RegistroAneel(**row).dict(by_alias=True)
                buffer.append(dado)
                if len(buffer) >= 35000:  
                    empreendimentosGD_collection.insert_many(buffer, ordered=False)
                    buffer.clear()
                    print("Buffer Salvo")
            except Exception as err:
                print("e    EXCEPTION   ", err, row)
        
        if buffer:
            empreendimentosGD_collection.insert_many(buffer, ordered=False)
        
        print(f"[SUCESSO] Chunk {idx} -> registros inseridos")
    except Exception as e:
        print(f"[ERRO] Falha ao processar chunk {idx}: {e}")








# def import_csv_data_service():
#     try:
#         empreendimentosGD_collection.drop()
#         empreendimentosGD_EXCEPTION_collection.drop()

#         reader_csv = pd.read_csv(
#             "https://dadosabertos.aneel.gov.br/dataset/5e0fafd2-21b9-4d5b-b622-40438d40aba2/resource/b1bd71e7-d0ad-4214-9053-cbd58e9564a7/download/empreendimento-geracao-distribuida.csv",
#             chunksize=50000,
#             encoding="latin1",
#             sep=";",
#             low_memory=False
#         )

#         futures = [] 
#         with ThreadPoolExecutor(max_workers=3) as executor:
#             for idx, chunk in enumerate(reader_csv, start=1):
#                 future = executor.submit(processing_chunk, chunk, idx)
#                 futures.append(future)

#             for future in as_completed(futures):
#                 future.result()  

#         cache_services()

#     except Exception as sub_err:
#         print(f"[ERRO] Falha ao importar e salvar csv: {sub_err}")


# def processing_chunk(chunk, id_chunk):
#     try:
#         records = chunk.to_dict(orient="records")
#         buffer = []

#         for row in records:
#             try:
#                 dado = RegistroAneel(**row).dict(by_alias=True)
#                 buffer.append(dado)

#                 if len(buffer) >= 5000:
#                     empreendimentosGD_collection.insert_many(buffer, ordered=False)
#                     buffer.clear()

#             except Exception as err:
#                 print(f"[EXCEPTION] Registro inválido no chunk {id_chunk}: {err}")
#                 try:
#                     row["_erro"] = str(err)
#                     row["_chunk"] = id_chunk
#                     empreendimentosGD_EXCEPTION_collection.insert_one(row)
#                 except Exception as sub_err:
#                     print(f"[ERRO] Falha ao salvar exceção no chunk {id_chunk}: {sub_err}")
#                     continue

#         if buffer:
#             empreendimentosGD_collection.insert_many(buffer, ordered=False)

#     except Exception as e:
#         print(f"[ERRO] Falha ao processar chunk {id_chunk}: {e}")











#  ==================== COMANDO MONGO IMPORT =======================
# mongoimport --uri="mongodb://localhost:27017/bdaneel" --collection="empreendimentosGD" --type=csv --headerline --file="C:\Users\rafae\Desktop\PVOperation_Desafio\BackendPVOperation\empreendimentosGD.csv"


# from ..config import Config
# from flask import Flask, jsonify
# import requests
# import subprocess
# import os
# from datetime import datetime


# MONGO_URI = (
#     "mongodb://localhost:27017/bdaneel")
# COLLECTION_NAME = "empreendimentosGD"
# CSV_URL = "https://dadosabertos.aneel.gov.br/dataset/5e0fafd2-21b9-4d5b-b622-40438d40aba2/resource/b1bd71e7-d0ad-4214-9053-cbd58e9564a7/download/empreendimento-geracao-distribuida.csv"
# LOCAL_FILE_RAW = "empreendimentosGD_raw.csv"
# LOCAL_FILE_CSV = "empreendimentosGD.csv"


# def import_csv_data_service():
#     try:
#         print("=== INÍCIO DA IMPORTAÇÃO ===")
#         inicio = datetime.now()

#         print("Convertendo CSV para vírgulas...")
#         df = pd.read_csv(CSV_URL, sep=';', encoding='latin1', low_memory=False)
#         df.to_csv(LOCAL_FILE_CSV, index=False)

#         os.remove(LOCAL_FILE_RAW)

#         comando = f'''
#         mongoimport --uri "{MONGO_URI}" \
#         --collection {COLLECTION_NAME} \
#         --type csv \
#         --headerline \
#         --file "{LOCAL_FILE_CSV}" \
#         --drop
#         '''

#         resultado = subprocess.run(
#             comando,
#             shell=True,
#             check=True,
#             capture_output=True,
#             text=True
#         )

#         # Remove CSV convertido após importação
#         os.remove(LOCAL_FILE_CSV)

#         tempo_total = (datetime.now() - inicio).total_seconds()
#         print(f"Tempo total: {tempo_total:.2f} segundos")
#         print("=== IMPORTAÇÃO CONCLUÍDA ===")

#         return jsonify({"status": "ok", "mensagem": resultado.stdout, "tempo_segundos": tempo_total})

#     except subprocess.CalledProcessError as e:
#         return jsonify({"status": "erro", "detalhes": e.stderr})
#     except Exception as e:
#         return jsonify({"status": "erro", "detalhes": str(e)})
