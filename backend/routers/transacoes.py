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
    "pagamento_banco", "falencia", "estorno", "troca", "venda_banco",
}

TIPOS_COM_INSOLVENCIA = {"aluguel", "transferencia", "leilao", "pagamento_banco"}


def _liquidar_forcado(
    devedor: Jogador,
    valor_divida: int,
    credor_id: Optional[str],
    sala_id: str,
    db: Session,
) -> dict:
    """Liquida propriedades do devedor para abater dívida. Retorna resultado."""
    sala = db.query(Sala).filter_by(id=sala_id).first()
    credor = db.query(Jogador).filter_by(id=credor_id).first() if credor_id else None

    posses = db.query(PossePropriedade).filter_by(sala_id=sala_id, jogador_id=devedor.id).all()
    posses_ordenadas = sorted(posses, key=lambda p: p.propriedade.valor_compra)

    propriedades_liquidadas = []

    for posse in posses_ordenadas:
        if devedor.saldo >= valor_divida:
            break

        prop = posse.propriedade
        item = {
            "nome": prop.nome,
            "hipotecada": posse.hipotecada,
            "casas_vendidas": 0,
            "hotel_vendido": False,
            "valor_abatido": 0,
            "transferida_para": None,
        }

        if posse.hipotecada:
            # Credor assume a propriedade hipotecada (com casas intactas) pelo valor da hipoteca + 20%
            custo_assumir = int(prop.valor_hipoteca * 1.2)
            posse.jogador_id = credor.id if credor else None
            if credor:
                credor.saldo -= custo_assumir
            devedor.saldo += custo_assumir
            item["valor_abatido"] = custo_assumir
            item["transferida_para"] = credor.nome if credor else "Banco"
        else:
            valor_abatido = 0
            if posse.tem_hotel:
                half = (prop.custo_hotel or 0) // 2
                devedor.saldo += half
                valor_abatido += half
                item["hotel_vendido"] = True
                posse.tem_hotel = False
                if sala:
                    sala.hoteis_disponiveis += 1
            if posse.num_casas > 0:
                half_casa = (prop.custo_casa or 0) // 2
                total_casas = posse.num_casas * half_casa
                devedor.saldo += total_casas
                valor_abatido += total_casas
                item["casas_vendidas"] = posse.num_casas
                if sala:
                    sala.casas_disponiveis += posse.num_casas
                posse.num_casas = 0
            devedor.saldo += prop.valor_compra
            valor_abatido += prop.valor_compra
            item["valor_abatido"] = valor_abatido
            posse.jogador_id = None

        propriedades_liquidadas.append(item)

    # Pagar dívida com o arrecadado
    falido = False
    if devedor.saldo >= valor_divida:
        devedor.saldo -= valor_divida
        if credor:
            credor.saldo += valor_divida
    else:
        pagamento = devedor.saldo
        devedor.saldo = 0
        devedor.status = "falido"
        if credor:
            credor.saldo += pagamento
        falido = True

    return {
        "falido": falido,
        "saldo_final": devedor.saldo,
        "propriedades_liquidadas": propriedades_liquidadas,
    }


def _resolve_transacao(transacao: Transacao, db: Session) -> tuple:
    """Aplica efeitos financeiros de uma transação aprovada.
    Retorna (falidos, aviso_dict | None).
    aviso_dict["aviso"]=True → cobrança bloqueada (aviso de insolvência).
    aviso_dict["liquidacao"]=True → liquidação forçada executada.
    """
    falidos = []
    destino_ja_pago = False

    if transacao.tipo in (
        "transferencia", "aluguel", "compra_propriedade",
        "leilao", "pagamento_banco", "compra_casa",
        "venda_casa", "hipoteca", "recuperar_hipoteca", "troca", "venda_banco"
    ):
        if transacao.origem_id:
            origem = db.query(Jogador).filter_by(id=transacao.origem_id).first()
            if origem:
                insolvente = (
                    transacao.tipo in TIPOS_COM_INSOLVENCIA
                    and origem.saldo < transacao.valor
                )
                if insolvente:
                    posses_ativas = db.query(PossePropriedade).filter_by(
                        sala_id=transacao.sala_id, jogador_id=origem.id
                    ).all()

                    if not posses_ativas:
                        # Falência imediata — paga o que tem
                        credor = (
                            db.query(Jogador).filter_by(id=transacao.destino_id).first()
                            if transacao.destino_id else None
                        )
                        if credor:
                            credor.saldo += origem.saldo
                        destino_ja_pago = True
                        origem.saldo = 0
                        origem.status = "falido"
                        falidos.append(origem.id)

                    elif origem.avisos_cobranca < 2:
                        # Aviso 1 ou 2 — não aplica a cobrança
                        origem.avisos_cobranca += 1
                        transacao.status = "reprovada"
                        transacao.resolvida_em = datetime.now(timezone.utc)
                        credor = (
                            db.query(Jogador).filter_by(id=transacao.destino_id).first()
                            if transacao.destino_id else None
                        )
                        return falidos, {
                            "aviso": True,
                            "num": origem.avisos_cobranca,
                            "jogador_id": origem.id,
                            "nome": origem.nome,
                            "valor": transacao.valor,
                            "credor_id": transacao.destino_id,
                            "credor_nome": credor.nome if credor else "Banco",
                        }

                    else:
                        # 3º aviso → liquidação forçada
                        resultado = _liquidar_forcado(
                            origem, transacao.valor, transacao.destino_id, transacao.sala_id, db
                        )
                        destino_ja_pago = True
                        if resultado["falido"]:
                            falidos.append(origem.id)
                        sala_obj = db.query(Sala).filter_by(id=transacao.sala_id).first()
                        if sala_obj:
                            sala_obj.ultima_atividade = datetime.now(timezone.utc)
                        return falidos, {
                            "liquidacao": True,
                            "jogador_id": origem.id,
                            "nome": origem.nome,
                            "falido": resultado["falido"],
                            "saldo_final": resultado["saldo_final"],
                            "propriedades_liquidadas": resultado["propriedades_liquidadas"],
                        }
                else:
                    origem.saldo -= transacao.valor
                    if origem.saldo < 0:
                        origem.saldo = 0
                        origem.status = "falido"
                        falidos.append(origem.id)

        if transacao.destino_id and not destino_ja_pago:
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

        if transacao.tipo == "venda_banco" and transacao.propriedade_id:
            posse = db.query(PossePropriedade).filter_by(
                sala_id=transacao.sala_id,
                propriedade_id=transacao.propriedade_id,
            ).first()
            if posse:
                posse.jogador_id = None

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

    return falidos, None


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


async def _broadcast_resultado(sala_id: str, transacao_id: str, transacao_status: str, aviso: Optional[dict], falidos: list):
    """Faz broadcasts após resolução de transação."""
    for falido_id in falidos:
        await manager.broadcast(sala_id, {"tipo": "jogador_falido", "dados": {"jogador_id": falido_id}})

    if aviso and aviso.get("aviso"):
        await manager.broadcast(sala_id, {"tipo": "transacao_reprovada", "dados": {"transacao_id": transacao_id}})
        await manager.broadcast(sala_id, {"tipo": "devedor_insolvente", "dados": aviso})
    elif aviso and aviso.get("liquidacao"):
        await manager.broadcast(sala_id, {"tipo": "transacao_aprovada", "dados": {"transacao_id": transacao_id}})
        await manager.broadcast(sala_id, {"tipo": "liquidacao_forcada", "dados": aviso})
    else:
        await manager.broadcast(sala_id, {"tipo": f"transacao_{transacao_status}", "dados": {"transacao_id": transacao_id, "status": transacao_status}})


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

    if body.tipo == "pagamento_banco":
        host = db.query(Jogador).filter_by(id=sala.host_jogador_id).first()
        if not host or host.session_token != body.session_token:
            raise HTTPException(status_code=403, detail="Apenas o host pode solicitar pagamento ao banco")
        origem = body.origem_id_override
        destino = None if body.origem_id_override else body.destino_id
    elif body.tipo in ("hipoteca", "venda_casa"):
        origem = None
        destino = jogador.id
    elif body.tipo == "aluguel":
        origem = body.destino_id
        destino = jogador.id
    elif body.tipo == "venda_banco":
        if not body.propriedade_id:
            raise HTTPException(status_code=400, detail="propriedade_id obrigatório para venda_banco")
        posse_vb = db.query(PossePropriedade).filter_by(
            sala_id=body.sala_id,
            propriedade_id=body.propriedade_id,
            jogador_id=jogador.id,
        ).first()
        if not posse_vb:
            raise HTTPException(status_code=400, detail="Propriedade não pertence ao jogador")
        if posse_vb.hipotecada or posse_vb.num_casas > 0 or posse_vb.tem_hotel:
            raise HTTPException(status_code=400, detail="Venda benfeitorias e recupere hipoteca antes de vender ao banco")
        origem = None
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

    votantes = [
        j for j in sala.jogadores
        if j.status == "ativo"
        and j.id != transacao.origem_id
        and j.id != transacao.destino_id
    ]
    if not votantes:
        transacao.status = "aprovada"
        transacao.resolvida_em = datetime.now(timezone.utc)
        falidos, aviso = _resolve_transacao(transacao, db)
        db.commit()
        await _broadcast_resultado(body.sala_id, transacao.id, transacao.status, aviso, falidos)
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
    aviso = None
    if resultado:
        transacao.status = resultado
        transacao.resolvida_em = datetime.now(timezone.utc)
        if resultado == "aprovada":
            falidos, aviso = _resolve_transacao(transacao, db)

    db.commit()

    if resultado:
        await _broadcast_resultado(transacao.sala_id, transacao_id, transacao.status, aviso, falidos)
    else:
        await manager.broadcast(transacao.sala_id, {
            "tipo": "transacao_voto_registrado",
            "dados": {"transacao_id": transacao_id, "jogador_id": jogador.id, "voto": body.voto},
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

    resultado = _check_resultado_votos(transacao, db) or "aprovada"
    agora = datetime.now(timezone.utc)

    # UPDATE atômico para evitar race condition
    updated = db.execute(
        sql_update(Transacao)
        .where(Transacao.id == transacao_id, Transacao.status == "pendente")
        .values(status=resultado, resolvida_em=agora)
    )
    if updated.rowcount == 0:
        db.rollback()
        return {"status": transacao.status}

    falidos = []
    aviso = None
    if resultado == "aprovada":
        transacao.status = resultado
        transacao.resolvida_em = agora
        falidos, aviso = _resolve_transacao(transacao, db)

    db.commit()

    await _broadcast_resultado(transacao.sala_id, transacao_id, transacao.status, aviso, falidos)
    return {"status": transacao.status}


@router.post("/{transacao_id}/estornar")
async def estornar(transacao_id: str, session_token: str, db: Session = Depends(get_db)):
    transacao = db.query(Transacao).filter_by(id=transacao_id).first()
    if not transacao or transacao.status != "aprovada":
        raise HTTPException(status_code=400, detail="Transação não encontrada ou não aprovada")

    sala = db.query(Sala).filter_by(id=transacao.sala_id).first()
    host = db.query(Jogador).filter_by(id=sala.host_jogador_id).first()
    if not host or host.session_token != session_token:
        raise HTTPException(status_code=403, detail="Apenas o host pode estornar")

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

    if transacao.propriedade_id:
        posse = db.query(PossePropriedade).filter_by(
            sala_id=transacao.sala_id,
            propriedade_id=transacao.propriedade_id,
        ).first()
        sala_p = db.query(Sala).filter_by(id=transacao.sala_id).first()
        if posse:
            if transacao.tipo == "compra_propriedade":
                posse.jogador_id = None
            elif transacao.tipo == "venda_banco":
                posse.jogador_id = transacao.destino_id
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
                    quantidade = 1
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
