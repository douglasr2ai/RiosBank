from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Leilao, Lance, Jogador, Sala, PossePropriedade, Transacao
from schemas import LeilaoCreate, LanceCreate
from ws_manager import manager

router = APIRouter(prefix="/leiloes", tags=["leiloes"])

INCREMENTOS_VALIDOS = {10_000, 50_000, 100_000}  # R$100, R$500, R$1.000 em centavos


@router.post("", status_code=201)
async def iniciar_leilao(body: LeilaoCreate, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter_by(id=body.sala_id).first()
    if not sala or sala.status != "em_andamento":
        raise HTTPException(status_code=400, detail="Sala inválida ou partida não iniciada")

    jogador = db.query(Jogador).filter_by(
        session_token=body.session_token, sala_id=body.sala_id
    ).first()
    if not jogador or jogador.status != "ativo":
        raise HTTPException(status_code=403, detail="Jogador inativo ou sessão inválida")

    posse = db.query(PossePropriedade).filter_by(
        sala_id=body.sala_id, propriedade_id=body.propriedade_id
    ).first()
    if not posse:
        raise HTTPException(status_code=404, detail="Propriedade não encontrada nesta sala")

    leilao_ativo = db.query(Leilao).filter_by(
        sala_id=body.sala_id, status="ativo"
    ).first()
    if leilao_ativo:
        raise HTTPException(status_code=400, detail="Já existe um leilão ativo nesta sala")

    lance_minimo = posse.propriedade.valor_compra if posse.jogador_id is None else 10_000

    leilao = Leilao(
        sala_id=body.sala_id,
        propriedade_id=body.propriedade_id,
        iniciado_por=jogador.id,
        lance_atual=lance_minimo,
        status="ativo",
    )
    db.add(leilao)
    db.commit()
    db.refresh(leilao)

    await manager.broadcast(body.sala_id, {
        "tipo": "leilao_iniciado",
        "dados": {
            "leilao_id": leilao.id,
            "propriedade_id": leilao.propriedade_id,
            "iniciado_por": leilao.iniciado_por,
            "lance_atual": leilao.lance_atual,
            "iniciado_em": leilao.iniciado_em.isoformat(),
        },
    })
    return {
        "id": leilao.id,
        "propriedade_id": leilao.propriedade_id,
        "iniciado_por": leilao.iniciado_por,
        "lance_atual": leilao.lance_atual,
        "status": leilao.status,
    }


@router.post("/{leilao_id}/lance")
async def dar_lance(leilao_id: str, body: LanceCreate, db: Session = Depends(get_db)):
    leilao = db.query(Leilao).filter_by(id=leilao_id, status="ativo").first()
    if not leilao:
        raise HTTPException(status_code=404, detail="Leilão não encontrado ou encerrado")

    if body.incremento not in INCREMENTOS_VALIDOS:
        raise HTTPException(status_code=400, detail="Incremento inválido. Use 10000, 50000 ou 100000")

    jogador = db.query(Jogador).filter_by(
        session_token=body.session_token, sala_id=leilao.sala_id
    ).first()
    if not jogador or jogador.status != "ativo":
        raise HTTPException(status_code=403, detail="Jogador inativo ou sessão inválida")

    if jogador.id == leilao.iniciado_por:
        raise HTTPException(status_code=400, detail="Quem iniciou o leilão não pode dar lances")

    novo_valor = leilao.lance_atual + body.incremento

    if jogador.saldo < novo_valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para este lance")

    lance = Lance(leilao_id=leilao_id, jogador_id=jogador.id, valor=novo_valor)
    db.add(lance)
    leilao.lance_atual = novo_valor
    leilao.lider_id = jogador.id
    db.commit()

    await manager.broadcast(leilao.sala_id, {
        "tipo": "lance_registrado",
        "dados": {
            "leilao_id": leilao_id,
            "lance_atual": leilao.lance_atual,
            "lider_id": leilao.lider_id,
            "lider_nome": jogador.nome,
        },
    })
    return {"lance_atual": leilao.lance_atual, "lider_id": leilao.lider_id}


@router.post("/{leilao_id}/encerrar")
async def encerrar_leilao(leilao_id: str, session_token: str, db: Session = Depends(get_db)):
    """Chamado pelo frontend quando o timer de 60s expira."""
    leilao = db.query(Leilao).filter_by(id=leilao_id).first()
    if not leilao or leilao.status != "ativo":
        return {"status": "already_closed"}

    jogador = db.query(Jogador).filter_by(
        session_token=session_token, sala_id=leilao.sala_id
    ).first()
    if not jogador:
        raise HTTPException(status_code=403, detail="Sessão inválida")

    leilao.status = "encerrado"
    leilao.encerrado_em = datetime.now(timezone.utc)

    resultado = {"leilao_id": leilao_id, "status": "encerrado", "vencedor_id": None}

    if leilao.lider_id:
        vencedor = db.query(Jogador).filter_by(id=leilao.lider_id).first()
        posse = db.query(PossePropriedade).filter_by(
            sala_id=leilao.sala_id, propriedade_id=leilao.propriedade_id
        ).first()

        if vencedor and posse:
            vencedor.saldo -= leilao.lance_atual
            posse.jogador_id = vencedor.id

            transacao = Transacao(
                sala_id=leilao.sala_id,
                tipo="leilao",
                valor=leilao.lance_atual,
                origem_id=vencedor.id,
                propriedade_id=leilao.propriedade_id,
                descricao=f"Leilão — {posse.propriedade.nome}",
                status="aprovada",
                resolvida_em=datetime.now(timezone.utc),
            )
            db.add(transacao)
            resultado["vencedor_id"] = vencedor.id
            resultado["vencedor_nome"] = vencedor.nome

    db.commit()

    await manager.broadcast(leilao.sala_id, {
        "tipo": "leilao_encerrado",
        "dados": resultado,
    })
    return resultado


@router.get("/{leilao_id}")
def get_leilao(leilao_id: str, db: Session = Depends(get_db)):
    leilao = db.query(Leilao).filter_by(id=leilao_id).first()
    if not leilao:
        raise HTTPException(status_code=404, detail="Leilão não encontrado")
    return {
        "id": leilao.id,
        "sala_id": leilao.sala_id,
        "propriedade_id": leilao.propriedade_id,
        "iniciado_por": leilao.iniciado_por,
        "lance_atual": leilao.lance_atual,
        "lider_id": leilao.lider_id,
        "status": leilao.status,
        "iniciado_em": leilao.iniciado_em.isoformat(),
        "encerrado_em": leilao.encerrado_em.isoformat() if leilao.encerrado_em else None,
    }
