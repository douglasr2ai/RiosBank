<template>
  <div class="page">
    <div class="wrap">
      <div class="top-row">
        <button class="back-btn" @click="$router.push({ name: 'landing' })">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
            <path d="M19 12H5M12 5l-7 7 7 7"/>
          </svg>
        </button>
        <div class="brand">Rios<span>Bank</span></div>
      </div>

      <div class="heading">
        <h2>Histórico de partidas</h2>
        <p>Digite o código e a senha da sala para acessar o resumo.</p>
      </div>

      <div class="glass card">
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

        <p v-if="erro" class="erro-msg">{{ erro }}</p>

        <button class="btn btn-green" :disabled="loading" @click="buscar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="width:16px;height:16px">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          {{ loading ? 'Buscando...' : 'Buscar partida' }}
        </button>
      </div>

      <div class="hint">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="width:14px;height:14px;opacity:.5">
          <circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/>
        </svg>
        Apenas quem conhece o código e a senha da sala pode acessar o histórico.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../stores/api'

const router = useRouter()
const codigoSala = ref('')
const senha = ref('')
const loading = ref(false)
const erro = ref('')

async function buscar() {
  if (!codigoSala.value.trim() || !senha.value) {
    erro.value = 'Preencha o código da sala e a senha.'
    return
  }
  erro.value = ''
  loading.value = true
  try {
    const data = await api.post('/historico/busca', {
      codigo: codigoSala.value.trim(),
      senha: senha.value,
    })
    router.push({ name: 'historico-resumo', params: { linkToken: data.link_token } })
  } catch (e) {
    erro.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page { min-height: 100dvh; display: flex; align-items: center; justify-content: center; padding: 32px 20px 48px; position: relative; }
.wrap { width: 100%; max-width: 360px; display: flex; flex-direction: column; gap: 24px; position: relative; z-index: 1; }
.top-row { display: flex; align-items: center; gap: 12px; }
.back-btn { width: 38px; height: 38px; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.09); border-radius: 12px; cursor: pointer; color: var(--text-2); transition: all .2s; }
.back-btn:hover { background: rgba(255,255,255,.09); color: var(--text); }
.back-btn svg { width: 18px; height: 18px; }
.brand { font-size: 22px; font-weight: 800; letter-spacing: -.5px; }
.brand span { color: var(--green); }
.heading h2 { font-size: 26px; font-weight: 800; letter-spacing: -.6px; }
.heading p { font-size: 13px; color: var(--text-2); margin-top: 5px; }
.card { padding: 22px; display: flex; flex-direction: column; gap: 12px; }
.erro-msg { font-size: 12px; color: var(--danger); }
.hint { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--text-2); line-height: 1.5; }
</style>
