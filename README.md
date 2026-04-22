# RiosBank

Banco digital em tempo real para partidas de **Super Banco Imobiliário**. Substitui o banco físico e as fichas — tudo pelo celular.

## O que é

Cada jogador acessa o app pelo navegador. Um jogador cria a sala e vira o **host**; os demais entram pelo link de convite. A partir daí:

- Transferências entre jogadores precisam de **aprovação coletiva** (maioria em 10 s)
- Propriedades são compradas, hipotecadas, construídas e leiloadas pelo app
- O host pode expulsar jogadores, estornar transações e encerrar a partida
- Histórico completo acessível após o fim da partida

## Pré-requisitos

| Ferramenta | Versão mínima |
|---|---|
| Docker + Docker Compose | Docker 24 |
| **ou** Python | 3.11+ |
| **ou** Node.js | 20+ |

---

## Rodando com Docker (recomendado)

```bash
# Na raiz do projeto
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend (API): http://localhost:8000

Para parar: `Ctrl+C` ou `docker compose down`

---

## Rodando localmente (sem Docker)

### Backend

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

> O arquivo `frontend/.env` já aponta para `localhost:8000` — não é necessário configurar nada.

---

## Como testar uma partida

1. Abra http://localhost:5173 em **duas abas** (ou dois dispositivos na mesma rede)
2. Na aba 1 → **Criar sala** → dê um nome e crie
3. Copie o link de convite que aparece no lobby
4. Na aba 2 → cole o link e entre com outro nome
5. Na aba 1 (host) → clique **Iniciar partida**

A partir daí use o painel do host para registrar transações e os jogadores para aprovar ou reprovar.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | Python · FastAPI · SQLAlchemy · SQLite (WAL) |
| Tempo real | WebSocket nativo |
| Frontend | Vue 3 · Pinia · Vite |
| Infra | Docker Compose |
