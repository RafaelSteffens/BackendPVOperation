
class Config:
    # MONGO_URI = "mongodb+srv://pvoperation:root@bdaneel.bgnfquy.mongodb.net/?retryWrites=true&w=majority&connectTimeoutMS=60000&socketTimeoutMS=60000&maxPoolSize=50&waitQueueTimeoutMS=60000&serverSelectionTimeoutMS=60000"
    # MONGO_URI = (
    #     "mongodb://localhost:27017/bdaneel"
    #     "?connectTimeoutMS=60000"
    #     "&socketTimeoutMS=60000"
    #     "&maxPoolSize=50"
    #     "&waitQueueTimeoutMS=60000"
    #     "&serverSelectionTimeoutMS=60000"
    # )
 
 
    #  CONFIGURAÇÕES DOCKER
    MONGO_URI = (
        "mongodb://mongo-server:27017/bdaneel"
        "?connectTimeoutMS=60000"
        "&socketTimeoutMS=60000"
        "&maxPoolSize=50"
        "&waitQueueTimeoutMS=60000"
        "&serverSelectionTimeoutMS=60000"
    )
    
    REDIS_URL = "redis://redis-server:6379/0"



