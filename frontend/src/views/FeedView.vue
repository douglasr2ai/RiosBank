<template>
  <div class="page">
    <div class="header">
      <div class="brand">Rios<span>Bank</span></div>
    </div>

    <div class="wrap">
      <p class="section-title">Fatos da partida</p>

      <div class="feed">
        <template v-for="(grupo, idx) in feedAgrupado" :key="idx">
          <div class="time-divider"><span>{{ grupo.label }}</span></div>
          <div
            v-for="t in grupo.items"
            :key="t.id"
            class="feed-item"
            :class="{ 'pending': t.status === 'pendente' }"
          >
            <div class="feed-icon" :class="iconClass(t)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <line x1="12" y1="1" x2="12" y2="23"/>
                <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
              </svg>
            </div>
            <div class="feed-body">
              <p class="feed-text" v-html="feedTexto(t)" />
              <div v-if="t.status === 'pendente'" class="timer-bar">
                <div class="timer-fill" />
              </div>
              <p class="feed-time">{{ timeAgo(t.criada_em) }}</p>
            </div>
          </div>
        </template>

        <div v-if="!partida.transacoes.length" class="empty text-muted">
          Nenhuma movimentação ainda.
        </div>
      </div>
    </div>

    <BottomNav :sala-id="salaId" />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useJogadorStore } from '../stores/jogadorStore'
import { usePartidaStore } from '../stores/partidaStore'
import BottomNav from '../components/BottomNav.vue'

const route = useRoute()
const salaId = computed(() => route.params.salaId)
const jogador = useJogadorStore()
const partida = usePartidaStore()

const nomeJog = (id) => {
  if (!id) return 'Banco'
  return partida.jogadores.find(j => j.id === id)?.nome || '?'
}

const formatMoney = (val) => {
  if (!val && val !== 0) return 'R$0'
  return `R$ ${(val / 100).toLocaleString('pt-BR', { minimumFractionDigits: 0 })}`
}

const iconClass = (t) => {
  if (t.status === 'pendente') return 'fi-amber'
  if (t.status === 'reprovada') return 'fi-red'
  if (t.destino_id === jogador.id) return 'fi-green'
  if (t.origem_id === jogador.id) return 'fi-red'
  return 'fi-blue'
}

const feedTexto = (t) => {
  if (t.descricao) return t.descricao
  const mapa = {
    transferencia: `<b>${nomeJog(t.origem_id)}</b> transferiu <span class="val">${formatMoney(t.valor)}</span> para <b>${nomeJog(t.destino_id)}</b>`,
    aluguel: `<b>${nomeJog(t.destino_id)}</b> recebeu aluguel de <b>${nomeJog(t.origem_id)}</b> · <span class="val-pos">+${formatMoney(t.valor)}</span>`,
    compra_propriedade: `<b>${nomeJog(t.origem_id)}</b> comprou imóvel · <span class="val-neg">-${formatMoney(t.valor)}</span>`,
    leilao: `Leilão encerrado · <span class="val">${formatMoney(t.valor)}</span>`,
    hipoteca: `<b>${nomeJog(t.destino_id)}</b> hipotecou imóvel`,
    recuperar_hipoteca: `<b>${nomeJog(t.origem_id)}</b> recuperou hipoteca`,
    compra_casa: `<b>${nomeJog(t.origem_id)}</b> comprou casa/hotel`,
    venda_casa: `<b>${nomeJog(t.origem_id)}</b> vendeu casa/hotel`,
    estorno: `Transação estornada · <span class="val">${formatMoney(t.valor)}</span>`,
    falencia: `<b>${nomeJog(t.origem_id)}</b> foi à falência`,
    pagamento_banco: `Pagamento do banco para <b>${nomeJog(t.destino_id)}</b>`,
  }
  return mapa[t.tipo] || t.tipo
}

const timeAgo = (iso) => {
  if (!iso) return ''
  const diff = Date.now() - new Date(iso).getTime()
  const m = Math.floor(diff / 60000)
  if (m < 1) return 'agora mesmo'
  if (m < 60) return `há ${m} min`
  return `há ${Math.floor(m / 60)}h`
}

const feedAgrupado = computed(() => {
  const items = [...partida.transacoes]
  if (!items.length) return []
  const grupos = []
  let lastLabel = null

  for (const t of items) {
    const label = timeAgo(t.criada_em)
    if (label !== lastLabel) {
      grupos.push({ label, items: [t] })
      lastLabel = label
    } else {
      grupos[grupos.length - 1].items.push(t)
    }
  }
  return grupos
})

onMounted(async () => {
  if (!partida.transacoes.length) await partida.carregarTransacoes(salaId.value)
})
</script>

<style scoped>
.page { min-height: 100dvh; display: flex; flex-direction: column; align-items: center; padding: 0 20px calc(var(--nav-h) + 24px); position: relative; }
.header { width: 100%; max-width: 360px; display: flex; align-items: center; justify-content: space-between; padding: 20px 0 16px; position: relative; z-index: 1; }
.brand { font-size: 20px; font-weight: 800; letter-spacing: -.5px; }
.brand span { color: var(--green); }
.wrap { width: 100%; max-width: 360px; display: flex; flex-direction: column; gap: 8px; position: relative; z-index: 1; }

.feed { display: flex; flex-direction: column; gap: 8px; }

.time-divider { display: flex; align-items: center; gap: 10px; margin: 2px 0; }
.time-divider::before, .time-divider::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,.06); }
.time-divider span { font-size: 10px; font-family: 'JetBrains Mono', monospace; color: var(--text-2); opacity: .6; }

.feed-item { background: var(--glass-bg); backdrop-filter: blur(24px); border: 1px solid var(--glass-br); border-radius: var(--radius-sm); padding: 12px 14px; display: flex; align-items: flex-start; gap: 12px; }
.feed-item.pending { border-color: rgba(246,173,85,.2); background: rgba(246,173,85,.05); }

.feed-icon { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.feed-icon svg { width: 16px; height: 16px; }
.fi-green { background: rgba(46,204,113,.15); color: var(--green); }
.fi-red { background: rgba(224,84,84,.15); color: var(--danger); }
.fi-blue { background: rgba(99,179,237,.15); color: var(--blue); }
.fi-amber { background: rgba(246,173,85,.15); color: var(--amber); }

.feed-body { flex: 1; }
.feed-text { font-size: 13px; font-weight: 600; line-height: 1.45; margin-bottom: 4px; }
.feed-time { font-size: 10px; font-family: 'JetBrains Mono', monospace; color: var(--text-2); opacity: .6; }

.timer-bar { height: 2px; background: rgba(246,173,85,.15); border-radius: 2px; margin: 4px 0; overflow: hidden; }
.timer-fill { height: 100%; width: 100%; background: var(--amber); animation: shrink 10s linear forwards; }
@keyframes shrink { to { width: 0; } }

.empty { font-size: 13px; text-align: center; padding: 32px 0; }

.feed-text :deep(b) { color: var(--text); }
.feed-text :deep(.val) { font-family: 'JetBrains Mono', monospace; color: var(--text); }
.feed-text :deep(.val-pos) { font-family: 'JetBrains Mono', monospace; color: var(--green); }
.feed-text :deep(.val-neg) { font-family: 'JetBrains Mono', monospace; color: var(--danger); }
</style>
