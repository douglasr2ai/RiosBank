import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from './api'

export const usePartidaStore = defineStore('partida', () => {
  const sala = ref(null)
  const jogadores = ref([])
  const posses = ref([])
  const transacoes = ref([])
  const aprovacaoPendente = ref(null)
  const leilaoAtivo = ref(null)

  const jogadoresAtivos = computed(() =>
    jogadores.value.filter(j => j.status === 'ativo')
  )

  const possesDe = (jogadorId) => posses.value.filter(p => p.jogador_id === jogadorId)

  const propriedadesDisponiveis = computed(() =>
    posses.value.filter(p => !p.jogador_id)
  )

  function setSala(data) {
    sala.value = data
    if (data.jogadores) {
      jogadores.value = data.jogadores
    }
  }

  function addTransacao(t) {
    const idx = transacoes.value.findIndex(x => x.id === t.id)
    if (idx >= 0) {
      transacoes.value[idx] = t
    } else {
      transacoes.value.unshift(t)
    }
  }

  function updateJogador(jogadorId, updates) {
    const idx = jogadores.value.findIndex(j => j.id === jogadorId)
    if (idx >= 0) {
      jogadores.value[idx] = { ...jogadores.value[idx], ...updates }
    }
  }

  function setAprovacaoPendente(dados) {
    aprovacaoPendente.value = { ...dados, votos: {} }
  }

  function registrarVoto(jogadorId, voto) {
    if (aprovacaoPendente.value) {
      aprovacaoPendente.value = {
        ...aprovacaoPendente.value,
        votos: { ...aprovacaoPendente.value.votos, [jogadorId]: voto },
      }
    }
  }

  function clearAprovacao() {
    aprovacaoPendente.value = null
  }

  function setLeilaoAtivo(dados) {
    leilaoAtivo.value = dados
  }

  function clearLeilao() {
    leilaoAtivo.value = null
  }

  function updatePosse(posseId, updates) {
    const idx = posses.value.findIndex(p => p.id === posseId)
    if (idx >= 0) {
      posses.value[idx] = { ...posses.value[idx], ...updates }
    }
  }

  async function carregarSala(salaId) {
    const data = await api.get(`/salas/${salaId}`)
    setSala(data)
    return data
  }

  async function carregarPropriedades(salaId) {
    const data = await api.get(`/salas/${salaId}/propriedades`)
    posses.value = data
  }

  async function carregarTransacoes(salaId) {
    const data = await api.get(`/transacoes/sala/${salaId}`)
    transacoes.value = data
  }

  function clear() {
    sala.value = null
    jogadores.value = []
    posses.value = []
    transacoes.value = []
    aprovacaoPendente.value = null
    leilaoAtivo.value = null
  }

  return {
    sala, jogadores, posses, transacoes, aprovacaoPendente, leilaoAtivo,
    jogadoresAtivos, possesDe, propriedadesDisponiveis,
    setSala, addTransacao, updateJogador, setAprovacaoPendente, registrarVoto, clearAprovacao,
    setLeilaoAtivo, clearLeilao, updatePosse,
    carregarSala, carregarPropriedades, carregarTransacoes, clear,
  }
})
