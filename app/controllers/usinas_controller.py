from flask import Blueprint, Response, request, jsonify, stream_with_context
import orjson
from ..extensions import redis_client
import json
from ..services.usinas_services.coordenadas_usinas_services import coords_usinas_services
from ..services.usinas_services.list_filters_services import list_filters_services
from ..services.usinas_services.list_usinas_by_filter_service import list_usinas_by_filter_service
from app.extensions import db

bp = Blueprint("usinas", __name__)

@bp.route("/api/usinas", methods=["GET"])
def list_usinas_by_filter():
    return list_usinas_by_filter_service()

@bp.route("/api/usinas/filtros", methods=["GET"])
def list_filters():
    return list_filters_services()

@bp.route("/api/CoordUsinas", methods=["GET"])
def coord_usinas():
    return coords_usinas_services()