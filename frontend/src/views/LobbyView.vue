<template>
  <div class="page">
    <div class="wrap">
      <!-- Header -->
      <div class="header">
        <div class="brand">Rios<span>Bank</span></div>
        <div class="status-pill">
          <span class="dot" /><span>Aguardando</span>
        </div>
      </div>

      <!-- Copiar link -->
      <div class="glass link-card">
        <div class="link-info">
          <p class="link-label text-muted">Link de convite</p>
          <p class="link-val mono">{{ linkCurto }}</p>
        </div>
        <button class="copy-btn" @click="copiarLink">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
          </svg>
          {{ copiado ? 'Copiado!' : 'Copiar' }}
        </button>
      </div>

      <!-- Info pills -->
      <div class="pills-row">
        <div class="info-pill">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <rect x="2" y="3" width="20" height="14" rx="2"/>
          </svg>
          <span>{{ salaInfo?.versao_jogo?.replace('_', ' ') || '—' }}</span>
        </div>
        <div class="info-pill">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
          </svg>
          <span class="mono">{{ saldoInicial }}</span>
        </div>
        <div class="info-pill">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>
          </svg>
          <span>{{ jogadores.length }}/8</span>
        </div>
      </div>

      <!-- Lista de jogadores -->
      <p class="section-title">Jogadores</p>
      <div class="jogadores-list">
        <div v-for="j in jogadores" :key="j.id" class="jogador-row glass">
          <div class="jog-avatar">{{ j.nome[0]?.toUpperCase() }}</div>
          <span class="jog-nome">{{ j.nome }}</span>
          <span v-if="j.id === salaInfo?.host_jogador_id" class="host-badge">host</span>
          <span v-if="j.id === jogador.id" class="eu-badge">você</span>
        </div>
      </div>

      <!-- Aviso histórico -->
      <div class="aviso-card glass">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="width:16px;height:16px;flex-shrink:0;color:var(--amber)">
          <circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/>
        </svg>
        <p class="aviso-text">
          Guarde o link de convite ou a senha da sala. Após a partida, eles dão acesso ao histórico e ao resultado final.
        </p>
      </div>

      <!-- Botões -->
      <div class="actions">
        <button v-if="isHost" class="btn btn-green" :disabled="jogadores.length < 2 || loading" @click="iniciar">
          {{ loading ? 'Iniciando...' : 'Iniciar partida' }}
        </button>
        <p v-else class="aguarda-host text-muted">Aguardando o host iniciar a partida...</p>
        <button class="btn btn-ghost" style="margin-top: 4px" @click="sair">Sair da sala</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useJogadorStore } from '../stores/jogadorStore'
import { usePartidaStore } from '../stores/partidaStore'
import { useWsStore } from '../stores/wsStore'
import { useToastStore } from '../stores/toastStore'
import { api } from '../stores/api'

const SALDO_INICIAL = { super_banco_imobiliario: 1_500_000 }

const route = useRoute()
const router = useRouter()
const jogador = useJogadorStore()
const partida = usePartidaStore()
const ws = useWsStore()
const toast = useToastStore()

const loading = ref(false)
const copiado = ref(false)

const salaInfo = computed(() => partida.sala)
const jogadores = computed(() => partida.jogadores.filter(j => j.status !== 'expulso'))
const isHost = computed(() => salaInfo.value?.host_jogador_id === jogador.id)
const saldoInicial = computed(() => {
  const centavos = SALDO_INICIAL[salaInfo.value?.versao_jogo] ?? 1_500_000
  return `R$ ${(centavos / 100).toLocaleString('pt-BR', { minimumFractionDigits: 0 })}`
})

const linkCurto = computed(() => {
  if (!salaInfo.value?.link_token) return '—'
  const base = window.location.origin
  return `${base}/join/${salaInfo.value.link_token}`
})

async function copiarLink() {
  try {
    await navigator.clipboard.writeText(linkCurto.value)
    copiado.value = true
    setTimeout(() => (copiado.value = false), 2000)
  } catch {}
}

async function iniciar() {
  loading.value = true
  try {
    await api.post(`/salas/${route.params.salaId}/start?session_token=${jogador.sessionToken}`)
  } catch (e) {
    toast.add(e.message)
  } finally {
    loading.value = false
  }
}

async function sair() {
  try {
    await api.post(`/salas/${route.params.salaId}/sair?session_token=${jogador.sessionToken}`)
  } catch {}
  jogador.clear()
  partida.clear()
  ws.disconnect()
  router.push({ name: 'entrar' })
}

onMounted(async () => {
  if (!partida.sala) {
    await partida.carregarSala(route.params.salaId)
  }
})
</script>

<style scoped>
.page {
  min-height: 100dvh;
  display: flex; align-items: flex-start; justify-content: center;
  padding: 0 20px 40px;
  position: relative;
}

.wrap {
  width: 100%; max-width: 360px;
  display: flex; flex-direction: column; gap: 14px;
  position: relative; z-index: 1; padding-top: 20px;
}

.header { display: flex; align-items: center; justify-content: space-between; padding: 4px 0 8px; }
.brand { font-size: 20px; font-weight: 800; letter-spacing: -.5px; }
.brand span { color: var(--green); }

.status-pill {
  display: flex; align-items: center; gap: 6px;
  background: rgba(246,173,85,.08); border: 1px solid rgba(246,173,85,.2);
  border-radius: 999px; padding: 6px 12px;
  font-size: 11px; font-weight: 700; color: var(--amber);
  font-family: 'JetBrains Mono', monospace;
}
.dot { width: 6px; height: 6px; border-radius: 50%; background: var(--amber); animation: pulse 1.5s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }

.link-card {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 16px;
}
.link-info { flex: 1; min-width: 0; }
.link-label { font-size: 11px; margin-bottom: 3px; }
.link-val { font-size: 11px; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.copy-btn {
  display: flex; align-items: center; gap: 6px;
  background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.1);
  border-radius: 10px; padding: 8px 12px;
  font-size: 12px; font-weight: 700; color: var(--text-2);
  font-family: 'Manrope', sans-serif; cursor: pointer; flex-shrink: 0; transition: all .2s;
}
.copy-btn svg { width: 14px; height: 14px; }
.copy-btn:hover { background: rgba(255,255,255,.1); color: var(--text); }

.pills-row { display: flex; gap: 8px; flex-wrap: wrap; }
.info-pill {
  display: flex; align-items: center; gap: 6px;
  background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.08);
  border-radius: 999px; padding: 6px 12px;
  font-size: 12px; font-weight: 600; color: var(--text-2);
}
.info-pill svg { width: 13px; height: 13px; }

.jogadores-list { display: flex; flex-direction: column; gap: 8px; }
.jogador-row {
  display: flex; align-items: center; gap: 10px;
  padding: 12px 14px; border-radius: 14px;
}
.jog-avatar {
  width: 34px; height: 34px; border-radius: 50%; flex-shrink: 0;
  background: var(--green-dim); border: 1px solid rgba(46,204,113,.2);
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700; color: var(--green);
}
.jog-nome { font-size: 14px; font-weight: 600; flex: 1; }

.host-badge, .eu-badge {
  font-size: 9px; font-weight: 700; font-family: 'JetBrains Mono', monospace;
  letter-spacing: .05em; text-transform: uppercase;
  border-radius: 999px; padding: 2px 7px;
}
.host-badge { background: var(--green-dim); color: var(--green); }
.eu-badge { background: rgba(255,255,255,.07); color: var(--text-2); }

.aviso-card {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 14px; border-radius: 14px;
  background: rgba(246,173,85,.05); border-color: rgba(246,173,85,.15);
}
.aviso-text { font-size: 12px; color: var(--text-2); line-height: 1.55; }

.actions { display: flex; flex-direction: column; gap: 8px; }
.aguarda-host { font-size: 13px; text-align: center; padding: 14px; }
</style>
