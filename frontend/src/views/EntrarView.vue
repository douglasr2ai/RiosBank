<template>
  <div class="page">
    <div class="wrap">
      <!-- Back -->
      <button class="back-row" @click="$router.push({ name: 'landing' })">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
          <path d="M19 12H5M12 5l-7 7 7 7"/>
        </svg>
        Voltar
      </button>

      <!-- Marca -->
      <div class="brand-block">
        <div class="brand">Rios<span>Bank</span></div>
        <p class="tagline">Controle financeiro preciso para o seu tabuleiro.</p>
        <div v-if="jogadoresJogando !== null" class="salas-pill">
          <span class="pill-dot" />
          {{ jogadoresJogando === 0 ? 'Nenhum jogador ativo agora' : `${jogadoresJogando} jogador${jogadoresJogando === 1 ? '' : 'es'} jogando agora` }}
        </div>
      </div>

      <!-- Entrar via link de convite -->
      <div v-if="linkToken" class="glass card">
        <h2 class="card-title">Entrar via convite</h2>
        <p class="hint-link text-muted">Você foi convidado para uma partida. Escolha seu apelido para entrar.</p>

        <div class="field">
          <label>Como quer ser chamado?</label>
          <div class="input-wrap">
            <span class="input-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </span>
            <input v-model="nomeJogador" type="text" placeholder="Seu apelido" />
          </div>
        </div>

        <p v-if="erro" class="erro-msg">{{ erro }}</p>

        <button class="btn btn-green" :disabled="loading" @click="entrarPorLink">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="width:16px;height:16px">
            <path d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4M10 17l5-5-5-5M15 12H3"/>
          </svg>
          {{ loading ? 'Entrando...' : 'Entrar na partida' }}
        </button>
      </div>

      <!-- Entrar na sala (busca por nome + senha) -->
      <div v-else class="glass card">
        <h2 class="card-title">Entrar em uma sala</h2>

        <div class="field">
          <label>Código da sala</label>
          <div class="input-wrap">
            <span class="input-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
              </svg>
            </span>
            <input v-model="codigoSala" type="text" inputmode="numeric" maxlength="6" placeholder="000000" class="mono" />
          </div>
        </div>

        <div class="field">
          <label>Senha</label>
          <div class="input-wrap">
            <span class="input-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <rect x="3" y="11" width="18" height="11" rx="2"/>
                <path d="M7 11V7a5 5 0 0110 0v4"/>
              </svg>
            </span>
            <input v-model="senha" type="password" placeholder="••••••" />
          </div>
        </div>

        <div class="field">
          <label>Como quer ser chamado?</label>
          <div class="input-wrap">
            <span class="input-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </span>
            <input v-model="nomeJogador" type="text" placeholder="Seu apelido" />
          </div>
        </div>

        <p v-if="erro" class="erro-msg">{{ erro }}</p>

        <button class="btn btn-green" :disabled="loading" @click="entrar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="width:16px;height:16px">
            <path d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4M10 17l5-5-5-5M15 12H3"/>
          </svg>
          {{ loading ? 'Entrando...' : 'Entrar na sala' }}
        </button>
      </div>

      <!-- Criar sala -->
      <button v-if="!linkToken" class="btn btn-ghost" @click="$router.push({ name: 'criar-sala' })">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="width:16px;height:16px">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/>
        </svg>
        Criar nova sala
      </button>

      <!-- Navbar inferior -->
      <div v-if="!linkToken" class="bottom-links">
        <button class="link-btn" @click="$router.push({ name: 'historico-busca' })">Histórico</button>
        <div class="divider-v" />
        <button class="link-btn" @click="$router.push({ name: 'landing' })">Início</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { api } from '../stores/api'
import { useJogadorStore } from '../stores/jogadorStore'
import { usePartidaStore } from '../stores/partidaStore'
import { useWsStore } from '../stores/wsStore'

const router = useRouter()
const route = useRoute()
const jogador = useJogadorStore()
const partida = usePartidaStore()
const ws = useWsStore()

const codigoSala = ref('')
const senha = ref('')
const nomeJogador = ref('')
const loading = ref(false)
const erro = ref('')
const jogadoresJogando = ref(null)

const linkToken = computed(() =>
  route.name === 'join' ? route.params.linkToken : null
)

onMounted(async () => {
  if (linkToken.value && jogador.nome) nomeJogador.value = jogador.nome
  try {
    const data = await api.get('/salas/stats')
    jogadoresJogando.value = data.jogadores_jogando
  } catch {}
})

async function entrarPorLink() {
  if (!nomeJogador.value.trim()) {
    erro.value = 'Preencha o seu apelido.'
    return
  }
  erro.value = ''
  loading.value = true
  try {
    const data = await api.post(`/salas/join/${linkToken.value}`, {
      link_token: linkToken.value,
      nome_jogador: nomeJogador.value.trim(),
    })
    await entrarNaSala(data)
  } catch (e) {
    erro.value = e.message
  } finally {
    loading.value = false
  }
}

async function entrar() {
  if (!codigoSala.value.trim() || !nomeJogador.value.trim()) {
    erro.value = 'Preencha o código da sala e o seu apelido.'
    return
  }
  erro.value = ''
  loading.value = true
  try {
    const data = await api.post('/salas/entrar', {
      codigo: codigoSala.value.trim(),
      senha: senha.value,
      nome_jogador: nomeJogador.value.trim(),
    })
    await entrarNaSala(data)
  } catch (e) {
    erro.value = e.message
  } finally {
    loading.value = false
  }
}

async function entrarNaSala(data) {
  jogador.setJogador(data.jogador)
  partida.setSala(data.sala)
  ws.connect(data.sala.id, data.jogador.session_token)
  await Promise.all([
    partida.carregarPropriedades(data.sala.id),
    partida.carregarTransacoes(data.sala.id),
  ])
  const status = data.sala.status
  if (status === 'lobby') {
    router.push({ name: 'lobby', params: { salaId: data.sala.id } })
  } else {
    router.push({ name: 'dashboard', params: { salaId: data.sala.id } })
  }
}
</script>

<style scoped>
.page {
  min-height: 100dvh;
  display: flex; align-items: center; justify-content: center;
  padding: 32px 20px 48px;
  position: relative;
}

.wrap {
  width: 100%; max-width: 360px;
  display: flex; flex-direction: column; gap: 16px;
  position: relative; z-index: 1;
}

.back-row {
  display: flex; align-items: center; gap: 8px;
  background: none; border: none; cursor: pointer;
  font-size: 13px; font-weight: 600; color: var(--text-2);
  font-family: 'Manrope', sans-serif; padding: 0;
  transition: color .2s; align-self: flex-start;
}
.back-row:hover { color: var(--text); }
.back-row svg { width: 16px; height: 16px; }

.brand-block { text-align: center; padding: 4px 0; }
.brand { font-size: 32px; font-weight: 800; letter-spacing: -1px; }
.brand span { color: var(--green); }
.tagline { font-size: 13px; color: var(--text-2); margin-top: 5px; }

.salas-pill {
  display: inline-flex; align-items: center; gap: 6px;
  margin-top: 10px;
  font-size: 11px; font-weight: 700;
  font-family: 'JetBrains Mono', monospace; letter-spacing: .04em;
  color: var(--green);
  background: var(--green-dim); border: 1px solid rgba(46,204,113,.2);
  border-radius: 999px; padding: 4px 12px;
}
.pill-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 6px var(--green);
  animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: .4; }
}

.card { padding: 22px; display: flex; flex-direction: column; gap: 12px; }
.card-title { font-size: 16px; font-weight: 700; }
.hint-link { font-size: 12px; line-height: 1.5; }
.erro-msg { font-size: 12px; color: var(--danger); }

.bottom-links {
  display: flex; align-items: center; justify-content: center;
  padding-top: 4px;
}
.link-btn {
  background: none; border: none; cursor: pointer;
  font-size: 13px; font-weight: 600; color: var(--text-2);
  font-family: 'Manrope', sans-serif; padding: 6px 16px;
  transition: color .2s;
}
.link-btn:hover { color: var(--text); }
.divider-v { width: 1px; height: 14px; background: rgba(255,255,255,.1); }
</style>
