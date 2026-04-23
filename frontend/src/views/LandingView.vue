<template>
  <div class="landing">
    <!-- Header -->
    <header class="header" :class="{ 'header--hidden': headerHidden }">
      <div class="header-inner">
        <RouterLink :to="{ name: 'landing' }" class="brand">Rios<span>Bank</span></RouterLink>
        <nav class="header-nav">
          <RouterLink :to="{ name: 'historico-busca' }" class="nav-link">Histórico</RouterLink>
          <a
            href="https://github.com/douglasr2ai/RiosBank"
            target="_blank"
            rel="noopener noreferrer"
            class="github-link"
            title="Open source — ver repositório"
          >
            <svg viewBox="0 0 24 24" fill="currentColor" style="width:18px;height:18px">
              <path d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.009-.868-.013-1.703-2.782.605-3.369-1.342-3.369-1.342-.454-1.155-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.031 1.531 1.031.892 1.529 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.268 2.75 1.026A9.578 9.578 0 0112 6.836c.85.004 1.705.115 2.504.337 1.909-1.294 2.747-1.026 2.747-1.026.546 1.377.202 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.741 0 .267.18.578.688.48A10.012 10.012 0 0022 12c0-5.523-4.477-10-10-10z"/>
            </svg>
            <span class="github-label">Open source</span>
          </a>
          <RouterLink :to="{ name: 'entrar' }" class="btn-jogar">
            Jogar
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="width:14px;height:14px">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </RouterLink>
        </nav>
      </div>
    </header>

    <!-- Hero -->
    <section class="hero">
      <div class="container hero-inner">
        <div class="hero-badge">Super Banco Imobiliário · Digital</div>
        <h1 class="hero-title">
          O banco digital do<br />
          <span class="accent">Super Banco Imobiliário</span>
        </h1>
        <p class="hero-tagline">
          Chega de confusão com dinheiro de papel. Controle as finanças da sua partida
          no celular, em tempo real — sem cadastro, sem app para instalar.
        </p>
        <div class="hero-ctas">
          <RouterLink :to="{ name: 'entrar' }" class="cta-primary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="width:18px;height:18px">
              <path d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4M10 17l5-5-5-5M15 12H3"/>
            </svg>
            Jogar agora
          </RouterLink>
          <RouterLink :to="{ name: 'criar-sala' }" class="cta-secondary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="width:18px;height:18px">
              <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/>
            </svg>
            Criar uma sala
          </RouterLink>
        </div>
        <div class="hero-meta">
          <span>Sem cadastro</span>
          <span class="meta-dot">·</span>
          <span>Gratuito</span>
          <span class="meta-dot">·</span>
          <span>Funciona no celular</span>
          <template v-if="salasAbertas !== null">
            <span class="meta-dot">·</span>
            <span class="meta-live">
              <span class="meta-live-dot" />
              {{ salasAbertas }} sala{{ salasAbertas === 1 ? '' : 's' }} aberta{{ salasAbertas === 1 ? '' : 's' }}
            </span>
          </template>
        </div>

        <!-- Card visual decorativo -->
        <div class="hero-card glass">
          <div class="hc-row">
            <div class="hc-avatar">D</div>
            <div class="hc-info">
              <span class="hc-name">Douglas</span>
              <span class="hc-tag">você</span>
            </div>
            <span class="hc-saldo mono">R$ 12.400</span>
          </div>
          <div class="hc-divider" />
          <div class="hc-row hc-row-sm">
            <div class="hc-dot" style="background:#E91E8C" />
            <span class="hc-prop">Av. Paulista</span>
            <span class="hc-casas mono">2 casas</span>
          </div>
          <div class="hc-row hc-row-sm">
            <div class="hc-dot" style="background:#2196F3" />
            <span class="hc-prop">Av. Atlântica</span>
            <span class="hc-casas mono">hotel</span>
          </div>
          <div class="hc-tag-row">
            <span class="hc-pill green">● Conectado</span>
            <span class="hc-pill">#2 no ranking</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Como funciona -->
    <section class="section" id="como-funciona">
      <div class="container">
        <p class="section-label">Como funciona</p>
        <h2 class="section-title">Três passos para começar</h2>
        <div class="steps">
          <article class="step glass" v-for="(s, i) in steps" :key="i">
            <div class="step-num mono">0{{ i + 1 }}</div>
            <h3 class="step-heading">{{ s.title }}</h3>
            <p class="step-text">{{ s.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- Funcionalidades -->
    <section class="section section-alt" id="funcionalidades">
      <div class="container">
        <p class="section-label">Funcionalidades</p>
        <h2 class="section-title">Tudo que você precisa na partida</h2>
        <div class="features">
          <article class="feature glass" v-for="f in features" :key="f.title">
            <div class="feature-icon" :class="f.iconClass">
              <component :is="'svg'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="width:22px;height:22px" v-html="f.icon" />
            </div>
            <h3 class="feature-title">{{ f.title }}</h3>
            <p class="feature-text">{{ f.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- FAQ -->
    <section class="section" id="faq">
      <div class="container container-narrow">
        <p class="section-label">FAQ</p>
        <h2 class="section-title">Perguntas frequentes</h2>
        <div class="faq-list">
          <article
            v-for="(q, i) in faqs"
            :key="i"
            class="faq-item glass"
            @click="toggleFaq(i)"
          >
            <div class="faq-header">
              <h3 class="faq-question">{{ q.question }}</h3>
              <div class="faq-chevron" :class="{ 'faq-chevron--open': openFaq === i }">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <path d="M6 9l6 6 6-6"/>
                </svg>
              </div>
            </div>
            <p v-show="openFaq === i" class="faq-answer">{{ q.answer }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- CTA final -->
    <section class="section cta-section">
      <div class="container container-narrow cta-inner">
        <h2 class="cta-title">Pronto para jogar?</h2>
        <p class="cta-sub">Crie uma sala em segundos e compartilhe o link com seus amigos.</p>
        <div class="hero-ctas">
          <RouterLink :to="{ name: 'entrar' }" class="cta-primary">Jogar agora</RouterLink>
          <RouterLink :to="{ name: 'criar-sala' }" class="cta-secondary">Criar uma sala</RouterLink>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="container footer-inner">
        <span class="footer-brand">Rios<span>Bank</span></span>
        <nav class="footer-nav">
          <RouterLink :to="{ name: 'entrar' }" class="footer-link">Jogar</RouterLink>
          <RouterLink :to="{ name: 'criar-sala' }" class="footer-link">Criar sala</RouterLink>
          <RouterLink :to="{ name: 'historico-busca' }" class="footer-link">Histórico</RouterLink>
        </nav>
        <span class="footer-copy">© 2026 RiosBank</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { api } from '../stores/api'

const headerHidden = ref(false)
const openFaq = ref(null)
const salasAbertas = ref(null)
let lastScrollY = 0

function onScroll() {
  const currentY = window.scrollY
  headerHidden.value = currentY > lastScrollY && currentY > 80
  lastScrollY = currentY
}

function toggleFaq(i) {
  openFaq.value = openFaq.value === i ? null : i
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  api.get('/salas/stats').then(d => { salasAbertas.value = d.salas_abertas }).catch(() => {})
})
onUnmounted(() => window.removeEventListener('scroll', onScroll))

const steps = [
  {
    title: 'Crie ou entre em uma sala',
    text: 'Defina um nome e senha para a sala e escolha seu apelido. Leva menos de 30 segundos.',
  },
  {
    title: 'Convide os jogadores',
    text: 'Compartilhe o link de convite no grupo. Cada jogador entra com o próprio celular, sem instalar nada.',
  },
  {
    title: 'Jogue sem banqueiro',
    text: 'Transferências, aluguéis, compras e leilões são aprovados por todos em tempo real com timer automático.',
  },
]

const features = [
  {
    title: 'Aprovação coletiva',
    text: 'Sem banqueiro: cada transação passa por aprovação de todos os jogadores. Timer de 10 segundos — sem voto conta como aprovação.',
    iconClass: 'fi-green',
    icon: '<path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
  },
  {
    title: 'Leilão em tempo real',
    text: 'Inicie um leilão de qualquer imóvel. Todos os jogadores dão lances com incrementos de R$100, R$500 ou R$1.000 dentro de 60 segundos.',
    iconClass: 'fi-amber',
    icon: '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',
  },
  {
    title: 'Histórico da partida',
    text: 'Após encerrar a partida, o ranking final e as estatísticas ficam disponíveis pelo link de convite da sala.',
    iconClass: 'fi-blue',
    icon: '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>',
  },
  {
    title: 'Sem cadastro',
    text: 'Basta o nome da sala e a senha. Nenhuma conta, nenhum app para instalar. Funciona em qualquer celular com navegador.',
    iconClass: 'fi-purple',
    icon: '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>',
  },
]

const faqs = [
  {
    question: 'O que é o RiosBank?',
    answer: 'O RiosBank é um banco digital para partidas presenciais de Super Banco Imobiliário. Ele substitui o dinheiro de papel e o banqueiro por um sistema web em tempo real, onde todos os jogadores aprovam as transações pelo celular.',
  },
  {
    question: 'Preciso criar uma conta ou instalar um app?',
    answer: 'Não. O RiosBank funciona direto no navegador do celular, sem cadastro e sem instalação. Basta criar ou entrar em uma sala com nome e senha.',
  },
  {
    question: 'Para qual versão do Super Banco Imobiliário funciona?',
    answer: 'O RiosBank foi desenvolvido para a versão Super Banco Imobiliário (com banco eletrônico), contendo os 22 imóveis e 2 ações da versão brasileira do jogo.',
  },
  {
    question: 'Quantos jogadores podem participar de uma partida?',
    answer: 'Até 8 jogadores podem participar de uma mesma partida no RiosBank.',
  },
  {
    question: 'Como acesso o histórico depois que a partida terminar?',
    answer: 'O link de convite da sala dá acesso ao resumo completo da partida após o encerramento, com ranking final, saldos e estatísticas de transações. Guarde o link ou a senha da sala.',
  },
]
</script>

<style scoped>
/* ── Layout base ─────────────────────────────────────────── */
.landing { min-height: 100dvh; }

.container {
  width: 100%; max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
}
.container-narrow { max-width: 720px; }

/* ── Header ──────────────────────────────────────────────── */
.header {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  background: rgba(6, 14, 8, .85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255,255,255,.07);
  transition: transform .3s ease;
}
.header--hidden { transform: translateY(-100%); }

.header-inner {
  max-width: 1100px; margin: 0 auto;
  padding: 0 24px;
  height: 60px;
  display: flex; align-items: center; justify-content: space-between;
}

.brand {
  font-size: 20px; font-weight: 800; letter-spacing: -.5px;
  color: var(--text); text-decoration: none;
}
.brand span, .footer-brand span { color: var(--green); }

.header-nav { display: flex; align-items: center; gap: 24px; }

.nav-link {
  font-size: 13px; font-weight: 600; color: var(--text-2);
  text-decoration: none; transition: color .2s;
}
.nav-link:hover { color: var(--text); }

.github-link {
  display: flex; align-items: center; gap: 6px;
  color: var(--text-2); text-decoration: none;
  font-size: 12px; font-weight: 600;
  transition: color .2s;
}
.github-link:hover { color: var(--text); }
.github-label { letter-spacing: .02em; }

.btn-jogar {
  display: flex; align-items: center; gap: 6px;
  background: linear-gradient(135deg, var(--green), var(--green-d));
  color: #fff; text-decoration: none;
  font-size: 13px; font-weight: 700; font-family: 'Manrope', sans-serif;
  padding: 8px 18px; border-radius: 10px;
  box-shadow: 0 4px 16px rgba(46,204,113,.25);
  transition: filter .2s;
}
.btn-jogar:hover { filter: brightness(1.08); }

/* ── Hero ────────────────────────────────────────────────── */
.hero {
  padding: 140px 0 100px;
  position: relative; overflow: hidden;
}
.hero-inner {
  display: flex; flex-direction: column; align-items: center;
  text-align: center; gap: 0;
}

.hero-badge {
  display: inline-flex; align-items: center;
  background: var(--green-dim); border: 1px solid rgba(46,204,113,.25);
  border-radius: 999px; padding: 6px 16px;
  font-size: 11px; font-weight: 700; font-family: 'JetBrains Mono', monospace;
  color: var(--green); letter-spacing: .08em; text-transform: uppercase;
  margin-bottom: 28px;
  animation: fadeInUp .6s ease both;
}

.hero-title {
  font-size: clamp(32px, 6vw, 60px);
  font-weight: 800; line-height: 1.12;
  letter-spacing: -1.5px; margin-bottom: 20px;
  animation: fadeInUp .6s .1s ease both;
}
.accent { color: var(--green); }

.hero-tagline {
  font-size: clamp(15px, 2vw, 18px);
  color: var(--text-2); line-height: 1.65;
  max-width: 560px; margin-bottom: 36px;
  animation: fadeInUp .6s .2s ease both;
}

.hero-ctas {
  display: flex; flex-wrap: wrap; gap: 12px; justify-content: center;
  margin-bottom: 24px;
  animation: fadeInUp .6s .3s ease both;
}

.cta-primary {
  display: inline-flex; align-items: center; gap: 8px;
  background: linear-gradient(135deg, var(--green), var(--green-d));
  color: #fff; text-decoration: none;
  font-size: 15px; font-weight: 700; font-family: 'Manrope', sans-serif;
  padding: 14px 28px; border-radius: 14px;
  box-shadow: 0 6px 24px rgba(46,204,113,.3), inset 0 1px 0 rgba(255,255,255,.2);
  transition: filter .2s, transform .1s;
}
.cta-primary:hover { filter: brightness(1.07); }
.cta-primary:active { transform: scale(.97); }

.cta-secondary {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.12);
  color: var(--text); text-decoration: none;
  font-size: 15px; font-weight: 700; font-family: 'Manrope', sans-serif;
  padding: 14px 28px; border-radius: 14px;
  transition: background .2s, transform .1s;
}
.cta-secondary:hover { background: rgba(255,255,255,.1); }
.cta-secondary:active { transform: scale(.97); }

.hero-meta {
  display: flex; align-items: center; gap: 10px;
  font-size: 12px; font-weight: 600; color: var(--text-2);
  margin-bottom: 52px;
  animation: fadeInUp .6s .35s ease both;
}
.meta-dot { opacity: .4; }

.meta-live { display: inline-flex; align-items: center; gap: 5px; color: var(--green); font-weight: 700; }
.meta-live-dot {
  width: 6px; height: 6px; border-radius: 50%; background: var(--green);
  box-shadow: 0 0 6px var(--green);
  animation: pulse-live 2s ease-in-out infinite;
}
@keyframes pulse-live {
  0%, 100% { opacity: 1; }
  50% { opacity: .35; }
}

/* Hero card decorativo */
.hero-card {
  width: 100%; max-width: 340px;
  padding: 20px; border-radius: 20px;
  display: flex; flex-direction: column; gap: 12px;
  animation: fadeInUp .7s .45s ease both;
}
.hc-row { display: flex; align-items: center; gap: 10px; }
.hc-row-sm { gap: 8px; }
.hc-avatar {
  width: 36px; height: 36px; border-radius: 50%; flex-shrink: 0;
  background: var(--green-dim); border: 1px solid rgba(46,204,113,.3);
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 700; color: var(--green);
}
.hc-info { flex: 1; display: flex; align-items: center; gap: 8px; }
.hc-name { font-size: 14px; font-weight: 700; }
.hc-tag {
  font-size: 9px; font-weight: 700; font-family: 'JetBrains Mono', monospace;
  background: rgba(255,255,255,.07); border-radius: 4px; padding: 1px 6px; color: var(--text-2);
}
.hc-saldo { font-size: 16px; font-weight: 700; color: var(--green); }
.hc-divider { height: 1px; background: rgba(255,255,255,.07); }
.hc-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.hc-prop { flex: 1; font-size: 13px; font-weight: 600; }
.hc-casas { font-size: 11px; color: var(--text-2); }
.hc-tag-row { display: flex; gap: 8px; flex-wrap: wrap; }
.hc-pill {
  font-size: 10px; font-weight: 600; font-family: 'JetBrains Mono', monospace;
  background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.1);
  border-radius: 999px; padding: 3px 10px; color: var(--text-2);
}
.hc-pill.green { background: var(--green-dim); border-color: rgba(46,204,113,.25); color: var(--green); }

/* ── Seções genéricas ────────────────────────────────────── */
.section { padding: 96px 0; }
.section-alt { background: rgba(255,255,255,.02); }

.section-label {
  font-size: 11px; font-family: 'JetBrains Mono', monospace;
  font-weight: 600; letter-spacing: .14em; text-transform: uppercase;
  color: var(--green); margin-bottom: 12px;
}
.section-title {
  font-size: clamp(24px, 4vw, 40px);
  font-weight: 800; letter-spacing: -.8px;
  margin-bottom: 48px; line-height: 1.15;
}

/* ── Steps ───────────────────────────────────────────────── */
.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}
.step {
  padding: 28px; border-radius: 20px;
  display: flex; flex-direction: column; gap: 12px;
}
.step-num {
  font-size: 13px; font-weight: 700; color: var(--green);
  letter-spacing: .06em;
}
.step-heading { font-size: 17px; font-weight: 700; }
.step-text { font-size: 14px; color: var(--text-2); line-height: 1.6; }

/* ── Features ────────────────────────────────────────────── */
.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}
.feature {
  padding: 28px; border-radius: 20px;
  display: flex; flex-direction: column; gap: 14px;
}
.feature-icon {
  width: 48px; height: 48px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.fi-green { background: rgba(46,204,113,.15); color: var(--green); }
.fi-amber { background: rgba(246,173,85,.15); color: var(--amber); }
.fi-blue  { background: rgba(99,179,237,.15);  color: var(--blue); }
.fi-purple{ background: rgba(156,39,176,.15);  color: #CE93D8; }
.feature-title { font-size: 17px; font-weight: 700; }
.feature-text  { font-size: 14px; color: var(--text-2); line-height: 1.6; }

/* ── FAQ ─────────────────────────────────────────────────── */
.faq-list { display: flex; flex-direction: column; gap: 8px; }
.faq-item {
  padding: 20px 22px; border-radius: 16px; cursor: pointer;
  transition: border-color .2s;
}
.faq-item:hover { border-color: rgba(46,204,113,.2); }
.faq-header { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
.faq-question { font-size: 15px; font-weight: 700; line-height: 1.4; }
.faq-chevron { color: var(--text-2); flex-shrink: 0; transition: transform .25s ease; }
.faq-chevron svg { width: 18px; height: 18px; display: block; }
.faq-chevron--open { transform: rotate(180deg); color: var(--green); }
.faq-answer {
  font-size: 14px; color: var(--text-2); line-height: 1.65;
  margin-top: 14px; padding-top: 14px;
  border-top: 1px solid rgba(255,255,255,.07);
}

/* ── CTA final ───────────────────────────────────────────── */
.cta-section { background: rgba(46,204,113,.04); border-top: 1px solid rgba(46,204,113,.08); border-bottom: 1px solid rgba(46,204,113,.08); }
.cta-inner { text-align: center; }
.cta-title { font-size: clamp(26px, 4vw, 40px); font-weight: 800; letter-spacing: -.8px; margin-bottom: 12px; }
.cta-sub { font-size: 16px; color: var(--text-2); margin-bottom: 36px; }

/* ── Footer ──────────────────────────────────────────────── */
.footer { border-top: 1px solid rgba(255,255,255,.07); padding: 32px 0; }
.footer-inner {
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 16px;
}
.footer-brand { font-size: 16px; font-weight: 800; color: var(--text); }
.footer-nav { display: flex; gap: 24px; }
.footer-link {
  font-size: 13px; font-weight: 600; color: var(--text-2);
  text-decoration: none; transition: color .2s;
}
.footer-link:hover { color: var(--text); }
.footer-copy { font-size: 12px; color: var(--text-2); opacity: .6; }

/* ── Animações ───────────────────────────────────────────── */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Responsivo mobile ───────────────────────────────────── */
@media (max-width: 640px) {
  .hero { padding: 100px 0 72px; }
  .section { padding: 72px 0; }
  .section-title { margin-bottom: 32px; }
  .nav-link { display: none; }
  .github-label { display: none; }
  .hero-ctas { flex-direction: column; align-items: stretch; }
  .cta-primary, .cta-secondary { justify-content: center; }
  .footer-inner { flex-direction: column; align-items: flex-start; gap: 12px; }
  .footer-nav { flex-wrap: wrap; gap: 16px; }
}
</style>
