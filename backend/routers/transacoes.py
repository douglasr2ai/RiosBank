from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import update as sql_update
from sqlalchemy.orm import Session

from database import get_db
from models import Transacao, Voto, Jogador, Sala, PossePropriedade
from schemas import TransacaoCreate, VotoCreate
from ws_manager import manager

router = APIRouter(prefix="/transacoes", tags=["transacoes"])

TIPOS_VALIDOS = {
    "transferencia", "compra_propriedade", "aluguel", "hipoteca",
    "recuperar_hipoteca", "compra_casa", "venda_casa", "leilao",
    "pagamento_banco", "falencia", "estorno", "troca",
}


def _resolve_transacao(transacao: Transacao, db: Session) -> list:
    """Aplica os efeitos financeiros de uma transação aprovada. Retorna IDs de jogadores que faliram."""
    falidos = []
    if transacao.tipo in ("transferencia", "aluguel", "compra_propriedade",
                          "leilao", "pagamento_banco", "compra_casa",
                          "venda_casa", "hipoteca", "recuperar_hipoteca", "troca"):
        if transacao.origem_id:
            origem = db.query(Jogador).filter_by(id=transacao.origem_id).first()
            if origem:
                origem.saldo -= transacao.valor
                if origem.saldo < 0:
                    origem.saldo = 0
                    origem.status = "falido"
                    falidos.append(origem.id)

        if transacao.destino_id:
            destino = db.query(Jogador).filter_by(id=transacao.destino_id).first()
            if destino:
                destino.saldo += transacao.valor

        if transacao.tipo == "compra_propriedade" and transacao.propriedade_id and transacao.origem_id:
            posse = db.query(PossePropriedade).filter_by(
                sala_id=transacao.sala_id,
                propriedade_id=transacao.propriedade_id,
            ).first()
            if posse:
                posse.jogador_id = transacao.origem_id

        if transacao.tipo == "hipoteca" and transacao.propriedade_id:
            posse = db.query(PossePropriedade).filter_by(
                sala_id=transacao.sala_id,
                propriedade_id=transacao.propriedade_id,
            ).first()
            if posse:
                posse.hipotecada = True

        if transacao.tipo == "recuperar_hipoteca" and transacao.propriedade_id:
            posse = db.query(PossePropriedade).filter_by(
                sala_id=transacao.sala_id,
                propriedade_id=transacao.propriedade_id,
            ).first()
            if posse:
                posse.hipotecada = False

        if transacao.tipo == "compra_casa" and transacao.propriedade_id:
            posse = db.query(PossePropriedade).filter_by(
                sala_id=transacao.sala_id,
                propriedade_id=transacao.propriedade_id,
            ).first()
            sala = db.query(Sala).filter_by(id=transacao.sala_id).first()
            if posse and sala:
                prop = posse.propriedade
                # hotel purchase: num_casas == 4 quando a transação foi criada
                # quantidade calculada a partir do valor enviado
                if prop and prop.custo_casa and prop.custo_casa > 0:
                    quantidade = max(1, round(transacao.valor / prop.custo_casa))
                else:
                    quantidade = 1
                for _ in range(quantidade):
                    if not posse.tem_hotel:
                        if posse.num_casas < 4:
                            posse.num_casas += 1
                            sala.casas_disponiveis -= 1
                        elif posse.num_casas == 4:
                            posse.tem_hotel = True
                            posse.num_casas = 0
                            sala.casas_disponiveis += 4
                            sala.hoteis_disponiveis -= 1

        if transacao.tipo == "venda_casa" and transacao.propriedade_id:
            posse = db.query(PossePropriedade).filter_by(
                sala_id=transacao.sala_id,
                propriedade_id=transacao.propriedade_id,
            ).first()
            sala = db.query(Sala).filter_by(id=transacao.sala_id).first()
            if posse and sala:
                prop = posse.propriedade
                half = (prop.custo_casa // 2) if (prop and prop.custo_casa) else 0
                if posse.tem_hotel:
                    quantidade = 1
                elif half > 0:
                    quantidade = max(1, round(transacao.valor / half))
                else:
                    quantidade = 1
                for _ in range(quantidade):
                    if posse.tem_hotel:
                        posse.tem_hotel = False
                        posse.num_casas = 4
                        sala.hoteis_disponiveis += 1
                        sala.casas_disponiveis -= 4
                    elif posse.num_casas > 0:
                        posse.num_casas -= 1
                        sala.casas_disponiveis += 1

    sala_obj = db.query(Sala).filter_by(id=transacao.sala_id).first()
    if sala_obj:
        sala_obj.ultima_atividade = datetime.now(timezone.utc)

    return falidos


def _check_resultado_votos(transacao: Transacao, db: Session) -> Optional[str]:
    """Retorna 'aprovada', 'reprovada' ou None se ainda indeciso."""
    sala = db.query(Sala).filter_by(id=transacao.sala_id).first()
    votantes_ids = [
        j.id for j in sala.jogadores
        if j.status == "ativo"
        and j.id != transacao.origem_id
        and j.id != transacao.destino_id
    ]
    if not votantes_ids:
        return "aprovada"

    votos = db.query(Voto).filter_by(transacao_id=transacao.id).all()
    reprovacoes = sum(1 for v in votos if v.voto == "reprovado")

    maioria = (len(votantes_ids) // 2) + 1
    if reprovacoes >= maioria:
        return "reprovada"

    if len(votos) == len(votantes_ids):
        return "aprovada"

    return None


@router.post("", status_code=201)
async def criar_transacao(body: TransacaoCreate, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter_by(id=body.sala_id).first()
    if not sala or sala.status != "em_andamento":
        raise HTTPException(status_code=400, detail="Sala inválida ou partida não iniciada")

    jogador = db.query(Jogador).filter_by(
        session_token=body.session_token, sala_id=body.sala_id
    ).first()
    if not jogador or jogador.status != "ativo":
        raise HTTPException(status_code=403, detail="Jogador inativo ou sessão inválida")

    if body.tipo not in TIPOS_VALIDOS:
        raise HTTPException(status_code=400, detail="Tipo de transação inválido")

    # pagamento_banco: host solicita dinheiro do/para o banco
    if body.tipo == "pagamento_banco":
        host = db.query(Jogador).filter_by(id=sala.host_jogador_id).first()
        if not host or host.session_token != body.session_token:
            raise HTTPException(status_code=403, detail="Apenas o host pode solicitar pagamento ao banco")
        # origem_id_override presente → jogador paga ao banco
        # caso contrário → banco paga ao jogador (destino_id)
        origem = body.origem_id_override
        destino = None if body.origem_id_override else body.destino_id
    elif body.tipo in ("hipoteca", "venda_casa"):
        # banco paga ao jogador
        origem = None
        destino = jogador.id
    elif body.tipo == "aluguel":
        # quem foi cobrado (body.destino_id) paga; jogador (cobrador) recebe
        origem = body.destino_id
        destino = jogador.id
    else:
        origem = jogador.id
        destino = body.destino_id

    transacao = Transacao(
        sala_id=body.sala_id,
        tipo=body.tipo,
        valor=body.valor,
        origem_id=origem,
        destino_id=destino,
        propriedade_id=body.propriedade_id,
        descricao=body.descricao,
        status="pendente",
    )

    db.add(transacao)
    db.commit()
    db.refresh(transacao)

    # Verificar se há outros votantes; se não houver, aprovar direto
    votantes = [
        j for j in sala.jogadores
        if j.status == "ativo"
        and j.id != transacao.origem_id
        and j.id != transacao.destino_id
    ]
    if not votantes:
        transacao.status = "aprovada"
        transacao.resolvida_em = datetime.now(timezone.utc)
        falidos = _resolve_transacao(transacao, db)
        db.commit()
        for falido_id in falidos:
            await manager.broadcast(body.sala_id, {
                "tipo": "jogador_falido", "dados": {"jogador_id": falido_id},
            })
        await manager.broadcast(body.sala_id, {
            "tipo": "transacao_aprovada",
            "dados": {"transacao_id": transacao.id},
        })
    else:
        await manager.broadcast(body.sala_id, {
            "tipo": "aprovacao_solicitada",
            "dados": {
                "transacao_id": transacao.id,
                "tipo": transacao.tipo,
                "valor": transacao.valor,
                "origem_id": transacao.origem_id,
                "destino_id": transacao.destino_id,
                "propriedade_id": transacao.propriedade_id,
                "descricao": transacao.descricao,
            },
        })

    return {"id": transacao.id, "status": transacao.status}


@router.post("/{transacao_id}/votar")
async def votar(transacao_id: str, body: VotoCreate, db: Session = Depends(get_db)):
    transacao = db.query(Transacao).filter_by(id=transacao_id).first()
    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    if transacao.status != "pendente":
        raise HTTPException(status_code=400, detail="Transação já resolvida")

    jogador = db.query(Jogador).filter_by(
        session_token=body.session_token, sala_id=transacao.sala_id
    ).first()
    if not jogador:
        raise HTTPException(status_code=403, detail="Sessão inválida")
    if jogador.id in (transacao.origem_id, transacao.destino_id):
        raise HTTPException(status_code=400, detail="Você não pode votar na própria transação")

    existente = db.query(Voto).filter_by(
        transacao_id=transacao_id, jogador_id=jogador.id
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Você já votou")

    voto = Voto(transacao_id=transacao_id, jogador_id=jogador.id, voto=body.voto)
    db.add(voto)
    db.flush()

    resultado = _check_resultado_votos(transacao, db)
    falidos = []
    if resultado:
        transacao.status = resultado
        transacao.resolvida_em = datetime.now(timezone.utc)
        if resultado == "aprovada":
            falidos = _resolve_transacao(transacao, db)

    db.commit()

    tipo_evento = f"transacao_{resultado}" if resultado else "transacao_voto_registrado"
    dados_evento: dict = {"transacao_id": transacao_id, "status": transacao.status}
    if not resultado:
        dados_evento["jogador_id"] = jogador.id
        dados_evento["voto"] = body.voto

    await manager.broadcast(transacao.sala_id, {"tipo": tipo_evento, "dados": dados_evento})

    for falido_id in falidos:
        await manager.broadcast(transacao.sala_id, {
            "tipo": "jogador_falido", "dados": {"jogador_id": falido_id},
        })

    return {"status": transacao.status}


@router.post("/{transacao_id}/resolver")
async def resolver_por_timeout(transacao_id: str, session_token: str, db: Session = Depends(get_db)):
    """Chamado pelo frontend quando o timer de 10s expira."""
    transacao = db.query(Transacao).filter_by(id=transacao_id).first()
    if not transacao or transacao.status != "pendente":
        return {"status": transacao.status if transacao else "not_found"}

    jogador = db.query(Jogador).filter_by(
        session_token=session_token, sala_id=transacao.sala_id
    ).first()
    if not jogador:
        raise HTTPException(status_code=403, detail="Sessão inválida")

    resultado = _check_resultado_votos(transacao, db)
    resultado = resultado or "aprovada"
    agora = datetime.now(timezone.utc)

    # UPDATE atômico: apenas o primeiro resolver que chegar executa (evita race condition)
    updated = db.execute(
        sql_update(Transacao)
        .where(Transacao.id == transacao_id, Transacao.status == "pendente")
        .values(status=resultado, resolvida_em=agora)
    )
    if updated.rowcount == 0:
        db.rollback()
        return {"status": transacao.status}

    falidos = []
    if resultado == "aprovada":
        falidos = _resolve_transacao(transacao, db)
    db.commit()

    for falido_id in falidos:
        await manager.broadcast(transacao.sala_id, {
            "tipo": "jogador_falido", "dados": {"jogador_id": falido_id},
        })

    await manager.broadcast(transacao.sala_id, {
        "tipo": f"transacao_{resultado}",
        "dados": {"transacao_id": transacao_id, "status": resultado},
    })
    return {"status": resultado}


@router.post("/{transacao_id}/estornar")
async def estornar(transacao_id: str, session_token: str, db: Session = Depends(get_db)):
    transacao = db.query(Transacao).filter_by(id=transacao_id).first()
    if not transacao or transacao.status != "aprovada":
        raise HTTPException(status_code=400, detail="Transação não encontrada ou não aprovada")

    sala = db.query(Sala).filter_by(id=transacao.sala_id).first()
    host = db.query(Jogador).filter_by(id=sala.host_jogador_id).first()
    if not host or host.session_token != session_token:
        raise HTTPException(status_code=403, detail="Apenas o host pode estornar")

    # Reverter efeito financeiro
    if transacao.origem_id:
        origem = db.query(Jogador).filter_by(id=transacao.origem_id).first()
        if origem:
            origem.saldo += transacao.valor
            if origem.status == "falido" and origem.saldo > 0:
                origem.status = "ativo"

    if transacao.destino_id:
        destino = db.query(Jogador).filter_by(id=transacao.destino_id).first()
        if destino:
            destino.saldo -= transacao.valor

    # Reverter efeito sobre propriedades
    if transacao.propriedade_id:
        posse = db.query(PossePropriedade).filter_by(
            sala_id=transacao.sala_id,
            propriedade_id=transacao.propriedade_id,
        ).first()
        sala_p = db.query(Sala).filter_by(id=transacao.sala_id).first()
        if posse:
            if transacao.tipo == "compra_propriedade":
                posse.jogador_id = None
            elif transacao.tipo == "hipoteca":
                posse.hipotecada = False
            elif transacao.tipo == "recuperar_hipoteca":
                posse.hipotecada = True
            elif transacao.tipo == "compra_casa" and sala_p:
                prop = posse.propriedade if posse else None
                if posse.tem_hotel:
                    quantidade = 1
                elif prop and prop.custo_casa and prop.custo_casa > 0:
                    quantidade = max(1, round(transacao.valor / prop.custo_casa))
                else:
                    quantidade = 1
                for _ in range(quantidade):
                    if posse.tem_hotel:
                        posse.tem_hotel = False
                        posse.num_casas = 4
                        sala_p.hoteis_disponiveis += 1
                        sala_p.casas_disponiveis -= 4
                    elif posse.num_casas > 0:
                        posse.num_casas -= 1
                        sala_p.casas_disponiveis += 1
            elif transacao.tipo == "venda_casa" and sala_p:
                prop = posse.propriedade if posse else None
                if posse.num_casas == 4:
                    quantidade = 1  # desfaz venda de hotel
                elif prop and prop.custo_casa and prop.custo_casa > 0:
                    half = prop.custo_casa // 2 or 1
                    quantidade = max(1, round(transacao.valor / half))
                else:
                    quantidade = 1
                for _ in range(quantidade):
                    if posse.num_casas == 4:
                        posse.tem_hotel = True
                        posse.num_casas = 0
                        sala_p.hoteis_disponiveis -= 1
                        sala_p.casas_disponiveis += 4
                    else:
                        posse.num_casas += 1
                        sala_p.casas_disponiveis -= 1

    transacao.status = "estornada"

    estorno = Transacao(
        sala_id=transacao.sala_id,
        tipo="estorno",
        valor=transacao.valor,
        origem_id=transacao.destino_id,
        destino_id=transacao.origem_id,
        estorno_de=transacao.id,
        descricao=f"Estorno de transação {transacao.id[:8]}",
        status="aprovada",
        resolvida_em=datetime.now(timezone.utc),
    )
    db.add(estorno)
    db.commit()

    await manager.broadcast(transacao.sala_id, {
        "tipo": "transacao_estornada",
        "dados": {"transacao_id": transacao_id},
    })
    return {"ok": True}


@router.get("/sala/{sala_id}")
def listar_transacoes(sala_id: str, db: Session = Depends(get_db)):
    transacoes = (
        db.query(Transacao)
        .filter_by(sala_id=sala_id)
        .order_by(Transacao.criada_em.desc())
        .limit(50)
        .all()
    )
    return [
        {
            "id": t.id,
            "tipo": t.tipo,
            "valor": t.valor,
            "origem_id": t.origem_id,
            "destino_id": t.destino_id,
            "propriedade_id": t.propriedade_id,
            "status": t.status,
            "descricao": t.descricao,
            "criada_em": t.criada_em.isoformat(),
            "resolvida_em": t.resolvida_em.isoformat() if t.resolvida_em else None,
        }
        for t in transacoes
    ]
