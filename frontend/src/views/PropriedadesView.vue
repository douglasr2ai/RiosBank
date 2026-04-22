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
                {{ !p.num_casas && !p.tem_hotel ? 'sem benfeitorias' : '' }}
              </span>
              <span v-else>Ação · dado × {{ formatMoney(p.propriedade.multiplicador_dado) }}</span>
              <span v-if="p.hipotecada" class="hipotecada-tag">hipotecada</span>
            </p>
          </div>
          <div class="prop-actions">
            <button v-if="!p.hipotecada && p.propriedade.tipo === 'rua'" class="pill-btn" @click="comprarCasa(p)">
              +casa
            </button>
            <button v-if="!p.hipotecada && (p.num_casas > 0 || p.tem_hotel)" class="pill-btn" @click="venderCasa(p)">
              -casa
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

async function comprarCasa(posse) {
  try {
    await api.post('/transacoes', {
      sala_id: salaId.value,
      session_token: jogador.sessionToken,
      tipo: 'compra_casa',
      valor: posse.propriedade.custo_casa,
      propriedade_id: posse.propriedade_id,
      descricao: `${jogador.nome} quer comprar casa em ${posse.propriedade.nome}`,
    })
  } catch (e) { toast.add(e.message) }
}

async function venderCasa(posse) {
  const valor = posse.tem_hotel
    ? Math.floor(posse.propriedade.custo_hotel / 2)
    : Math.floor(posse.propriedade.custo_casa / 2)
  try {
    await api.post('/transacoes', {
      sala_id: salaId.value,
      session_token: jogador.sessionToken,
      tipo: 'venda_casa',
      valor,
      propriedade_id: posse.propriedade_id,
      descricao: `${jogador.nome} quer vender casa/hotel em ${posse.propriedade.nome}`,
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
.pill-ok { background: var(--green-dim); border-color: rgba(46,204,113,.2); color: var(--green); }
.pill-warn { background: rgba(246,173,85,.1); border-color: rgba(246,173,85,.2); color: var(--amber); }

.empty { font-size: 13px; text-align: center; padding: 32px 0; }
</style>
