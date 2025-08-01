from flask import Blueprint, request, jsonify
from app.extensions import db

bp = Blueprint("usinas", __name__)
empreendimentosGD_collection = db["empreendimentoGD"]

@bp.route("/api/usinas", methods=["GET"])
def listar_usinas():
    # Paginação
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))
    skip = (page - 1) * per_page

    # Filtros
    filtros = {}
    campos_filtro = ["SigUF", "NomMunicipio", "SigAgente", "NomTitularEmpreendimento"]
    for campo in campos_filtro:
        valor = request.args.get(campo)
        if valor:
            filtros[campo] = {"$regex": valor, "$options": "i"}

    # Busca
    cursor = empreendimentosGD_collection.find(filtros, {"_id": 0}).skip(skip).limit(per_page)
    total = empreendimentosGD_collection.count_documents(filtros)



    
    # COORDENADASLEAFT
    cursor_coords = empreendimentosGD_collection.find(
    filtros, 
    {
        "_id": 0,
        "NumCoordNEmpreendimento": 1,
        "NumCoordEEmpreendimento": 1,
        "NomTitularEmpreendimento": 1
    }
    )

    coordenadasFiltradas = [
        {
            "lat": doc["NumCoordNEmpreendimento"],
            "lon": doc["NumCoordEEmpreendimento"],
            "nome": doc.get("NomTitularEmpreendimento")
        }
        for doc in cursor_coords
        if doc.get("NumCoordNEmpreendimento") and doc.get("NumCoordEEmpreendimento")
    ]

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total + per_page - 1) // per_page,
        "filters_applied": filtros,
        "data": list(cursor),
        "coordenadasFiltradas": coordenadasFiltradas
    })


@bp.route("/api/usinas/filtros", methods=["GET"])
def listar_filtros():
    uf = request.args.get("SigUF")
    municipio = request.args.get("NomMunicipio")

    filtros = {}

    if uf:
        filtros["SigUF"] = uf
    if municipio:
        filtros["NomMunicipio"] = municipio

    return jsonify({
        "SigUF": empreendimentosGD_collection.distinct("SigUF"),
        "NomMunicipio": empreendimentosGD_collection.distinct("NomMunicipio", {"SigUF": uf}) if uf else [],
        "SigAgente": empreendimentosGD_collection.distinct("SigAgente", filtros) if uf or municipio else []
    })

# @bp.route("/api/usinas/coordenadasFiltradas", methods=["GET"])
# def mostrarEmpreendimentosLeaft():

