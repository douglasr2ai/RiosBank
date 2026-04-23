<template>
  <div class="page">
    <div class="header">
      <div class="brand">Rios<span>Bank</span></div>
    </div>

    <div class="wrap">
      <div class="tabs">
        <button class="tab" :class="{ active: aba === 'minhas' }" @click="aba = 'minhas'">
          Minhas ({{ minhas.length }})
        </button>
        <button class="tab" :class="{ active: aba === 'disponiveis' }" @click="aba = 'disponiveis'">
          Disponíveis ({{ disponiveis.length }})
        </button>
      </div>

      <!-- Minhas propriedades -->
      <div v-if="aba === 'minhas'" class="prop-list">
        <div v-if="!minhas.length" class="empty text-muted">Você não tem imóveis ainda.</div>
        <div v-for="p in minhas" :key="p.id" class="prop-card glass">
          <div class="prop-colorbar" :style="{ background: p.propriedade.cor_hex || '#78909C' }" />
          <div class="prop-body">
            <p class="prop-nome">{{ p.propriedade.nome }}</p>
            <p class="prop-meta text-muted">
              <span v-if="p.propriedade.tipo === 'rua'">
                {{ p.num_casas > 0 ? p.num_casas + ' casa(s)' : '' }}
                {{ p.tem_hotel ? '1 hotel' : '' }}
                {{ !p.num_casas && !p.tem_hotel ? 'sem casas' : '' }}
              </span>
              <span v-else>Ação · dado × {{ formatMoney(p.propriedade.multiplicador_dado) }}</span>
              <span v-if="p.hipotecada" class="hipotecada-tag">hipotecada</span>
            </p>
          </div>
          <div class="prop-actions">
            <button
              v-if="!p.hipotecada && p.propriedade.tipo === 'rua'"
              class="pill-btn pill-casa"
              @click="abrirCasasModal(p)"
            >
              🏠 casas
            </button>
            <button v-if="!p.hipotecada" class="pill-btn pill-warn" @click="hipotecar(p)">
              hipot.
            </button>
            <button v-if="p.hipotecada" class="pill-btn pill-ok" @click="recuperar(p)">
              resgatar
            </button>
            <button class="pill-btn" @click="iniciarLeilao(p)">leilão</button>
          </div>
        </div>
      </div>

      <!-- Disponíveis -->
      <div v-if="aba === 'disponiveis'" class="prop-list">
        <div v-if="!disponiveis.length" class="empty text-muted">Nenhum imóvel disponível.</div>
        <div v-for="p in disponiveis" :key="p.id" class="prop-card glass">
          <div class="prop-colorbar" :style="{ background: p.propriedade.cor_hex || '#78909C' }" />
          <div class="prop-body">
            <p class="prop-nome">{{ p.propriedade.nome }}</p>
            <p class="prop-meta text-muted">
              <span class="mono">{{ formatMoney(p.propriedade.valor_compra) }}</span>
              <span v-if="p.propriedade.tipo === 'rua'"> · aluguel base {{ formatMoney(p.propriedade.aluguel_sem_casa) }}</span>
            </p>
          </div>
          <button class="pill-btn pill-ok" @click="comprar(p)">comprar</button>
        </div>
      </div>
    </div>

    <!-- Modal de casas -->
    <div v-if="showCasasModal && casasPosse" class="modal-overlay" @click.self="showCasasModal = false">
      <div class="modal-sheet glass">
        <div class="sheet-handle" />

        <!-- Header da propriedade -->
        <div class="casa-header">
          <span class="casa-cor" :style="{ background: casasPosse.propriedade.cor_hex || '#78909C' }" />
          <span class="casa-nome">{{ casasPosse.propriedade.nome }}</span>
        </div>

        <!-- Stepper -->
        <div class="casa-section-label">Quantas casas?</div>
        <div class="casa-stepper">
          <button
            v-for="opt in casasOpcoes"
            :key="opt.valor"
            class="casa-opt"
            :class="{
              'opt-current': opt.valor === casasAtual,
              'opt-selected': opt.valor === casasTarget,
              'opt-disabled': !opt.disponivel,
            }"
            :disabled="!opt.disponivel"
            @click="casasTarget = opt.valor"
          >
            <span class="opt-label">{{ opt.label }}</span>
            <span v-if="opt.aluguel != null" class="opt-aluguel">{{ formatMoneyShort(opt.aluguel) }}</span>
          </button>
        </div>

        <!-- Resumo -->
        <div v-if="casasTarget !== null && casasTarget !== casasAtual" class="casa-resumo">
          <div class="resumo-acao">{{ casasResumoAcao }}</div>
          <div class="resumo-valor" :class="casasNetCusto > 0 ? 'val-neg' : 'val-pos'">
            {{ casasNetCusto > 0 ? '-' : '+' }}{{ formatMoney(Math.abs(casasNetCusto)) }}
          </div>
        </div>

        <p v-if="casasErro" class="erro-msg">{{ casasErro }}</p>

        <button
          class="btn btn-green"
          :disabled="casasTarget === null || casasTarget === casasAtual"
          @click="confirmarCasas"
        >
          Confirmar
        </button>
      </div>
    </div>

    <BottomNav :sala-id="salaId" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
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

const aba = ref('minhas')

const minhas = computed(() => partida.posses.filter(p => p.jogador_id === jogador.id))
const disponiveis = computed(() => partida.posses.filter(p => !p.jogador_id))

const formatMoney = (val) => {
  if (!val && val !== 0) return 'R$0'
  return `R$ ${(val / 100).toLocaleString('pt-BR', { minimumFractionDigits: 0 })}`
}

const formatMoneyShort = (val) => {
  if (!val && val !== 0) return ''
  const r = val / 100
  if (r >= 1000) return `${(r / 1000).toFixed(r % 1000 === 0 ? 0 : 1)}k`
  return `${r}`
}

// ── Modal casas ──────────────────────────────────────────────────────────

const showCasasModal = ref(false)
const casasPosse = ref(null)
const casasTarget = ref(null)   // 0-4 = casas, 5 = hotel
const casasErro = ref('')

// 5 = hotel
const casasAtual = computed(() => {
  if (!casasPosse.value) return 0
  return casasPosse.value.tem_hotel ? 5 : casasPosse.value.num_casas
})

const casasOpcoes = computed(() => {
  if (!casasPosse.value) return []
  const p = casasPosse.value.propriedade
  const atual = casasAtual.value
  const sala = partida.sala

  return [
    { valor: 0, label: '0', aluguel: p.aluguel_sem_casa,  disponivel: atual !== 0 },
    { valor: 1, label: '1', aluguel: p.aluguel_1_casa,    disponivel: atual !== 1 && (atual > 1 || (sala?.casas_disponiveis ?? 0) >= 1) },
    { valor: 2, label: '2', aluguel: p.aluguel_2_casas,   disponivel: atual !== 2 && (atual > 2 || (sala?.casas_disponiveis ?? 0) >= (2 - atual)) },
    { valor: 3, label: '3', aluguel: p.aluguel_3_casas,   disponivel: atual !== 3 && (atual > 3 || (sala?.casas_disponiveis ?? 0) >= (3 - atual)) },
    { valor: 4, label: '4', aluguel: p.aluguel_4_casas,   disponivel: atual !== 4 && atual !== 5 && (atual > 4 || (sala?.casas_disponiveis ?? 0) >= (4 - atual)) },
    { valor: 5, label: '🏨', aluguel: p.aluguel_hotel,   disponivel: atual === 4 || atual === 5 },
  ]
})

const casasNetCusto = computed(() => {
  const p = casasPosse.value?.propriedade
  if (!p || casasTarget.value === null) return 0
  const atual = casasAtual.value
  const target = casasTarget.value

  if (atual === 4 && target === 5) return p.custo_hotel ?? p.custo_casa    // comprar hotel
  if (atual === 5 && target === 4) return -Math.floor((p.custo_hotel ?? p.custo_casa) / 2) // vender hotel
  if (target > atual) return (target - atual) * p.custo_casa               // comprar casas
  return (target - atual) * Math.floor(p.custo_casa / 2)                   // vender casas (negativo = recebe)
})

const casasResumoAcao = computed(() => {
  const atual = casasAtual.value
  const target = casasTarget.value
  if (atual === 5 && target === 4) return 'Vender hotel → 4 casas'
  if (atual === 4 && target === 5) return 'Comprar hotel'
  if (target > atual) return `Comprar ${target - atual} casa(s) · de ${atual} → ${target}`
  return `Vender ${atual - target} casa(s) · de ${atual} → ${target}`
})

function abrirCasasModal(posse) {
  casasPosse.value = posse
  casasTarget.value = null
  casasErro.value = ''
  showCasasModal.value = true
}

async function confirmarCasas() {
  casasErro.value = ''
  const atual = casasAtual.value
  const target = casasTarget.value
  const p = casasPosse.value
  const prop = p.propriedade
  const custo = casasNetCusto.value   // positivo = paga, negativo = recebe

  try {
    if (target > atual || (atual === 4 && target === 5)) {
      // Comprar casas / hotel
      await api.post('/transacoes', {
        sala_id: salaId.value,
        session_token: jogador.sessionToken,
        tipo: 'compra_casa',
        valor: Math.abs(custo),
        propriedade_id: p.propriedade_id,
        descricao: casasResumoAcao.value + ` em ${prop.nome}`,
      })
    } else {
      // Vender casas / hotel
      await api.post('/transacoes', {
        sala_id: salaId.value,
        session_token: jogador.sessionToken,
        tipo: 'venda_casa',
        valor: Math.abs(custo),
        propriedade_id: p.propriedade_id,
        descricao: casasResumoAcao.value + ` em ${prop.nome}`,
      })
    }
    showCasasModal.value = false
  } catch (e) {
    casasErro.value = e.message
  }
}

// ── Outras ações ──────────────────────────────────────────────────────────

async function comprar(posse) {
  try {
    await api.post('/transacoes', {
      sala_id: salaId.value,
      session_token: jogador.sessionToken,
      tipo: 'compra_propriedade',
      valor: posse.propriedade.valor_compra,
      propriedade_id: posse.propriedade_id,
      descricao: `${jogador.nome} quer comprar ${posse.propriedade.nome}`,
    })
  } catch (e) { toast.add(e.message) }
}

async function hipotecar(posse) {
  try {
    await api.post('/transacoes', {
      sala_id: salaId.value,
      session_token: jogador.sessionToken,
      tipo: 'hipoteca',
      valor: posse.propriedade.valor_hipoteca,
      propriedade_id: posse.propriedade_id,
      descricao: `${jogador.nome} quer hipotecar ${posse.propriedade.nome}`,
    })
  } catch (e) { toast.add(e.message) }
}

async function recuperar(posse) {
  const custo = Math.round(posse.propriedade.valor_hipoteca * 1.2)
  try {
    await api.post('/transacoes', {
      sala_id: salaId.value,
      session_token: jogador.sessionToken,
      tipo: 'recuperar_hipoteca',
      valor: custo,
      propriedade_id: posse.propriedade_id,
      descricao: `${jogador.nome} quer recuperar hipoteca de ${posse.propriedade.nome}`,
    })
  } catch (e) { toast.add(e.message) }
}

async function iniciarLeilao(posse) {
  try {
    await api.post('/leiloes', {
      sala_id: salaId.value,
      session_token: jogador.sessionToken,
      propriedade_id: posse.propriedade_id,
    })
  } catch (e) { toast.add(e.message) }
}

onMounted(async () => {
  if (!partida.posses.length) await partida.carregarPropriedades(salaId.value)
})
</script>

<style scoped>
.page { min-height: 100dvh; display: flex; flex-direction: column; align-items: center; padding: 0 20px calc(var(--nav-h) + 24px); position: relative; }
.header { width: 100%; max-width: 360px; display: flex; align-items: center; justify-content: space-between; padding: 20px 0 16px; position: relative; z-index: 1; }
.brand { font-size: 20px; font-weight: 800; letter-spacing: -.5px; }
.brand span { color: var(--green); }
.wrap { width: 100%; max-width: 360px; display: flex; flex-direction: column; gap: 12px; position: relative; z-index: 1; }

.tabs { display: flex; gap: 4px; background: rgba(255,255,255,.04); border-radius: 12px; padding: 4px; }
.tab { flex: 1; padding: 8px; border: none; background: none; border-radius: 9px; font-size: 12px; font-weight: 700; font-family: 'Manrope', sans-serif; color: var(--text-2); cursor: pointer; transition: all .2s; }
.tab.active { background: rgba(46,204,113,.15); color: var(--green); }

.prop-list { display: flex; flex-direction: column; gap: 8px; }
.prop-card { display: flex; align-items: center; gap: 0; border-radius: 14px; overflow: hidden; }
.prop-colorbar { width: 4px; align-self: stretch; flex-shrink: 0; }
.prop-body { flex: 1; padding: 12px 10px; min-width: 0; }
.prop-nome { font-size: 13px; font-weight: 700; }
.prop-meta { font-size: 11px; margin-top: 2px; display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }

.hipotecada-tag { background: rgba(224,84,84,.1); color: var(--danger); border-radius: 4px; padding: 1px 6px; font-size: 10px; font-weight: 700; }

.prop-actions { display: flex; gap: 4px; padding: 8px 10px 8px 0; flex-wrap: wrap; justify-content: flex-end; }
.pill-btn { background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.1); border-radius: 8px; padding: 4px 8px; font-size: 10px; font-weight: 700; font-family: 'Manrope', sans-serif; color: var(--text-2); cursor: pointer; white-space: nowrap; transition: all .15s; }
.pill-btn:hover { background: rgba(255,255,255,.1); color: var(--text); }
.pill-ok   { background: var(--green-dim); border-color: rgba(46,204,113,.2); color: var(--green); }
.pill-warn { background: rgba(246,173,85,.1); border-color: rgba(246,173,85,.2); color: var(--amber); }
.pill-casa { background: rgba(156,39,176,.1); border-color: rgba(156,39,176,.2); color: #CE93D8; }

.empty { font-size: 13px; text-align: center; padding: 32px 0; }

/* ── Modal ── */
.modal-overlay { position: fixed; inset: 0; z-index: 80; background: rgba(0,0,0,.6); backdrop-filter: blur(4px); display: flex; align-items: flex-end; justify-content: center; }
.modal-sheet { width: 100%; max-width: 480px; border-radius: 24px 24px 0 0; padding: 16px 20px 40px; display: flex; flex-direction: column; gap: 16px; }
.sheet-handle { width: 40px; height: 4px; background: rgba(255,255,255,.15); border-radius: 2px; align-self: center; margin-bottom: 4px; }

.casa-header { display: flex; align-items: center; gap: 10px; }
.casa-cor { width: 12px; height: 12px; border-radius: 4px; flex-shrink: 0; }
.casa-nome { font-size: 17px; font-weight: 800; }

.casa-section-label { font-size: 11px; font-family: 'JetBrains Mono', monospace; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: var(--text-2); }

.casa-stepper { display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; }
.casa-opt {
  display: flex; flex-direction: column; align-items: center; gap: 3px;
  padding: 10px 4px;
  background: rgba(255,255,255,.05);
  border: 1px solid rgba(255,255,255,.09);
  border-radius: 12px;
  cursor: pointer;
  font-family: 'Manrope', sans-serif;
  transition: all .15s;
}
.opt-label { font-size: 16px; font-weight: 800; color: var(--text); }
.opt-aluguel { font-size: 9px; font-family: 'JetBrains Mono', monospace; color: var(--text-2); }

.casa-opt.opt-current { border-color: rgba(255,255,255,.25); background: rgba(255,255,255,.08); }
.casa-opt.opt-current .opt-label { color: var(--text-2); }

.casa-opt.opt-selected { border-color: rgba(46,204,113,.4); background: var(--green-dim); }
.casa-opt.opt-selected .opt-label { color: var(--green); }
.casa-opt.opt-selected .opt-aluguel { color: var(--green); opacity: .8; }

.casa-opt.opt-disabled { opacity: .3; cursor: not-allowed; }

.casa-resumo {
  display: flex; align-items: center; justify-content: space-between;
  background: rgba(255,255,255,.04); border: 1px solid rgba(255,255,255,.08);
  border-radius: var(--radius-sm); padding: 12px 14px;
}
.resumo-acao { font-size: 13px; font-weight: 600; }
.resumo-valor { font-family: 'JetBrains Mono', monospace; font-size: 15px; font-weight: 700; }
.val-pos { color: var(--green); }
.val-neg { color: var(--danger); }

.erro-msg { font-size: 12px; color: var(--danger); }
</style>
