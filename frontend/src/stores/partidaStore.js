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
  const insolvenciaAviso = ref(null)
  const liquidacaoInfo = ref(null)

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

  function upsertJogador(dados) {
    const idx = jogadores.value.findIndex(j => j.id === dados.jogador_id)
    const entrada = {
      id: dados.jogador_id,
      nome: dados.nome,
      saldo: dados.saldo,
      status: dados.status,
      ordem_entrada: dados.ordem_entrada,
      online: dados.online,
    }
    if (idx >= 0) {
      jogadores.value[idx] = { ...jogadores.value[idx], ...entrada }
    } else {
      jogadores.value.push(entrada)
      jogadores.value.sort((a, b) => a.ordem_entrada - b.ordem_entrada)
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

  function marcarNegociacaoAceita(transacaoId) {
    if (aprovacaoPendente.value?.transacao_id === transacaoId) {
      aprovacaoPendente.value = { ...aprovacaoPendente.value, destinatario_aceitou: true }
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

  function setInsolvenciaAviso(dados) {
    insolvenciaAviso.value = dados
    liquidacaoInfo.value = null
  }

  function setLiquidacaoInfo(dados) {
    liquidacaoInfo.value = dados
    insolvenciaAviso.value = null
  }

  function clearInsolvencia() {
    insolvenciaAviso.value = null
    liquidacaoInfo.value = null
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
    insolvenciaAviso.value = null
    liquidacaoInfo.value = null
  }

  return {
    sala, jogadores, posses, transacoes, aprovacaoPendente, leilaoAtivo,
    insolvenciaAviso, liquidacaoInfo,
    jogadoresAtivos, possesDe, propriedadesDisponiveis,
    setSala, addTransacao, updateJogador, upsertJogador, setAprovacaoPendente, registrarVoto, marcarNegociacaoAceita, clearAprovacao,
    setLeilaoAtivo, clearLeilao, updatePosse,
    setInsolvenciaAviso, setLiquidacaoInfo, clearInsolvencia,
    carregarSala, carregarPropriedades, carregarTransacoes, clear,
  }
})
