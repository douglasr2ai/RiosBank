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
        <div v-for="p in minhas" :key="p.id" class="prop-card glass" @click="abrirDetalhe(p)">
          <div class="prop-colorbar" :style="{ background: p.propriedade.cor_hex || '#78909C' }" />
          <div class="prop-body">
            <div class="prop-row">
              <span class="prop-nome">{{ p.propriedade.nome }}</span>
              <span v-if="p.hipotecada" class="tag tag-danger">hipotecada</span>
            </div>
            <div class="prop-info">
              <template v-if="p.tem_hotel">
                <span class="hotel-dot">H</span>
              </template>
              <template v-else-if="p.num_casas > 0">
                <span v-for="n in p.num_casas" :key="n" class="casa-dot" />
              </template>
              <span v-else class="prop-meta text-muted">
                {{ p.propriedade.tipo === 'acao' ? 'Ação' : 'sem casas' }}
              </span>
            </div>
          </div>
          <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <polyline points="9 18 15 12 9 6"/>
          </svg>
        </div>
      </div>

      <!-- Disponíveis -->
      <div v-if="aba === 'disponiveis'" class="prop-list">
        <div v-if="!disponiveis.length" class="empty text-muted">Nenhum imóvel disponível.</div>
        <div v-for="p in disponiveis" :key="p.id" class="prop-card glass">
          <div class="prop-colorbar" :style="{ background: p.propriedade.cor_hex || '#78909C' }" />
          <div class="prop-body">
            <div class="prop-row">
              <span class="prop-nome">{{ p.propriedade.nome }}</span>
              <span class="prop-meta mono">{{ formatMoney(p.propriedade.valor_compra) }}</span>
            </div>
            <span class="prop-meta text-muted">
              <template v-if="p.propriedade.tipo === 'rua'">aluguel base {{ formatMoney(p.propriedade.aluguel_sem_casa) }}</template>
              <template v-else>Ação · dado × {{ formatMoney(p.propriedade.multiplicador_dado) }}</template>
            </span>
          </div>
          <button class="pill-btn pill-ok" @click.stop="comprar(p)">Comprar</button>
        </div>
      </div>
    </div>

    <!-- Modal de detalhe (minhas propriedades) -->
    <div v-if="detalhePosse" class="modal-overlay" @click.self="fecharDetalhe">
      <div class="modal-sheet glass">
        <div class="sheet-handle" />

        <!-- Header -->
        <div class="detalhe-header">
          <span class="detalhe-cor" :style="{ background: detalhePosse.propriedade.cor_hex || '#78909C' }" />
          <span class="detalhe-nome">{{ detalhePosse.propriedade.nome }}</span>
          <span v-if="detalhePosse.hipotecada" class="tag tag-danger">hipotecada</span>
        </div>

        <!-- Tabela de aluguéis (apenas rua) -->
        <div v-if="detalhePosse.propriedade.tipo === 'rua'" class="aluguel-table">
          <p class="section-label">Aluguéis</p>
          <div
            v-for="linha in tabelaAlugueis"
            :key="linha.label"
            class="aluguel-row"
            :class="{ 'row-ativo': linha.ativo }"
          >
            <span class="row-label">{{ linha.label }}</span>
            <span class="row-valor mono">{{ formatMoney(linha.valor) }}</span>
          </div>
        </div>

        <!-- Info de ação -->
        <div v-else class="acao-info">
          <p class="section-label">Tipo: Ação</p>
          <p class="acao-multi">Dado × <strong>{{ formatMoney(detalhePosse.propriedade.multiplicador_dado) }}</strong></p>
        </div>

        <!-- Stepper de casas (somente rua não hipotecada) -->
        <div v-if="detalhePosse.propriedade.tipo === 'rua' && !detalhePosse.hipotecada">
          <p class="section-label">Casas / Hotel</p>
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

          <div v-if="casasTarget !== null && casasTarget !== casasAtual" class="casa-resumo">
            <div class="resumo-acao">{{ casasResumoAcao }}</div>
            <div class="resumo-valor" :class="casasNetCusto > 0 ? 'val-neg' : 'val-pos'">
              {{ casasNetCusto > 0 ? '-' : '+' }}{{ formatMoney(Math.abs(casasNetCusto)) }}
            </div>
          </div>

          <p v-if="casasErro" class="erro-msg">{{ casasErro }}</p>

          <button
            class="btn btn-purple"
            :disabled="casasTarget === null || casasTarget === casasAtual"
            @click="confirmarCasas"
          >
            Confirmar casas
          </button>
        </div>

        <!-- Ações -->
        <div class="detalhe-actions">
          <button
            v-if="!detalhePosse.hipotecada"
            class="btn btn-amber"
            @click="hipotecar(detalhePosse)"
          >
            Hipotecar · receber {{ formatMoney(detalhePosse.propriedade.valor_hipoteca) }}
          </button>
          <button
            v-if="detalhePosse.hipotecada"
            class="btn btn-green"
            @click="recuperar(detalhePosse)"
          >
            Recuperar hipoteca · pagar {{ formatMoney(Math.round(detalhePosse.propriedade.valor_hipoteca * 1.2)) }}
          </button>
          <button class="btn btn-ghost-outline" @click="iniciarLeilao(detalhePosse)">
            Iniciar leilão
          </button>
          <button
            v-if="!detalhePosse.hipotecada && detalhePosse.num_casas === 0 && !detalhePosse.tem_hotel"
            class="btn btn-ghost-outline btn-danger-outline"
            @click="venderBanco(detalhePosse)"
          >
            Vender ao banco · {{ formatMoney(detalhePosse.propriedade.valor_hipoteca) }}
          </button>
          <button
            v-if="!detalhePosse.hipotecada && (detalhePosse.num_casas > 0 || detalhePosse.tem_hotel)"
            class="btn btn-ghost-outline btn-danger-outline"
            disabled
            title="Venda todas as casas/hotel antes de vender ao banco"
          >
            Vender ao banco (venda casas antes)
          </button>
        </div>
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
const detalhePosse = ref(null)

const minhas = computed(() => partida.posses.filter(p => p.jogador_id === jogador.id))
const disponiveis = computed(() => partida.posses.filter(p => !p.jogador_id))

function formatMoney(val) {
  if (!val && val !== 0) return 'R$ 0'
  return `R$ ${(val / 100).toLocaleString('pt-BR', { minimumFractionDigits: 0 })}`
}

function formatMoneyShort(val) {
  if (!val && val !== 0) return ''
  const r = val / 100
  if (r >= 1000) return `${(r / 1000).toFixed(r % 1000 === 0 ? 0 : 1)}k`
  return `${r}`
}

// ── Detalhe modal ────────────────────────────────────────────────────────────

function abrirDetalhe(posse) {
  detalhePosse.value = posse
  casasTarget.value = null
  casasErro.value = ''
}

function fecharDetalhe() {
  detalhePosse.value = null
  casasTarget.value = null
  casasErro.value = ''
}

const tabelaAlugueis = computed(() => {
  if (!detalhePosse.value) return []
  const p = detalhePosse.value
  const prop = p.propriedade
  const casasAtualVal = p.tem_hotel ? 5 : p.num_casas
  return [
    { label: 'Sem casas', valor: prop.aluguel_sem_casa,  ativo: casasAtualVal === 0 },
    { label: '1 casa',    valor: prop.aluguel_1_casa,    ativo: casasAtualVal === 1 },
    { label: '2 casas',   valor: prop.aluguel_2_casas,   ativo: casasAtualVal === 2 },
    { label: '3 casas',   valor: prop.aluguel_3_casas,   ativo: casasAtualVal === 3 },
    { label: '4 casas',   valor: prop.aluguel_4_casas,   ativo: casasAtualVal === 4 },
    { label: 'Hotel',     valor: prop.aluguel_hotel,     ativo: casasAtualVal === 5 },
  ].filter(l => l.valor != null)
})

// ── Stepper de casas ─────────────────────────────────────────────────────────

const casasTarget = ref(null)
const casasErro = ref('')

const casasAtual = computed(() => {
  if (!detalhePosse.value) return 0
  return detalhePosse.value.tem_hotel ? 5 : detalhePosse.value.num_casas
})

const casasOpcoes = computed(() => {
  if (!detalhePosse.value) return []
  const p = detalhePosse.value.propriedade
  const atual = casasAtual.value
  const sala = partida.sala
  return [
    { valor: 0, label: '0', aluguel: p.aluguel_sem_casa,  disponivel: atual !== 0 },
    { valor: 1, label: '1', aluguel: p.aluguel_1_casa,    disponivel: atual !== 1 && (atual > 1 || (sala?.casas_disponiveis ?? 0) >= 1) },
    { valor: 2, label: '2', aluguel: p.aluguel_2_casas,   disponivel: atual !== 2 && (atual > 2 || (sala?.casas_disponiveis ?? 0) >= (2 - atual)) },
    { valor: 3, label: '3', aluguel: p.aluguel_3_casas,   disponivel: atual !== 3 && (atual > 3 || (sala?.casas_disponiveis ?? 0) >= (3 - atual)) },
    { valor: 4, label: '4', aluguel: p.aluguel_4_casas,   disponivel: atual !== 4 && atual !== 5 && (atual > 4 || (sala?.casas_disponiveis ?? 0) >= (4 - atual)) },
    { valor: 5, label: 'H',  aluguel: p.aluguel_hotel,    disponivel: atual === 4 || atual === 5 },
  ]
})

const casasNetCusto = computed(() => {
  const p = detalhePosse.value?.propriedade
  if (!p || casasTarget.value === null) return 0
  const atual = casasAtual.value
  const target = casasTarget.value
  if (atual === 4 && target === 5) return p.custo_hotel ?? p.custo_casa
  if (atual === 5 && target === 4) return -Math.floor((p.custo_hotel ?? p.custo_casa) / 2)
  if (target > atual) return (target - atual) * p.custo_casa
  return (target - atual) * Math.floor(p.custo_casa / 2)
})

const casasResumoAcao = computed(() => {
  const atual = casasAtual.value
  const target = casasTarget.value
  if (atual === 5 && target === 4) return 'Vender hotel → 4 casas'
  if (atual === 4 && target === 5) return 'Comprar hotel'
  if (target > atual) return `Comprar ${target - atual} casa(s) · de ${atual} → ${target}`
  return `Vender ${atual - target} casa(s) · de ${atual} → ${target}`
})

async function confirmarCasas() {
  casasErro.value = ''
  const atual = casasAtual.value
  const target = casasTarget.value
  const p = detalhePosse.value
  const prop = p.propriedade
  const custo = casasNetCusto.value

  try {
    if (target > atual || (atual === 4 && target === 5)) {
      await api.post('/transacoes', {
        sala_id: salaId.value,
        session_token: jogador.sessionToken,
        tipo: 'compra_casa',
        valor: Math.abs(custo),
        propriedade_id: p.propriedade_id,
        descricao: casasResumoAcao.value + ` em ${prop.nome}`,
      })
    } else {
      await api.post('/transacoes', {
        sala_id: salaId.value,
        session_token: jogador.sessionToken,
        tipo: 'venda_casa',
        valor: Math.abs(custo),
        propriedade_id: p.propriedade_id,
        descricao: casasResumoAcao.value + ` em ${prop.nome}`,
      })
    }
    casasTarget.value = null
    fecharDetalhe()
  } catch (e) {
    casasErro.value = e.message
  }
}

// ── Outras ações ─────────────────────────────────────────────────────────────

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
    fecharDetalhe()
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
    fecharDetalhe()
  } catch (e) { toast.add(e.message) }
}

async function iniciarLeilao(posse) {
  try {
    await api.post('/leiloes', {
      sala_id: salaId.value,
      session_token: jogador.sessionToken,
      propriedade_id: posse.propriedade_id,
    })
    fecharDetalhe()
  } catch (e) { toast.add(e.message) }
}

async function venderBanco(posse) {
  try {
    await api.post('/transacoes', {
      sala_id: salaId.value,
      session_token: jogador.sessionToken,
      tipo: 'venda_banco',
      valor: posse.propriedade.valor_hipoteca,
      propriedade_id: posse.propriedade_id,
      descricao: `${jogador.nome} vende ${posse.propriedade.nome} ao banco`,
    })
    fecharDetalhe()
  } catch (e) { toast.add(e.message) }
}

onMounted(async () => {
  if (!partida.posses.length) await partida.carregarPropriedades(salaId.value)
})
</script>

<style scoped>
.page { min-height: 100dvh; display: flex; flex-direction: column; align-items: center; padding: 0 20px calc(var(--nav-h) + 24px); }
.header { width: 100%; max-width: 360px; display: flex; align-items: center; justify-content: space-between; padding: 20px 0 16px; }
.brand { font-size: 20px; font-weight: 800; letter-spacing: -.5px; }
.brand span { color: var(--green); }
.wrap { width: 100%; max-width: 360px; display: flex; flex-direction: column; gap: 12px; }

.tabs { display: flex; gap: 4px; background: rgba(255,255,255,.04); border-radius: 12px; padding: 4px; }
.tab { flex: 1; padding: 8px; border: none; background: none; border-radius: 9px; font-size: 12px; font-weight: 700; font-family: 'Manrope', sans-serif; color: var(--text-2); cursor: pointer; transition: all .2s; }
.tab.active { background: rgba(46,204,113,.15); color: var(--green); }

.prop-list { display: flex; flex-direction: column; gap: 6px; }

.prop-card {
  display: flex; align-items: center; gap: 0;
  border-radius: 14px; overflow: hidden;
  cursor: pointer; transition: background .15s;
}
.prop-card:hover { background: rgba(255,255,255,.09); }

.prop-colorbar { width: 4px; align-self: stretch; flex-shrink: 0; }

.prop-body { flex: 1; padding: 12px 10px; min-width: 0; display: flex; flex-direction: column; gap: 4px; }
.prop-row { display: flex; align-items: center; gap: 6px; }
.prop-nome { font-size: 13px; font-weight: 700; flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.prop-info { display: flex; align-items: center; gap: 4px; }
.prop-meta { font-size: 11px; }
.mono { font-family: 'JetBrains Mono', monospace; }

.tag { font-size: 9px; font-weight: 700; border-radius: 4px; padding: 1px 6px; flex-shrink: 0; letter-spacing: .03em; }
.tag-danger { background: rgba(224,84,84,.1); color: var(--danger); }

.casa-dot { width: 8px; height: 8px; border-radius: 2px; background: var(--green); flex-shrink: 0; }
.hotel-dot {
  width: 18px; height: 18px; border-radius: 4px;
  background: rgba(224,84,84,.2); color: var(--danger);
  font-size: 10px; font-weight: 800;
  display: flex; align-items: center; justify-content: center;
}

.chevron { width: 16px; height: 16px; color: var(--text-2); opacity: .4; flex-shrink: 0; margin-right: 12px; }

.pill-btn { background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.1); border-radius: 8px; padding: 6px 12px; font-size: 11px; font-weight: 700; font-family: 'Manrope', sans-serif; color: var(--text-2); cursor: pointer; white-space: nowrap; transition: all .15s; margin-right: 10px; }
.pill-btn:hover { background: rgba(255,255,255,.1); }
.pill-ok { background: var(--green-dim); border-color: rgba(46,204,113,.2); color: var(--green); }

.empty { font-size: 13px; text-align: center; padding: 32px 0; }

/* ── Modal de detalhe ── */
.modal-overlay { position: fixed; inset: 0; z-index: 80; background: rgba(0,0,0,.6); backdrop-filter: blur(4px); display: flex; align-items: flex-end; justify-content: center; }
.modal-sheet {
  width: 100%; max-width: 480px;
  border-radius: 24px 24px 0 0;
  padding: 16px 20px 40px;
  display: flex; flex-direction: column; gap: 14px;
  max-height: 90dvh; overflow-y: auto;
}
.sheet-handle { width: 40px; height: 4px; background: rgba(255,255,255,.15); border-radius: 2px; align-self: center; margin-bottom: 4px; flex-shrink: 0; }

.detalhe-header { display: flex; align-items: center; gap: 10px; }
.detalhe-cor { width: 14px; height: 14px; border-radius: 4px; flex-shrink: 0; }
.detalhe-nome { font-size: 18px; font-weight: 800; flex: 1; }

.section-label { font-size: 10px; font-family: 'JetBrains Mono', monospace; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: var(--text-2); margin-bottom: 6px; }

.aluguel-table { display: flex; flex-direction: column; gap: 2px; }
.aluguel-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 7px 10px; border-radius: 8px;
  font-size: 12px;
  transition: background .1s;
}
.aluguel-row.row-ativo { background: var(--green-dim); }
.aluguel-row.row-ativo .row-label { color: var(--green); font-weight: 700; }
.aluguel-row.row-ativo .row-valor { color: var(--green); }
.row-label { color: var(--text-2); }
.row-valor { font-family: 'JetBrains Mono', monospace; font-weight: 700; }

.acao-info { display: flex; flex-direction: column; gap: 4px; }
.acao-multi { font-size: 14px; font-weight: 600; }

.casa-stepper { display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; margin-bottom: 10px; }
.casa-opt { display: flex; flex-direction: column; align-items: center; gap: 3px; padding: 10px 4px; background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.09); border-radius: 12px; cursor: pointer; font-family: 'Manrope', sans-serif; transition: all .15s; }
.opt-label { font-size: 16px; font-weight: 800; color: var(--text); }
.opt-aluguel { font-size: 9px; font-family: 'JetBrains Mono', monospace; color: var(--text-2); }
.casa-opt.opt-current { border-color: rgba(255,255,255,.25); background: rgba(255,255,255,.08); }
.casa-opt.opt-current .opt-label { color: var(--text-2); }
.casa-opt.opt-selected { border-color: rgba(156,39,176,.5); background: rgba(156,39,176,.12); }
.casa-opt.opt-selected .opt-label { color: #CE93D8; }
.casa-opt.opt-selected .opt-aluguel { color: #CE93D8; opacity: .8; }
.casa-opt.opt-disabled { opacity: .3; cursor: not-allowed; }

.casa-resumo { display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,.04); border: 1px solid rgba(255,255,255,.08); border-radius: var(--radius-sm); padding: 10px 12px; margin-bottom: 10px; }
.resumo-acao { font-size: 12px; font-weight: 600; }
.resumo-valor { font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 700; }
.val-pos { color: var(--green); }
.val-neg { color: var(--danger); }

.detalhe-actions { display: flex; flex-direction: column; gap: 8px; }

.btn-amber { background: rgba(246,173,85,.12); border: 1px solid rgba(246,173,85,.25); color: var(--amber); border-radius: 12px; padding: 12px 16px; font-size: 13px; font-weight: 700; font-family: 'Manrope', sans-serif; cursor: pointer; text-align: center; transition: all .15s; }
.btn-amber:hover { background: rgba(246,173,85,.2); }

.btn-purple { background: rgba(156,39,176,.12); border: 1px solid rgba(156,39,176,.25); color: #CE93D8; border-radius: 12px; padding: 12px 16px; font-size: 13px; font-weight: 700; font-family: 'Manrope', sans-serif; cursor: pointer; text-align: center; transition: all .15s; width: 100%; }
.btn-purple:disabled { opacity: .4; cursor: not-allowed; }
.btn-purple:not(:disabled):hover { background: rgba(156,39,176,.2); }

.btn-ghost-outline { background: transparent; border: 1px solid rgba(255,255,255,.15); color: var(--text-2); border-radius: 12px; padding: 12px 16px; font-size: 13px; font-weight: 700; font-family: 'Manrope', sans-serif; cursor: pointer; text-align: center; transition: all .15s; }
.btn-ghost-outline:hover { background: rgba(255,255,255,.06); color: var(--text); }

.btn-danger-outline { border-color: rgba(224,84,84,.25); color: var(--danger); }
.btn-danger-outline:not([disabled]):hover { background: rgba(224,84,84,.08); }
.btn-danger-outline:disabled { opacity: .35; cursor: not-allowed; }

.erro-msg { font-size: 12px; color: var(--danger); }
</style>
