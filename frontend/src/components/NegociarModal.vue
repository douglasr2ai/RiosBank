<template>
  <div v-if="modelValue" class="overlay" @click.self="fechar">
    <div class="sheet glass">
      <div class="sheet-handle" />
      <h3 class="modal-title">Negociar</h3>

      <!-- Passo 1: Selecionar jogador -->
      <template v-if="passo === 1">
        <p class="step-hint text-muted">Com quem você quer negociar?</p>
        <div class="jogadores-list">
          <button
            v-for="j in outrosJogadores"
            :key="j.id"
            class="jogador-card"
            @click="selecionarJogador(j)"
          >
            <div class="jog-avatar">{{ j.nome?.[0]?.toUpperCase() }}</div>
            <div class="jog-info">
              <span class="jog-nome">{{ j.nome }}</span>
              <span class="jog-saldo text-muted mono">{{ formatMoney(j.saldo) }}</span>
            </div>
            <svg class="jog-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <polyline points="9 18 15 12 9 6"/>
            </svg>
          </button>
          <p v-if="!outrosJogadores.length" class="no-items text-muted">Nenhum outro jogador ativo.</p>
        </div>
      </template>

      <!-- Passo 2: Montar oferta -->
      <template v-else-if="passo === 2">
        <div class="destino-header">
          <button class="back-btn" @click="passo = 1">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <polyline points="15 18 9 12 15 6"/>
            </svg>
          </button>
          <div class="jog-avatar sm">{{ jogadorSelecionado?.nome?.[0]?.toUpperCase() }}</div>
          <span class="destino-nome">{{ jogadorSelecionado?.nome }}</span>
        </div>

        <!-- Você oferece -->
        <div class="secao-negoc">
          <p class="secao-titulo">Você oferece</p>

          <div class="field">
            <label>Dinheiro (R$)</label>
            <div class="input-wrap">
              <span class="input-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="width:15px;height:15px">
                  <line x1="12" y1="1" x2="12" y2="23"/>
                  <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
                </svg>
              </span>
              <input v-model.number="dinheiroEnviado" type="number" placeholder="0" min="0" />
            </div>
          </div>

          <div v-if="minhasPropriedadesNeg.length" class="props-list">
            <p class="props-label text-muted">Imóveis</p>
            <label
              v-for="p in minhasPropriedadesNeg"
              :key="p.id"
              class="prop-check"
              :class="{ 'prop-check--on': propEnviadas.includes(p.propriedade_id) }"
            >
              <input
                type="checkbox"
                :value="p.propriedade_id"
                v-model="propEnviadas"
                style="display:none"
              />
              <span class="prop-cor" :style="p.propriedade.cor_hex ? `background:${p.propriedade.cor_hex}` : ''" />
              <span class="prop-nome">{{ p.propriedade.nome }}</span>
              <span class="prop-check-icon">
                <svg v-if="propEnviadas.includes(p.propriedade_id)" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
              </span>
            </label>
          </div>
        </div>

        <!-- Você quer receber -->
        <div class="secao-negoc">
          <p class="secao-titulo">Você quer receber</p>

          <div class="field">
            <label>Dinheiro (R$)</label>
            <div class="input-wrap">
              <span class="input-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="width:15px;height:15px">
                  <line x1="12" y1="1" x2="12" y2="23"/>
                  <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
                </svg>
              </span>
              <input v-model.number="dinheiroRecebido" type="number" placeholder="0" min="0" />
            </div>
          </div>

          <div v-if="propsDestinatario.length" class="props-list">
            <p class="props-label text-muted">Imóveis de {{ jogadorSelecionado?.nome }}</p>
            <label
              v-for="p in propsDestinatario"
              :key="p.id"
              class="prop-check"
              :class="{ 'prop-check--on': propRecebidas.includes(p.propriedade_id) }"
            >
              <input
                type="checkbox"
                :value="p.propriedade_id"
                v-model="propRecebidas"
                style="display:none"
              />
              <span class="prop-cor" :style="p.propriedade.cor_hex ? `background:${p.propriedade.cor_hex}` : ''" />
              <span class="prop-nome">{{ p.propriedade.nome }}</span>
              <span class="prop-check-icon">
                <svg v-if="propRecebidas.includes(p.propriedade_id)" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
              </span>
            </label>
          </div>
          <p v-else-if="jogadorSelecionado" class="no-items text-muted">{{ jogadorSelecionado.nome }} não tem imóveis disponíveis.</p>
        </div>

        <p v-if="erro" class="erro-msg">{{ erro }}</p>

        <button
          class="btn btn-pink"
          :disabled="!ofertaValida || enviando"
          @click="propor"
        >
          {{ enviando ? 'Enviando...' : 'Propor negociação' }}
        </button>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useJogadorStore } from '../stores/jogadorStore'
import { usePartidaStore } from '../stores/partidaStore'
import { api } from '../stores/api'

const props = defineProps({
  modelValue: Boolean,
  salaId: String,
})

const emit = defineEmits(['update:modelValue'])

const jogador = useJogadorStore()
const partida = usePartidaStore()

const passo = ref(1)
const jogadorSelecionado = ref(null)
const dinheiroEnviado = ref(0)
const dinheiroRecebido = ref(0)
const propEnviadas = ref([])
const propRecebidas = ref([])
const erro = ref('')
const enviando = ref(false)

const outrosJogadores = computed(() =>
  partida.jogadoresAtivos.filter(j => j.id !== jogador.id)
)

const minhasPropriedadesNeg = computed(() =>
  partida.posses.filter(p => p.jogador_id === jogador.id && !p.hipotecada)
)

const propsDestinatario = computed(() =>
  partida.posses.filter(
    p => p.jogador_id === jogadorSelecionado.value?.id && !p.hipotecada
  )
)

const ofertaValida = computed(() => {
  const temEnvia = (dinheiroEnviado.value > 0) || propEnviadas.value.length > 0
  const temRecebe = (dinheiroRecebido.value > 0) || propRecebidas.value.length > 0
  return temEnvia && temRecebe
})

const formatMoney = (val) => {
  if (!val && val !== 0) return 'R$ 0'
  return `R$ ${(val / 100).toLocaleString('pt-BR', { minimumFractionDigits: 0 })}`
}

function selecionarJogador(j) {
  jogadorSelecionado.value = j
  dinheiroEnviado.value = 0
  dinheiroRecebido.value = 0
  propEnviadas.value = []
  propRecebidas.value = []
  erro.value = ''
  passo.value = 2
}

function fechar() {
  emit('update:modelValue', false)
  // Reset state
  passo.value = 1
  jogadorSelecionado.value = null
  dinheiroEnviado.value = 0
  dinheiroRecebido.value = 0
  propEnviadas.value = []
  propRecebidas.value = []
  erro.value = ''
}

async function propor() {
  if (!ofertaValida.value) return
  erro.value = ''
  enviando.value = true
  try {
    await api.post('/transacoes', {
      sala_id: props.salaId,
      session_token: jogador.sessionToken,
      tipo: 'negociacao',
      valor: 0,
      destino_id: jogadorSelecionado.value.id,
      negociacao_dados: {
        dinheiro_enviado: Math.round((dinheiroEnviado.value || 0) * 100),
        dinheiro_recebido: Math.round((dinheiroRecebido.value || 0) * 100),
        propriedades_enviadas: [...propEnviadas.value],
        propriedades_recebidas: [...propRecebidas.value],
      },
    })
    fechar()
  } catch (e) {
    erro.value = e.message || 'Erro ao propor negociação'
  } finally {
    enviando.value = false
  }
}
</script>

<style scoped>
.overlay {
  position: fixed; inset: 0; z-index: 80;
  background: rgba(0, 0, 0, .65);
  backdrop-filter: blur(4px);
  display: flex; align-items: flex-end; justify-content: center;
}

.sheet {
  width: 100%; max-width: 480px;
  border-radius: 24px 24px 0 0;
  padding: 16px 20px 40px;
  display: flex; flex-direction: column; gap: 16px;
  max-height: 90dvh;
  overflow-y: auto;
}

.sheet-handle {
  width: 40px; height: 4px;
  background: rgba(255, 255, 255, .15);
  border-radius: 2px;
  align-self: center; margin-bottom: 4px;
  flex-shrink: 0;
}

.modal-title { font-size: 18px; font-weight: 800; flex-shrink: 0; }

.step-hint { font-size: 13px; }

.jogadores-list { display: flex; flex-direction: column; gap: 8px; }

.jogador-card {
  display: flex; align-items: center; gap: 12px;
  background: rgba(255, 255, 255, .04);
  border: 1px solid rgba(255, 255, 255, .08);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  cursor: pointer; transition: all .2s;
  font-family: 'Manrope', sans-serif;
}
.jogador-card:hover { background: rgba(255, 255, 255, .08); border-color: rgba(255, 255, 255, .15); }
.jogador-card:active { transform: scale(.98); }

.jog-avatar {
  width: 38px; height: 38px; border-radius: 50%; flex-shrink: 0;
  background: rgba(236, 72, 153, .15);
  border: 1px solid rgba(236, 72, 153, .25);
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 800; color: #ec4899;
}
.jog-avatar.sm { width: 28px; height: 28px; font-size: 11px; flex-shrink: 0; }

.jog-info { flex: 1; display: flex; flex-direction: column; gap: 2px; text-align: left; }
.jog-nome { font-size: 14px; font-weight: 700; color: var(--text); }
.jog-saldo { font-size: 12px; }

.jog-arrow { width: 16px; height: 16px; color: var(--text-2); flex-shrink: 0; }

.destino-header {
  display: flex; align-items: center; gap: 10px;
}

.back-btn {
  width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;
  background: rgba(255, 255, 255, .06);
  border: 1px solid rgba(255, 255, 255, .1);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: var(--text-2);
  transition: background .15s;
}
.back-btn:hover { background: rgba(255, 255, 255, .12); }
.back-btn svg { width: 16px; height: 16px; }

.destino-nome { font-size: 15px; font-weight: 700; }

.secao-negoc {
  background: rgba(255, 255, 255, .03);
  border: 1px solid rgba(255, 255, 255, .07);
  border-radius: 14px;
  padding: 14px;
  display: flex; flex-direction: column; gap: 10px;
}

.secao-titulo { font-size: 13px; font-weight: 700; color: var(--text-2); }

.props-list { display: flex; flex-direction: column; gap: 6px; }
.props-label { font-size: 11px; margin-bottom: 2px; }

.prop-check {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, .03);
  border: 1px solid rgba(255, 255, 255, .07);
  border-radius: var(--radius-sm);
  cursor: pointer; transition: all .15s;
}
.prop-check--on {
  background: rgba(236, 72, 153, .08);
  border-color: rgba(236, 72, 153, .25);
}
.prop-check:hover { background: rgba(255, 255, 255, .07); }
.prop-check--on:hover { background: rgba(236, 72, 153, .13); }

.prop-cor {
  width: 10px; height: 10px; border-radius: 3px; flex-shrink: 0;
  background: var(--text-2);
}
.prop-nome { flex: 1; font-size: 13px; font-weight: 600; color: var(--text); }
.prop-check-icon {
  width: 20px; height: 20px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  color: #ec4899;
}
.prop-check-icon svg { width: 14px; height: 14px; }

.no-items { font-size: 13px; text-align: center; padding: 8px 0; }
.erro-msg { font-size: 12px; color: var(--danger); }

.btn-pink {
  background: rgba(236, 72, 153, .15);
  border: 1px solid rgba(236, 72, 153, .3);
  color: #ec4899;
  padding: 14px;
  border-radius: var(--radius-sm);
  font-size: 14px; font-weight: 700;
  cursor: pointer; transition: all .2s;
  font-family: 'Manrope', sans-serif;
}
.btn-pink:hover:not(:disabled) {
  background: rgba(236, 72, 153, .25);
  border-color: rgba(236, 72, 153, .5);
}
.btn-pink:disabled {
  opacity: .4; cursor: not-allowed;
}
</style>
