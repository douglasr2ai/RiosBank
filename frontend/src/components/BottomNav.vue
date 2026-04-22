<template>
  <nav class="bottom-nav">
    <RouterLink :to="{ name: 'dashboard', params: { salaId } }" class="nav-item" active-class="active">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
        <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
      </svg>
      <span>Início</span>
    </RouterLink>

    <RouterLink :to="{ name: 'propriedades', params: { salaId } }" class="nav-item" active-class="active">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
      </svg>
      <span>Imóveis</span>
    </RouterLink>

    <RouterLink :to="{ name: 'feed', params: { salaId } }" class="nav-item" active-class="active">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/>
        <line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/>
        <line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/>
      </svg>
      <span>Feed</span>
    </RouterLink>

    <RouterLink :to="{ name: 'ranking', params: { salaId } }" class="nav-item" active-class="active">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
        <polyline points="17 6 23 6 23 12"/>
      </svg>
      <span>Ranking</span>
    </RouterLink>

    <RouterLink v-if="isHost" :to="{ name: 'host', params: { salaId } }" class="nav-item" active-class="active">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
      </svg>
      <span>Host</span>
    </RouterLink>
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
  position: fixed; bottom: 0; left: 0; right: 0; z-index: 50;
  height: var(--nav-h);
  display: flex; align-items: center;
  background: rgba(6, 14, 8, .92);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255,255,255,.07);
  padding: 0 8px env(safe-area-inset-bottom);
}

.nav-item {
  flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px;
  padding: 8px 4px;
  color: var(--text-2); text-decoration: none;
  font-size: 10px; font-weight: 600;
  transition: color .2s;
}
.nav-item svg { width: 20px; height: 20px; }
.nav-item.active { color: var(--green); }
</style>
