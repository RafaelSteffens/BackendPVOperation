import os

class Config:
    # # Configuração do MongoDB
    # MONGO_URI = os.getenv(
    #     "MONGO_URI", 
    #     "mongodb+srv://pvoperation:root@bdaneel.bgnfquy.mongodb.net/"
    # )
    # MONGO_DBNAME = os.getenv("MONGO_DBNAME", "bdaneel")  # Nome do banco de dados
    MONGO_URI = "mongodb+srv://pvoperation:root@bdaneel.bgnfquy.mongodb.net/?retryWrites=true&w=majority&connectTimeoutMS=60000&socketTimeoutMS=60000&maxPoolSize=50&waitQueueTimeoutMS=60000&serverSelectionTimeoutMS=60000"
    # MONGO_DBNAME = "bdaneel"