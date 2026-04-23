<template>
  <div class="page">
    <div class="header">
      <div class="brand">Rios<span>Bank</span></div>
      <div class="header-right">
        <div class="player-pill">
          <div class="pp-avatar">{{ jogador.nome?.[0]?.toUpperCase() }}</div>
          <span class="pp-nome">{{ jogador.nome }}</span>
          <span class="ws-dot" :class="ws.connected ? 'dot-ok' : 'dot-off'" :title="ws.connected ? 'Conectado' : 'Reconectando…'" />
        </div>
        <button class="exit-btn" title="Sair da partida" @click="sairDaPartida">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
        </button>
      </div>
    </div>

    <div class="wrap">
      <!-- Saldo card -->
      <div class="saldo-card glass">
        <p class="saldo-label text-muted">Saldo</p>
        <p class="saldo-valor mono">{{ formatMoney(jogador.saldo) }}</p>
        <div class="stats-row">
          <div class="stat">
            <span class="stat-val mono">{{ minhasPropriedades.length }}</span>
            <span class="stat-label text-muted">imóveis</span>
          </div>
          <div class="stat-div" />
          <div class="stat">
            <span class="stat-val mono">{{ totalCasas }}</span>
            <span class="stat-label text-muted">casas</span>
          </div>
          <div class="stat-div" />
          <div class="stat">
            <span class="stat-val mono">#{{ minhaPos }}</span>
            <span class="stat-label text-muted">ranking</span>
          </div>
        </div>
      </div>

      <!-- Ações rápidas -->
      <p class="section-title">Ações</p>
      <div class="acoes-grid">
        <button class="acao-btn" @click="abrirTransferencia">
          <div class="acao-icon icon-blue">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
            </svg>
          </div>
          <span>Transferir</span>
        </button>
        <button class="acao-btn" @click="abrirAluguel">
          <div class="acao-icon icon-amber">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
            </svg>
          </div>
          <span>Cobrar aluguel</span>
        </button>
        <button v-if="isHost" class="acao-btn" @click="$router.push({ name: 'host', params: { salaId } })">
          <div class="acao-icon icon-green">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
          </div>
          <span>Painel host</span>
        </button>
        <button class="acao-btn" @click="$router.push({ name: 'propriedades', params: { salaId } })">
          <div class="acao-icon icon-purple">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
            </svg>
          </div>
          <span>Comprar imóvel</span>
        </button>
      </div>

      <!-- Últimas transações -->
      <p class="section-title">Últimas movimentações</p>
      <div class="feed-mini">
        <div v-if="transacoesPendentes.length > 0" class="feed-item pending">
          <div class="feed-icon fi-amber">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
            </svg>
          </div>
          <div class="feed-body">
            <p class="feed-text">{{ transacoesPendentes.length }} transação(ões) aguardando aprovação</p>
          </div>
        </div>
        <div v-for="t in ultimasTransacoes" :key="t.id" class="feed-item">
          <div class="feed-icon" :class="iconClass(t)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
            </svg>
          </div>
          <div class="feed-body">
            <p class="feed-text">{{ descricaoTransacao(t) }}</p>
            <p class="feed-time">{{ timeAgo(t.criada_em) }}</p>
          </div>
        </div>
        <p v-if="!transacoes.length" class="no-items text-muted">Nenhuma movimentação ainda.</p>
      </div>
    </div>

    <!-- Modal transferência -->
    <div v-if="showTransferencia" class="modal-overlay" @click.self="showTransferencia = false">
      <div class="modal-sheet glass">
        <div class="sheet-handle" />
        <h3 class="modal-title">Transferir</h3>
        <div class="field">
          <label>Para quem?</label>
          <select v-model="tForm.destino_id" style="padding-left:14px">
            <option value="" disabled>Selecione o jogador</option>
            <option v-for="j in outrosJogadores" :key="j.id" :value="j.id">{{ j.nome }}</option>
          </select>
        </div>
        <div class="field">
          <label>Valor (R$)</label>
          <div class="input-wrap">
            <span class="input-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="width:15px;height:15px"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg></span>
            <input v-model.number="tForm.valor_reais" type="number" placeholder="0" min="1" />
          </div>
        </div>
        <p v-if="tErro" class="erro-msg">{{ tErro }}</p>
        <button class="btn btn-green" @click="enviarTransferencia">Solicitar aprovação</button>
      </div>
    </div>

    <!-- Modal cobrar aluguel -->
    <div v-if="showAluguel" class="modal-overlay" @click.self="showAluguel = false">
      <div class="modal-sheet glass">
        <div class="sheet-handle" />
        <h3 class="modal-title">Cobrar aluguel</h3>

        <div class="field">
          <label>Qual imóvel?</label>
          <select v-model="aForm.posse_id" style="padding-left:14px" @change="onPosseSelecionada">
            <option value="" disabled>Selecione o imóvel</option>
            <option v-for="p in minhasPropriedades" :key="p.id" :value="p.id">
              {{ p.propriedade.nome }}
            </option>
          </select>
        </div>

        <!-- Input de dados para ações -->
        <div v-if="aPosseSelecionada && isAcao" class="field">
          <label>Soma dos dados</label>
          <div class="input-wrap">
            <span class="input-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="width:15px;height:15px">
                <rect x="2" y="2" width="20" height="20" rx="4"/><circle cx="8" cy="8" r="1.5" fill="currentColor" stroke="none"/><circle cx="16" cy="16" r="1.5" fill="currentColor" stroke="none"/><circle cx="16" cy="8" r="1.5" fill="currentColor" stroke="none"/><circle cx="8" cy="16" r="1.5" fill="currentColor" stroke="none"/>
              </svg>
            </span>
            <input
              v-model.number="aForm.soma_dados"
              type="number" placeholder="ex: 7" min="2" max="12"
              @input="onSomaDados"
            />
          </div>
          <div v-if="aForm.soma_dados" class="aluguel-preview" style="margin-top:4px">
            <div class="preview-prop">
              <span class="prop-cor" :style="`background:${aPosseSelecionada.propriedade.cor_hex}`" />
              <span class="preview-nome">{{ aPosseSelecionada.propriedade.nome }}</span>
              <span class="preview-estado">{{ aForm.soma_dados }} × R$ {{ (aPosseSelecionada.propriedade.multiplicador_dado / 100).toLocaleString('pt-BR') }}</span>
            </div>
            <div class="preview-valor">{{ formatMoney(aAluguelAuto) }}</div>
          </div>
        </div>

        <!-- Preview do aluguel calculado (propriedades normais) -->
        <div v-else-if="aPosseSelecionada" class="aluguel-preview">
          <div class="preview-prop">
            <span
              class="prop-cor"
              :style="aPosseSelecionada.propriedade.cor_hex ? `background:${aPosseSelecionada.propriedade.cor_hex}` : ''"
            />
            <span class="preview-nome">{{ aPosseSelecionada.propriedade.nome }}</span>
            <span class="preview-estado">
              <template v-if="aPosseSelecionada.tem_hotel">🏨 hotel</template>
              <template v-else-if="aPosseSelecionada.num_casas > 0">{{ aPosseSelecionada.num_casas }} casa(s)</template>
              <template v-else>sem casas</template>
            </span>
          </div>
          <div class="preview-valor">{{ formatMoney(aAluguelAuto) }}</div>
        </div>

        <div class="field">
          <label>De quem cobrar?</label>
          <select v-model="aForm.destino_id" style="padding-left:14px">
            <option value="" disabled>Selecione o jogador</option>
            <option v-for="j in outrosJogadores" :key="j.id" :value="j.id">{{ j.nome }}</option>
          </select>
        </div>

        <div class="field" style="display:none">
          <div class="input-wrap">
            <input v-model.number="aForm.valor_reais" type="number" />
          </div>
        </div>

        <p v-if="aErro" class="erro-msg">{{ aErro }}</p>
        <button class="btn btn-green" @click="enviarAluguel">Cobrar</button>
      </div>
    </div>

    <BottomNav :sala-id="salaId" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useJogadorStore } from '../stores/jogadorStore'
import { usePartidaStore } from '../stores/partidaStore'
import { useWsStore } from '../stores/wsStore'
import { api } from '../stores/api'
import BottomNav from '../components/BottomNav.vue'

const route = useRoute()
const router = useRouter()
const salaId = computed(() => route.params.salaId)
const jogador = useJogadorStore()
const partida = usePartidaStore()
const ws = useWsStore()

const showTransferencia = ref(false)
const showAluguel = ref(false)
const tForm = ref({ destino_id: '', valor_reais: '' })
const aForm = ref({ posse_id: '', destino_id: '', valor_reais: '', soma_dados: '' })
const tErro = ref('')
const aErro = ref('')

const isHost = computed(() => partida.sala?.host_jogador_id === jogador.id)
const transacoes = computed(() => partida.transacoes)
const ultimasTransacoes = computed(() => transacoes.value.filter(t => t.status === 'aprovada').slice(0, 4))
const transacoesPendentes = computed(() => transacoes.value.filter(t => t.status === 'pendente'))
const minhasPropriedades = computed(() => partida.posses.filter(p => p.jogador_id === jogador.id))

const aPosseSelecionada = computed(() =>
  minhasPropriedades.value.find(p => p.id === aForm.value.posse_id) ?? null
)

const isAcao = computed(() => aPosseSelecionada.value?.propriedade?.tipo === 'acao')

const aAluguelAuto = computed(() => {
  const p = aPosseSelecionada.value
  if (!p) return 0
  const prop = p.propriedade
  if (prop.tipo === 'acao') {
    const soma = Number(aForm.value.soma_dados) || 0
    return soma * (prop.multiplicador_dado ?? 0)
  }
  if (p.tem_hotel)        return prop.aluguel_hotel   ?? 0
  if (p.num_casas === 4)  return prop.aluguel_4_casas ?? 0
  if (p.num_casas === 3)  return prop.aluguel_3_casas ?? 0
  if (p.num_casas === 2)  return prop.aluguel_2_casas ?? 0
  if (p.num_casas === 1)  return prop.aluguel_1_casa  ?? 0
  return prop.aluguel_sem_casa ?? 0
})

function onPosseSelecionada() {
  aForm.value.soma_dados = ''
  aForm.value.valor_reais = isAcao.value ? '' : aAluguelAuto.value / 100
}

function onSomaDados() {
  if (aForm.value.soma_dados) {
    aForm.value.valor_reais = aAluguelAuto.value / 100
  }
}
const totalCasas = computed(() => minhasPropriedades.value.reduce((s, p) => s + p.num_casas, 0))
const outrosJogadores = computed(() => partida.jogadoresAtivos.filter(j => j.id !== jogador.id))

const rankingOrdenado = computed(() =>
  [...partida.jogadoresAtivos].sort((a, b) => b.saldo - a.saldo)
)
const minhaPos = computed(() => {
  const idx = rankingOrdenado.value.findIndex(j => j.id === jogador.id)
  return idx >= 0 ? idx + 1 : '—'
})

const formatMoney = (val) => {
  if (!val && val !== 0) return 'R$ 0'
  return `R$ ${(val / 100).toLocaleString('pt-BR', { minimumFractionDigits: 0 })}`
}

const iconClass = (t) => {
  if (t.destino_id === jogador.id) return 'fi-green'
  if (t.origem_id === jogador.id) return 'fi-red'
  return 'fi-gray'
}

const nomeJog = (id) => {
  if (!id) return 'Banco'
  return partida.jogadores.find(j => j.id === id)?.nome || '?'
}

const descricaoTransacao = (t) => {
  if (t.descricao) return t.descricao
  const tipos = {
    transferencia: `${nomeJog(t.origem_id)} → ${nomeJog(t.destino_id)} · ${formatMoney(t.valor)}`,
    aluguel: `Aluguel ${nomeJog(t.destino_id)} cobrou de ${nomeJog(t.origem_id)}`,
    compra_propriedade: `${nomeJog(t.origem_id)} comprou imóvel`,
    leilao: `Leilão encerrado`,
  }
  return tipos[t.tipo] || t.tipo
}

const timeAgo = (iso) => {
  if (!iso) return ''
  const diff = Date.now() - new Date(iso).getTime()
  const m = Math.floor(diff / 60000)
  if (m < 1) return 'agora mesmo'
  if (m < 60) return `há ${m} min`
  return `há ${Math.floor(m / 60)}h`
}

function abrirTransferencia() {
  tForm.value = { destino_id: '', valor_reais: '' }
  tErro.value = ''
  showTransferencia.value = true
}

function abrirAluguel() {
  aForm.value = { posse_id: '', destino_id: '', valor_reais: '', soma_dados: '' }
  aErro.value = ''
  showAluguel.value = true
}

async function enviarTransferencia() {
  if (!tForm.value.destino_id || !tForm.value.valor_reais) {
    tErro.value = 'Preencha todos os campos.'
    return
  }
  try {
    await api.post('/transacoes', {
      sala_id: salaId.value,
      session_token: jogador.sessionToken,
      tipo: 'transferencia',
      valor: Math.round(tForm.value.valor_reais * 100),
      destino_id: tForm.value.destino_id,
    })
    showTransferencia.value = false
  } catch (e) {
    tErro.value = e.message
  }
}

async function enviarAluguel() {
  if (!aForm.value.posse_id || !aForm.value.destino_id) {
    aErro.value = 'Selecione o imóvel e o jogador.'
    return
  }
  if (isAcao.value && !aForm.value.soma_dados) {
    aErro.value = 'Informe a soma dos dados.'
    return
  }
  const valor = aAluguelAuto.value
  if (!valor) {
    aErro.value = 'Valor de aluguel não calculado.'
    return
  }
  const nomeImovel = aPosseSelecionada.value?.propriedade?.nome
  const descricao = nomeImovel
    ? `Aluguel de ${nomeImovel} cobrado por ${jogador.nome}`
    : `Aluguel cobrado por ${jogador.nome}`
  try {
    await api.post('/transacoes', {
      sala_id: salaId.value,
      session_token: jogador.sessionToken,
      tipo: 'aluguel',
      valor,
      destino_id: aForm.value.destino_id,
      descricao,
    })
    showAluguel.value = false
  } catch (e) {
    aErro.value = e.message
  }
}

async function sairDaPartida() {
  if (!confirm('Sair da partida? Você será marcado como expulso e não poderá retornar.')) return
  try {
    await api.post(`/salas/${salaId.value}/sair?session_token=${jogador.sessionToken}`)
  } catch {}
  ws.disconnect()
  router.push('/')
}

onMounted(async () => {
  if (!partida.sala) await partida.carregarSala(salaId.value)
  if (!partida.posses.length) await partida.carregarPropriedades(salaId.value)
  if (!partida.transacoes.length) await partida.carregarTransacoes(salaId.value)
})
</script>

<style scoped>
.page {
  min-height: 100dvh;
  display: flex; flex-direction: column; align-items: center;
  padding: 0 20px calc(var(--nav-h) + 24px);
  position: relative;
}

.header {
  width: 100%; max-width: 360px;
  display: flex; align-items: center; justify-content: space-between;
  padding: 20px 0 16px; position: relative; z-index: 1;
}
.brand { font-size: 20px; font-weight: 800; letter-spacing: -.5px; }
.brand span { color: var(--green); }

.header-right { display: flex; align-items: center; gap: 8px; }

.player-pill {
  display: flex; align-items: center; gap: 7px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-br);
  border-radius: 999px; padding: 6px 12px 6px 6px;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.exit-btn {
  width: 34px; height: 34px; border-radius: 50%;
  background: rgba(224, 84, 84, .08);
  border: 1px solid rgba(224, 84, 84, .2);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: var(--danger);
  transition: background .15s, border-color .15s;
  flex-shrink: 0;
}
.exit-btn:hover { background: rgba(224, 84, 84, .18); border-color: rgba(224, 84, 84, .4); }
.exit-btn svg { width: 16px; height: 16px; }
.pp-avatar {
  width: 26px; height: 26px; border-radius: 50%;
  background: var(--green-dim); border: 1px solid rgba(46,204,113,.25);
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 800; color: var(--green);
}
.pp-nome { font-size: 13px; font-weight: 700; }
.ws-dot {
  width: 7px; height: 7px; border-radius: 50%;
  flex-shrink: 0;
}
.dot-ok  { background: var(--green); box-shadow: 0 0 5px var(--green); }
.dot-off { background: var(--danger); animation: blink .9s step-start infinite; }
@keyframes blink { 50% { opacity: 0; } }

.wrap {
  width: 100%; max-width: 360px;
  display: flex; flex-direction: column; gap: 14px;
  position: relative; z-index: 1;
}

.saldo-card {
  padding: 22px;
}
.saldo-label { font-size: 12px; margin-bottom: 4px; }
.saldo-valor { font-size: 32px; font-weight: 700; margin-bottom: 16px; color: var(--green); }
.stats-row { display: flex; align-items: center; gap: 16px; }
.stat { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.stat-val { font-size: 16px; font-weight: 700; }
.stat-label { font-size: 10px; }
.stat-div { width: 1px; height: 24px; background: rgba(255,255,255,.08); }

.acoes-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
.acao-btn {
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.08);
  border-radius: 16px; padding: 14px 8px;
  cursor: pointer; transition: all .2s;
  font-size: 10px; font-weight: 600; color: var(--text-2);
  font-family: 'Manrope', sans-serif;
}
.acao-btn:hover { background: rgba(255,255,255,.09); }
.acao-btn:active { transform: scale(.95); }
.acao-icon {
  width: 44px; height: 44px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}
.acao-icon svg { width: 20px; height: 20px; }
.icon-blue { background: rgba(99,179,237,.15); color: var(--blue); }
.icon-amber { background: rgba(246,173,85,.15); color: var(--amber); }
.icon-green { background: var(--green-dim); color: var(--green); }
.icon-purple { background: rgba(156,39,176,.15); color: #CE93D8; }

.feed-mini { display: flex; flex-direction: column; gap: 8px; }
.feed-item {
  background: var(--glass-bg); border: 1px solid var(--glass-br);
  border-radius: var(--radius-sm); padding: 12px 14px;
  display: flex; align-items: flex-start; gap: 12px;
  backdrop-filter: blur(24px);
}
.feed-item.pending { border-color: rgba(246,173,85,.2); background: rgba(246,173,85,.05); }
.feed-icon { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.feed-icon svg { width: 16px; height: 16px; }
.fi-green { background: rgba(46,204,113,.15); color: var(--green); }
.fi-red { background: rgba(224,84,84,.15); color: var(--danger); }
.fi-amber { background: rgba(246,173,85,.15); color: var(--amber); }
.fi-gray { background: rgba(255,255,255,.07); color: var(--text-2); }
.feed-body { flex: 1; }
.feed-text { font-size: 13px; font-weight: 600; }
.feed-time { font-size: 10px; font-family: 'JetBrains Mono', monospace; color: var(--text-2); opacity: .6; margin-top: 3px; }
.no-items { font-size: 13px; text-align: center; padding: 16px 0; }
.erro-msg { font-size: 12px; color: var(--danger); }

/* Modals */
.modal-overlay {
  position: fixed; inset: 0; z-index: 80;
  background: rgba(0,0,0,.6); backdrop-filter: blur(4px);
  display: flex; align-items: flex-end; justify-content: center;
}
.modal-sheet {
  width: 100%; max-width: 480px;
  border-radius: 24px 24px 0 0; padding: 16px 20px 40px;
  display: flex; flex-direction: column; gap: 14px;
}
.sheet-handle {
  width: 40px; height: 4px; background: rgba(255,255,255,.15);
  border-radius: 2px; align-self: center; margin-bottom: 4px;
}
.modal-title { font-size: 18px; font-weight: 800; }

.aluguel-preview {
  display: flex; align-items: center; justify-content: space-between;
  background: var(--green-dim);
  border: 1px solid rgba(46,204,113,.2);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  gap: 12px;
}
.preview-prop { display: flex; align-items: center; gap: 8px; flex: 1; min-width: 0; }
.prop-cor { width: 10px; height: 10px; border-radius: 3px; flex-shrink: 0; background: var(--text-2); }
.preview-nome { font-size: 13px; font-weight: 700; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.preview-estado { font-size: 11px; color: var(--text-2); white-space: nowrap; flex-shrink: 0; }
.preview-valor { font-family: 'JetBrains Mono', monospace; font-size: 16px; font-weight: 700; color: var(--green); flex-shrink: 0; }
</style>
