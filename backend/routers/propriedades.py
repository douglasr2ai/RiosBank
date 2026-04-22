from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Propriedade, PossePropriedade, Sala, Jogador

router = APIRouter(tags=["propriedades"])


def _posse_dict(p: PossePropriedade) -> dict:
    prop = p.propriedade
    return {
        "id": p.id,
        "propriedade_id": p.propriedade_id,
        "jogador_id": p.jogador_id,
        "hipotecada": p.hipotecada,
        "num_casas": p.num_casas,
        "tem_hotel": p.tem_hotel,
        "propriedade": {
            "id": prop.id,
            "nome": prop.nome,
            "tipo": prop.tipo,
            "grupo_cor": prop.grupo_cor,
            "cor_hex": prop.cor_hex,
            "valor_compra": prop.valor_compra,
            "valor_hipoteca": prop.valor_hipoteca,
            "multiplicador_dado": prop.multiplicador_dado,
            "aluguel_sem_casa": prop.aluguel_sem_casa,
            "aluguel_1_casa": prop.aluguel_1_casa,
            "aluguel_2_casas": prop.aluguel_2_casas,
            "aluguel_3_casas": prop.aluguel_3_casas,
            "aluguel_4_casas": prop.aluguel_4_casas,
            "aluguel_hotel": prop.aluguel_hotel,
            "custo_casa": prop.custo_casa,
            "custo_hotel": prop.custo_hotel,
        },
    }


@router.get("/propriedades")
def listar_catalogo(versao: str = "super_banco_imobiliario", db: Session = Depends(get_db)):
    props = db.query(Propriedade).filter_by(versao_jogo=versao).all()
    return [
        {
            "id": p.id,
            "nome": p.nome,
            "tipo": p.tipo,
            "grupo_cor": p.grupo_cor,
            "cor_hex": p.cor_hex,
            "valor_compra": p.valor_compra,
            "valor_hipoteca": p.valor_hipoteca,
            "multiplicador_dado": p.multiplicador_dado,
            "aluguel_sem_casa": p.aluguel_sem_casa,
            "aluguel_1_casa": p.aluguel_1_casa,
            "aluguel_2_casas": p.aluguel_2_casas,
            "aluguel_3_casas": p.aluguel_3_casas,
            "aluguel_4_casas": p.aluguel_4_casas,
            "aluguel_hotel": p.aluguel_hotel,
            "custo_casa": p.custo_casa,
            "custo_hotel": p.custo_hotel,
        }
        for p in props
    ]


@router.get("/salas/{sala_id}/propriedades")
def posses_da_sala(sala_id: str, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter_by(id=sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    posses = db.query(PossePropriedade).filter_by(sala_id=sala_id).all()
    return [_posse_dict(p) for p in posses]
