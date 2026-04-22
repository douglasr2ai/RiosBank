import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import Jogador, Sala
from ws_manager import manager
from seed import seed_propriedades

from routers import salas, jogadores, transacoes, propriedades, leiloes, historico


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("data", exist_ok=True)
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        seed_propriedades(db)
    finally:
        db.close()
    yield


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
        db2 = next(get_db())
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
                import asyncio
                asyncio.create_task(
                    manager.broadcast(sala_id, {
                        "tipo": "host_alterado",
                        "dados": {"novo_host_id": candidato.id, "nome": candidato.nome},
                    })
                )
                break
