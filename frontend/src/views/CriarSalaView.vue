<template>
  <div class="page">
    <div class="wrap">
      <div class="top-row">
        <button class="back-btn" @click="$router.back()">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
            <path d="M19 12H5M12 5l-7 7 7 7"/>
          </svg>
        </button>
        <div class="brand">Rios<span>Bank</span></div>
      </div>

      <div class="heading">
        <h2>Criar sala</h2>
        <p>Configure sua partida e compartilhe o link com os jogadores.</p>
      </div>

      <div class="glass card">
        <div class="field">
          <label>Nome da sala</label>
          <div class="input-wrap">
            <span class="input-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
              </svg>
            </span>
            <input v-model="form.nome" type="text" placeholder="Ex: Sala da Família" />
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
            <input v-model="form.senha" type="password" placeholder="Crie uma senha" />
          </div>
        </div>

        <div class="field">
          <label>Versão do jogo</label>
          <div class="input-wrap">
            <span class="input-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
              </svg>
            </span>
            <select v-model="form.versao_jogo" style="padding-left: 40px">
              <option value="super_banco_imobiliario">Super Banco Imobiliário · R$25.000</option>
            </select>
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
            <input v-model="form.nome_jogador" type="text" placeholder="Seu apelido" />
          </div>
        </div>

        <p v-if="erro" class="erro-msg">{{ erro }}</p>

        <button class="btn btn-green" :disabled="loading" @click="criar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="width:16px;height:16px">
            <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/>
          </svg>
          {{ loading ? 'Criando...' : 'Criar sala' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../stores/api'
import { useJogadorStore } from '../stores/jogadorStore'
import { usePartidaStore } from '../stores/partidaStore'
import { useWsStore } from '../stores/wsStore'

const router = useRouter()
const jogador = useJogadorStore()
const partida = usePartidaStore()
const ws = useWsStore()

const form = ref({
  nome: '',
  senha: '',
  versao_jogo: 'super_banco_imobiliario',
  nome_jogador: '',
})
const loading = ref(false)
const erro = ref('')

async function criar() {
  if (!form.value.nome.trim() || !form.value.senha || !form.value.nome_jogador.trim()) {
    erro.value = 'Preencha todos os campos.'
    return
  }
  erro.value = ''
  loading.value = true
  try {
    const data = await api.post('/salas', form.value)
    jogador.setJogador(data.jogador)
    partida.setSala(data.sala)
    ws.connect(data.sala.id, data.jogador.session_token)
    router.push({ name: 'lobby', params: { salaId: data.sala.id } })
  } catch (e) {
    erro.value = e.message
  } finally {
    loading.value = false
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
  display: flex; flex-direction: column; gap: 24px;
  position: relative; z-index: 1;
}

.top-row { display: flex; align-items: center; gap: 12px; }

.back-btn {
  width: 38px; height: 38px;
  display: flex; align-items: center; justify-content: center;
  background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.09);
  border-radius: 12px; cursor: pointer; color: var(--text-2); transition: all .2s;
}
.back-btn:hover { background: rgba(255,255,255,.09); color: var(--text); }
.back-btn svg { width: 18px; height: 18px; }

.brand { font-size: 22px; font-weight: 800; letter-spacing: -.5px; }
.brand span { color: var(--green); }

.heading h2 { font-size: 26px; font-weight: 800; letter-spacing: -.6px; }
.heading p { font-size: 13px; color: var(--text-2); margin-top: 5px; }

.card { padding: 22px; display: flex; flex-direction: column; gap: 12px; }
.erro-msg { font-size: 12px; color: var(--danger); }
</style>
