from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from app.extensions import db
from app.models.registroAneel import RegistroAneel

COLLECTION = db["empreendimentoGD"]

def importar_csv(filepath="./empreendimento-geracao-distribuida.csv", chunksize=10000):
    df_iter = pd.read_csv(
        filepath,
        chunksize=chunksize,
        encoding="latin1",
        sep=";",
        low_memory=True
    )

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(processar_chunk, chunk) for chunk in df_iter]
        for future in futures:
            future.result()  # força aguardar conclusão

def processar_chunk(chunk):
    validos = []
    for _, row in chunk.iterrows():
        try:
            dado = RegistroAneel(**row.to_dict()).dict(by_alias=True)
            validos.append(dado)
        except Exception:
            continue
    if validos:
        COLLECTION.insert_many(validos, ordered=False)
