<template>
  <div class="regras">
    <header class="r-header">
      <div class="r-header-inner">
        <RouterLink :to="{ name: 'landing' }" class="brand">Rios<span>Bank</span></RouterLink>
        <nav class="r-nav">
          <RouterLink :to="{ name: 'tutorial' }" class="nav-link">Tutorial</RouterLink>
          <RouterLink :to="{ name: 'entrar' }" class="btn-jogar">Jogar</RouterLink>
        </nav>
      </div>
    </header>

    <section class="hero">
      <div class="container">
        <p class="kicker">Regras do jogo</p>
        <h1 class="title">Regras do Banco Imobiliário</h1>
        <p class="sub">Guia completo do Super Banco Imobiliário: do objetivo do jogo até a falência. Use o RiosBank para substituir o dinheiro de papel e o banqueiro — sem instalar nada.</p>
        <div class="cta-strip">
          <span>Quer pular o banqueiro?</span>
          <RouterLink :to="{ name: 'entrar' }" class="cta-inline">Jogar com o RiosBank →</RouterLink>
        </div>
      </div>
    </section>

    <section class="container content">
      <article id="objetivo">
        <h2>1. Objetivo do jogo</h2>
        <p>O Banco Imobiliário é um jogo de tabuleiro em que cada jogador percorre as casas, compra imóveis, cobra aluguéis e busca levar os adversários à falência. <strong>Vence o último jogador que ainda tiver patrimônio positivo</strong> — todos os outros precisam ter declarado falência.</p>
        <p>A jornada do dinheiro envolve compra de propriedades, construção de casas e hotéis, leilões, hipotecas e cartas de Sorte e Revés. O ritmo é alto: uma única jogada pode mudar todo o equilíbrio.</p>
      </article>

      <article id="preparacao">
        <h2>2. Preparação</h2>
        <p>Antes de começar:</p>
        <ul>
          <li>Monte o tabuleiro e separe as cartas de Sorte/Revés e os títulos de propriedade.</li>
          <li>Cada jogador escolhe um peão.</li>
          <li>Cada jogador recebe um valor inicial em dinheiro (R$ 30.000 na versão Super Banco Imobiliário).</li>
          <li>Defina quem será o banqueiro — ou use o RiosBank para que essa função fique automática.</li>
        </ul>
        <div class="cta-card">
          <h3>O RiosBank substitui o banqueiro</h3>
          <p>Nenhum jogador precisa controlar o caixa. Cada transação é aprovada por todos em tempo real, e o app calcula aluguéis, leilões e falências automaticamente.</p>
          <RouterLink :to="{ name: 'entrar' }" class="cta-card-btn">Criar sala →</RouterLink>
        </div>
      </article>

      <article id="turno">
        <h2>3. Como jogar um turno</h2>
        <p>O turno mais jovem começa. Em ordem horária, cada jogador:</p>
        <ol>
          <li>Joga os dois dados e move o peão a quantidade de casas indicada.</li>
          <li>Aplica o efeito da casa onde parou (comprar imóvel, pagar aluguel, sacar carta, ir para a Cadeia, etc.).</li>
          <li>Pode comprar casas/hotéis, hipotecar imóveis ou negociar com outros jogadores antes de passar a vez.</li>
        </ol>
        <p><strong>Bônus do dado duplo:</strong> se tirar dois números iguais, jogue de novo. Três duplas seguidas mandam o jogador direto para a Cadeia.</p>
      </article>

      <article id="compra">
        <h2>4. Compra de imóveis</h2>
        <p>Ao cair em um imóvel <strong>sem dono</strong>, o jogador tem duas opções:</p>
        <ul>
          <li><strong>Comprar</strong> pelo valor indicado no tabuleiro. Recebe o título de propriedade e passa a cobrar aluguel de quem cair ali.</li>
          <li><strong>Recusar</strong>. O imóvel vai automaticamente a leilão entre todos os jogadores, incluindo quem recusou.</li>
        </ul>
        <p>No RiosBank, a opção aparece no Dashboard. Se você recusar, o leilão começa imediatamente para todos.</p>
      </article>

      <article id="alugueis">
        <h2>5. Aluguéis</h2>
        <p>Quem cai em imóvel alheio paga aluguel ao dono. O valor depende de quantas casas estão construídas:</p>
        <ul>
          <li><strong>Sem casa</strong>: aluguel base do título.</li>
          <li><strong>1 a 4 casas</strong>: valor crescente conforme indicado no título.</li>
          <li><strong>Hotel</strong>: valor máximo.</li>
          <li><strong>Monopólio sem construção</strong>: aluguel base é dobrado.</li>
          <li><strong>Imóvel hipotecado</strong>: dono não cobra aluguel.</li>
        </ul>
        <p>Companhias (luz, telefone) e estações cobram conforme regra própria — geralmente um múltiplo do dado tirado pelo devedor.</p>
      </article>

      <article id="construcao">
        <h2>6. Construção (casas e hotéis)</h2>
        <p>Para construir, o jogador precisa <strong>possuir todos os imóveis do mesmo grupo de cor</strong> (monopólio). Aí pode comprar casas pelo valor indicado no título.</p>
        <p><strong>Regra do uniforme:</strong> a construção deve ser distribuída por igual dentro do grupo. Não dá pra ter 3 casas em um e 0 em outro do mesmo grupo. A diferença máxima é de 1 casa.</p>
        <p>Quando todas as propriedades do grupo tiverem 4 casas, é possível trocar as 4 casas por 1 hotel — pagando a diferença ao banco.</p>
      </article>

      <article id="hipoteca">
        <h2>7. Hipoteca e desipoteca</h2>
        <p>Sem dinheiro? Hipoteque um imóvel para receber metade do valor de compra. Enquanto hipotecado:</p>
        <ul>
          <li>O imóvel não cobra aluguel.</li>
          <li>Não pode receber casas ou hotéis.</li>
          <li>Continua sendo seu — outros jogadores não podem cair e comprar.</li>
        </ul>
        <p>Para desipotecar, pague o valor da hipoteca + 10% de juros ao banco.</p>
      </article>

      <article id="sorte-cadeia">
        <h2>8. Cartas de Sorte/Revés e Cadeia</h2>
        <p>Casas marcadas com "?" mandam o jogador sacar uma carta de Sorte ou Revés. As cartas podem dar dinheiro, cobrar uma taxa, mover o peão ou mandar direto para a Cadeia.</p>
        <p><strong>Cadeia:</strong> para sair, escolha uma das opções:</p>
        <ul>
          <li>Pagar a multa imediatamente (R$ 500).</li>
          <li>Jogar os dados e tentar tirar uma dupla nas próximas 3 jogadas.</li>
          <li>Usar uma carta "Saída livre da prisão", se tiver.</li>
        </ul>
        <p>Mesmo na cadeia, o jogador continua cobrando aluguéis e participando de leilões.</p>
      </article>

      <article id="leilao">
        <h2>9. Leilão</h2>
        <p>O leilão acontece quando alguém recusa comprar um imóvel. Todos os jogadores (incluindo quem recusou) podem dar lances. O imóvel vai para quem oferecer o maior valor — não existe lance mínimo nas regras oficiais, mas no RiosBank o lance inicial parte de R$ 100 para evitar abuso.</p>
        <p>No RiosBank, o leilão tem um timer de 60 segundos que reinicia a cada novo lance. Isso garante que ninguém fique esperando indefinidamente.</p>
      </article>

      <article id="falencia">
        <h2>10. Falência e fim de jogo</h2>
        <p>Um jogador declara <strong>falência</strong> quando não consegue pagar uma dívida (aluguel, taxa, hipoteca). Ele liquida tudo que tem:</p>
        <ul>
          <li>Se a dívida é com outro jogador: o credor fica com todos os imóveis e o que sobrar do caixa.</li>
          <li>Se a dívida é com o banco: tudo volta ao banco e os imóveis vão a leilão.</li>
        </ul>
        <p>O jogo termina quando <strong>resta apenas um jogador solvente</strong>. Esse é o vencedor.</p>
      </article>

      <div class="cta-final">
        <h2>Pronto para jogar?</h2>
        <p>Crie uma sala e jogue com seus amigos em segundos. Sem cadastro, sem app pra instalar.</p>
        <RouterLink :to="{ name: 'entrar' }" class="cta-primary">Jogar agora</RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useSeoMeta } from '../composables/useSeoMeta'

useSeoMeta({
  title: 'Regras do Banco Imobiliário — Guia completo | RiosBank',
  description: 'Guia completo das regras do Banco Imobiliário: objetivo, preparação, turno, compra, aluguéis, construção, hipoteca, leilão e falência. Tudo em uma página.',
  canonical: 'https://riosbank.r2pulse.com/regras',
  jsonLd: {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Article',
        headline: 'Regras do Banco Imobiliário — Guia completo',
        author: { '@type': 'Organization', name: 'RiosBank' },
        publisher: { '@type': 'Organization', name: 'RiosBank' },
        datePublished: '2026-05-18',
        inLanguage: 'pt-BR',
        mainEntityOfPage: 'https://riosbank.r2pulse.com/regras',
      },
      {
        '@type': 'HowTo',
        name: 'Como jogar Banco Imobiliário',
        description: 'Passo a passo das regras do Banco Imobiliário, do início ao fim da partida.',
        step: [
          { '@type': 'HowToStep', name: 'Objetivo do jogo', text: 'Levar todos os adversários à falência. O último jogador solvente vence.' },
          { '@type': 'HowToStep', name: 'Preparação', text: 'Cada jogador recebe R$ 30.000 e escolhe um peão. Defina o banqueiro ou use o RiosBank para automatizar.' },
          { '@type': 'HowToStep', name: 'Turno', text: 'Joga os dados, move o peão, aplica o efeito da casa. Pode comprar, hipotecar ou negociar antes de passar a vez.' },
          { '@type': 'HowToStep', name: 'Compra de imóveis', text: 'Ao cair em imóvel sem dono, pode comprar pelo valor do título ou recusar — nesse caso, o imóvel vai a leilão.' },
          { '@type': 'HowToStep', name: 'Aluguéis', text: 'Quem cai em imóvel alheio paga aluguel ao dono. O valor cresce com casas e hotéis.' },
          { '@type': 'HowToStep', name: 'Construção', text: 'Com monopólio do grupo de cor, pode construir casas e hotéis. Construção deve ser uniforme dentro do grupo.' },
          { '@type': 'HowToStep', name: 'Hipoteca', text: 'Hipoteque um imóvel para receber metade do valor. Não cobra aluguel enquanto hipotecado.' },
          { '@type': 'HowToStep', name: 'Sorte/Revés e Cadeia', text: 'Cartas surpresa podem dar dinheiro, cobrar taxa ou mandar pra Cadeia. Pra sair, pague multa ou tire dupla.' },
          { '@type': 'HowToStep', name: 'Leilão', text: 'Imóveis recusados vão a leilão entre todos os jogadores. No RiosBank, timer de 60s reinicia a cada lance.' },
          { '@type': 'HowToStep', name: 'Falência e fim de jogo', text: 'Quem não consegue pagar uma dívida declara falência. O último jogador solvente vence.' },
        ],
      },
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          { '@type': 'ListItem', position: 1, name: 'Início', item: 'https://riosbank.r2pulse.com/' },
          { '@type': 'ListItem', position: 2, name: 'Regras', item: 'https://riosbank.r2pulse.com/regras' },
        ],
      },
    ],
  },
})
</script>

<style scoped>
.regras { min-height: 100dvh; padding-bottom: 60px; }
.container { width: 100%; max-width: 760px; margin: 0 auto; padding: 0 24px; }

.r-header {
  position: sticky; top: 0; z-index: 50;
  background: rgba(6,14,8,.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255,255,255,.07);
}
.r-header-inner {
  max-width: 1100px; margin: 0 auto;
  padding: 0 24px;
  height: 60px;
  display: flex; align-items: center; justify-content: space-between;
}
.brand { font-size: 20px; font-weight: 800; color: var(--text); text-decoration: none; }
.brand span { color: var(--green); }
.r-nav { display: flex; align-items: center; gap: 20px; }
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
  font-size: clamp(28px, 5vw, 44px);
  font-weight: 800;
  letter-spacing: -1px;
  line-height: 1.15;
  margin-bottom: 16px;
}
.sub {
  font-size: 16px; line-height: 1.65;
  color: var(--text-2);
  max-width: 600px;
  margin-bottom: 22px;
}
.cta-strip {
  display: inline-flex; align-items: center; gap: 12px;
  background: var(--green-dim);
  border: 1px solid rgba(46,204,113,.2);
  border-radius: 999px;
  padding: 8px 16px;
  font-size: 13px;
  color: var(--text);
}
.cta-inline {
  font-weight: 700;
  color: var(--green);
  text-decoration: none;
}

.content { padding-top: 32px; display: flex; flex-direction: column; gap: 40px; }

article h2 {
  font-size: 22px; font-weight: 800;
  letter-spacing: -.4px;
  margin-bottom: 14px;
  color: var(--text);
}
article h3 {
  font-size: 16px; font-weight: 700;
  margin-bottom: 6px;
}
article p {
  font-size: 15px;
  color: var(--text-2);
  line-height: 1.7;
  margin-bottom: 12px;
}
article p strong { color: var(--text); font-weight: 700; }
article ul, article ol {
  font-size: 15px;
  color: var(--text-2);
  line-height: 1.7;
  margin: 0 0 12px 22px;
}
article li { margin-bottom: 4px; }
article li strong { color: var(--text); font-weight: 700; }

.cta-card {
  background: var(--green-dim);
  border: 1px solid rgba(46,204,113,.25);
  border-radius: 16px;
  padding: 20px;
  margin: 18px 0;
}
.cta-card h3 { color: var(--green); }
.cta-card p { color: var(--text); }
.cta-card-btn {
  display: inline-block;
  margin-top: 8px;
  background: linear-gradient(135deg, var(--green), var(--green-d));
  color: #fff;
  text-decoration: none;
  font-size: 13px;
  font-weight: 700;
  padding: 10px 18px;
  border-radius: 10px;
}

.cta-final {
  background: rgba(46,204,113,.04);
  border: 1px solid rgba(46,204,113,.08);
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  margin-top: 24px;
}
.cta-final h2 { font-size: 24px; margin-bottom: 6px; }
.cta-final p { margin-bottom: 18px; }
.cta-primary {
  display: inline-block;
  background: linear-gradient(135deg, var(--green), var(--green-d));
  color: #fff;
  text-decoration: none;
  font-size: 15px;
  font-weight: 700;
  padding: 14px 28px;
  border-radius: 14px;
}
</style>
