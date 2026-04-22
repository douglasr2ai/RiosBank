<template>
  <div class="overlay">
    <div class="sheet glass">
      <div class="sheet-handle" />

      <!-- Cabeçalho -->
      <div class="leilao-header">
        <div class="prop-info">
          <div
            class="color-dot"
            :style="{ background: propInfo?.cor_hex || '#78909C' }"
          />
          <div>
            <p class="prop-nome">{{ propInfo?.nome || 'Propriedade' }}</p>
            <p class="iniciador text-muted">Iniciado por {{ iniciadorNome }}</p>
          </div>
        </div>
        <div v-if="ws.connected" class="tela-ativa">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
          </svg>
          Tela ativa
        </div>
      </div>

      <!-- Timer + Lance atual -->
      <div class="timer-lance-row">
        <div class="timer-wrap">
          <div class="timer-ring">
            <svg viewBox="0 0 72 72" class="ring-svg">
              <circle cx="36" cy="36" r="30" class="ring-bg"/>
              <circle
                cx="36" cy="36" r="30"
                class="ring-progress"
                :stroke-dasharray="188.5"
                :stroke-dashoffset="188.5 - (188.5 * timer / DURACAO)"
              />
            </svg>
            <span class="timer-num mono">{{ timer }}</span>
          </div>
          <p class="timer-label text-muted">segundos</p>
        </div>

        <div class="lance-atual-card">
          <p class="lance-label text-muted">Lance atual</p>
          <p class="lance-valor mono text-amber">{{ formatMoney(dados.lance_atual) }}</p>
          <p v-if="dados.lider_nome" class="lance-lider text-muted">{{ dados.lider_nome }}</p>
          <p v-else class="lance-lider text-muted">Sem lances</p>
        </div>
      </div>

      <!-- Participantes -->
      <div class="participantes">
        <div
          v-for="j in participantes"
          :key="j.id"
          class="part-avatar"
          :class="{
            'pa-lider': j.id === dados.lider_id,
            'pa-eu': j.id === jogador.id,
            'pa-vendedor': j.id === dados.iniciado_por,
          }"
          :title="j.nome"
        >
          {{ j.nome[0].toUpperCase() }}
        </div>
      </div>

      <!-- Botões de lance -->
      <div v-if="podeApostar" class="incrementos">
        <p class="proximo-minimo text-muted">
          Próximo mínimo: <span class="mono text-green">{{ formatMoney(dados.lance_atual + 10_000) }}</span>
        </p>
        <div class="inc-row">
          <button class="inc-btn" @click="darLance(10_000)">+R$100</button>
          <button class="inc-btn" @click="darLance(50_000)">+R$500</button>
          <button class="inc-btn inc-big" @click="darLance(100_000)">+R$1.000</button>
        </div>
      </div>

      <p v-else class="spectator-hint text-muted">
        {{ jogador.id === dados.iniciado_por ? 'Você iniciou este leilão e não pode dar lances.' : 'Acompanhe o leilão.' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { usePartidaStore } from '../stores/partidaStore'
import { useJogadorStore } from '../stores/jogadorStore'
import { useWsStore } from '../stores/wsStore'
import { useToastStore } from '../stores/toastStore'
import { api } from '../stores/api'

const DURACAO = 60
const partida = usePartidaStore()
const jogador = useJogadorStore()
const ws = useWsStore()
const toast = useToastStore()

const dados = computed(() => partida.leilaoAtivo || {})
const timer = ref(DURACAO)
let interval = null

const propInfo = computed(() => {
  const posseId = dados.value?.propriedade_id
  if (!posseId) return null
  const posse = partida.posses.find(p => p.propriedade_id === posseId)
  return posse?.propriedade || null
})

const iniciadorNome = computed(() =>
  partida.jogadores.find(j => j.id === dados.value?.iniciado_por)?.nome || '?'
)

const participantes = computed(() =>
  partida.jogadoresAtivos
)

const podeApostar = computed(() =>
  jogador.id !== dados.value?.iniciado_por && jogador.status !== 'falido'
)

const formatMoney = (val) => {
  if (!val && val !== 0) return 'R$0'
  return `R$ ${(val / 100).toLocaleString('pt-BR', { minimumFractionDigits: 0 })}`
}

async function darLance(incremento) {
  try {
    await api.post(`/leiloes/${dados.value.leilao_id}/lance`, {
      session_token: jogador.sessionToken,
      incremento,
    })
  } catch (e) {
    toast.add(e.message)
  }
}

async function encerrarLeilao() {
  if (!dados.value?.leilao_id) return
  try {
    await api.post(`/leiloes/${dados.value.leilao_id}/encerrar?session_token=${jogador.sessionToken}`)
  } catch {}
}

onMounted(() => {
  timer.value = DURACAO
  interval = setInterval(() => {
    timer.value--
    if (timer.value <= 0) {
      clearInterval(interval)
      encerrarLeilao()
    }
  }, 1000)
})

onUnmounted(() => clearInterval(interval))
</script>

<style scoped>
.overlay {
  position: fixed; inset: 0; z-index: 100;
  background: rgba(0, 0, 0, .7);
  backdrop-filter: blur(6px);
  display: flex; align-items: flex-end; justify-content: center;
}

.sheet {
  width: 100%; max-width: 480px;
  border-radius: 24px 24px 0 0;
  padding: 16px 20px 40px;
  display: flex; flex-direction: column; gap: 16px;
}

.sheet-handle {
  width: 40px; height: 4px;
  background: rgba(255, 255, 255, .15);
  border-radius: 2px; align-self: center; margin-bottom: 4px;
}

.leilao-header { display: flex; align-items: center; justify-content: space-between; }

.prop-info { display: flex; align-items: center; gap: 10px; }
.color-dot { width: 12px; height: 12px; border-radius: 50%; }
.prop-nome { font-size: 15px; font-weight: 700; }
.iniciador { font-size: 12px; margin-top: 2px; }

.tela-ativa {
  display: flex; align-items: center; gap: 5px;
  font-size: 11px; font-weight: 600; color: var(--green);
  background: var(--green-dim);
  border: 1px solid rgba(46, 204, 113, .2);
  border-radius: 999px; padding: 4px 10px;
}
.tela-ativa svg { width: 12px; height: 12px; }

.timer-lance-row { display: flex; gap: 14px; align-items: center; }

.timer-wrap { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.timer-ring {
  position: relative; width: 72px; height: 72px;
  display: flex; align-items: center; justify-content: center;
}
.ring-svg { position: absolute; inset: 0; transform: rotate(-90deg); }
.ring-bg { fill: none; stroke: rgba(255,255,255,.08); stroke-width: 4; }
.ring-progress { fill: none; stroke: var(--amber); stroke-width: 4; stroke-linecap: round; transition: stroke-dashoffset .9s linear; }
.timer-num { font-size: 20px; font-weight: 700; z-index: 1; }
.timer-label { font-size: 10px; }

.lance-atual-card {
  flex: 1; background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.08);
  border-radius: 14px; padding: 14px;
}
.lance-label { font-size: 11px; margin-bottom: 4px; }
.lance-valor { font-size: 22px; font-weight: 700; }
.lance-lider { font-size: 11px; margin-top: 3px; }

.participantes { display: flex; gap: 8px; flex-wrap: wrap; }
.part-avatar {
  width: 34px; height: 34px; border-radius: 50%;
  background: rgba(255,255,255,.07);
  border: 1px solid rgba(255,255,255,.1);
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; color: var(--text-2);
}
.pa-lider { background: rgba(246,173,85,.15); border-color: rgba(246,173,85,.3); color: var(--amber); }
.pa-eu { background: var(--green-dim); border-color: rgba(46,204,113,.3); color: var(--green); }
.pa-vendedor { opacity: .4; }

.proximo-minimo { font-size: 12px; margin-bottom: 6px; }

.inc-row { display: flex; gap: 8px; }
.inc-btn {
  flex: 1; padding: 12px 8px;
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.1);
  border-radius: 12px;
  font-size: 13px; font-weight: 700;
  font-family: 'Manrope', sans-serif;
  color: var(--text); cursor: pointer;
  transition: all .15s;
}
.inc-btn:hover { background: rgba(255,255,255,.1); }
.inc-btn:active { transform: scale(.96); }
.inc-big {
  background: rgba(46,204,113,.1);
  border-color: rgba(46,204,113,.25);
  color: var(--green);
}

.spectator-hint { font-size: 13px; text-align: center; }
</style>
