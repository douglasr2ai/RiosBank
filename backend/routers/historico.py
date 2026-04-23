from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import HistoricoPartida
from schemas import HistoricoBusca
from passlib.context import CryptContext

router = APIRouter(prefix="/historico", tags=["historico"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _historico_dict(h: HistoricoPartida) -> dict:
    return {
        "id": h.id,
        "link_token": h.link_token,
        "nome_sala": h.nome_sala,
        "codigo": h.codigo,
        "jogadores_count": h.jogadores_count,
        "iniciada_em": h.iniciada_em.isoformat(),
        "encerrada_em": h.encerrada_em.isoformat(),
        "duracao_minutos": h.duracao_minutos,
        "vencedor_nome": h.vencedor_nome,
        "total_transacoes": h.total_transacoes,
        "ranking": h.ranking,
    }


@router.get("/{link_token}")
def get_por_link(link_token: str, db: Session = Depends(get_db)):
    h = db.query(HistoricoPartida).filter_by(link_token=link_token).first()
    if not h:
        raise HTTPException(status_code=404, detail="Histórico não encontrado")
    return _historico_dict(h)


@router.post("/busca")
def buscar_historico(body: HistoricoBusca, db: Session = Depends(get_db)):
    h = db.query(HistoricoPartida).filter_by(codigo=body.codigo.strip()).first()
    if not h or not pwd_context.verify(body.senha, h.senha_hash):
        raise HTTPException(status_code=404, detail="Histórico não encontrado ou senha inválida")
    return _historico_dict(h)
