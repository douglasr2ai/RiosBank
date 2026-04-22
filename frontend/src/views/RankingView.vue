<template>
  <div class="page">
    <div class="header">
      <div class="brand">Rios<span>Bank</span></div>
    </div>

    <div class="wrap">
      <p class="section-title">Ranking ao vivo</p>

      <!-- 1º lugar destaque -->
      <div v-if="ranking[0]" class="primeiro glass">
        <div class="ouro-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
        </div>
        <div class="primeiro-info">
          <p class="primeiro-nome">{{ ranking[0].nome }}</p>
          <p class="primeiro-saldo mono">{{ formatMoney(ranking[0].saldo) }}</p>
        </div>
        <div class="pos-badge gold">#1</div>
      </div>

      <!-- Demais jogadores -->
      <div class="outros-list">
        <div
          v-for="(j, i) in ranking.slice(1)"
          :key="j.id"
          class="rank-row glass"
          :class="{ 'rank-falido': j.status === 'falido', 'rank-eu': j.id === jogador.id }"
        >
          <div class="pos-badge" :class="badgeClass(i + 2)">#{{ i + 2 }}</div>
          <div class="rank-avatar">{{ j.nome[0]?.toUpperCase() }}</div>
          <div class="rank-info">
            <p class="rank-nome">{{ j.nome }} <span v-if="j.id === jogador.id" class="eu-tag">você</span></p>
            <div class="bar-wrap">
              <div class="bar-fill" :style="{ width: barWidth(j.saldo) + '%' }" />
            </div>
          </div>
          <p class="rank-saldo mono" :class="j.status === 'falido' ? 'text-danger' : 'text-green'">
            {{ j.status === 'falido' ? 'R$ 0' : formatMoney(j.saldo) }}
          </p>
        </div>
      </div>

      <p class="hint-ranking text-muted">Saldo atual · sem liquidação</p>
    </div>

    <BottomNav :sala-id="salaId" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useJogadorStore } from '../stores/jogadorStore'
import { usePartidaStore } from '../stores/partidaStore'
import BottomNav from '../components/BottomNav.vue'

const route = useRoute()
const salaId = computed(() => route.params.salaId)
const jogador = useJogadorStore()
const partida = usePartidaStore()

const ranking = computed(() =>
  [...partida.jogadores]
    .filter(j => j.status !== 'expulso')
    .sort((a, b) => b.saldo - a.saldo)
)

const maxSaldo = computed(() => Math.max(...ranking.value.map(j => j.saldo), 1))

const formatMoney = (val) => {
  if (!val && val !== 0) return 'R$ 0'
  return `R$ ${(val / 100).toLocaleString('pt-BR', { minimumFractionDigits: 0 })}`
}

const barWidth = (saldo) => Math.max(4, (saldo / maxSaldo.value) * 100)

const badgeClass = (pos) => {
  if (pos === 2) return 'silver'
  if (pos === 3) return 'bronze'
  return ''
}
</script>

<style scoped>
.page { min-height: 100dvh; display: flex; flex-direction: column; align-items: center; padding: 0 20px calc(var(--nav-h) + 24px); position: relative; }
.header { width: 100%; max-width: 360px; display: flex; align-items: center; justify-content: space-between; padding: 20px 0 16px; position: relative; z-index: 1; }
.brand { font-size: 20px; font-weight: 800; letter-spacing: -.5px; }
.brand span { color: var(--green); }
.wrap { width: 100%; max-width: 360px; display: flex; flex-direction: column; gap: 10px; position: relative; z-index: 1; }

.primeiro { padding: 18px; display: flex; align-items: center; gap: 14px; }
.ouro-icon { width: 44px; height: 44px; border-radius: 50%; background: rgba(246,173,85,.15); border: 1px solid rgba(246,173,85,.25); display: flex; align-items: center; justify-content: center; color: var(--amber); flex-shrink: 0; }
.ouro-icon svg { width: 20px; height: 20px; }
.primeiro-info { flex: 1; }
.primeiro-nome { font-size: 16px; font-weight: 700; }
.primeiro-saldo { font-size: 18px; font-weight: 700; color: var(--green); margin-top: 2px; }

.outros-list { display: flex; flex-direction: column; gap: 8px; }
.rank-row { display: flex; align-items: center; gap: 10px; padding: 12px 14px; border-radius: 14px; }
.rank-falido { opacity: .5; }
.rank-eu { border-color: rgba(46,204,113,.25); }

.rank-avatar { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,.07); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0; }
.rank-info { flex: 1; min-width: 0; }
.rank-nome { font-size: 13px; font-weight: 600; margin-bottom: 5px; display: flex; align-items: center; gap: 6px; }
.eu-tag { font-size: 9px; font-weight: 700; font-family: 'JetBrains Mono', monospace; background: rgba(255,255,255,.07); border-radius: 4px; padding: 1px 5px; color: var(--text-2); }

.bar-wrap { height: 4px; background: rgba(255,255,255,.06); border-radius: 2px; overflow: hidden; }
.bar-fill { height: 100%; background: linear-gradient(90deg, var(--green-d), var(--green)); border-radius: 2px; transition: width .5s ease; }

.rank-saldo { font-size: 13px; font-weight: 700; flex-shrink: 0; }

.pos-badge {
  width: 28px; height: 28px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 10px; font-weight: 700; font-family: 'JetBrains Mono', monospace;
  background: rgba(255,255,255,.07); color: var(--text-2);
}
.pos-badge.gold { background: rgba(246,173,85,.2); color: var(--amber); }
.pos-badge.silver { background: rgba(200,200,220,.15); color: #B0BEC5; }
.pos-badge.bronze { background: rgba(160,90,50,.2); color: #BCAAA4; }

.hint-ranking { font-size: 11px; text-align: center; padding: 4px 0; }
</style>
