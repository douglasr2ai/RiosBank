<template>
  <div class="tutorial">
    <header class="t-header">
      <div class="t-header-inner">
        <RouterLink :to="{ name: 'landing' }" class="brand">Rios<span>Bank</span></RouterLink>
        <nav class="t-nav">
          <RouterLink :to="{ name: 'regras' }" class="nav-link">Regras</RouterLink>
          <RouterLink :to="{ name: 'entrar' }" class="btn-jogar">Jogar</RouterLink>
        </nav>
      </div>
    </header>

    <section class="hero">
      <div class="container">
        <p class="kicker">Tutorial</p>
        <h1 class="title">Como usar o RiosBank</h1>
        <p class="sub">Conheça as 6 telas principais do app e para que serve cada botão. Tudo em poucos minutos — sem instalar nada.</p>
      </div>
    </section>

    <section class="container content">
      <article v-for="(tela, i) in telas" :key="tela.slug" :id="tela.slug" class="tela">
        <div class="tela-num mono">0{{ i + 1 }}</div>
        <h2 class="tela-title">{{ tela.titulo }}</h2>
        <p class="tela-desc">{{ tela.descricao }}</p>

        <div class="tela-mockup">
          <component :is="tela.componente" />
        </div>

        <dl class="tela-botoes">
          <template v-for="b in tela.botoes" :key="b.nome">
            <dt>{{ b.nome }}</dt>
            <dd>{{ b.funcao }}</dd>
          </template>
        </dl>
      </article>
    </section>

    <section class="cta-section">
      <div class="container narrow center">
        <h2 class="cta-title">Pronto para experimentar?</h2>
        <p class="cta-sub">Crie uma sala agora e compartilhe o link com seus amigos.</p>
        <RouterLink :to="{ name: 'entrar' }" class="cta-primary">Jogar agora</RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useSeoMeta } from '../composables/useSeoMeta'
import TutorialMockLobby from '../components/tutorial/TutorialMockLobby.vue'
import TutorialMockDashboard from '../components/tutorial/TutorialMockDashboard.vue'
import TutorialMockAprovacao from '../components/tutorial/TutorialMockAprovacao.vue'
import TutorialMockHost from '../components/tutorial/TutorialMockHost.vue'
import TutorialMockLeilao from '../components/tutorial/TutorialMockLeilao.vue'
import TutorialMockHistorico from '../components/tutorial/TutorialMockHistorico.vue'

const telas = [
  {
    slug: 'lobby',
    titulo: 'Lobby da sala',
    componente: TutorialMockLobby,
    descricao: 'Tela onde os jogadores aguardam o início da partida. O host vê o link de convite, expulsa quem não vai jogar e dá início quando todos estiverem prontos.',
    botoes: [
      { nome: 'Link de convite', funcao: 'Compartilhe no grupo para que os outros jogadores entrem com o próprio celular. Não precisa de cadastro.' },
      { nome: 'Lista de jogadores', funcao: 'Mostra quem está conectado em tempo real. O ponto verde indica online.' },
      { nome: 'Iniciar partida', funcao: 'Disponível apenas para o host. Só funciona com 2 ou mais jogadores online.' },
    ],
  },
  {
    slug: 'dashboard',
    titulo: 'Dashboard do jogador',
    componente: TutorialMockDashboard,
    descricao: 'Sua tela principal durante o jogo. Mostra seu saldo, o saldo dos outros e os botões de ação para registrar qualquer movimento financeiro.',
    botoes: [
      { nome: 'Transferir', funcao: 'Envia dinheiro para outro jogador. A transação só é efetivada após aprovação coletiva.' },
      { nome: 'Pagar aluguel', funcao: 'Atalho para pagar o aluguel calculado automaticamente quando você cai em um imóvel alheio.' },
      { nome: 'Comprar imóvel', funcao: 'Adquire o imóvel onde sua peça parou. Se recusar, o imóvel vai a leilão.' },
      { nome: 'Negociar', funcao: 'Inicia uma troca de imóveis e/ou dinheiro com outro jogador. Precisa do aceite dele e da aprovação dos demais.' },
    ],
  },
  {
    slug: 'aprovacao',
    titulo: 'Aprovação coletiva',
    componente: TutorialMockAprovacao,
    descricao: 'Toda transação aparece nessa tela para todos os jogadores. Cada um tem 10 segundos para votar. Sem voto conta como aprovação — o jogo não trava.',
    botoes: [
      { nome: 'Aprovar', funcao: 'Confirma que a transação é legítima. A maioria simples decide.' },
      { nome: 'Reprovar', funcao: 'Bloqueia transações erradas (valor errado, jogador errado, etc.) sem precisar discutir.' },
      { nome: 'Timer', funcao: 'Conta 10 segundos. Quando zera, o sistema decide pela maioria e libera o saldo automaticamente.' },
    ],
  },
  {
    slug: 'host',
    titulo: 'Painel do host',
    componente: TutorialMockHost,
    descricao: 'Quem cria a sala vira host. O painel concentra as ações administrativas — corrigir erros, expulsar quem não está jogando e encerrar a partida.',
    botoes: [
      { nome: 'Estornar transação', funcao: 'Reverte uma transação aprovada por engano. Gera uma nova aprovação coletiva.' },
      { nome: 'Ajustar saldo', funcao: 'Corrige saldos em caso de erro de operação fora do app (ex: ninguém votou na hora certa).' },
      { nome: 'Expulsar jogador', funcao: 'Remove alguém da partida — quem foi expulso não consegue voltar com o mesmo perfil.' },
      { nome: 'Encerrar partida', funcao: 'Finaliza o jogo e gera o histórico permanente. Use quando alguém vencer ou todos desistirem.' },
    ],
  },
  {
    slug: 'leilao',
    titulo: 'Leilão de imóveis',
    componente: TutorialMockLeilao,
    descricao: 'Quando alguém recusa comprar um imóvel ou usa a opção de leilão, todos os jogadores podem dar lances em tempo real. Tem 60 segundos para o último lance.',
    botoes: [
      { nome: 'Lance atual', funcao: 'Mostra o maior lance até o momento e quem está liderando.' },
      { nome: '+ R$ 100 / R$ 500 / R$ 1.000', funcao: 'Botões de incremento rápido. Cada lance estende o timer para garantir disputa justa.' },
      { nome: 'Timer 60s', funcao: 'Reinicia a cada lance novo. Quando zera, o líder leva o imóvel pelo valor do lance.' },
    ],
  },
  {
    slug: 'historico',
    titulo: 'Histórico da partida',
    componente: TutorialMockHistorico,
    descricao: 'Quando o host encerra a partida, todos vão para essa tela. O resumo fica acessível para sempre pelo link permanente — pode revisitar quando quiser.',
    botoes: [
      { nome: 'Pódio', funcao: 'Ranking final pelo saldo (dinheiro + imóveis). Quem zerou primeiro fica em último.' },
      { nome: 'Estatísticas', funcao: 'Maior compra, aluguel mais caro pago, número de leilões — para zoeira e revisão.' },
      { nome: 'Link permanente', funcao: 'URL fixa da partida. Compartilhe com quem perdeu pra ver o estrago.' },
    ],
  },
]

useSeoMeta({
  title: 'Tutorial do RiosBank — Como usar o banco digital do Banco Imobiliário',
  description: 'Tutorial completo das 6 telas do RiosBank: lobby, dashboard, aprovação, painel do host, leilão e histórico. Aprenda para que serve cada botão.',
  canonical: 'https://riosbank.r2pulse.com/tutorial',
  jsonLd: {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'HowTo',
        name: 'Como usar o RiosBank',
        description: 'Passo a passo das 6 telas principais do app RiosBank para partidas de Banco Imobiliário.',
        step: [
          { '@type': 'HowToStep', name: 'Lobby da sala', text: 'O host compartilha o link de convite. Os jogadores entram com o próprio celular. Quando todos estiverem online, o host inicia a partida.' },
          { '@type': 'HowToStep', name: 'Dashboard do jogador', text: 'Cada jogador vê o próprio saldo, o dos outros e os botões para transferir, pagar aluguel, comprar imóvel ou negociar.' },
          { '@type': 'HowToStep', name: 'Aprovação coletiva', text: 'Toda transação aparece para todos. Cada jogador tem 10 segundos para aprovar ou reprovar. Sem voto conta como aprovação.' },
          { '@type': 'HowToStep', name: 'Painel do host', text: 'O host pode estornar transações, ajustar saldos, expulsar jogadores e encerrar a partida.' },
          { '@type': 'HowToStep', name: 'Leilão de imóveis', text: 'Imóveis não comprados vão a leilão de 60 segundos. Todos podem dar lances com incrementos rápidos.' },
          { '@type': 'HowToStep', name: 'Histórico da partida', text: 'Ao encerrar, o ranking final, estatísticas e link permanente ficam disponíveis para todos.' },
        ],
      },
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          { '@type': 'ListItem', position: 1, name: 'Início', item: 'https://riosbank.r2pulse.com/' },
          { '@type': 'ListItem', position: 2, name: 'Tutorial', item: 'https://riosbank.r2pulse.com/tutorial' },
        ],
      },
    ],
  },
})
</script>

<style scoped>
.tutorial { min-height: 100dvh; padding-bottom: 60px; }
.container { width: 100%; max-width: 1100px; margin: 0 auto; padding: 0 24px; }
.container.narrow { max-width: 720px; }
.center { text-align: center; }

.t-header {
  position: sticky; top: 0; z-index: 50;
  background: rgba(6,14,8,.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255,255,255,.07);
}
.t-header-inner {
  max-width: 1100px; margin: 0 auto;
  padding: 0 24px;
  height: 60px;
  display: flex; align-items: center; justify-content: space-between;
}
.brand { font-size: 20px; font-weight: 800; color: var(--text); text-decoration: none; }
.brand span { color: var(--green); }
.t-nav { display: flex; align-items: center; gap: 20px; }
.nav-link { font-size: 13px; font-weight: 600; color: var(--text-2); text-decoration: none; }
.nav-link:hover { color: var(--text); }
.btn-jogar {
  background: linear-gradient(135deg, var(--green), var(--green-d));
  color: #fff;
  text-decoration: none;
  font-size: 13px; font-weight: 700;
  padding: 8px 18px; border-radius: 10px;
}

.hero { padding: 80px 0 40px; }
.kicker {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--green);
  margin-bottom: 10px;
}
.title {
  font-size: clamp(28px, 5vw, 48px);
  font-weight: 800;
  letter-spacing: -1px;
  line-height: 1.15;
  margin-bottom: 16px;
}
.sub {
  font-size: 16px; line-height: 1.65;
  color: var(--text-2);
  max-width: 600px;
}

.content { padding-top: 32px; display: flex; flex-direction: column; gap: 80px; }

.tela {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 36px;
  align-items: start;
}
.tela:nth-child(even) {
  grid-template-areas: 'mock text';
}
.tela:nth-child(even) .tela-mockup { grid-area: mock; }
.tela:nth-child(even) .tela-num,
.tela:nth-child(even) .tela-title,
.tela:nth-child(even) .tela-desc,
.tela:nth-child(even) .tela-botoes { grid-area: text; }

.tela-num {
  font-size: 13px; font-weight: 700;
  color: var(--green);
  letter-spacing: .06em;
  margin-bottom: 8px;
}
.tela-title {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -.5px;
  margin-bottom: 12px;
}
.tela-desc {
  font-size: 15px; color: var(--text-2); line-height: 1.65;
  margin-bottom: 22px;
}
.tela-mockup { max-width: 360px; justify-self: center; width: 100%; }

.tela-botoes { display: flex; flex-direction: column; gap: 12px; }
.tela-botoes dt {
  font-size: 14px; font-weight: 700; color: var(--text);
  margin-bottom: 2px;
}
.tela-botoes dd {
  font-size: 13px; color: var(--text-2); line-height: 1.6;
  margin-bottom: 4px;
}

.cta-section {
  background: rgba(46,204,113,.04);
  border-top: 1px solid rgba(46,204,113,.08);
  padding: 64px 0;
  margin-top: 40px;
}
.cta-title { font-size: clamp(24px, 4vw, 36px); font-weight: 800; letter-spacing: -.6px; margin-bottom: 10px; }
.cta-sub { font-size: 15px; color: var(--text-2); margin-bottom: 24px; }
.cta-primary {
  display: inline-flex; align-items: center;
  background: linear-gradient(135deg, var(--green), var(--green-d));
  color: #fff; text-decoration: none;
  font-size: 15px; font-weight: 700;
  padding: 14px 28px; border-radius: 14px;
  box-shadow: 0 6px 24px rgba(46,204,113,.3);
}

.mono { font-family: 'JetBrains Mono', monospace; }

@media (max-width: 760px) {
  .tela { grid-template-columns: 1fr; gap: 20px; }
  .tela:nth-child(even) { grid-template-areas: none; }
  .tela:nth-child(even) .tela-mockup,
  .tela:nth-child(even) .tela-num,
  .tela:nth-child(even) .tela-title,
  .tela:nth-child(even) .tela-desc,
  .tela:nth-child(even) .tela-botoes { grid-area: auto; }
  .content { gap: 60px; }
}
</style>
