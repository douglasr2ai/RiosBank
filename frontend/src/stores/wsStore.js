import { defineStore } from 'pinia'
import { ref } from 'vue'
import { usePartidaStore } from './partidaStore'
import { useJogadorStore } from './jogadorStore'
import router from '../router'

const WS_BASE = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

export const useWsStore = defineStore('ws', () => {
  const connected = ref(false)
  let ws = null
  let pingInterval = null
  let salaId = null

  function connect(sala_id, session_token) {
    salaId = sala_id
    if (ws) ws.close()

    ws = new WebSocket(`${WS_BASE}/ws/${sala_id}/${session_token}`)

    ws.onopen = () => {
      connected.value = true
      pingInterval = setInterval(() => {
        if (ws?.readyState === WebSocket.OPEN) ws.send('ping')
      }, 25_000)
    }

    ws.onclose = (e) => {
      connected.value = false
      clearInterval(pingInterval)
      if (e.code === 4001) {
        // Expulso
        useJogadorStore().clear()
        router.push({ name: 'entrar' })
        return
      }
      if (e.code === 4002) {
        // Partida encerrada
        return
      }
      // Reconnect automático
      setTimeout(() => {
        const jogador = useJogadorStore()
        if (jogador.sessionToken) connect(sala_id, jogador.sessionToken)
      }, 3_000)
    }

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data)
        handleMessage(msg).catch(console.error)
      } catch {}
    }
  }

  function disconnect() {
    clearInterval(pingInterval)
    ws?.close()
    ws = null
    connected.value = false
  }

  async function handleMessage(msg) {
    const partida = usePartidaStore()
    const jogador = useJogadorStore()

    switch (msg.tipo) {
      case 'jogador_conectado':
        partida.upsertJogador(msg.dados)
        break

      case 'jogador_desconectado':
        partida.updateJogador(msg.dados.jogador_id, { online: msg.dados.online })
        break

      case 'partida_iniciada':
        partida.setSala(msg.dados)
        router.push({ name: 'dashboard', params: { salaId: msg.dados.id } })
        break

      case 'host_alterado':
        if (partida.sala) partida.sala.host_jogador_id = msg.dados.novo_host_id
        break

      case 'jogador_expulso':
        if (msg.dados.jogador_id === jogador.id) {
          jogador.clear()
          partida.clear()
          disconnect()
          router.push({ name: 'entrar' })
        } else {
          partida.updateJogador(msg.dados.jogador_id, { status: 'expulso' })
        }
        break

      case 'aprovacao_solicitada':
        partida.setAprovacaoPendente(msg.dados)
        break

      case 'transacao_voto_registrado':
        partida.registrarVoto(msg.dados.jogador_id, msg.dados.voto)
        break

      case 'transacao_aprovada':
      case 'transacao_reprovada':
      case 'transacao_estornada': {
        partida.clearAprovacao()
        if (salaId) {
          await partida.carregarSala(salaId)
          await Promise.all([
            partida.carregarPropriedades(salaId),
            partida.carregarTransacoes(salaId),
          ])
          const meuJogador = partida.jogadores.find(j => j.id === jogador.id)
          if (meuJogador) jogador.updateSaldo(meuJogador.saldo)
        }
        break
      }

      case 'jogador_falido':
        partida.updateJogador(msg.dados.jogador_id, { status: 'falido' })
        break

      case 'leilao_iniciado':
        partida.setLeilaoAtivo(msg.dados)
        break

      case 'lance_registrado':
        if (partida.leilaoAtivo) {
          partida.leilaoAtivo.lance_atual = msg.dados.lance_atual
          partida.leilaoAtivo.lider_id = msg.dados.lider_id
          partida.leilaoAtivo.lider_nome = msg.dados.lider_nome
        }
        break

      case 'leilao_encerrado':
        partida.clearLeilao()
        if (salaId) {
          await partida.carregarSala(salaId)
          await Promise.all([
            partida.carregarPropriedades(salaId),
            partida.carregarTransacoes(salaId),
          ])
          const meuJogador = partida.jogadores.find(j => j.id === jogador.id)
          if (meuJogador) jogador.updateSaldo(meuJogador.saldo)
        }
        break

      case 'partida_encerrada':
        partida.clear()
        disconnect()
        router.push({ name: 'historico-resumo', params: { linkToken: msg.dados.link_token } })
        break
    }
  }

  return { connected, connect, disconnect }
})
