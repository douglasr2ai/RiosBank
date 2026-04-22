<template>
  <div class="page">
    <div class="header">
      <div class="brand">Rios<span>Bank</span></div>
      <div class="host-badge">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="width:12px;height:12px">
          <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
        </svg>
        Host
      </div>
    </div>

    <div class="wrap">
      <!-- Pagamento ao banco -->
      <p class="section-title">Pagamento do banco</p>
      <div class="glass panel">
        <div class="toggle-row">
          <button class="toggle-btn" :class="{ active: bancoDir === 'receber' }" @click="bancoDir = 'receber'">Jogador recebe</button>
          <button class="toggle-btn" :class="{ active: bancoDir === 'pagar' }" @click="bancoDir = 'pagar'">Jogador paga</button>
        </div>
        <div class="field">
          <label>Jogador</label>
          <select v-model="bForm.jogador_id" style="padding-left:14px">
            <option value="" disabled>Selecione</option>
            <option v-for="j in jogadoresAtivos" :key="j.id" :value="j.id">{{ j.nome }}</option>
          </select>
        </div>
        <div class="field">
          <label>Valor (R$)</label>
          <div class="input-wrap">
            <span class="input-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="width:15px;height:15px"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg></span>
            <input v-model.number="bForm.valor_reais" type="number" min="1" placeholder="0" />
          </div>
        </div>
        <button class="btn btn-green" @click="solicitarBanco">Solicitar aprovação</button>
      </div>

      <!-- Jogadores + expulsar -->
      <p class="section-title">Jogadores</p>
      <div class="jogadores-list">
        <div v-for="j in jogadoresAtivos" :key="j.id" class="jog-row glass">
          <div class="jog-avatar">{{ j.nome[0]?.toUpperCase() }}</div>
          <div class="jog-info">
            <p class="jog-nome">{{ j.nome }}</p>
            <p class="jog-saldo mono text-muted">{{ formatMoney(j.saldo) }}</p>
          </div>
          <button
            v-if="j.id !== jogador.id"
            class="expulsar-btn"
            :class="{ 'confirming': confirmando?.tipo === 'expulsar' && confirmando?.id === j.id }"
            @click="clickExpulsar(j)"
          >
            <svg v-if="!(confirmando?.tipo === 'expulsar' && confirmando?.id === j.id)" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="width:14px;height:14px">
              <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/>
            </svg>
            {{ confirmando?.tipo === 'expulsar' && confirmando?.id === j.id ? 'Confirmar?' : 'Expulsar' }}
          </button>
        </div>
      </div>

      <!-- Transações recentes + estornar -->
      <p class="section-title">Estornar transação</p>
      <div class="transacoes-list">
        <div v-if="!transacoesAprovadas.length" class="empty text-muted">Nenhuma transação para estornar.</div>
        <div v-for="t in transacoesAprovadas.slice(0, 8)" :key="t.id" class="trans-row glass">
          <div class="trans-info">
            <p class="trans-desc">{{ descricao(t) }}</p>
            <p class="trans-val mono text-muted">{{ formatMoney(t.valor) }}</p>
          </div>
          <button
            class="estornar-btn"
            :class="{ 'confirming': confirmando?.tipo === 'estornar' && confirmando?.id === t.id }"
            @click="clickEstornar(t.id)"
          >
            {{ confirmando?.tipo === 'estornar' && confirmando?.id === t.id ? 'Confirmar?' : 'Estornar' }}
          </button>
        </div>
      </div>

      <!-- Encerrar partida -->
      <div class="danger-card glass">
        <p class="danger-title">Encerrar partida</p>
        <p class="danger-desc text-muted">O sistema fará a liquidação automática e salvará o ranking final.</p>
        <button
          class="btn"
          :class="confirmando?.tipo === 'encerrar' ? 'btn-danger-confirming' : 'btn-danger'"
          style="margin-top: 4px"
          @click="clickEncerrar"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="width:16px;height:16px">
            <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6M10 11v6M14 11v6M9 6V4a1 1 0 011-1h4a1 1 0 011 1v2"/>
          </svg>
          {{ confirmando?.tipo === 'encerrar' ? 'Clique para confirmar' : 'Encerrar partida' }}
        </button>
      </div>
    </div>

    <BottomNav :sala-id="salaId" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useJogadorStore } from '../stores/jogadorStore'
import { usePartidaStore } from '../stores/partidaStore'
import { useToastStore } from '../stores/toastStore'
import { api } from '../stores/api'
import BottomNav from '../components/BottomNav.vue'

const route = useRoute()
const salaId = computed(() => route.params.salaId)
const jogador = useJogadorStore()
const partida = usePartidaStore()
const toast = useToastStore()

const bancoDir = ref('receber')
const bForm = ref({ jogador_id: '', valor_reais: '' })
const confirmando = ref(null)
let confirmTimer = null

const jogadoresAtivos = computed(() => partida.jogadoresAtivos)
const transacoesAprovadas = computed(() =>
  partida.transacoes.filter(t => t.status === 'aprovada' && t.tipo !== 'estorno')
)

const formatMoney = (val) => {
  if (!val && val !== 0) return 'R$0'
  return `R$ ${(val / 100).toLocaleString('pt-BR', { minimumFractionDigits: 0 })}`
}

const nomeJog = (id) => {
  if (!id) return 'Banco'
  return partida.jogadores.find(j => j.id === id)?.nome || '?'
}

const descricao = (t) => {
  if (t.descricao) return t.descricao
  return `${nomeJog(t.origem_id)} → ${nomeJog(t.destino_id)}`
}

function pedirConfirmacao(tipo, id = null) {
  clearTimeout(confirmTimer)
  confirmando.value = { tipo, id }
  confirmTimer = setTimeout(() => { confirmando.value = null }, 3500)
}

async function solicitarBanco() {
  if (!bForm.value.jogador_id || !bForm.value.valor_reais) return
  const valor = Math.round(bForm.value.valor_reais * 100)
  try {
    await api.post('/transacoes', {
      sala_id: salaId.value,
      session_token: jogador.sessionToken,
      tipo: 'pagamento_banco',
      valor,
      destino_id: bancoDir.value === 'receber' ? bForm.value.jogador_id : undefined,
      origem_id_override: bancoDir.value === 'pagar' ? bForm.value.jogador_id : undefined,
      descricao: bancoDir.value === 'receber'
        ? `${nomeJog(bForm.value.jogador_id)} recebe ${formatMoney(valor)} do banco`
        : `${nomeJog(bForm.value.jogador_id)} paga ${formatMoney(valor)} ao banco`,
    })
    bForm.value = { jogador_id: '', valor_reais: '' }
  } catch (e) { toast.add(e.message) }
}

function clickExpulsar(j) {
  if (confirmando.value?.tipo === 'expulsar' && confirmando.value?.id === j.id) {
    confirmando.value = null
    expulsar(j)
  } else {
    pedirConfirmacao('expulsar', j.id)
  }
}

async function expulsar(j) {
  try {
    await api.delete(`/salas/${salaId.value}/jogadores/${j.id}?session_token=${jogador.sessionToken}`)
  } catch (e) { toast.add(e.message) }
}

function clickEstornar(id) {
  if (confirmando.value?.tipo === 'estornar' && confirmando.value?.id === id) {
    confirmando.value = null
    estornar(id)
  } else {
    pedirConfirmacao('estornar', id)
  }
}

async function estornar(transacaoId) {
  try {
    await api.post(`/transacoes/${transacaoId}/estornar?session_token=${jogador.sessionToken}`)
  } catch (e) { toast.add(e.message) }
}

function clickEncerrar() {
  if (confirmando.value?.tipo === 'encerrar') {
    confirmando.value = null
    encerrar()
  } else {
    pedirConfirmacao('encerrar')
  }
}

async function encerrar() {
  try {
    await api.post(`/salas/${salaId.value}/encerrar?session_token=${jogador.sessionToken}`)
  } catch (e) { toast.add(e.message) }
}
</script>

<style scoped>
.page { min-height: 100dvh; display: flex; flex-direction: column; align-items: center; padding: 0 20px calc(var(--nav-h) + 24px); position: relative; }
.header { width: 100%; max-width: 360px; display: flex; align-items: center; justify-content: space-between; padding: 20px 0 16px; position: relative; z-index: 1; }
.brand { font-size: 20px; font-weight: 800; letter-spacing: -.5px; }
.brand span { color: var(--green); }
.host-badge { display: flex; align-items: center; gap: 5px; background: var(--green-dim); border: 1px solid rgba(46,204,113,.2); border-radius: 999px; padding: 5px 11px; font-size: 11px; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: var(--green); }

.wrap { width: 100%; max-width: 360px; display: flex; flex-direction: column; gap: 12px; position: relative; z-index: 1; }

.panel { padding: 18px; display: flex; flex-direction: column; gap: 12px; }
.toggle-row { display: flex; gap: 4px; background: rgba(255,255,255,.04); border-radius: 10px; padding: 3px; }
.toggle-btn { flex: 1; padding: 7px; border: none; background: none; border-radius: 8px; font-size: 12px; font-weight: 700; font-family: 'Manrope', sans-serif; color: var(--text-2); cursor: pointer; transition: all .2s; }
.toggle-btn.active { background: rgba(46,204,113,.15); color: var(--green); }

.jogadores-list, .transacoes-list { display: flex; flex-direction: column; gap: 8px; }
.jog-row { display: flex; align-items: center; gap: 10px; padding: 12px 14px; border-radius: 14px; }
.jog-avatar { width: 34px; height: 34px; border-radius: 50%; background: var(--green-dim); border: 1px solid rgba(46,204,113,.2); display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; color: var(--green); flex-shrink: 0; }
.jog-info { flex: 1; }
.jog-nome { font-size: 14px; font-weight: 600; }
.jog-saldo { font-size: 12px; margin-top: 2px; }
.expulsar-btn { display: flex; align-items: center; gap: 5px; background: rgba(224,84,84,.08); border: 1px solid rgba(224,84,84,.2); border-radius: 8px; padding: 6px 10px; font-size: 11px; font-weight: 700; font-family: 'Manrope', sans-serif; color: var(--danger); cursor: pointer; flex-shrink: 0; transition: all .2s; }
.expulsar-btn:hover { background: rgba(224,84,84,.15); }
.expulsar-btn.confirming, .estornar-btn.confirming { background: rgba(246,173,85,.15); border-color: rgba(246,173,85,.3); color: var(--amber); }

.trans-row { display: flex; align-items: center; gap: 12px; padding: 12px 14px; border-radius: 12px; }
.trans-info { flex: 1; min-width: 0; }
.trans-desc { font-size: 12px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.trans-val { font-size: 11px; margin-top: 2px; }
.estornar-btn { background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.1); border-radius: 8px; padding: 5px 10px; font-size: 11px; font-weight: 700; font-family: 'Manrope', sans-serif; color: var(--text-2); cursor: pointer; flex-shrink: 0; }
.estornar-btn:hover { background: rgba(255,255,255,.1); }

.danger-card { padding: 18px; display: flex; flex-direction: column; gap: 8px; border-color: rgba(224,84,84,.15); background: rgba(224,84,84,.04); }
.danger-title { font-size: 15px; font-weight: 700; color: var(--danger); }
.danger-desc { font-size: 12px; line-height: 1.5; }
.btn-danger-confirming { background: rgba(246,173,85,.15); border: 1px solid rgba(246,173,85,.3); color: var(--amber); font-size: 14px; font-weight: 700; padding: 12px 20px; border-radius: var(--radius); width: 100%; cursor: pointer; font-family: 'Manrope', sans-serif; display: flex; align-items: center; justify-content: center; gap: 8px; }

.empty { font-size: 13px; text-align: center; padding: 16px 0; }
</style>
