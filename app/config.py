
class Config:
    # MONGO_URI = "mongodb+srv://pvoperation:root@bdaneel.bgnfquy.mongodb.net/?retryWrites=true&w=majority&connectTimeoutMS=60000&socketTimeoutMS=60000&maxPoolSize=50&waitQueueTimeoutMS=60000&serverSelectionTimeoutMS=60000"
  
    # CONFIGURAÇÕES CONTAINER
    MONGO_URI = "mongodb://mongo-server:27017/bdaneel?connectTimeoutMS=5000&socketTimeoutMS=5000&maxPoolSize=200&waitQueueTimeoutMS=1000&serverSelectionTimeoutMS=5000&readPreference=secondaryPreferred"
    REDIS_URL = "redis://redis-server:6379/0"



