<template>
  <div class="overlay">
    <div class="sheet glass">
      <div class="sheet-handle" />

      <p class="section-title">Aprovação necessária</p>

      <div class="descricao-card">
        <div class="desc-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <line x1="12" y1="1" x2="12" y2="23"/>
            <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
          </svg>
        </div>
        <div>
          <p class="desc-text">{{ descricaoFormatada }}</p>
          <p class="desc-valor mono text-green">{{ formatMoney(dados.valor) }}</p>
        </div>
      </div>

      <!-- Timer + voters -->
      <div class="timer-row">
        <div class="timer-ring">
          <svg viewBox="0 0 44 44" class="ring-svg">
            <circle cx="22" cy="22" r="18" class="ring-bg"/>
            <circle
              cx="22" cy="22" r="18"
              class="ring-progress"
              :stroke-dasharray="113"
              :stroke-dashoffset="113 - (113 * timer / DURACAO)"
            />
          </svg>
          <span class="timer-num mono">{{ timer }}</span>
        </div>

        <div class="voters">
          <div
            v-for="v in votantes"
            :key="v.id"
            class="voter-avatar"
            :class="{
              'va-aprovado': v.voto === 'aprovado',
              'va-reprovado': v.voto === 'reprovado',
            }"
            :title="v.nome"
          >
            {{ v.nome[0].toUpperCase() }}
          </div>
        </div>
      </div>

      <p class="hint-text text-muted">Sem voto = aprovação automática</p>

      <div v-if="podeVotar" class="btn-row">
        <button class="btn btn-danger" @click="votar('reprovado')">Reprovar</button>
        <button class="btn btn-green" @click="votar('aprovado')">Aprovar</button>
      </div>
      <p v-else class="participante-hint text-muted">
        Você está envolvido nesta transação.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { usePartidaStore } from '../stores/partidaStore'
import { useJogadorStore } from '../stores/jogadorStore'
import { api } from '../stores/api'

const DURACAO = 10
const partida = usePartidaStore()
const jogador = useJogadorStore()

const dados = computed(() => partida.aprovacaoPendente)
const timer = ref(DURACAO)
let interval = null

const votantes = computed(() => {
  const votos = dados.value?.votos || {}
  return partida.jogadoresAtivos
    .filter(j => j.id !== dados.value?.origem_id && j.id !== dados.value?.destino_id)
    .map(j => ({ ...j, voto: votos[j.id] ?? null }))
})

const podeVotar = computed(() => {
  if (!dados.value) return false
  return jogador.id !== dados.value.origem_id && jogador.id !== dados.value.destino_id
})

const nomeJogador = (id) => {
  if (!id) return 'Banco'
  return partida.jogadores.find(j => j.id === id)?.nome || '?'
}

const descricaoFormatada = computed(() => {
  if (!dados.value) return ''
  const { tipo, origem_id, destino_id, descricao } = dados.value
  if (descricao) return descricao
  const mapa = {
    transferencia: `${nomeJogador(origem_id)} → ${nomeJogador(destino_id)}`,
    aluguel: `Aluguel de ${nomeJogador(destino_id)} para ${nomeJogador(origem_id)}`,
    compra_propriedade: `${nomeJogador(origem_id)} quer comprar propriedade`,
    compra_casa: `${nomeJogador(origem_id)} quer comprar casa`,
    venda_casa: `${nomeJogador(origem_id)} quer vender casa`,
    hipoteca: `${nomeJogador(destino_id)} quer hipotecar propriedade`,
    recuperar_hipoteca: `${nomeJogador(origem_id)} quer recuperar hipoteca`,
    pagamento_banco: `Pagamento do banco para ${nomeJogador(destino_id)}`,
  }
  return mapa[tipo] || tipo
})

const formatMoney = (val) => {
  if (!val && val !== 0) return ''
  return `R$ ${(val / 100).toLocaleString('pt-BR', { minimumFractionDigits: 0, maximumFractionDigits: 2 })}`
}

async function votar(voto) {
  try {
    await api.post(`/transacoes/${dados.value.transacao_id}/votar`, {
      session_token: jogador.sessionToken,
      voto,
    })
  } catch (e) {
    console.error(e)
  }
}

async function resolverTimeout() {
  if (!dados.value) return
  try {
    await api.post(`/transacoes/${dados.value.transacao_id}/resolver?session_token=${jogador.sessionToken}`)
  } catch {}
}

onMounted(() => {
  timer.value = DURACAO
  interval = setInterval(() => {
    timer.value--
    if (timer.value <= 0) {
      clearInterval(interval)
      resolverTimeout()
    }
  }, 1000)
})

onUnmounted(() => clearInterval(interval))
</script>

<style scoped>
.overlay {
  position: fixed; inset: 0; z-index: 100;
  background: rgba(0, 0, 0, .65);
  backdrop-filter: blur(4px);
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
  border-radius: 2px;
  align-self: center; margin-bottom: 4px;
}

.descricao-card {
  display: flex; align-items: center; gap: 14px;
  background: rgba(255, 255, 255, .04);
  border: 1px solid rgba(255, 255, 255, .08);
  border-radius: 14px; padding: 14px;
}

.desc-icon {
  width: 40px; height: 40px; border-radius: 50%; flex-shrink: 0;
  background: var(--green-dim);
  border: 1px solid rgba(46, 204, 113, .2);
  display: flex; align-items: center; justify-content: center;
  color: var(--green);
}
.desc-icon svg { width: 18px; height: 18px; }

.desc-text { font-size: 13px; font-weight: 600; color: var(--text); margin-bottom: 3px; }
.desc-valor { font-size: 16px; font-weight: 700; }

.timer-row {
  display: flex; align-items: center; gap: 16px;
}

.timer-ring {
  position: relative; width: 56px; height: 56px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
}
.ring-svg { position: absolute; inset: 0; transform: rotate(-90deg); width: 56px; height: 56px; }
.ring-bg { fill: none; stroke: rgba(255,255,255,.08); stroke-width: 3; }
.ring-progress { fill: none; stroke: var(--green); stroke-width: 3; stroke-linecap: round; transition: stroke-dashoffset .9s linear; }
.timer-num { font-size: 18px; font-weight: 700; z-index: 1; }

.voters { display: flex; flex-wrap: wrap; gap: 8px; }
.voter-avatar {
  width: 34px; height: 34px; border-radius: 50%;
  background: rgba(255, 255, 255, .07);
  border: 1px solid rgba(255, 255, 255, .1);
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; color: var(--text-2);
  transition: all .2s;
}
.va-aprovado { background: var(--green-dim); border-color: rgba(46, 204, 113, .3); color: var(--green); }
.va-reprovado { background: rgba(224, 84, 84, .12); border-color: rgba(224, 84, 84, .25); color: var(--danger); }

.hint-text { font-size: 12px; text-align: center; }

.btn-row { display: flex; gap: 10px; }
.btn-row .btn { flex: 1; }

.participante-hint { font-size: 13px; text-align: center; }
</style>
