<template>
  <div class="overlay">
    <div class="sheet glass">
      <div class="sheet-handle" />

      <p class="section-title">{{ dados?.tipo === 'negociacao' ? 'Proposta de negociação' : 'Aprovação necessária' }}</p>

      <!-- Card de negociação -->
      <template v-if="dados?.tipo === 'negociacao'">
        <div class="negoc-card">
          <div class="negoc-proponente">
            <div class="negoc-avatar">{{ nomeJogador(dados.origem_id)?.[0]?.toUpperCase() }}</div>
            <span class="negoc-proponente-nome">{{ nomeJogador(dados.origem_id) }}</span>
            <span class="negoc-label text-muted">propôs</span>
          </div>

          <div class="negoc-lados">
            <div class="negoc-lado">
              <p class="negoc-lado-titulo">Oferece</p>
              <p v-if="dados.negociacao_dados?.dinheiro_enviado > 0" class="negoc-valor mono text-green">
                {{ formatMoney(dados.negociacao_dados.dinheiro_enviado) }}
              </p>
              <template v-if="dados.negociacao_dados?.propriedades_enviadas?.length">
                <div
                  v-for="pid in dados.negociacao_dados.propriedades_enviadas"
                  :key="pid"
                  class="negoc-prop"
                >
                  <span class="negoc-prop-cor" :style="corDaPropriedade(pid)" />
                  <span class="negoc-prop-nome">{{ nomeDaPropriedade(pid) }}</span>
                </div>
              </template>
              <p v-if="!dados.negociacao_dados?.dinheiro_enviado && !dados.negociacao_dados?.propriedades_enviadas?.length" class="negoc-nada text-muted">—</p>
            </div>

            <div class="negoc-seta">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <path d="M7 16V4m0 0L3 8m4-4l4 4M17 8v12m0 0l4-4m-4 4l-4-4"/>
              </svg>
            </div>

            <div class="negoc-lado">
              <p class="negoc-lado-titulo">Quer receber</p>
              <p v-if="dados.negociacao_dados?.dinheiro_recebido > 0" class="negoc-valor mono text-green">
                {{ formatMoney(dados.negociacao_dados.dinheiro_recebido) }}
              </p>
              <template v-if="dados.negociacao_dados?.propriedades_recebidas?.length">
                <div
                  v-for="pid in dados.negociacao_dados.propriedades_recebidas"
                  :key="pid"
                  class="negoc-prop"
                >
                  <span class="negoc-prop-cor" :style="corDaPropriedade(pid)" />
                  <span class="negoc-prop-nome">{{ nomeDaPropriedade(pid) }}</span>
                </div>
              </template>
              <p v-if="!dados.negociacao_dados?.dinheiro_recebido && !dados.negociacao_dados?.propriedades_recebidas?.length" class="negoc-nada text-muted">—</p>
            </div>
          </div>
        </div>

        <!-- Timer para negociação -->
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
          <div class="negoc-aguardando-txt">
            <template v-if="podeVotar && !jaVotei">Aceite ou rejeite esta proposta</template>
            <template v-else-if="podeVotar && jaVotei">Resposta registrada</template>
            <template v-else-if="jogador.id === dados.origem_id">Aguardando resposta de {{ nomeJogador(dados.destino_id) }}...</template>
            <template v-else>Negociação em andamento — apenas {{ nomeJogador(dados.destino_id) }} pode aceitar ou rejeitar</template>
          </div>
        </div>

        <div v-if="podeVotar && !jaVotei" class="btn-row">
          <button class="btn btn-danger" @click="votar('reprovado')">Rejeitar</button>
          <button class="btn btn-green" @click="votar('aprovado')">Aceitar</button>
        </div>
        <div v-else-if="podeVotar && jaVotei" class="voto-confirmado">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          Resposta enviada
        </div>
      </template>

      <!-- Card de transação normal -->
      <template v-else>
        <div class="descricao-card">
          <div class="desc-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <line x1="12" y1="1" x2="12" y2="23"/>
              <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
            </svg>
          </div>
          <div>
            <p class="desc-text">{{ descricaoFormatada }}</p>
            <p class="desc-valor mono text-green">{{ formatMoney(dados?.valor) }}</p>
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

        <div v-if="podeVotar && !jaVotei" class="btn-row">
          <button class="btn btn-danger" @click="votar('reprovado')">Reprovar</button>
          <button class="btn btn-green" @click="votar('aprovado')">Aprovar</button>
        </div>
        <div v-else-if="podeVotar && jaVotei" class="voto-confirmado">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          Voto registrado · aguardando os demais
        </div>
        <p v-else class="participante-hint text-muted">
          Você está envolvido nesta transação.
        </p>
      </template>
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
const jaVotei = ref(false)
let interval = null

const votantes = computed(() => {
  if (dados.value?.tipo === 'negociacao') return []  // só destinatário vota, não exibe lista
  const votos = dados.value?.votos || {}
  return partida.jogadoresAtivos
    .filter(j => j.id !== dados.value?.origem_id && j.id !== dados.value?.destino_id)
    .map(j => ({ ...j, voto: votos[j.id] ?? null }))
})

const podeVotar = computed(() => {
  if (!dados.value) return false
  if (dados.value.tipo === 'negociacao') {
    return jogador.id === dados.value.destino_id
  }
  return jogador.id !== dados.value.origem_id && jogador.id !== dados.value.destino_id
})

const nomeJogador = (id) => {
  if (!id) return 'Banco'
  return partida.jogadores.find(j => j.id === id)?.nome || '?'
}

const nomeDaPropriedade = (pid) => {
  const posse = partida.posses.find(p => p.propriedade_id === pid)
  return posse?.propriedade?.nome || `#${pid}`
}

const corDaPropriedade = (pid) => {
  const posse = partida.posses.find(p => p.propriedade_id === pid)
  const cor = posse?.propriedade?.cor_hex
  return cor ? `background:${cor}` : ''
}

const descricaoFormatada = computed(() => {
  if (!dados.value) return ''
  const { tipo, origem_id, destino_id, descricao } = dados.value
  if (tipo === 'negociacao') {
    const nd = dados.value.negociacao_dados
    if (!nd) return `${nomeJogador(origem_id)} propôs uma negociação`
    const partes = []
    if (nd.dinheiro_enviado > 0) partes.push(`R$ ${(nd.dinheiro_enviado / 100).toLocaleString('pt-BR')}`)
    if (nd.propriedades_enviadas?.length) partes.push(`${nd.propriedades_enviadas.length} imóvel(is)`)
    const recebe = []
    if (nd.dinheiro_recebido > 0) recebe.push(`R$ ${(nd.dinheiro_recebido / 100).toLocaleString('pt-BR')}`)
    if (nd.propriedades_recebidas?.length) recebe.push(`${nd.propriedades_recebidas.length} imóvel(is)`)
    return `${nomeJogador(origem_id)} oferece ${partes.join(' + ') || 'nada'} por ${recebe.join(' + ') || 'nada'} de ${nomeJogador(destino_id)}`
  }
  if (descricao) return descricao
  const mapa = {
    transferencia: `${nomeJogador(origem_id)} → ${nomeJogador(destino_id)}`,
    aluguel: `${nomeJogador(destino_id)} cobrando aluguel de ${nomeJogador(origem_id)}`,
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
    jaVotei.value = true
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

.voto-confirmado {
  display: flex; align-items: center; justify-content: center; gap: 8px;
  padding: 14px;
  background: var(--green-dim);
  border: 1px solid rgba(46, 204, 113, .2);
  border-radius: var(--radius-sm);
  font-size: 13px; font-weight: 600; color: var(--green);
}
.voto-confirmado svg { width: 16px; height: 16px; flex-shrink: 0; }

.participante-hint { font-size: 13px; text-align: center; }

/* Negociação */
.negoc-card {
  background: rgba(255, 255, 255, .03);
  border: 1px solid rgba(255, 255, 255, .08);
  border-radius: 14px;
  padding: 14px;
  display: flex; flex-direction: column; gap: 12px;
}

.negoc-proponente {
  display: flex; align-items: center; gap: 8px;
}

.negoc-avatar {
  width: 28px; height: 28px; border-radius: 50%; flex-shrink: 0;
  background: rgba(236, 72, 153, .15);
  border: 1px solid rgba(236, 72, 153, .25);
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 800; color: #ec4899;
}

.negoc-proponente-nome { font-size: 13px; font-weight: 700; }
.negoc-label { font-size: 12px; }

.negoc-lados {
  display: flex; gap: 8px; align-items: flex-start;
}

.negoc-lado {
  flex: 1; display: flex; flex-direction: column; gap: 6px;
  background: rgba(255, 255, 255, .03);
  border: 1px solid rgba(255, 255, 255, .07);
  border-radius: 10px;
  padding: 10px;
  min-width: 0;
}

.negoc-lado-titulo {
  font-size: 11px; font-weight: 700; color: var(--text-2); text-transform: uppercase; letter-spacing: .5px;
}

.negoc-valor { font-size: 14px; font-weight: 700; }

.negoc-prop {
  display: flex; align-items: center; gap: 6px;
}

.negoc-prop-cor {
  width: 8px; height: 8px; border-radius: 2px; flex-shrink: 0;
  background: var(--text-2);
}

.negoc-prop-nome {
  font-size: 11px; font-weight: 600; color: var(--text);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

.negoc-nada { font-size: 12px; }

.negoc-seta {
  display: flex; align-items: center; justify-content: center;
  padding-top: 28px;
  color: var(--text-2); flex-shrink: 0;
}
.negoc-seta svg { width: 18px; height: 18px; }

.negoc-aguardando-txt {
  flex: 1; font-size: 13px; font-weight: 600; color: var(--text-2);
}
</style>
