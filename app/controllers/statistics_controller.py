from flask import Blueprint, jsonify
from app.extensions import db
from ..extensions import redis_client
import json
from ..services.usinas_services.statistics_services import statistics_services

bp = Blueprint("estatisticas", __name__)

@bp.route("/api/estatisticas", methods=["GET"])
def statistics():
    return statistics_services()
