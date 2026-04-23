from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Sala, Jogador, PossePropriedade, Propriedade, HistoricoPartida, Transacao
from schemas import (
    SalaCreate, SalaBusca, JoinByLink, EntrarSalaResponse,
    SalaInfo, JogadorDetalhado,
)
from seed import SALDO_INICIAL
from ws_manager import manager
from passlib.context import CryptContext

router = APIRouter(prefix="/salas", tags=["salas"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _sala_info(sala: Sala) -> dict:
    return {
        "id": sala.id,
        "nome": sala.nome,
        "link_token": sala.link_token,
        "status": sala.status,
        "versao_jogo": sala.versao_jogo,
        "casas_disponiveis": sala.casas_disponiveis,
        "hoteis_disponiveis": sala.hoteis_disponiveis,
        "host_jogador_id": sala.host_jogador_id,
        "jogadores": [
            {
                "id": j.id,
                "nome": j.nome,
                "saldo": j.saldo,
                "status": j.status,
                "ordem_entrada": j.ordem_entrada,
            }
            for j in sorted(sala.jogadores, key=lambda x: x.ordem_entrada)
            if j.status != "expulso"
        ],
    }


def _criar_jogador(db: Session, sala: Sala, nome: str) -> Jogador:
    ativos = [j for j in sala.jogadores if j.status != "expulso"]
    if len(ativos) >= 8:
        raise HTTPException(status_code=400, detail="Sala cheia (máximo 8 jogadores)")
    saldo_inicial = SALDO_INICIAL.get(sala.versao_jogo, 1_500_000)
    jogador = Jogador(
        sala_id=sala.id,
        nome=nome,
        saldo=saldo_inicial,
        status="ativo",
        ordem_entrada=len(ativos),
    )
    db.add(jogador)
    db.flush()
    return jogador


# ── Criar sala ────────────────────────────────────────────────────────────

@router.post("", status_code=201)
def criar_sala(body: SalaCreate, db: Session = Depends(get_db)):
    sala = Sala(
        nome=body.nome,
        senha_hash=pwd_context.hash(body.senha),
        versao_jogo=body.versao_jogo,
    )
    db.add(sala)
    db.flush()

    jogador = _criar_jogador(db, sala, body.nome_jogador)
    sala.host_jogador_id = jogador.id
    db.commit()
    db.refresh(sala)
    db.refresh(jogador)

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


# ── Entrar por busca (nome + senha) ──────────────────────────────────────

@router.post("/busca")
def entrar_por_busca(body: SalaBusca, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter(Sala.nome == body.nome, Sala.status != "encerrada").first()
    if not sala or not pwd_context.verify(body.senha, sala.senha_hash):
        raise HTTPException(status_code=404, detail="Sala não encontrada ou senha inválida")
    if sala.status == "encerrada":
        raise HTTPException(status_code=410, detail="Partida já encerrada")

    jogador = _criar_jogador(db, sala, body.nome_jogador)
    db.commit()
    db.refresh(sala)
    db.refresh(jogador)

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


# ── Entrar por link direto ────────────────────────────────────────────────

@router.post("/join/{link_token}")
def entrar_por_link(link_token: str, body: JoinByLink, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter(Sala.link_token == link_token, Sala.status != "encerrada").first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada ou partida encerrada")

    jogador = _criar_jogador(db, sala, body.nome_jogador)
    db.commit()
    db.refresh(sala)
    db.refresh(jogador)

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


# ── Info da sala ──────────────────────────────────────────────────────────

@router.get("/{sala_id}")
def get_sala(sala_id: str, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter_by(id=sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    return _sala_info(sala)


# ── Iniciar partida ───────────────────────────────────────────────────────

@router.post("/{sala_id}/start")
async def iniciar_partida(sala_id: str, session_token: str, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter_by(id=sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada")

    host = db.query(Jogador).filter_by(id=sala.host_jogador_id).first()
    if not host or host.session_token != session_token:
        raise HTTPException(status_code=403, detail="Apenas o host pode iniciar")

    if sala.status != "lobby":
        raise HTTPException(status_code=400, detail="Partida já iniciada")

    ativos = [j for j in sala.jogadores if j.status == "ativo"]
    if len(ativos) < 2:
        raise HTTPException(status_code=400, detail="Mínimo de 2 jogadores para iniciar")

    # Seed posse_propriedades: todas disponíveis no banco
    props = db.query(Propriedade).filter_by(versao_jogo=sala.versao_jogo).all()
    for prop in props:
        posse = PossePropriedade(sala_id=sala.id, propriedade_id=prop.id)
        db.add(posse)

    sala.status = "em_andamento"
    sala.ultima_atividade = datetime.now(timezone.utc)
    db.commit()
    db.refresh(sala)

    await manager.broadcast(sala_id, {"tipo": "partida_iniciada", "dados": _sala_info(sala)})
    return _sala_info(sala)


# ── Expulsar jogador (host) ───────────────────────────────────────────────

@router.delete("/{sala_id}/jogadores/{jogador_id}")
async def expulsar_jogador(
    sala_id: str, jogador_id: str, session_token: str, db: Session = Depends(get_db)
):
    sala = db.query(Sala).filter_by(id=sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada")

    host = db.query(Jogador).filter_by(id=sala.host_jogador_id).first()
    if not host or host.session_token != session_token:
        raise HTTPException(status_code=403, detail="Apenas o host pode expulsar")

    alvo = db.query(Jogador).filter_by(id=jogador_id, sala_id=sala_id).first()
    if not alvo:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    if alvo.id == host.id:
        raise HTTPException(status_code=400, detail="Host não pode se expulsar")

    alvo.status = "expulso"
    db.commit()

    await manager.broadcast(sala_id, {
        "tipo": "jogador_expulso",
        "dados": {"jogador_id": jogador_id, "nome": alvo.nome},
    })
    return {"ok": True}


# ── Sair da sala (auto-saída) ─────────────────────────────────────────────

@router.post("/{sala_id}/sair")
async def sair_da_sala(sala_id: str, session_token: str, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter_by(id=sala_id).first()
    if not sala or sala.status not in ("lobby", "em_andamento"):
        raise HTTPException(status_code=404, detail="Sala não encontrada")

    jogador = db.query(Jogador).filter_by(session_token=session_token, sala_id=sala_id).first()
    if not jogador or jogador.status == "expulso":
        raise HTTPException(status_code=403, detail="Sessão inválida")

    is_host = sala.host_jogador_id == jogador.id
    if is_host:
        outros = [j for j in sala.jogadores if j.status == "ativo" and j.id != jogador.id]
        if outros:
            novo_host = min(outros, key=lambda j: j.ordem_entrada)
            sala.host_jogador_id = novo_host.id
            await manager.broadcast(sala_id, {
                "tipo": "host_alterado",
                "dados": {"novo_host_id": novo_host.id, "nome": novo_host.nome},
            })

    jogador.status = "expulso"
    db.commit()

    await manager.broadcast(sala_id, {
        "tipo": "jogador_expulso",
        "dados": {"jogador_id": jogador.id, "nome": jogador.nome},
    })
    return {"ok": True}


# ── Encerrar partida (host) ───────────────────────────────────────────────

@router.post("/{sala_id}/encerrar")
async def encerrar_partida(sala_id: str, session_token: str, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter_by(id=sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada")

    host = db.query(Jogador).filter_by(id=sala.host_jogador_id).first()
    if not host or host.session_token != session_token:
        raise HTTPException(status_code=403, detail="Apenas o host pode encerrar")

    if sala.status != "em_andamento":
        raise HTTPException(status_code=400, detail="Partida não está em andamento")

    agora = datetime.now(timezone.utc)
    sala.status = "encerrada"
    sala.encerrada_em = agora

    # Liquidação automática
    ativos = [j for j in sala.jogadores if j.status in ("ativo", "falido")]
    posses = db.query(PossePropriedade).filter_by(sala_id=sala_id).all()

    for posse in posses:
        if posse.jogador_id is None:
            continue
        dono = next((j for j in ativos if j.id == posse.jogador_id), None)
        if not dono:
            continue
        prop = posse.propriedade

        if posse.hipotecada:
            custo_resgate = int(prop.valor_hipoteca * 1.2)
            if dono.saldo >= custo_resgate:
                dono.saldo -= custo_resgate
            # Se não puder pagar, volta ao banco (sem nenhum valor)
        else:
            if posse.tem_hotel:
                dono.saldo += (prop.custo_hotel or 0) // 2
            elif posse.num_casas > 0:
                dono.saldo += ((prop.custo_casa or 0) * posse.num_casas) // 2
            dono.saldo += prop.valor_compra

    # Ranking final
    ranking_jogadores = sorted(
        [j for j in sala.jogadores if j.status not in ("expulso",)],
        key=lambda j: j.saldo,
        reverse=True,
    )
    vencedor = ranking_jogadores[0] if ranking_jogadores else None

    def _prop_list(jogador_id):
        resultado = []
        for p in posses:
            if p.jogador_id != jogador_id:
                continue
            item = {"nome": p.propriedade.nome, "tipo": p.propriedade.tipo}
            if p.propriedade.tipo == "rua":
                item["casas"] = p.num_casas
                item["hotel"] = p.tem_hotel
            resultado.append(item)
        return resultado

    ranking_json = [
        {
            "posicao": i + 1,
            "nome": j.nome,
            "saldo_final": j.saldo,
            "propriedades": _prop_list(j.id),
        }
        for i, j in enumerate(ranking_jogadores)
    ]

    total_transacoes = db.query(Transacao).filter_by(
        sala_id=sala_id, status="aprovada"
    ).count()

    iniciada_em = sala.criada_em
    if iniciada_em and iniciada_em.tzinfo is None:
        iniciada_em = iniciada_em.replace(tzinfo=timezone.utc)
    duracao = max(0, int((agora - iniciada_em).total_seconds() / 60)) if iniciada_em else 0

    historico = HistoricoPartida(
        nome_sala=sala.nome,
        senha_hash=sala.senha_hash,
        link_token=sala.link_token,
        jogadores_count=len([j for j in sala.jogadores if j.status != "expulso"]),
        iniciada_em=iniciada_em,
        encerrada_em=agora,
        duracao_minutos=duracao,
        vencedor_nome=vencedor.nome if vencedor else "—",
        total_transacoes=total_transacoes,
        ranking=ranking_json,
    )
    db.add(historico)
    db.commit()

    await manager.broadcast(sala_id, {
        "tipo": "partida_encerrada",
        "dados": {
            "link_token": sala.link_token,
            "ranking": ranking_json,
        },
    })
    return {"link_token": sala.link_token, "ranking": ranking_json}
