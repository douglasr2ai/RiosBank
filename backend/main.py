import os
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import engine, get_db, Base, SessionLocal
from models import Jogador, Sala
from ws_manager import manager
from seed import seed_propriedades

from routers import salas, jogadores, transacoes, propriedades, leiloes, historico


INATIVIDADE_LIMITE = timedelta(minutes=20)
INTERVALO_VERIFICACAO = 300  # 5 minutos


async def _tarefa_encerramento_inativo():
    """Encerra partidas em andamento sem atividade por INATIVIDADE_LIMITE."""
    while True:
        await asyncio.sleep(INTERVALO_VERIFICACAO)
        db = SessionLocal()
        try:
            agora = datetime.now(timezone.utc)
            salas_ativas = db.query(Sala).filter_by(status="em_andamento").all()
            for sala in salas_ativas:
                ult = sala.ultima_atividade
                if ult and ult.tzinfo is None:
                    ult = ult.replace(tzinfo=timezone.utc)
                if not ult or (agora - ult) >= INATIVIDADE_LIMITE:
                    try:
                        await salas._encerrar_sala_auto(sala, db)
                    except Exception as exc:
                        print(f"[auto-close] sala {sala.id}: {exc}")
        except Exception as exc:
            print(f"[auto-close] erro geral: {exc}")
        finally:
            db.close()


def _aplicar_migrations():
    """Aplica colunas novas em bancos já existentes (create_all não altera tabelas)."""
    with engine.connect() as conn:
        cols_jogadores = {row[1] for row in conn.execute(text("PRAGMA table_info(jogadores)"))}
        if "avisos_cobranca" not in cols_jogadores:
            conn.execute(text("ALTER TABLE jogadores ADD COLUMN avisos_cobranca INTEGER NOT NULL DEFAULT 0"))
            conn.commit()

        cols_salas = {row[1] for row in conn.execute(text("PRAGMA table_info(salas)"))}
        if "ultima_atividade" not in cols_salas:
            conn.execute(text("ALTER TABLE salas ADD COLUMN ultima_atividade DATETIME"))
            conn.commit()
        if "codigo" not in cols_salas:
            conn.execute(text("ALTER TABLE salas ADD COLUMN codigo VARCHAR(6)"))
            conn.commit()

        cols_historico = {row[1] for row in conn.execute(text("PRAGMA table_info(historico_partidas)"))}
        if "codigo" not in cols_historico:
            conn.execute(text("ALTER TABLE historico_partidas ADD COLUMN codigo VARCHAR(6)"))
            conn.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("data", exist_ok=True)
    Base.metadata.create_all(bind=engine)
    _aplicar_migrations()
    db = next(get_db())
    try:
        seed_propriedades(db)
    finally:
        db.close()
    task = asyncio.create_task(_tarefa_encerramento_inativo())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="RiosBank API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(salas.router)
app.include_router(jogadores.router)
app.include_router(transacoes.router)
app.include_router(propriedades.router)
app.include_router(leiloes.router)
app.include_router(historico.router)


@app.get("/health")
def health():
    return {"status": "ok"}


# ── WebSocket ─────────────────────────────────────────────────────────────

@app.websocket("/ws/{sala_id}/{session_token}")
async def websocket_endpoint(
    websocket: WebSocket,
    sala_id: str,
    session_token: str,
    db: Session = Depends(get_db),
):
    jogador = db.query(Jogador).filter_by(
        session_token=session_token, sala_id=sala_id
    ).first()

    if not jogador or jogador.status == "expulso":
        await websocket.close(code=4001)
        return

    sala = db.query(Sala).filter_by(id=sala_id).first()
    if not sala or sala.status == "encerrada":
        await websocket.close(code=4002)
        return

    await manager.connect(websocket, sala_id, session_token)

    # Notificar sala que jogador conectou/reconectou
    await manager.broadcast(sala_id, {
        "tipo": "jogador_conectado",
        "dados": {
            "jogador_id": jogador.id,
            "nome": jogador.nome,
            "saldo": jogador.saldo,
            "status": jogador.status,
            "ordem_entrada": jogador.ordem_entrada,
            "online": True,
        },
    })

    # Suceder host se necessário (host desconectado)
    _verificar_sucessao_host(sala_id, sala, db)

    try:
        while True:
            # Mensagens client → server (ping/keep-alive)
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, sala_id)

        # Notificar sala que jogador desconectou
        await manager.broadcast(sala_id, {
            "tipo": "jogador_desconectado",
            "dados": {"jogador_id": jogador.id, "nome": jogador.nome, "online": False},
        })

        # Verificar se o host desconectou e promover substituto
        db2 = SessionLocal()
        try:
            sala2 = db2.query(Sala).filter_by(id=sala_id).first()
            if sala2 and sala2.host_jogador_id == jogador.id:
                _verificar_sucessao_host(sala_id, sala2, db2, force=True)
        finally:
            db2.close()


def _verificar_sucessao_host(sala_id: str, sala: Sala, db: Session, force: bool = False):
    connected = manager.connected_tokens(sala_id)
    host = db.query(Jogador).filter_by(id=sala.host_jogador_id).first()

    if force or not host or host.session_token not in connected:
        # Promover o jogador ativo com menor ordem_entrada que está online
        ativos = (
            db.query(Jogador)
            .filter_by(sala_id=sala_id, status="ativo")
            .order_by(Jogador.ordem_entrada)
            .all()
        )
        for candidato in ativos:
            if candidato.session_token in connected and candidato.id != sala.host_jogador_id:
                sala.host_jogador_id = candidato.id
                db.commit()
                asyncio.create_task(
                    manager.broadcast(sala_id, {
                        "tipo": "host_alterado",
                        "dados": {"novo_host_id": candidato.id, "nome": candidato.nome},
                    })
                )
                break
