from __future__ import annotations
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel


# ── Sala ──────────────────────────────────────────────────────────────────

class SalaCreate(BaseModel):
    nome: str
    senha: str
    versao_jogo: str = "super_banco_imobiliario"
    nome_jogador: str


class SalaBusca(BaseModel):
    nome: str
    senha: str
    nome_jogador: str


class SalaEntrarPorCodigo(BaseModel):
    codigo: str
    senha: str
    nome_jogador: str


class JoinByLink(BaseModel):
    link_token: str
    nome_jogador: str


class SalaInfo(BaseModel):
    id: str
    nome: str
    link_token: str
    status: str
    versao_jogo: str
    casas_disponiveis: int
    hoteis_disponiveis: int
    host_jogador_id: Optional[str]

    class Config:
        from_attributes = True


# ── Jogador ───────────────────────────────────────────────────────────────

class JogadorInfo(BaseModel):
    id: str
    nome: str
    saldo: int
    status: str
    ordem_entrada: int

    class Config:
        from_attributes = True


class JogadorDetalhado(JogadorInfo):
    session_token: str

    class Config:
        from_attributes = True


class EntrarSalaResponse(BaseModel):
    sala: SalaInfo
    jogador: JogadorDetalhado


class ReconnectRequest(BaseModel):
    session_token: str


# ── Transação ─────────────────────────────────────────────────────────────

class TransacaoCreate(BaseModel):
    sala_id: str
    session_token: str
    tipo: str
    valor: int
    destino_id: Optional[str] = None
    origem_id_override: Optional[str] = None  # usado por pagamento_banco para indicar quem paga
    propriedade_id: Optional[int] = None
    descricao: Optional[str] = None
    negociacao_dados: Optional[dict] = None


class VotoCreate(BaseModel):
    session_token: str
    voto: str  # aprovado | reprovado


class TransacaoInfo(BaseModel):
    id: str
    tipo: str
    valor: int
    origem_id: Optional[str]
    destino_id: Optional[str]
    propriedade_id: Optional[int]
    status: str
    descricao: Optional[str]
    criada_em: datetime
    resolvida_em: Optional[datetime]

    class Config:
        from_attributes = True


# ── Propriedade ───────────────────────────────────────────────────────────

class PropriedadeInfo(BaseModel):
    id: int
    nome: str
    tipo: str
    grupo_cor: Optional[str]
    cor_hex: Optional[str]
    valor_compra: int
    valor_hipoteca: int
    multiplicador_dado: Optional[int]
    aluguel_sem_casa: Optional[int]
    aluguel_1_casa: Optional[int]
    aluguel_2_casas: Optional[int]
    aluguel_3_casas: Optional[int]
    aluguel_4_casas: Optional[int]
    aluguel_hotel: Optional[int]
    custo_casa: Optional[int]
    custo_hotel: Optional[int]

    class Config:
        from_attributes = True


class PosseInfo(BaseModel):
    id: str
    propriedade_id: int
    jogador_id: Optional[str]
    hipotecada: bool
    num_casas: int
    tem_hotel: bool
    propriedade: PropriedadeInfo

    class Config:
        from_attributes = True


class PropriedadeAcao(BaseModel):
    session_token: str
    sala_id: str


# ── Leilão ────────────────────────────────────────────────────────────────

class LeilaoCreate(BaseModel):
    sala_id: str
    session_token: str
    propriedade_id: int


class LanceCreate(BaseModel):
    session_token: str
    incremento: int  # 10000 | 50000 | 100000 (R$100/R$500/R$1000 em centavos)


class LeilaoInfo(BaseModel):
    id: str
    sala_id: str
    propriedade_id: int
    iniciado_por: str
    lance_atual: int
    lider_id: Optional[str]
    status: str
    iniciado_em: datetime
    encerrado_em: Optional[datetime]

    class Config:
        from_attributes = True


# ── Histórico ─────────────────────────────────────────────────────────────

class HistoricoBusca(BaseModel):
    codigo: str
    senha: str


class HistoricoInfo(BaseModel):
    id: str
    nome_sala: str
    jogadores_count: int
    iniciada_em: datetime
    encerrada_em: datetime
    duracao_minutos: int
    vencedor_nome: str
    total_transacoes: int
    ranking: Any

    class Config:
        from_attributes = True


# ── WebSocket eventos (payload) ───────────────────────────────────────────

class WSEvento(BaseModel):
    tipo: str
    dados: Any
