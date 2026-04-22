import { createRouter, createWebHistory } from 'vue-router'
import { useJogadorStore } from '../stores/jogadorStore'

const routes = [
  { path: '/', name: 'home', component: () => import('../views/HomeView.vue') },
  { path: '/criar', name: 'criar-sala', component: () => import('../views/CriarSalaView.vue') },
  { path: '/lobby/:salaId', name: 'lobby', component: () => import('../views/LobbyView.vue'), meta: { requiresSession: true } },
  { path: '/jogo/:salaId', name: 'dashboard', component: () => import('../views/DashboardView.vue'), meta: { requiresSession: true } },
  { path: '/jogo/:salaId/propriedades', name: 'propriedades', component: () => import('../views/PropriedadesView.vue'), meta: { requiresSession: true } },
  { path: '/jogo/:salaId/feed', name: 'feed', component: () => import('../views/FeedView.vue'), meta: { requiresSession: true } },
  { path: '/jogo/:salaId/ranking', name: 'ranking', component: () => import('../views/RankingView.vue'), meta: { requiresSession: true } },
  { path: '/jogo/:salaId/host', name: 'host', component: () => import('../views/HostView.vue'), meta: { requiresSession: true } },
  { path: '/espectador/:salaId', name: 'espectador', component: () => import('../views/EspectadorView.vue'), meta: { requiresSession: true } },
  { path: '/historico', name: 'historico-busca', component: () => import('../views/HistoricoBuscaView.vue') },
  { path: '/historico/:linkToken', name: 'historico-resumo', component: () => import('../views/HistoricoResumoView.vue') },
  { path: '/join/:linkToken', name: 'join', component: () => import('../views/HomeView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  if (to.meta.requiresSession) {
    const jogador = useJogadorStore()
    if (!jogador.sessionToken) {
      return { name: 'home' }
    }
  }
})

export default router
