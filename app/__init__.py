from flask import Flask
from .config import Config
from .extensions import init_mongo
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_mongo(app)

    from .controllers.atualizaBD import bp as main_bp
    from .controllers.usinas import bp as usinas
    from .controllers.estatisticas import bp as estatisticas
    app.register_blueprint(main_bp)
    app.register_blueprint(usinas)
    app.register_blueprint(estatisticas)

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})



    return app
