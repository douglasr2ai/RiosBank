<template>
  <Teleport to="body">
    <div v-if="visivel" class="overlay">
      <!-- Banner topo -->
      <div class="banner">
        <div class="banner-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
        </div>
        <div class="banner-text">
          <p class="banner-titulo">Você faliu</p>
          <p class="banner-sub">Saldo final: <strong class="mono">R$ 0</strong> — todos os seus bens foram liquidados.</p>
        </div>
      </div>

      <!-- Feed de transações -->
      <div class="feed-wrap">
        <p class="feed-label">Últimas movimentações</p>
        <div class="feed">
          <div v-for="t in ultimasTransacoes" :key="t.id" class="feed-item">
            <div class="feed-icon-wrap" :class="iconClass(t)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <line x1="12" y1="1" x2="12" y2="23"/>
                <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
              </svg>
            </div>
            <div class="feed-body">
              <p class="feed-text">{{ descricao(t) }}</p>
              <p class="feed-time">{{ timeAgo(t.criada_em) }}</p>
            </div>
          </div>
          <p v-if="!ultimasTransacoes.length" class="vazio">Nenhuma movimentação.</p>
        </div>
      </div>

      <!-- Rodapé -->
      <div class="footer">
        <p class="footer-hint">Você pode acompanhar o jogo até o encerramento.</p>
        <button class="btn-sair" @click="sair">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="width:16px;height:16px">
            <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          Sair da partida
        </button>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useJogadorStore } from '../stores/jogadorStore'
import { usePartidaStore } from '../stores/partidaStore'
import { useWsStore } from '../stores/wsStore'
import { api } from '../stores/api'

const router = useRouter()
const jogador = useJogadorStore()
const partida = usePartidaStore()
const ws = useWsStore()

const visivel = computed(() =>
  jogador.isFalido && partida.sala?.status === 'em_andamento'
)

const ultimasTransacoes = computed(() =>
  partida.transacoes.filter(t => t.status === 'aprovada').slice(0, 6)
)

const nomeJog = (id) => {
  if (!id) return 'Banco'
  return partida.jogadores.find(j => j.id === id)?.nome || '?'
}

function formatMoney(val) {
  if (!val && val !== 0) return 'R$ 0'
  return `R$ ${(val / 100).toLocaleString('pt-BR', { minimumFractionDigits: 0 })}`
}

function descricao(t) {
  if (t.descricao) return t.descricao
  const mapa = {
    transferencia: `${nomeJog(t.origem_id)} → ${nomeJog(t.destino_id)} · ${formatMoney(t.valor)}`,
    aluguel: `Aluguel ${nomeJog(t.destino_id)} ← ${nomeJog(t.origem_id)} · ${formatMoney(t.valor)}`,
    compra_propriedade: `${nomeJog(t.origem_id)} comprou imóvel`,
    leilao: `Leilão encerrado`,
  }
  return mapa[t.tipo] || t.tipo
}

function iconClass(t) {
  if (t.destino_id === jogador.id) return 'fi-green'
  if (t.origem_id === jogador.id) return 'fi-red'
  return 'fi-gray'
}

function timeAgo(iso) {
  if (!iso) return ''
  const diff = Date.now() - new Date(iso).getTime()
  const m = Math.floor(diff / 60000)
  if (m < 1) return 'agora mesmo'
  if (m < 60) return `há ${m} min`
  return `há ${Math.floor(m / 60)}h`
}

async function sair() {
  const salaId = partida.sala?.id
  if (salaId) {
    try {
      await api.post(`/salas/${salaId}/sair?session_token=${jogador.sessionToken}`)
    } catch {}
  }
  ws.disconnect()
  jogador.clear()
  partida.clear()
  router.push({ name: 'landing' })
}
</script>

<style scoped>
.overlay {
  position: fixed; inset: 0; z-index: 180;
  background: rgba(6, 14, 8, .97);
  display: flex; flex-direction: column;
  overflow-y: auto;
}

/* Banner */
.banner {
  display: flex; align-items: flex-start; gap: 14px;
  background: rgba(224, 84, 84, .08);
  border-bottom: 1px solid rgba(224, 84, 84, .2);
  padding: 20px 20px 18px;
  flex-shrink: 0;
}

.banner-icon {
  width: 44px; height: 44px; border-radius: 50%; flex-shrink: 0;
  background: rgba(224, 84, 84, .15);
  border: 1px solid rgba(224, 84, 84, .25);
  display: flex; align-items: center; justify-content: center;
  color: var(--danger);
  margin-top: 2px;
}
.banner-icon svg { width: 22px; height: 22px; }

.banner-titulo {
  font-size: 20px; font-weight: 800; color: var(--danger);
  letter-spacing: -.3px; margin-bottom: 4px;
}
.banner-sub { font-size: 13px; color: var(--text-2); line-height: 1.5; }
.banner-sub strong { color: var(--text); }

/* Feed */
.feed-wrap {
  flex: 1;
  padding: 20px 20px 0;
  display: flex; flex-direction: column; gap: 10px;
  max-width: 480px; width: 100%; margin: 0 auto;
}

.feed-label {
  font-size: 11px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase;
  color: var(--text-2); font-family: 'JetBrains Mono', monospace;
}

.feed { display: flex; flex-direction: column; gap: 8px; }

.feed-item {
  display: flex; align-items: flex-start; gap: 12px;
  background: var(--glass-bg); border: 1px solid var(--glass-br);
  border-radius: var(--radius-sm); padding: 12px 14px;
}

.feed-icon-wrap {
  width: 34px; height: 34px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
}
.feed-icon-wrap svg { width: 15px; height: 15px; }
.fi-green { background: rgba(46,204,113,.15); color: var(--green); }
.fi-red   { background: rgba(224,84,84,.15);  color: var(--danger); }
.fi-gray  { background: rgba(255,255,255,.07); color: var(--text-2); }

.feed-body { flex: 1; }
.feed-text { font-size: 13px; font-weight: 600; }
.feed-time { font-size: 10px; font-family: 'JetBrains Mono', monospace; color: var(--text-2); opacity: .5; margin-top: 3px; }
.vazio { font-size: 13px; color: var(--text-2); text-align: center; padding: 24px 0; }

/* Footer */
.footer {
  flex-shrink: 0;
  padding: 20px;
  max-width: 480px; width: 100%; margin: 0 auto;
  display: flex; flex-direction: column; gap: 10px;
}

.footer-hint {
  font-size: 12px; color: var(--text-2); text-align: center; line-height: 1.5;
}

.btn-sair {
  display: flex; align-items: center; justify-content: center; gap: 8px;
  width: 100%; padding: 14px;
  background: rgba(224, 84, 84, .12);
  border: 1px solid rgba(224, 84, 84, .25);
  border-radius: var(--radius-sm);
  color: var(--danger);
  font-size: 15px; font-weight: 700; font-family: 'Manrope', sans-serif;
  cursor: pointer; transition: background .15s;
}
.btn-sair:hover { background: rgba(224, 84, 84, .2); }
.btn-sair:active { transform: scale(.98); }
</style>
