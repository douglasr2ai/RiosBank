<template>
  <div>
    <div class="bg-glow" />
    <div class="bg-noise" />
    <RouterView />
    <AprovacaoModal v-if="partida.aprovacaoPendente" />
    <LeilaoOverlay v-if="partida.leilaoAtivo" />
    <InsolvenciaModal />
    <ToastContainer />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import { useJogadorStore } from './stores/jogadorStore'
import { usePartidaStore } from './stores/partidaStore'
import { useWsStore } from './stores/wsStore'
import AprovacaoModal from './components/AprovacaoModal.vue'
import LeilaoOverlay from './components/LeilaoOverlay.vue'
import InsolvenciaModal from './components/InsolvenciaModal.vue'
import ToastContainer from './components/ToastContainer.vue'

const router = useRouter()
const jogador = useJogadorStore()
const partida = usePartidaStore()
const ws = useWsStore()

onMounted(async () => {
  if (jogador.sessionToken) {
    const result = await jogador.reconnect()
    if (result) {
      partida.setSala(result.sala)
      const salaId = result.sala.id
      const status = result.sala.status

      ws.connect(salaId, jogador.sessionToken)
      await Promise.all([
        partida.carregarPropriedades(salaId),
        partida.carregarTransacoes(salaId),
      ])

      if (status === 'lobby') {
        router.push({ name: 'lobby', params: { salaId } })
      } else if (status === 'em_andamento') {
        if (result.jogador.status === 'falido') {
          router.push({ name: 'espectador', params: { salaId } })
        } else {
          router.push({ name: 'dashboard', params: { salaId } })
        }
      }
    }
  }
})
</script>
