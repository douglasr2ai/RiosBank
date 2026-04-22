"""
Catálogo de propriedades do Super Banco Imobiliário.
Todos os valores em centavos (R$1 = 100).
PENDENTE: valor_compra de cada propriedade — preencher com os valores do tabuleiro.
"""
from sqlalchemy.orm import Session
from models import Propriedade

VERSAO = "super_banco_imobiliario"

SALDO_INICIAL = {
    "super_banco_imobiliario": 2_500_000,  # R$25.000
}

PROPRIEDADES = [
    # ── VERDE CLARO (3) ──────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "verde_claro", "cor_hex": "#8BC34A",
        "nome": "Av. Beira Mar",
        "valor_compra": 0, "valor_hipoteca": 50_000,
        "custo_casa": 50_000, "custo_hotel": 50_000,
        "aluguel_sem_casa": 2_000, "aluguel_1_casa": 10_000,
        "aluguel_2_casas": 30_000, "aluguel_3_casas": 90_000,
        "aluguel_4_casas": 160_000, "aluguel_hotel": 250_000,
    },
    {
        "tipo": "rua", "grupo_cor": "verde_claro", "cor_hex": "#8BC34A",
        "nome": "Av. Brasil",
        "valor_compra": 0, "valor_hipoteca": 50_000,
        "custo_casa": 50_000, "custo_hotel": 50_000,
        "aluguel_sem_casa": 4_000, "aluguel_1_casa": 20_000,
        "aluguel_2_casas": 60_000, "aluguel_3_casas": 180_000,
        "aluguel_4_casas": 320_000, "aluguel_hotel": 450_000,
    },
    {
        "tipo": "rua", "grupo_cor": "verde_claro", "cor_hex": "#8BC34A",
        "nome": "Av. 9 de Julho",
        "valor_compra": 0, "valor_hipoteca": 50_000,
        "custo_casa": 50_000, "custo_hotel": 50_000,
        "aluguel_sem_casa": 6_000, "aluguel_1_casa": 30_000,
        "aluguel_2_casas": 90_000, "aluguel_3_casas": 270_000,
        "aluguel_4_casas": 400_000, "aluguel_hotel": 500_000,
    },
    # ── ROXO (2) ─────────────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "roxo", "cor_hex": "#9C27B0",
        "nome": "Av. Ipiranga",
        "valor_compra": 0, "valor_hipoteca": 50_000,
        "custo_casa": 50_000, "custo_hotel": 50_000,
        "aluguel_sem_casa": 6_000, "aluguel_1_casa": 30_000,
        "aluguel_2_casas": 90_000, "aluguel_3_casas": 270_000,
        "aluguel_4_casas": 400_000, "aluguel_hotel": 500_000,
    },
    {
        "tipo": "rua", "grupo_cor": "roxo", "cor_hex": "#9C27B0",
        "nome": "Av. São João",
        "valor_compra": 0, "valor_hipoteca": 60_000,
        "custo_casa": 50_000, "custo_hotel": 50_000,
        "aluguel_sem_casa": 8_000, "aluguel_1_casa": 40_000,
        "aluguel_2_casas": 100_000, "aluguel_3_casas": 300_000,
        "aluguel_4_casas": 450_000, "aluguel_hotel": 600_000,
    },
    # ── VERDE ESCURO (3) ─────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "verde_escuro", "cor_hex": "#388E3C",
        "nome": "Av. Recife",
        "valor_compra": 0, "valor_hipoteca": 70_000,
        "custo_casa": 100_000, "custo_hotel": 100_000,
        "aluguel_sem_casa": 10_000, "aluguel_1_casa": 50_000,
        "aluguel_2_casas": 150_000, "aluguel_3_casas": 450_000,
        "aluguel_4_casas": 625_000, "aluguel_hotel": 750_000,
    },
    {
        "tipo": "rua", "grupo_cor": "verde_escuro", "cor_hex": "#388E3C",
        "nome": "Av. Brigadeiro Faria Lima",
        "valor_compra": 0, "valor_hipoteca": 70_000,
        "custo_casa": 100_000, "custo_hotel": 100_000,
        "aluguel_sem_casa": 10_000, "aluguel_1_casa": 50_000,
        "aluguel_2_casas": 150_000, "aluguel_3_casas": 450_000,
        "aluguel_4_casas": 625_000, "aluguel_hotel": 750_000,
    },
    {
        "tipo": "rua", "grupo_cor": "verde_escuro", "cor_hex": "#388E3C",
        "nome": "Av. Paulista",
        "valor_compra": 0, "valor_hipoteca": 80_000,
        "custo_casa": 100_000, "custo_hotel": 100_000,
        "aluguel_sem_casa": 12_000, "aluguel_1_casa": 60_000,
        "aluguel_2_casas": 180_000, "aluguel_3_casas": 500_000,
        "aluguel_4_casas": 700_000, "aluguel_hotel": 900_000,
    },
    # ── AZUL CLARO (3) ───────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "azul_claro", "cor_hex": "#29B6F6",
        "nome": "R. da Consolação",
        "valor_compra": 0, "valor_hipoteca": 100_000,
        "custo_casa": 100_000, "custo_hotel": 100_000,
        "aluguel_sem_casa": 14_000, "aluguel_1_casa": 70_000,
        "aluguel_2_casas": 200_000, "aluguel_3_casas": 550_000,
        "aluguel_4_casas": 750_000, "aluguel_hotel": 950_000,
    },
    {
        "tipo": "rua", "grupo_cor": "azul_claro", "cor_hex": "#29B6F6",
        "nome": "Av. Santo Amaro",
        "valor_compra": 0, "valor_hipoteca": 100_000,
        "custo_casa": 100_000, "custo_hotel": 100_000,
        "aluguel_sem_casa": 14_000, "aluguel_1_casa": 70_000,
        "aluguel_2_casas": 200_000, "aluguel_3_casas": 550_000,
        "aluguel_4_casas": 750_000, "aluguel_hotel": 950_000,
    },
    {
        "tipo": "rua", "grupo_cor": "azul_claro", "cor_hex": "#29B6F6",
        "nome": "Av. Rebouças",
        "valor_compra": 0, "valor_hipoteca": 100_000,
        "custo_casa": 100_000, "custo_hotel": 100_000,
        "aluguel_sem_casa": 16_000, "aluguel_1_casa": 80_000,
        "aluguel_2_casas": 220_000, "aluguel_3_casas": 600_000,
        "aluguel_4_casas": 800_000, "aluguel_hotel": 1_000_000,
    },
    # ── VERMELHO (3) ─────────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "vermelho", "cor_hex": "#E53935",
        "nome": "Av. do Estado",
        "valor_compra": 0, "valor_hipoteca": 110_000,
        "custo_casa": 150_000, "custo_hotel": 150_000,
        "aluguel_sem_casa": 18_000, "aluguel_1_casa": 90_000,
        "aluguel_2_casas": 250_000, "aluguel_3_casas": 700_000,
        "aluguel_4_casas": 875_000, "aluguel_hotel": 1_050_000,
    },
    {
        "tipo": "rua", "grupo_cor": "vermelho", "cor_hex": "#E53935",
        "nome": "Av. do Contorno",
        "valor_compra": 0, "valor_hipoteca": 110_000,
        "custo_casa": 150_000, "custo_hotel": 150_000,
        "aluguel_sem_casa": 18_000, "aluguel_1_casa": 90_000,
        "aluguel_2_casas": 250_000, "aluguel_3_casas": 700_000,
        "aluguel_4_casas": 875_000, "aluguel_hotel": 1_050_000,
    },
    {
        "tipo": "rua", "grupo_cor": "vermelho", "cor_hex": "#E53935",
        "nome": "Av. Rio Branco",
        "valor_compra": 0, "valor_hipoteca": 120_000,
        "custo_casa": 150_000, "custo_hotel": 150_000,
        "aluguel_sem_casa": 20_000, "aluguel_1_casa": 100_000,
        "aluguel_2_casas": 300_000, "aluguel_3_casas": 750_000,
        "aluguel_4_casas": 925_000, "aluguel_hotel": 1_100_000,
    },
    # ── AMARELO (3) ──────────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "amarelo", "cor_hex": "#FDD835",
        "nome": "Av. Presidente Vargas",
        "valor_compra": 260_000, "valor_hipoteca": 130_000,
        "custo_casa": 150_000, "custo_hotel": 150_000,
        "aluguel_sem_casa": 22_000, "aluguel_1_casa": 110_000,
        "aluguel_2_casas": 333_000, "aluguel_3_casas": 800_000,
        "aluguel_4_casas": 975_000, "aluguel_hotel": 1_150_000,
    },
    {
        "tipo": "rua", "grupo_cor": "amarelo", "cor_hex": "#FDD835",
        "nome": "Av. Niemeyer",
        "valor_compra": 260_000, "valor_hipoteca": 130_000,
        "custo_casa": 150_000, "custo_hotel": 150_000,
        "aluguel_sem_casa": 22_000, "aluguel_1_casa": 110_000,
        "aluguel_2_casas": 330_000, "aluguel_3_casas": 800_000,
        "aluguel_4_casas": 975_000, "aluguel_hotel": 1_150_000,
    },
    {
        "tipo": "rua", "grupo_cor": "amarelo", "cor_hex": "#FDD835",
        "nome": "Av. Vieira Souto",
        "valor_compra": 280_000, "valor_hipoteca": 140_000,
        "custo_casa": 150_000, "custo_hotel": 150_000,
        "aluguel_sem_casa": 26_000, "aluguel_1_casa": 130_000,
        "aluguel_2_casas": 360_000, "aluguel_3_casas": 850_000,
        "aluguel_4_casas": 1_025_000, "aluguel_hotel": 1_200_000,
    },
    # ── LARANJA (3) ──────────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "laranja", "cor_hex": "#FB8C00",
        "nome": "R. Oscar Freire",
        "valor_compra": 300_000, "valor_hipoteca": 150_000,
        "custo_casa": 200_000, "custo_hotel": 200_000,
        "aluguel_sem_casa": 26_000, "aluguel_1_casa": 130_000,
        "aluguel_2_casas": 390_000, "aluguel_3_casas": 900_000,
        "aluguel_4_casas": 1_100_000, "aluguel_hotel": 1_275_000,
    },
    {
        "tipo": "rua", "grupo_cor": "laranja", "cor_hex": "#FB8C00",
        "nome": "Av. Ibirapuera",
        "valor_compra": 300_000, "valor_hipoteca": 150_000,
        "custo_casa": 200_000, "custo_hotel": 200_000,
        "aluguel_sem_casa": 26_000, "aluguel_1_casa": 130_000,
        "aluguel_2_casas": 390_000, "aluguel_3_casas": 900_000,
        "aluguel_4_casas": 1_100_000, "aluguel_hotel": 1_275_000,
    },
    {
        "tipo": "rua", "grupo_cor": "laranja", "cor_hex": "#FB8C00",
        "nome": "Av. Jucelino Kubitschek",
        "valor_compra": 320_000, "valor_hipoteca": 160_000,
        "custo_casa": 200_000, "custo_hotel": 200_000,
        "aluguel_sem_casa": 28_000, "aluguel_1_casa": 150_000,
        "aluguel_2_casas": 450_000, "aluguel_3_casas": 1_000_000,
        "aluguel_4_casas": 1_200_000, "aluguel_hotel": 1_400_000,
    },
    # ── ROSA (2) ─────────────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "rosa", "cor_hex": "#AD1457",
        "nome": "Av. Higienópolis",
        "valor_compra": 350_000, "valor_hipoteca": 175_000,
        "custo_casa": 200_000, "custo_hotel": 200_000,
        "aluguel_sem_casa": 35_000, "aluguel_1_casa": 175_000,
        "aluguel_2_casas": 500_000, "aluguel_3_casas": 1_100_000,
        "aluguel_4_casas": 1_300_000, "aluguel_hotel": 1_500_000,
    },
    {
        "tipo": "rua", "grupo_cor": "rosa", "cor_hex": "#AD1457",
        "nome": "Av. Morumbi",
        "valor_compra": 400_000, "valor_hipoteca": 200_000,
        "custo_casa": 200_000, "custo_hotel": 200_000,
        "aluguel_sem_casa": 50_000, "aluguel_1_casa": 200_000,
        "aluguel_2_casas": 600_000, "aluguel_3_casas": 1_400_000,
        "aluguel_4_casas": 1_700_000, "aluguel_hotel": 2_000_000,
    },
    # ── AÇÕES (6) — aluguel = soma dos dados × R$500 ─────────────────────────
    {
        "tipo": "acao", "grupo_cor": None, "cor_hex": "#78909C",
        "nome": "Emissora de TV",
        "valor_compra": 200_000, "valor_hipoteca": 100_000,
        "multiplicador_dado": 50_000,
    },
    {
        "tipo": "acao", "grupo_cor": None, "cor_hex": "#78909C",
        "nome": "Estrela Card",
        "valor_compra": 200_000, "valor_hipoteca": 100_000,
        "multiplicador_dado": 50_000,
    },
    {
        "tipo": "acao", "grupo_cor": None, "cor_hex": "#78909C",
        "nome": "Banco",
        "valor_compra": 200_000, "valor_hipoteca": 100_000,
        "multiplicador_dado": 50_000,
    },
    {
        "tipo": "acao", "grupo_cor": None, "cor_hex": "#78909C",
        "nome": "Petroleira",
        "valor_compra": 200_000, "valor_hipoteca": 100_000,
        "multiplicador_dado": 50_000,
    },
    {
        "tipo": "acao", "grupo_cor": None, "cor_hex": "#78909C",
        "nome": "E-Commerce",
        "valor_compra": 200_000, "valor_hipoteca": 100_000,
        "multiplicador_dado": 50_000,
    },
    {
        "tipo": "acao", "grupo_cor": None, "cor_hex": "#78909C",
        "nome": "Companhia Aérea",
        "valor_compra": 200_000, "valor_hipoteca": 100_000,
        "multiplicador_dado": 50_000,
    },
]


def seed_propriedades(db: Session):
    count_db = db.query(Propriedade).filter_by(versao_jogo=VERSAO).count()
    if count_db == len(PROPRIEDADES):
        return

    # Re-seed: remove registros antigos e insere os novos
    db.query(Propriedade).filter_by(versao_jogo=VERSAO).delete()
    for data in PROPRIEDADES:
        prop = Propriedade(versao_jogo=VERSAO, **data)
        db.add(prop)
    db.commit()
