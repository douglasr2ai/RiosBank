<template>
  <div class="page">
    <div class="header">
      <div class="brand">Rios<span>Bank</span></div>
      <div class="falido-pill">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="width:12px;height:12px">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        Falido
      </div>
    </div>

    <div class="wrap">
      <!-- Banner falência -->
      <div class="bankrupt-banner glass">
        <div class="bankrupt-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <line x1="12" y1="1" x2="12" y2="23"/>
            <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
          </svg>
        </div>
        <div>
          <strong>Você foi à falência</strong>
          <span>Acompanhe a partida como espectador até o fim.</span>
        </div>
      </div>

      <p class="section-title">Fatos da partida</p>

      <div class="feed">
        <div v-for="t in partida.transacoes" :key="t.id" class="feed-item">
          <div class="feed-icon" :class="t.origem_id === jogador.id ? 'fi-red' : 'fi-blue'">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <line x1="12" y1="1" x2="12" y2="23"/>
              <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
            </svg>
          </div>
          <div class="feed-body">
            <p class="feed-text">{{ feedTexto(t) }}</p>
            <p class="feed-time">{{ timeAgo(t.criada_em) }}</p>
          </div>
        </div>
        <div v-if="!partida.transacoes.length" class="empty text-muted">Nenhuma movimentação.</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useJogadorStore } from '../stores/jogadorStore'
import { usePartidaStore } from '../stores/partidaStore'

const route = useRoute()
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

const feedTexto = (t) => {
  if (t.descricao) return t.descricao
  const mapa = {
    transferencia: `${nomeJog(t.origem_id)} → ${nomeJog(t.destino_id)} · ${formatMoney(t.valor)}`,
    aluguel: `Aluguel recebido por ${nomeJog(t.destino_id)}`,
    compra_propriedade: `${nomeJog(t.origem_id)} comprou imóvel`,
    leilao: `Leilão encerrado`,
    falencia: `${nomeJog(t.origem_id)} foi à falência`,
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

onMounted(async () => {
  if (!partida.transacoes.length) await partida.carregarTransacoes(route.params.salaId)
})
</script>

<style scoped>
.page { min-height: 100dvh; display: flex; flex-direction: column; align-items: center; padding: 0 20px 40px; position: relative; }
.header { width: 100%; max-width: 360px; display: flex; align-items: center; justify-content: space-between; padding: 20px 0 16px; position: relative; z-index: 1; }
.brand { font-size: 20px; font-weight: 800; letter-spacing: -.5px; }
.brand span { color: var(--green); }
.falido-pill { display: flex; align-items: center; gap: 6px; background: rgba(224,84,84,.08); border: 1px solid rgba(224,84,84,.2); border-radius: 999px; padding: 6px 12px; font-size: 11px; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: var(--danger); }

.wrap { width: 100%; max-width: 360px; display: flex; flex-direction: column; gap: 14px; position: relative; z-index: 1; }

.bankrupt-banner { padding: 18px; display: flex; align-items: center; gap: 14px; border-color: rgba(224,84,84,.18); background: rgba(224,84,84,.07); }
.bankrupt-icon { width: 46px; height: 46px; border-radius: 50%; background: rgba(224,84,84,.12); border: 1px solid rgba(224,84,84,.2); display: flex; align-items: center; justify-content: center; color: var(--danger); flex-shrink: 0; }
.bankrupt-icon svg { width: 20px; height: 20px; }
.bankrupt-banner strong { display: block; font-size: 15px; font-weight: 800; margin-bottom: 3px; }
.bankrupt-banner span { font-size: 12px; color: var(--text-2); }

.feed { display: flex; flex-direction: column; gap: 8px; }
.feed-item { background: var(--glass-bg); backdrop-filter: blur(24px); border: 1px solid var(--glass-br); border-radius: var(--radius-sm); padding: 12px 14px; display: flex; align-items: flex-start; gap: 12px; }
.feed-icon { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.feed-icon svg { width: 16px; height: 16px; }
.fi-red { background: rgba(224,84,84,.15); color: var(--danger); }
.fi-blue { background: rgba(99,179,237,.15); color: var(--blue); }
.feed-body { flex: 1; }
.feed-text { font-size: 13px; font-weight: 600; line-height: 1.45; margin-bottom: 3px; }
.feed-time { font-size: 10px; font-family: 'JetBrains Mono', monospace; color: var(--text-2); opacity: .6; }
.empty { font-size: 13px; text-align: center; padding: 32px 0; }
</style>
