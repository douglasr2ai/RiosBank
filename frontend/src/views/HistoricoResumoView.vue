<template>
  <div class="page">
    <div class="wrap">
      <div class="top-row">
        <button class="back-btn" @click="$router.push({ name: 'landing' })">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
            <path d="M19 12H5M12 5l-7 7 7 7"/>
          </svg>
        </button>
        <div class="brand">Rios<span>Bank</span></div>
      </div>

      <div v-if="loading" class="loading text-muted">Carregando...</div>
      <div v-else-if="erro" class="erro-card glass">
        <p class="text-danger">{{ erro }}</p>
        <button class="btn btn-ghost" style="margin-top:8px" @click="$router.push({ name: 'historico-busca' })">Buscar manualmente</button>
      </div>
      <template v-else-if="historico">
        <!-- Meta -->
        <div class="meta-grid glass">
          <div class="meta-item">
            <p class="meta-label text-muted">Data</p>
            <p class="meta-val">{{ formatData(historico.encerrada_em) }}</p>
          </div>
          <div class="meta-item">
            <p class="meta-label text-muted">Duração</p>
            <p class="meta-val mono">{{ historico.duracao_minutos }}min</p>
          </div>
          <div class="meta-item">
            <p class="meta-label text-muted">Jogadores</p>
            <p class="meta-val mono">{{ historico.jogadores_count }}</p>
          </div>
          <div class="meta-item">
            <p class="meta-label text-muted">Transações</p>
            <p class="meta-val mono">{{ historico.total_transacoes }}</p>
          </div>
        </div>

        <!-- Vencedor -->
        <div class="vencedor-card glass">
          <div class="vencedor-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
          </div>
          <div>
            <p class="vencedor-label text-muted">Vencedor</p>
            <p class="vencedor-nome">{{ historico.vencedor_nome }}</p>
          </div>
          <div class="pos-badge gold">#1</div>
        </div>

        <!-- Ranking completo -->
        <p class="section-title">Ranking final</p>
        <div class="ranking-list">
          <div v-for="p in historico.ranking" :key="p.posicao" class="rank-item glass">
            <div class="pos-badge" :class="badgeClass(p.posicao)">#{{ p.posicao }}</div>
            <div class="rank-info">
              <p class="rank-nome">{{ p.nome }}</p>
              <div class="prop-chips">
                <div
                  v-for="prop in p.propriedades"
                  :key="prop.nome"
                  class="prop-chip"
                  :title="chipTitle(prop)"
                >
                  <span class="chip-dot" />
                  {{ prop.nome }}
                  <span v-if="prop.hotel" class="chip-tag hotel">H</span>
                  <span v-else-if="prop.casas > 0" class="chip-tag casas">{{ prop.casas }}</span>
                </div>
              </div>
            </div>
            <p class="rank-saldo mono text-green">{{ formatMoney(p.saldo_final) }}</p>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../stores/api'

const route = useRoute()
const historico = ref(null)
const loading = ref(true)
const erro = ref('')

const formatMoney = (val) => {
  if (!val && val !== 0) return 'R$ 0'
  return `R$ ${(val / 100).toLocaleString('pt-BR', { minimumFractionDigits: 0 })}`
}

const formatData = (iso) => {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('pt-BR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

const badgeClass = (pos) => {
  if (pos === 1) return 'gold'
  if (pos === 2) return 'silver'
  if (pos === 3) return 'bronze'
  return ''
}

const chipTitle = (prop) => {
  if (prop.tipo === 'acao') return `${prop.nome} (ação)`
  return `${prop.nome} · ${prop.casas || 0} casa(s)${prop.hotel ? ' · hotel' : ''}`
}

onMounted(async () => {
  const linkToken = route.params.linkToken
  try {
    historico.value = await api.get(`/historico/${linkToken}`)
  } catch (e) {
    erro.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page { min-height: 100dvh; display: flex; align-items: flex-start; justify-content: center; padding: 32px 20px 48px; position: relative; }
.wrap { width: 100%; max-width: 360px; display: flex; flex-direction: column; gap: 16px; position: relative; z-index: 1; }

.top-row { display: flex; align-items: center; gap: 12px; }
.back-btn { width: 38px; height: 38px; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.09); border-radius: 12px; cursor: pointer; color: var(--text-2); transition: all .2s; }
.back-btn:hover { background: rgba(255,255,255,.09); color: var(--text); }
.back-btn svg { width: 18px; height: 18px; }
.brand { font-size: 22px; font-weight: 800; letter-spacing: -.5px; }
.brand span { color: var(--green); }

.loading { font-size: 14px; text-align: center; padding: 48px 0; }
.erro-card { padding: 20px; text-align: center; }

.meta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0; padding: 18px; border-radius: var(--radius); }
.meta-item { padding: 8px 12px; }
.meta-label { font-size: 11px; margin-bottom: 3px; }
.meta-val { font-size: 14px; font-weight: 700; }

.vencedor-card { padding: 18px; display: flex; align-items: center; gap: 14px; }
.vencedor-icon { width: 44px; height: 44px; border-radius: 50%; background: rgba(246,173,85,.15); border: 1px solid rgba(246,173,85,.25); display: flex; align-items: center; justify-content: center; color: var(--amber); flex-shrink: 0; }
.vencedor-icon svg { width: 20px; height: 20px; }
.vencedor-label { font-size: 11px; margin-bottom: 2px; }
.vencedor-nome { font-size: 17px; font-weight: 800; }

.ranking-list { display: flex; flex-direction: column; gap: 8px; }
.rank-item { display: flex; align-items: flex-start; gap: 10px; padding: 14px; border-radius: 14px; }
.rank-info { flex: 1; min-width: 0; }
.rank-nome { font-size: 14px; font-weight: 700; margin-bottom: 6px; }
.rank-saldo { font-size: 14px; font-weight: 700; flex-shrink: 0; margin-top: 2px; }

.pos-badge { width: 28px; height: 28px; border-radius: 50%; flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; font-family: 'JetBrains Mono', monospace; background: rgba(255,255,255,.07); color: var(--text-2); }
.pos-badge.gold { background: rgba(246,173,85,.2); color: var(--amber); }
.pos-badge.silver { background: rgba(200,200,220,.15); color: #B0BEC5; }
.pos-badge.bronze { background: rgba(160,90,50,.2); color: #BCAAA4; }

.prop-chips { display: flex; flex-wrap: wrap; gap: 4px; }
.prop-chip { display: flex; align-items: center; gap: 4px; background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.08); border-radius: 6px; padding: 3px 8px; font-size: 10px; font-weight: 600; color: var(--text-2); }
.chip-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--green-dim); flex-shrink: 0; }
.chip-tag { font-size: 9px; font-weight: 700; font-family: 'JetBrains Mono', monospace; border-radius: 3px; padding: 0 3px; }
.chip-tag.hotel { background: rgba(246,173,85,.15); color: var(--amber); }
.chip-tag.casas { background: var(--green-dim); color: var(--green); }
</style>
