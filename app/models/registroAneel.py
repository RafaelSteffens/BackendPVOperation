from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import math
from bson import ObjectId

class RegistroAneel(BaseModel):
    data_geracao: Optional[datetime] = Field(alias="DatGeracaoConjuntoDados")
    periodo_referencia: Optional[str] = Field(alias="AnmPeriodoReferencia")
    cnpj_distribuidora: Optional[str] = Field(alias="NumCNPJDistribuidora")
    sigla_agente: Optional[str] = Field(alias="SigAgente")
    nome_agente: Optional[str] = Field(alias="NomAgente")
    cod_classe_consumo: Optional[int] = Field(alias="CodClasseConsumo")
    classe_consumo: Optional[str] = Field(alias="DscClasseConsumo")
    cod_subgrupo: Optional[int] = Field(alias="CodSubGrupoTarifario")
    subgrupo_tarifario: Optional[str] = Field(alias="DscSubGrupoTarifario")
    uf_ibge: Optional[int] = Field(alias="CodUFibge")
    uf: Optional[str] = Field(alias="SigUF")
    regiao: Optional[str] = Field(alias="NomRegiao")
    municipio: Optional[str] = Field(alias="NomMunicipio")
    cep: Optional[str] = Field(alias="CodCEP")
    cpf_cnpj: Optional[str] = Field(alias="NumCPFCNPJ")
    titular: Optional[str] = Field(alias="NomTitularEmpreendimento")
    cod_empreendimento: Optional[str] = Field(alias="CodEmpreendimento")
    potencia_kw: Optional[float] = Field(alias="MdaPotenciaInstaladaKW")
    fonte_geracao: Optional[str] = Field(alias="DscFonteGeracao")
    porte: Optional[str] = Field(alias="DscPorte")
    latitude: Optional[float] = Field(alias="NumCoordNEmpreendimento")
    longitude: Optional[float] = Field(alias="NumCoordEEmpreendimento")
    rank: Optional[float] = None

    def __init__(self, **data):
        data = self._normalize(data)
        super().__init__(**data)

    @staticmethod
    def _normalize(data: dict) -> dict:
        """Converte NaN e tipos incompatíveis para None ou formato esperado"""

        def to_str(val):
            if val is None or (isinstance(val, float) and math.isnan(val)):
                return None
            return str(val).strip()

        def to_float(val):
            if val is None or (isinstance(val, float) and (math.isnan(val) or math.isinf(val))):
                return None
            if isinstance(val, str):
                val = val.replace(",", ".").strip()
            try:
                return float(val)
            except:
                return None

        def to_int(val):
            f = to_float(val)
            return int(f) if f is not None else None

        def to_date(val):
            if not val:
                return None
            try:
                return datetime.strptime(str(val).strip(), "%Y-%m-%d")
            except:
                return None

        # Normaliza os campos
        data["NumCNPJDistribuidora"] = to_str(data.get("NumCNPJDistribuidora"))
        data["NumCPFCNPJ"] = to_str(data.get("NumCPFCNPJ"))
        data["CodEmpreendimento"] = to_str(data.get("CodEmpreendimento"))
        data["NomTitularEmpreendimento"] = to_str(data.get("NomTitularEmpreendimento"))
        data["NomMunicipio"] = to_str(data.get("NomMunicipio"))
        data["SigUF"] = to_str(data.get("SigUF"))

        data["MdaPotenciaInstaladaKW"] = to_float(data.get("MdaPotenciaInstaladaKW"))
        data["NumCoordNEmpreendimento"] = to_float(data.get("NumCoordNEmpreendimento"))
        data["NumCoordEEmpreendimento"] = to_float(data.get("NumCoordEEmpreendimento"))

        data["CodUFibge"] = to_int(data.get("CodUFibge"))
        data["CodClasseConsumo"] = to_int(data.get("CodClasseConsumo"))
        data["CodSubGrupoTarifario"] = to_int(data.get("CodSubGrupoTarifario"))

        data["DatGeracaoConjuntoDados"] = to_date(data.get("DatGeracaoConjuntoDados"))

        return data

    class Config:
        populate_by_name = True
        extra = "ignore"
