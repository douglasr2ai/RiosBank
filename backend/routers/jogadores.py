from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Jogador, Sala
from schemas import ReconnectRequest

router = APIRouter(prefix="/jogadores", tags=["jogadores"])


@router.post("/reconnect")
def reconnect(body: ReconnectRequest, db: Session = Depends(get_db)):
    jogador = db.query(Jogador).filter_by(session_token=body.session_token).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Sessão inválida")

    sala = db.query(Sala).filter_by(id=jogador.sala_id).first()
    if not sala or sala.status == "encerrada":
        raise HTTPException(status_code=410, detail="Partida encerrada ou não existe")

    if jogador.status == "expulso":
        raise HTTPException(status_code=403, detail="Você foi expulso desta sala")

    from routers.salas import _sala_info
    return {
        "sala": _sala_info(sala),
        "jogador": {
            "id": jogador.id,
            "nome": jogador.nome,
            "saldo": jogador.saldo,
            "status": jogador.status,
            "ordem_entrada": jogador.ordem_entrada,
            "session_token": jogador.session_token,
        },
    }


@router.get("/{jogador_id}")
def get_jogador(jogador_id: str, db: Session = Depends(get_db)):
    jogador = db.query(Jogador).filter_by(id=jogador_id).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return {
        "id": jogador.id,
        "nome": jogador.nome,
        "saldo": jogador.saldo,
        "status": jogador.status,
        "ordem_entrada": jogador.ordem_entrada,
    }
