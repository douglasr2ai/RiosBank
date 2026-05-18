<template>
  <div class="mock mock-historico">
    <div class="hdr">
      <span class="hdr-pre">HISTÓRICO DE PARTIDA</span>
      <span class="hdr-title">Reis do Tabuleiro</span>
      <span class="hdr-sub">Duração 1h 24min · 87 transações</span>
    </div>

    <div class="podium">
      <div class="pod second">
        <span class="pos">2º</span>
        <span class="nm">Douglas</span>
        <span class="bal mono">R$ 9.400</span>
      </div>
      <div class="pod first">
        <span class="pos">🏆 1º</span>
        <span class="nm">Marina</span>
        <span class="bal mono">R$ 18.250</span>
      </div>
      <div class="pod third">
        <span class="pos">3º</span>
        <span class="nm">Rafael</span>
        <span class="bal mono">R$ 0</span>
      </div>
    </div>

    <div class="stats">
      <div class="stat"><span class="s-label">Maior compra</span><span class="s-value mono">R$ 5.200</span></div>
      <div class="stat"><span class="s-label">Aluguel + caro</span><span class="s-value mono">R$ 2.800</span></div>
      <div class="stat"><span class="s-label">Leilões</span><span class="s-value mono">3</span></div>
    </div>

    <div class="share">
      <span class="share-label">Link permanente desta partida</span>
      <span class="share-value mono">riosbank.r2pulse.com/historico/…</span>
    </div>

    <template v-if="annotations">
      <span
        v-for="a in annotations"
        :key="a.label"
        class="annotation"
        :style="a.position"
      >{{ a.label }}</span>
    </template>
  </div>
</template>

<script setup>
defineProps({ annotations: { type: Array, default: null } })
</script>

<style scoped>
.mock {
  position: relative;
  background: var(--glass-bg);
  border: 1px solid var(--glass-br);
  border-radius: 18px;
  padding: 18px;
  font-family: 'Manrope', sans-serif;
  color: var(--text);
  display: flex; flex-direction: column; gap: 14px;
}
.hdr { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.hdr-pre {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  letter-spacing: .14em;
  color: var(--green);
}
.hdr-title { font-size: 16px; font-weight: 800; }
.hdr-sub { font-size: 11px; color: var(--text-2); }
.podium {
  display: grid;
  grid-template-columns: 1fr 1.2fr 1fr;
  gap: 6px;
  align-items: end;
}
.pod {
  background: rgba(255,255,255,.03);
  border-radius: 10px;
  padding: 10px 6px;
  display: flex; flex-direction: column; align-items: center; gap: 3px;
}
.pod.first { background: var(--green-dim); border: 1px solid rgba(46,204,113,.3); }
.pos { font-size: 12px; font-weight: 800; color: var(--text-2); }
.pod.first .pos { color: var(--green); }
.nm { font-size: 12px; font-weight: 700; }
.bal { font-size: 11px; color: var(--text-2); }
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
.stat {
  background: rgba(255,255,255,.03);
  border-radius: 8px;
  padding: 6px;
  display: flex; flex-direction: column; align-items: center; gap: 2px;
}
.s-label { font-size: 9px; color: var(--text-2); letter-spacing: .08em; text-transform: uppercase; }
.s-value { font-size: 12px; font-weight: 700; color: var(--text); }
.share {
  background: rgba(46,204,113,.06);
  border: 1px solid rgba(46,204,113,.18);
  border-radius: 10px;
  padding: 10px;
  display: flex; flex-direction: column; gap: 3px;
}
.share-label { font-size: 10px; color: var(--green); text-transform: uppercase; letter-spacing: .1em; }
.share-value { font-size: 11px; color: var(--text); word-break: break-all; }
.annotation {
  position: absolute;
  background: var(--green);
  color: #06140E;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  pointer-events: none;
  white-space: nowrap;
}
.mono { font-family: 'JetBrains Mono', monospace; }
</style>
