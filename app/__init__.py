# app/__init__.py
from flask import Flask
from .config import Config
from .extensions import init_mongo

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # inicializa mongo
    init_mongo(app)

    # exemplo de import de rotas
    from .controllers.main import bp as main_bp
    from .controllers.usinas import bp as usinas
    from .controllers.estatisticas import bp as estatisticas
    app.register_blueprint(main_bp)
    app.register_blueprint(usinas)
    app.register_blueprint(estatisticas)

    from flask_cors import CORS

    # depois de criar o app
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})



    return app
