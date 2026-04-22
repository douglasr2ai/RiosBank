import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from './api'

export const useJogadorStore = defineStore('jogador', () => {
  const id = ref(localStorage.getItem('rb_jogador_id') || null)
  const nome = ref(localStorage.getItem('rb_jogador_nome') || null)
  const sessionToken = ref(localStorage.getItem('rb_session_token') || null)
  const saldo = ref(0)
  const status = ref('ativo')
  const ordemEntrada = ref(0)

  const isFalido = computed(() => status.value === 'falido')

  function setJogador(data) {
    id.value = data.id
    nome.value = data.nome
    sessionToken.value = data.session_token
    saldo.value = data.saldo
    status.value = data.status
    ordemEntrada.value = data.ordem_entrada
    localStorage.setItem('rb_jogador_id', data.id)
    localStorage.setItem('rb_jogador_nome', data.nome)
    localStorage.setItem('rb_session_token', data.session_token)
  }

  function updateSaldo(novoSaldo) {
    saldo.value = novoSaldo
  }

  function updateStatus(novoStatus) {
    status.value = novoStatus
  }

  function clear() {
    id.value = null
    nome.value = null
    sessionToken.value = null
    saldo.value = 0
    status.value = 'ativo'
    ordemEntrada.value = 0
    localStorage.removeItem('rb_jogador_id')
    localStorage.removeItem('rb_jogador_nome')
    localStorage.removeItem('rb_session_token')
  }

  async function reconnect() {
    if (!sessionToken.value) return false
    try {
      const data = await api.post('/jogadores/reconnect', { session_token: sessionToken.value })
      setJogador(data.jogador)
      return data
    } catch {
      clear()
      return false
    }
  }

  return {
    id, nome, sessionToken, saldo, status, ordemEntrada,
    isFalido,
    setJogador, updateSaldo, updateStatus, clear, reconnect,
  }
})
