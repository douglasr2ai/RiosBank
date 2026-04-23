<template>
  <nav class="bottom-nav">
    <div class="nav-inner">
      <RouterLink :to="{ name: 'dashboard', params: { salaId } }" class="nav-item" active-class="active">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
        </svg>
        <span>Início</span>
      </RouterLink>

      <RouterLink :to="{ name: 'propriedades', params: { salaId } }" class="nav-item" active-class="active">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <rect x="1" y="3" width="15" height="13" rx="2"/><path d="M16 8h5l3 3v5h-8V8z"/>
        </svg>
        <span>Imóveis</span>
      </RouterLink>

      <RouterLink :to="{ name: 'feed', params: { salaId } }" class="nav-item" active-class="active">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
        </svg>
        <span>Feed</span>
      </RouterLink>

      <RouterLink :to="{ name: 'ranking', params: { salaId } }" class="nav-item" active-class="active">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
        </svg>
        <span>Ranking</span>
      </RouterLink>

      <RouterLink v-if="isHost" :to="{ name: 'host', params: { salaId } }" class="nav-item" active-class="active">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
        </svg>
        <span>Host</span>
      </RouterLink>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { computed } from 'vue'
import { useJogadorStore } from '../stores/jogadorStore'
import { usePartidaStore } from '../stores/partidaStore'

const props = defineProps({ salaId: String })
const jogador = useJogadorStore()
const partida = usePartidaStore()
const isHost = computed(() => partida.sala?.host_jogador_id === jogador.id)
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 50;
  display: flex;
  justify-content: center;
  padding: 0 20px calc(20px + env(safe-area-inset-bottom, 0px));
  pointer-events: none;
}

.nav-inner {
  width: 100%;
  max-width: 360px;
  background: rgba(10, 18, 12, .78);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, .10);
  border-radius: 22px;
  padding: 10px 8px;
  display: flex;
  align-items: center;
  justify-content: space-around;
  pointer-events: all;
  box-shadow: 0 8px 32px rgba(0, 0, 0, .45), inset 0 1px 0 rgba(255, 255, 255, .06);
}

.nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 6px 10px;
  border-radius: 14px;
  color: var(--text-2);
  text-decoration: none;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: .02em;
  transition: color .18s, background .18s;
}

.nav-item svg { width: 20px; height: 20px; }

.nav-item.active {
  background: var(--green-dim);
  color: var(--green);
}
</style>
