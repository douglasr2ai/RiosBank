<template>
  <Teleport to="body">
    <div v-if="visivel" class="overlay" @click.self="fechar">
      <div class="sheet glass">
        <div class="handle" />

        <!-- Aviso de insolvência (1º ou 2º) -->
        <template v-if="aviso && !liquidacao">
          <div class="icon-wrap" :class="aviso.num === 2 ? 'icon-danger' : 'icon-amber'">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/>
            </svg>
          </div>

          <div v-if="ehDevedor" class="content">
            <h3 class="titulo">Saldo insuficiente</h3>
            <p class="subtitulo">
              Você não tem saldo para pagar <strong>{{ formatMoney(aviso.valor) }}</strong>
              a <strong>{{ aviso.credor_nome }}</strong>.
            </p>
            <div class="aviso-pill" :class="aviso.num === 2 ? 'pill-danger' : 'pill-amber'">
              Aviso {{ aviso.num }}/3 — {{ aviso.num === 2 ? 'próxima cobrança liquida seus bens' : 'negocie suas propriedades' }}
            </div>
            <p class="dica">
              Hipoteque ou leiloe seus imóveis para levantar fundos.
              {{ aviso.num === 2 ? 'Na 3ª cobrança, seus bens serão liquidados automaticamente.' : '' }}
            </p>
          </div>

          <div v-else-if="ehCreador" class="content">
            <h3 class="titulo">Devedor sem saldo</h3>
            <p class="subtitulo">
              <strong>{{ aviso.nome }}</strong> recebeu o aviso {{ aviso.num }}/3.
              A cobrança não foi aplicada.
            </p>
            <div class="aviso-pill" :class="aviso.num === 2 ? 'pill-danger' : 'pill-amber'">
              {{ aviso.num === 2 ? 'Próxima cobrança liquida os bens automaticamente' : 'Aguarde e cobre novamente quando quiser' }}
            </div>
          </div>

          <div v-else class="content">
            <h3 class="titulo">Aviso de insolvência</h3>
            <p class="subtitulo">
              <strong>{{ aviso.nome }}</strong> não tem saldo para pagar <strong>{{ formatMoney(aviso.valor) }}</strong>.
              Aviso {{ aviso.num }}/3.
            </p>
          </div>

          <div class="actions">
            <button v-if="ehDevedor" class="btn btn-green" @click="verPropriedades">
              Ver minhas propriedades
            </button>
            <button class="btn btn-ghost" @click="fechar">Fechar</button>
          </div>
        </template>

        <!-- Resultado de liquidação forçada -->
        <template v-else-if="liquidacao">
          <div class="icon-wrap" :class="liquidacao.falido ? 'icon-danger' : 'icon-amber'">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
          </div>

          <div class="content">
            <h3 class="titulo">{{ liquidacao.falido ? 'Falência declarada' : 'Liquidação forçada' }}</h3>
            <p class="subtitulo">
              Bens de <strong>{{ liquidacao.nome }}</strong> foram liquidados para cobrir a dívida.
            </p>

            <div v-if="liquidacao.propriedades_liquidadas?.length" class="liq-list">
              <div v-for="(p, i) in liquidacao.propriedades_liquidadas" :key="i" class="liq-item">
                <span class="liq-nome">{{ p.nome }}</span>
                <span class="liq-detalhe">
                  <template v-if="p.hipotecada">transferida → {{ p.transferida_para }}</template>
                  <template v-else>
                    {{ p.hotel_vendido ? 'hotel + ' : '' }}{{ p.casas_vendidas > 0 ? p.casas_vendidas + ' casas + ' : '' }}imóvel
                  </template>
                </span>
                <span class="liq-val">{{ formatMoney(p.valor_abatido) }}</span>
              </div>
            </div>

            <div class="saldo-final" :class="liquidacao.falido ? 'saldo-zero' : 'saldo-ok'">
              Saldo final: <strong>{{ formatMoney(liquidacao.saldo_final) }}</strong>
              {{ liquidacao.falido ? '— Falido' : '' }}
            </div>
          </div>

          <div class="actions">
            <button class="btn btn-ghost" @click="fechar">Fechar</button>
          </div>
        </template>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usePartidaStore } from '../stores/partidaStore'
import { useJogadorStore } from '../stores/jogadorStore'

const router = useRouter()
const route = useRoute()
const partida = usePartidaStore()
const jogador = useJogadorStore()

const aviso = computed(() => partida.insolvenciaAviso)
const liquidacao = computed(() => partida.liquidacaoInfo)
const visivel = computed(() => !!(aviso.value || liquidacao.value))

const ehDevedor = computed(() => aviso.value?.jogador_id === jogador.id)
const ehCreador = computed(() => aviso.value?.credor_id === jogador.id)

function formatMoney(val) {
  if (!val && val !== 0) return 'R$ 0'
  return `R$ ${(val / 100).toLocaleString('pt-BR', { minimumFractionDigits: 0 })}`
}

function fechar() {
  partida.clearInsolvencia()
}

function verPropriedades() {
  partida.clearInsolvencia()
  const salaId = route.params.salaId
  router.push({ name: 'propriedades', params: { salaId } })
}
</script>

<style scoped>
.overlay {
  position: fixed; inset: 0; z-index: 200;
  background: rgba(0,0,0,.65); backdrop-filter: blur(4px);
  display: flex; align-items: flex-end; justify-content: center;
}

.sheet {
  width: 100%; max-width: 480px;
  border-radius: 24px 24px 0 0;
  padding: 16px 20px 40px;
  display: flex; flex-direction: column; gap: 16px;
}

.handle {
  width: 40px; height: 4px;
  background: rgba(255,255,255,.15); border-radius: 2px;
  align-self: center; margin-bottom: 4px;
}

.icon-wrap {
  width: 52px; height: 52px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  align-self: center;
}
.icon-wrap svg { width: 24px; height: 24px; }
.icon-amber { background: rgba(246,173,85,.15); color: var(--amber); }
.icon-danger { background: rgba(224,84,84,.15); color: var(--danger); }

.content { display: flex; flex-direction: column; gap: 10px; }

.titulo { font-size: 19px; font-weight: 800; }
.subtitulo { font-size: 14px; color: var(--text-2); line-height: 1.5; }
.subtitulo strong { color: var(--text); }

.aviso-pill {
  display: inline-flex; align-self: flex-start;
  border-radius: 999px; padding: 5px 12px;
  font-size: 11px; font-weight: 700;
  font-family: 'JetBrains Mono', monospace; letter-spacing: .03em;
}
.pill-amber { background: rgba(246,173,85,.12); color: var(--amber); border: 1px solid rgba(246,173,85,.25); }
.pill-danger { background: rgba(224,84,84,.12); color: var(--danger); border: 1px solid rgba(224,84,84,.25); }

.dica { font-size: 12px; color: var(--text-2); line-height: 1.55; }

.liq-list {
  display: flex; flex-direction: column; gap: 6px;
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.08);
  border-radius: 12px; padding: 10px 12px;
}
.liq-item { display: flex; align-items: center; gap: 8px; font-size: 12px; }
.liq-nome { font-weight: 700; flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.liq-detalhe { color: var(--text-2); font-size: 11px; flex-shrink: 0; }
.liq-val { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--amber); flex-shrink: 0; }

.saldo-final {
  font-size: 13px; font-weight: 600;
  padding: 10px 12px; border-radius: 10px;
}
.saldo-zero { background: rgba(224,84,84,.08); color: var(--danger); border: 1px solid rgba(224,84,84,.15); }
.saldo-ok { background: var(--green-dim); color: var(--green); border: 1px solid rgba(46,204,113,.2); }

.actions { display: flex; flex-direction: column; gap: 8px; }
</style>
