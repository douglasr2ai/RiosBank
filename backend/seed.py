"""
Catálogo de propriedades do Super Banco Imobiliário (versão aproximada).
Todos os valores em centavos (R$1 = 100).
TODO: Confirmar valores exatos com o manual do jogo físico.
"""
from sqlalchemy.orm import Session
from models import Propriedade

VERSAO = "super_banco_imobiliario"

# Saldo inicial por versão do jogo (em centavos)
SALDO_INICIAL = {
    "super_banco_imobiliario": 1_500_000,  # R$15.000
}

PROPRIEDADES = [
    # ── ROXO ────────────────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "roxo", "cor_hex": "#9C27B0",
        "nome": "Av. Mediterrânea",
        "valor_compra": 60_000, "valor_hipoteca": 30_000, "custo_casa": 50_000, "custo_hotel": 50_000,
        "aluguel_sem_casa": 200, "aluguel_1_casa": 1_000,
        "aluguel_2_casas": 3_000, "aluguel_3_casas": 9_000,
        "aluguel_4_casas": 16_000, "aluguel_hotel": 25_000,
    },
    {
        "tipo": "rua", "grupo_cor": "roxo", "cor_hex": "#9C27B0",
        "nome": "Av. Báltica",
        "valor_compra": 60_000, "valor_hipoteca": 30_000, "custo_casa": 50_000, "custo_hotel": 50_000,
        "aluguel_sem_casa": 400, "aluguel_1_casa": 2_000,
        "aluguel_2_casas": 6_000, "aluguel_3_casas": 18_000,
        "aluguel_4_casas": 32_000, "aluguel_hotel": 45_000,
    },
    # ── AZUL CLARO ──────────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "azul_claro", "cor_hex": "#4FC3F7",
        "nome": "Av. Oriental",
        "valor_compra": 100_000, "valor_hipoteca": 50_000, "custo_casa": 50_000, "custo_hotel": 50_000,
        "aluguel_sem_casa": 600, "aluguel_1_casa": 3_000,
        "aluguel_2_casas": 9_000, "aluguel_3_casas": 27_000,
        "aluguel_4_casas": 40_000, "aluguel_hotel": 55_000,
    },
    {
        "tipo": "rua", "grupo_cor": "azul_claro", "cor_hex": "#4FC3F7",
        "nome": "Av. Vermont",
        "valor_compra": 100_000, "valor_hipoteca": 50_000, "custo_casa": 50_000, "custo_hotel": 50_000,
        "aluguel_sem_casa": 600, "aluguel_1_casa": 3_000,
        "aluguel_2_casas": 9_000, "aluguel_3_casas": 27_000,
        "aluguel_4_casas": 40_000, "aluguel_hotel": 55_000,
    },
    {
        "tipo": "rua", "grupo_cor": "azul_claro", "cor_hex": "#4FC3F7",
        "nome": "Av. Connecticut",
        "valor_compra": 120_000, "valor_hipoteca": 60_000, "custo_casa": 50_000, "custo_hotel": 50_000,
        "aluguel_sem_casa": 800, "aluguel_1_casa": 4_000,
        "aluguel_2_casas": 10_000, "aluguel_3_casas": 30_000,
        "aluguel_4_casas": 45_000, "aluguel_hotel": 60_000,
    },
    # ── ROSA ────────────────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "rosa", "cor_hex": "#E91E63",
        "nome": "Av. St. Charles",
        "valor_compra": 140_000, "valor_hipoteca": 70_000, "custo_casa": 100_000, "custo_hotel": 100_000,
        "aluguel_sem_casa": 1_000, "aluguel_1_casa": 5_000,
        "aluguel_2_casas": 15_000, "aluguel_3_casas": 45_000,
        "aluguel_4_casas": 62_500, "aluguel_hotel": 75_000,
    },
    {
        "tipo": "rua", "grupo_cor": "rosa", "cor_hex": "#E91E63",
        "nome": "Av. dos Estados",
        "valor_compra": 140_000, "valor_hipoteca": 70_000, "custo_casa": 100_000, "custo_hotel": 100_000,
        "aluguel_sem_casa": 1_000, "aluguel_1_casa": 5_000,
        "aluguel_2_casas": 15_000, "aluguel_3_casas": 45_000,
        "aluguel_4_casas": 62_500, "aluguel_hotel": 75_000,
    },
    {
        "tipo": "rua", "grupo_cor": "rosa", "cor_hex": "#E91E63",
        "nome": "Av. Virginia",
        "valor_compra": 160_000, "valor_hipoteca": 80_000, "custo_casa": 100_000, "custo_hotel": 100_000,
        "aluguel_sem_casa": 1_200, "aluguel_1_casa": 6_000,
        "aluguel_2_casas": 18_000, "aluguel_3_casas": 50_000,
        "aluguel_4_casas": 70_000, "aluguel_hotel": 90_000,
    },
    # ── LARANJA ─────────────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "laranja", "cor_hex": "#FF9800",
        "nome": "Av. St. James",
        "valor_compra": 180_000, "valor_hipoteca": 90_000, "custo_casa": 100_000, "custo_hotel": 100_000,
        "aluguel_sem_casa": 1_400, "aluguel_1_casa": 7_000,
        "aluguel_2_casas": 20_000, "aluguel_3_casas": 55_000,
        "aluguel_4_casas": 75_000, "aluguel_hotel": 95_000,
    },
    {
        "tipo": "rua", "grupo_cor": "laranja", "cor_hex": "#FF9800",
        "nome": "Av. Tennessee",
        "valor_compra": 180_000, "valor_hipoteca": 90_000, "custo_casa": 100_000, "custo_hotel": 100_000,
        "aluguel_sem_casa": 1_400, "aluguel_1_casa": 7_000,
        "aluguel_2_casas": 20_000, "aluguel_3_casas": 55_000,
        "aluguel_4_casas": 75_000, "aluguel_hotel": 95_000,
    },
    {
        "tipo": "rua", "grupo_cor": "laranja", "cor_hex": "#FF9800",
        "nome": "Av. New York",
        "valor_compra": 200_000, "valor_hipoteca": 100_000, "custo_casa": 100_000, "custo_hotel": 100_000,
        "aluguel_sem_casa": 1_600, "aluguel_1_casa": 8_000,
        "aluguel_2_casas": 22_000, "aluguel_3_casas": 60_000,
        "aluguel_4_casas": 80_000, "aluguel_hotel": 100_000,
    },
    # ── VERMELHO ────────────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "vermelho", "cor_hex": "#F44336",
        "nome": "Av. Kentucky",
        "valor_compra": 220_000, "valor_hipoteca": 110_000, "custo_casa": 150_000, "custo_hotel": 150_000,
        "aluguel_sem_casa": 1_800, "aluguel_1_casa": 9_000,
        "aluguel_2_casas": 25_000, "aluguel_3_casas": 70_000,
        "aluguel_4_casas": 87_500, "aluguel_hotel": 105_000,
    },
    {
        "tipo": "rua", "grupo_cor": "vermelho", "cor_hex": "#F44336",
        "nome": "Av. Indiana",
        "valor_compra": 220_000, "valor_hipoteca": 110_000, "custo_casa": 150_000, "custo_hotel": 150_000,
        "aluguel_sem_casa": 1_800, "aluguel_1_casa": 9_000,
        "aluguel_2_casas": 25_000, "aluguel_3_casas": 70_000,
        "aluguel_4_casas": 87_500, "aluguel_hotel": 105_000,
    },
    {
        "tipo": "rua", "grupo_cor": "vermelho", "cor_hex": "#F44336",
        "nome": "Av. Illinois",
        "valor_compra": 240_000, "valor_hipoteca": 120_000, "custo_casa": 150_000, "custo_hotel": 150_000,
        "aluguel_sem_casa": 2_000, "aluguel_1_casa": 10_000,
        "aluguel_2_casas": 30_000, "aluguel_3_casas": 75_000,
        "aluguel_4_casas": 92_500, "aluguel_hotel": 110_000,
    },
    # ── AMARELO ─────────────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "amarelo", "cor_hex": "#FFEB3B",
        "nome": "Av. Atlantic",
        "valor_compra": 260_000, "valor_hipoteca": 130_000, "custo_casa": 150_000, "custo_hotel": 150_000,
        "aluguel_sem_casa": 2_200, "aluguel_1_casa": 11_000,
        "aluguel_2_casas": 33_000, "aluguel_3_casas": 80_000,
        "aluguel_4_casas": 97_500, "aluguel_hotel": 115_000,
    },
    {
        "tipo": "rua", "grupo_cor": "amarelo", "cor_hex": "#FFEB3B",
        "nome": "Av. Ventnor",
        "valor_compra": 260_000, "valor_hipoteca": 130_000, "custo_casa": 150_000, "custo_hotel": 150_000,
        "aluguel_sem_casa": 2_200, "aluguel_1_casa": 11_000,
        "aluguel_2_casas": 33_000, "aluguel_3_casas": 80_000,
        "aluguel_4_casas": 97_500, "aluguel_hotel": 115_000,
    },
    {
        "tipo": "rua", "grupo_cor": "amarelo", "cor_hex": "#FFEB3B",
        "nome": "Av. Marvin Gardens",
        "valor_compra": 280_000, "valor_hipoteca": 140_000, "custo_casa": 150_000, "custo_hotel": 150_000,
        "aluguel_sem_casa": 2_400, "aluguel_1_casa": 12_000,
        "aluguel_2_casas": 36_000, "aluguel_3_casas": 85_000,
        "aluguel_4_casas": 102_500, "aluguel_hotel": 120_000,
    },
    # ── VERDE ───────────────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "verde", "cor_hex": "#4CAF50",
        "nome": "Av. Pacific",
        "valor_compra": 300_000, "valor_hipoteca": 150_000, "custo_casa": 200_000, "custo_hotel": 200_000,
        "aluguel_sem_casa": 2_600, "aluguel_1_casa": 13_000,
        "aluguel_2_casas": 39_000, "aluguel_3_casas": 90_000,
        "aluguel_4_casas": 110_000, "aluguel_hotel": 127_500,
    },
    {
        "tipo": "rua", "grupo_cor": "verde", "cor_hex": "#4CAF50",
        "nome": "Av. North Carolina",
        "valor_compra": 300_000, "valor_hipoteca": 150_000, "custo_casa": 200_000, "custo_hotel": 200_000,
        "aluguel_sem_casa": 2_600, "aluguel_1_casa": 13_000,
        "aluguel_2_casas": 39_000, "aluguel_3_casas": 90_000,
        "aluguel_4_casas": 110_000, "aluguel_hotel": 127_500,
    },
    {
        "tipo": "rua", "grupo_cor": "verde", "cor_hex": "#4CAF50",
        "nome": "Av. Pennsylvania",
        "valor_compra": 320_000, "valor_hipoteca": 160_000, "custo_casa": 200_000, "custo_hotel": 200_000,
        "aluguel_sem_casa": 2_800, "aluguel_1_casa": 15_000,
        "aluguel_2_casas": 45_000, "aluguel_3_casas": 100_000,
        "aluguel_4_casas": 120_000, "aluguel_hotel": 140_000,
    },
    # ── AZUL ESCURO ─────────────────────────────────────────────────────────
    {
        "tipo": "rua", "grupo_cor": "azul_escuro", "cor_hex": "#1565C0",
        "nome": "Av. Park Place",
        "valor_compra": 350_000, "valor_hipoteca": 175_000, "custo_casa": 200_000, "custo_hotel": 200_000,
        "aluguel_sem_casa": 3_500, "aluguel_1_casa": 17_500,
        "aluguel_2_casas": 50_000, "aluguel_3_casas": 110_000,
        "aluguel_4_casas": 130_000, "aluguel_hotel": 150_000,
    },
    {
        "tipo": "rua", "grupo_cor": "azul_escuro", "cor_hex": "#1565C0",
        "nome": "Av. Boardwalk",
        "valor_compra": 400_000, "valor_hipoteca": 200_000, "custo_casa": 200_000, "custo_hotel": 200_000,
        "aluguel_sem_casa": 5_000, "aluguel_1_casa": 20_000,
        "aluguel_2_casas": 60_000, "aluguel_3_casas": 140_000,
        "aluguel_4_casas": 170_000, "aluguel_hotel": 200_000,
    },
    # ── AÇÕES (dado × multiplicador) ────────────────────────────────────────
    {
        "tipo": "acao", "grupo_cor": None, "cor_hex": "#78909C",
        "nome": "Companhia Elétrica",
        "valor_compra": 150_000, "valor_hipoteca": 75_000,
        "multiplicador_dado": 40_000,  # aluguel = dado × R$400
    },
    {
        "tipo": "acao", "grupo_cor": None, "cor_hex": "#78909C",
        "nome": "Companhia de Águas",
        "valor_compra": 150_000, "valor_hipoteca": 75_000,
        "multiplicador_dado": 40_000,  # aluguel = dado × R$400
    },
]


def seed_propriedades(db: Session):
    existing = db.query(Propriedade).filter_by(versao_jogo=VERSAO).first()
    if existing:
        return

    for data in PROPRIEDADES:
        prop = Propriedade(versao_jogo=VERSAO, **data)
        db.add(prop)
    db.commit()
