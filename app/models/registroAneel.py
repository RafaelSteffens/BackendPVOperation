from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import math


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
    rank: Optional[float] = None
    location: Optional[dict] = None  

    def __init__(self, **data):
        data = self._normalize(data)
        super().__init__(**data)

    @staticmethod
    def _normalize(data: dict) -> dict:

        def to_str(val):
            if val is None or (isinstance(val, float) and math.isnan(val)):
                return None
            return str(val).strip()

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
            
        def to_none(val):
            if val is None:
                return None

            if isinstance(val, float) and math.isnan(val):
                return None

            if isinstance(val, str) and val.strip().lower() in ("nan", "", "none", "null"):
                return None
            return val
                
        def to_float(val):
            if val is None or (isinstance(val, float) and (math.isnan(val) or math.isinf(val))):
                return None
            if isinstance(val, str):
                val = val.replace(",", ".").strip()
            try:
                return float(val)
            except:
                return None    
        
        def to_GeoLocalizacao(val):
            num = to_float(val)

            if num is None:
                return None

            if -90 <= num <= 90 or -180 <= num <= 180:
                return round(num, 6)

            if abs(num) > 180:
                corrigido = num / 100
                if -90 <= corrigido <= 90 or -180 <= corrigido <= 180:
                    return round(corrigido, 6)

            return None

        
        lat = to_GeoLocalizacao(data.get("NumCoordNEmpreendimento"))
        lon = to_GeoLocalizacao(data.get("NumCoordEEmpreendimento"))

        if lat is not None and lon is not None:
            data["location"] = {
                    "type": "Point",
                    "coordinates": [lon, lat]
                }
        else:
            data["location"] = None
        
            

        # Normaliza os campos
        data["NumCNPJDistribuidora"] = to_str(data.get("NumCNPJDistribuidora"))
        data["NumCPFCNPJ"] = to_str(data.get("NumCPFCNPJ"))
        data["CodEmpreendimento"] = to_str(data.get("CodEmpreendimento"))
        data["NomTitularEmpreendimento"] = to_str(data.get("NomTitularEmpreendimento"))
        data["NomMunicipio"] = to_str(data.get("NomMunicipio"))
        data["SigUF"] = to_str(data.get("SigUF"))
        data["MdaPotenciaInstaladaKW"] = to_float(data.get("MdaPotenciaInstaladaKW"))
        data["CodUFibge"] = to_int(data.get("CodUFibge"))
        data["CodClasseConsumo"] = to_int(data.get("CodClasseConsumo"))
        data["CodSubGrupoTarifario"] = to_int(data.get("CodSubGrupoTarifario"))
        data["DatGeracaoConjuntoDados"] = to_date(data.get("DatGeracaoConjuntoDados"))
        data["SigAgente"] = to_none(data.get("SigAgente"))
        data["NomAgente"] = to_none(data.get("NomAgente"))
        data["CodCEP"] = to_none(data.get("CodCEP"))


        return data

    class Config:
        populate_by_name = True
        extra = "ignore"
