from concurrent.futures import ProcessPoolExecutor
import pandas as pd
from app.extensions import db
from app.models.registroAneel import RegistroAneel
from datetime import datetime

empreendimentosGD_collection = db["empreendimentosGD"]
empreendimentosGD_EXCEPTION_collection = db["empreendimentosGD_EXCEPTION_collection"]


def importar_csv():
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

    with ProcessPoolExecutor(max_workers=7) as executor:
        for idx, chunk in enumerate(leitorCSV, start=1):
            executor.submit(processar_chunk, chunk, idx)


    horafinal =datetime.now()
    tempo_total = horafinal - horainicial
    print(f"Tempo total: {tempo_total.total_seconds()/60:.2f} minutos")
    print("=================================== IMPORTAÇÃO CONCLUÍDA ===========================")


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
