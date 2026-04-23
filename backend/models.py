import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from database import Base


def new_uuid():
    return str(uuid.uuid4())


def now_utc():
    return datetime.now(timezone.utc)


class Sala(Base):
    __tablename__ = "salas"

    id = Column(String, primary_key=True, default=new_uuid)
    nome = Column(String, nullable=False)
    senha_hash = Column(String, nullable=False)
    link_token = Column(String, nullable=False, unique=True, default=new_uuid)
    status = Column(String, nullable=False, default="lobby")  # lobby | em_andamento | encerrada
    host_jogador_id = Column(String, ForeignKey("jogadores.id"), nullable=True)
    casas_disponiveis = Column(Integer, nullable=False, default=32)
    hoteis_disponiveis = Column(Integer, nullable=False, default=12)
    versao_jogo = Column(String, nullable=False, default="super_banco_imobiliario")
    criada_em = Column(DateTime, default=now_utc)
    encerrada_em = Column(DateTime, nullable=True)
    ultima_atividade = Column(DateTime, nullable=True)

    jogadores = relationship(
        "Jogador", foreign_keys="Jogador.sala_id", back_populates="sala", cascade="all, delete-orphan"
    )
    posse_propriedades = relationship("PossePropriedade", back_populates="sala", cascade="all, delete-orphan")
    transacoes = relationship("Transacao", back_populates="sala", cascade="all, delete-orphan")
    leiloes = relationship("Leilao", back_populates="sala", cascade="all, delete-orphan")


class Jogador(Base):
    __tablename__ = "jogadores"

    id = Column(String, primary_key=True, default=new_uuid)
    sala_id = Column(String, ForeignKey("salas.id"), nullable=False)
    nome = Column(String, nullable=False)
    session_token = Column(String, nullable=False, unique=True, default=new_uuid)
    saldo = Column(Integer, nullable=False, default=0)
    status = Column(String, nullable=False, default="ativo")  # ativo | falido | expulso
    ordem_entrada = Column(Integer, nullable=False, default=0)
    avisos_cobranca = Column(Integer, nullable=False, default=0)
    criado_em = Column(DateTime, default=now_utc)

    sala = relationship("Sala", foreign_keys=[sala_id], back_populates="jogadores")
    posses = relationship("PossePropriedade", back_populates="jogador")
    votos = relationship("Voto", back_populates="jogador")
    lances = relationship("Lance", back_populates="jogador")


class Propriedade(Base):
    __tablename__ = "propriedades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    versao_jogo = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # rua | acao
    grupo_cor = Column(String, nullable=True)
    cor_hex = Column(String, nullable=True)
    valor_compra = Column(Integer, nullable=False)
    valor_hipoteca = Column(Integer, nullable=False)
    multiplicador_dado = Column(Integer, nullable=True)
    aluguel_sem_casa = Column(Integer, nullable=True)
    aluguel_1_casa = Column(Integer, nullable=True)
    aluguel_2_casas = Column(Integer, nullable=True)
    aluguel_3_casas = Column(Integer, nullable=True)
    aluguel_4_casas = Column(Integer, nullable=True)
    aluguel_hotel = Column(Integer, nullable=True)
    custo_casa = Column(Integer, nullable=True)
    custo_hotel = Column(Integer, nullable=True)

    posses = relationship("PossePropriedade", back_populates="propriedade")


class PossePropriedade(Base):
    __tablename__ = "posse_propriedades"

    id = Column(String, primary_key=True, default=new_uuid)
    sala_id = Column(String, ForeignKey("salas.id"), nullable=False)
    propriedade_id = Column(Integer, ForeignKey("propriedades.id"), nullable=False)
    jogador_id = Column(String, ForeignKey("jogadores.id"), nullable=True)  # null = banco
    hipotecada = Column(Boolean, nullable=False, default=False)
    num_casas = Column(Integer, nullable=False, default=0)
    tem_hotel = Column(Boolean, nullable=False, default=False)

    sala = relationship("Sala", back_populates="posse_propriedades")
    propriedade = relationship("Propriedade", back_populates="posses")
    jogador = relationship("Jogador", back_populates="posses")


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(String, primary_key=True, default=new_uuid)
    sala_id = Column(String, ForeignKey("salas.id"), nullable=False)
    tipo = Column(String, nullable=False)
    # tipos: transferencia | compra_propriedade | aluguel | hipoteca | recuperar_hipoteca
    #        compra_casa | venda_casa | leilao | pagamento_banco | falencia | estorno | troca
    valor = Column(Integer, nullable=False)
    origem_id = Column(String, ForeignKey("jogadores.id"), nullable=True)
    destino_id = Column(String, ForeignKey("jogadores.id"), nullable=True)
    propriedade_id = Column(Integer, ForeignKey("propriedades.id"), nullable=True)
    status = Column(String, nullable=False, default="pendente")  # pendente | aprovada | reprovada | estornada
    estorno_de = Column(String, ForeignKey("transacoes.id"), nullable=True)
    descricao = Column(Text, nullable=True)
    criada_em = Column(DateTime, default=now_utc)
    resolvida_em = Column(DateTime, nullable=True)

    sala = relationship("Sala", back_populates="transacoes")
    origem = relationship("Jogador", foreign_keys=[origem_id])
    destino = relationship("Jogador", foreign_keys=[destino_id])
    votos = relationship("Voto", back_populates="transacao", cascade="all, delete-orphan")


class Voto(Base):
    __tablename__ = "votos"

    id = Column(String, primary_key=True, default=new_uuid)
    transacao_id = Column(String, ForeignKey("transacoes.id"), nullable=False)
    jogador_id = Column(String, ForeignKey("jogadores.id"), nullable=False)
    voto = Column(String, nullable=False)  # aprovado | reprovado
    criado_em = Column(DateTime, default=now_utc)

    transacao = relationship("Transacao", back_populates="votos")
    jogador = relationship("Jogador", back_populates="votos")


class Leilao(Base):
    __tablename__ = "leiloes"

    id = Column(String, primary_key=True, default=new_uuid)
    sala_id = Column(String, ForeignKey("salas.id"), nullable=False)
    propriedade_id = Column(Integer, ForeignKey("propriedades.id"), nullable=False)
    iniciado_por = Column(String, ForeignKey("jogadores.id"), nullable=False)
    lance_atual = Column(Integer, nullable=False, default=0)
    lider_id = Column(String, ForeignKey("jogadores.id"), nullable=True)
    status = Column(String, nullable=False, default="ativo")  # ativo | encerrado
    iniciado_em = Column(DateTime, default=now_utc)
    encerrado_em = Column(DateTime, nullable=True)

    sala = relationship("Sala", back_populates="leiloes")
    lances = relationship("Lance", back_populates="leilao", cascade="all, delete-orphan")


class Lance(Base):
    __tablename__ = "lances"

    id = Column(String, primary_key=True, default=new_uuid)
    leilao_id = Column(String, ForeignKey("leiloes.id"), nullable=False)
    jogador_id = Column(String, ForeignKey("jogadores.id"), nullable=False)
    valor = Column(Integer, nullable=False)
    criado_em = Column(DateTime, default=now_utc)

    leilao = relationship("Leilao", back_populates="lances")
    jogador = relationship("Jogador", back_populates="lances")


class HistoricoPartida(Base):
    __tablename__ = "historico_partidas"

    id = Column(String, primary_key=True, default=new_uuid)
    nome_sala = Column(String, nullable=False)
    senha_hash = Column(String, nullable=False)
    link_token = Column(String, nullable=False, unique=True)
    jogadores_count = Column(Integer, nullable=False)
    iniciada_em = Column(DateTime, nullable=False)
    encerrada_em = Column(DateTime, nullable=False)
    duracao_minutos = Column(Integer, nullable=False)
    vencedor_nome = Column(String, nullable=False)
    total_transacoes = Column(Integer, nullable=False)
    ranking = Column(JSON, nullable=False)
